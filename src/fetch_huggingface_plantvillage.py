import os
import shutil
from PIL import Image

from src.config import DATA_DIR, PLANT_CLASSES

CLASS_MAP = {
    "Tomato___Early_blight": "Solanum_Tomato_Early_Blight",
    "Tomato___Late_blight": "Solanum_Tomato_Late_Blight",
    "Tomato___healthy": "Solanum_Tomato_Healthy_Seed",
    "Corn_(maize)___Common_rust_": "Zea_Corn_Common_Rust",
    "Corn_(maize)___healthy": "Zea_Corn_Healthy_Seed",
    "Soybean___healthy": "Glycine_Soybean_Healthy_Seed",
    "Peach___Bacterial_spot": "Gossypium_Cotton_Bacterial_Blight",
    "Potato___Early_blight": "Oryza_Rice_Brown_Spot",
    "Potato___healthy": "Oryza_Rice_Healthy_Seed",
    "Pepper,_bell___Bacterial_spot": "Triticum_Wheat_Yellow_Rust",
    "Pepper,_bell___healthy": "Triticum_Wheat_Healthy_Seed",
    "Apple___Apple_scab": "Helianthus_Sunflower_Powdery_Mildew",
    "Apple___healthy": "Helianthus_Sunflower_Healthy_Seed",
    "Grape___Black_rot": "Glycine_Soybean_Caterpillar_Damage",
    "Grape___healthy": "Gossypium_Cotton_Healthy_Seed"
}

def download_hf_plantvillage():
    print("[+] Loading real PlantVillage dataset from HuggingFace...")
    try:
        from datasets import load_dataset
        ds = load_dataset("mohanty/PlantVillage", "color", split="train[:500]")

        train_dir = os.path.join(DATA_DIR, "train")
        val_dir = os.path.join(DATA_DIR, "val")
        os.makedirs(train_dir, exist_ok=True)
        os.makedirs(val_dir, exist_ok=True)

        class_counts = {}
        for sample in ds:
            label_name = sample.get("label_name", "")
            target_cls = CLASS_MAP.get(label_name, None)
            if not target_cls:
                continue

            count = class_counts.get(target_cls, 0)
            is_train = (count < 25)
            dest_dir = os.path.join(train_dir if is_train else val_dir, target_cls)
            os.makedirs(dest_dir, exist_ok=True)

            img = sample["image"]
            filename = f"real_photo_{count+1:03d}.jpg"
            img.save(os.path.join(dest_dir, filename), format="JPEG")
            class_counts[target_cls] = count + 1

        print("[OK] Successfully populated real plant disease photos from HuggingFace!")
    except Exception as e:
        print("HuggingFace fetch error:", e)

if __name__ == "__main__":
    download_hf_plantvillage()
