import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

print("Fixing Deep Learning Model for Diabetes Dataset")
print("=" * 60)

# Load training data
train_df = pd.read_csv('data/processed/train.csv')
X_train = train_df.drop(columns=['Outcome']).values
y_train = train_df['Outcome'].values

print(f"Training data shape: {X_train.shape}")
print(f"Number of features: {X_train.shape[1]}")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Save the scaler
os.makedirs('week2/models_corrected', exist_ok=True)
joblib.dump(scaler, 'week2/models_corrected/scaler_corrected.pkl')

# Create CORRECT deep learning model with 8 input features
def create_diabetes_dl_model():
    model = keras.Sequential([
        # Input layer: 8 features for diabetes dataset
        layers.Input(shape=(8,)),
        
        # Hidden layers
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.3),
        
        layers.Dense(32, activation='relu'),
        layers.Dropout(0.3),
        
        layers.Dense(16, activation='relu'),
        
        # Output layer (binary classification)
        layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy', 
                 keras.metrics.Precision(name='precision'),
                 keras.metrics.Recall(name='recall'),
                 keras.metrics.AUC(name='auc')]
    )
    
    return model

# Create and train the model
model = create_diabetes_dl_model()
model.summary()

# Callbacks
callbacks = [
    keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True, monitor='val_auc'),
    keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=5, min_lr=1e-6)
]

# Load validation data
val_df = pd.read_csv('data/processed/validation.csv')
X_val = val_df.drop(columns=['Outcome']).values
y_val = val_df['Outcome'].values
X_val_scaled = scaler.transform(X_val)

print("\nTraining corrected deep learning model...")
history = model.fit(
    X_train_scaled, y_train,
    validation_data=(X_val_scaled, y_val),
    epochs=100,
    batch_size=16,
    callbacks=callbacks,
    verbose=1
)

# Save the corrected model
model.save('week2/models_corrected/deep_learning_corrected.h5')
print("\nCorrected deep learning model saved to 'week2/models_corrected/deep_learning_corrected.h5'")

# Quick test with validation data
val_loss, val_acc, val_precision, val_recall, val_auc = model.evaluate(X_val_scaled, y_val, verbose=0)
print("\nValidation Results:")
print(f"Accuracy: {val_acc:.4f}")
print(f"Precision: {val_precision:.4f}")
print(f"Recall: {val_recall:.4f}")
print(f"AUC: {val_auc:.4f}")

print("\nDeep Learning model FIXED! Now re-run Week 3 evaluation.")
