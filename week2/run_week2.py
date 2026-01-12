"""
Week 2 Model Development Runner
"""

import os
import sys

def check_environment():
    """Check Python environment and packages"""
    print("="*60)
    print("WEEK 2: AI HEALTH PREDICTOR - MODEL DEVELOPMENT")
    print("="*60)
    
    print("\nChecking Python environment...")
    import sys
    print(f"Python version: {sys.version}")
    
    # Check essential packages
    required_packages = {
        'pandas': 'Data manipulation',
        'numpy': 'Numerical computations',
        'scikit-learn': 'Machine learning',
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
    
    csv_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.csv'):
                csv_files.append(os.path.join(root, file))
    
    if csv_files:
        print(f"Found {len(csv_files)} CSV files:")
        for file in csv_files[:3]:  # Show first 3
            print(f"  - {file}")
        if len(csv_files) > 3:
            print(f"  ... and {len(csv_files) - 3} more")
        return True
    else:
        print("No CSV files found.")
        print("The notebook will create sample data if needed.")
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
    print("\nNext Steps:")
    print("1. Open the Jupyter notebook:")
    print("   week2/week2_model_development.ipynb")
    print("\n2. Run the cells in order:")
    print("   - Data loading and exploration")
    print("   - Data preparation")
    print("   - Model training (4 baseline models)")
    print("   - Model evaluation and selection")
    print("   - Saving models and reports")
    print("\n3. Check the generated files:")
    print("   - week2/models/: Saved models")
    print("   - week2/reports/: Performance reports")
    print("\n4. For Week 3 (next week):")
    print("   - We'll build the Streamlit UI")
    print("   - Deploy the application")
    print("\nGood luck with your Week 2 project!")

if __name__ == "__main__":
    main()
