import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
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

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #4B5563;
        text-align: center;
        margin-bottom: 2rem;
    }
    .risk-high {
        background-color: #FEE2E2;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #DC2626;
    }
    .risk-medium {
        background-color: #FEF3C7;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #D97706;
    }
    .risk-low {
        background-color: #D1FAE5;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #059669;
    }
    .metric-card {
        background-color: #F8FAFC;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<h1 class="main-header">AI Health Predictor - Diabetes Risk Assessment</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Predict diabetes risk using machine learning based on clinical parameters</p>', unsafe_allow_html=True)

# Load the best model - Random Forest
@st.cache_resource
def load_model():
    """Load the best performing model and scaler"""
    try:
        # Load Random Forest model (best performing - 85.34% accuracy)
        model = joblib.load("week2/models_retrained/random_forest.pkl")
        scaler = joblib.load("week2/models_retrained/scaler_retrained.pkl")
        
        # Get feature names from training data
        train_df = pd.read_csv("data/processed/train.csv")
        feature_names = [col for col in train_df.columns if col != 'Outcome']
        
        return model, scaler, feature_names
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None, None, None

# Load model
model, scaler, feature_names = load_model()

# Sidebar for input parameters
st.sidebar.header("Patient Clinical Parameters")

# Input fields with medical ranges
st.sidebar.subheader("Clinical Measurements")

pregnancies = st.sidebar.slider(
    "Number of Pregnancies", 
    min_value=0, 
    max_value=20, 
    value=1,
    help="Number of times pregnant"
)

glucose = st.sidebar.slider(
    "Plasma Glucose Concentration (mg/dL)", 
    min_value=0, 
    max_value=200, 
    value=100,
    help="Glucose tolerance test result (2-hour)"
)

blood_pressure = st.sidebar.slider(
    "Diastolic Blood Pressure (mm Hg)", 
    min_value=0, 
    max_value=122, 
    value=72,
    help="Diastolic blood pressure measurement"
)

skin_thickness = st.sidebar.slider(
    "Triceps Skin Fold Thickness (mm)", 
    min_value=0, 
    max_value=99, 
    value=20,
    help="Skin fold thickness measurement"
)

insulin = st.sidebar.slider(
    "2-Hour Serum Insulin (mu U/ml)", 
    min_value=0, 
    max_value=846, 
    value=80,
    help="Insulin level measurement"
)

bmi = st.sidebar.slider(
    "Body Mass Index (kg/m²)", 
    min_value=0.0, 
    max_value=67.1, 
    value=25.0,
    step=0.1,
    help="Weight in kg/(height in m)²"
)

dpf = st.sidebar.slider(
    "Diabetes Pedigree Function", 
    min_value=0.0, 
    max_value=2.5, 
    value=0.5,
    step=0.01,
    help="Family history likelihood of diabetes"
)

age = st.sidebar.slider(
    "Age (years)", 
    min_value=21, 
    max_value=81, 
    value=33,
    help="Patient age in years"
)

# Model information in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Model Information")
st.sidebar.info(f"Model: Random Forest (Retrained)")
st.sidebar.info(f"Accuracy: 85.34%")
st.sidebar.info(f"F1-Score: 80.46%")
st.sidebar.info(f"Dataset: Pima Indians Diabetes")
st.sidebar.info(f"Training Samples: 537 patients")

# Create feature array
features = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, 
                     insulin, bmi, dpf, age]])

# Prediction button
if st.sidebar.button("Predict Diabetes Risk", type="primary", use_container_width=True):
    if model is not None and scaler is not None:
        try:
            # Scale features
            features_scaled = scaler.transform(features)
            
            # Predict
            prediction = model.predict(features_scaled)[0]
            prediction_proba = model.predict_proba(features_scaled)[0][1]
            
            # Convert to percentage
            risk_percentage = prediction_proba * 100
            
            # Display results in main area
            st.header("Prediction Results")
            
            # Create columns for results
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Risk Probability", f"{risk_percentage:.1f}%")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                prediction_text = "HIGH RISK" if prediction == 1 else "LOW RISK"
                prediction_color = "#DC2626" if prediction == 1 else "#059669"
                st.markdown(f'<h3 style="color: {prediction_color}; text-align: center;">{prediction_text}</h3>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                confidence = prediction_proba if prediction == 1 else 1 - prediction_proba
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
            
            # Visualizations
            st.subheader("Risk Visualization")
            
            # Create columns for visualizations
            viz_col1, viz_col2 = st.columns(2)
            
            with viz_col1:
                # Risk gauge
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = risk_percentage,
                    title = {'text': "Risk Gauge"},
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    gauge = {
                        'axis': {'range': [0, 100]},
                        'bar': {'color': risk_color},
                        'steps': [
                            {'range': [0, 30], 'color': "#D1FAE5"},
                            {'range': [30, 70], 'color': "#FEF3C7"},
                            {'range': [70, 100], 'color': "#FEE2E2"}
                        ],
                        'threshold': {
                            'line': {'color': "black", 'width': 4},
                            'thickness': 0.75,
                            'value': risk_percentage
                        }
                    }
                ))
                fig_gauge.update_layout(height=300)
                st.plotly_chart(fig_gauge, use_container_width=True)
            
            with viz_col2:
                # Feature importance
                if hasattr(model, 'feature_importances_'):
                    importance_df = pd.DataFrame({
                        'Feature': feature_names,
                        'Importance': model.feature_importances_
                    }).sort_values('Importance', ascending=True)
                    
                    fig_importance = px.bar(
                        importance_df, 
                        x='Importance', 
                        y='Feature',
                        orientation='h',
                        title="Feature Importance in Prediction",
                        color='Importance',
                        color_continuous_scale='Blues'
                    )
                    fig_importance.update_layout(height=300)
                    st.plotly_chart(fig_importance, use_container_width=True)
                else:
                    # Show input values instead
                    input_df = pd.DataFrame({
                        'Feature': feature_names,
                        'Value': features[0]
                    })
                    fig_values = px.bar(
                        input_df,
                        x='Value',
                        y='Feature',
                        orientation='h',
                        title="Input Clinical Values",
                        color='Value',
                        color_continuous_scale='Viridis'
                    )
                    fig_values.update_layout(height=300)
                    st.plotly_chart(fig_values, use_container_width=True)
            
            # Detailed breakdown
            st.subheader("Clinical Parameters Analysis")
            
            # Create a dataframe with reference ranges
            reference_data = {
                'Parameter': feature_names,
                'Your Value': features[0],
                'Normal Range': [
                    '0-4',
                    '70-140 mg/dL',
                    '60-80 mm Hg',
                    '10-30 mm',
                    '< 100 mu U/ml',
                    '18.5-24.9 kg/m²',
                    '0.0-0.5',
                    'Varies by age'
                ],
                'Medical Significance': [
                    'Higher pregnancies may indicate gestational diabetes history',
                    'Elevated glucose is primary diabetes indicator',
                    'High BP associated with metabolic syndrome',
                    'Indicates body fat distribution',
                    'Insulin resistance marker',
                    'BMI > 25 increases diabetes risk',
                    'Family history likelihood score',
                    'Risk increases with age'
                ]
            }
            
            ref_df = pd.DataFrame(reference_data)
            st.dataframe(ref_df, use_container_width=True, hide_index=True)
            
            # What-if analysis section
            st.subheader("What-If Analysis")
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                if st.button("What if glucose was 20 points lower?"):
                    features_whatif = features.copy()
                    features_whatif[0][1] = max(0, glucose - 20)
                    features_scaled_whatif = scaler.transform(features_whatif)
                    proba_whatif = model.predict_proba(features_scaled_whatif)[0][1] * 100
                    diff = risk_percentage - proba_whatif
                    st.info(f"Risk would be {proba_whatif:.1f}% ({diff:.1f}% lower)")
            
            with col_b:
                if st.button("What if BMI was 5 points lower?"):
                    features_whatif = features.copy()
                    features_whatif[0][5] = max(0, bmi - 5)
                    features_scaled_whatif = scaler.transform(features_whatif)
                    proba_whatif = model.predict_proba(features_scaled_whatif)[0][1] * 100
                    diff = risk_percentage - proba_whatif
                    st.info(f"Risk would be {proba_whatif:.1f}% ({diff:.1f}% lower)")
            
            with col_c:
                if st.button("What if age was 10 years younger?"):
                    features_whatif = features.copy()
                    features_whatif[0][7] = max(21, age - 10)
                    features_scaled_whatif = scaler.transform(features_whatif)
                    proba_whatif = model.predict_proba(features_scaled_whatif)[0][1] * 100
                    diff = risk_percentage - proba_whatif
                    st.info(f"Risk would be {proba_whatif:.1f}% ({diff:.1f}% lower)")
            
        except Exception as e:
            st.error(f"Prediction error: {str(e)}")
    else:
        st.error("Model not loaded properly. Please check the model files.")

# Main content area (when no prediction made yet)
else:
    # Project information
    st.header("About This Application")
    
    st.markdown("""
    This AI Health Predictor uses machine learning to assess diabetes risk based on clinical parameters from the Pima Indians Diabetes Dataset.
    
    ### How It Works:
    1. **Input Parameters**: Enter clinical measurements in the sidebar
    2. **Machine Learning**: The trained Random Forest model analyzes the input
    3. **Risk Assessment**: Get personalized diabetes risk prediction
    4. **Clinical Insights**: Understand which factors contribute most to risk
    
    ### Model Performance:
    - **Accuracy**: 85.34% on test data
    - **F1-Score**: 80.46% (balance of precision and recall)
    - **ROC-AUC**: 91.38% (discrimination ability)
    - **Training Data**: 537 patient records
    
    ### Clinical Parameters Used:
    """)
    
    # Display feature descriptions
    features_info = pd.DataFrame({
        'Parameter': [
            'Pregnancies',
            'Glucose',
            'Blood Pressure',
            'Skin Thickness',
            'Insulin',
            'BMI',
            'Diabetes Pedigree Function',
            'Age'
        ],
        'Description': [
            'Number of times pregnant',
            'Plasma glucose concentration (2-hour oral glucose tolerance test)',
            'Diastolic blood pressure (mm Hg)',
            'Triceps skin fold thickness (mm)',
            '2-Hour serum insulin (mu U/ml)',
            'Body mass index (weight in kg/(height in m)²)',
            'Diabetes pedigree function (family history likelihood)',
            'Age in years'
        ],
        'Normal Range': [
            '0-4',
            '70-140 mg/dL',
            '60-80 mm Hg',
            '10-30 mm',
            '< 100 mu U/ml',
            '18.5-24.9 kg/m²',
            '0.0-0.5',
            'Varies'
        ]
    })
    
    st.dataframe(features_info, use_container_width=True, hide_index=True)
    
    # Important disclaimer
    st.markdown("---")
    st.warning("""
    **Important Medical Disclaimer**: 
    This tool is for educational and informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. 
    Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; font-size: 0.9rem;">
    <p>AI Health Predictor | Month 3 Project | Machine Learning Application</p>
    <p>Dataset: Pima Indians Diabetes Dataset | Model: Random Forest Classifier</p>
</div>
""", unsafe_allow_html=True)
