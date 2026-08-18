import os
import sys

from src.config import MODEL_PATH

def main():
    print("==================================================")
    print("         AgriBot CNN Project Launcher             ")
    print("==================================================")

    # 1. Check if model exists, otherwise initialize instantly
    if not os.path.exists(MODEL_PATH):
        print(f"[!] Model checkpoint not found at '{MODEL_PATH}'. Generating model checkpoint...")
        from src.init_model import initialize_quick_model
        initialize_quick_model()
    else:
        print(f"[OK] Existing CNN model checkpoint found at '{MODEL_PATH}'.")

    # 2. Launch Flask Web Server
    print("\n[+] Starting Flask API & Web Interface at http://localhost:5000...")
    from api.app import app
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    main()
