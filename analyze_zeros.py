import pandas as pd
import numpy as np

print("=" * 70)
print("ANALYSIS OF ZEROS IN MEDICAL COLUMNS")
print("=" * 70)

df = pd.read_csv('data/diabetes.csv')

# Medical columns where zero indicates missing data
medical_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']

print("\nCOUNT OF ZEROS IN MEDICAL COLUMNS:")
print("-" * 40)

for col in medical_cols:
    zero_count = (df[col] == 0).sum()
    total_count = len(df[col])
    percentage = (zero_count / total_count) * 100
    
    # Medical interpretation
    if col == 'Glucose':
        interpretation = "IMPOSSIBLE - Fasting glucose can't be 0"
    elif col == 'BloodPressure':
        interpretation = "IMPOSSIBLE - Blood pressure can't be 0"
    elif col == 'BMI':
        interpretation = "IMPOSSIBLE - BMI can't be 0"
    elif col == 'Insulin':
        interpretation = "Could be actual 0 or missing"
    else:
        interpretation = "Possibly missing"
    
    print(f"{col:20}: {zero_count:4} zeros ({percentage:5.1f}%) - {interpretation}")

print("\n" + "=" * 70)
print("DATA CLEANING STRATEGY")
print("=" * 70)
print("""
RECOMMENDED APPROACH:
1. Glucose, BloodPressure, BMI: Replace zeros with NaN (missing)
   - These CANNOT be physically zero
   
2. SkinThickness: Replace zeros with NaN or median
   - Skin thickness could be very thin but not zero
   
3. Insulin: Keep zeros as they might be valid (some people produce no insulin)
   - Or analyze further
   
4. Impute missing values with:
   - Median values
   - Or median grouped by Outcome
   
EXAMPLE IMPUTATION:
  Glucose missing → Median glucose for people with same Outcome
""")

# Show example of imputation
print("\nExample - Median values by Outcome:")
for col in medical_cols:
    if col != 'Insulin':  # Insulin might have valid zeros
        median_by_outcome = df[df[col] > 0].groupby('Outcome')[col].median()
        print(f"\n{col}:")
        print(f"  No Diabetes (0): {median_by_outcome.get(0, 'N/A'):.1f}")
        print(f"  Diabetes (1):    {median_by_outcome.get(1, 'N/A'):.1f}")
