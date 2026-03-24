"""
FarmAI Backend — predict.py
=============================
This file is the bridge between the Flask server and the AI model.

RIGHT NOW (Phase 2):
    It returns a realistic fake prediction so the backend works
    end-to-end before the real model is trained.

PHASE 3:
    We replace the fake prediction with a real TensorFlow model.
    The function signature stays EXACTLY the same — server.py won't
    need to change at all.

This pattern is called a "stub" or "mock" — professional developers
use it to build and test systems before all parts are ready.
"""

import os
import random

# ── Phase 3 will uncomment these ──────────────────────────────────────────────
# import numpy as np
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image as keras_image

# ── All 17 disease classes the model will recognise ───────────────────────────
CLASS_NAMES = [
    "Tomato Early Blight",
    "Tomato Late Blight",
    "Tomato Leaf Mold",
    "Tomato Yellow Leaf Curl",
    "Tomato Bacterial Spot",
    "Tomato Healthy",
    "Potato Early Blight",
    "Potato Late Blight",
    "Potato Healthy",
    "Corn Common Rust",
    "Corn Gray Leaf Spot",
    "Corn Northern Leaf Blight",
    "Corn Healthy",
    "Apple Scab",
    "Apple Black Rot",
    "Apple Cedar Apple Rust",
    "Apple Healthy",
]

# Map each disease to its crop type
CROP_MAP = {
    "Tomato": ["Tomato Early Blight", "Tomato Late Blight", "Tomato Leaf Mold",
               "Tomato Yellow Leaf Curl", "Tomato Bacterial Spot", "Tomato Healthy"],
    "Potato": ["Potato Early Blight", "Potato Late Blight", "Potato Healthy"],
    "Corn":   ["Corn Common Rust", "Corn Gray Leaf Spot", "Corn Northern Leaf Blight", "Corn Healthy"],
    "Apple":  ["Apple Scab", "Apple Black Rot", "Apple Cedar Apple Rust", "Apple Healthy"],
}


def get_crop_from_disease(disease_name: str) -> str:
    """Return the crop name for a given disease."""
    for crop, diseases in CROP_MAP.items():
        if disease_name in diseases:
            return crop
    return "Unknown"


# ══════════════════════════════════════════════════════════════════════════════
# PHASE 2 — FAKE (STUB) PREDICTOR
# Returns a random disease with a realistic confidence score.
# Replace this function body in Phase 3 with real model inference.
# ══════════════════════════════════════════════════════════════════════════════

def predict_disease(image_path: str) -> tuple[str, float, str]:
    """
    Analyse a leaf image and return the predicted disease.

    Args:
        image_path : path to the uploaded image file

    Returns:
        (disease_name, confidence_percent, crop_name)
        e.g. ("Tomato Early Blight", 92.4, "Tomato")
    """
    # ── Validate image file exists ─────────────────────────────────────────────
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    # ══════════════════════════════════════════════════════════════════════════
    # PHASE 2: STUB — remove everything below and use Phase 3 code instead
    # ══════════════════════════════════════════════════════════════════════════
    disease_name = random.choice(CLASS_NAMES)
    confidence   = round(random.uniform(78.0, 98.5), 1)
    crop         = get_crop_from_disease(disease_name)
    return disease_name, confidence, crop

    # ══════════════════════════════════════════════════════════════════════════
    # PHASE 3: REAL MODEL — uncomment this block when model.h5 is ready
    # ══════════════════════════════════════════════════════════════════════════
    #
    # MODEL_PATH = "model.h5"
    # IMG_SIZE   = (224, 224)
    #
    # # Load model once (cached after first call)
    # if not hasattr(predict_disease, "_model"):
    #     predict_disease._model = load_model(MODEL_PATH)
    #
    # # Preprocess the image
    # img = keras_image.load_img(image_path, target_size=IMG_SIZE)
    # img_array = keras_image.img_to_array(img)           # shape: (224, 224, 3)
    # img_array = img_array / 255.0                        # normalize to [0, 1]
    # img_array = np.expand_dims(img_array, axis=0)        # shape: (1, 224, 224, 3)
    #
    # # Run inference
    # predictions  = predict_disease._model.predict(img_array)  # shape: (1, 17)
    # class_index  = int(np.argmax(predictions[0]))              # index of highest prob
    # confidence   = float(predictions[0][class_index]) * 100    # convert to percentage
    # disease_name = CLASS_NAMES[class_index]
    # crop         = get_crop_from_disease(disease_name)
    #
    # return disease_name, confidence, crop


# ── Quick test ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Create a dummy image file to test
    test_path = "test_leaf.jpg"
    with open(test_path, "wb") as f:
        f.write(b"fake_image_data")  # just for path validation

    disease, conf, crop = predict_disease(test_path)
    print(f"\nTest prediction:")
    print(f"  Disease    : {disease}")
    print(f"  Confidence : {conf}%")
    print(f"  Crop       : {crop}")

    os.remove(test_path)
