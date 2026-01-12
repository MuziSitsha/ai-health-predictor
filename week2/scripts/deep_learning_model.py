import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import joblib
import matplotlib.pyplot as plt
import os

def create_advanced_dl_model(input_shape, name="health_predictor_dl"):
    model = models.Sequential(name=name)
    
    # Input layer
    model.add(layers.Input(shape=(input_shape,)))
    
    # Hidden layers
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.Dropout(0.3))
    
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.Dropout(0.3))
    
    model.add(layers.Dense(32, activation='relu'))
    
    # Output layer
    model.add(layers.Dense(1, activation='sigmoid'))
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy', 
                 keras.metrics.Precision(name='precision'),
                 keras.metrics.Recall(name='recall'),
                 keras.metrics.AUC(name='auc')]
    )
    
    return model

def train_and_evaluate_model():
    print("Loading data...")
    
    try:
        # Try to load Week 1 data
        df = pd.read_csv('data/processed/cleaned_health_data.csv')
        print(f"Success: Loaded data with shape {df.shape}")
    except FileNotFoundError:
        print("Week 1 data not found. Creating sample data...")
        # Create sample data
        np.random.seed(42)
        n_samples = 1000
        
        df = pd.DataFrame({
            'age': np.random.randint(20, 80, n_samples),
            'bmi': np.random.uniform(18.5, 40, n_samples),
            'glucose': np.random.uniform(70, 200, n_samples),
            'blood_pressure': np.random.uniform(80, 180, n_samples),
            'cholesterol': np.random.uniform(150, 300, n_samples),
            'target': np.random.randint(0, 2, n_samples)
        })
        print(f"Created sample data with shape {df.shape}")
    
    # Prepare features and target
    if 'target' in df.columns:
        target_col = 'target'
    else:
        target_col = df.columns[-1]
    
    X = df.drop(columns=[target_col]).values
    y = df[target_col].values
    
    print(f"Dataset shape: {X.shape}")
    print(f"Target distribution: Positive: {y.sum()}, Negative: {len(y)-y.sum()}")
    
    # Split data
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
    )
    
    print(f"Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")
    
    # Create model
    model = create_advanced_dl_model(X_train.shape[1])
    model.summary()
    
    # Callbacks
    callbacks = [
        keras.callbacks.EarlyStopping(
            patience=10, 
            restore_best_weights=True,
            monitor='val_auc'
        ),
        keras.callbacks.ReduceLROnPlateau(
            factor=0.5, 
            patience=5, 
            min_lr=1e-6
        )
    ]
    
    # Train model
    print("\nTraining model...")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=50,
        batch_size=32,
        callbacks=callbacks,
        verbose=1
    )
    
    # Evaluate on test set
    test_results = model.evaluate(X_test, y_test, verbose=0)
    
    print("\n" + "="*50)
    print("DEEP LEARNING MODEL - TEST RESULTS")
    print("="*50)
    print(f"Loss: {test_results[0]:.4f}")
    print(f"Accuracy: {test_results[1]:.4f}")
    print(f"Precision: {test_results[2]:.4f}")
    print(f"Recall: {test_results[3]:.4f}")
    print(f"AUC: {test_results[4]:.4f}")
    
    # Save model
    os.makedirs('week2/models', exist_ok=True)
    model.save('week2/models/deep_learning_model.h5')
    print("\nModel saved as 'week2/models/deep_learning_model.h5'")
    
    # Plot training history
    plot_training_history(history)
    
    return model, history, test_results

def plot_training_history(history):
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    metrics = ['loss', 'accuracy', 'precision', 'recall']
    titles = ['Loss', 'Accuracy', 'Precision', 'Recall']
    
    for idx, (metric, title) in enumerate(zip(metrics, titles)):
        ax = axes[idx//2, idx%2]
        ax.plot(history.history[metric], label=f'Training {title}')
        ax.plot(history.history[f'val_{metric}'], label=f'Validation {title}')
        ax.set_title(f'{title} over Epochs')
        ax.set_xlabel('Epochs')
        ax.set_ylabel(title)
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('week2/models/training_history.png', dpi=150)
    print("Training history plot saved as 'week2/models/training_history.png'")
    plt.show()

if __name__ == "__main__":
    print("Training Advanced Deep Learning Model for Health Prediction...")
    model, history, results = train_and_evaluate_model()
