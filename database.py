"""
FarmAI Backend — database.py
==============================
Sets up the SQLite database and provides functions to
read disease and treatment information.

Run this file once to create the database:
    python database.py
"""

import sqlite3

DB_PATH = "farmai.db"

# ════════════════════════════════════════════════════════════════════════
# DISEASE DATA
# ════════════════════════════════════════════════════════════════════════

DISEASE_DATA = [

    # ================= APPLE =================
    ("Apple Scab", "Apple",
     "Olive-green to brown scabby lesions on leaves and fruit.", "High"),

    ("Apple Black Rot", "Apple",
     "Brown circular spots on leaves and dark sunken fruit rot.", "High"),

    ("Apple Cedar Apple Rust", "Apple",
     "Bright orange-yellow spots on leaves.", "Medium"),

    ("Apple Healthy", "Apple",
     "No disease detected. Crop appears healthy.", "None"),

    # ================= BLUEBERRY =================
    ("Blueberry Healthy", "Blueberry",
     "No disease detected. Plant appears healthy.", "None"),

    # ================= CHERRY =================
    ("Cherry Healthy", "Cherry",
     "No disease detected. Plant appears healthy.", "None"),

    ("Cherry Powdery Mildew", "Cherry",
     "White powdery fungal growth on leaves and shoots.", "Medium"),

    # ================= CORN =================
    ("Corn Common Rust", "Corn",
     "Powdery orange-brown pustules on leaves.", "Medium"),

    ("Corn Gray Leaf Spot", "Corn",
     "Rectangular gray-tan lesions along leaf veins.", "Medium"),

    ("Corn Northern Leaf Blight", "Corn",
     "Long cigar-shaped gray-green lesions.", "High"),

    ("Corn Healthy", "Corn",
     "No disease detected. Crop appears healthy.", "None"),

    # ================= GRAPE =================
    ("Grape Black Rot", "Grape",
     "Dark circular lesions on leaves and fruit.", "High"),

    ("Grape Esca", "Grape",
     "Leaf discoloration and wood decay.", "High"),

    ("Grape Leaf Blight", "Grape",
     "Brown dead patches on leaves.", "Medium"),

    ("Grape Healthy", "Grape",
     "No disease detected. Crop appears healthy.", "None"),

    # ================= ORANGE =================
    ("Orange Huanglongbing", "Orange",
     "Yellow shoots and blotchy mottled leaves.", "High"),

    # ================= PEACH =================
    ("Peach Bacterial Spot", "Peach",
     "Dark lesions on leaves and fruits.", "Medium"),

    ("Peach Healthy", "Peach",
     "No disease detected. Crop appears healthy.", "None"),

    # ================= PEPPER =================
    ("Pepper Bell Bacterial Spot", "Pepper",
     "Small water-soaked lesions on leaves and fruits.", "Medium"),

    ("Pepper Bell Healthy", "Pepper",
     "No disease detected. Crop appears healthy.", "None"),

    # ================= POTATO =================
    ("Potato Early Blight", "Potato",
     "Dark brown circular lesions with concentric rings.", "Medium"),

    ("Potato Late Blight", "Potato",
     "Rapidly spreading brown lesions with white mold.", "High"),

    ("Potato Healthy", "Potato",
     "No disease detected. Crop appears healthy.", "None"),

    # ================= RASPBERRY =================
    ("Raspberry Healthy", "Raspberry",
     "No disease detected. Crop appears healthy.", "None"),

    # ================= SOYBEAN =================
    ("Soybean Healthy", "Soybean",
     "No disease detected. Crop appears healthy.", "None"),

    # ================= SQUASH =================
    ("Squash Powdery Mildew", "Squash",
     "White powdery fungal growth on leaves.", "Medium"),

    # ================= STRAWBERRY =================
    ("Strawberry Leaf Scorch", "Strawberry",
     "Purple spots enlarging into scorched patches.", "Medium"),

    ("Strawberry Healthy", "Strawberry",
     "No disease detected. Crop appears healthy.", "None"),

    # ================= TOMATO =================
    ("Tomato Early Blight", "Tomato",
     "Brown spots with concentric rings on older leaves.", "Medium"),

    ("Tomato Late Blight", "Tomato",
     "Water-soaked patches turning brown with white mold.", "High"),

    ("Tomato Leaf Mold", "Tomato",
     "Yellow spots with olive-green mold underneath.", "Medium"),

    ("Tomato Bacterial Spot", "Tomato",
     "Small dark spots with yellow halo.", "Medium"),

    ("Tomato Septoria Leaf Spot", "Tomato",
     "Small circular spots with dark margins.", "Medium"),

    ("Tomato Target Spot", "Tomato",
     "Brown concentric spots on leaves.", "Medium"),

    ("Tomato Mosaic Virus", "Tomato",
     "Mottled leaves with green patches.", "High"),

    ("Tomato Spider Mites", "Tomato",
     "Yellow spots and webbing on leaves.", "Medium"),

    ("Tomato Yellow Leaf Curl Virus", "Tomato",
     "Leaf curling and yellowing caused by virus.", "High"),

    ("Tomato Healthy", "Tomato",
     "No disease detected. Crop appears healthy.", "None"),
]

# ════════════════════════════════════════════════════════════════════════
# TREATMENT DATA
# ════════════════════════════════════════════════════════════════════════

TREATMENT_DATA = [

    (
        "Apple Scab",
        "Captan 50% WP",
        "2.5g per litre",
        "Lime Sulfur",
        "Spray during dormant season",
        "Effective broad-spectrum control",
        "Strong smell and repeated use needed",
        "Destroy fallen leaves and prune trees",
    ),

    (
        "Apple Black Rot",
        "Thiophanate-methyl",
        "1.5g per litre",
        "Bordeaux Mixture",
        "Weekly spray",
        "Effective systemic fungicide",
        "Resistance may develop",
        "Remove infected fruit and branches",
    ),

    (
        "Apple Cedar Apple Rust",
        "Myclobutanil",
        "1g per litre",
        "Sulfur Spray",
        "3g per litre",
        "Prevents fungal spread",
        "Requires repeated spraying",
        "Remove nearby cedar trees",
    ),

    (
        "Apple Healthy",
        "No treatment needed",
        "Continue monitoring",
        "No treatment needed",
        "Continue monitoring",
        "Plant is healthy",
        "Continue weekly observation",
        "Maintain proper irrigation",
    ),

    (
        "Blueberry Healthy",
        "No treatment needed",
        "Continue monitoring",
        "No treatment needed",
        "Continue monitoring",
        "Plant is healthy",
        "Continue weekly observation",
        "Maintain proper nutrients",
    ),

    (
        "Cherry Powdery Mildew",
        "Sulfur Fungicide",
        "2g per litre",
        "Neem Oil",
        "30ml per litre",
        "Controls fungal growth",
        "Needs repeated application",
        "Improve airflow around plants",
    ),

    (
        "Cherry Healthy",
        "No treatment needed",
        "Continue monitoring",
        "No treatment needed",
        "Continue monitoring",
        "Plant is healthy",
        "Continue weekly observation",
        "Maintain proper watering",
    ),

    (
        "Corn Common Rust",
        "Propiconazole",
        "1ml per litre",
        "Sulfur Dust",
        "20g per litre",
        "Fast fungal control",
        "Can be costly",
        "Use resistant hybrids",
    ),

    (
        "Corn Gray Leaf Spot",
        "Azoxystrobin",
        "1ml per litre",
        "Trichoderma",
        "5g per litre",
        "Long residual protection",
        "Expensive treatment",
        "Rotate crops regularly",
    ),

    (
        "Corn Northern Leaf Blight",
        "Mancozeb + Carbendazim",
        "2.5g per litre",
        "Neem Oil",
        "30ml per litre",
        "Low-cost effective control",
        "Less effective in advanced stages",
        "Remove crop debris",
    ),

    (
        "Corn Healthy",
        "No treatment needed",
        "Continue monitoring",
        "No treatment needed",
        "Continue monitoring",
        "Plant is healthy",
        "Continue weekly observation",
        "Maintain soil fertility",
    ),

    (
        "Grape Black Rot",
        "Mancozeb",
        "2g per litre",
        "Neem Oil",
        "30ml per litre",
        "Controls fungal growth",
        "Needs early spraying",
        "Prune infected parts",
    ),

    (
        "Grape Esca",
        "No effective cure",
        "—",
        "Trichoderma",
        "Soil application",
        "Biological management possible",
        "Recovery is slow",
        "Avoid trunk injury",
    ),

    (
        "Grape Leaf Blight",
        "Copper Fungicide",
        "2g per litre",
        "Neem Oil",
        "30ml per litre",
        "Broad fungal control",
        "Repeated use required",
        "Remove infected leaves",
    ),

    (
        "Grape Healthy",
        "No treatment needed",
        "Continue monitoring",
        "No treatment needed",
        "Continue monitoring",
        "Plant is healthy",
        "Continue weekly observation",
        "Maintain proper pruning",
    ),

    (
        "Orange Huanglongbing",
        "No cure available",
        "—",
        "Neem Oil",
        "30ml per litre",
        "Controls psyllid insects",
        "Disease is fatal",
        "Remove infected trees",
    ),

    (
        "Peach Bacterial Spot",
        "Copper Oxychloride",
        "3g per litre",
        "Bordeaux Mixture",
        "Weekly spray",
        "Controls bacterial infection",
        "Copper buildup risk",
        "Use resistant varieties",
    ),

    (
        "Peach Healthy",
        "No treatment needed",
        "Continue monitoring",
        "No treatment needed",
        "Continue monitoring",
        "Plant is healthy",
        "Continue weekly observation",
        "Maintain orchard hygiene",
    ),

    (
        "Pepper Bell Bacterial Spot",
        "Copper Fungicide",
        "3g per litre",
        "Neem Oil",
        "30ml per litre",
        "Effective against bacteria",
        "Needs multiple sprays",
        "Avoid wet field operations",
    ),

    (
        "Pepper Bell Healthy",
        "No treatment needed",
        "Continue monitoring",
        "No treatment needed",
        "Continue monitoring",
        "Plant is healthy",
        "Continue weekly observation",
        "Maintain proper irrigation",
    ),

    (
        "Potato Early Blight",
        "Mancozeb",
        "2.5g per litre",
        "Neem Oil",
        "30ml per litre",
        "Effective preventive control",
        "Repeated application needed",
        "Use certified seeds",
    ),

    (
        "Potato Late Blight",
        "Cymoxanil + Mancozeb",
        "2.5g per litre",
        "Copper Hydroxide",
        "2.5g per litre",
        "Fast systemic protection",
        "Disease spreads rapidly",
        "Avoid night irrigation",
    ),

    (
        "Potato Healthy",
        "No treatment needed",
        "Continue monitoring",
        "No treatment needed",
        "Continue monitoring",
        "Plant is healthy",
        "Continue weekly observation",
        "Maintain balanced fertilization",
    ),

    (
        "Raspberry Healthy",
        "No treatment needed",
        "Continue monitoring",
        "No treatment needed",
        "Continue monitoring",
        "Plant is healthy",
        "Continue weekly observation",
        "Maintain proper nutrients",
    ),

    (
        "Soybean Healthy",
        "No treatment needed",
        "Continue monitoring",
        "No treatment needed",
        "Continue monitoring",
        "Plant is healthy",
        "Continue weekly observation",
        "Maintain healthy soil",
    ),

    (
        "Squash Powdery Mildew",
        "Sulfur Fungicide",
        "2g per litre",
        "Milk Spray",
        "1:10 milk-water ratio",
        "Eco-friendly treatment",
        "Less effective in severe infection",
        "Improve airflow",
    ),

    (
        "Strawberry Leaf Scorch",
        "Captan",
        "2g per litre",
        "Neem Oil",
        "30ml per litre",
        "Controls fungal spread",
        "Needs repeated spraying",
        "Avoid overhead irrigation",
    ),

    (
        "Strawberry Healthy",
        "No treatment needed",
        "Continue monitoring",
        "No treatment needed",
        "Continue monitoring",
        "Plant is healthy",
        "Continue weekly observation",
        "Maintain proper spacing",
    ),

    (
        "Tomato Early Blight",
        "Mancozeb",
        "2.5g per litre",
        "Neem Oil",
        "30ml per litre",
        "Fast fungal control",
        "Repeated spraying required",
        "Avoid overhead irrigation",
    ),

    (
        "Tomato Late Blight",
        "Metalaxyl + Mancozeb",
        "2g per litre",
        "Copper Hydroxide",
        "2g per litre",
        "Highly effective treatment",
        "Resistance can develop",
        "Increase plant spacing",
    ),

    (
        "Tomato Leaf Mold",
        "Chlorothalonil",
        "2g per litre",
        "Baking Soda Spray",
        "5g per litre",
        "Effective greenhouse control",
        "Can burn leaves if overused",
        "Reduce humidity",
    ),

    (
        "Tomato Bacterial Spot",
        "Copper Oxychloride",
        "3g per litre",
        "Bordeaux Mixture",
        "Weekly spray",
        "Controls bacteria effectively",
        "Copper toxicity possible",
        "Use disease-free seeds",
    ),

    (
        "Tomato Septoria Leaf Spot",
        "Mancozeb",
        "2.5g per litre",
        "Neem Oil",
        "30ml per litre",
        "Prevents rapid spread",
        "Needs early detection",
        "Remove infected leaves",
    ),

    (
        "Tomato Target Spot",
        "Chlorothalonil",
        "2g per litre",
        "Neem Oil",
        "30ml per litre",
        "Controls fungal spots",
        "Repeated spraying needed",
        "Ensure good airflow",
    ),

    (
        "Tomato Mosaic Virus",
        "No chemical cure",
        "—",
        "Neem Oil",
        "30ml per litre",
        "Prevents pest spread",
        "No direct cure available",
        "Remove infected plants",
    ),

    (
        "Tomato Spider Mites",
        "Abamectin",
        "0.5ml per litre",
        "Neem Oil",
        "30ml per litre",
        "Effective mite control",
        "Resistance may develop",
        "Maintain humidity",
    ),

    (
        "Tomato Yellow Leaf Curl Virus",
        "Imidacloprid",
        "0.3ml per litre",
        "Neem Oil + Sticky traps",
        "Use with yellow traps",
        "Controls whiteflies",
        "Virus cannot be cured",
        "Use resistant varieties",
    ),

    (
        "Tomato Healthy",
        "No treatment needed",
        "Continue monitoring",
        "No treatment needed",
        "Continue monitoring",
        "Plant is healthy",
        "Continue weekly observation",
        "Maintain balanced fertilization",
    ),
]

# ════════════════════════════════════════════════════════════════════════
# DATABASE FUNCTIONS
# ════════════════════════════════════════════════════════════════════════

def init_db():

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS diseases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            crop TEXT NOT NULL,
            symptoms TEXT NOT NULL,
            severity TEXT NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS treatments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease_name TEXT NOT NULL,
            chemical TEXT NOT NULL,
            chemical_dose TEXT NOT NULL,
            organic TEXT NOT NULL,
            organic_dose TEXT NOT NULL,
            pros TEXT NOT NULL,
            cons TEXT NOT NULL,
            prevention TEXT NOT NULL
        )
    """)

    c.executemany("""
        INSERT OR IGNORE INTO diseases
        (name, crop, symptoms, severity)
        VALUES (?, ?, ?, ?)
    """, DISEASE_DATA)

    c.executemany("""
        INSERT OR IGNORE INTO treatments
        (disease_name, chemical, chemical_dose,
         organic, organic_dose, pros, cons, prevention)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, TREATMENT_DATA)

    conn.commit()
    conn.close()

    print("✅ Database initialized successfully")
    print(f"✅ Loaded {len(DISEASE_DATA)} diseases")
    print(f"✅ Loaded {len(TREATMENT_DATA)} treatments")


def get_treatment(disease_name):

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("""
        SELECT d.name, d.crop, d.symptoms, d.severity,
               t.chemical, t.chemical_dose,
               t.organic, t.organic_dose,
               t.pros, t.cons, t.prevention
        FROM diseases d
        LEFT JOIN treatments t
        ON d.name = t.disease_name
        WHERE d.name = ?
    """, (disease_name,))

    row = c.fetchone()
    conn.close()

    if not row:
        return {
            "disease": disease_name,
            "crop": "Unknown",
            "symptoms": "Not found",
            "severity": "Unknown",
        }

    return dict(row)


def get_all_diseases():

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT name, crop, severity
        FROM diseases
        ORDER BY crop, name
    """)

    rows = c.fetchall()
    conn.close()

    return [
        {
            "name": r[0],
            "crop": r[1],
            "severity": r[2]
        }
        for r in rows
    ]


if __name__ == "__main__":

    init_db()