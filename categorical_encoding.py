import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder
from sklearn.feature_extraction import FeatureHasher

# Create sample dataset with different types of categorical variables
np.random.seed(42)
data = {
    'employee_id': range(1, 11),
    'education': ['High School', 'Bachelor', 'Master', 'PhD', 'Bachelor', 
                 'High School', 'Master', 'PhD', 'Bachelor', 'Master'],
    'department': ['IT', 'HR', 'Finance', 'IT', 'Marketing', 
                  'HR', 'Finance', 'IT', 'Marketing', 'HR'],
    'city': ['NYC', 'LA', 'Chicago', 'NYC', 'Houston', 
            'LA', 'Chicago', 'NYC', 'Houston', 'LA'],
    'performance': ['Poor', 'Average', 'Good', 'Excellent', 'Good',
                   'Average', 'Excellent', 'Good', 'Average', 'Excellent'],
    'salary': [45000, 55000, 75000, 85000, 62000, 48000, 78000, 80000, 58000, 72000]
}

df = pd.DataFrame(data)

print("=== ENCODING CATEGORICAL VARIABLES ===")
print("\n1. ORIGINAL DATASET")
print("-" * 40)
print(df)

print(f"\nCategorical columns and their unique values:")
categorical_cols = df.select_dtypes(include=['object']).columns
for col in categorical_cols:
    print(f"{col}: {df[col].unique()}")

# METHOD 1: LABEL ENCODING
print("\n2. METHOD 1: LABEL ENCODING")
print("-" * 40)

df_label = df.copy()

# Label encoding for ordinal data (education has natural order)
print("Label Encoding for ORDINAL data (Education):")
le_education = LabelEncoder()
df_label['education_encoded'] = le_education.fit_transform(df_label['education'])

# Show the mapping
education_mapping = dict(zip(le_education.classes_, le_education.transform(le_education.classes_)))
print(f"Education mapping: {education_mapping}")
print(df_label[['education', 'education_encoded']].drop_duplicates().sort_values('education_encoded'))

# Label encoding for performance (also ordinal)
print(f"\nLabel Encoding for ORDINAL data (Performance):")
le_performance = LabelEncoder()
df_label['performance_encoded'] = le_performance.fit_transform(df_label['performance'])

performance_mapping = dict(zip(le_performance.classes_, le_performance.transform(le_performance.classes_)))
print(f"Performance mapping: {performance_mapping}")
print(df_label[['performance', 'performance_encoded']].drop_duplicates().sort_values('performance_encoded'))

print(f"\nWarning: Label encoding department and city creates artificial ordering!")
# This is just for demonstration - don't do this for nominal data!
le_dept = LabelEncoder()
df_label['department_encoded'] = le_dept.fit_transform(df_label['department'])
print(f"Department mapping: {dict(zip(le_dept.classes_, le_dept.transform(le_dept.classes_)))}")

# METHOD 2: ORDINAL ENCODING (BETTER FOR ORDINAL DATA)
print("\n3. METHOD 2: ORDINAL ENCODING")
print("-" * 40)

df_ordinal = df.copy()

# Define proper order for ordinal variables
education_order = ['High School', 'Bachelor', 'Master', 'PhD']
performance_order = ['Poor', 'Average', 'Good', 'Excellent']

ordinal_encoder = OrdinalEncoder(categories=[education_order, performance_order])
df_ordinal[['education_ordinal', 'performance_ordinal']] = ordinal_encoder.fit_transform(
    df_ordinal[['education', 'performance']])

print("Ordinal Encoding with proper ordering:")
print("Education order:", education_order)
print("Performance order:", performance_order)
print(df_ordinal[['education', 'education_ordinal', 'performance', 'performance_ordinal']].drop_duplicates())

# METHOD 3: ONE-HOT ENCODING
print("\n4. METHOD 3: ONE-HOT ENCODING")
print("-" * 40)

df_onehot = df.copy()

# One-hot encoding for nominal data (department and city)
print("One-Hot Encoding for NOMINAL data:")

# Using pandas get_dummies
dept_dummies = pd.get_dummies(df_onehot['department'], prefix='dept')
city_dummies = pd.get_dummies(df_onehot['city'], prefix='city')

print(f"\nDepartment one-hot encoded columns:")
print(dept_dummies.columns.tolist())
print(dept_dummies.head())

print(f"\nCity one-hot encoded columns:")
print(city_dummies.columns.tolist())
print(city_dummies.head())

# Combine with original dataframe
df_onehot = pd.concat([df_onehot, dept_dummies, city_dummies], axis=1)
print(f"\nDataset shape after one-hot encoding: {df_onehot.shape}")

# METHOD 4: SKLEARN ONE-HOT ENCODER
print("\n5. METHOD 4: SKLEARN ONE-HOT ENCODER")
print("-" * 40)

from sklearn.preprocessing import OneHotEncoder

df_sklearn_oh = df.copy()

# Using sklearn OneHotEncoder
oh_encoder = OneHotEncoder(sparse_output=False, drop='first')  # drop='first' to avoid dummy variable trap
encoded_features = oh_encoder.fit_transform(df_sklearn_oh[['department', 'city']])

# Get feature names
feature_names = oh_encoder.get_feature_names_out(['department', 'city'])
print(f"Feature names: {feature_names}")

# Create DataFrame with encoded features
encoded_df = pd.DataFrame(encoded_features, columns=feature_names)
print(encoded_df)

# METHOD 5: TARGET ENCODING (MEAN ENCODING)
print("\n6. METHOD 5: TARGET ENCODING")
print("-" * 40)

df_target = df.copy()

print("Target Encoding using salary as target:")

# Calculate mean salary for each department
dept_salary_mean = df_target.groupby('department')['salary'].mean()
print(f"\nMean salary by department:")
print(dept_salary_mean)

# Replace department with mean salary
df_target['department_target_encoded'] = df_target['department'].map(dept_salary_mean)

# Same for city
city_salary_mean = df_target.groupby('city')['salary'].