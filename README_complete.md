# AI Health Predictor - Diabetes Risk Assessment

A machine learning application that predicts diabetes risk based on clinical parameters using the Pima Indians Diabetes Dataset.

## Features
- Interactive web interface built with Streamlit
- Real-time diabetes risk prediction
- Multiple visualization tools (risk gauge, feature importance charts)
- Support for both light and dark themes
- Educational what-if scenario analysis

## Project Structure
ai-health-predictor/
├── app.py # Main Streamlit application
├── requirements.txt # Python dependencies
├── project_reflection.md # Project documentation and reflections
├── week1_completion_summary.txt
├── week2_model_development.ipynb
├── src/ # Data preparation scripts
├── notebooks/ # Exploratory data analysis
├── week2/ # Model development
├── week3/ # Model evaluation
├── data/ # Dataset and processed data
└── .streamlit/ # Streamlit configuration

text

## Installation & Local Run
```bash
# Clone repository
git clone https://github.com/MuziSitsha/ai-health-predictor.git
cd ai-health-predictor

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
Live Deployment
[Add your Streamlit Community Cloud deployment link here after deployment]

Model Information
Primary Model: Random Forest Classifier (0.85 accuracy)

Alternative Model: Deep Learning Neural Network (Keras/TensorFlow)

Dataset: Pima Indians Diabetes Dataset (768 samples, 8 features)

Course Requirements
This project completes all requirements for Month 3 of the AI Health Predictor course:

Week 1: Data Preparation

Week 2: Model Development

Week 3: Model Evaluation

Week 4: UI Development & Deployment
