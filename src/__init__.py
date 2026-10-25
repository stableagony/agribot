# AgriBot CNN Package Initialization
from .config import PLANT_CLASSES, PLANT_GENUS_DETAILS, CLASS_TO_DETAILS, CLASS_TO_IDX
from .model import PlantLeafNet, build_cnn_model
from .predict import predict_plant_disease
