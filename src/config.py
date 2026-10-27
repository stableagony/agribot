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

# Plant & Leaf Class Mappings (15 Authentic PlantVillage Benchmark Classes in Alphabetical Order)
PLANT_CLASSES = [
    "Capsicum_Pepper_Bacterial_Spot",
    "Capsicum_Pepper_Healthy",
    "Malus_Apple_Healthy",
    "Malus_Apple_Scab",
    "Solanum_Potato_Early_Blight",
    "Solanum_Potato_Healthy",
    "Solanum_Potato_Late_Blight",
    "Solanum_Tomato_Early_Blight",
    "Solanum_Tomato_Healthy",
    "Solanum_Tomato_Late_Blight",
    "Vitis_Grape_Black_Rot",
    "Vitis_Grape_Healthy",
    "Zea_Corn_Common_Rust",
    "Zea_Corn_Healthy",
    "Zea_Corn_Northern_Leaf_Blight"
]

CLASS_TO_IDX = {name: i for i, name in enumerate(PLANT_CLASSES)}

PLANT_GENUS_DETAILS = {
    0: {"genus": "Capsicum (Bell Pepper)", "type": "Solanaceous Vegetable", "disease": "Bacterial Spot (Xanthomonas campestris)", "is_healthy": False},
    1: {"genus": "Capsicum (Bell Pepper)", "type": "Solanaceous Vegetable", "disease": "Healthy Leaf Sample", "is_healthy": True},
    2: {"genus": "Malus (Apple)", "type": "Deciduous Fruit Foliage", "disease": "Healthy Leaf Sample", "is_healthy": True},
    3: {"genus": "Malus (Apple)", "type": "Deciduous Fruit Foliage", "disease": "Apple Scab (Venturia inaequalis)", "is_healthy": False},
    4: {"genus": "Solanum (Potato)", "type": "Tuber Crop Foliage", "disease": "Early Blight (Alternaria solani)", "is_healthy": False},
    5: {"genus": "Solanum (Potato)", "type": "Tuber Crop Foliage", "disease": "Healthy Leaf Sample", "is_healthy": True},
    6: {"genus": "Solanum (Potato)", "type": "Tuber Crop Foliage", "disease": "Late Blight (Phytophthora infestans)", "is_healthy": False},
    7: {"genus": "Solanum (Tomato)", "type": "Solanaceous Vegetable", "disease": "Early Blight (Alternaria solani)", "is_healthy": False},
    8: {"genus": "Solanum (Tomato)", "type": "Solanaceous Vegetable", "disease": "Healthy Leaf Sample", "is_healthy": True},
    9: {"genus": "Solanum (Tomato)", "type": "Solanaceous Vegetable", "disease": "Late Blight (Phytophthora infestans)", "is_healthy": False},
    10: {"genus": "Vitis (Grape)", "type": "Vineyard Fruit Foliage", "disease": "Black Rot (Guignardia bidwellii)", "is_healthy": False},
    11: {"genus": "Vitis (Grape)", "type": "Vineyard Fruit Foliage", "disease": "Healthy Leaf Sample", "is_healthy": True},
    12: {"genus": "Zea (Corn / Maize)", "type": "Cereal Crop Foliage", "disease": "Common Rust (Puccinia sorghi)", "is_healthy": False},
    13: {"genus": "Zea (Corn / Maize)", "type": "Cereal Crop Foliage", "disease": "Healthy Leaf Sample", "is_healthy": True},
    14: {"genus": "Zea (Corn / Maize)", "type": "Cereal Crop Foliage", "disease": "Northern Leaf Blight (Exserohilum turcicum)", "is_healthy": False}
}

CLASS_TO_DETAILS = {PLANT_CLASSES[i]: details for i, details in PLANT_GENUS_DETAILS.items()}
