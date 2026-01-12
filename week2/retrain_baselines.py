import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import joblib
import os

print("Retraining baseline models with current scikit-learn version")
print("=" * 60)

# Load training data
train_df = pd.read_csv('data/processed/train.csv')
X_train = train_df.drop(columns=['Outcome'])
y_train = train_df['Outcome']

print(f"Training data shape: {X_train.shape}")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Save scaler
os.makedirs('week2/models_retrained', exist_ok=True)
joblib.dump(scaler, 'week2/models_retrained/scaler_retrained.pkl')

# Train models
models = {
    'logistic_regression': LogisticRegression(max_iter=1000, random_state=42),
    'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'gradient_boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'svm': SVC(probability=True, random_state=42)
}

# Load validation data for quick test
val_df = pd.read_csv('data/processed/validation.csv')
X_val = val_df.drop(columns=['Outcome'])
y_val = val_df['Outcome']
X_val_scaled = scaler.transform(X_val)

for name, model in models.items():
    print(f"\nTraining {name}...")
    model.fit(X_train_scaled, y_train)
    
    # Save model
    joblib.dump(model, f'week2/models_retrained/{name}.pkl')
    
    # Quick validation
    if hasattr(model, 'predict_proba'):
        y_pred_proba = model.predict_proba(X_val_scaled)[:, 1]
    else:
        y_pred = model.predict(X_val_scaled)
        y_pred_proba = np.zeros_like(y_pred, dtype=float)
    
    accuracy = model.score(X_val_scaled, y_val)
    print(f"  Validation accuracy: {accuracy:.4f}")

print("\nAll baseline models retrained and saved to 'week2/models_retrained/'")
