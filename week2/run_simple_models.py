"""
Week 2: Simple Model Training Script
Run this if you prefer not to use Jupyter Notebook
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)
import joblib
import json
import os
from datetime import datetime

print("="*70)
print("WEEK 2: AI HEALTH PREDICTOR - MODEL DEVELOPMENT")
print("="*70)

# Create directories
os.makedirs('week2/models', exist_ok=True)
os.makedirs('week2/reports', exist_ok=True)
os.makedirs('week2/data', exist_ok=True)

print("\nSTEP 1: Loading Data...")

# Check for existing data
csv_files = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.csv'):
            csv_files.append(os.path.join(root, file))

if csv_files:
    print(f"Found {len(csv_files)} CSV files")
    # Use the first CSV file
    data_path = csv_files[0]
    df = pd.read_csv(data_path)
    print(f"Loaded: {data_path}")
else:
    print("No CSV files found. Creating sample diabetes dataset...")
    np.random.seed(42)
    n_samples = 768
    df = pd.DataFrame({
        'Pregnancies': np.random.randint(0, 10, n_samples),
        'Glucose': np.random.randint(70, 200, n_samples),
        'BloodPressure': np.random.randint(60, 120, n_samples),
        'SkinThickness': np.random.randint(20, 50, n_samples),
        'Insulin': np.random.randint(0, 300, n_samples),
        'BMI': np.round(np.random.uniform(18, 40, n_samples), 1),
        'DiabetesPedigreeFunction': np.round(np.random.uniform(0.1, 1.5, n_samples), 3),
        'Age': np.random.randint(20, 70, n_samples),
        'Outcome': np.random.randint(0, 2, n_samples)
    })
    # Save the sample data
    df.to_csv('week2/data/sample_diabetes.csv', index=False)
    print("Saved sample data: week2/data/sample_diabetes.csv")

print(f"\nDataset shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

print("\nSTEP 2: Data Exploration...")

# Identify target
target_candidates = ['Outcome', 'target', 'diagnosis', 'result']
target_col = None
for col in target_candidates:
    if col in df.columns:
        target_col = col
        break
if target_col is None:
    target_col = df.columns[-1]

print(f"Target variable: '{target_col}'")
print(f"Target distribution:\n{df[target_col].value_counts()}")

# Handle missing values
if df.isnull().sum().sum() > 0:
    print(f"\nFilling {df.isnull().sum().sum()} missing values...")
    df = df.fillna(df.median())

# Separate features and target
X = df.drop(columns=[target_col])
y = df[target_col]

print(f"\nFeatures shape: {X.shape}")
print(f"Target shape: {y.shape}")

print("\nSTEP 3: Data Preparation...")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set: {X_train.shape}")
print(f"Testing set: {X_test.shape}")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\nSTEP 4: Training Models...")

# Define models
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'SVM': SVC(probability=True, random_state=42)
}

results = []

print("\nTraining progress:")
for name, model in models.items():
    print(f"  Training {name}...")
    model.fit(X_train_scaled, y_train)
    
    # Predictions
    y_pred = model.predict(X_test_scaled)
    
    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    # ROC-AUC if available
    if hasattr(model, 'predict_proba'):
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        roc_auc = roc_auc_score(y_test, y_pred_proba)
    else:
        roc_auc = None
    
    results.append({
        'Model': name,
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1-Score': f1,
        'ROC-AUC': roc_auc
    })
    
    print(f"    Accuracy: {accuracy:.4f}, F1: {f1:.4f}")

# Create results DataFrame
results_df = pd.DataFrame(results)
print("\n" + "="*60)
print("MODEL PERFORMANCE COMPARISON")
print("="*60)
print(results_df.to_string())

# Find best model
best_idx = results_df['Accuracy'].idxmax()
best_model_name = results_df.loc[best_idx, 'Model']
best_model = models[best_model_name]
best_accuracy = results_df.loc[best_idx, 'Accuracy']

print(f"\nBEST MODEL: {best_model_name}")
print(f"   Accuracy: {best_accuracy:.4f}")

print("\nSTEP 5: Evaluating Best Model...")

# Get predictions from best model
y_pred = best_model.predict(X_test_scaled)

print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(cm)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nSTEP 6: Saving Models and Reports...")

# Save scaler
joblib.dump(scaler, 'week2/models/scaler.pkl')
print("Scaler saved: week2/models/scaler.pkl")

# Save all models
for name, model in models.items():
    filename = f"week2/models/{name.lower().replace(' ', '_')}.pkl"
    joblib.dump(model, filename)
    print(f"{name} saved: {filename}")

# Save best model separately
joblib.dump(best_model, 'week2/models/best_model.pkl')
print(f"Best model saved: week2/models/best_model.pkl")

# Save feature names
feature_names = X.columns.tolist()
with open('week2/models/feature_names.json', 'w') as f:
    json.dump(feature_names, f)
print("Feature names saved: week2/models/feature_names.json")

# Create performance report
report = {
    'timestamp': datetime.now().isoformat(),
    'dataset': {
        'shape': df.shape,
        'target': target_col,
        'features': feature_names
    },
    'best_model': {
        'name': best_model_name,
        'accuracy': float(best_accuracy),
        'metrics': {
            'precision': float(results_df.loc[best_idx, 'Precision']),
            'recall': float(results_df.loc[best_idx, 'Recall']),
            'f1_score': float(results_df.loc[best_idx, 'F1-Score'])
        }
    },
    'all_models': results_df.to_dict('records')
}

with open('week2/reports/performance_report.json', 'w') as f:
    json.dump(report, f, indent=2)
print("Performance report saved: week2/reports/performance_report.json")

# Save predictions
predictions_df = pd.DataFrame({
    'actual': y_test.values,
    'predicted': y_pred
})
predictions_df.to_csv('week2/reports/test_predictions.csv', index=False)
print("Test predictions saved: week2/reports/test_predictions.csv")

# Save confusion matrix
cm_df = pd.DataFrame(cm,
                     index=['Actual Negative', 'Actual Positive'],
                     columns=['Predicted Negative', 'Predicted Positive'])
cm_df.to_csv('week2/reports/confusion_matrix.csv')
print("Confusion matrix saved: week2/reports/confusion_matrix.csv")

# Create visualization
print("\nSTEP 7: Creating Visualizations...")

plt.figure(figsize=(12, 5))

# Model comparison bar chart
plt.subplot(1, 2, 1)
x_pos = np.arange(len(results_df))
plt.bar(x_pos, results_df['Accuracy'], color=['skyblue', 'lightgreen', 'salmon', 'gold'])
plt.xticks(x_pos, results_df['Model'], rotation=45)
plt.title('Model Accuracy Comparison')
plt.ylabel('Accuracy')
plt.ylim(0, 1)

# Add value labels
for i, v in enumerate(results_df['Accuracy']):
    plt.text(i, v + 0.02, f'{v:.3f}', ha='center')

# Confusion matrix heatmap
plt.subplot(1, 2, 2)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Negative', 'Positive'],
            yticklabels=['Negative', 'Positive'])
plt.title(f'Confusion Matrix - {best_model_name}')
plt.ylabel('Actual')
plt.xlabel('Predicted')

plt.tight_layout()
plt.savefig('week2/reports/model_results.png', dpi=150, bbox_inches='tight')
print("Visualization saved: week2/reports/model_results.png")

print("\n" + "="*70)
print("WEEK 2 COMPLETED SUCCESSFULLY!")
print("="*70)
print("\nSummary:")
print(f"- Best Model: {best_model_name}")
print(f"- Accuracy: {best_accuracy:.4f}")
print(f"- Models Trained: {len(models)}")
print("\nFiles created:")
print("week2/models/")
for file in os.listdir('week2/models'):
    print(f"    {file}")
print("\nweek2/reports/")
for file in os.listdir('week2/reports'):
    print(f"    {file}")
print("\nNext: Proceed to Week 3 for UI development and deployment!")
