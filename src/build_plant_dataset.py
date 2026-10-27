import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from src.config import DATA_DIR, PLANT_CLASSES, IMG_WIDTH, IMG_HEIGHT

def create_synthetic_plant_image(class_name, idx, is_train=True):
    """
    Generates realistic plant leaf / disease pattern images with distinct color palettes,
    morphological shapes, texture noise, and spot pathology for testing & demonstration.
    """
    img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), color=(20, 30, 20))
    draw = ImageDraw.Draw(img)

    # Color palette & shape based on plant genus & disease state
    if "Zea_Corn" in class_name:
        bg_color = (230, 200, 80) if "Healthy" in class_name else (140, 90, 30)
        spot_color = (180, 50, 20) if "Rust" in class_name else ((70, 70, 40) if "Blight" in class_name else None)
        shape = "ellipse"
    elif "Solanum_Tomato" in class_name:
        bg_color = (40, 180, 60) if "Healthy" in class_name else (90, 110, 40)
        spot_color = (60, 40, 20) if "Blight" in class_name else None
        shape = "leaf"
    elif "Solanum_Potato" in class_name:
        bg_color = (45, 170, 55) if "Healthy" in class_name else (85, 100, 35)
        spot_color = (75, 45, 15) if "Blight" in class_name else None
        shape = "leaf"
    elif "Capsicum_Pepper" in class_name:
        bg_color = (35, 160, 50) if "Healthy" in class_name else (95, 120, 45)
        spot_color = (40, 30, 15) if "Spot" in class_name else None
        shape = "leaf"
    elif "Malus_Apple" in class_name:
        bg_color = (50, 165, 65) if "Healthy" in class_name else (110, 130, 50)
        spot_color = (50, 60, 30) if "Scab" in class_name else None
        shape = "leaf"
    else: # Vitis Grape
        bg_color = (55, 175, 70) if "Healthy" in class_name else (100, 115, 60)
        spot_color = (35, 20, 20) if "Rot" in class_name else None
        shape = "leaf"

    # Draw Base Object
    if shape == "ellipse":
        draw.ellipse([20, 20, 108, 108], fill=bg_color, outline=(10, 10, 10))
    elif shape == "grain":
        draw.ellipse([35, 15, 93, 113], fill=bg_color, outline=(10, 10, 10))
    elif shape == "leaf":
        draw.polygon([(64, 15), (110, 64), (64, 113), (18, 64)], fill=bg_color, outline=(10, 10, 10))
    else: # cotton
        draw.ellipse([25, 25, 103, 103], fill=bg_color, outline=(200, 200, 200))

    # Draw Pathological Spots if infected
    if spot_color:
        np.random.seed(idx + (100 if is_train else 500))
        for _ in range(12):
            rx = int(np.random.randint(30, 98))
            ry = int(np.random.randint(30, 98))
            rr = int(np.random.randint(4, 12))
            draw.ellipse([rx - rr, ry - rr, rx + rr, ry + rr], fill=spot_color)

    # Add Gaussian Noise blur for realism
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    return img

def build_plant_leaf_dataset():
    """
    Initializes plant leaf & disease dataset directory structure and populates sample images.
    """
    print("[+] Building Plant Leaf & Disease Dataset structure...")
    train_dir = os.path.join(DATA_DIR, "train")
    val_dir = os.path.join(DATA_DIR, "val")

    for cls in PLANT_CLASSES:
        cls_train_path = os.path.join(train_dir, cls)
        cls_val_path = os.path.join(val_dir, cls)
        os.makedirs(cls_train_path, exist_ok=True)
        os.makedirs(cls_val_path, exist_ok=True)

        # Generate 20 train images and 5 val images per class
        for i in range(20):
            img = create_synthetic_plant_image(cls, i, is_train=True)
            img.save(os.path.join(cls_train_path, f"leaf_img_{i+1:03d}.jpg"))

        for i in range(5):
            img = create_synthetic_plant_image(cls, i, is_train=False)
            img.save(os.path.join(cls_val_path, f"val_img_{i+1:03d}.jpg"))

    print(f"[OK] Generated {len(PLANT_CLASSES)} Plant Leaf classes in '{DATA_DIR}'!")
    print(f"     Train directory: '{train_dir}'")
    print(f"     Val directory:   '{val_dir}'")

if __name__ == "__main__":
    build_plant_leaf_dataset()
