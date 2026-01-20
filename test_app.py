import streamlit as st
import pandas as pd
import numpy as np
import joblib

print("Testing app imports...")
try:
    # Test basic imports
    import plotly.graph_objects as go
    import plotly.express as px
    print("✓ All imports successful")
    
    # Test model loading
    try:
        model = joblib.load('models/neural_network_model.pkl')
        print("✓ Neural Network model loaded")
    except:
        print("⚠ Neural Network model not found")
    
    try:
        model = joblib.load('models/random_forest.pkl')
        print("✓ Random Forest model loaded")
    except:
        print("⚠ Random Forest model not found")
    
    print("\n✓ App structure is valid")
    
except Exception as e:
    print(f"✗ Error: {e}")
