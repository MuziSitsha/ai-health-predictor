import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="AI Health Predictor - Diabetes Risk Assessment",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for theme FIRST before any use
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = 'light'

# Initialize page navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'  # 'home', 'high_risk', 'low_risk', 'custom'

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

# Custom CSS
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; color: #1E3A8A; text-align: center; margin-bottom: 1rem; }
    .sub-header { font-size: 1.2rem; color: #4B5563; text-align: center; margin-bottom: 2rem; }
    .risk-high { 
        background-color: #FEE2E2; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #DC2626;
        box-shadow: 0 4px 6px rgba(220, 38, 38, 0.1);
    }
    .risk-medium { 
        background-color: #FEF3C7; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #D97706;
        box-shadow: 0 4px 6px rgba(217, 119, 6, 0.1);
    }
    .risk-low { 
        background-color: #D1FAE5; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #059669;
        box-shadow: 0 4px 6px rgba(5, 150, 105, 0.1);
    }
    .metric-card { background-color: #F8FAFC; padding: 20px; border-radius: 10px; border: 1px solid #E2E8F0; text-align: center; }
    .what-if-btn { margin: 5px; width: 100%; }
</style>
""", unsafe_allow_html=True)

# Apply dark/light mode theme
if st.session_state.theme_mode == 'dark':
    st.markdown("""
    <style>
        .stApp {
            background-color: #1a1a1a;
            color: #e0e0e0;
        }
        [data-testid="stAppViewContainer"] {
            background-color: #1a1a1a;
            color: #e0e0e0;
        }
        [data-testid="stSidebar"] {
            background-color: #242424;
        }
        [data-testid="stHeader"] {
            background-color: transparent;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #e0e0e0 !important;
        }
        .main-header {
            color: #42a5f5 !important;
        }
        .sub-header {
            color: #90caf9 !important;
        }
        .risk-high {
            background-color: #5D1F1A !important;
            color: #ffcdd2 !important;
            border-left: 5px solid #ef5350 !important;
            box-shadow: 0 4px 6px rgba(239, 83, 80, 0.3) !important;
        }
        .risk-medium {
            background-color: #5d4a1a !important;
            color: #ffe082 !important;
            border-left: 5px solid #ffa726 !important;
            box-shadow: 0 4px 6px rgba(255, 167, 38, 0.3) !important;
        }
        .risk-low {
            background-color: #1b5e20 !important;
            color: #c8e6c9 !important;
            border-left: 5px solid #66bb6a !important;
            box-shadow: 0 4px 6px rgba(102, 187, 106, 0.3) !important;
        }
        .metric-card {
            background-color: #2a2a2a !important;
            color: #e0e0e0 !important;
            border: 1px solid #424242 !important;
        }
        p, label, span {
            color: #e0e0e0 !important;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        .stApp {
            background-color: #ffffff;
            color: #1a1a1a;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #1E3A8A !important;
        }
        .main-header {
            color: #1E3A8A !important;
        }
        .sub-header {
            color: #4B5563 !important;
        }
        .risk-high {
            background-color: #FEE2E2 !important;
            color: #7f1d1d !important;
            border-left: 5px solid #DC2626 !important;
            box-shadow: 0 4px 6px rgba(220, 38, 38, 0.15) !important;
        }
        .risk-medium {
            background-color: #FEF3C7 !important;
            color: #78350f !important;
            border-left: 5px solid #D97706 !important;
            box-shadow: 0 4px 6px rgba(217, 119, 6, 0.15) !important;
        }
        .risk-low {
            background-color: #D1FAE5 !important;
            color: #065f46 !important;
            border-left: 5px solid #059669 !important;
            box-shadow: 0 4px 6px rgba(5, 150, 105, 0.15) !important;
        }
        .metric-card {
            background-color: #F8FAFC !important;
            color: #1a1a1a !important;
            border: 1px solid #E2E8F0 !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">AI Health Predictor - Diabetes Risk Assessment</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Predict diabetes risk using machine learning based on clinical parameters</p>', unsafe_allow_html=True)

# Load model
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
        return None, None, None

model, scaler, feature_names = load_model()

# Sidebar theme toggle at the top
if st.sidebar.button("Switch to Dark Mode" if st.session_state.theme_mode == 'light' else "Switch to Light Mode", key="theme_toggle", use_container_width=True):
    st.session_state.theme_mode = 'dark' if st.session_state.theme_mode == 'light' else 'light'
    st.rerun()

st.sidebar.markdown("---")

# HOME PAGE
if st.session_state.current_page == 'home':
    # Show welcome content
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 30px; border-radius: 15px; background-color: #f0f9ff; border: 2px solid #0284c7;">
            <h2>High Risk Profile</h2>
            <p>See what a high risk profile looks like with concerning clinical parameters.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore High Risk Example", use_container_width=True, key="home_high_risk_btn"):
            st.session_state.current_page = 'high_risk'
            st.session_state.pregnancies = 6
            st.session_state.glucose = 180
            st.session_state.blood_pressure = 85
            st.session_state.skin_thickness = 40
            st.session_state.insulin = 300
            st.session_state.bmi = 35.0
            st.session_state.dpf = 1.2
            st.session_state.age = 55
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 30px; border-radius: 15px; background-color: #f0fdf4; border: 2px solid #22c55e;">
            <h2>Low Risk Profile</h2>
            <p>See what a low risk profile looks like with healthy clinical parameters.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Low Risk Example", use_container_width=True, key="home_low_risk_btn"):
            st.session_state.current_page = 'low_risk'
            st.session_state.pregnancies = 1
            st.session_state.glucose = 90
            st.session_state.blood_pressure = 70
            st.session_state.skin_thickness = 25
            st.session_state.insulin = 60
            st.session_state.bmi = 22.0
            st.session_state.dpf = 0.3
            st.session_state.age = 28
            st.rerun()
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 30px; border-radius: 15px; background-color: #fff7ed; border: 2px solid #f97316;">
            <h2>Custom Profile</h2>
            <p>Create your own profile by adjusting the parameters manually.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Create Custom Profile", use_container_width=True, key="home_custom_btn"):
            st.session_state.current_page = 'custom'
            st.rerun()
    
    st.markdown("---")
    st.markdown("""
    ### Welcome to AI Health Predictor
    
    This application helps you understand your diabetes risk based on clinical health parameters. 
    Choose one of the options above to get started:
    
    - **High Risk Example**: Demonstrates what a high-risk profile might look like
    - **Low Risk Example**: Shows characteristics of a healthy, low-risk profile
    - **Custom Profile**: Adjust your own clinical parameters to see your personal risk assessment
    
    Our machine learning model is trained on the Pima Indians Diabetes Dataset and provides
    risk predictions based on 8 key clinical measurements.
    """)

# CUSTOM PAGE - Full interface with sliders
elif st.session_state.current_page == 'custom':
st.sidebar.header("Patient Clinical Parameters")

st.sidebar.subheader("Quick Examples")
col1, col2, col3 = st.sidebar.columns(3)

# Create buttons and trigger actions immediately
with col1:
    if st.sidebar.button("High Risk", use_container_width=True, key="high_risk_btn"):
        st.session_state.pregnancies = 6
        st.session_state.glucose = 180
        st.session_state.blood_pressure = 85
        st.session_state.skin_thickness = 40
        st.session_state.insulin = 300
        st.session_state.bmi = 35.0
        st.session_state.dpf = 1.2
        st.session_state.age = 55
        st.rerun()

with col2:
    if st.sidebar.button("Low Risk", use_container_width=True, key="low_risk_btn"):
        st.session_state.pregnancies = 1
        st.session_state.glucose = 90
        st.session_state.blood_pressure = 70
        st.session_state.skin_thickness = 25
        st.session_state.insulin = 60
        st.session_state.bmi = 22.0
        st.session_state.dpf = 0.3
        st.session_state.age = 28
        st.rerun()

with col3:
    if st.sidebar.button("Reset", use_container_width=True, key="reset_btn"):
        st.session_state.pregnancies = 1
        st.session_state.glucose = 100
        st.session_state.blood_pressure = 72
        st.session_state.skin_thickness = 20
        st.session_state.insulin = 80
        st.session_state.bmi = 25.0
        st.session_state.dpf = 0.5
        st.session_state.age = 33
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("Clinical Measurements")

# Input sliders - direct binding with simple value assignment
pregnancies = st.sidebar.slider(
    "Number of Pregnancies", 0, 20, st.session_state.pregnancies,
    help="Number of times pregnant",
    key="pregnancies_slider"
)
st.session_state.pregnancies = pregnancies

glucose = st.sidebar.slider(
    "Plasma Glucose Concentration (mg/dL)", 0, 200, st.session_state.glucose,
    help="Glucose tolerance test result (2-hour)",
    key="glucose_slider"
)
st.session_state.glucose = glucose

blood_pressure = st.sidebar.slider(
    "Diastolic Blood Pressure (mm Hg)", 0, 122, st.session_state.blood_pressure,
    help="Diastolic blood pressure measurement",
    key="blood_pressure_slider"
)
st.session_state.blood_pressure = blood_pressure

skin_thickness = st.sidebar.slider(
    "Triceps Skin Fold Thickness (mm)", 0, 99, st.session_state.skin_thickness,
    help="Skin fold thickness measurement",
    key="skin_thickness_slider"
)
st.session_state.skin_thickness = skin_thickness

insulin = st.sidebar.slider(
    "2-Hour Serum Insulin (mu U/ml)", 0, 846, st.session_state.insulin,
    help="Insulin level measurement",
    key="insulin_slider"
)
st.session_state.insulin = insulin

bmi = st.sidebar.slider(
    "Body Mass Index (kg/m²)", 0.0, 67.1, st.session_state.bmi, 0.1,
    help="Weight in kg/(height in m)²",
    key="bmi_slider"
)
st.session_state.bmi = bmi

dpf = st.sidebar.slider(
    "Diabetes Pedigree Function", 0.0, 2.5, st.session_state.dpf, 0.01,
    help="Family history likelihood of diabetes",
    key="dpf_slider"
)
st.session_state.dpf = dpf

age = st.sidebar.slider(
    "Age (years)", 21, 81, st.session_state.age,
    help="Patient age in years",
    key="age_slider"
)
st.session_state.age = age

# Main prediction button
predict_button = st.sidebar.button("Predict Diabetes Risk", type="primary", use_container_width=True)

# Function to make prediction
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
    return None, None

# Create current features array
current_features = np.array([[st.session_state.pregnancies, st.session_state.glucose, 
                              st.session_state.blood_pressure, st.session_state.skin_thickness,
                              st.session_state.insulin, st.session_state.bmi, 
                              st.session_state.dpf, st.session_state.age]])

# Auto-make prediction whenever values change OR when button is clicked
st.session_state.current_features = current_features
st.session_state.current_prediction, st.session_state.current_proba = make_prediction(current_features)
st.session_state.prediction_made = True

# Display results - always show the prediction
if st.session_state.prediction_made and st.session_state.current_prediction is not None:
    risk_percentage = st.session_state.current_proba * 100

    # Display results
    st.header("Prediction Results")

    # Dynamic Risk Progress Bar
    risk_percentage = st.session_state.current_proba * 100
    
    # Determine color based on risk level
    if risk_percentage < 25:
        bar_color = "#059669"  # Green for low risk
        bar_label = "LOW RISK"
    elif risk_percentage < 50:
        bar_color = "#D97706"  # Orange for moderate risk
        bar_label = "MODERATE RISK"
    elif risk_percentage < 75:
        bar_color = "#DC2626"  # Red for high risk
        bar_label = "HIGH RISK"
    else:
        bar_color = "#7f1d1d"  # Dark red for very high risk
        bar_label = "VERY HIGH RISK"
    
    # Create progress bar HTML
    progress_html = f"""
    <div style="margin: 20px 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <strong style="font-size: 16px;">Risk Level: {bar_label}</strong>
            <strong style="font-size: 16px;">{risk_percentage:.1f}%</strong>
        </div>
        <div style="width: 100%; height: 30px; background-color: #e0e0e0; border-radius: 15px; overflow: hidden; box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);">
            <div style="width: {risk_percentage}%; height: 100%; background: linear-gradient(90deg, {bar_color}, {bar_color}cc); border-radius: 15px; transition: width 0.3s ease; display: flex; align-items: center; justify-content: flex-end; padding-right: 10px;">
                <span style="color: white; font-weight: bold; font-size: 12px;">{risk_percentage:.0f}%</span>
            </div>
        </div>
    </div>
    """
    st.markdown(progress_html, unsafe_allow_html=True)

    # Results columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Risk Probability", f"{risk_percentage:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        prediction_text = "HIGH RISK" if st.session_state.current_prediction == 1 else "LOW RISK"
        prediction_color = "#DC2626" if st.session_state.current_prediction == 1 else "#059669"
        st.markdown(f'<h3 style="color: {prediction_color}; text-align: center;">{prediction_text}</h3>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        confidence = st.session_state.current_proba if st.session_state.current_prediction == 1 else 1 - st.session_state.current_proba
        st.metric("Model Confidence", f"{confidence*100:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Risk classification
    st.subheader("Risk Classification")
    
# Risk classification with better accuracy
    if risk_percentage < 25:
        risk_class = "LOW RISK"
        risk_color = "#059669"
        risk_css = "risk-low"
        recommendation = "Excellent health status! Maintain your current healthy lifestyle with regular checkups every 2-3 years."
        risk_description = "Your diabetes risk is minimal. Continue with balanced diet and regular exercise."
    elif risk_percentage < 50:
        risk_class = "MODERATE RISK"
        risk_color = "#D97706"
        risk_css = "risk-medium"
        recommendation = "Your risk is moderate. Consider lifestyle modifications: reduce sugar intake, increase physical activity, and maintain healthy weight."
        risk_description = "Monitor your health metrics regularly. Annual checkups are recommended."
    elif risk_percentage < 75:
        risk_class = "HIGH RISK"
        risk_color = "#DC2626"
        risk_css = "risk-high"
        recommendation = "You have elevated diabetes risk. Consult a healthcare professional for a comprehensive assessment and personalized care plan."
        risk_description = "Implement lifestyle changes immediately and monitor glucose levels regularly."
    else:
        risk_class = "VERY HIGH RISK"
        risk_color = "#7f1d1d"
        risk_css = "risk-high"
        recommendation = "Critical: Please consult with a healthcare professional immediately. Early intervention is essential for preventing diabetes."
        risk_description = "Urgent medical consultation and monitoring required. Consider diabetes screening."

    st.markdown(f'<div class="{risk_css}">', unsafe_allow_html=True)
    st.markdown(f'<h3 style="color: {risk_color};">{risk_class} ZONE</h3>', unsafe_allow_html=True)
    st.markdown(f'<p><strong>{risk_description}</strong></p>', unsafe_allow_html=True)
    st.markdown(f'<p><strong>Recommendation:</strong> {recommendation}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # What-if Analysis Section
    st.subheader("What-If Scenario Analysis")
    st.write("See how changing parameters affects your risk:")
    
    whatif_col1, whatif_col2, whatif_col3 = st.columns(3)
    
    # Create containers for what-if results
    whatif_result_placeholder = st.empty()
    
    def run_whatif_scenario(scenario_name, modified_features):
        """Run a what-if scenario and display results without page refresh"""
        with whatif_result_placeholder.container():
            whatif_pred, whatif_proba = make_prediction(modified_features)
            if whatif_pred is not None:
                whatif_risk = whatif_proba * 100
                current_risk = risk_percentage
                diff = whatif_risk - current_risk
                
                st.info(f"""
                **{scenario_name}**
                - New Risk: {whatif_risk:.1f}%
                - Change: {'+' if diff > 0 else ''}{diff:.1f}%
                - New Classification: {'HIGH RISK' if whatif_pred == 1 else 'LOW RISK'}
                """)
    
    with whatif_col1:
        if st.button("Glucose -20 points", use_container_width=True, key="whatif1"):
            modified = current_features.copy()
            modified[0][1] = max(0, st.session_state.glucose - 20)
            run_whatif_scenario("Glucose 20 points lower", modified)
    
    with whatif_col2:
        if st.button("BMI -5 points", use_container_width=True, key="whatif2"):
            modified = current_features.copy()
            modified[0][5] = max(0, st.session_state.bmi - 5)
            run_whatif_scenario("BMI 5 points lower", modified)
    
    with whatif_col3:
        if st.button("Age -10 years", use_container_width=True, key="whatif3"):
            modified = current_features.copy()
            modified[0][7] = max(21, st.session_state.age - 10)
            run_whatif_scenario("10 years younger", modified)
    
    # Additional what-if scenarios
    st.write("More scenarios:")
    whatif_col4, whatif_col5, whatif_col6 = st.columns(3)
    
    with whatif_col4:
        if st.button("Blood Pressure -10", use_container_width=True, key="whatif4"):
            modified = current_features.copy()
            modified[0][2] = max(0, st.session_state.blood_pressure - 10)
            run_whatif_scenario("Blood Pressure 10 points lower", modified)
    
    with whatif_col5:
        if st.button("No Pregnancies", use_container_width=True, key="whatif5"):
            modified = current_features.copy()
            modified[0][0] = 0
            run_whatif_scenario("No pregnancies", modified)
    
    with whatif_col6:
        if st.button("Ideal BMI (22)", use_container_width=True, key="whatif6"):
            modified = current_features.copy()
            modified[0][5] = 22.0
            run_whatif_scenario("Ideal BMI (22.0)", modified)
    
    # Visualizations
    st.subheader("Risk Visualization")
    
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        # Risk gauge
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = risk_percentage,
            title = {"text": "Risk Gauge"},
            domain = {"x": [0, 1], "y": [0, 1]},
            gauge = {
                "axis": {"range": [0, 100]},
                "bar": {"color": risk_color},
                "steps": [
                    {"range": [0, 30], "color": "#D1FAE5"},
                    {"range": [30, 70], "color": "#FEF3C7"},
                    {"range": [70, 100], "color": "#FEE2E2"}
                ],
                "threshold": {
                    "line": {"color": "black", "width": 4},
                    "thickness": 0.75,
                    "value": risk_percentage
                }
            }
        ))
        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with viz_col2:
        # Feature importance
        if hasattr(model, 'feature_importances_'):
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
    
    # Current parameters table
    st.subheader("Your Current Parameters")
    params_df = pd.DataFrame({
        "Parameter": feature_names,
        "Your Value": current_features[0],
        "Normal Range": [
            "0-4",
            "70-140 mg/dL",
            "60-80 mm Hg",
            "10-30 mm",
            "< 100 mu U/ml",
            "18.5-24.9 kg/m²",
            "0.0-0.5",
            "Varies by age"
        ]
    })
    st.dataframe(params_df, use_container_width=True, hide_index=True)

# If no prediction made yet, show instructions
else:
    st.header("How to Use This Predictor")
    st.markdown("""
    1. Adjust the clinical parameters in the sidebar
    2. Click **'Predict Diabetes Risk'** to see your risk assessment
    3. Try the **'Show High Risk Example'** button to see high-risk profile
    4. Use **'What-If'** scenarios to see how changes affect risk
    
    ### High-Risk Indicators:
    - Glucose > 140 mg/dL
    - BMI > 30 kg/m²
    - Age > 45 years
    - Multiple pregnancies
    - Family history of diabetes (high Diabetes Pedigree)
    
    ### Model Information:
    - **Accuracy**: 85.34% on test data
    - **F1-Score**: 80.46% (balance of precision and recall)
    - **Training Data**: 537 patient records from Pima Indians Diabetes Dataset
    """)

# Sidebar model info
st.sidebar.markdown("---")
st.sidebar.subheader("Model Information")
st.sidebar.info("Model: Random Forest (Retrained)")
st.sidebar.info("Accuracy: 85.34%")
st.sidebar.info("F1-Score: 80.46%")
st.sidebar.info("Dataset: Pima Indians Diabetes")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; font-size: 0.9rem;">
    <p>AI Health Predictor | Month 3 Project | Machine Learning Application</p>
    <p>Dataset: Pima Indians Diabetes Dataset | Model: Random Forest Classifier</p>
    <p><strong>Disclaimer:</strong> This tool is for educational purposes only. Not a substitute for professional medical advice.</p>
</div>
""", unsafe_allow_html=True)
