"""
Week 2 Model Development Runner - Fixed version
"""

import os
import sys

def check_environment():
    """Check Python environment and packages"""
    print("="*60)
    print("WEEK 2: AI HEALTH PREDICTOR - MODEL DEVELOPMENT")
    print("="*60)
    
    print("\nChecking Python environment...")
    print(f"Python version: {sys.version}")
    
    # Check essential packages - using the correct import names
    required_packages = {
        'pandas': 'Data manipulation',
        'numpy': 'Numerical computations',
        'sklearn': 'Machine learning',  # Changed from scikit-learn to sklearn
        'matplotlib': 'Data visualization',
        'seaborn': 'Statistical visualization'
    }
    
    print("\nChecking required packages...")
    missing = []
    for package, description in required_packages.items():
        try:
            __import__(package)
            print(f"✓ {package}: {description}")
        except ImportError:
            print(f"✗ {package}: MISSING - {description}")
            missing.append(package)
    
    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("Install them using:")
        print(f"pip install {' '.join(missing)}")
        return False
    
    return True

def setup_directories():
    """Create necessary directories"""
    print("\nSetting up directories...")
    
    directories = [
        'week2/models',
        'week2/reports',
        'week2/data'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  Created: {directory}/")
    
    return True

def check_data():
    """Check if data is available"""
    print("\nChecking for data files...")
    
    import os
    csv_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.csv'):
                csv_files.append(os.path.join(root, file))
    
    if csv_files:
        print(f"Found {len(csv_files)} CSV files:")
        for file in csv_files[:5]:  # Show first 5
            print(f"  - {file}")
        if len(csv_files) > 5:
            print(f"  ... and {len(csv_files) - 5} more")
        return True
    else:
        print("No CSV files found.")
        print("The notebook will create sample diabetes data.")
        return True

def main():
    """Main function"""
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Setup directories
    setup_directories()
    
    # Check data
    check_data()
    
    # Instructions
    print("\n" + "="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    print("\nTo start Week 2:")
    print("\nOPTION 1: Run Jupyter Notebook (Recommended)")
    print("  jupyter notebook week2/week2_model_development.ipynb")
    print("\nOPTION 2: If you don't have Jupyter installed:")
    print("  pip install notebook")
    print("  Then run: jupyter notebook")
    print("\nOPTION 3: Run as Python script (simplified)")
    print("  python week2/run_simple_models.py")
    print("\nThe notebook includes:")
    print("  1. Data loading and exploration")
    print("  2. Data preparation")
    print("  3. Training 4 baseline models")
    print("  4. Model evaluation and comparison")
    print("  5. Saving models and reports")
    print("\nGood luck with your Week 2 project!")

if __name__ == "__main__":
    main()
