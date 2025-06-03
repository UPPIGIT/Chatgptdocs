import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer

# Create dataset with missing values
np.random.seed(42)
data = {
    'age': [25, 30, np.nan, 40, 45, 28, np.nan, 33, 29, 35],
    'salary': [50000, np.nan, 75000, 80000, np.nan, 55000, 90000, 65000, 58000, 72000],
    'experience': [2, 5, 8, np.nan, 15, 3, 18, 6, 4, 9],
    'department': ['IT', 'HR', np.nan, 'Finance', 'HR', 'IT', 'Finance', np.nan, 'IT', 'HR'],
    'city': ['NYC', 'LA', 'Chicago', 'NYC', np.nan, 'LA', 'Chicago', 'NYC', 'LA', 'Chicago']
}

df = pd.DataFrame(data)

print("=== HANDLING MISSING VALUES ===")
print("\n1. ORIGINAL DATASET WITH MISSING VALUES")
print("-" * 40)
print(df)
print(f"\nMissing values per column:")
print(df.isnull().sum())

# METHOD 1: REMOVE ROWS/COLUMNS WITH MISSING VALUES
print("\n2. METHOD 1: REMOVAL")
print("-" * 40)

# Remove rows with any missing values
df_drop_rows = df.dropna()
print(f"After dropping rows with missing values:")
print(f"Original shape: {df.shape}")
print(f"New shape: {df_drop_rows.shape}")
print(f"Rows removed: {df.shape[0] - df_drop_rows.shape[0]}")

# Remove columns with missing values
df_drop_cols = df.dropna(axis=1)
print(f"\nAfter dropping columns with missing values:")
print(f"Original columns: {df.shape[1]}")
print(f"New columns: {df_drop_cols.shape[1]}")
print(f"Remaining columns: {list(df_drop_cols.columns)}")

# METHOD 2: SIMPLE IMPUTATION
print("\n3. METHOD 2: SIMPLE IMPUTATION")
print("-" * 40)

df_simple = df.copy()

# For numerical columns - Mean imputation
print("Numerical columns - Mean imputation:")
numerical_cols = ['age', 'salary', 'experience']
for col in numerical_cols:
    mean_value = df_simple[col].mean()
    df_simple[col].fillna(mean_value, inplace=True)
    print(f"  {col}: filled {df[col].isnull().sum()} missing values with mean = {mean_value:.2f}")

# For categorical columns - Mode imputation
print("\nCategorical columns - Mode imputation:")
categorical_cols = ['department', 'city']
for col in categorical_cols:
    mode_value = df_simple[col].mode()[0]  # mode() returns a Series, take first value
    df_simple[col].fillna(mode_value, inplace=True)
    print(f"  {col}: filled {df[col].isnull().sum()} missing values with mode = '{mode_value}'")

print(f"\nAfter simple imputation:")
print(df_simple)
print(f"Missing values: {df_simple.isnull().sum().sum()}")

# METHOD 3: USING SKLEARN SIMPLEIMPUTER
print("\n4. METHOD 3: SKLEARN SIMPLEIMPUTER")
print("-" * 40)

df_sklearn = df.copy()

# Numerical columns
num_imputer = SimpleImputer(strategy='mean')  # Can also use 'median', 'most_frequent'
df_sklearn[numerical_cols] = num_imputer.fit_transform(df_sklearn[numerical_cols])

# Categorical columns
cat_imputer = SimpleImputer(strategy='most_frequent')
df_sklearn[categorical_cols] = cat_imputer.fit_transform(df_sklearn[categorical_cols])

print("After sklearn SimpleImputer:")
print(df_sklearn)

# METHOD 4: KNN IMPUTATION
print("\n5. METHOD 4: KNN IMPUTATION")
print("-" * 40)

# KNN works only with numerical data, so let's encode categorical first
df_knn = df.copy()

# Encode categorical variables for KNN
from sklearn.preprocessing import LabelEncoder
le_dept = LabelEncoder()
le_city = LabelEncoder()

# Handle missing values in categorical columns first
df_knn['department'].fillna('Unknown', inplace=True)
df_knn['city'].fillna('Unknown', inplace=True)

# Now encode
df_knn['department_encoded'] = le_dept.fit_transform(df_knn['department'])
df_knn['city_encoded'] = le_city.fit_transform(df_knn['city'])

# Apply KNN imputation to numerical columns
knn_imputer = KNNImputer(n_neighbors=3)
columns_for_knn = ['age', 'salary', 'experience', 'department_encoded', 'city_encoded']
df_knn[columns_for_knn] = knn_imputer.fit_transform(df_knn[columns_for_knn])

print("After KNN imputation (showing only numerical columns):")
print(df_knn[['age', 'salary', 'experience']])

# METHOD 5: FORWARD/BACKWARD FILL
print("\n6. METHOD 5: FORWARD/BACKWARD FILL")
print("-" * 40)

df_fill = df.copy()

# Forward fill - use previous valid value
print("Forward fill example:")
df_ffill = df_fill.fillna(method='ffill')
print(df_ffill[['age', 'salary']])

# Backward fill - use next valid value
print("\nBackward fill example:")
df_bfill = df_fill.fillna(method='bfill')
print(df_bfill[['age', 'salary']])

# METHOD 6: CUSTOM IMPUTATION
print("\n7. METHOD 6: CUSTOM IMPUTATION")
print("-" * 40)

df_custom = df.copy()

# Custom logic: Fill salary based on experience
print("Custom imputation - Salary based on experience:")
# Create a simple rule: salary = 45000 + (experience * 2500)
def estimate_salary(row):
    if pd.isna(row['salary']) and not pd.isna(row['experience']):
        return 45000 + (row['experience'] * 2500)
    return row['salary']

df_custom['salary'] = df_custom.apply(estimate_salary, axis=1)
print(df_custom[['salary', 'experience']])

# COMPARISON OF METHODS
print("\n8. COMPARISON OF METHODS")
print("-" * 40)
print("Method Comparison:")
print(f"1. Drop rows:     {df_drop_rows.shape[0]} rows remaining")
print(f"2. Drop columns:  {df_drop_cols.shape[1]} columns remaining")
print(f"3. Simple impute: {df_simple.isnull().sum().sum()} missing values")
print(f"4. Sklearn impute:{df_sklearn.isnull().sum().sum()} missing values")
print(f"5. KNN impute:    {df_knn[numerical_cols].isnull().sum().sum()} missing values")
print(f"6. Custom impute: {df_custom.isnull().sum().sum()} missing values")

print("\n=== WHEN TO USE EACH METHOD ===")
print("• Drop rows: When you have plenty of data and few missing values")
print("• Drop columns: When a column has too many missing values (>50%)")
print("• Mean/Mode: Simple, fast, works well for normally distributed data")
print("• Median: Better than mean when data has outliers")
print("• KNN: When you want to use relationships between features")
print("• Forward/Backward fill: For time series data")
print("• Custom: When you have domain knowledge about the data")