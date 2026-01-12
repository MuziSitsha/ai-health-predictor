import pandas as pd
import numpy as np
import joblib
import tensorflow as tf
from tensorflow import keras
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                           f1_score, roc_auc_score, confusion_matrix, 
                           classification_report, roc_curve, auc)
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json

print("WEEK 3: MODEL EVALUATION & INTEGRATION")
print("=" * 60)

# Create week3 directory if it doesn't exist
os.makedirs('week3', exist_ok=True)
os.makedirs('week3/plots', exist_ok=True)

# 1. LOAD TEST DATA
print("\n1. Loading test data...")
test_df = pd.read_csv('data/processed/test.csv')
X_test = test_df.drop(columns=['Outcome'])
y_test = test_df['Outcome']
feature_names = X_test.columns.tolist()

print(f"Test data shape: {X_test.shape}")
print(f"Features: {feature_names}")
print(f"Test samples: {len(X_test)}, Positive cases: {y_test.sum()} ({y_test.sum()/len(y_test)*100:.1f}%)")

# 2. LOAD SCALER
print("\n2. Loading feature scaler...")
scaler = None
if os.path.exists('week2/models/scaler.pkl'):
    scaler = joblib.load('week2/models/scaler.pkl')
    X_test_scaled = scaler.transform(X_test)
    print("   Scaler loaded and applied to test data")
else:
    X_test_scaled = X_test.values
    print("   No scaler found. Using raw features.")

# 3. LOAD AND EVALUATE MODELS
print("\n3. Loading and evaluating models...")
models_info = {
    'Logistic Regression': {'path': 'week2/models/logistic_regression.pkl', 'type': 'sklearn'},
    'Random Forest': {'path': 'week2/models/random_forest.pkl', 'type': 'sklearn'},
    'Gradient Boosting': {'path': 'week2/models/gradient_boosting.pkl', 'type': 'sklearn'},
    'SVM': {'path': 'week2/models/svm.pkl', 'type': 'sklearn'},
    'Deep Learning (Keras)': {'path': 'week2/models/deep_learning_model.h5', 'type': 'keras'}
}

results = []
all_predictions = {}

for model_name, info in models_info.items():
    model_path = info['path']
    model_type = info['type']
    
    if not os.path.exists(model_path):
        print(f"   Skipping {model_name}: File not found at {model_path}")
        continue
    
    try:
        print(f"\n   Evaluating {model_name}...")
        
        # Load model
        if model_type == 'keras':
            model = keras.models.load_model(model_path)
        else:
            model = joblib.load(model_path)
        
        # Make predictions
        if model_type == 'keras':
            y_pred_proba = model.predict(X_test_scaled, verbose=0).flatten()
            y_pred = (y_pred_proba > 0.5).astype(int)
        else:
            if hasattr(model, 'predict_proba'):
                y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
            else:
                # For SVM without probability
                y_pred = model.predict(X_test_scaled)
                y_pred_proba = np.zeros_like(y_pred, dtype=float)
                y_pred_proba[y_pred == 1] = 0.9
                y_pred_proba[y_pred == 0] = 0.1
            
            y_pred = model.predict(X_test_scaled)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        auc_score = roc_auc_score(y_test, y_pred_proba) if len(np.unique(y_pred_proba)) > 1 else 0.5
        
        # Store results
        results.append({
            'Model': model_name,
            'Accuracy': accuracy,
            'Precision': precision,
            'Recall': recall,
            'F1_Score': f1,
            'ROC_AUC': auc_score
        })
        
        # Store predictions for later visualization
        all_predictions[model_name] = {
            'y_true': y_test,
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba,
            'model_type': model_type
        }
        
        print(f"     Accuracy:  {accuracy:.4f}")
        print(f"     Precision: {precision:.4f}")
        print(f"     Recall:    {recall:.4f}")
        print(f"     F1-Score:  {f1:.4f}")
        print(f"     ROC-AUC:   {auc_score:.4f}")
        
        # Print confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        print(f"     Confusion Matrix:\n{cm}")
        
    except Exception as e:
        print(f"     Error evaluating {model_name}: {e}")

# 4. COMPARE MODELS
print("\n" + "=" * 60)
print("MODEL COMPARISON SUMMARY")
print("=" * 60)

if results:
    results_df = pd.DataFrame(results)
    
    # Format for display
    display_df = results_df.copy()
    for col in ['Accuracy', 'Precision', 'Recall', 'F1_Score', 'ROC_AUC']:
        display_df[col] = display_df[col].apply(lambda x: f"{x:.4f}")
    
    print(display_df.to_string(index=False))
    
    # Save results
    results_df.to_csv('week3/model_comparison_results.csv', index=False)
    print("\nDetailed results saved to 'week3/model_comparison_results.csv'")
    
    # Find best model (using F1-Score as primary metric)
    best_f1_idx = results_df['F1_Score'].idxmax()
    best_model_name = results_df.loc[best_f1_idx, 'Model']
    best_f1 = results_df.loc[best_f1_idx, 'F1_Score']
    
    print(f"\nBEST MODEL: {best_model_name}")
    print(f"Primary Reason: Highest F1-Score ({best_f1:.4f})")
    
    # Save best model info for UI
    best_model_info = {
        'best_model': best_model_name,
        'best_model_file': models_info[best_model_name]['path'],
        'metrics': results_df.loc[best_f1_idx].to_dict(),
        'selected_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
        'selection_criteria': 'Highest F1-Score (balance of precision and recall)'
    }
    
    with open('week3/best_model_info.json', 'w') as f:
        json.dump(best_model_info, f, indent=2)
    
    print(f"Best model info saved to 'week3/best_model_info.json'")
    
    # 5. CREATE VISUALIZATIONS
    print("\n" + "=" * 60)
    print("CREATING VISUALIZATIONS")
    print("=" * 60)
    
    # 5a. Model comparison bar chart
    plt.figure(figsize=(12, 8))
    
    metrics_to_plot = ['Accuracy', 'Precision', 'Recall', 'F1_Score', 'ROC_AUC']
    x = np.arange(len(results_df))
    width = 0.15
    
    fig, ax = plt.subplots(figsize=(14, 8))
    for i, metric in enumerate(metrics_to_plot):
        offset = (i - len(metrics_to_plot)/2) * width
        bars = ax.bar(x + offset, results_df[metric], width, label=metric)
    
    ax.set_xlabel('Models')
    ax.set_ylabel('Score')
    ax.set_title('Model Performance Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(results_df['Model'], rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('week3/plots/model_comparison.png', dpi=150, bbox_inches='tight')
    print("   Saved: week3/plots/model_comparison.png")
    
    # 5b. ROC Curves
    plt.figure(figsize=(10, 8))
    for model_name, preds in all_predictions.items():
        if len(np.unique(preds['y_pred_proba'])) > 1:
            fpr, tpr, _ = roc_curve(preds['y_true'], preds['y_pred_proba'])
            roc_auc = auc(fpr, tpr)
            plt.plot(fpr, tpr, lw=2, label=f'{model_name} (AUC = {roc_auc:.3f})')
    
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curves - All Models')
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)
    plt.savefig('week3/plots/roc_curves.png', dpi=150)
    print("   Saved: week3/plots/roc_curves.png")
    
    # 5c. Confusion matrix for best model
    if best_model_name in all_predictions:
        plt.figure(figsize=(8, 6))
        cm = confusion_matrix(all_predictions[best_model_name]['y_true'], 
                             all_predictions[best_model_name]['y_pred'])
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['No Diabetes', 'Diabetes'],
                   yticklabels=['No Diabetes', 'Diabetes'])
        plt.title(f'Confusion Matrix - {best_model_name}')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig('week3/plots/best_model_confusion_matrix.png', dpi=150)
        print("   Saved: week3/plots/best_model_confusion_matrix.png")
    
    plt.close('all')
    
    # 6. CREATE SAMPLE PREDICTIONS
    print("\n" + "=" * 60)
    print("SAMPLE PREDICTIONS")
    print("=" * 60)
    
    # Take 5 random samples from test set
    sample_indices = np.random.choice(len(X_test), min(5, len(X_test)), replace=False)
    sample_predictions = []
    
    for idx in sample_indices:
        sample_features = X_test.iloc[idx].values.reshape(1, -1)
        true_label = y_test.iloc[idx]
        
        if scaler is not None:
            sample_features_scaled = scaler.transform(sample_features)
        else:
            sample_features_scaled = sample_features
        
        # Get prediction from best model
        if best_model_name in models_info:
            model_path = models_info[best_model_name]['path']
            if models_info[best_model_name]['type'] == 'keras':
                model = keras.models.load_model(model_path)
                pred_proba = model.predict(sample_features_scaled, verbose=0)[0][0]
            else:
                model = joblib.load(model_path)
                if hasattr(model, 'predict_proba'):
                    pred_proba = model.predict_proba(sample_features_scaled)[0, 1]
                else:
                    pred_proba = model.predict(sample_features_scaled)[0]
            
            pred_label = 1 if pred_proba > 0.5 else 0
            
            sample_predictions.append({
                'sample_id': idx,
                'features': X_test.iloc[idx].to_dict(),
                'true_outcome': int(true_label),
                'predicted_probability': float(pred_proba),
                'predicted_outcome': int(pred_label),
                'correct': bool(true_label == pred_label)
            })
    
    # Save sample predictions
    if sample_predictions:
        sample_df = pd.DataFrame(sample_predictions)
        sample_df.to_csv('week3/sample_predictions.csv', index=False)
        print("\nSample predictions saved to 'week3/sample_predictions.csv'")
        print("\nFirst 2 sample predictions:")
        for i in range(min(2, len(sample_predictions))):
            pred = sample_predictions[i]
            print(f"\nSample {pred['sample_id']}:")
            print(f"  True Outcome: {pred['true_outcome']} ({'Diabetes' if pred['true_outcome'] == 1 else 'No Diabetes'})")
            print(f"  Predicted Probability: {pred['predicted_probability']:.3f}")
            print(f"  Predicted Outcome: {pred['predicted_outcome']} ({'Diabetes' if pred['predicted_outcome'] == 1 else 'No Diabetes'})")
            print(f"  Correct: {'YES' if pred['correct'] else 'NO'}")
    
    print("\n" + "=" * 60)
    print("WEEK 3 EVALUATION COMPLETE")
    print("=" * 60)
    print("\nNEXT STEPS FOR WEEK 4:")
    print("1. The best model has been identified and saved")
    print(f"2. Integrate '{best_model_name}' into your Streamlit UI (app.py)")
    print("3. Update app.py to load the correct model file")
    print("4. Test the full pipeline")
    print("5. Deploy to Streamlit Community Cloud")
    
else:
    print("No models were successfully evaluated.")
    print("Please ensure you have completed Week 2 model development.")

print("\nScript execution complete.")
