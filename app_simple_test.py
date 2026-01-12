import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.title("Simple Diabetes Predictor Test")

# Try to load model with error handling
try:
    st.write("Attempting to load model...")
    model = joblib.load("week2/models_retrained/random_forest.pkl")
    st.success("Model loaded successfully!")
    
    # Try to load scaler
    scaler = joblib.load("week2/models_retrained/scaler_retrained.pkl")
    st.success("Scaler loaded successfully!")
    
    # Show model info
    st.write(f"Model type: {type(model).__name__}")
    
    # Test prediction
    test_features = np.array([[1, 100, 72, 20, 80, 25.0, 0.5, 33]])
    test_scaled = scaler.transform(test_features)
    prediction = model.predict(test_scaled)
    proba = model.predict_proba(test_scaled)
    
    st.write(f"Test prediction: {prediction[0]}")
    st.write(f"Probability: {proba[0]}")
    
except Exception as e:
    st.error(f"Error: {str(e)}")
    st.write("Full error details:")
    st.exception(e)
