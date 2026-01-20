import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import warnings
warnings.filterwarnings('ignore')

print("Training a new Neural Network model...")

# Create synthetic training data (or use real data if available)
np.random.seed(42)
n_samples = 1000

# Generate realistic diabetes data
X = np.zeros((n_samples, 8))

# Realistic ranges based on Pima Indians Diabetes Dataset
X[:, 0] = np.random.randint(0, 17, n_samples)  # Pregnancies: 0-16
X[:, 1] = np.random.randint(50, 200, n_samples)  # Glucose: 50-199
X[:, 2] = np.random.randint(40, 130, n_samples)  # BloodPressure: 40-129
X[:, 3] = np.random.randint(10, 100, n_samples)  # SkinThickness: 10-99
X[:, 4] = np.random.randint(0, 850, n_samples)   # Insulin: 0-846
X[:, 5] = np.random.uniform(18.0, 68.0, n_samples)  # BMI: 18-67.1
X[:, 6] = np.random.uniform(0.08, 2.5, n_samples)  # DiabetesPedigree: 0.08-2.42
X[:, 7] = np.random.randint(21, 82, n_samples)    # Age: 21-81

# Create target based on realistic patterns (higher glucose, BMI, age = higher risk)
y = (
    (X[:, 1] > 140).astype(int) * 0.4 +  # High glucose
    (X[:, 5] > 30).astype(int) * 0.3 +   # High BMI
    (X[:, 7] > 50).astype(int) * 0.2 +   # Older age
    (np.random.rand(n_samples) > 0.5).astype(int) * 0.1  # Random factor
)
y = (y > 0.5).astype(int)  # Convert to binary

print(f"Created dataset: {n_samples} samples")
print(f"Class distribution: {np.sum(y==0)} negative, {np.sum(y==1)} positive")

# Split data
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Neural Network
print("\nTraining MLP Classifier...")
nn_model = MLPClassifier(
    hidden_layer_sizes=(32, 16),  # Simpler architecture
    activation='relu',
    solver='adam',
    max_iter=300,
    random_state=42,
    verbose=True
)

nn_model.fit(X_train_scaled, y_train)

# Evaluate
from sklearn.metrics import accuracy_score
y_pred = nn_model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nNeural Network Accuracy: {accuracy:.2%}")

# Save model and scaler
joblib.dump(nn_model, 'models/neural_network_fixed.pkl')
joblib.dump(scaler, 'models/nn_scaler_fixed.pkl')

print("\n✓ Model saved as: models/neural_network_fixed.pkl")
print("✓ Scaler saved as: models/nn_scaler_fixed.pkl")

# Test the model
test_sample = X_test_scaled[0:1]
prediction = nn_model.predict(test_sample)
probability = nn_model.predict_proba(test_sample)
print(f"\nTest prediction: {prediction[0]}")
print(f"Test probabilities: {probability[0]}")
print(f"Model type: {type(nn_model)}")
print(f"Has predict: {hasattr(nn_model, 'predict')}")
print(f"Has predict_proba: {hasattr(nn_model, 'predict_proba')}")

# Also save as the main neural network file (backup old one first)
import os
if os.path.exists('models/neural_network_model.pkl'):
    os.rename('models/neural_network_model.pkl', 'models/neural_network_model_backup.pkl')
    print("\n✓ Backed up old neural network model")

os.rename('models/neural_network_fixed.pkl', 'models/neural_network_model.pkl')
os.rename('models/nn_scaler_fixed.pkl', 'models/nn_scaler.pkl')
print("✓ Set new model as primary neural network model")
