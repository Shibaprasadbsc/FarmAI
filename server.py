"""
FarmAI Backend — server.py
===========================
This is the main Flask application.
Run it with:  python server.py
It will start a local server at http://127.0.0.1:5000
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from predict import predict_disease          # our AI module (Phase 3)
from database import get_treatment           # our DB module
from translator import translate_text        # our translator module

# ── App setup ──────────────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)   # allows the frontend (different port) to talk to this server

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_FILE_SIZE_MB = 10

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ── Helper ─────────────────────────────────────────────────────────────────────
def allowed_file(filename):
    """Return True if the file extension is in our allowed list."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ══════════════════════════════════════════════════════════════════════════════
# ENDPOINT 1 — Health check
# GET /health
# Purpose : lets the frontend (or Render/Heroku) verify the server is alive.
# ══════════════════════════════════════════════════════════════════════════════
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "FarmAI API is running"})


# ══════════════════════════════════════════════════════════════════════════════
# ENDPOINT 2 — Predict disease
# POST /predict-disease
# Body : multipart/form-data  →  field "file" (image) + optional "language"
# Returns : JSON with disease name, confidence, crop, treatment, translation
# ══════════════════════════════════════════════════════════════════════════════
@app.route("/predict-disease", methods=["POST"])
def predict():
    # ── 1. Validate file was sent ──────────────────────────────────────────────
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded. Send an image in the 'file' field."}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename. Please select an image."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": f"Invalid file type. Allowed: {ALLOWED_EXTENSIONS}"}), 400

    # ── 2. Save file temporarily ───────────────────────────────────────────────
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # ── 3. Run AI model ────────────────────────────────────────────────────────
    try:
        disease_name, confidence, crop = predict_disease(filepath)
    except Exception as e:
        return jsonify({"error": f"Model prediction failed: {str(e)}"}), 500

    # ── 4. Get treatment from database ─────────────────────────────────────────
    treatment = get_treatment(disease_name)

    # ── 5. Translate if needed ─────────────────────────────────────────────────
    language = request.form.get("language", "en")   # default English
    translated = {}
    if language != "en":
        translated = {
            "disease":    translate_text(disease_name, language),
            "chemical":   translate_text(treatment["chemical"], language),
            "organic":    translate_text(treatment["organic"], language),
            "prevention": translate_text(treatment["prevention"], language),
        }

    # ── 6. Clean up uploaded file ──────────────────────────────────────────────
    os.remove(filepath)

    # ── 7. Build and return response ───────────────────────────────────────────
    return jsonify({
        "status":     "success",
        "disease":    disease_name,
        "crop":       crop,
        "confidence": round(confidence, 2),
        "severity":   treatment.get("severity", "Medium"),
        "treatment":  treatment,
        "translated": translated,
        "language":   language,
    })


# ══════════════════════════════════════════════════════════════════════════════
# ENDPOINT 3 — Get treatment for a known disease name
# GET /get-treatment/<disease_name>
# Example : GET /get-treatment/Tomato Early Blight
# ══════════════════════════════════════════════════════════════════════════════
@app.route("/get-treatment/<path:disease_name>", methods=["GET"])
def get_treatment_route(disease_name):
    treatment = get_treatment(disease_name)
    if not treatment:
        return jsonify({"error": f"No treatment found for: {disease_name}"}), 404
    return jsonify({"disease": disease_name, "treatment": treatment})


# ══════════════════════════════════════════════════════════════════════════════
# ENDPOINT 4 — Translate any text
# POST /translate
# Body : JSON  →  { "text": "...", "target_lang": "hi" }
# ══════════════════════════════════════════════════════════════════════════════
@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    if not data or "text" not in data or "target_lang" not in data:
        return jsonify({"error": "Send JSON with 'text' and 'target_lang' fields."}), 400
    translated = translate_text(data["text"], data["target_lang"])
    return jsonify({"original": data["text"], "translated": translated, "language": data["target_lang"]})


# ══════════════════════════════════════════════════════════════════════════════
# ENDPOINT 5 — List all supported diseases
# GET /diseases
# ══════════════════════════════════════════════════════════════════════════════
@app.route("/diseases", methods=["GET"])
def list_diseases():
    from database import get_all_diseases
    diseases = get_all_diseases()
    return jsonify({"diseases": diseases, "count": len(diseases)})


# ── Run ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("🌱 FarmAI Backend starting on http://127.0.0.1:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)
