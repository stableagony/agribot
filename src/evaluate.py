import os
import torch
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False

from sklearn.metrics import classification_report, confusion_matrix

from src.config import MODEL_PATH, CONFUSION_MATRIX_PATH, CIFAR10_CLASSES, PLANT_GENUS_MAP
from src.dataset import load_cifar_dataloaders
from src.model import build_cnn_model

def evaluate(model=None, test_loader=None):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print("==================================================")
    print(f"      AgriBot PyTorch Model Evaluation ({device})   ")
    print("==================================================")

    if test_loader is None:
        _, _, test_loader, _ = load_cifar_dataloaders()

    if model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Train the model first!")
        print(f"[+] Loading trained model weights from {MODEL_PATH}...")
        model = build_cnn_model().to(device)
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device))

    model.eval()
    all_preds = []
    all_targets = []
    criterion = torch.nn.CrossEntropyLoss()
    test_loss = 0.0

    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            test_loss += loss.item() * images.size(0)

            _, predicted = outputs.max(1)
            all_preds.extend(predicted.cpu().numpy())
            all_targets.extend(labels.cpu().numpy())

    total_samples = len(all_targets)
    test_loss = test_loss / total_samples
    test_acc = 100.0 * np.sum(np.array(all_preds) == np.array(all_targets)) / total_samples

    print(f"\n[OK] Test Loss:     {test_loss:.4f}")
    print(f"[OK] Test Accuracy: {test_acc:.2f}%\n")

    print("--- Classification Report ---")
    print(classification_report(all_targets, all_preds, target_names=CIFAR10_CLASSES))

    # Confusion Matrix Plot
    cm = confusion_matrix(all_targets, all_preds)
    plt.figure(figsize=(10, 8))
    
    if HAS_SEABORN:
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=CIFAR10_CLASSES,
                    yticklabels=CIFAR10_CLASSES)
    else:
        plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        plt.colorbar()
        tick_marks = np.arange(len(CIFAR10_CLASSES))
        plt.xticks(tick_marks, CIFAR10_CLASSES, rotation=45)
        plt.yticks(tick_marks, CIFAR10_CLASSES)

    plt.title('CNN Model Confusion Matrix')
    plt.xlabel('Predicted Category')
    plt.ylabel('True Category')
    plt.tight_layout()
    plt.savefig(CONFUSION_MATRIX_PATH, dpi=300)
    plt.close()
    print(f"[OK] Saved confusion matrix heatmap to {CONFUSION_MATRIX_PATH}")

    print("\n--- Sample Plant Seed & Disease Mapping Predictions ---")
    for i in range(min(5, len(all_preds))):
        pred_idx = all_preds[i]
        true_idx = all_targets[i]
        mapping = PLANT_GENUS_MAP.get(pred_idx, {})

        print(f"Sample #{i+1}:")
        print(f"  True CIFAR Class : {CIFAR10_CLASSES[true_idx]}")
        print(f"  Predicted Genus  : {mapping.get('genus', 'Unknown')} ({mapping.get('type', '')})")
        print(f"  Disease Status   : {mapping.get('disease', 'Unknown')}\n")

    return test_acc, test_loss

if __name__ == "__main__":
    evaluate()
