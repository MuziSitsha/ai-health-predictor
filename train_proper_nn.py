import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import warnings
warnings.filterwarnings('ignore')

print("Training proper neural network model...")

# Try to load real data first
try:
    df = pd.read_csv('data/diabetes.csv')
    print(f"Loaded real data: {df.shape}")
    X = df.drop('Outcome', axis=1).values
    y = df['Outcome'].values
except:
    # Create synthetic data
    print("Creating synthetic data...")
    np.random.seed(42)
    n_samples = 768
    
    # Realistic diabetes data ranges
    X = np.zeros((n_samples, 8))
    X[:, 0] = np.random.randint(0, 17, n_samples)  # Pregnancies
    X[:, 1] = np.random.randint(50, 200, n_samples)  # Glucose
    X[:, 2] = np.random.randint(40, 130, n_samples)  # BloodPressure
    X[:, 3] = np.random.randint(10, 100, n_samples)  # SkinThickness
    X[:, 4] = np.random.randint(0, 850, n_samples)   # Insulin
    X[:, 5] = np.random.uniform(18.0, 68.0, n_samples)  # BMI
    X[:, 6] = np.random.uniform(0.08, 2.5, n_samples)  # DiabetesPedigree
    X[:, 7] = np.random.randint(21, 82, n_samples)    # Age
    
    # Create target with realistic patterns
    risk_score = (
        (X[:, 1] - 100) / 100 +  # Glucose contribution
        (X[:, 5] - 25) / 20 +     # BMI contribution
        (X[:, 7] - 30) / 50 +     # Age contribution
        np.random.randn(n_samples) * 0.3  # Random noise
    )
    y = (risk_score > 0).astype(int)

print(f"Dataset: {X.shape[0]} samples, {y.sum()} positive cases ({y.sum()/len(y):.1%})")

# Split and scale
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
print("\nTraining neural network...")
model = MLPClassifier(
    hidden_layer_sizes=(64, 32, 16),  # 3 hidden layers as mentioned in your app
    activation='relu',
    solver='adam',
    alpha=0.0001,
    batch_size=32,
    learning_rate='constant',
    learning_rate_init=0.001,
    max_iter=500,
    random_state=42,
    verbose=True,
    early_stopping=True,
    validation_fraction=0.1
)

model.fit(X_train_scaled, y_train)

# Evaluate
from sklearn.metrics import accuracy_score, classification_report
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel accuracy: {accuracy:.2%}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, 'models/neural_network_model.pkl')
joblib.dump(scaler, 'models/nn_scaler.pkl')

print("\n✓ Model saved to: models/neural_network_model.pkl")
print("✓ Scaler saved to: models/nn_scaler.pkl")

# Verify
print("\nVerifying saved model...")
loaded_model = joblib.load('models/neural_network_model.pkl')
loaded_scaler = joblib.load('models/nn_scaler.pkl')

test_sample = X_test_scaled[0:1]
pred = loaded_model.predict(test_sample)
prob = loaded_model.predict_proba(test_sample)

print(f"Test prediction: {pred[0]}")
print(f"Test probabilities: {prob[0]}")
print(f"Model type: {type(loaded_model)}")
print(f"Has predict: {hasattr(loaded_model, 'predict')}")
print(f"Has predict_proba: {hasattr(loaded_model, 'predict_proba')}")
print(f"Hidden layers: {loaded_model.hidden_layer_sizes}")

print("\n✓ Neural network is ready for use!")
