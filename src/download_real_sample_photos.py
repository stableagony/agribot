import os
import urllib.request
import ssl
from PIL import Image

from src.config import DATA_DIR, PLANT_CLASSES

# Direct public URLs of authentic photographic plant disease & crop seed samples
REAL_IMAGE_URLS = {
    "Solanum_Tomato_Early_Blight": [
        "https://upload.wikimedia.org/wikipedia/commons/ thumb/8/87/Tomato_Early_Blight.JPG/640px-Tomato_Early_Blight.JPG",
        "https://upload.wikimedia.org/wikipedia/commons/4/4b/Alternaria_solani_leaf.jpg"
    ],
    "Zea_Corn_Common_Rust": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Puccinia_sorghi_on_Zea_mays.jpg/640px-Puccinia_sorghi_on_Zea_mays.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/5/52/Common_rust_corn_leaf.jpg"
    ],
    "Solanum_Tomato_Late_Blight": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Late_blight_on_tomato_leaf.jpg/640px-Late_blight_on_tomato_leaf.jpg"
    ],
    "Oryza_Rice_Brown_Spot": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Rice_brown_spot.jpg/640px-Rice_brown_spot.jpg"
    ],
    "Triticum_Wheat_Yellow_Rust": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Stripe_rust_on_wheat.jpg/640px-Stripe_rust_on_wheat.jpg"
    ],
    "Helianthus_Sunflower_Powdery_Mildew": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Powdery_mildew_on_sunflower_leaf.jpg/640px-Powdery_mildew_on_sunflower_leaf.jpg"
    ]
}

def download_real_photos():
    print("[+] Downloading real photographic plant disease samples...")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    train_dir = os.path.join(DATA_DIR, "train")
    val_dir = os.path.join(DATA_DIR, "val")

    downloaded = 0
    for cls_name, urls in REAL_IMAGE_URLS.items():
        c_train = os.path.join(train_dir, cls_name)
        c_val = os.path.join(val_dir, cls_name)
        os.makedirs(c_train, exist_ok=True)
        os.makedirs(c_val, exist_ok=True)

        for i, url in enumerate(urls):
            try:
                # Clean space in URL
                clean_url = url.replace(" ", "")
                req = urllib.request.Request(clean_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                dest = os.path.join(c_train if i == 0 else c_val, f"real_photo_{i+1:02d}.jpg")
                with urllib.request.urlopen(req, context=ctx, timeout=10) as resp, open(dest, 'wb') as f:
                    f.write(resp.read())

                # Resize to standard 128x128
                with Image.open(dest) as img:
                    img_resized = img.convert('RGB').resize((128, 128))
                    img_resized.save(dest, format='JPEG')
                
                downloaded += 1
                print(f"  [✓] Downloaded real photo for '{cls_name}' -> {dest}")
            except Exception as e:
                print(f"  [!] Failed to fetch {clean_url}: {e}")

    print(f"\n[OK] Successfully saved {downloaded} real photographic plant disease samples!")

if __name__ == "__main__":
    download_real_photos()
