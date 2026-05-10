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

MODEL_PATH = os.path.join(BASE_DIR, "final_model_v4")

CLASS_NAMES_PATH = os.path.join(BASE_DIR, "class_names.json")

IMG_SIZE = (128, 128)


# =========================
# LOAD CLASS NAMES
# =========================
with open(CLASS_NAMES_PATH, "r") as f:
    CLASS_NAMES = json.load(f)

if isinstance(CLASS_NAMES, dict):
    CLASS_NAMES = list(CLASS_NAMES.values())


# =========================
# CLASS NAME STANDARDIZATION
# =========================
CLASS_MAPPING = {

    "Apple___Apple_scab": "Apple Scab",
    "Apple___Black_rot": "Apple Black Rot",
    "Apple___Cedar_apple_rust": "Apple Cedar Apple Rust",
    "Apple___healthy": "Apple Healthy",

    "Blueberry___healthy": "Blueberry Healthy",

    "Cherry_(including_sour)___healthy": "Cherry Healthy",
    "Cherry_(including_sour)___Powdery_mildew": "Cherry Powdery Mildew",

    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot":
        "Corn Gray Leaf Spot",

    "Corn_(maize)___Common_rust_":
        "Corn Common Rust",

    "Corn_(maize)___healthy":
        "Corn Healthy",

    "Corn_(maize)___Northern_Leaf_Blight":
        "Corn Northern Leaf Blight",

    "Grape___Black_rot":
        "Grape Black Rot",

    "Grape___Esca_(Black_Measles)":
        "Grape Esca",

    "Grape___healthy":
        "Grape Healthy",

    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)":
        "Grape Leaf Blight",

    "Orange___Haunglongbing_(Citrus_greening)":
        "Orange Haunglongbing",

    "Peach___Bacterial_spot":
        "Peach Bacterial Spot",

    "Peach___healthy":
        "Peach Healthy",

    "Pepper,_bell___Bacterial_spot":
        "Pepper Bacterial Spot",

    "Pepper,_bell___healthy":
        "Pepper Healthy",

    "Potato___Early_blight":
        "Potato Early Blight",

    "Potato___healthy":
        "Potato Healthy",

    "Potato___Late_blight":
        "Potato Late Blight",

    "Raspberry___healthy":
        "Raspberry Healthy",

    "Soybean___healthy":
        "Soybean Healthy",

    "Squash___Powdery_mildew":
        "Squash Powdery Mildew",

    "Strawberry___healthy":
        "Strawberry Healthy",

    "Strawberry___Leaf_scorch":
        "Strawberry Leaf Scorch",

    "Tomato___Bacterial_spot":
        "Tomato Bacterial Spot",

    "Tomato___Early_blight":
        "Tomato Early Blight",

    "Tomato___healthy":
        "Tomato Healthy",

    "Tomato___Late_blight":
        "Tomato Late Blight",

    "Tomato___Leaf_Mold":
        "Tomato Leaf Mold",

    "Tomato___Septoria_leaf_spot":
        "Tomato Septoria Leaf Spot",

    "Tomato___Spider_mites Two-spotted_spider_mite":
        "Tomato Spider Mites",

    "Tomato___Target_Spot":
        "Tomato Target Spot",

    "Tomato___Tomato_mosaic_virus":
        "Tomato Mosaic Virus",

    "Tomato___Tomato_Yellow_Leaf_Curl_Virus":
        "Tomato Yellow Leaf Curl Virus",
}


# =========================
# LOAD MODEL
# =========================
def load_saved_model():

    print("🚀 Loading model...")

    model = keras.Sequential([
        keras.layers.InputLayer(
            input_shape=(128, 128, 3)
        ),

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
def get_crop_from_disease(disease_name: str):

    name = disease_name.lower()

    if "tomato" in name:
        return "Tomato"

    if "potato" in name:
        return "Potato"

    if "corn" in name or "maize" in name:
        return "Corn"

    if "apple" in name:
        return "Apple"

    if "grape" in name:
        return "Grape"

    if "pepper" in name:
        return "Pepper"

    if "cherry" in name:
        return "Cherry"

    if "peach" in name:
        return "Peach"

    if "strawberry" in name:
        return "Strawberry"

    if "blueberry" in name:
        return "Blueberry"

    if "raspberry" in name:
        return "Raspberry"

    if "soybean" in name:
        return "Soybean"

    if "orange" in name:
        return "Orange"

    if "squash" in name:
        return "Squash"

    return "Unknown"


# =========================
# MAIN PREDICTION FUNCTION
# =========================
def predict_disease(image_path: str):

    # Load model once
    if not hasattr(predict_disease, "_model"):
        predict_disease._model = load_saved_model()

    model = predict_disease._model

    # Validate image
    if not os.path.exists(image_path):
        raise ValueError("Image not found")

    print(f"📸 Processing: {image_path}")

    # Load image
    img = Image.open(image_path).convert("RGB")

    img = img.resize(IMG_SIZE)

    arr = np.array(img).astype(np.float32)

    arr = preprocess_input(arr)

    arr = np.expand_dims(arr, axis=0)

    # Predict
    preds = model.predict(arr)

    # Handle dict output
    if isinstance(preds, dict):
        preds = list(preds.values())[0]

    idx = int(np.argmax(preds[0]))

    confidence = float(preds[0][idx]) * 100

    raw_name = CLASS_NAMES[idx]

    print("RAW MODEL LABEL:", raw_name)

    # Standardized disease name
    disease = CLASS_MAPPING.get(
        raw_name,
        raw_name.replace("_", " ")
    )

    print("STANDARDIZED LABEL:", disease)

    # Low confidence
    if confidence < 3:

        return (
            "Unknown Disease",
            round(confidence, 1),
            "Unknown"
        )

    crop = get_crop_from_disease(disease)

    return disease, round(confidence, 1), crop


# =========================
# TEST BLOCK
# =========================
if __name__ == "__main__":

    print("predict.py READY")

    test_img = "test.jpg"

    if os.path.exists(test_img):

        result = predict_disease(test_img)

        print("\n✅ FINAL OUTPUT:")
        print(result)

    else:
        print("⚠️ Add test.jpg for testing")
        