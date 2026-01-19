#!/usr/bin/env python3
import os
import sys

print("Testing app.py requirements...")

# Check if we can import the necessary modules
try:
    import streamlit
    print("✓ streamlit")
except: print("✗ streamlit")

try:
    import joblib
    print("✓ joblib")
except: print("✗ joblib")

try:
    import sklearn
    print("✓ scikit-learn")
except: print("✗ scikit-learn")

print("\nChecking file paths...")
files = [
    ("random_forest.pkl", "Model in root"),
    ("scaler_retrained.pkl", "Scaler in root"),
    ("week2/models_retrained/random_forest.pkl", "Model in week2"),
    ("week2/models_retrained/scaler_retrained.pkl", "Scaler in week2"),
    ("data/processed/train.csv", "Train data")
]

for filepath, desc in files:
    if os.path.exists(filepath):
        print(f"✓ {desc}: {filepath}")
    else:
        print(f"✗ {desc}: {filepath}")

print("\nTesting model loading...")
try:
    # Try to import the load_model function
    with open('app.py', 'r') as f:
        code = f.read()
    
    # Extract the load_model function
    import re
    match = re.search(r'def load_model\(\):.*?return model, scaler, feature_names', code, re.DOTALL)
    if match:
        print("✓ load_model function found in app.py")
        
        # Try to execute just that function
        exec_lines = [
            'import joblib',
            'import os',
            'def mock_st():',
            '    class Mock:',
            '        def error(self, msg): print(f"ERROR: {msg}")',
            '        def success(self, msg): print(f"SUCCESS: {msg}")',
            '    return Mock()',
            'st = mock_st()',
            match.group(0)
        ]
        
        exec('\n'.join(exec_lines))
        
        # Try to call it
        try:
            result = load_model()
            if result[0] is not None and result[1] is not None:
                print("✓ load_model executed successfully")
                print(f"  Model type: {type(result[0])}")
                print(f"  Scaler type: {type(result[1])}")
                print(f"  Features: {result[2]}")
            else:
                print("✗ load_model returned None (file not found)")
        except Exception as e:
            print(f"✗ Error executing load_model: {e}")
    else:
        print("✗ Could not find load_model function")
        
except Exception as e:
    print(f"Error: {e}")

print("\nTest complete!")
