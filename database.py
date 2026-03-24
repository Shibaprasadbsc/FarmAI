"""
FarmAI Backend — database.py
==============================
Sets up the SQLite database and provides functions to
read disease and treatment information.

Run this file once to create the database:
    python database.py
"""

import sqlite3
import os

DB_PATH = "farmai.db"


# ══════════════════════════════════════════════════════════════════════════════
# DATABASE SETUP
# Creates tables and fills them with disease/treatment data
# ══════════════════════════════════════════════════════════════════════════════

DISEASE_DATA = [
    # (disease_name, crop, symptoms, severity)
    ("Tomato Early Blight",         "Tomato",  "Brown spots with concentric rings on older leaves. Yellow halo.",           "Medium"),
    ("Tomato Late Blight",          "Tomato",  "Water-soaked grey-green patches turning brown. White mold on underside.",   "High"),
    ("Tomato Leaf Mold",            "Tomato",  "Pale green-yellow spots on upper leaf. Olive-green mold underneath.",       "Medium"),
    ("Tomato Yellow Leaf Curl",     "Tomato",  "Upward leaf curling, yellowing, stunted growth. Spread by whiteflies.",    "High"),
    ("Tomato Bacterial Spot",       "Tomato",  "Small dark water-soaked spots with yellow halo. Spots turn brown.",        "Medium"),
    ("Tomato Healthy",              "Tomato",  "No disease detected. Crop appears healthy.",                               "None"),
    ("Potato Early Blight",         "Potato",  "Dark brown circular lesions with concentric rings on older leaves.",       "Medium"),
    ("Potato Late Blight",          "Potato",  "Rapidly spreading brown lesions. White mold in humid conditions.",         "High"),
    ("Potato Healthy",              "Potato",  "No disease detected. Crop appears healthy.",                               "None"),
    ("Corn Common Rust",            "Corn",    "Powdery orange-brown pustules on both leaf surfaces.",                     "Medium"),
    ("Corn Gray Leaf Spot",         "Corn",    "Rectangular gray-tan lesions along leaf veins.",                           "Medium"),
    ("Corn Northern Leaf Blight",   "Corn",    "Long cigar-shaped gray-green lesions on leaves.",                         "High"),
    ("Corn Healthy",                "Corn",    "No disease detected. Crop appears healthy.",                               "None"),
    ("Apple Scab",                  "Apple",   "Olive-green to brown scabby lesions on leaves and fruit.",                "High"),
    ("Apple Black Rot",             "Apple",   "Brown circular spots on leaves. Dark sunken rot on fruit.",               "High"),
    ("Apple Cedar Apple Rust",      "Apple",   "Bright orange-yellow spots on upper leaf surface.",                       "Medium"),
    ("Apple Healthy",               "Apple",   "No disease detected. Crop appears healthy.",                              "None"),
]

TREATMENT_DATA = [
    # (disease_name, chemical, chemical_dose, organic, organic_dose, pros, cons, prevention)
    (
        "Tomato Early Blight",
        "Mancozeb 75% WP",
        "2.5g per litre of water. Spray every 7–10 days. Stop 7 days before harvest.",
        "Neem Oil 3%",
        "Mix 30ml neem oil + 1L water + 2 drops dish soap. Spray every 5 days in morning.",
        "Fast-acting. Widely available. Low cost (Rs 80/kg).",
        "Chemical residue on produce. Harmful to bees. Wear gloves.",
        "Avoid overhead irrigation. Crop rotation every 2 seasons. Remove infected leaves immediately.",
    ),
    (
        "Tomato Late Blight",
        "Metalaxyl + Mancozeb (Ridomil Gold)",
        "2g per litre of water. Spray at first sign. Repeat every 7 days.",
        "Copper Hydroxide",
        "2g per litre of water. Spray weekly. Do not apply in temperatures above 35°C.",
        "Highly effective if caught early. Systemic — absorbed into plant.",
        "Expensive. Resistance can develop. Do not overuse.",
        "Plant resistant varieties. Avoid wetting leaves. Increase plant spacing. Destroy infected plants.",
    ),
    (
        "Tomato Leaf Mold",
        "Chlorothalonil 75% WP",
        "2g per litre. Spray both sides of leaves every 10 days.",
        "Baking Soda Spray",
        "5g baking soda + 1L water + few drops soap. Spray weekly.",
        "Effective in greenhouse conditions. Broad spectrum.",
        "Moderate cost. May cause slight leaf burn if overused.",
        "Improve greenhouse ventilation. Reduce humidity below 85%. Prune lower leaves.",
    ),
    (
        "Tomato Yellow Leaf Curl",
        "Imidacloprid 17.8% SL (targets whitefly vector)",
        "0.3ml per litre. Spray on leaf undersides where whiteflies hide.",
        "Neem Oil + Yellow Sticky Traps",
        "Neem oil 3% spray + hang 1 yellow sticky trap per 10 plants.",
        "Controls whitefly spread quickly.",
        "No direct cure for virus — only prevents spread. Early action is critical.",
        "Use virus-resistant tomato varieties. Remove heavily infected plants. Control weeds around field.",
    ),
    (
        "Tomato Bacterial Spot",
        "Copper Oxychloride 50% WP",
        "3g per litre. Apply every 7 days starting at first symptom.",
        "Bordeaux Mixture (1%)",
        "Mix 10g copper sulfate + 10g lime + 1L water. Apply weekly.",
        "Controls bacterial and fungal issues together.",
        "Can cause copper toxicity in soil if overused.",
        "Use disease-free seeds. Avoid working in field when leaves are wet. Sterilize tools.",
    ),
    (
        "Tomato Healthy",
        "No treatment needed",
        "Continue regular care and monitoring.",
        "No treatment needed",
        "Continue regular care and monitoring.",
        "Crop is healthy.",
        "Continue monitoring weekly for early signs.",
        "Maintain regular watering schedule. Use balanced fertilizer. Monitor weekly.",
    ),
    (
        "Potato Early Blight",
        "Mancozeb 75% WP",
        "2.5g per litre. Spray every 7 days. Begin at plant emergence.",
        "Neem Oil 3%",
        "30ml neem oil + 1L water. Spray every 5 days.",
        "Preventive treatment before disease spreads widely.",
        "Needs repeated application. Chemical residue concern.",
        "Destroy infected plant debris after harvest. Plant certified seed potatoes.",
    ),
    (
        "Potato Late Blight",
        "Cymoxanil + Mancozeb (Curzate)",
        "2.5g per litre. Spray every 5–7 days. Critical to act fast.",
        "Copper Hydroxide 77%",
        "2.5g per litre. Spray weekly. Apply before rain if possible.",
        "Very effective if started early. Systemic protection.",
        "Disease spreads extremely fast — even one missed spray matters.",
        "Plant resistant varieties (Kufri Jyoti). Avoid irrigating at night. Remove volunteer potato plants.",
    ),
    (
        "Potato Healthy",
        "No treatment needed",
        "Continue regular care and monitoring.",
        "No treatment needed",
        "Continue regular care and monitoring.",
        "Crop is healthy.",
        "Continue monitoring weekly.",
        "Maintain regular watering. Avoid over-fertilizing with nitrogen.",
    ),
    (
        "Corn Common Rust",
        "Propiconazole 25% EC",
        "1ml per litre. Spray at first pustule appearance.",
        "Sulfur Dust 80% WP",
        "20g per litre. Apply as fine dust in early morning.",
        "Fast knockdown of fungal spores.",
        "Propiconazole is costly. Sulfur can cause phytotoxicity in heat.",
        "Plant rust-resistant hybrid varieties. Avoid dense planting.",
    ),
    (
        "Corn Gray Leaf Spot",
        "Azoxystrobin 23% SC",
        "1ml per litre. Spray at silking stage (most vulnerable).",
        "Trichoderma viride (biological)",
        "5g per litre. Soil drench + foliar spray. Apply preventively.",
        "Azoxystrobin provides long residual protection (2–3 weeks).",
        "Expensive. Requires precise timing at silking.",
        "Crop rotation with non-host crop. Till infected residue into soil. Plant early-maturing varieties.",
    ),
    (
        "Corn Northern Leaf Blight",
        "Mancozeb + Carbendazim",
        "2.5g per litre. Spray at disease onset. Repeat every 10 days.",
        "Neem Oil 3%",
        "30ml per litre. Spray every 7 days.",
        "Effective and low-cost combination.",
        "Must be applied early — less effective once >50% leaf area infected.",
        "Use resistant hybrids. Rotate with non-cereal crops. Remove crop debris after harvest.",
    ),
    (
        "Corn Healthy",
        "No treatment needed",
        "Continue regular care and monitoring.",
        "No treatment needed",
        "Continue regular care and monitoring.",
        "Crop is healthy.",
        "Continue monitoring weekly.",
        "Monitor for insect damage and nutrient deficiency as well.",
    ),
    (
        "Apple Scab",
        "Captan 50% WP",
        "2.5g per litre. Begin spraying at green tip stage. Repeat every 10 days.",
        "Lime Sulfur 3%",
        "Spray during dormant season before bud break. Highly effective preventive.",
        "Captan is broad-spectrum and affordable.",
        "Lime sulfur has strong smell. Cannot use near harvest.",
        "Rake and destroy fallen leaves in autumn. Prune for open canopy. Plant scab-resistant varieties.",
    ),
    (
        "Apple Black Rot",
        "Thiophanate-methyl 70% WP",
        "1.5g per litre. Spray from pink stage through petal fall.",
        "Bordeaux Mixture 1%",
        "Apply after pruning wounds and before rain.",
        "Systemic fungicide — moves into plant tissue.",
        "Resistance develops if used every season — rotate with other fungicides.",
        "Remove and destroy mummified fruit. Prune out dead wood. Sterilize pruning tools with alcohol.",
    ),
    (
        "Apple Cedar Apple Rust",
        "Myclobutanil 20% WP",
        "1g per litre. Spray from tight cluster through cover sprays.",
        "Sulfur Spray",
        "3g per litre. Apply every 7–10 days during wet spring weather.",
        "Highly effective — stops spore germination.",
        "Cannot be applied after petal fall (phytotoxicity risk).",
        "Remove nearby juniper/cedar trees (alternate host). Plant rust-resistant varieties.",
    ),
    (
        "Apple Healthy",
        "No treatment needed",
        "Continue regular monitoring and standard care.",
        "No treatment needed",
        "Continue regular monitoring and standard care.",
        "Crop is healthy.",
        "Continue monitoring weekly.",
        "Maintain regular pruning for airflow. Keep orchard floor clean.",
    ),
]


def init_db():
    """Create the database tables and populate with data."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create diseases table
    c.execute("""
        CREATE TABLE IF NOT EXISTS diseases (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT UNIQUE NOT NULL,
            crop        TEXT NOT NULL,
            symptoms    TEXT NOT NULL,
            severity    TEXT NOT NULL
        )
    """)

    # Create treatments table
    c.execute("""
        CREATE TABLE IF NOT EXISTS treatments (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            disease_name    TEXT NOT NULL,
            chemical        TEXT NOT NULL,
            chemical_dose   TEXT NOT NULL,
            organic         TEXT NOT NULL,
            organic_dose    TEXT NOT NULL,
            pros            TEXT NOT NULL,
            cons            TEXT NOT NULL,
            prevention      TEXT NOT NULL,
            FOREIGN KEY (disease_name) REFERENCES diseases(name)
        )
    """)

    # Insert disease data (skip if already exists)
    c.executemany("""
        INSERT OR IGNORE INTO diseases (name, crop, symptoms, severity)
        VALUES (?, ?, ?, ?)
    """, DISEASE_DATA)

    # Insert treatment data (skip if already exists)
    c.executemany("""
        INSERT OR IGNORE INTO treatments
            (disease_name, chemical, chemical_dose, organic, organic_dose, pros, cons, prevention)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, TREATMENT_DATA)

    conn.commit()
    conn.close()
    print(f"✅ Database ready: {DB_PATH}")
    print(f"   {len(DISEASE_DATA)} diseases loaded")
    print(f"   {len(TREATMENT_DATA)} treatments loaded")


# ══════════════════════════════════════════════════════════════════════════════
# PUBLIC FUNCTIONS — called by server.py
# ══════════════════════════════════════════════════════════════════════════════

def get_treatment(disease_name: str) -> dict:
    """
    Given a disease name, return its full treatment info as a dict.
    Returns a default 'not found' dict if disease not in DB.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row          # lets us access columns by name
    c = conn.cursor()

    c.execute("""
        SELECT d.name, d.crop, d.symptoms, d.severity,
               t.chemical, t.chemical_dose, t.organic, t.organic_dose,
               t.pros, t.cons, t.prevention
        FROM diseases d
        LEFT JOIN treatments t ON d.name = t.disease_name
        WHERE d.name = ?
    """, (disease_name,))

    row = c.fetchone()
    conn.close()

    if not row:
        return {
            "disease":       disease_name,
            "crop":          "Unknown",
            "symptoms":      "Not found",
            "severity":      "Unknown",
            "chemical":      "Consult local agricultural officer",
            "chemical_dose": "—",
            "organic":       "Consult local agricultural officer",
            "organic_dose":  "—",
            "pros":          "—",
            "cons":          "—",
            "prevention":    "Monitor crop regularly",
        }

    return dict(row)


def get_all_diseases() -> list:
    """Return a list of all disease names in the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, crop, severity FROM diseases ORDER BY crop, name")
    rows = c.fetchall()
    conn.close()
    return [{"name": r[0], "crop": r[1], "severity": r[2]} for r in rows]


# ── Run directly to initialise the database ────────────────────────────────────
if __name__ == "__main__":
    init_db()
