import pandas as pd
import numpy as np
import os

def load_and_clean_data():
    """Load diabetes data, clean zeros as missing values."""
    print("Loading and cleaning diabetes dataset...")
    
    # Load data
    df = pd.read_csv('data/diabetes.csv')
    print(f"Original shape: {df.shape}")
    
    # Create a copy for cleaning
    df_clean = df.copy()
    
    print("\n1. Handling zeros as missing values:")
    print("-" * 40)
    
    # Replace impossible zeros with NaN
    impossible_zero_cols = ['Glucose', 'BloodPressure', 'BMI']
    for col in impossible_zero_cols:
        zero_count = (df_clean[col] == 0).sum()
        if zero_count > 0:
            df_clean[col] = df_clean[col].replace(0, np.nan)
            print(f"  {col}: Replaced {zero_count} zeros with NaN")
    
    # For SkinThickness, replace zeros with NaN
    zero_count = (df_clean['SkinThickness'] == 0).sum()
    if zero_count > 0:
        df_clean['SkinThickness'] = df_clean['SkinThickness'].replace(0, np.nan)
        print(f"  SkinThickness: Replaced {zero_count} zeros with NaN")
    
    # Insulin zeros might be valid (type 1 diabetes)
    insulin_zeros = (df_clean['Insulin'] == 0).sum()
    print(f"  Insulin: Kept {insulin_zeros} zeros (may be valid)")
    
    print("\n2. Imputing missing values:")
    print("-" * 40)
    
    # Impute with median grouped by Outcome
    missing_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'BMI']
    
    for col in missing_cols:
        if df_clean[col].isnull().any():
            # Calculate median for each outcome group (using non-NaN values)
            median_by_outcome = df_clean.groupby('Outcome')[col].median()
            
            # Impute values based on outcome
            for outcome in [0, 1]:
                mask = (df_clean[col].isnull()) & (df_clean['Outcome'] == outcome)
                df_clean.loc[mask, col] = median_by_outcome[outcome]
            
            imputed_count = df_clean[col].isnull().sum()
            print(f"  {col}: Imputed with median by Outcome group")
    
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
    
    # Show summary of imputed values
    print("\nSummary of cleaned data:")
    print(f"Total samples: {len(cleaned_df)}")
    print(f"Diabetic (1): {sum(cleaned_df['Outcome'] == 1)}")
    print(f"Non-diabetic (0): {sum(cleaned_df['Outcome'] == 0)}")
