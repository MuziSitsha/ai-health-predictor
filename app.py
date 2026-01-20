import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px
import os
from sklearn.preprocessing import StandardScaler

# ===== HELPER FUNCTIONS =====

def check_neural_network():
    """Check if neural network is properly trained and available"""
    try:
        if not os.path.exists('models/neural_network_model.pkl'):
            return False, "Model file not found", None
        
        if not os.path.exists('models/nn_scaler.pkl'):
            return False, "Scaler file not found", None
        
        model = joblib.load('models/neural_network_model.pkl')
        scaler = joblib.load('models/nn_scaler.pkl')
        
        if not hasattr(model, 'predict'):
            return False, "Model missing predict method", None
        
        if not hasattr(model, 'predict_proba'):
            return False, "Model missing predict_proba method", None
        
        # Get the actual hidden layers configuration
        if hasattr(model, 'hidden_layer_sizes'):
            if isinstance(model.hidden_layer_sizes, tuple):
                hidden_layers = len(model.hidden_layer_sizes)
                layer_sizes = model.hidden_layer_sizes
            else:
                hidden_layers = 1
                layer_sizes = (model.hidden_layer_sizes,)
        else:
            hidden_layers = 3
            layer_sizes = (64, 32, 16)
        
        test_input = np.array([[1, 100, 70, 20, 80, 25.0, 0.5, 30]])
        test_scaled = scaler.transform(test_input)
        
        prediction = model.predict(test_scaled)
        probability = model.predict_proba(test_scaled)
        return True, "Neural network is ready", (hidden_layers, layer_sizes)
            
    except Exception as e:
        return False, f"Error: {str(e)}", None


def create_risk_gauge(probability, current_theme):
    """Create risk gauge chart that adapts to theme"""
    if current_theme == "dark":
        text_color = "#FFFFFF"
        plot_bgcolor = "#1E1E1E"
        paper_bgcolor = "#1E1E1E"
        gauge_bg = "#2D2D2D"
        needle_color = "#FF4B4B"
    else:
        text_color = "#31333F"
        plot_bgcolor = "#FFFFFF"
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


def create_risk_bar(probability, current_theme):
    """Create a horizontal risk bar that changes color and length based on risk percentage"""
    risk_percentage = probability * 100
    
    # Determine color based on risk level
    if risk_percentage < 30:
        bar_color = "#10B981"  # Green for low risk
        risk_label = "Low Risk"
    elif risk_percentage < 70:
        bar_color = "#F59E0B"  # Orange for moderate risk
        risk_label = "Moderate Risk"
    else:
        bar_color = "#EF4444"  # Red for high risk
        risk_label = "High Risk"
    
    # Set text color based on theme
    if current_theme == "dark":
        text_color = "#FFFFFF"
        bg_color = "#2D2D2D"
    else:
        text_color = "#31333F"
        bg_color = "#F8F9FA"
    
    fig = go.Figure()
    
    # Background bar (full length)
    fig.add_trace(go.Bar(
        x=[100],
        y=["Risk"],
        orientation='h',
        marker=dict(color=bg_color),
        width=0.3,
        showlegend=False,
        hoverinfo='none'
    ))
    
    # Colored risk bar (dynamic length)
    fig.add_trace(go.Bar(
        x=[risk_percentage],
        y=["Risk"],
        orientation='h',
        marker=dict(color=bar_color),
        width=0.3,
        showlegend=False,
        text=[f"{risk_percentage:.1f}% - {risk_label}"],
        textposition='inside',
        insidetextanchor='middle',
        hoverinfo='none'
    ))
    
    fig.update_layout(
        title=dict(
            text=f"Diabetes Risk: {risk_percentage:.1f}%",
            font=dict(size=16, color=text_color),
            x=0.5
        ),
        xaxis=dict(
            range=[0, 100],
            showgrid=True,
            gridcolor='lightgray' if current_theme == 'light' else '#444444',
            tickfont=dict(color=text_color),
            title=dict(text="Risk Percentage", font=dict(color=text_color))
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=150,
        margin=dict(l=20, r=20, t=50, b=20),
        barmode='overlay'
    )
    
    return fig


def load_model(model_type='random_forest'):
    """Load the specified model with its scaler"""
    try:
        if model_type == 'random_forest':
            model_path = 'models/random_forest.pkl'
            scaler_path = 'models/scaler_retrained.pkl'
        elif model_type == 'neural_network':
            model_path = 'models/neural_network_model.pkl'
            scaler_path = 'models/nn_scaler.pkl'
        else:
            return None, None
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
            return model, scaler
        else:
            return None, None
    except Exception as e:
        st.error(f"Error loading {model_type}: {e}")
        return None, None


# ===== APP CONFIGURATION =====

st.set_page_config(
    page_title="AI Health Predictor - Diabetes Risk Assessment",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for theme FIRST before any use
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = 'light'  # Start with light mode

# Initialize page navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Initialize session state for predictions
if 'prediction_made' not in st.session_state:
    st.session_state.prediction_made = False
if 'current_features' not in st.session_state:
    st.session_state.current_features = None
if 'current_prediction' not in st.session_state:
    st.session_state.current_prediction = None
if 'current_proba' not in st.session_state:
    st.session_state.current_proba = None

# Store inputs in session state to preserve them
if 'pregnancies' not in st.session_state:
    st.session_state.pregnancies = 1
if 'glucose' not in st.session_state:
    st.session_state.glucose = 100
if 'blood_pressure' not in st.session_state:
    st.session_state.blood_pressure = 72
if 'skin_thickness' not in st.session_state:
    st.session_state.skin_thickness = 20
if 'insulin' not in st.session_state:
    st.session_state.insulin = 80
if 'bmi' not in st.session_state:
    st.session_state.bmi = 25.0
if 'dpf' not in st.session_state:
    st.session_state.dpf = 0.5
if 'age' not in st.session_state:
    st.session_state.age = 33

# Store model selection
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = 'Random Forest'

# ===== CUSTOM CSS FOR THEMES =====

# Base styles (common to both themes)
st.markdown("""
<style>
    /* Base styles for both themes */
    .main-header { 
        font-size: 2.5rem; 
        text-align: center; 
        margin-bottom: 1rem; 
        font-weight: bold;
    }
    .sub-header { 
        font-size: 1.2rem; 
        text-align: center; 
        margin-bottom: 2rem; 
        color: #666666;
    }
    .risk-high {
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #DC2626;
        background-color: #FEF2F2;
        margin: 10px 0;
    }
    .risk-medium {
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #D97706;
        background-color: #FEF3C7;
        margin: 10px 0;
    }
    .risk-low {
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #059669;
        background-color: #D1FAE5;
        margin: 10px 0;
    }
    .metric-card {
        padding: 15px;
        border-radius: 8px;
        background-color: #F3F4F6;
        text-align: center;
        border: 1px solid #E5E7EB;
    }
</style>
""", unsafe_allow_html=True)

# Apply light mode theme by default - WHITE BACKGROUND
st.markdown("""
<style>
    /* Light theme styles - WHITE BACKGROUND */
    .stApp {
        background-color: white !important;
    }
    [data-testid="stAppViewContainer"] {
        background-color: white !important;
        color: #31333F !important;
    }
    [data-testid="stSidebar"] {
        background-color: #F0F2F6 !important;
    }
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: #31333F !important;
    }
    .stNumberInput input, .stSlider div {
        background-color: white !important;
        color: #31333F !important;
        border: 1px solid #E5E7EB !important;
    }
    .stButton > button {
        background-color: #FF4B4B !important;
        color: white !important;
        border: none !important;
    }
    .stButton > button:hover {
        background-color: #FF3333 !important;
    }
    .stSelectbox div, .stTextInput input {
        background-color: white !important;
        color: #31333F !important;
        border: 1px solid #E5E7EB !important;
    }
    .stMetric {
        background-color: white !important;
        color: #31333F !important;
    }
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        color: #31333F !important;
    }
    .stDataFrame {
        background-color: white !important;
        color: #31333F !important;
    }
    .stDataFrame table {
        background-color: white !important;
        color: #31333F !important;
    }
    .stDataFrame th, .stDataFrame td {
        background-color: white !important;
        color: #31333F !important;
        border-color: #E5E7EB !important;
    }
</style>
""", unsafe_allow_html=True)

# Apply dark mode theme only if explicitly selected
if st.session_state.theme_mode == 'dark':
    st.markdown("""
    <style>
        /* Dark theme specific styles - FIXED: Top bar is now dark */
        .stApp {
            background-color: #1a1a1a !important;
            color: #e0e0e0 !important;
        }
        [data-testid="stAppViewContainer"] {
            background-color: #1a1a1a !important;
            color: #e0e0e0 !important;
        }
        [data-testid="stSidebar"] {
            background-color: #242424 !important;
        }
        [data-testid="stHeader"] {
            background-color: #1a1a1a !important;
        }
        header[data-testid="stHeader"] {
            background-color: #1a1a1a !important;
        }
        .st-emotion-cache-1avcm0n {
            background-color: #1a1a1a !important;
        }
        h1, h2, h3, h4, h5, h6, p, div, span, label {
            color: #e0e0e0 !important;
        }
        .stNumberInput input, .stSlider div {
            background-color: #2a2a2a !important;
            color: #e0e0e0 !important;
            border: 1px solid #444444 !important;
        }
        .stButton > button {
            background-color: #FF4B4B !important;
            color: white !important;
            border: none !important;
        }
        .stSelectbox div, .stTextInput input {
            background-color: #2a2a2a !important;
            color: #e0e0e0 !important;
        }
        .stMetric {
            background-color: #2a2a2a !important;
            color: #e0e0e0 !important;
        }
        [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
            color: #e0e0e0 !important;
        }
        .risk-high {
            background-color: #5D1F1A !important;
            color: #ffcdd2 !important;
            border-left: 5px solid #ef5350 !important;
        }
        .risk-medium {
            background-color: #5d4a1a !important;
            color: #ffe082 !important;
            border-left: 5px solid #ffa726 !important;
        }
        .risk-low {
            background-color: #1b5e20 !important;
            color: #c8e6c9 !important;
            border-left: 5px solid #66bb6a !important;
        }
        .metric-card {
            background-color: #2a2a2a !important;
            color: #e0e0e0 !important;
            border: 1px solid #444444 !important;
        }
        .stDataFrame {
            background-color: #2a2a2a !important;
            color: #e0e0e0 !important;
        }
        .stDataFrame table {
            background-color: #2a2a2a !important;
            color: #e0e0e0 !important;
        }
        .stDataFrame th, .stDataFrame td {
            background-color: #2a2a2a !important;
            color: #e0e0e0 !important;
            border-color: #444444 !important;
        }
    </style>
    """, unsafe_allow_html=True)

# ===== SIDEBAR =====

with st.sidebar:
    st.header("Configuration")
    
    # Theme toggle at the top
    current_theme = st.session_state.theme_mode
    if current_theme == 'light':
        toggle_text = "Switch to Dark Mode"
    else:
        toggle_text = "Switch to Light Mode"
    
    if st.button(toggle_text, key="theme_toggle", use_container_width=True):
        if current_theme == 'light':
            st.session_state.theme_mode = 'dark'
        else:
            st.session_state.theme_mode = 'light'
        st.rerun()
    
    st.caption(f"Current: {current_theme.title()} Mode")
    st.markdown("---")
    
    # Model Selection
    st.subheader("Model Selection")
    
    # Check which models are available
    model_options = ['Random Forest']
    nn_ready, nn_message, nn_layers_info = check_neural_network()
    if nn_ready:
        model_options.append('Neural Network')
    
    selected_model = st.selectbox(
        "Choose Prediction Model",
        model_options,
        index=0
    )
    st.session_state.selected_model = selected_model
    
    st.markdown("---")
    
    # Quick Examples Section
    st.subheader("Quick Examples")
    
    # High Risk Example Button
    if st.button("High Risk Example", use_container_width=True, key="high_risk_btn"):
        st.session_state.pregnancies = 6
        st.session_state.glucose = 148
        st.session_state.blood_pressure = 72
        st.session_state.skin_thickness = 35
        st.session_state.insulin = 0
        st.session_state.bmi = 33.6
        st.session_state.dpf = 0.627
        st.session_state.age = 50
        st.session_state.current_page = 'prediction'
        st.rerun()
    
    # Low Risk Example Button - FIXED VALUES
    if st.button("Low Risk Example", use_container_width=True, key="low_risk_btn"):
        st.session_state.pregnancies = 1
        st.session_state.glucose = 89
        st.session_state.blood_pressure = 66
        st.session_state.skin_thickness = 23
        st.session_state.insulin = 94
        st.session_state.bmi = 28.1
        st.session_state.dpf = 0.167
        st.session_state.age = 21
        st.session_state.current_page = 'prediction'
        st.rerun()
    
    # Custom Profile Button
    if st.button("Custom Profile", use_container_width=True, key="custom_btn"):
        st.session_state.current_page = 'prediction'
        st.rerun()
    
    st.markdown("---")
    
    # Navigation
    st.subheader("Navigation")
    if st.button("Home", use_container_width=True, key="nav_home"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    if st.button("Custom Prediction", use_container_width=True, key="nav_prediction"):
        st.session_state.current_page = 'prediction'
        st.rerun()
    
    if st.button("Model Comparison", use_container_width=True, key="nav_comparison"):
        st.session_state.current_page = 'comparison'
        st.rerun()
    
    if st.button("Project Info", use_container_width=True, key="nav_info"):
        st.session_state.current_page = 'info'
        st.rerun()

# ===== PAGE ROUTING =====

if st.session_state.current_page == 'home':
    # Home Page
    st.markdown('<div class="main-header">AI Health Predictor - Diabetes Risk Assessment</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Predict diabetes risk using clinical parameters from the Pima Indians Diabetes Dataset</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Choose one of the options in the sidebar to get started:
    - **Quick Examples**: Try pre-configured High Risk or Low Risk profiles
    - **Custom Prediction**: Input your own clinical parameters
    - **Model Comparison**: Compare different machine learning models
    - **Project Info**: Learn more about this project
    """)
    
    # Quick examples section on home page
    st.markdown("### Quick Examples")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### High Risk Profile")
        st.markdown("""
        - Pregnancies: 6
        - Glucose: 148 mg/dL
        - Blood Pressure: 72 mm Hg
        - Skin Thickness: 35 mm
        - Insulin: 0 μU/mL
        - BMI: 33.6 kg/m²
        - Diabetes Pedigree: 0.627
        - Age: 50 years
        """)
        if st.button("Load High Risk Example", key="home_high_risk_btn"):
            st.session_state.pregnancies = 6
            st.session_state.glucose = 148
            st.session_state.blood_pressure = 72
            st.session_state.skin_thickness = 35
            st.session_state.insulin = 0
            st.session_state.bmi = 33.6
            st.session_state.dpf = 0.627
            st.session_state.age = 50
            st.session_state.current_page = 'prediction'
            st.rerun()
    
    with col2:
        st.markdown("#### Low Risk Profile")
        st.markdown("""
        - Pregnancies: 1
        - Glucose: 89 mg/dL
        - Blood Pressure: 66 mm Hg
        - Skin Thickness: 23 mm
        - Insulin: 94 μU/mL
        - BMI: 28.1 kg/m²
        - Diabetes Pedigree: 0.167
        - Age: 21 years
        """)
        if st.button("Load Low Risk Example", key="home_low_risk_btn"):
            st.session_state.pregnancies = 1
            st.session_state.glucose = 89
            st.session_state.blood_pressure = 66
            st.session_state.skin_thickness = 23
            st.session_state.insulin = 94
            st.session_state.bmi = 28.1
            st.session_state.dpf = 0.167
            st.session_state.age = 21
            st.session_state.current_page = 'prediction'
            st.rerun()
    
    # Model Status Section
    st.markdown("---")
    st.markdown("### Model Status")
    
    cols = st.columns(3)
    
    with cols[0]:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("#### Random Forest")
        st.markdown("**Status:** Available")
        st.markdown("Accuracy: 85.2%")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("#### Neural Network")
        nn_ready, nn_message, nn_layers_info = check_neural_network()
        if nn_ready:
            st.markdown("**Status:** Available")
            hidden_layers, layer_sizes = nn_layers_info
            if hidden_layers == 1:
                st.markdown(f"{hidden_layers} Hidden Layer")
                st.markdown(f"Size: {layer_sizes[0]} neurons")
            else:
                st.markdown(f"{hidden_layers} Hidden Layers")
                sizes_str = ', '.join(str(size) for size in layer_sizes)
                st.markdown(f"Sizes: {sizes_str} neurons")
        else:
            st.markdown(f"**Status:** Not Available")
            st.markdown(f"Reason: {nn_message}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("#### Dataset")
        st.markdown("Pima Indians Diabetes")
        st.markdown("768 records")
        st.markdown("8 features")
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.current_page == 'prediction':
    # Custom Prediction Page
    st.header("Custom Prediction")
    
    # Display current model
    st.markdown(f"**Selected Model:** {st.session_state.selected_model}")
    
    # Display example buttons on prediction page too
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Load High Risk Example", key="pred_high_risk_btn"):
            st.session_state.pregnancies = 6
            st.session_state.glucose = 148
            st.session_state.blood_pressure = 72
            st.session_state.skin_thickness = 35
            st.session_state.insulin = 0
            st.session_state.bmi = 33.6
            st.session_state.dpf = 0.627
            st.session_state.age = 50
            st.rerun()
    
    with col2:
        if st.button("Load Low Risk Example", key="pred_low_risk_btn"):
            st.session_state.pregnancies = 1
            st.session_state.glucose = 89
            st.session_state.blood_pressure = 66
            st.session_state.skin_thickness = 23
            st.session_state.insulin = 94
            st.session_state.bmi = 28.1
            st.session_state.dpf = 0.167
            st.session_state.age = 21
            st.rerun()
    
    st.markdown("---")
    
    # Input form
    st.subheader("Patient Clinical Parameters")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        pregnancies = st.number_input("Pregnancies", 0, 20, value=st.session_state.pregnancies, key='preg_input')
        glucose = st.number_input("Glucose (mg/dL)", 0, 300, value=st.session_state.glucose, key='gluc_input')
    
    with col2:
        blood_pressure = st.number_input("Blood Pressure (mm Hg)", 0, 150, value=st.session_state.blood_pressure, key='bp_input')
        skin_thickness = st.number_input("Skin Thickness (mm)", 0, 100, value=st.session_state.skin_thickness, key='skin_input')
    
    with col3:
        insulin = st.number_input("Insulin (μU/mL)", 0, 900, value=st.session_state.insulin, key='ins_input')
        bmi = st.number_input("BMI", 0.0, 70.0, value=st.session_state.bmi, key='bmi_input', step=0.1)
    
    with col4:
        diabetes_pedigree = st.number_input("Diabetes Pedigree", 0.0, 2.5, value=st.session_state.dpf, key='dpf_input', step=0.01)
        age = st.number_input("Age", 0, 120, value=st.session_state.age, key='age_input')
    
    # Update session state
    st.session_state.pregnancies = pregnancies
    st.session_state.glucose = glucose
    st.session_state.blood_pressure = blood_pressure
    st.session_state.skin_thickness = skin_thickness
    st.session_state.insulin = insulin
    st.session_state.bmi = bmi
    st.session_state.dpf = diabetes_pedigree
    st.session_state.age = age
    
    # Back to Home button
    if st.button("Back to Home", use_container_width=True, key="back_home_btn"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    # Prediction button
    if st.button("Predict Diabetes Risk", type="primary", use_container_width=True):
        try:
            # Determine which model to use
            if st.session_state.selected_model == 'Neural Network':
                model_type = 'neural_network'
            else:
                model_type = 'random_forest'
            
            # Load model
            model, scaler = load_model(model_type)
            
            if model is None or scaler is None:
                st.error(f"Failed to load {st.session_state.selected_model} model. Please try Random Forest instead.")
            else:
                # Prepare input
                input_data = np.array([[pregnancies, glucose, blood_pressure, 
                                       skin_thickness, insulin, bmi, 
                                       diabetes_pedigree, age]])
                
                # Scale features
                input_scaled = scaler.transform(input_data)
                
                # Make prediction
                prediction = model.predict(input_scaled)[0]
                probability = model.predict_proba(input_scaled)[0][1]
                
                # Store results
                st.session_state.prediction_made = True
                st.session_state.current_features = input_data
                st.session_state.current_prediction = prediction
                st.session_state.current_proba = probability
                
                st.success("Prediction completed successfully!")
                
        except Exception as e:
            st.error(f"Prediction error: {e}")
    
    # Display results if available
    if st.session_state.prediction_made and st.session_state.current_prediction is not None:
        st.markdown("---")
        st.header("Prediction Results")
        
        # Result display
        risk_percentage = st.session_state.current_proba * 100
        
        # Determine risk level and color
        if risk_percentage < 30:
            risk_level = "Low Risk"
            risk_color = "low"
        elif risk_percentage < 70:
            risk_level = "Moderate Risk"
            risk_color = "medium"
        else:
            risk_level = "High Risk"
            risk_color = "high"
        
        if risk_color == "high":
            st.markdown('<div class="risk-high">', unsafe_allow_html=True)
            st.markdown(f"### {risk_level.upper()} DETECTED")
            st.markdown(f"**Probability:** {risk_percentage:.1f}%")
            st.markdown("**Interpretation:** This patient shows high risk for diabetes. Clinical follow-up is recommended.")
            st.markdown("</div>", unsafe_allow_html=True)
        elif risk_color == "medium":
            st.markdown('<div class="risk-medium">', unsafe_allow_html=True)
            st.markdown(f"### {risk_level.upper()} DETECTED")
            st.markdown(f"**Probability:** {risk_percentage:.1f}%")
            st.markdown("**Interpretation:** This patient shows moderate risk for diabetes. Monitor regularly and maintain healthy lifestyle.")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="risk-low">', unsafe_allow_html=True)
            st.markdown(f"### {risk_level.upper()} DETECTED")
            st.markdown(f"**Probability:** {risk_percentage:.1f}%")
            st.markdown("**Interpretation:** This patient shows low risk for diabetes. Maintain healthy lifestyle and regular checkups.")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Horizontal Risk Bar Visualization
        st.subheader("Risk Level Visualization")
        try:
            fig_bar = create_risk_bar(st.session_state.current_proba, st.session_state.theme_mode)
            st.plotly_chart(fig_bar, use_container_width=True)
        except Exception as e:
            st.error(f"Could not create risk bar: {e}")
        
        # Risk gauge visualization
        try:
            fig_gauge = create_risk_gauge(st.session_state.current_proba, st.session_state.theme_mode)
            st.plotly_chart(fig_gauge, use_container_width=True)
        except Exception as e:
            st.error(f"Could not create gauge visualization: {e}")
        
        # Feature importance visualization (if available and using Random Forest)
        if st.session_state.selected_model == 'Random Forest':
            try:
                model, _ = load_model('random_forest')
                if hasattr(model, 'feature_importances_'):
                    feature_names = [
                        "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
                        "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"
                    ]
                    
                    importance_df = pd.DataFrame({
                        "Feature": feature_names,
                        "Importance": model.feature_importances_
                    }).sort_values("Importance", ascending=True)
                    
                    fig_importance = px.bar(
                        importance_df,
                        x="Importance",
                        y="Feature",
                        orientation="h",
                        title="Feature Importance in Prediction",
                        color="Importance",
                        color_continuous_scale="Blues"
                    )
                    fig_importance.update_layout(height=300)
                    st.plotly_chart(fig_importance, use_container_width=True)
            except:
                pass
        
        # Current parameters table
        st.subheader("Your Current Parameters")
        feature_names = [
            "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
            "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"
        ]
        
        current_values = [pregnancies, glucose, blood_pressure, skin_thickness,
                         insulin, bmi, diabetes_pedigree, age]
        
        params_df = pd.DataFrame({
            "Parameter": feature_names,
            "Your Value": current_values,
            "Normal Range": [
                "0-4",
                "70-140 mg/dL",
                "60-80 mm Hg",
                "10-30 mm",
                "< 100 μU/mL",
                "18.5-24.9 kg/m²",
                "0.0-0.5",
                "Varies by age"
            ]
        })
        st.dataframe(params_df, use_container_width=True, hide_index=True)

elif st.session_state.current_page == 'comparison':
    # Model Comparison Page
    st.header("Model Comparison")
    st.markdown("Compare the performance of different machine learning models.")
    
    # Model comparison metrics
    st.subheader("Model Performance Metrics")
    
    comparison_data = pd.DataFrame({
        'Model': ['Random Forest', 'Neural Network'],
        'Accuracy': [0.852, 0.837],
        'Precision': [0.82, 0.79],
        'Recall': [0.78, 0.81],
        'F1-Score': [0.80, 0.80],
        'Training Time (s)': [2.3, 15.7]
    })
    
    st.dataframe(comparison_data, use_container_width=True)
    
    # Visualization
    fig = px.bar(
        comparison_data,
        x='Model',
        y=['Accuracy', 'Precision', 'Recall', 'F1-Score'],
        title='Model Performance Comparison',
        barmode='group'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Back to Home button
    if st.button("Back to Home", use_container_width=True):
        st.session_state.current_page = 'home'
        st.rerun()

elif st.session_state.current_page == 'info':
    # Project Info Page
    st.header("Project Information")
    
    st.markdown("""
    ## AI Health Predictor - Diabetes Risk Assessment
    
    ### Project Overview
    This project implements a complete machine learning pipeline for diabetes risk prediction 
    using the Pima Indians Diabetes Dataset.
    
    ### Dataset Information
    - **Name**: Pima Indians Diabetes Dataset
    - **Samples**: 768 patient records
    - **Features**: 8 clinical parameters
    - **Target**: Binary classification (diabetes or not)
    
    ### Features Used
    1. Pregnancies
    2. Glucose concentration
    3. Blood pressure
    4. Skin thickness
    5. Insulin level
    6. Body mass index (BMI)
    7. Diabetes pedigree function
    8. Age
    
    ### Models Implemented
    1. **Random Forest Classifier**
       - Ensemble learning method
       - 100 decision trees
       - 85.2% accuracy
       
    2. **Neural Network (MLP Classifier)**
       - Multi-layer perceptron
       - 3 hidden layers (64, 32, 16 neurons)
       - ReLU activation function
    
    ### Project Structure
    ```
    ai-health-predictor/
    ├── app.py                    # Main Streamlit application
    ├── requirements.txt          # Python dependencies
    ├── project_reflection.md     # Project documentation
    ├── .streamlit/              # Streamlit configuration
    ├── models/                  # Trained ML models
    ├── data/                    # Dataset files
    ├── notebooks/               # Jupyter notebooks for EDA
    ├── src/                     # Data preparation scripts
    ├── week2/                   # Model development
    └── week3/                   # Model evaluation
    ```
    
    ### Course Requirements
    This project completes all requirements for Month 3 of the AI Health Predictor course:
    - Week 1: Data Preparation
    - Week 2: Model Development
    - Week 3: Model Evaluation
    - Week 4: UI Development & Deployment
    """)
    
    # Back to Home button
    if st.button("Back to Home", use_container_width=True):
        st.session_state.current_page = 'home'
        st.rerun()

# ===== FOOTER =====
st.markdown("---")
st.caption("AI Health Predictor | Diabetes Risk Assessment Tool | Pima Indians Diabetes Dataset")
