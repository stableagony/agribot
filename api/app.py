import os
import io
import base64
import random
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS

from src.config import BASE_DIR, DATA_DIR, MODELS_DIR, MODEL_PATH, PLANT_CLASSES, PLANT_GENUS_DETAILS, CLASS_TO_DETAILS
from src.predict import predict_plant_disease

app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'api', 'templates'),
            static_folder=os.path.join(BASE_DIR, 'api', 'static'))
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
CORS(app)

PRESET_MAP = {
    "tomato_early": "Solanum_Tomato_Early_Blight",
    "tomato_late": "Solanum_Tomato_Late_Blight",
    "tomato_healthy": "Solanum_Tomato_Healthy",
    "corn_rust": "Zea_Corn_Common_Rust",
    "corn_blight": "Zea_Corn_Northern_Leaf_Blight",
    "potato_blight": "Solanum_Potato_Early_Blight",
    "pepper_spot": "Capsicum_Pepper_Bacterial_Spot",
    "apple_scab": "Malus_Apple_Scab",
    "grape_rot": "Vitis_Grape_Black_Rot"
}

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/models/<path:filename>')
def serve_models(filename):
    """
    Serves model assets (training history plot, confusion matrix, etc.) to the web UI.
    """
    return send_from_directory(MODELS_DIR, filename)

@app.route('/api/health', methods=['GET'])
def health_check():
    model_exists = os.path.exists(MODEL_PATH)
    return jsonify({
        "status": "online",
        "service": "AgriBot CNN Plant & Disease Classifier",
        "dataset": "Plant & Leaf Pathological Dataset",
        "model_loaded": model_exists,
        "model_path": MODEL_PATH,
        "classes_count": len(PLANT_CLASSES)
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        image = None
        threshold = 0.25
        
        # 1. File Upload
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                image = Image.open(file.stream)
            if 'threshold' in request.form:
                try:
                    threshold = float(request.form['threshold']) / 100.0 if float(request.form['threshold']) > 1.0 else float(request.form['threshold'])
                except (ValueError, TypeError):
                    threshold = 0.25
        
        # 2. Base64 Upload
        elif request.is_json and 'image_base64' in request.json:
            b64_str = request.json['image_base64']
            if ',' in b64_str:
                b64_str = b64_str.split(',')[1]
            img_bytes = base64.b64decode(b64_str)
            image = Image.open(io.BytesIO(img_bytes))
            if 'threshold' in request.json:
                try:
                    t_val = float(request.json['threshold'])
                    threshold = t_val / 100.0 if t_val > 1.0 else t_val
                except (ValueError, TypeError):
                    threshold = 0.25

        if image is None:
            return jsonify({"success": False, "error": "No image file or base64 data provided"}), 400

        result = predict_plant_disease(image, threshold=threshold)
        return jsonify(result)

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/sample', methods=['GET'])
def get_sample_image():
    """
    Returns a sample image from the plant leaf validation dataset.
    Supports ?preset=<name> or ?class=<class_name> to pick specific classes.
    """
    try:
        val_dir = os.path.join(DATA_DIR, "val")
        if not os.path.exists(val_dir):
            from src.build_plant_dataset import build_plant_leaf_dataset
            build_plant_leaf_dataset()

        classes = [d for d in os.listdir(val_dir) if os.path.isdir(os.path.join(val_dir, d))]
        if not classes:
            return jsonify({"success": False, "error": "Validation dataset empty"}), 500

        preset_param = request.args.get('preset')
        class_param = request.args.get('class')

        target_class = None
        if preset_param and preset_param in PRESET_MAP:
            mapped_cls = PRESET_MAP[preset_param]
            if mapped_cls in classes:
                target_class = mapped_cls
        elif class_param and class_param in classes:
            target_class = class_param

        chosen_class = target_class if target_class else random.choice(classes)
        class_folder = os.path.join(val_dir, chosen_class)
        images = [f for f in os.listdir(class_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

        if not images:
            return jsonify({"success": False, "error": f"No sample images found for class {chosen_class}"}), 500

        chosen_img_name = random.choice(images)
        chosen_img_path = os.path.join(class_folder, chosen_img_name)

        pil_img = Image.open(chosen_img_path)
        
        buffered = io.BytesIO()
        pil_img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        mapped_info = CLASS_TO_DETAILS.get(chosen_class, {})

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
