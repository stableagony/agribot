import os
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from src.config import BATCH_SIZE, EPOCHS, LEARNING_RATE, MODEL_PATH, PLOT_PATH, PLANT_CLASSES
from src.dataset import load_plant_dataloaders
from src.model import build_cnn_model

def get_device():
    return torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def plot_training_history(train_accs, val_accs, train_losses, val_losses, save_path=PLOT_PATH):
    epochs_range = range(1, len(train_accs) + 1)
    plt.figure(figsize=(12, 5))

    # Accuracy
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, train_accs, 'b-o', label='Train Accuracy')
    plt.plot(epochs_range, val_accs, 'g-s', label='Val Accuracy')
    plt.title('Plant Leaf Model Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy (%)')
    plt.legend()
    plt.grid(True)

    # Loss
    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, train_losses, 'b-o', label='Train Loss')
    plt.plot(epochs_range, val_losses, 'g-s', label='Val Loss')
    plt.title('Plant Leaf Model Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"[OK] Saved training history plot to {save_path}")

def train():
    device = get_device()
    print("==================================================")
    print(f"  AgriBot Plant Leaf CNN Training Engine ({device}) ")
    print("==================================================")

    train_loader, val_loader, val_dataset = load_plant_dataloaders(batch_size=BATCH_SIZE)

    model = build_cnn_model(num_classes=len(PLANT_CLASSES)).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=2)

    best_val_acc = 0.0
    train_accs, val_accs, train_losses, val_losses = [], [], [], []

    for epoch in range(1, EPOCHS + 1):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

        epoch_train_loss = running_loss / total
        epoch_train_acc = 100.0 * correct / total

        model.eval()
        val_running_loss = 0.0
        val_correct = 0
        val_total = 0

        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)

                val_running_loss += loss.item() * images.size(0)
                _, predicted = outputs.max(1)
                val_total += labels.size(0)
                val_correct += predicted.eq(labels).sum().item()

        epoch_val_loss = val_running_loss / val_total
        epoch_val_acc = 100.0 * val_correct / val_total

        scheduler.step(epoch_val_acc)

        train_accs.append(epoch_train_acc)
        val_accs.append(epoch_val_acc)
        train_losses.append(epoch_train_loss)
        val_losses.append(epoch_val_loss)

        print(f"Epoch [{epoch:02d}/{EPOCHS:02d}] "
              f"Train Loss: {epoch_train_loss:.4f} | Train Acc: {epoch_train_acc:.2f}% || "
              f"Val Loss: {epoch_val_loss:.4f} | Val Acc: {epoch_val_acc:.2f}%")

        if epoch_val_acc >= best_val_acc:
            best_val_acc = epoch_val_acc
            torch.save(model.state_dict(), MODEL_PATH)
            print(f"  [->] Saved new best model checkpoint (Val Acc: {best_val_acc:.2f}%) to {MODEL_PATH}")

    plot_training_history(train_accs, val_accs, train_losses, val_losses)
    print("\n[OK] Plant Leaf CNN Model Training Complete!")
    return model, val_loader

if __name__ == "__main__":
    train()
