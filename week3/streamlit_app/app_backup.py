"""
Week 3: Streamlit UI for AI Health Predictor
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import os
import sys

# Add the parent directory to path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="AI Health Predictor",
    page_icon="Ìø•",
    layout="wide"
)

# Title
st.title("Ìø• AI Health Predictor")
st.markdown("Predict diabetes risk based on health parameters")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Make Prediction", "Model Info", "About"])

def load_model_and_scaler():
    """Load the trained model and scaler"""
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

if page == "Home":
    st.header("Welcome to AI Health Predictor")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### About this App
        This application uses machine learning to predict diabetes risk 
        based on health parameters.
        
        **Features:**
        - Real-time risk prediction
        - Multiple model comparison
        - Detailed probability analysis
        - Model performance visualization
        """)
    
    with col2:
        st.markdown("""
        ### How to Use
        1. Go to **Make Prediction** page
        2. Enter health parameters
        3. Click **Predict** button
        4. View your risk assessment
        
        **Model Performance:**
        - Accuracy: 75.97%
        - Best Model: Random Forest
        - Trained on 768 samples
        """)
    
    # Show sample of training data
    st.subheader("Sample Training Data")
    try:
        df_sample = pd.read_csv('data/diabetes.csv')
        st.dataframe(df_sample.head(10), use_container_width=True)
    except:
        st.info("Sample data not available")

elif page == "Make Prediction":
    st.header("Make a Prediction")
    
    # Load model
    model, scaler, feature_names = load_model_and_scaler()
    
    if model and scaler and feature_names:
        # Create input form
        with st.form("prediction_form"):
            st.subheader("Enter Health Parameters")
            
            # Create input fields based on feature names
            inputs = {}
            cols = st.columns(2)
            
            # Map common diabetes features
            feature_mapping = {
                'Pregnancies': (0, 20, 0, "Number of pregnancies"),
                'Glucose': (0, 200, 100, "Glucose level (mg/dL)"),
                'BloodPressure': (0, 150, 70, "Blood pressure (mm Hg)"),
                'SkinThickness': (0, 100, 20, "Skin thickness (mm)"),
                'Insulin': (0, 300, 80, "Insulin level (ŒºU/mL)"),
                'BMI': (0.0, 50.0, 25.0, "Body Mass Index"),
                'DiabetesPedigreeFunction': (0.0, 2.5, 0.5, "Diabetes pedigree function"),
                'Age': (0, 100, 30, "Age (years)")
            }
            
            for i, feature in enumerate(feature_names[:8]):  # Show first 8 features
                col_idx = i % 2
                with cols[col_idx]:
                    if feature in feature_mapping:
                        min_val, max_val, default_val, help_text = feature_mapping[feature]
                        if feature in ['BMI', 'DiabetesPedigreeFunction']:
                            inputs[feature] = st.number_input(
                                f"{feature}",
                                min_value=float(min_val),
                                max_value=float(max_val),
                                value=float(default_val),
                                step=0.1,
                                help=help_text
                            )
                        else:
                            inputs[feature] = st.number_input(
                                f"{feature}",
                                min_value=min_val,
                                max_value=max_val,
                                value=default_val,
                                help=help_text
                            )
                    else:
                        inputs[feature] = st.number_input(
                            f"{feature}",
                            value=0.0,
                            help="Enter value"
                        )
            
            # Submit button
            submitted = st.form_submit_button("Predict Diabetes Risk")
            
            if submitted:
                # Prepare input data
                input_data = []
                for feature in feature_names:
                    input_data.append(inputs.get(feature, 0.0))
                
                input_array = np.array(input_data).reshape(1, -1)
                
                # Scale the input
                input_scaled = scaler.transform(input_array)
                
                # Make prediction
                prediction = model.predict(input_scaled)[0]
                probability = model.predict_proba(input_scaled)[0][1]
                
                # Display results
                st.subheader("Prediction Results")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Prediction", "Diabetic" if prediction == 1 else "Non-Diabetic")
                
                with col2:
                    st.metric("Probability", f"{probability:.1%}")
                
                with col3:
                    risk_level = "High" if probability > 0.7 else "Medium" if probability > 0.3 else "Low"
                    st.metric("Risk Level", risk_level)
                
                # Progress bar for probability
                st.progress(float(probability))
                st.caption(f"Diabetes Risk Probability: {probability:.1%}")
                
                # Interpretation
                st.subheader("Interpretation")
                if prediction == 1:
                    st.warning("""
                    ‚ö†Ô∏è **Potential Diabetes Risk Detected**
                    
                    Recommendations:
                    - Consult with a healthcare professional
                    - Monitor blood sugar levels regularly
                    - Maintain a healthy diet and exercise routine
                    - Schedule regular check-ups
                    """)
                else:
                    st.success("""
                    ‚úÖ **Low Diabetes Risk**
                    
                    Keep up the good work:
                    - Continue healthy lifestyle habits
                    - Regular health check-ups
                    - Balanced diet and exercise
                    """)
                
                # Feature importance
                if hasattr(model, 'feature_importances_'):
                    st.subheader("Feature Importance")
                    importance_df = pd.DataFrame({
                        'Feature': feature_names,
                        'Importance': model.feature_importances_
                    }).sort_values('Importance', ascending=False)
                    
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.barh(importance_df['Feature'][:10], importance_df['Importance'][:10])
                    ax.set_xlabel('Importance')
                    ax.set_title('Top 10 Feature Importance')
                    st.pyplot(fig)

elif page == "Model Info":
    st.header("Model Information")
    
    # Load performance report
    try:
        with open('week2/reports/performance_report.json', 'r') as f:
            report = json.load(f)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Best Model")
            st.metric("Model", report['best_model']['name'])
            st.metric("Accuracy", f"{report['best_model']['accuracy']:.2%}")
            st.metric("Precision", f"{report['best_model']['metrics']['precision']:.2%}")
            st.metric("Recall", f"{report['best_model']['metrics']['recall']:.2%}")
            st.metric("F1-Score", f"{report['best_model']['metrics']['f1_score']:.2%}")
        
        with col2:
            st.subheader("Dataset Info")
            st.metric("Total Samples", report['dataset']['shape'][0])
            st.metric("Features", len(report['dataset']['features']))
            st.metric("Target Variable", report['dataset']['target'])
        
        # Show all models comparison
        st.subheader("All Models Comparison")
        models_df = pd.DataFrame(report['all_models'])
        st.dataframe(models_df.style.format({
            'Accuracy': '{:.2%}',
            'Precision': '{:.2%}',
            'Recall': '{:.2%}',
            'F1-Score': '{:.2%}',
            'ROC-AUC': '{:.3f}'
        }), use_container_width=True)
        
        # Show confusion matrix
        st.subheader("Confusion Matrix")
        try:
            cm_df = pd.read_csv('week2/reports/confusion_matrix.csv', index_col=0)
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(cm_df.astype(float), annot=True, fmt='.0f', cmap='Blues', ax=ax)
            ax.set_title('Confusion Matrix')
            st.pyplot(fig)
        except:
            st.info("Confusion matrix not available")
            
    except Exception as e:
        st.error(f"Error loading model info: {e}")

elif page == "About":
    st.header("About This Project")
    
    st.markdown("""
    ### AI Health Predictor
    
    **Project Overview:**
    This is a machine learning application that predicts diabetes risk based on 
    health parameters. The project is part of a 3-month AI development program.
    
    **Week 1:** Data Preparation
    - Data collection and cleaning
    - Exploratory data analysis
    - Feature engineering
    
    **Week 2:** Model Development
    - Multiple model training (Logistic Regression, Random Forest, etc.)
    - Model evaluation and comparison
    - Model saving and reporting
    
    **Week 3:** UI Development & Deployment
    - Streamlit web interface
    - Model deployment
    - Cloud hosting
    
    **Technical Stack:**
    - Python 3.12
    - Scikit-learn for machine learning
    - Streamlit for web interface
    - Pandas/Numpy for data processing
    - Matplotlib/Seaborn for visualization
    
    **Dataset:**
    - Pima Indians Diabetes Dataset
    - 768 samples, 8 features
    - Binary classification (Diabetic/Non-Diabetic)
    
    **Disclaimer:**
    This tool is for educational purposes only. It is not a substitute for 
    professional medical advice, diagnosis, or treatment.
    """)

# Footer
st.markdown("---")
st.markdown("¬© 2024 AI Health Predictor | Educational Project | Week 3 Submission")
