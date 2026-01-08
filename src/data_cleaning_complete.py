import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_and_clean_data():
    """Load diabetes data, clean zeros as missing values, and impute."""
    print("=" * 70)
    print("COMPLETE DATA CLEANING PIPELINE")
    print("=" * 70)
    
    # Load data
    df = pd.read_csv('data/diabetes.csv')
    print(f"Original shape: {df.shape}")
    
    # Create a copy for cleaning
    df_clean = df.copy()
    
    print("\n1. HANDLING ZEROS AS MISSING VALUES:")
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
    
    print("\n2. IMPUTING MISSING VALUES:")
    print("-" * 40)
    
    # Columns with missing values after cleaning
    missing_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'BMI']
    
    # Impute with median grouped by Outcome
    for col in missing_cols:
        if df_clean[col].isnull().any():
            # Calculate median for each outcome group
            median_by_outcome = df_clean.groupby('Outcome')[col].median()
            
            # Impute values based on outcome
            for outcome in [0, 1]:
                mask = (df_clean[col].isnull()) & (df_clean['Outcome'] == outcome)
                df_clean.loc[mask, col] = median_by_outcome[outcome]
            
            imputed_count = df_clean[col].isnull().sum()
            print(f"  {col}: Imputed with median by Outcome group")
    
    print("\n3. FEATURE ENGINEERING:")
    print("-" * 40)
    
    # Create BMI categories
    def categorize_bmi(bmi):
        if bmi < 18.5:
            return 'Underweight'
        elif 18.5 <= bmi < 25:
            return 'Normal'
        elif 25 <= bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'
    
    df_clean['BMI_Category'] = df_clean['BMI'].apply(categorize_bmi)
    
    # Create age groups
    def categorize_age(age):
        if age < 30:
            return 'Young'
        elif 30 <= age < 50:
            return 'Middle-aged'
        else:
            return 'Senior'
    
    df_clean['Age_Group'] = df_clean['Age'].apply(categorize_age)
    
    # Create glucose status
    def categorize_glucose(glucose):
        if glucose < 100:
            return 'Normal'
        elif 100 <= glucose < 126:
            return 'Prediabetic'
        else:
            return 'Diabetic'
    
    df_clean['Glucose_Status'] = df_clean['Glucose'].apply(categorize_glucose)
    
    print("  Created new features:")
    print("    - BMI_Category (Underweight/Normal/Overweight/Obese)")
    print("    - Age_Group (Young/Middle-aged/Senior)")
    print("    - Glucose_Status (Normal/Prediabetic/Diabetic)")
    
    print("\n4. ENCODING CATEGORICAL FEATURES:")
    print("-" * 40)
    
    # One-hot encode categorical features
    categorical_cols = ['BMI_Category', 'Age_Group', 'Glucose_Status']
    df_encoded = pd.get_dummies(df_clean, columns=categorical_cols, drop_first=True)
    
    print(f"  Original columns: {len(df_clean.columns)}")
    print(f"  After encoding: {len(df_encoded.columns)} columns")
    
    print("\n5. DATA SPLITTING:")
    print("-" * 40)
    
    # Separate features and target
    X = df_encoded.drop('Outcome', axis=1)
    y = df_encoded['Outcome']
    
    # Split into train (70%), validation (15%), test (15%)
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42, stratify=y
    )
    
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.1765, random_state=42, stratify=y_temp
    )
    
    print(f"  Training set:   {X_train.shape[0]} samples ({X_train.shape[0]/len(X)*100:.1f}%)")
    print(f"  Validation set: {X_val.shape[0]} samples ({X_val.shape[0]/len(X)*100:.1f}%)")
    print(f"  Validation set: {X_test.shape[0]} samples ({X_test.shape[0]/len(X)*100:.1f}%)")
    
    print("\n6. FEATURE SCALING:")
    print("-" * 40)
    
    # Original numerical features (before encoding)
    original_numerical = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
                         'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
    
    # Scale numerical features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train[original_numerical])
    X_val_scaled = scaler.transform(X_val[original_numerical])
    X_test_scaled = scaler.transform(X_test[original_numerical])
    
    # Convert back to DataFrames
    X_train_scaled_df = pd.DataFrame(X_train_scaled, 
                                     columns=[f'{col}_scaled' for col in original_numerical])
    X_val_scaled_df = pd.DataFrame(X_val_scaled, 
                                   columns=[f'{col}_scaled' for col in original_numerical])
    X_test_scaled_df = pd.DataFrame(X_test_scaled, 
                                    columns=[f'{col}_scaled' for col in original_numerical])
    
    # Combine scaled features with categorical features
    categorical_features = [col for col in X_train.columns if col not in original_numerical]
    
    X_train_final = pd.concat([X_train_scaled_df, 
                              X_train[categorical_features].reset_index(drop=True)], axis=1)
    X_val_final = pd.concat([X_val_scaled_df, 
                            X_val[categorical_features].reset_index(drop=True)], axis=1)
    X_test_final = pd.concat([X_test_scaled_df, 
                             X_test[categorical_features].reset_index(drop=True)], axis=1)
    
    print("  Scaled numerical features using StandardScaler")
    print(f"  Final feature count: {X_train_final.shape[1]}")
    
    print("\n7. SAVING PROCESSED DATA:")
    print("-" * 40)
    
    # Create directories
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    # Save processed data
    X_train_final.to_pickle('data/processed/X_train.pkl')
    X_val_final.to_pickle('data/processed/X_val.pkl')
    X_test_final.to_pickle('data/processed/X_test.pkl')
    
    y_train.to_pickle('data/processed/y_train.pkl')
    y_val.to_pickle('data/processed/y_val.pkl')
    y_test.to_pickle('data/processed/y_test.pkl')
    
    # Save scaler
    joblib.dump(scaler, 'models/scaler.pkl')
    
    # Save column names
    joblib.dump(list(X_train_final.columns), 'data/processed/feature_columns.pkl')
    joblib.dump(original_numerical, 'data/processed/original_numerical_columns.pkl')
    
    print("  Saved files:")
    print("    - data/processed/X_train.pkl, X_val.pkl, X_test.pkl")
    print("    - data/processed/y_train.pkl, y_val.pkl, y_test.pkl")
    print("    - models/scaler.pkl")
    print("    - data/processed/feature_columns.pkl")
    print("    - data/processed/original_numerical_columns.pkl")
    
    print("\n" + "=" * 70)
    print("DATA CLEANING PIPELINE COMPLETE!")
    print("=" * 70)
    
    # Display summary
    print(f"\nFinal dataset shapes:")
    print(f"  X_train: {X_train_final.shape}")
    print(f"  X_val:   {X_val_final.shape}")
    print(f"  X_test:  {X_test_final.shape}")
    print(f"  y_train: {y_train.shape}")
    print(f"  y_val:   {y_val.shape}")
    print(f"  y_test:  {y_test.shape}")
    
    return {
        'X_train': X_train_final, 'X_val': X_val_final, 'X_test': X_test_final,
        'y_train': y_train, 'y_val': y_val, 'y_test': y_test,
        'scaler': scaler
    }

if __name__ == "__main__":
    processed_data = load_and_clean_data()
