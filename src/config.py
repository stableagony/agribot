import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "plant_seeds_dataset")
MODELS_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODELS_DIR, "plant_disease_cnn.pth")
PLOT_PATH = os.path.join(MODELS_DIR, "training_history.png")
CONFUSION_MATRIX_PATH = os.path.join(MODELS_DIR, "confusion_matrix.png")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# Image & Training Hyperparameters
IMG_WIDTH = 128
IMG_HEIGHT = 128
NUM_CHANNELS = 3
INPUT_SHAPE = (NUM_CHANNELS, IMG_HEIGHT, IMG_WIDTH)
BATCH_SIZE = 32
EPOCHS = 10
LEARNING_RATE = 0.001

# Plant & Seed Class Mappings (15 Dedicated Plant Genus & Pathological Disease Categories)
PLANT_CLASSES = [
    "Zea_Corn_Healthy_Seed",
    "Zea_Corn_Common_Rust",
    "Solanum_Tomato_Healthy_Seed",
    "Solanum_Tomato_Early_Blight",
    "Solanum_Tomato_Late_Blight",
    "Oryza_Rice_Healthy_Seed",
    "Oryza_Rice_Brown_Spot",
    "Triticum_Wheat_Healthy_Seed",
    "Triticum_Wheat_Yellow_Rust",
    "Glycine_Soybean_Healthy_Seed",
    "Glycine_Soybean_Caterpillar_Damage",
    "Gossypium_Cotton_Healthy_Seed",
    "Gossypium_Cotton_Bacterial_Blight",
    "Helianthus_Sunflower_Healthy_Seed",
    "Helianthus_Sunflower_Powdery_Mildew"
]

PLANT_GENUS_DETAILS = {
    0: {"genus": "Zea (Corn / Maize)", "type": "Grain Seed", "disease": "Healthy Seed Batch", "is_healthy": True},
    1: {"genus": "Zea (Corn / Maize)", "type": "Crop Leaf", "disease": "Common Rust (Puccinia sorghi)", "is_healthy": False},
    2: {"genus": "Solanum (Tomato)", "type": "Vegetable Seed", "disease": "Healthy Seed Batch", "is_healthy": True},
    3: {"genus": "Solanum (Tomato)", "type": "Foliage", "disease": "Early Blight (Alternaria solani)", "is_healthy": False},
    4: {"genus": "Solanum (Tomato)", "type": "Foliage", "disease": "Late Blight (Phytophthora infestans)", "is_healthy": False},
    5: {"genus": "Oryza (Rice)", "type": "Cereal Seed", "disease": "Healthy Seed Batch", "is_healthy": True},
    6: {"genus": "Oryza (Rice)", "type": "Cereal Crop", "disease": "Brown Spot (Bipolaris oryzae)", "is_healthy": False},
    7: {"genus": "Triticum (Wheat)", "type": "Cereal Seed", "disease": "Healthy Seed Batch", "is_healthy": True},
    8: {"genus": "Triticum (Wheat)", "type": "Cereal Crop", "disease": "Yellow Rust (Puccinia striiformis)", "is_healthy": False},
    9: {"genus": "Glycine (Soybean)", "type": "Legume Seed", "disease": "Healthy Seed Batch", "is_healthy": True},
    10: {"genus": "Glycine (Soybean)", "type": "Legume Leaf", "disease": "Caterpillar Foliage Damage", "is_healthy": False},
    11: {"genus": "Gossypium (Cotton)", "type": "Fiber Seed", "disease": "Healthy Seed Batch", "is_healthy": True},
    12: {"genus": "Gossypium (Cotton)", "type": "Fiber Crop", "disease": "Bacterial Blight (Xanthomonas)", "is_healthy": False},
    13: {"genus": "Helianthus (Sunflower)", "type": "Oilseed", "disease": "Healthy Seed Batch", "is_healthy": True},
    14: {"genus": "Helianthus (Sunflower)", "type": "Oilseed Leaf", "disease": "Powdery Mildew (Golovinomyces)", "is_healthy": False}
}
