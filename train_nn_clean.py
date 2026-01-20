# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
import joblib
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("DIABETES NEURAL NETWORK TRAINING")
print("=" * 60)

# Load the dataset
print("\n1. Loading dataset...")
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
column_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
                'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']

try:
    df = pd.read_csv(url, names=column_names)
    print(f"   Dataset loaded: {df.shape[0]} samples, {df.shape[1]} features")
except Exception as e:
    print(f"   Error loading dataset: {e}")
    print("   Creating synthetic data for demonstration...")
    np.random.seed(42)
    n_samples = 768
    df = pd.DataFrame({
        'Pregnancies': np.random.randint(0, 17, n_samples),
        'Glucose': np.random.randint(0, 199, n_samples),
        'BloodPressure': np.random.randint(0, 122, n_samples),
        'SkinThickness': np.random.randint(0, 99, n_samples),
        'Insulin': np.random.randint(0, 846, n_samples),
        'BMI': np.random.uniform(0, 67.1, n_samples),
        'DiabetesPedigreeFunction': np.random.uniform(0.08, 2.42, n_samples),
        'Age': np.random.randint(21, 81, n_samples),
        'Outcome': np.random.randint(0, 2, n_samples)
    })

# Data preparation
print(f"\n2. Data preparation...")
print(f"   Outcome: {sum(df['Outcome'] == 0)} non-diabetic, {sum(df['Outcome'] == 1)} diabetic")

X = df.drop('Outcome', axis=1)
y = df['Outcome']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
X_train, X_val, y_train, y_val = train_test_split(
    X_train, y_train, test_size=0.2, random_state=42, stratify=y_train
)

print(f"   Training set: {X_train.shape}")
print(f"   Validation set: {X_val.shape}")
print(f"   Test set: {X_test.shape}")

# Standardize
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

joblib.dump(scaler, 'nn_scaler.pkl')
print("   Scaler saved: nn_scaler.pkl")

# Create neural network
print("\n3. Creating Neural Network...")
model = MLPClassifier(
    hidden_layer_sizes=(64, 32, 16),
    activation='relu',
    solver='adam',
    max_iter=200,
    random_state=42,
    early_stopping=True
)

print("   Training model...")
model.fit(X_train_scaled, y_train)

# Evaluate
print("\n4. Evaluating model...")
train_score = model.score(X_train_scaled, y_train)
val_score = model.score(X_val_scaled, y_val)
test_score = model.score(X_test_scaled, y_test)

print(f"   Training Accuracy: {train_score:.4f}")
print(f"   Validation Accuracy: {val_score:.4f}")
print(f"   Test Accuracy: {test_score:.4f}")

# Predictions
y_pred = model.predict(X_test_scaled)
y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]

# Metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
roc_auc = roc_auc_score(y_test, y_pred_proba)

print(f"\n5. Detailed metrics:")
print(f"   Accuracy: {accuracy:.4f}")
print(f"   Precision: {precision:.4f}")
print(f"   Recall: {recall:.4f}")
print(f"   ROC-AUC: {roc_auc:.4f}")

# Save model
joblib.dump(model, 'neural_network_model.pkl')
print("\n6. Saving model...")
print("   Model saved: neural_network_model.pkl")

print("\n" + "=" * 60)
print("TRAINING COMPLETE!")
print("=" * 60)
