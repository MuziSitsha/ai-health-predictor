import re

# Read the app.py file
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

print("Looking for problematic lines...")

# Find and replace the model loading line
if 'model = joblib.load("week2/models_retrained/random_forest.pkl")' in content:
    print("Found model loading line")
    
    # Replace with better version
    new_model_load = '''        # Try multiple paths for model
        model = None
        model_paths = ["week2/models_retrained/random_forest.pkl", "./week2/models_retrained/random_forest.pkl", "random_forest.pkl", "./random_forest.pkl"]
        for path in model_paths:
            try:
                import os
                if os.path.exists(path):
                    model = joblib.load(path)
                    break
            except:
                continue'''
    
    content = content.replace(
        '        model = joblib.load("week2/models_retrained/random_forest.pkl")',
        new_model_load
    )

# Find and replace the scaler loading line
if 'scaler = joblib.load("week2/models_retrained/scaler_retrained.pkl")' in content:
    print("Found scaler loading line")
    
    new_scaler_load = '''        # Try multiple paths for scaler
        scaler = None
        scaler_paths = ["week2/models_retrained/scaler_retrained.pkl", "./week2/models_retrained/scaler_retrained.pkl", "scaler_retrained.pkl", "./scaler_retrained.pkl"]
        for path in scaler_paths:
            try:
                import os
                if os.path.exists(path):
                    scaler = joblib.load(path)
                    break
            except:
                continue'''
    
    content = content.replace(
        '        scaler = joblib.load("week2/models_retrained/scaler_retrained.pkl")',
        new_scaler_load
    )

# Find and replace the train.csv line and feature_names
lines = content.split('\n')
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    if 'train_df = pd.read_csv("data/processed/train.csv")' in line:
        print("Found train.csv line")
        # Skip this line and the next one (feature_names line)
        i += 2
        # Add our hardcoded feature names
        new_lines.append('        # Define feature names (from Pima Indians Diabetes Dataset)')
        new_lines.append('        feature_names = [')
        new_lines.append('            "Pregnancies", ')
        new_lines.append('            "Glucose", ')
        new_lines.append('            "BloodPressure", ')
        new_lines.append('            "SkinThickness", ')
        new_lines.append('            "Insulin", ')
        new_lines.append('            "BMI", ')
        new_lines.append('            "DiabetesPedigreeFunction", ')
        new_lines.append('            "Age"')
        new_lines.append('        ]')
    else:
        new_lines.append(line)
        i += 1

content = '\n'.join(new_lines)

# Write back
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed app.py successfully!")
