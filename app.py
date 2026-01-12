import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os

# Set page config
st.set_page_config(
    page_title="AI Health Predictor",
    layout="wide"
)

# Title
st.title("AI Health Predictor")
st.markdown("Predict diabetes risk based on health parameters")

# Function to load model
def load_model_and_scaler():
    try:
        # Load scaler
        scaler = joblib.load('week2/models/scaler.pkl')
        
        # Load best model
        model = joblib.load('week2/models/best_model.pkl')
        
        # Load feature names
        with open('week2/models/feature_names.json', 'r') as f:
            feature_names = json.load(f)
        
        return model, scaler, feature_names
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None, None

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Make Prediction", "Model Info"])

if page == "Home":
    st.header("Welcome to AI Health Predictor")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### About this App
        This application uses machine learning to predict diabetes risk.
        
        **Features:**
        - Real-time risk prediction
        - Model comparison
        - Probability analysis
        """)
    
    with col2:
        st.markdown("""
        ### How to Use
        1. Go to Make Prediction page
        2. Enter health parameters
        3. Click Predict button
        4. View your risk assessment
        
        **Model Performance:**
        - Accuracy: 75.97%
        - Best Model: Random Forest
        """)

elif page == "Make Prediction":
    st.header("Make a Prediction")
    
    model, scaler, feature_names = load_model_and_scaler()
    
    if model and scaler and feature_names:
        # Create input form
        with st.form("prediction_form"):
            st.subheader("Enter Health Parameters")
            
            inputs = {}
            
            col1, col2 = st.columns(2)
            
            with col1:
                inputs['Pregnancies'] = st.number_input(
                    "Pregnancies",
                    min_value=0,
                    max_value=20,
                    value=3
                )
                
                inputs['Glucose'] = st.number_input(
                    "Glucose",
                    min_value=0,
                    max_value=300,
                    value=120
                )
                
                inputs['BloodPressure'] = st.number_input(
                    "BloodPressure",
                    min_value=0,
                    max_value=150,
                    value=70
                )
                
                inputs['SkinThickness'] = st.number_input(
                    "SkinThickness",
                    min_value=0,
                    max_value=100,
                    value=20
                )
            
            with col2:
                inputs['Insulin'] = st.number_input(
                    "Insulin",
                    min_value=0,
                    max_value=300,
                    value=80
                )
                
                inputs['BMI'] = st.number_input(
                    "BMI",
                    min_value=0.0,
                    max_value=50.0,
                    value=25.0,
                    step=0.1
                )
                
                inputs['DiabetesPedigreeFunction'] = st.number_input(
                    "DiabetesPedigreeFunction",
                    min_value=0.0,
                    max_value=2.5,
                    value=0.5,
                    step=0.01
                )
                
                inputs['Age'] = st.number_input(
                    "Age",
                    min_value=0,
                    max_value=100,
                    value=30
                )
            
            submitted = st.form_submit_button("Predict Diabetes Risk")
            
            if submitted:
                # Prepare input data
                input_data = []
                for feature in feature_names:
                    input_data.append(inputs.get(feature, 0.0))
                
                input_array = np.array(input_data).reshape(1, -1)
                input_scaled = scaler.transform(input_array)
                
                try:
                    prediction = model.predict(input_scaled)[0]
                    
                    if hasattr(model, 'predict_proba'):
                        probability = model.predict_proba(input_scaled)[0][1]
                    else:
                        probability = float(prediction)
                    
                    st.subheader("Prediction Results")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        prediction_text = "Diabetic" if prediction == 1 else "Non-Diabetic"
                        st.metric("Prediction", prediction_text)
                    
                    with col2:
                        st.metric("Probability", f"{probability:.1%}")
                    
                    with col3:
                        if probability > 0.7:
                            risk_level = "High"
                        elif probability > 0.3:
                            risk_level = "Medium"
                        else:
                            risk_level = "Low"
                        st.metric("Risk Level", risk_level)
                    
                    st.progress(float(probability))
                    
                    if prediction == 1 or probability > 0.5:
                        st.warning("Potential diabetes risk detected. Consult a healthcare professional.")
                    else:
                        st.success("Low diabetes risk detected. Maintain healthy habits.")
                        
                except Exception as e:
                    st.error(f"Error making prediction: {str(e)}")
    else:
        st.error("Could not load the model.")

elif page == "Model Info":
    st.header("Model Information")
    
    try:
        report_path = 'week2/reports/performance_report.json'
        if os.path.exists(report_path):
            with open(report_path, 'r') as f:
                report = json.load(f)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Best Model")
                st.metric("Model", report['best_model']['name'])
                st.metric("Accuracy", f"{report['best_model']['accuracy']:.2%}")
            
            with col2:
                st.subheader("Dataset Info")
                st.metric("Total Samples", report['dataset']['shape'][0])
                st.metric("Features", len(report['dataset']['features']))
        else:
            st.info("Performance report not found")
            st.metric("Best Model", "Random Forest")
            st.metric("Accuracy", "75.97%")
            
    except Exception as e:
        st.error(f"Error loading model info: {str(e)}")

# Footer
st.markdown("---")
st.markdown("AI Health Predictor | Educational Project | Week 3 Deployment")
