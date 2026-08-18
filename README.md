# 🌿 AgriBot — Plant Genus & Disease Intelligence Platform

> **Enterprise-grade CNN plant pathology detection system** powered by PyTorch deep learning, trained on the real [PlantVillage Dataset](https://github.com/spMohanty/PlantVillage-Dataset).

---

## 📸 Features

- **15-Class CNN Classifier** — Detects plant genus & leaf disease across 7 major crop families
- **Real PlantVillage Photographs** — Trained on authentic 256×256 RGB disease photos
- **Plant Verification Filter** — Rejects non-plant images using vegetation spectrum analysis
- **Interactive Web UI** — Multi-tab enterprise dashboard with radar scanner, attention map overlay, live confidence chart, and plant encyclopedia
- **REST API** — Flask-powered endpoints for single-image inference

---

## 🏗️ Architecture

```
PlantSeedNet (PyTorch CNN)
├── Conv Block 1  → 32 channels + BatchNorm + MaxPool
├── Conv Block 2  → 64 channels + BatchNorm + MaxPool
├── Conv Block 3  → 128 channels + Dropout(0.2)
├── Conv Block 4  → 256 channels + GlobalAvgPool
└── Classifier    → FC(256→128) + BN + Dropout(0.5) → 15 classes
```

**Input:** 128 × 128 × 3 RGB | **Parameters:** ~2.1M | **Val Accuracy:** 86.67%

---

## 🌿 Supported Plant Classes

| Genus | Crop | Conditions |
|---|---|---|
| *Solanum* | Tomato | Healthy, Early Blight, Late Blight |
| *Zea* | Corn / Maize | Healthy, Common Rust |
| *Oryza* | Rice | Healthy, Brown Spot |
| *Triticum* | Wheat | Healthy, Yellow Rust |
| *Glycine* | Soybean | Healthy, Caterpillar Damage |
| *Gossypium* | Cotton | Healthy, Bacterial Blight |
| *Helianthus* | Sunflower | Healthy, Powdery Mildew |

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download Real PlantVillage Dataset

```bash
python -m src.fetch_real_plantvillage
```

### 3. Train the CNN Model

```bash
python -m src.train
```

### 4. Launch the Web Application

```bash
python run.py
```

Then open **[http://localhost:5000](http://localhost:5000)** in your browser.

---

## 🖥️ Web Dashboard Tabs

| Tab | Description |
|---|---|
| **🔬 Classifier Studio** | Drag-and-drop image upload, random sample presets, sensitivity slider, attention map overlay |
| **🧠 Neural Architecture** | Layer pipeline diagram, training history, confusion matrix |
| **📖 Plant Encyclopedia** | Searchable & filterable card grid for all 15 plant diseases with treatment protocols |
| **⚡ System Telemetry** | Live confidence Bezier chart, inference latency tracker, system log console |

---

## 📡 REST API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Web dashboard |
| `/api/health` | GET | Server & model status |
| `/api/sample` | GET | Random validation image sample |
| `/api/predict` | POST | CNN inference (multipart file or base64 JSON) |

### Example — Predict from File

```bash
curl -X POST http://localhost:5000/api/predict \
  -F "image=@/path/to/leaf_photo.jpg"
```

### Example — Health Check

```bash
curl http://localhost:5000/api/health
```

---

## 📁 Project Structure

```
agribot/
├── api/
│   ├── app.py              # Flask REST API server
│   ├── templates/
│   │   └── index.html      # Enterprise web dashboard
│   └── static/
│       ├── style.css       # Premium design system
│       └── app.js          # Interactive client-side JS
├── src/
│   ├── config.py           # Hyperparameters & class definitions
│   ├── model.py            # PlantSeedNet CNN architecture
│   ├── dataset.py          # ImageFolder data loader & augmentations
│   ├── train.py            # Training loop with checkpointing
│   ├── predict.py          # Inference engine & plant verifier
│   ├── evaluate.py         # Evaluation & confusion matrix
│   ├── build_plant_dataset.py      # Synthetic dataset builder
│   └── fetch_real_plantvillage.py  # Real PlantVillage dataset fetcher
├── data/                   # Dataset directory (not tracked)
├── models/                 # Saved model weights (.pth)
├── requirements.txt
└── run.py                  # One-command launcher
```

---

## 📦 Requirements

```
torch>=2.0.0
torchvision>=0.15.0
flask>=3.0.0
flask-cors
numpy
pillow
matplotlib
scikit-learn
seaborn
```

---

## 📜 Dataset Credit

Real plant disease photographs from the **PlantVillage Dataset**:
> Mohanty, S.P., Hughes, D.P., & Salathé, M. (2016). *Using Deep Learning for Image-Based Plant Disease Detection*. Frontiers in Plant Science.  
> GitHub: [spMohanty/PlantVillage-Dataset](https://github.com/spMohanty/PlantVillage-Dataset)

---

## 👤 Author

**stableagony** — Semester 4 Deep Learning Project
