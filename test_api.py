"""
FarmAI Backend — test_api.py
==============================
Test every API endpoint without needing Postman.
Run with:  python test_api.py

Make sure server.py is running in another terminal first!
"""

import requests
import json
import os

BASE_URL = "http://127.0.0.1:5000"

def separator(title):
    print(f"\n{'─'*50}")
    print(f"  TEST: {title}")
    print('─'*50)

def show(response):
    print(f"  Status : {response.status_code}")
    try:
        data = response.json()
        print(f"  Body   : {json.dumps(data, indent=4, ensure_ascii=False)[:600]}")
    except:
        print(f"  Body   : {response.text[:200]}")


# ── TEST 1: Health check ───────────────────────────────────────────────────────
separator("GET /health")
r = requests.get(f"{BASE_URL}/health")
show(r)

# ── TEST 2: List all diseases ──────────────────────────────────────────────────
separator("GET /diseases")
r = requests.get(f"{BASE_URL}/diseases")
show(r)

# ── TEST 3: Get treatment for a disease ───────────────────────────────────────
separator("GET /get-treatment/Tomato Early Blight")
r = requests.get(f"{BASE_URL}/get-treatment/Tomato Early Blight")
show(r)

# ── TEST 4: Translate text ────────────────────────────────────────────────────
separator("POST /translate  →  Hindi")
r = requests.post(f"{BASE_URL}/translate", json={
    "text": "Tomato Early Blight",
    "target_lang": "hi"
})
show(r)

# ── TEST 5: Predict disease (with a real image) ──────────────────────────────
separator("POST /predict-disease  (real image)")

image_path = "uploads/test.jpg"

with open(image_path, "rb") as f:
    r = requests.post(
        f"{BASE_URL}/predict-disease",
        files={"file": ("test.jpg", f, "image/jpeg")},
        data={"language": "hi"}
    )

show(r)


# ── TEST 6: Error handling ─────────────────────────────────────────────────────
separator("POST /predict-disease  (no file — should return error)")
r = requests.post(f"{BASE_URL}/predict-disease")
show(r)

print(f"\n{'='*50}")
print("  All tests done!")
print(f"{'='*50}\n")
