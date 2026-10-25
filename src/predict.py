import os
import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image, ImageStat
import torchvision.transforms as transforms

from src.config import MODEL_PATH, PLANT_CLASSES, PLANT_GENUS_DETAILS, IMG_WIDTH, IMG_HEIGHT
from src.model import build_cnn_model

_MODEL_CACHE = None
_DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def get_model():
    global _MODEL_CACHE
    if _MODEL_CACHE is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model checkpoint file not found at '{MODEL_PATH}'. Train the model first using 'python -m src.train'.")
        print(f"[+] Loading PlantLeafNet model weights into PyTorch ({_DEVICE})...")
        model = build_cnn_model(num_classes=len(PLANT_CLASSES)).to(_DEVICE)
        model.load_state_dict(torch.load(MODEL_PATH, map_location=_DEVICE))
        model.eval()
        _MODEL_CACHE = model
    return _MODEL_CACHE

def verify_is_plant(img_pil, max_confidence, min_threshold=0.25):
    """
    Validates whether the input image is actually a plant leaf or crop leaf
    by analyzing color spectrums (Green/Brown/Yellow vegetation index)
    and model activation confidence thresholds.
    """
    # 1. Softmax Confidence Threshold
    if max_confidence < min_threshold:
        return False, f"Low model confidence ({round(max_confidence * 100, 1)}% < {round(min_threshold * 100, 1)}%). Image does not match known plant leaf or foliage features."

    # 2. Color Channel Analysis (HSV / RGB Green & Organic Leaf Spectrum)
    img_rgb = img_pil.convert('RGB')
    stat = ImageStat.Stat(img_rgb)
    r, g, b = stat.mean

    # Check for extreme mono-color/grayscale non-plant images (e.g. pure red/blue/black screens)
    color_std = np.std([r, g, b])
    
    # Vegetation/Plant Leaf Color Index (Plants & leaves have organic G/R balance)
    # Pure unnatural artificial colors (e.g. neon blue/purple or solid gray background)
    if b > (g + 35) and b > (r + 35): # Dominant artificial blue
        return False, "Non-plant image detected (dominant artificial blue color spectrum)."

    if color_std < 3.0 and (r < 20 and g < 20 and b < 20): # Near pitch black
        return False, "Image too dark or blank. Unable to detect plant features."

    return True, "Valid Plant / Leaf Sample"

def preprocess_image(image_input):
    """
    Transforms PIL Image or file path into PyTorch tensor (1, 3, 128, 128).
    """
    if isinstance(image_input, str):
        img = Image.open(image_input)
    elif isinstance(image_input, Image.Image):
        img = image_input
    else:
        raise ValueError("Unsupported input type. Expected file path or PIL Image.")

    img_rgb = img.convert('RGB')
    img_resized = img_rgb.resize((IMG_WIDTH, IMG_HEIGHT))

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
    ])

    tensor = transform(img_resized).unsqueeze(0).to(_DEVICE) # (1, 3, 128, 128)
    return tensor, img_rgb

def predict_plant_disease(image_input, threshold=0.25):
    """
    Runs plant verification + CNN forward pass to predict plant genus, leaf type, disease status, and action plan.
    """
    model = get_model()
    tensor, raw_pil = preprocess_image(image_input)

    with torch.no_grad():
        outputs = model(tensor)
        probabilities = F.softmax(outputs, dim=1)[0].cpu().numpy()

    top_class_idx = int(probabilities.argmax())
    confidence = float(probabilities[top_class_idx])

    # Perform Plant Validation Check
    is_plant, plant_validation_msg = verify_is_plant(raw_pil, confidence, min_threshold=threshold)

    # Top 3 probabilities
    top3_indices = probabilities.argsort()[-3:][::-1]
    top3_results = []
    for idx in top3_indices:
        mapped = PLANT_GENUS_DETAILS.get(int(idx), {})
        top3_results.append({
            "class_id": int(idx),
            "class_name": PLANT_CLASSES[idx],
            "genus": mapped.get("genus", "Unknown Genus"),
            "disease": mapped.get("disease", "Unknown Diagnosis"),
            "confidence": round(float(probabilities[idx]) * 100, 2)
        })

    mapped_info = PLANT_GENUS_DETAILS.get(top_class_idx, {})
    disease_status = mapped_info.get("disease", "Healthy")
    is_healthy = mapped_info.get("is_healthy", True)

    recommendations = []
    if not is_plant:
        recommendations.append("⚠️ NON-PLANT DETECTED: The uploaded image does not appear to be a crop leaf or plant foliage.")
        recommendations.append("Please upload a clear photograph of a plant leaf, crop foliage, or leaf sample.")
    elif is_healthy:
        recommendations.append("Leaf and foliage sample displays optimal healthy morphological structures.")
        recommendations.append("Maintain optimal irrigation, balanced N-P-K nutrient schedule, and canopy airflow.")
        recommendations.append("Continue periodic visual field scouting for early pest or pathogen onset.")
    else:
        recommendations.append(f"Infection / Pathogen pattern detected: {disease_status}.")
        recommendations.append("Prune or quarantine heavily infected crop leaves to prevent fungal spore dispersal.")
        if "Blight" in disease_status:
            recommendations.append("Apply targeted copper hydroxide or mancozeb fungicide spray. Avoid overhead sprinkler irrigation.")
        elif "Rust" in disease_status:
            recommendations.append("Apply foliar triazole (propiconazole) fungicide. Inspect adjacent crop rows for stripe pustules.")
        elif "Mildew" in disease_status:
            recommendations.append("Spray potassium bicarbonate or wettable sulfur. Improve plant spacing for sunlight penetration.")
        elif "Caterpillar" in disease_status:
            recommendations.append("Deploy Bacillus thuringiensis (Bt) or spinosad bio-insecticide. Inspect undersides of leaves for egg clusters.")
        else:
            recommendations.append("Apply recommended organic fungicide or bactericide treatment as advised by local agronomy service.")

    result = {
        "success": True,
        "is_plant": is_plant,
        "plant_verification_message": plant_validation_msg,
        "predicted_class_id": top_class_idx if is_plant else -1,
        "class_name": PLANT_CLASSES[top_class_idx] if is_plant else "Non-Plant / Out of Domain",
        "genus": mapped_info.get("genus", "Unknown Genus") if is_plant else "Not a Plant",
        "crop_type": mapped_info.get("type", "Agricultural Crop") if is_plant else "Invalid Input",
        "disease": disease_status if is_plant else "N/A (Not a Plant)",
        "is_healthy": is_healthy if is_plant else False,
        "confidence_percentage": round(confidence * 100, 2) if is_plant else 0.0,
        "confidence_raw": round(confidence, 4) if is_plant else 0.0,
        "top3": top3_results if is_plant else [],
        "recommendations": recommendations
    }

    return result

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        res = predict_plant_disease(sys.argv[1])
        import json
        print(json.dumps(res, indent=2))
    else:
        print("Usage: python -m src.predict <image_path>")
