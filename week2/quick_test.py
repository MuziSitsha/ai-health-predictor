"""
Quick test to verify Week 2 setup
"""

import sys

def test_imports():
    """Test if all required imports work"""
    print("Testing imports...")
    
    imports_to_test = [
        ('pandas', 'pd'),
        ('numpy', 'np'),
        ('sklearn.model_selection', 'train_test_split'),
        ('sklearn.preprocessing', 'StandardScaler'),
        ('sklearn.linear_model', 'LogisticRegression'),
        ('sklearn.ensemble', 'RandomForestClassifier'),
        ('sklearn.metrics', 'accuracy_score')
    ]
    
    for module, alias in imports_to_test:
        try:
            exec(f"import {module} as {alias}")
            print(f"✓ {module}")
        except ImportError as e:
            print(f"✗ {module}: {e}")
            return False
    
    return True

def test_directories():
    """Test if directories exist"""
    print("\nTesting directories...")
    
    import os
    directories = ['week2', 'week2/models', 'week2/reports']
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"✓ {directory}/")
        else:
            print(f"✗ {directory}/ (creating...)")
            os.makedirs(directory, exist_ok=True)
    
    return True

def main():
    """Main test function"""
    print("="*50)
    print("WEEK 2 SETUP TEST")
    print("="*50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import test failed!")
        print("Install missing packages with: pip install pandas numpy scikit-learn matplotlib seaborn")
        sys.exit(1)
    
    # Test directories
    test_directories()
    
    print("\n" + "="*50)
    print("✅ SETUP TEST PASSED!")
    print("="*50)
    print("\nYou're ready to start Week 2!")
    print("\nTo begin:")
    print("1. Run the notebook: week2/week2_model_development.ipynb")
    print("2. Or run: python week2/run_week2.py for setup instructions")
    print("\nGood luck with your project!")

if __name__ == "__main__":
    main()
