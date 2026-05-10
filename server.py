# =========================
# 1. IMPORTS
# =========================
import os
import uuid
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from predict import predict_disease
from database import get_treatment
from translator import translate_text


# =========================
# 2. APP INIT (VERY IMPORTANT)
# =========================
app = Flask(__name__)
CORS(app)


# =========================
# 3. CONFIG
# =========================
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_FILE_SIZE_MB = 10

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================
# 4. HELPER
# =========================
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# =========================
# 5. HEALTH ROUTE
# =========================
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "FarmAI API is running"})


# =========================
# 6. PREDICT ROUTE
# =========================
@app.route("/predict-disease", methods=["POST"])
def predict():

    # ── Validate request ──
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename.strip() == "":
        return jsonify({"error": "Empty filename"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    # ── Save file ──
    unique_name = f"{uuid.uuid4()}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, unique_name)

    try:
        file.save(filepath)
        print(f"📂 Saved: {filepath}")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # ── Prediction ──
    try:
        print("🧠 Running prediction...")
        disease_name, confidence, crop = predict_disease(filepath)

    except Exception as e:
        import traceback
        traceback.print_exc()

        if os.path.exists(filepath):
            os.remove(filepath)

        return jsonify({
            "error": str(e),
            "type": type(e).__name__
        }), 500

    # ── Treatment ──
    try:
        treatment = get_treatment(disease_name)
    except:
        treatment = {
            "chemical": "Not available",
            "organic": "Not available",
            "prevention": "Not available",
            "severity": "Unknown"
        }

    # ── Translation ──
    language = request.form.get("language", "en")

    translated = {}

    if language != "en":

        try:

            translated = {

                "disease": translate_text(
                    disease_name,
                    language
                ),

                "symptoms": translate_text(
                    treatment.get("symptoms", ""),
                    language
                ),

                "chemical": translate_text(
                    treatment.get("chemical", ""),
                    language
                ),

                "chemical_dose": translate_text(
                    treatment.get("chemical_dose", ""),
                    language
                ),

                "organic": translate_text(
                    treatment.get("organic", ""),
                    language
                ),

                "organic_dose": translate_text(
                    treatment.get("organic_dose", ""),
                    language
                ),

                "prevention": translate_text(
                    treatment.get("prevention", ""),
                    language
                ),

                "pros": translate_text(
                    treatment.get("pros", ""),
                    language
                ),

                "cons": translate_text(
                    treatment.get("cons", ""),
                    language
                )

            }

            print("TRANSLATED:")
            print(translated)

        except Exception as e:

            print("TRANSLATION ERROR:")
            print(e)

    # ── Cleanup ──
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        print("Delete error:", e)

    # ── Response ──
    return jsonify({
        "status": "success",
        "disease": disease_name,
        "crop": crop,
        "confidence": round(confidence, 2),
        "severity": treatment.get("severity", "Medium"),
        "treatment": treatment,
        "translated": translated,
        "language": language
    })


# =========================
# 7. OTHER ROUTES
# =========================
@app.route("/get-treatment/<path:disease_name>", methods=["GET"])
def get_treatment_route(disease_name):
    treatment = get_treatment(disease_name)
    return jsonify({"disease": disease_name, "treatment": treatment})


@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()

    if not data or "text" not in data or "target_lang" not in data:
        return jsonify({"error": "Invalid request"}), 400

    translated = translate_text(data["text"], data["target_lang"])

    return jsonify({
        "original": data["text"],
        "translated": translated,
        "language": data["target_lang"]
    })


@app.route("/diseases", methods=["GET"])
def list_diseases():
    from database import get_all_diseases
    diseases = get_all_diseases()
    return jsonify({"diseases": diseases, "count": len(diseases)})


@app.route("/")
def home():
    return render_template("index.html")


# =========================
# 8. RUN
# =========================
if __name__ == "__main__":
    print("🌱 FarmAI Backend running on http://127.0.0.1:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)