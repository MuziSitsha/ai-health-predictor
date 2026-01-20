#!/bin/bash
# Create models directory
mkdir -p models

# Check if models exist
echo "Checking for model files..."
if [ ! -f "models/random_forest.pkl" ]; then
    echo "Warning: random_forest.pkl not found in models directory."
    echo "Please train your model and place it in the models/ directory."
fi

if [ ! -f "models/scaler_retrained.pkl" ]; then
    echo "Warning: scaler_retrained.pkl not found in models directory."
fi
