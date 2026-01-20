import streamlit as st
import joblib
import os

print("Testing model loading...")

# Test the paths your app uses
paths_to_test = [
    "models/random_forest.pkl",
    "./models/random_forest.pkl",
    "random_forest.pkl",
    "./random_forest.pkl"
]

for path in paths_to_test:
    print(f"\nTrying: {path}")
    if os.path.exists(path):
        try:
            model = joblib.load(path)
            print(f"✓ SUCCESS: Loaded {type(model)}")
        except Exception as e:
            print(f"✗ ERROR: {e}")
    else:
        print(f"✗ File not found")

print("\n" + "="*50)
print("Testing scaler...")
scaler_paths = [
    "models/scaler_retrained.pkl",
    "./models/scaler_retrained.pkl",
    "scaler_retrained.pkl",
    "./scaler_retrained.pkl"
]

for path in scaler_paths:
    print(f"\nTrying: {path}")
    if os.path.exists(path):
        try:
            scaler = joblib.load(path)
            print(f"✓ SUCCESS: Loaded {type(scaler)}")
        except Exception as e:
            print(f"✗ ERROR: {e}")
    else:
        print(f"✗ File not found")
