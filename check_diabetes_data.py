import pandas as pd
import numpy as np

print("Checking Diabetes Dataset Structure")
print("=" * 50)

# Load the main cleaned dataset
df = pd.read_csv('data/processed/diabetes_cleaned.csv')
print(f"Dataset: diabetes_cleaned.csv")
print(f"Shape: {df.shape} (Rows: {df.shape[0]}, Columns: {df.shape[1]})")
print(f"Columns: {list(df.columns)}")
print(f"Data types:\n{df.dtypes}")
print(f"\nFirst 3 rows:")
print(df.head(3))

# Check the target column (usually last column or named 'Outcome')
target_col = None
if 'Outcome' in df.columns:
    target_col = 'Outcome'
elif df.columns[-1] in ['target', 'class', 'diabetes']:
    target_col = df.columns[-1]
else:
    # Assume last column is target
    target_col = df.columns[-1]

print(f"\nTarget column identified as: '{target_col}'")
print(f"Target value distribution:")
print(df[target_col].value_counts())
print(f"Percentage positive: {(df[target_col].sum()/len(df))*100:.1f}%")

# Also check the split datasets
print("\n" + "=" * 50)
print("Checking train/test/validation splits:")
for split_name in ['train', 'test', 'validation']:
    try:
        split_df = pd.read_csv(f'data/processed/{split_name}.csv')
        print(f"{split_name}.csv: {split_df.shape}, Target distribution: {split_df[target_col].value_counts().to_dict()}")
    except:
        print(f"{split_name}.csv: Not found or error loading")

print("\n" + "=" * 50)
print("DATA CHECK COMPLETE")
