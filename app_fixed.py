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

# Custom CSS
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; color: #1E3A8A; text-align: center; margin-bottom: 1rem; }
    .sub-header { font-size: 1.2rem; color: #4B5563; text-align: center; margin-bottom: 2rem; }
    .risk-high { background-color: #FEE2E2; padding: 15px; border-radius: 10px; border-left: 5px solid #DC2626; }
    .risk-medium { background-color: #FEF3C7; padding: 15px; border-radius: 10px; border-left: 5px solid #D97706; }
    .risk-low { background-color: #D1FAE5; padding: 15px; border-radius: 10px; border-left: 5px solid #059669; }
    .metric-card { background-color: #F8FAFC; padding: 20px; border-radius: 10px; border: 1px solid #E2E8F0; text-align: center; }
    .what-if-btn { margin: 5px; width: 100%; }
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

# Initialize session state for predictions
if 'prediction_made' not in st.session_state:
    st.session_state.prediction_made = False
if 'current_features' not in st.session_state:
    st.session_state.current_features = None
if 'current_prediction' not in st.session_state:
    st.session_state.current_prediction = None
if 'current_proba' not in st.session_state:
    st.session_state.current_proba = None

# Sidebar
st.sidebar.header("Patient Clinical Parameters")
st.sidebar.subheader("Clinical Measurements")

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

# Input sliders - use separate widget keys to allow session state modification
pregnancies = st.sidebar.slider(
    "Number of Pregnancies", 0, 20, st.session_state.pregnancies,
    help="Number of times pregnant",
    key="preg_input"
)
if pregnancies != st.session_state.pregnancies:
    st.session_state.pregnancies = pregnancies

glucose = st.sidebar.slider(
    "Plasma Glucose Concentration (mg/dL)", 0, 200, st.session_state.glucose,
    help="Glucose tolerance test result (2-hour)",
    key="glucose_input"
)
if glucose != st.session_state.glucose:
    st.session_state.glucose = glucose

blood_pressure = st.sidebar.slider(
    "Diastolic Blood Pressure (mm Hg)", 0, 122, st.session_state.blood_pressure,
    help="Diastolic blood pressure measurement",
    key="bp_input"
)
if blood_pressure != st.session_state.blood_pressure:
    st.session_state.blood_pressure = blood_pressure

skin_thickness = st.sidebar.slider(
    "Triceps Skin Fold Thickness (mm)", 0, 99, st.session_state.skin_thickness,
    help="Skin fold thickness measurement",
    key="skin_input"
)
if skin_thickness != st.session_state.skin_thickness:
    st.session_state.skin_thickness = skin_thickness

insulin = st.sidebar.slider(
    "2-Hour Serum Insulin (mu U/ml)", 0, 846, st.session_state.insulin,
    help="Insulin level measurement",
    key="insulin_input"
)
if insulin != st.session_state.insulin:
    st.session_state.insulin = insulin

bmi = st.sidebar.slider(
    "Body Mass Index (kg/mÂ²)", 0.0, 67.1, st.session_state.bmi, 0.1,
    help="Weight in kg/(height in m)Â²",
    key="bmi_input"
)
if bmi != st.session_state.bmi:
    st.session_state.bmi = bmi

dpf = st.sidebar.slider(
    "Diabetes Pedigree Function", 0.0, 2.5, st.session_state.dpf, 0.01,
    help="Family history likelihood of diabetes",
    key="dpf_input"
)
if dpf != st.session_state.dpf:
    st.session_state.dpf = dpf

age = st.sidebar.slider(
    "Age (years)", 21, 81, st.session_state.age,
    help="Patient age in years",
    key="age_input"
)
if age != st.session_state.age:
    st.session_state.age = age

# HIGH RISK EXAMPLE button
st.sidebar.markdown("---")
st.sidebar.subheader("Quick Examples")

if st.sidebar.button("Show High Risk Example", type="secondary"):
    # Set values for high risk profile
    st.session_state.pregnancies = 6
    st.session_state.glucose = 180
    st.session_state.blood_pressure = 85
    st.session_state.skin_thickness = 40
    st.session_state.insulin = 300
    st.session_state.bmi = 35.0
    st.session_state.dpf = 1.2
    st.session_state.age = 55
    st.rerun()

if st.sidebar.button("Show Low Risk Example", type="secondary"):
    # Set values for low risk profile
    st.session_state.pregnancies = 1
    st.session_state.glucose = 90
    st.session_state.blood_pressure = 70
    st.session_state.skin_thickness = 25
    st.session_state.insulin = 60
    st.session_state.bmi = 22.0
    st.session_state.dpf = 0.3
    st.session_state.age = 28
    st.rerun()

if st.sidebar.button("Reset to Default", type="secondary"):
    # Reset to default values
    st.session_state.pregnancies = 1
    st.session_state.glucose = 100
    st.session_state.blood_pressure = 72
    st.session_state.skin_thickness = 20
    st.session_state.insulin = 80
    st.session_state.bmi = 25.0
    st.session_state.dpf = 0.5
    st.session_state.age = 33
    st.rerun()

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

# Make prediction if button clicked or if we need to update
if predict_button:
    st.session_state.current_features = current_features
    st.session_state.current_prediction, st.session_state.current_proba = make_prediction(current_features)
    st.session_state.prediction_made = True
    st.rerun()

# Display results if prediction was made
if st.session_state.prediction_made and st.session_state.current_prediction is not None:
    risk_percentage = st.session_state.current_proba * 100
    
    # Display results
    st.header("Prediction Results")
    
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
    
    if risk_percentage < 30:
        risk_class = "LOW RISK"
        risk_color = "#059669"
        risk_css = "risk-low"
        recommendation = "Maintain current healthy lifestyle with regular checkups."
    elif risk_percentage < 70:
        risk_class = "MEDIUM RISK"
        risk_color = "#D97706"
        risk_css = "risk-medium"
        recommendation = "Consider lifestyle modifications and consult healthcare provider for monitoring."
    else:
        risk_class = "HIGH RISK"
        risk_color = "#DC2626"
        risk_css = "risk-high"
        recommendation = "Strongly recommend consultation with healthcare professional for comprehensive assessment."
    
    st.markdown(f'<div class="{risk_css}">', unsafe_allow_html=True)
    st.markdown(f'<h3 style="color: {risk_color};">{risk_class} ZONE</h3>', unsafe_allow_html=True)
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
