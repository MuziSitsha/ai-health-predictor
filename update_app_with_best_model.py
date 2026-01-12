import json

print("Updating Streamlit app with best model...")

try:
    with open('week3/final_model_selection.json', 'r') as f:
        decision = json.load(f)
    
    best_model = decision['best_model']
    best_model_path = decision['best_model_path']
    
    print(f"Best model: {best_model}")
    print(f"Model path: {best_model_path}")
    
    # Check current app.py
    with open('app.py', 'r') as f:
        app_content = f.read()
    
    # Simple check
    if 'load_model' in app_content or 'joblib.load' in app_content:
        print("\nYour app.py already has model loading code.")
        print("Please update it manually to use:")
        print(f"  Model: {best_model}")
        print(f"  File: {best_model_path}")
        print("  Scaler: week2/models_retrained/scaler_retrained.pkl")
    else:
        print("\nCreating updated app.py template...")
        
        template = '''
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler

# Set page config
st.set_page_config(
    page_title="AI Health Predictor - Diabetes Risk Assessment",
    page_icon="í¿¥",
    layout="wide"
)

# Title
st.title("í¿¥ AI Health Predictor - Diabetes Risk Assessment")
st.markdown("Predict your risk of diabetes based on health parameters")

# Load the best model
@st.cache_resource
def load_model():
    """Load the best performing model"""
    try:
        # UPDATE THIS PATH to your best model
        model = joblib.load("''' + best_model_path + '''")
        scaler = joblib.load("week2/models_retrained/scaler_retrained.pkl")
        return model, scaler
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

model, scaler = load_model()

# Sidebar for input
st.sidebar.header("Patient Health Parameters")

# Input fields matching your diabetes dataset
pregnancies = st.sidebar.slider("Pregnancies", 0, 20, 1)
glucose = st.sidebar.slider("Glucose Level", 0, 200, 100)
blood_pressure = st.sidebar.slider("Blood Pressure", 0, 122, 72)
skin_thickness = st.sidebar.slider("Skin Thickness", 0, 99, 20)
insulin = st.sidebar.slider("Insulin", 0, 846, 80)
bmi = st.sidebar.slider("BMI", 0.0, 67.1, 25.0)
dpf = st.sidebar.slider("Diabetes Pedigree Function", 0.0, 2.5, 0.5)
age = st.sidebar.slider("Age", 21, 81, 33)

# Create feature array
features = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]])

# Make prediction
if st.sidebar.button("Predict Diabetes Risk"):
    if model is not None and scaler is not None:
        try:
            # Scale features
            features_scaled = scaler.transform(features)
            
            # Predict
            prediction = model.predict(features_scaled)
            prediction_proba = model.predict_proba(features_scaled)[:, 1] if hasattr(model, 'predict_proba') else [0.5]
            
            # Display results
            st.header("Prediction Results")
            
            risk_percentage = prediction_proba[0] * 100
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Risk Level", f"{risk_percentage:.1f}%")
                if prediction[0] == 1:
                    st.error("High Risk of Diabetes")
                    st.warning("Recommendation: Consult a healthcare professional")
                else:
                    st.success("Low Risk of Diabetes")
                    st.info("Recommendation: Maintain healthy lifestyle")
            
            with col2:
                # Risk gauge
                st.subheader("Risk Gauge")
                st.progress(int(risk_percentage))
                
                # Interpretation
                if risk_percentage < 30:
                    st.info("Low Risk Zone")
                elif risk_percentage < 70:
                    st.warning("Moderate Risk Zone")
                else:
                    st.error("High Risk Zone")
            
            # Feature importance (if available)
            if hasattr(model, 'feature_importances_'):
                st.subheader("Feature Importance")
                feature_names = ["Pregnancies", "Glucose", "Blood Pressure", "Skin Thickness", 
                               "Insulin", "BMI", "Diabetes Pedigree", "Age"]
                importances = model.feature_importances_
                
                importance_df = pd.DataFrame({
                    'Feature': feature_names,
                    'Importance': importances
                }).sort_values('Importance', ascending=False)
                
                st.dataframe(importance_df, use_container_width=True)
                
        except Exception as e:
            st.error(f"Prediction error: {e}")
    else:
        st.error("Model not loaded properly. Please check the model files.")

# Main area - project info
st.header("About This Application")
st.markdown("""
This AI Health Predictor uses machine learning to assess diabetes risk based on:
- **Dataset**: Pima Indians Diabetes Dataset
- **Best Model**: ''' + best_model + '''
- **Accuracy**: As evaluated on test data
- **Purpose**: Educational tool for diabetes risk assessment

**Note**: This tool is for educational purposes only. Always consult with healthcare professionals for medical advice.
""")

# Display model info
st.sidebar.header("Model Information")
st.sidebar.info(f"Best Model: {best_model}")
st.sidebar.info("Trained on Pima Indians Diabetes Dataset")

if __name__ == "__main__":
    pass
'''
        
        # Save the template
        with open('app_updated.py', 'w') as f:
            f.write(template)
        
        print("\nUpdated app template saved as 'app_updated.py'")
        print("To use it: mv app_updated.py app.py")
        print("Then run: streamlit run app.py")
        
except FileNotFoundError:
    print("Final model selection not found. Please run the corrected evaluation first.")
    print("Run: python week3/evaluate_corrected_models.py")
