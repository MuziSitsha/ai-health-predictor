# DIABETES DATASET - DATA DICTIONARY

## Dataset: Pima Indians Diabetes Database
- **Source**: National Institute of Diabetes and Digestive and Kidney Diseases
- **Samples**: 768 female patients of Pima Indian heritage (21+ years old)
- **Purpose**: Predict diabetes onset based on diagnostic measurements

## COLUMNS:

### 1. Pregnancies
- **Type**: Integer
- **Description**: Number of times pregnant
- **Range**: 0-17
- **Notes**: Direct measurement

### 2. Glucose
- **Type**: Integer
- **Description**: Plasma glucose concentration (2 hours in oral glucose tolerance test)
- **Range**: 0-199 mg/dL
- **Medical Note**: Normal range: 70-140 mg/dL
- **Data Issue**: Zeros represent missing values (impossible physiologically)

### 3. BloodPressure
- **Type**: Integer  
- **Description**: Diastolic blood pressure (mm Hg)
- **Range**: 0-122 mm Hg
- **Medical Note**: Normal: 60-80 mm Hg, Hypertension: >90 mm Hg
- **Data Issue**: Zeros represent missing values (impossible physiologically)

### 4. SkinThickness
- **Type**: Integer
- **Description**: Triceps skin fold thickness (mm)
- **Range**: 0-99 mm
- **Data Issue**: Zeros likely represent missing values

### 5. Insulin
- **Type**: Integer
- **Description**: 2-Hour serum insulin (mu U/ml)
- **Range**: 0-846 mu U/ml
- **Note**: Some patients may have zero insulin (type 1 diabetes)

### 6. BMI
- **Type**: Float
- **Description**: Body mass index (weight in kg/(height in m)²)
- **Range**: 0-67.1
- **Medical Categories**:
  - Underweight: <18.5
  - Normal: 18.5-24.9  
  - Overweight: 25-29.9
  - Obese: ≥30
- **Data Issue**: Zeros represent missing values (impossible physiologically)

### 7. DiabetesPedigreeFunction
- **Type**: Float
- **Description**: Diabetes pedigree function (indicates genetic predisposition)
- **Range**: 0.078-2.42
- **Note**: Higher values indicate stronger family history of diabetes

### 8. Age
- **Type**: Integer
- **Description**: Age in years
- **Range**: 21-81 years

### 9. Outcome (TARGET VARIABLE)
- **Type**: Integer (Binary)
- **Description**: Diabetes diagnosis
- **Values**:
  - 0 = NO Diabetes (Negative class)
  - 1 = YES Diabetes (Positive class)
- **Distribution**: 
  - Class 0: 500 samples (65.1%)
  - Class 1: 268 samples (34.9%)

## DATA QUALITY ISSUES:

### Missing Values Represented as Zeros:
1. **Glucose**: 0 = Missing (physically impossible)
2. **BloodPressure**: 0 = Missing (physically impossible)
3. **BMI**: 0 = Missing (physically impossible)
4. **SkinThickness**: 0 = Possibly missing
5. **Insulin**: 0 = Could be valid or missing

### Recommended Handling:
1. Replace zeros with NaN for: Glucose, BloodPressure, BMI
2. Consider replacing zeros for: SkinThickness
3. Keep zeros for Insulin (may be valid for type 1 diabetes)
4. Impute missing values with median (or median by Outcome group)

## MEDICAL CONTEXT:
- Dataset focuses on Pima Indian population (high diabetes prevalence)
- All patients are females ≥21 years old
- Used for diabetes prediction research since 1990
- Common benchmark dataset in machine learning
