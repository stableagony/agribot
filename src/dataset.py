import os
import torch
from torch.utils.data import DataLoader
import torchvision
import torchvision.transforms as transforms
from src.config import DATA_DIR, BATCH_SIZE, IMG_WIDTH, IMG_HEIGHT, PLANT_CLASSES
from src.build_plant_dataset import build_plant_leaf_dataset

def get_plant_transforms():
    """
    Data transformation & augmentation pipeline tailored for 128x128 plant leaf & disease images.
    """
    train_transform = transforms.Compose([
        transforms.Resize((IMG_HEIGHT, IMG_WIDTH)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
    ])

    val_transform = transforms.Compose([
        transforms.Resize((IMG_HEIGHT, IMG_WIDTH)),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
    ])

    return train_transform, val_transform

def load_plant_dataloaders(batch_size=BATCH_SIZE):
    """
    Loads Plant Leaf & Disease dataset using torchvision.datasets.ImageFolder.
    """
    train_dir = os.path.join(DATA_DIR, "train")
    val_dir = os.path.join(DATA_DIR, "val")

    if not os.path.exists(train_dir) or len(os.listdir(train_dir)) == 0:
        print("[!] Plant leaf dataset not found. Generating initial dataset...")
        build_plant_leaf_dataset()

    print(f"[+] Loading Plant & Leaf dataset from '{DATA_DIR}'...")
    train_transform, val_transform = get_plant_transforms()

    train_dataset = torchvision.datasets.ImageFolder(root=train_dir, transform=train_transform)
    val_dataset = torchvision.datasets.ImageFolder(root=val_dir, transform=val_transform)

    if train_dataset.classes != PLANT_CLASSES:
        print("[!] Warning: Detected classes differ from configured PLANT_CLASSES:")
        print(f"    Detected:   {train_dataset.classes}")
        print(f"    Configured: {PLANT_CLASSES}")

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

    print(f"[OK] Training samples:   {len(train_dataset)}")
    print(f"[OK] Validation samples: {len(val_dataset)}")
    print(f"[OK] Detected Classes:   {len(train_dataset.classes)}")

    return train_loader, val_loader, val_dataset
