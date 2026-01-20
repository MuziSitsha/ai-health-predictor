import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
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
except:
    print("   Could not load from URL, trying local file...")
    # If you have the CSV locally
    df = pd.read_csv('diabetes.csv')

# Check for missing values
print(f"\n2. Data quality check:")
print(f"   Missing values: {df.isnull().sum().sum()}")
print(f"   Outcome distribution:")
print(f"   - No Diabetes (0): {sum(df['Outcome'] == 0)} samples")
print(f"   - Diabetes (1): {sum(df['Outcome'] == 1)} samples")

# Prepare features and target
X = df.drop('Outcome', axis=1)
y = df['Outcome']

# Split the data
print("\n3. Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
X_train, X_val, y_train, y_val = train_test_split(
    X_train, y_train, test_size=0.2, random_state=42, stratify=y_train
)

print(f"   Training set: {X_train.shape}")
print(f"   Validation set: {X_val.shape}")
print(f"   Test set: {X_test.shape}")

# Standardize the features
print("\n4. Standardizing features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# Save the scaler
joblib.dump(scaler, 'neural_network_scaler.pkl')
print("   Scaler saved: neural_network_scaler.pkl")

# Build the neural network
print("\n5. Building neural network...")
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    layers.Dropout(0.3),
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(16, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='binary_crossentropy',
    metrics=['accuracy', keras.metrics.AUC(name='auc')]
)

print("   Model architecture:")
model.summary()

# Train the model
print("\n6. Training model...")
early_stopping = keras.callbacks.EarlyStopping(
    patience=20,
    restore_best_weights=True
)

history = model.fit(
    X_train_scaled, y_train,
    validation_data=(X_val_scaled, y_val),
    epochs=100,
    batch_size=32,
    callbacks=[early_stopping],
    verbose=1
)

# Evaluate the model
print("\n7. Evaluating model...")
# On validation set
val_loss, val_accuracy, val_auc = model.evaluate(X_val_scaled, y_val, verbose=0)
print(f"   Validation Accuracy: {val_accuracy:.4f}")
print(f"   Validation AUC: {val_auc:.4f}")

# On test set
test_loss, test_accuracy, test_auc = model.evaluate(X_test_scaled, y_test, verbose=0)
print(f"   Test Accuracy: {test_accuracy:.4f}")
print(f"   Test AUC: {test_auc:.4f}")

# Make predictions
y_pred_proba = model.predict(X_test_scaled)
y_pred = (y_pred_proba > 0.5).astype(int).flatten()

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred_proba)

print(f"\n8. Detailed metrics on test set:")
print(f"   Accuracy:  {accuracy:.4f}")
print(f"   Precision: {precision:.4f}")
print(f"   Recall:    {recall:.4f}")
print(f"   ROC-AUC:   {roc_auc:.4f}")

# Save the model
print("\n9. Saving model...")
model.save('diabetes_neural_network.h5')
print("   Model saved: diabetes_neural_network.h5")

# Compare with Random Forest if available
print("\n10. Comparison with baseline (if available)...")
try:
    rf_model = joblib.load('random_forest.pkl')
    rf_pred = rf_model.predict(X_test_scaled)
    rf_proba = rf_model.predict_proba(X_test_scaled)[:, 1]
    
    rf_accuracy = accuracy_score(y_test, rf_pred)
    rf_auc = roc_auc_score(y_test, rf_proba)
    
    print(f"   Random Forest Accuracy: {rf_accuracy:.4f}")
    print(f"   Random Forest AUC:      {rf_auc:.4f}")
    print(f"   Neural Network Accuracy: {accuracy:.4f}")
    print(f"   Neural Network AUC:      {roc_auc:.4f}")
    
    if accuracy > rf_accuracy:
        print("   ✅ Neural Network outperforms Random Forest on accuracy")
    else:
        print("   ⚠ Random Forest outperforms Neural Network on accuracy")
        
except FileNotFoundError:
    print("   Random Forest model not found for comparison")

print("\n" + "=" * 60)
print("TRAINING COMPLETE!")
print("=" * 60)
print("\nFiles created:")
print("1. diabetes_neural_network.h5 - Neural network model")
print("2. neural_network_scaler.pkl - Feature scaler")
print("\nNext steps:")
print("1. Update app.py to use this model")
print("2. Add model comparison to your Streamlit app")
