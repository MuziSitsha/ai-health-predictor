import pandas as pd
import numpy as np
import os

print("=" * 70)
print("WEEK 1: DATA PREPARATION - FINAL STEP")
print("=" * 70)

# 1. Load and clean data
print("\n1. Loading and cleaning data...")
df = pd.read_csv('data/diabetes.csv')

# Clean zeros as NaN
for col in ['Glucose', 'BloodPressure', 'BMI', 'SkinThickness']:
    df[col] = df[col].replace(0, np.nan)

# Impute with median by Outcome
for col in ['Glucose', 'BloodPressure', 'BMI', 'SkinThickness']:
    if df[col].isnull().any():
        median_by_outcome = df.groupby('Outcome')[col].median()
        for outcome in [0, 1]:
            mask = (df[col].isnull()) & (df['Outcome'] == outcome)
            df.loc[mask, col] = median_by_outcome[outcome]

# 2. Save cleaned data
print("\n2. Saving cleaned data...")
os.makedirs('data/processed', exist_ok=True)
df.to_csv('data/processed/diabetes_cleaned.csv', index=False)
print(f"  Saved: data/processed/diabetes_cleaned.csv")

# 3. Create basic splits (without scikit-learn for now)
print("\n3. Creating train/validation/test splits...")

# Simple random split (70/15/15)
np.random.seed(42)
indices = np.arange(len(df))
np.random.shuffle(indices)

train_size = int(0.7 * len(df))
val_size = int(0.15 * len(df))

train_idx = indices[:train_size]
val_idx = indices[train_size:train_size + val_size]
test_idx = indices[train_size + val_size:]

train_df = df.iloc[train_idx]
val_df = df.iloc[val_idx]
test_df = df.iloc[test_idx]

# Save splits
train_df.to_csv('data/processed/train.csv', index=False)
val_df.to_csv('data/processed/validation.csv', index=False)
test_df.to_csv('data/processed/test.csv', index=False)

print(f"  Train set: {len(train_df)} samples ({len(train_df)/len(df)*100:.1f}%)")
print(f"  Validation set: {len(val_df)} samples ({len(val_df)/len(df)*100:.1f}%)")
print(f"  Test set: {len(test_df)} samples ({len(test_df)/len(df)*100:.1f}%)")

# 4. Create summary
print("\n4. Creating summary report...")
summary = f"""WEEK 1 COMPLETION SUMMARY
{"=" * 50}

DATASET: Pima Indians Diabetes
- Total samples: {len(df)}
- Features: {len(df.columns) - 1} (8 medical + 1 target)
- Target distribution:
  * No Diabetes (0): {sum(df['Outcome'] == 0)} ({sum(df['Outcome'] == 0)/len(df)*100:.1f}%)
  * Diabetes (1): {sum(df['Outcome'] == 1)} ({sum(df['Outcome'] == 1)/len(df)*100:.1f}%)

DATA CLEANING:
- Replaced zeros with NaN for: Glucose, BloodPressure, BMI, SkinThickness
- Imputed missing values using median by Outcome group
- Kept Insulin zeros (may be valid for type 1 diabetes)

DATA SPLITS:
- Training: {len(train_df)} samples ({len(train_df)/len(df)*100:.1f}%)
- Validation: {len(val_df)} samples ({len(val_df)/len(df)*100:.1f}%)
- Test: {len(test_df)} samples ({len(test_df)/len(df)*100:.1f}%)

FILES CREATED:
- data/processed/diabetes_cleaned.csv (complete cleaned dataset)
- data/processed/train.csv (training set)
- data/processed/validation.csv (validation set)
- data/processed/test.csv (test set)

NEXT STEPS (Week 2):
- Build machine learning models
- Train on training set
- Validate on validation set
- Test on test set
"""

with open('week1_completion_summary.txt', 'w') as f:
    f.write(summary)

print("  Saved: week1_completion_summary.txt")

print("\n" + "=" * 70)
print("WEEK 1 COMPLETED SUCCESSFULLY! ✅")
print("=" * 70)
print("\nYou are now ready for Week 2: Model Development")
print("Your cleaned data is in: data/processed/")
