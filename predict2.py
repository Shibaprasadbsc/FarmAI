# =========================
# IMPORTS
# =========================
import os
import json
import numpy as np
from PIL import Image

from tensorflow import keras
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


# =========================
# PATHS
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 🔥 SavedModel folder (NOT .h5 / .keras)
MODEL_PATH = os.path.join(BASE_DIR, "final_model_v4")

CLASS_NAMES_PATH = os.path.join(BASE_DIR, "class_names.json")

IMG_SIZE = (128, 128)


# =========================
# LOAD CLASS NAMES
# =========================
with open(CLASS_NAMES_PATH, "r") as f:
    CLASS_NAMES = json.load(f)

# Ensure list format
if isinstance(CLASS_NAMES, dict):
    CLASS_NAMES = list(CLASS_NAMES.values())


# =========================
# LOAD MODEL (KERAS 3 FIX)
# =========================
def load_saved_model():
    print("🚀 Loading SavedModel using TFSMLayer...")

    model = keras.Sequential([
        keras.layers.InputLayer(input_shape=(128, 128, 3)),
        keras.layers.TFSMLayer(
            MODEL_PATH,
            call_endpoint="serving_default"
        )
    ])

    print("✅ Model loaded successfully")
    return model


# =========================
# HELPER FUNCTION
# =========================
def get_crop_from_disease(disease_name: str) -> str:
    name = disease_name.lower()

    if "tomato" in name: return "Tomato"
    if "potato" in name: return "Potato"
    if "corn" in name or "maize" in name: return "Corn"
    if "apple" in name: return "Apple"
    if "grape" in name: return "Grape"
    if "pepper" in name: return "Pepper"
    if "cherry" in name: return "Cherry"
    if "peach" in name: return "Peach"
    if "strawberry" in name: return "Strawberry"

    return "Unknown"


# =========================
# MAIN FUNCTION
# =========================
def predict_disease(image_path: str):

    # Load model only once
    if not hasattr(predict_disease, "_model"):
        predict_disease._model = load_saved_model()

    model = predict_disease._model

    # Validate image path
    if not os.path.exists(image_path):
        raise ValueError("Image not found")

    print(f"📸 Processing image: {image_path}")

    # Load and preprocess image
    img = Image.open(image_path).convert("RGB")
    img = img.resize(IMG_SIZE)

    arr = np.array(img).astype(np.float32)
    arr = preprocess_input(arr)
    arr = np.expand_dims(arr, axis=0)

    preds = model.predict(arr)

    # 🔥 Handle dict output from TFSMLayer
    if isinstance(preds, dict):
        preds = list(preds.values())[0]

    # Now safe
    idx = int(np.argmax(preds[0]))
    confidence = float(preds[0][idx]) * 100

    raw_name = CLASS_NAMES[idx]

    # Format disease name
    parts = raw_name.split("___")
    if len(parts) > 1:
        disease = parts[0] + " " + parts[1].replace("_", " ")
    else:
        disease = raw_name.replace("_", " ")

    # Low confidence handling
    if confidence < 3:
        return "Unknown Disease", round(confidence, 1), "Unknown"

    crop = get_crop_from_disease(disease)

    return disease, round(confidence, 1), crop


# =========================
# TEST BLOCK
# =========================
if __name__ == "__main__":
    print("predict.py — READY")

    test_img = "test.jpg"

    if os.path.exists(test_img):
        result = predict_disease(test_img)
        print("\n✅ FINAL OUTPUT:", result)
    else:
        print("⚠️ Add test.jpg for testing")