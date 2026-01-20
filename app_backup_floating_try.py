import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go

def check_neural_network():
    """Check if neural network is properly trained and available"""
    try:
        import os
        import joblib
        
        # Check if files exist
        if not os.path.exists('models/neural_network_model.pkl'):
            return False, "Model file not found"
        
        if not os.path.exists('models/nn_scaler.pkl'):
            return False, "Scaler file not found"
        
        # Try to load model
        model = joblib.load('models/neural_network_model.pkl')
        scaler = joblib.load('models/nn_scaler.pkl')
        
        # Check model attributes
        if not hasattr(model, 'predict'):
            return False, "Model missing predict method"
        
        if not hasattr(model, 'predict_proba'):
            return False, "Model missing predict_proba method"
        
        # Test prediction
        import numpy as np
        test_input = np.array([[1, 100, 70, 20, 80, 25.0, 0.5, 30]])
        test_scaled = scaler.transform(test_input)
        
        try:
            prediction = model.predict(test_scaled)
            probability = model.predict_proba(test_scaled)
            return True, "Neural network is ready"
        except:
            return False, "Model failed test prediction"
            
    except Exception as e:
        return False, f"Error: {str(e)}"


def create_risk_gauge(probability, current_theme):
    """Create risk gauge chart that adapts to theme"""
    import plotly.graph_objects as go
    
    # Set colors based on theme
    if current_theme == "dark":
        text_color = "#e0e0e0"
        plot_bgcolor = "#242424"
        paper_bgcolor = "#242424"
        gauge_bg = "#2a2a2a"
        needle_color = "#ff6b6b"
    else:
        text_color = "#31333F"
        plot_bgcolor = "#F0F2F6"
        paper_bgcolor = "#FFFFFF"
        gauge_bg = "#F8F9FA"
        needle_color = "#FF4B4B"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability * 100,
        domain={"x": [0, 1], "y": [0, 1]},
        title={
            "text": "Risk Level",
            "font": {"size": 20, "color": text_color}
        },
        number={
            "font": {"size": 40, "color": text_color},
            "suffix": "%"
        },
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 1,
                "tickcolor": text_color,
                "tickfont": {"color": text_color}
            },
            "bar": {"color": needle_color},
            "bgcolor": gauge_bg,
            "borderwidth": 2,
            "bordercolor": text_color,
            "steps": [
                {"range": [0, 30], "color": "#10B981"},
                {"range": [30, 70], "color": "#F59E0B"},
                {"range": [70, 100], "color": "#EF4444"}
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": probability * 100
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor=paper_bgcolor,
        plot_bgcolor=plot_bgcolor,
        font={"color": text_color},
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

import plotly.express as px

# Set page config
st.set_page_config(
    page_title="AI Health Predictor",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = 'Random Forest'
if 'prediction_made' not in st.session_state:
    st.session_state.prediction_made = False

# Default values
defaults = {
    'pregnancies': 1, 'glucose': 100, 'blood_pressure': 72,
    'skin_thickness': 20, 'insulin': 80, 'bmi': 25.0,
    'dpf': 0.5, 'age': 33
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Title
st.title("AI Health Predictor - Diabetes Risk Assessment")
st.markdown("Predict diabetes risk using multiple machine learning models")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    
    # Model Selection
    st.subheader("Model Selection")
    model_options = ['Random Forest']
    
    # Check which models are available
                try:
                    model = joblib.load('models/neural_network_model.pkl')
                    # Load neural network scaler if exists
                    if os.path.exists('models/nn_scaler.pkl'):
                        scaler = joblib.load('models/nn_scaler.pkl')
                except Exception as e:
                    st.error(f"Failed to load neural network: {e}")
                    # Fallback to random forest
                    model = joblib.load('models/random_forest.pkl')
                    scaler = joblib.load('models/scaler_retrained.pkl')
    
    selected_model = st.selectbox(
        "Choose Prediction Model",
        model_options,
        index=model_options.index(st.session_state.selected_model) 
        if st.session_state.selected_model in model_options else 0
    )
    st.session_state.selected_model = selected_model
    
    st.markdown("---")
    
    # Navigation
    st.subheader("Navigation")
    if st.button("Home", use_container_width=True):
        st.session_state.current_page = 'home'
        st.rerun()
    
    if st.button("Custom Prediction", use_container_width=True):
        st.session_state.current_page = 'prediction'
        st.rerun()
    
    if st.button("Model Comparison", use_container_width=True):
        st.session_state.current_page = 'comparison'
        st.rerun()
    
    if st.button("Project Info", use_container_width=True):
        st.session_state.current_page = 'info'
        st.rerun()

# Page routing
if st.session_state.current_page == 'home':
    # Home Page
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("## Project Overview")
        st.markdown("""
        This project demonstrates a complete machine learning pipeline for diabetes risk prediction.
        
        **Key Features:**
        - Multiple ML models comparison
        - Interactive parameter tuning
        - Real-time predictions
        - Comprehensive visualizations
        - Deployed on Streamlit Cloud
        
        **Models Implemented:**
        1. **Random Forest** - Traditional ensemble method
        2. **Neural Network** - Deep learning approach
        """)
    
    with col2:
        st.markdown("## Quick Start")
        st.markdown("""
        1. **Select a model** from the sidebar
        2. **Go to Custom Prediction**
        3. **Adjust clinical parameters**
        4. **Click Predict** to see results
        5. **Compare models** in the comparison section
        """)
        
        if st.button("Start Predicting Now", type="primary", use_container_width=True):
            st.session_state.current_page = 'prediction'
            st.rerun()
    
    st.markdown("---")
    
    # Model Status
    st.markdown("## Model Status")
    cols = st.columns(3)
    
    with cols[0]:
        st.metric("Random Forest", "Available", "Baseline Model")
    
    with cols[1]:
            try:
                import os
                if os.path.exists('models/neural_network_model.pkl'):
                    nn_model = joblib.load('models/neural_network_model.pkl')
                    if hasattr(nn_model, 'predict') and hasattr(nn_model, 'predict_proba'):
                        st.metric("Neural Network", "Available", "3 Hidden Layers")
                    else:
                        st.metric("Neural Network", "Incomplete", "Retrain needed")
                else:
                    st.metric("Neural Network", "Not Trained", "Train required")
            except:
                st.metric("Neural Network", "Not Trained", "Train required")
