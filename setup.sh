#!/bin/bash
# Setup script for Streamlit Cloud

# Create models directory
mkdir -p models

# Install dependencies
pip install -r requirements.txt

echo "Setup complete!"
