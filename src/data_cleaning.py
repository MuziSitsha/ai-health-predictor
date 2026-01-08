import pandas as pd
import numpy as np
import os

def load_and_clean_data():
    """Load diabetes data and clean zeros as missing values."""
    print("Loading and cleaning diabetes dataset...")
    
    # Load data
    df = pd.read_csv('data/diabetes.csv')
    print(f"Original shape: {df.shape}")
    
    # Create a copy for cleaning
    df_clean = df.copy()
    
    # Columns where zero indicates missing data
    # These are medically impossible to be zero
    impossible_zero_cols = ['Glucose', 'BloodPressure', 'BMI']
    
    # Columns where zero might be missing or actual zero
    possible_zero_cols = ['SkinThickness', 'Insulin']
    
    print("\n1. Handling zeros as missing values:")
    print("-" * 40)
    
    # Replace impossible zeros with NaN
    for col in impossible_zero_cols:
        zero_count = (df_clean[col] == 0).sum()
        if zero_count > 0:
            df_clean[col] = df_clean[col].replace(0, np.nan)
            print(f"  {col}: Replaced {zero_count} zeros with NaN")
    
    # For SkinThickness, also replace zeros with NaN (likely missing)
    zero_count = (df_clean['SkinThickness'] == 0).sum()
    if zero_count > 0:
        df_clean['SkinThickness'] = df_clean['SkinThickness'].replace(0, np.nan)
        print(f"  SkinThickness: Replaced {zero_count} zeros with NaN")
    
    # Insulin zeros might be valid (type 1 diabetes), so we keep them
    insulin_zeros = (df_clean['Insulin'] == 0).sum()
    print(f"  Insulin: Kept {insulin_zeros} zeros (may be valid)")
    
    print("\n2. Missing values after cleaning:")
    print("-" * 40)
    missing_counts = df_clean.isnull().sum()
    for col in df_clean.columns:
        if missing_counts[col] > 0:
            percentage = (missing_counts[col] / len(df_clean)) * 100
            print(f"  {col}: {missing_counts[col]} missing ({percentage:.1f}%)")
    
    print("\n3. Saving cleaned data...")
    os.makedirs('data/processed', exist_ok=True)
    df_clean.to_csv('data/processed/diabetes_cleaned.csv', index=False)
    print(f"  Saved to: data/processed/diabetes_cleaned.csv")
    
    return df_clean

if __name__ == "__main__":
    cleaned_df = load_and_clean_data()
    print(f"\nCleaned dataset shape: {cleaned_df.shape}")
    print("\nFirst 5 rows of cleaned data:")
    print(cleaned_df.head())
