import os
import torch
import torch.nn as nn
import torch.optim as optim

from src.config import MODEL_PATH, MODELS_DIR, PLANT_CLASSES
from src.model import build_cnn_model

def initialize_quick_model():
    """
    Creates and saves an initialized PlantLeafNet PyTorch CNN model checkpoint immediately.
    """
    print("[+] Initializing PlantLeafNet PyTorch CNN model weights...")
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    num_classes = len(PLANT_CLASSES)
    model = build_cnn_model(num_classes=num_classes).to(device)

    # Quick dummy forward/backward pass
    dummy_x = torch.randn(8, 3, 128, 128).to(device)
    dummy_y = torch.randint(0, num_classes, (8,)).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    optimizer.zero_grad()
    out = model(dummy_x)
    loss = criterion(out, dummy_y)
    loss.backward()
    optimizer.step()

    torch.save(model.state_dict(), MODEL_PATH)
    print(f"[OK] Successfully generated plant disease model checkpoint at '{MODEL_PATH}'!")

if __name__ == "__main__":
    initialize_quick_model()
