import pandas as pd
import os

def download_diabetes_data():
    """Download Pima Indians Diabetes dataset."""
    print("Downloading diabetes dataset...")
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Dataset URL
    url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.csv'
    
    # Column names
    columns = [
        'Pregnancies',
        'Glucose',
        'BloodPressure',
        'SkinThickness',
        'Insulin',
        'BMI',
        'DiabetesPedigreeFunction',
        'Age',
        'Outcome'  # 0 = No Diabetes, 1 = Diabetes
    ]
    
    try:
        # Download dataset
        df = pd.read_csv(url, header=None, names=columns)
        
        # Save to CSV
        df.to_csv('data/diabetes.csv', index=False)
        
        print("Dataset downloaded successfully!")
        print(f"Shape: {df.shape}")
        print(f"Saved to: data/diabetes.csv")
        print("\nFirst 5 rows:")
        print(df.head())
        
        return df
        
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        return None

if __name__ == "__main__":
    download_diabetes_data()
