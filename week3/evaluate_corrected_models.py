import pandas as pd
import numpy as np
import joblib
import tensorflow as tf
from tensorflow import keras
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import os
import json

print("WEEK 3: EVALUATING CORRECTED MODELS")
print("=" * 60)

# Load test data
test_df = pd.read_csv('data/processed/test.csv')
X_test = test_df.drop(columns=['Outcome'])
y_test = test_df['Outcome']

print(f"Test data: {X_test.shape}, Positive cases: {y_test.sum()}/{len(y_test)}")

# Load retrained scaler
scaler = joblib.load('week2/models_retrained/scaler_retrained.pkl')
X_test_scaled = scaler.transform(X_test)

# Evaluate all corrected models
models_to_evaluate = [
    ('Logistic Regression (retrained)', 'week2/models_retrained/logistic_regression.pkl', 'sklearn'),
    ('Random Forest (retrained)', 'week2/models_retrained/random_forest.pkl', 'sklearn'),
    ('Gradient Boosting (retrained)', 'week2/models_retrained/gradient_boosting.pkl', 'sklearn'),
    ('SVM (retrained)', 'week2/models_retrained/svm.pkl', 'sklearn'),
    ('Deep Learning (corrected)', 'week2/models_corrected/deep_learning_corrected.h5', 'keras')
]

results = []

for model_name, model_path, model_type in models_to_evaluate:
    if not os.path.exists(model_path):
        print(f"Skipping {model_name}: File not found")
        continue
    
    try:
        print(f"\nEvaluating {model_name}...")
        
        # Load model
        if model_type == 'keras':
            model = keras.models.load_model(model_path)
            y_pred_proba = model.predict(X_test_scaled, verbose=0).flatten()
            y_pred = (y_pred_proba > 0.5).astype(int)
        else:
            model = joblib.load(model_path)
            y_pred = model.predict(X_test_scaled)
            y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        auc_score = roc_auc_score(y_test, y_pred_proba)
        
        results.append({
            'Model': model_name,
            'Accuracy': f"{accuracy:.4f}",
            'Precision': f"{precision:.4f}",
            'Recall': f"{recall:.4f}",
            'F1_Score': f"{f1:.4f}",
            'ROC_AUC': f"{auc_score:.4f}"
        })
        
        print(f"  Accuracy:  {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall:    {recall:.4f}")
        print(f"  F1-Score:  {f1:.4f}")
        print(f"  ROC-AUC:   {auc_score:.4f}")
        
        cm = confusion_matrix(y_test, y_pred)
        print(f"  Confusion Matrix:\n{cm}")
        
    except Exception as e:
        print(f"  Error: {e}")

# Display results
if results:
    print("\n" + "=" * 60)
    print("FINAL MODEL COMPARISON (CORRECTED MODELS)")
    print("=" * 60)
    
    results_df = pd.DataFrame(results)
    print(results_df.to_string(index=False))
    
    # Find best model
    results_df['F1_Score_num'] = results_df['F1_Score'].astype(float)
    best_idx = results_df['F1_Score_num'].idxmax()
    best_model = results_df.loc[best_idx, 'Model']
    best_f1 = results_df.loc[best_idx, 'F1_Score']
    
    print(f"\nBEST MODEL FOR DEPLOYMENT: {best_model}")
    print(f"F1-Score: {best_f1}")
    
    # Save final decision
    final_decision = {
        'best_model': best_model,
        'best_model_path': next(path for name, path, _ in models_to_evaluate if name == best_model),
        'all_results': results,
        'selection_criteria': 'Highest F1-Score',
        'test_set_size': len(X_test),
        'test_positive_cases': int(y_test.sum())
    }
    
    with open('week3/final_model_selection.json', 'w') as f:
        json.dump(final_decision, f, indent=2)
    
    print("\nFinal model selection saved to 'week3/final_model_selection.json'")
    
    # Integration instructions
    print("\n" + "=" * 60)
    print("INTEGRATION INSTRUCTIONS FOR WEEK 4:")
    print("=" * 60)
    print(f"1. Use '{best_model}' for your Streamlit app")
    print(f"2. Model file: {final_decision['best_model_path']}")
    print(f"3. Scaler file: week2/models_retrained/scaler_retrained.pkl")
    print(f"4. Features (in order): {list(X_test.columns)}")
    print("\nRun: streamlit run app.py to test integration")
    
else:
    print("No models were successfully evaluated.")

print("\nEvaluation complete.")
