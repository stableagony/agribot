import os
import io
import base64
import random
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from src.config import BASE_DIR, DATA_DIR, MODEL_PATH, PLANT_CLASSES, PLANT_GENUS_DETAILS
from src.predict import predict_plant_disease

app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'api', 'templates'),
            static_folder=os.path.join(BASE_DIR, 'api', 'static'))
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
CORS(app)

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    model_exists = os.path.exists(MODEL_PATH)
    return jsonify({
        "status": "online",
        "service": "AgriBot CNN Plant & Disease Classifier",
        "dataset": "Plant & Seed Pathological Dataset",
        "model_loaded": model_exists,
        "model_path": MODEL_PATH
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        image = None
        
        # 1. File Upload
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                image = Image.open(file.stream)
        
        # 2. Base64 Upload
        elif request.is_json and 'image_base64' in request.json:
            b64_str = request.json['image_base64']
            if ',' in b64_str:
                b64_str = b64_str.split(',')[1]
            img_bytes = base64.b64decode(b64_str)
            image = Image.open(io.BytesIO(img_bytes))

        if image is None:
            return jsonify({"success": False, "error": "No image file or base64 data provided"}), 400

        result = predict_plant_disease(image)
        return jsonify(result)

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/sample', methods=['GET'])
def get_sample_image():
    """
    Returns a random sample image from the plant seeds validation dataset.
    """
    try:
        val_dir = os.path.join(DATA_DIR, "val")
        if not os.path.exists(val_dir):
            from src.build_plant_dataset import build_plant_seeds_dataset
            build_plant_seeds_dataset()

        classes = [d for d in os.listdir(val_dir) if os.path.isdir(os.path.join(val_dir, d))]
        if not classes:
            return jsonify({"success": False, "error": "Validation dataset empty"}), 500

        chosen_class = random.choice(classes)
        class_folder = os.path.join(val_dir, chosen_class)
        images = [f for f in os.listdir(class_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

        if not images:
            return jsonify({"success": False, "error": "No sample images found"}), 500

        chosen_img_name = random.choice(images)
        chosen_img_path = os.path.join(class_folder, chosen_img_name)

        pil_img = Image.open(chosen_img_path)
        
        buffered = io.BytesIO()
        pil_img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        class_idx = PLANT_CLASSES.index(chosen_class) if chosen_class in PLANT_CLASSES else 0
        mapped_info = PLANT_GENUS_DETAILS.get(class_idx, {})

        return jsonify({
            "success": True,
            "sample_class": chosen_class,
            "true_genus": mapped_info.get("genus", "Unknown"),
            "true_disease": mapped_info.get("disease", "Unknown"),
            "image_base64": f"data:image/jpeg;base64,{img_str}"
        })
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    print("[+] Launching AgriBot Enterprise Web Application...")
    app.run(host='0.0.0.0', port=5000, debug=True)
