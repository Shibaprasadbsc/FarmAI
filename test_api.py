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

# ── TEST 5: Predict disease (with a dummy image) ──────────────────────────────
separator("POST /predict-disease  (dummy image)")
# Create a tiny dummy image file
dummy_path = "dummy_leaf.jpg"
with open(dummy_path, "wb") as f:
    # Minimal valid JPEG header so Flask accepts it
    f.write(bytes([
        0xFF,0xD8,0xFF,0xE0,0x00,0x10,0x4A,0x46,0x49,0x46,0x00,0x01,
        0x01,0x00,0x00,0x01,0x00,0x01,0x00,0x00,0xFF,0xD9
    ]))

with open(dummy_path, "rb") as f:
    r = requests.post(f"{BASE_URL}/predict-disease",
        files={"file": ("dummy_leaf.jpg", f, "image/jpeg")},
        data={"language": "hi"}
    )
show(r)

os.remove(dummy_path)

# ── TEST 6: Error handling ─────────────────────────────────────────────────────
separator("POST /predict-disease  (no file — should return error)")
r = requests.post(f"{BASE_URL}/predict-disease")
show(r)

print(f"\n{'='*50}")
print("  All tests done!")
print(f"{'='*50}\n")
