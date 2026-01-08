import pandas as pd
import numpy as np

print("Testing data analysis...")
df = pd.read_csv('data/diabetes.csv')

print(f"\\nDataset shape: {df.shape}")
print(f"\\nColumns: {list(df.columns)}")

print("\\nMissing values per column:")
print(df.isnull().sum())

print("\\nData types:")
print(df.dtypes)

print("\\nStatistical summary:")
print(df.describe())

print("\\nTarget variable distribution:")
print(df['Outcome'].value_counts())
print("\\nPercentage:")
print(df['Outcome'].value_counts(normalize=True) * 100)
