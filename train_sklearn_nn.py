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
print("DIABETES NEURAL NETWORK TRAINING (scikit-learn)")
print("=" * 60)

# Load the dataset
print("\n1. Loading dataset...")
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
column_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']

try:
    df = pd.read_csv(url, names=column_names)
    print(f"   ‚úÖ Dataset loaded: {df.shape[0]} samples, {df.shape[1]} features")
except Exception as e:
    print(f"   ‚ùå Error loading dataset: {e}")
    # Create synthetic data
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
    print(f"   ‚úÖ Created synthetic dataset: {df.shape[0]} samples")

# Data preparation
print(f"\n2. Data preparation...")
print(f"   Outcome distribution: {sum(df['Outcome'] == 0)} non-diabetic, {sum(df['Outcome'] == 1)} diabetic")

X = df.drop('Outcome', axis=1)
y = df['Outcome']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
X_train, X_val, y_train, y_val = train_test_split(
    X_train, y_train, test_size=0.2, random_state=42, stratify=y_train
)

print(f"   ‚úÖ Training set: {X_train.shape}")
print(f"   ‚úÖ Validation set: {X_val.shape}")
print(f"   ‚úÖ Test set: {X_test.shape}")

# Standardize
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

joblib.dump(scaler, 'sklearn_nn_scaler.pkl')
print("   ‚úÖ Scaler saved: sklearn_nn_scaler.pkl")

# Create neural network
print("\n3. Creating Neural Network...")
model = MLPClassifier(
    hidden_layer_sizes=(64, 32, 16),  # 3 hidden layers
    activation='relu',
    solver='adam',
    alpha=0.0001,
    batch_size=32,
    learning_rate='constant',
    learning_rate_init=0.001,
    max_iter=200,
    random_state=42,
    early_stopping=True,
    validation_fraction=0.2,
    n_iter_no_change=20,
    verbose=True
)

print("   ‚úÖ Training model...")
model.fit(X_train_scaled, y_train)

# Evaluate
print("\n4. Evaluating model...")
train_score = model.score(X_train_scaled, y_train)
val_score = model.score(X_val_scaled, y_val)
test_score = model.score(X_test_scaled, y_test)

print(f"   Ì≥ä Training Accuracy:   {train_score:.4f}")
print(f"   Ì≥ä Validation Accuracy: {val_score:.4f}")
print(f"   Ì≥ä Test Accuracy:       {test_score:.4f}")

# Predictions
y_pred = model.predict(X_test_scaled)
y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]

# Metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
roc_auc = roc_auc_score(y_test, y_pred_proba)

print(f"\n5. Detailed metrics:")
print(f"   Ì≥à Accuracy:  {accuracy:.4f}")
print(f"   Ì≥à Precision: {precision:.4f}")
print(f"   Ì≥à Recall:    {recall:.4f}")
print(f"   Ì≥à ROC-AUC:   {roc_auc:.4f}")

# Save model
joblib.dump(model, 'sklearn_neural_network.pkl')
print("\n6. Saving model...")
print("   ‚úÖ Model saved: sklearn_neural_network.pkl")

# Compare with Random Forest
print("\n7. Comparing with Random Forest...")
try:
    rf_model = joblib.load('random_forest.pkl')
    rf_scaler = joblib.load('scaler_retrained.pkl')
    
    X_test_rf_scaled = rf_scaler.transform(X_test)
    rf_pred = rf_model.predict(X_test_rf_scaled)
    rf_proba = rf_model.predict_proba(X_test_rf_scaled)[:, 1]
    
    rf_accuracy = accuracy_score(y_test, rf_pred)
    rf_auc = roc_auc_score(y_test, rf_proba)
    
    print(f"   Ì¥ñ Random Forest Accuracy: {rf_accuracy:.4f}")
    print(f"   Ì¥ñ Random Forest AUC:      {rf_auc:.4f}")
    print(f"   Ì∑† Neural Network Accuracy: {accuracy:.4f}")
    print(f"   Ì∑† Neural Network AUC:      {roc_auc:.4f}")
    
    # Save comparison
    comparison = pd.DataFrame({
        'Model': ['Random Forest', 'Neural Network (scikit-learn)'],
        'Accuracy': [rf_accuracy, accuracy],
        'AUC': [rf_auc, roc_auc],
        'Precision': [precision_score(y_test, rf_pred, zero_division=0), precision],
        'Recall': [recall_score(y_test, rf_pred, zero_division=0), recall]
    })
    comparison.to_csv('sklearn_model_comparison.csv', index=False)
    print("   ‚úÖ Comparison saved: sklearn_model_comparison.csv")
    
except FileNotFoundError:
    print("   ‚ö† Random Forest model not found for comparison")

print("\n" + "=" * 60)
print("Ìæâ TRAINING COMPLETE!")
print("=" * 60)
print("\nÌ≥Å Files created:")
print("1. sklearn_neural_network.pkl - Neural network model")
print("2. sklearn_nn_scaler.pkl - Feature scaler")
print("3. sklearn_model_comparison.csv - Model comparison")
print("\nÌ∫Ä Next steps:")
print("1. Update app.py to include this model")
print("2. Add model comparison visualization")
