#!/usr/bin/env python3
"""
Script to fix the app.py model loading issues (without Unicode)
"""

# Read the current app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and fix the load_model function
old_load_model = '''# Load model
@st.cache_resource
def load_model():
    try:
        model = joblib.load("week2/models_retrained/random_forest.pkl")
        scaler = joblib.load("week2/models_retrained/scaler_retrained.pkl")
        train_df = pd.read_csv("data/processed/train.csv")
        feature_names = [col for col in train_df.columns if col != 'Outcome']
        return model, scaler, feature_names
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None, None, None'''

# Replace with fixed version
new_load_model = '''# Load model
@st.cache_resource
def load_model():
    try:
        # Try multiple possible locations for model files
        model_paths = [
            "week2/models_retrained/random_forest.pkl",
            "./week2/models_retrained/random_forest.pkl",
            "random_forest.pkl",
            "./random_forest.pkl"
        ]
        
        scaler_paths = [
            "week2/models_retrained/scaler_retrained.pkl",
            "./week2/models_retrained/scaler_retrained.pkl",
            "scaler_retrained.pkl",
            "./scaler_retrained.pkl"
        ]
        
        model = None
        scaler = None
        
        # Try to load model from different paths
        for path in model_paths:
            try:
                import os
                if os.path.exists(path):
                    model = joblib.load(path)
                    st.success(f"Model loaded from: {path}")
                    break
            except Exception as e:
                continue
        
        # Try to load scaler from different paths
        for path in scaler_paths:
            try:
                import os
                if os.path.exists(path):
                    scaler = joblib.load(path)
                    st.success(f"Scaler loaded from: {path}")
                    break
            except Exception as e:
                continue
        
        # Define feature names (since train.csv doesn't exist)
        # These are from the Pima Indians Diabetes Dataset
        feature_names = [
            "Pregnancies", 
            "Glucose", 
            "BloodPressure", 
            "SkinThickness", 
            "Insulin", 
            "BMI", 
            "DiabetesPedigreeFunction", 
            "Age"
        ]
        
        return model, scaler, feature_names
        
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        import traceback
        st.error(f"Traceback: {traceback.format_exc()}")
        return None, None, None'''

# Replace the old function with the new one
if old_load_model in content:
    content = content.replace(old_load_model, new_load_model)
    print("Fixed load_model function")
else:
    print("Could not find exact load_model function pattern")
    
# Also fix the make_prediction function to handle missing model gracefully
old_make_prediction = '''    # Function to make prediction
    def make_prediction(features_array):
        if model is not None and scaler is not None:
            try:
                features_scaled = scaler.transform(features_array)
                prediction = model.predict(features_scaled)[0]
                prediction_proba = model.predict_proba(features_scaled)[0][1]
                return prediction, prediction_proba
            except Exception as e:
                st.error(f"Prediction error: {str(e)}")
                return None, None
        return None, None'''

new_make_prediction = '''    # Function to make prediction
    def make_prediction(features_array):
        if model is not None and scaler is not None:
            try:
                # Scale features
                features_scaled = scaler.transform(features_array)
                
                # Make prediction
                prediction = model.predict(features_scaled)[0]
                
                # Get probability if available
                if hasattr(model, 'predict_proba'):
                    prediction_proba = model.predict_proba(features_scaled)[0][1]
                else:
                    # Default to 0.5 if no probability available
                    prediction_proba = 0.5 if prediction == 1 else 0.5
                    
                return prediction, prediction_proba
                
            except Exception as e:
                st.error(f"Prediction error: {str(e)}")
                import traceback
                st.error(f"Error details: {traceback.format_exc()}")
                return None, None
        else:
            st.error("Model or scaler not loaded properly")
            return None, None'''

if old_make_prediction in content:
    content = content.replace(old_make_prediction, new_make_prediction)
    print("Fixed make_prediction function")
else:
    print("Could not find exact make_prediction function pattern")

# Write the fixed content back to app.py
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated app.py with fixed model loading")
print("\nNext steps:")
print("1. Run: git add app.py")
print("2. Run: git commit -m 'Fix model loading in app.py'")
print("3. Run: git push origin main")
