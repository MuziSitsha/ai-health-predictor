import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
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
    
    fig_gauge = create_risk_gauge(st.session_state.current_proba, st.session_state.theme_mode) * 100,
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
        joblib.load('models/neural_network_model.pkl')
        model_options.append('Neural Network')
    except:
        st.info("Neural Network not trained yet")
    
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
            joblib.load('models/neural_network_model.pkl')
            st.metric("Neural Network", "Available", "3 Hidden Layers")
        except:
            st.metric("Neural Network", "Not Trained", "Train required")
    
    with cols[2]:
        st.metric("Project Status", "Complete", "Ready for Submission")

elif st.session_state.current_page == 'prediction':
    # Prediction Page
    st.markdown(f"## Prediction with {st.session_state.selected_model}")
    
    # Input Parameters
    st.markdown("### Clinical Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.pregnancies = st.slider("Pregnancies", 0, 20, st.session_state.pregnancies)
        st.session_state.glucose = st.slider("Glucose (mg/dL)", 0, 200, st.session_state.glucose)
        st.session_state.blood_pressure = st.slider("Blood Pressure (mm Hg)", 0, 122, st.session_state.blood_pressure)
        st.session_state.skin_thickness = st.slider("Skin Thickness (mm)", 0, 99, st.session_state.skin_thickness)
    
    with col2:
        st.session_state.insulin = st.slider("Insulin (mu U/ml)", 0, 846, st.session_state.insulin)
        st.session_state.bmi = st.slider("BMI (kg/m2)", 0.0, 67.1, st.session_state.bmi, 0.1)
        st.session_state.dpf = st.slider("Diabetes Pedigree Function", 0.0, 2.5, st.session_state.dpf, 0.01)
        st.session_state.age = st.slider("Age (years)", 21, 81, st.session_state.age)
    
    # Create features array
    features = np.array([[st.session_state.pregnancies, st.session_state.glucose,
                         st.session_state.blood_pressure, st.session_state.skin_thickness,
                         st.session_state.insulin, st.session_state.bmi,
                         st.session_state.dpf, st.session_state.age]])
    
    # Prediction button
    if st.button("Predict Diabetes Risk", type="primary", use_container_width=True):
        st.session_state.prediction_made = True
        
        try:
            if selected_model == 'Random Forest':
                # Load RF model
                model = joblib.load('models/random_forest.pkl')
                scaler = joblib.load('models/scaler_retrained.pkl')
                features_scaled = scaler.transform(features)
                proba = model.predict_proba(features_scaled)[0][1]
                prediction = model.predict(features_scaled)[0]
            
            else:  # Neural Network
                # Load NN model
                model = joblib.load('models/neural_network_model.pkl')
                scaler = joblib.load('models/nn_scaler.pkl')
                features_scaled = scaler.transform(features)
                proba = model.predict_proba(features_scaled)[0][1]
                prediction = 1 if proba > 0.5 else 0
            
            # Store results
            st.session_state.current_proba = proba
            st.session_state.current_prediction = prediction
            
        except Exception as e:
            st.error(f"Prediction error: {str(e)}")
            st.info("Make sure models are trained. Using demo prediction.")
            # Demo prediction
            st.session_state.current_proba = 0.35
            st.session_state.current_prediction = 0
    
    # Display results if prediction was made
    if st.session_state.prediction_made and 'current_proba' in st.session_state:
        risk_percentage = st.session_state.current_proba * 100
        
        # Risk gauge
        st.markdown("### Risk Assessment")
        
        # Determine risk level
        if risk_percentage < 25:
            bar_color, risk_level = "#059669", "Low Risk"
        elif risk_percentage < 50:
            bar_color, risk_level = "#D97706", "Moderate Risk"
        elif risk_percentage < 75:
            bar_color, risk_level = "#DC2626", "High Risk"
        else:
            bar_color, risk_level = "#7f1d1d", "Very High Risk"
        
        # Gauge visualization
        fig_gauge = create_risk_gauge(st.session_state.current_proba, st.session_state.theme_mode)(
            mode="gauge+number",
            value=risk_percentage,
            title={'text': f"Diabetes Risk - {risk_level}"},
            domain={'x': [0, 1], 'y': [0, 1]},
            number={'suffix': '%'},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': bar_color},
                'steps': [
                    {'range': [0, 30], 'color': '#D1FAE5'},
                    {'range': [30, 70], 'color': '#FEF3C7'},
                    {'range': [70, 100], 'color': '#FEE2E2'}
                ]
            }
        ))
        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Risk Probability", f"{risk_percentage:.1f}%")
        with col2:
            pred_text = "High Risk" if st.session_state.current_prediction == 1 else "Low Risk"
            st.metric("Prediction", pred_text)
        with col3:
            confidence = st.session_state.current_proba if st.session_state.current_prediction == 1 else 1 - st.session_state.current_proba
            st.metric("Model Confidence", f"{confidence*100:.1f}%")
        
        # Recommendations
        st.markdown(f"### Recommendations for {risk_level}")
        
        if risk_level == "Low Risk":
            st.success("Maintain healthy lifestyle with regular exercise and balanced diet.")
        elif risk_level == "Moderate Risk":
            st.warning("Monitor glucose levels and consider lifestyle changes.")
        else:
            st.error("Consult healthcare professional for comprehensive assessment.")

elif st.session_state.current_page == 'comparison':
    # Model Comparison Page
    st.markdown("## Model Comparison")
    
    # Create comparison data
    comparison_data = [
        {
            'Model': 'Random Forest',
            'Accuracy': '75-80%',
            'AUC': '0.80-0.85',
            'Training Time': 'Fast',
            'Interpretability': 'Medium'
        },
        {
            'Model': 'Neural Network',
            'Accuracy': '78-82%',
            'AUC': '0.82-0.87',
            'Training Time': 'Medium',
            'Interpretability': 'Low'
        }
    ]
    
    df_compare = pd.DataFrame(comparison_data)
    st.dataframe(df_compare, use_container_width=True)
    
    # Visualization
    fig = px.bar(df_compare, x='Model', y=['Accuracy', 'AUC'], 
                 barmode='group', title='Model Performance Comparison')
    st.plotly_chart(fig, use_container_width=True)

else:  # info page
    # Project Information Page
    st.markdown("## Project Information")
    
    st.markdown("""
    ### Month 3 Project - AI Health Predictor
    
    **Project Requirements:**
    - Data preparation
    - Model development (Random Forest + Neural Network)
    - Model evaluation
    - UI development with Streamlit
    - Deployment to Streamlit Cloud
    
    **Technical Stack:**
    - Python, scikit-learn
    - Streamlit for UI
    - Plotly for visualizations
    - Joblib for model saving
    
    **Deployment:**
    - Platform: Streamlit Community Cloud
    - URL: https://ai-health-predictor-kaknzejwgvtneyqpxzsm5b.streamlit.app/
    
    **GitHub:** https://github.com/MuziSitsha/ai-health-predictor
    
    **Note:** This is for educational purposes only.
    """)

# Footer
st.markdown("---")
st.markdown("Month 3 Project - AI Health Predictor | January 2026 | Educational Use Only")
