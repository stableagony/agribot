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

from src.config import MODEL_PATH, CONFUSION_MATRIX_PATH, PLANT_CLASSES, PLANT_GENUS_DETAILS, BATCH_SIZE
from src.dataset import load_plant_dataloaders
from src.model import build_cnn_model

def evaluate(model=None, test_loader=None):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print("==================================================")
    print(f"      AgriBot PyTorch Model Evaluation ({device})   ")
    print("==================================================")

    if test_loader is None:
        _, test_loader, _ = load_plant_dataloaders(batch_size=BATCH_SIZE)

    if model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Train the model first using 'python -m src.train'!")
        print(f"[+] Loading trained model weights from {MODEL_PATH}...")
        model = build_cnn_model(num_classes=len(PLANT_CLASSES)).to(device)
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
    test_loss = test_loss / max(total_samples, 1)
    test_acc = 100.0 * np.sum(np.array(all_preds) == np.array(all_targets)) / max(total_samples, 1)

    print(f"\n[OK] Validation Loss:     {test_loss:.4f}")
    print(f"[OK] Validation Accuracy: {test_acc:.2f}%\n")

    print("--- Classification Report ---")
    present_labels = sorted(list(set(all_targets).union(set(all_preds))))
    present_names = [PLANT_CLASSES[i] for i in present_labels]
    print(classification_report(all_targets, all_preds, labels=present_labels, target_names=present_names, zero_division=0))

    # Confusion Matrix Plot
    cm = confusion_matrix(all_targets, all_preds, labels=list(range(len(PLANT_CLASSES))))
    plt.figure(figsize=(12, 10))
    
    # Shorten class names for cleaner visualization
    short_labels = [c.replace("_Leaf", "").replace("_", " ") for c in PLANT_CLASSES]

    if HAS_SEABORN:
        sns.heatmap(cm, annot=True, fmt='d', cmap='Greens',
                    xticklabels=short_labels,
                    yticklabels=short_labels)
    else:
        plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Greens)
        plt.colorbar()
        tick_marks = np.arange(len(PLANT_CLASSES))
        plt.xticks(tick_marks, short_labels, rotation=90)
        plt.yticks(tick_marks, short_labels)

    plt.title('Plant Leaf & Pathology CNN Confusion Matrix')
    plt.xlabel('Predicted Category')
    plt.ylabel('True Category')
    plt.tight_layout()
    plt.savefig(CONFUSION_MATRIX_PATH, dpi=300)
    plt.close()
    print(f"[OK] Saved confusion matrix heatmap to {CONFUSION_MATRIX_PATH}")

    print("\n--- Sample Plant Leaf Predictions ---")
    for i in range(min(5, len(all_preds))):
        pred_idx = all_preds[i]
        true_idx = all_targets[i]
        pred_meta = PLANT_GENUS_DETAILS.get(pred_idx, {})
        true_meta = PLANT_GENUS_DETAILS.get(true_idx, {})

        print(f"Sample #{i+1}:")
        print(f"  True Class      : {PLANT_CLASSES[true_idx]} ({true_meta.get('genus', 'Unknown')})")
        print(f"  Predicted Class : {PLANT_CLASSES[pred_idx]} ({pred_meta.get('genus', 'Unknown')})")
        print(f"  Status          : {'CORRECT' if pred_idx == true_idx else 'MISMATCH'}\n")

    return test_acc, test_loss

if __name__ == "__main__":
    evaluate()
