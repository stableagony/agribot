import os
import shutil
from PIL import Image

from src.config import DATA_DIR, PLANT_CLASSES

CLASS_MAP = {
    "Pepper,_bell___Bacterial_spot": "Capsicum_Pepper_Bacterial_Spot",
    "Pepper,_bell___healthy": "Capsicum_Pepper_Healthy",
    "Apple___healthy": "Malus_Apple_Healthy",
    "Apple___Apple_scab": "Malus_Apple_Scab",
    "Potato___Early_blight": "Solanum_Potato_Early_Blight",
    "Potato___healthy": "Solanum_Potato_Healthy",
    "Potato___Late_blight": "Solanum_Potato_Late_Blight",
    "Tomato___Early_blight": "Solanum_Tomato_Early_Blight",
    "Tomato___healthy": "Solanum_Tomato_Healthy",
    "Tomato___Late_blight": "Solanum_Tomato_Late_Blight",
    "Grape___Black_rot": "Vitis_Grape_Black_Rot",
    "Grape___healthy": "Vitis_Grape_Healthy",
    "Corn_(maize)___Common_rust_": "Zea_Corn_Common_Rust",
    "Corn_(maize)___healthy": "Zea_Corn_Healthy",
    "Corn_(maize)___Northern_Leaf_Blight": "Zea_Corn_Northern_Leaf_Blight"
}

def download_hf_plantvillage(train_per_class=100, val_per_class=25):
    print("[+] Loading authentic PlantVillage dataset from HuggingFace...")
    try:
        from datasets import load_dataset
        ds = load_dataset("mohanty/PlantVillage", "default", split="train")

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
            if count >= (train_per_class + val_per_class):
                continue

            is_train = (count < train_per_class)
            dest_dir = os.path.join(train_dir if is_train else val_dir, target_cls)
            os.makedirs(dest_dir, exist_ok=True)

            img = sample["image"]
            filename = f"hf_leaf_{count+1:04d}.jpg"
            img.save(os.path.join(dest_dir, filename), format="JPEG")
            class_counts[target_cls] = count + 1

        print(f"[OK] Successfully populated {sum(class_counts.values())} real plant disease photos from HuggingFace!")
    except Exception as e:
        print("[!] HuggingFace fetch error:", e)

if __name__ == "__main__":
    download_hf_plantvillage()
