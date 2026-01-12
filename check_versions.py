import sys
import streamlit
import sklearn
import pandas as pd
import numpy as np
import joblib

print("VERSION CHECK")
print("=" * 50)
print(f"Python: {sys.version}")
print(f"Streamlit: {streamlit.__version__}")
print(f"scikit-learn: {sklearn.__version__}")
print(f"Pandas: {pd.__version__}")
print(f"NumPy: {np.__version__}")
print(f"Joblib: {joblib.__version__}")

# Check file paths
import os
print("\nFILE PATH CHECK")
print("=" * 50)

files_to_check = [
    'week2/models_retrained/random_forest.pkl',
    'week2/models_retrained/scaler_retrained.pkl',
    'data/processed/train.csv'
]

for file in files_to_check:
    exists = os.path.exists(file)
    if exists:
        size = os.path.getsize(file)
        print(f"✓ {file}: {size:,} bytes")
    else:
        print(f"✗ {file}: NOT FOUND")

# Check working directory
print(f"\nWorking directory: {os.getcwd()}")
