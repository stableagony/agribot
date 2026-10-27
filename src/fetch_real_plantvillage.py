import os
import shutil
import glob
import stat
import subprocess
from PIL import Image

from src.config import BASE_DIR, DATA_DIR, PLANT_CLASSES

TEMP_CLONE_DIR = os.path.join(BASE_DIR, "data", "temp_plantvillage")

def robust_rmtree(path):
    if not os.path.exists(path):
        return
    def _onerror(func, p, excinfo):
        try:
            os.chmod(p, stat.S_IWRITE)
            func(p)
        except Exception:
            pass
    shutil.rmtree(path, onerror=_onerror)

# 1-to-1 Authentic PlantVillage directory names to AgriBot 15 Classes
CLASS_MAPPING = {
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

def fetch_and_populate_real_images(train_per_class=100, val_per_class=25):
    """
    Downloads authentic real photographic plant disease images from PlantVillage dataset repo
    and organizes them into data/plant_leaf_dataset/train and val across 15 genuine classes.
    """
    print("==================================================")
    print("  [+] Fetching Real Photographic PlantVillage Images ")
    print("==================================================")

    raw_color_dir = os.path.join(TEMP_CLONE_DIR, "raw", "color")
    if not os.path.exists(raw_color_dir):
        robust_rmtree(TEMP_CLONE_DIR)
        print("[+] Shallow cloning PlantVillage dataset repository (~300MB)...")
        cmd = ["git", "clone", "--depth", "1", "https://github.com/spMohanty/PlantVillage-Dataset.git", TEMP_CLONE_DIR]
        subprocess.run(cmd, check=True)
    else:
        print("[+] Using existing cloned repository in data/temp_plantvillage...")
    if not os.path.exists(raw_color_dir):
        print(f"[!] Warning: Raw color directory not found at {raw_color_dir}")
        return

    train_dir = os.path.join(DATA_DIR, "train")
    val_dir = os.path.join(DATA_DIR, "val")

    # Clear previous directory contents
    robust_rmtree(train_dir)
    robust_rmtree(val_dir)
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

    total_real_copied = 0

    for source_folder, target_cls in CLASS_MAPPING.items():
        src_path = os.path.join(raw_color_dir, source_folder)
        if not os.path.exists(src_path):
            print(f"[!] Source folder '{source_folder}' not found. Skipping.")
            continue

        target_train = os.path.join(train_dir, target_cls)
        target_val = os.path.join(val_dir, target_cls)
        os.makedirs(target_train, exist_ok=True)
        os.makedirs(target_val, exist_ok=True)

        images = glob.glob(os.path.join(src_path, "*.[jJ][pP][gG]")) + glob.glob(os.path.join(src_path, "*.[pP][nN][gG]"))
        if not images:
            print(f"[!] No images in '{source_folder}'. Skipping.")
            continue

        train_samples = images[:train_per_class]
        val_samples = images[train_per_class:train_per_class + val_per_class]

        for i, img_p in enumerate(train_samples):
            dest = os.path.join(target_train, f"pv_leaf_{i+1:04d}.jpg")
            shutil.copy(img_p, dest)
            total_real_copied += 1

        for i, img_p in enumerate(val_samples):
            dest = os.path.join(target_val, f"pv_leaf_val_{i+1:04d}.jpg")
            shutil.copy(img_p, dest)
            total_real_copied += 1

        print(f"  [OK] {target_cls:<35}: {len(train_samples)} train, {len(val_samples)} val")

    # Cleanup temporary repo to save disk space
    print("[+] Cleaning up temporary clone directory...")
    robust_rmtree(TEMP_CLONE_DIR)

    print(f"\n[OK] Successfully populated dataset with {total_real_copied} authentic PlantVillage images!")
    print(f"     Train directory: '{train_dir}'")
    print(f"     Val directory:   '{val_dir}'")

if __name__ == "__main__":
    fetch_and_populate_real_images()
