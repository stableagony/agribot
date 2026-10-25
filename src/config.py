import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "plant_leaf_dataset")
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

# Plant & Leaf Class Mappings (Alphabetical order matching PyTorch torchvision.datasets.ImageFolder)
PLANT_CLASSES = [
    "Glycine_Soybean_Caterpillar_Damage",
    "Glycine_Soybean_Healthy_Leaf",
    "Gossypium_Cotton_Bacterial_Blight",
    "Gossypium_Cotton_Healthy_Leaf",
    "Helianthus_Sunflower_Healthy_Leaf",
    "Helianthus_Sunflower_Powdery_Mildew",
    "Oryza_Rice_Brown_Spot",
    "Oryza_Rice_Healthy_Leaf",
    "Solanum_Tomato_Early_Blight",
    "Solanum_Tomato_Healthy_Leaf",
    "Solanum_Tomato_Late_Blight",
    "Triticum_Wheat_Healthy_Leaf",
    "Triticum_Wheat_Yellow_Rust",
    "Zea_Corn_Common_Rust",
    "Zea_Corn_Healthy_Leaf"
]

CLASS_TO_IDX = {name: i for i, name in enumerate(PLANT_CLASSES)}

PLANT_GENUS_DETAILS = {
    0: {"genus": "Glycine (Soybean)", "type": "Legume Foliage", "disease": "Caterpillar Foliage Damage (Spodoptera litura)", "is_healthy": False},
    1: {"genus": "Glycine (Soybean)", "type": "Legume Foliage", "disease": "Healthy Leaf Sample", "is_healthy": True},
    2: {"genus": "Gossypium (Cotton)", "type": "Fiber Crop Foliage", "disease": "Bacterial Blight (Xanthomonas)", "is_healthy": False},
    3: {"genus": "Gossypium (Cotton)", "type": "Fiber Crop Foliage", "disease": "Healthy Leaf Sample", "is_healthy": True},
    4: {"genus": "Helianthus (Sunflower)", "type": "Oilseed Crop Foliage", "disease": "Healthy Leaf Sample", "is_healthy": True},
    5: {"genus": "Helianthus (Sunflower)", "type": "Oilseed Crop Foliage", "disease": "Powdery Mildew (Golovinomyces)", "is_healthy": False},
    6: {"genus": "Oryza (Rice)", "type": "Cereal Crop Foliage", "disease": "Brown Spot (Bipolaris oryzae)", "is_healthy": False},
    7: {"genus": "Oryza (Rice)", "type": "Cereal Crop Foliage", "disease": "Healthy Leaf Sample", "is_healthy": True},
    8: {"genus": "Solanum (Tomato)", "type": "Vegetable Foliage", "disease": "Early Blight (Alternaria solani)", "is_healthy": False},
    9: {"genus": "Solanum (Tomato)", "type": "Vegetable Foliage", "disease": "Healthy Leaf Sample", "is_healthy": True},
    10: {"genus": "Solanum (Tomato)", "type": "Vegetable Foliage", "disease": "Late Blight (Phytophthora infestans)", "is_healthy": False},
    11: {"genus": "Triticum (Wheat)", "type": "Cereal Crop Foliage", "disease": "Healthy Leaf Sample", "is_healthy": True},
    12: {"genus": "Triticum (Wheat)", "type": "Cereal Crop Foliage", "disease": "Yellow Rust (Puccinia striiformis)", "is_healthy": False},
    13: {"genus": "Zea (Corn / Maize)", "type": "Cereal Crop Foliage", "disease": "Common Rust (Puccinia sorghi)", "is_healthy": False},
    14: {"genus": "Zea (Corn / Maize)", "type": "Cereal Crop Foliage", "disease": "Healthy Leaf Sample", "is_healthy": True}
}

CLASS_TO_DETAILS = {PLANT_CLASSES[i]: details for i, details in PLANT_GENUS_DETAILS.items()}
