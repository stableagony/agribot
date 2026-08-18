# AgriBot CNN Package Initialization
from .config import PLANT_CLASSES, PLANT_GENUS_DETAILS
from .model import PlantSeedNet, build_cnn_model
from .predict import predict_plant_disease
