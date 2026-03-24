"""
FarmAI Backend — setup.py
===========================
Run this ONE TIME to set up everything.
After this, just run:  python server.py
"""

import subprocess
import sys
import os

print("=" * 55)
print("  FarmAI Backend — First-time Setup")
print("=" * 55)

# Step 1: Install dependencies
print("\n[1/3] Installing Python packages...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
print("      ✅ Packages installed")

# Step 2: Create database
print("\n[2/3] Setting up database...")
from database import init_db
init_db()
print("      ✅ Database created (farmai.db)")

# Step 3: Quick test
print("\n[3/3] Running quick test...")
from predict import predict_disease
from database import get_treatment

# Create dummy image
with open("test.jpg", "wb") as f:
    f.write(b"test")

disease, conf, crop = predict_disease("test.jpg")
treatment = get_treatment(disease)
os.remove("test.jpg")

print(f"      ✅ Predict: {disease} ({conf}%) — {crop}")
print(f"      ✅ Treatment fetched: {treatment['chemical'][:40]}...")

print("\n" + "=" * 55)
print("  Setup complete! Now run:")
print()
print("      python server.py")
print()
print("  Then open in browser:")
print("      http://127.0.0.1:5000/health")
print("=" * 55)
