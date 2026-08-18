import torch
import torch.nn as nn
import torch.nn.functional as F

class PlantSeedNet(nn.Module):
    """
    Deep Convolutional Neural Network for Plant Seed Genus & Disease Classification.
    Features 4 Convolutional Blocks with Batch Normalization, Max Pooling, and Dropout.
    """
    def __init__(self, num_classes=15):
        super(PlantSeedNet, self).__init__()
        
        # Block 1: 3 -> 32 channels (128x128 -> 64x64)
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 32, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(32)
        self.pool1 = nn.MaxPool2d(2, 2)
        self.drop1 = nn.Dropout(0.2)

        # Block 2: 32 -> 64 channels (64x64 -> 32x32)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(64)
        self.conv4 = nn.Conv2d(64, 64, kernel_size=3, padding=1)
        self.bn4 = nn.BatchNorm2d(64)
        self.pool2 = nn.MaxPool2d(2, 2)
        self.drop2 = nn.Dropout(0.25)

        # Block 3: 64 -> 128 channels (32x32 -> 16x16)
        self.conv5 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn5 = nn.BatchNorm2d(128)
        self.conv6 = nn.Conv2d(128, 128, kernel_size=3, padding=1)
        self.bn6 = nn.BatchNorm2d(128)
        self.pool3 = nn.MaxPool2d(2, 2)
        self.drop3 = nn.Dropout(0.3)

        # Block 4: 128 -> 256 channels (16x16 -> 8x8)
        self.conv7 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.bn7 = nn.BatchNorm2d(256)
        self.pool4 = nn.MaxPool2d(2, 2)
        self.drop4 = nn.Dropout(0.35)

        # Adaptive Global Average Pooling
        self.global_pool = nn.AdaptiveAvgPool2d((1, 1))

        # Classifier
        self.fc1 = nn.Linear(256, 128)
        self.bn_fc = nn.BatchNorm1d(128)
        self.drop_fc = nn.Dropout(0.5)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        # Block 1
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = self.pool1(x)
        x = self.drop1(x)

        # Block 2
        x = F.relu(self.bn3(self.conv3(x)))
        x = F.relu(self.bn4(self.conv4(x)))
        x = self.pool2(x)
        x = self.drop2(x)

        # Block 3
        x = F.relu(self.bn5(self.conv5(x)))
        x = F.relu(self.bn6(self.conv6(x)))
        x = self.pool3(x)
        x = self.drop3(x)

        # Block 4
        x = F.relu(self.bn7(self.conv7(x)))
        x = self.pool4(x)
        x = self.drop4(x)

        # Pooling & Dense
        x = self.global_pool(x)
        x = x.view(x.size(0), -1) # Flatten to (batch, 256)
        x = F.relu(self.bn_fc(self.fc1(x)))
        x = self.drop_fc(x)
        x = self.fc2(x)
        return x

def build_cnn_model(num_classes=15):
    return PlantSeedNet(num_classes=num_classes)

if __name__ == "__main__":
    model = build_cnn_model()
    dummy = torch.randn(2, 3, 128, 128)
    out = model(dummy)
    print("PlantSeedNet Output Shape:", out.shape)
