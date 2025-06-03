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
city_salary_mean = df_target.groupby('city')['salary'].mean()
print(f"\nMean salary by city:")
print(city_salary_mean)

df_target['city_target_encoded'] = df_target['city'].map(city_salary_mean)

print(f"\nTarget encoded values:")
print(df_target[['department', 'department_target_encoded', 'city', 'city_target_encoded', 'salary']])

# METHOD 6: BINARY ENCODING
print("\n7. METHOD 6: BINARY ENCODING")
print("-" * 40)

def binary_encode(series):
    """Simple binary encoding implementation"""
    # Get unique values and create mapping
    unique_vals = series.unique()
    n_bits = int(np.ceil(np.log2(len(unique_vals))))
    
    # Create binary mapping
    binary_mapping = {}
    for i, val in enumerate(unique_vals):
        binary_str = format(i, f'0{n_bits}b')
        binary_mapping[val] = [int(bit) for bit in binary_str]
    
    return binary_mapping

df_binary = df.copy()

# Binary encode department
dept_binary_map = binary_encode(df_binary['department'])
print(f"Department binary mapping:")
for dept, binary in dept_binary_map.items():
    print(f"  {dept}: {binary}")

# Create binary columns for department
n_bits_dept = len(list(dept_binary_map.values())[0])
for i in range(n_bits_dept):
    df_binary[f'dept_bit_{i}'] = df_binary['department'].map(
        lambda x: dept_binary_map[x][i])

print(f"\nBinary encoded department columns:")
print(df_binary[['department'] + [f'dept_bit_{i}' for i in range(n_bits_dept)]])

# METHOD 7: FREQUENCY ENCODING
print("\n8. METHOD 7: FREQUENCY ENCODING")
print("-" * 40)

df_freq = df.copy()

# Count frequency of each category
dept_counts = df_freq['department'].value_counts()
city_counts = df_freq['city'].value_counts()

print(f"Department frequencies:")
print(dept_counts)

print(f"\nCity frequencies:")
print(city_counts)

# Replace with frequencies
df_freq['department_freq_encoded'] = df_freq['department'].map(dept_counts)
df_freq['city_freq_encoded'] = df_freq['city'].map(city_counts)

print(f"\nFrequency encoded values:")
print(df_freq[['department', 'department_freq_encoded', 'city', 'city_freq_encoded']])

# METHOD 8: FEATURE HASHING
print("\n9. METHOD 8: FEATURE HASHING")
print("-" * 40)

# Feature hashing for high-cardinality categorical variables
hasher = FeatureHasher(n_features=8, input_type='string')

# Convert categories to list of strings
dept_list = [[dept] for dept in df['department']]
hashed_features = hasher.transform(dept_list).toarray()

print(f"Feature hashing for department (8 features):")
hashed_df = pd.DataFrame(hashed_features, columns=[f'hash_{i}' for i in range(8)])
print(hashed_df)

# COMPARISON OF METHODS
print("\n10. COMPARISON OF ENCODING METHODS")
print("-" * 50)

print("Method Comparison:")
print(f"Original dataset shape: {df.shape}")
print(f"Label encoding: adds {len(categorical_cols)} columns")
print(f"One-hot encoding: adds {len(dept_dummies.columns) + len(city_dummies.columns)} columns")
print(f"Target encoding: adds {2} columns (maintains same info)")
print(f"Binary encoding: adds {n_bits_dept} columns for department")
print(f"Frequency encoding: adds {2} columns")
print(f"Feature hashing: adds {8} columns (configurable)")

# Show final comparison table
comparison_data = {
    'Original': df['department'].iloc[:5].tolist(),
    'Label_Encoded': df_label['department_encoded'].iloc[:5].tolist(),
    'Target_Encoded': df_target['department_target_encoded'].iloc[:5].tolist(),
    'Freq_Encoded': df_freq['department_freq_encoded'].iloc[:5].tolist()
}

print(f"\nEncoding comparison for first 5 department values:")
comparison_df = pd.DataFrame(comparison_data)
print(comparison_df)

print("\n=== WHEN TO USE EACH METHOD ===")
print("📚 LABEL ENCODING:")
print("  ✓ Use for: Ordinal data with natural ordering (education levels, ratings)")
print("  ✗ Avoid for: Nominal data (creates artificial ordering)")

print("\n🔢 ORDINAL ENCODING:")
print("  ✓ Use for: Ordinal data when you want to specify custom ordering")
print("  ✓ Better than label encoding for controlling order")

print("\n🎯 ONE-HOT ENCODING:")
print("  ✓ Use for: Nominal data with low cardinality (<10-15 categories)")
print("  ✓ Most common method for nominal categorical variables")
print("  ✗ Avoid for: High cardinality (creates too many columns)")

print("\n📊 TARGET ENCODING:")
print("  ✓ Use for: High cardinality nominal data")
print("  ✓ Captures relationship between category and target")
print("  ⚠️ Risk of: Overfitting, requires careful cross-validation")

print("\n💾 BINARY ENCODING:")
print("  ✓ Use for: Medium-high cardinality data")
print("  ✓ More compact than one-hot encoding")
print("  ✓ Good balance between information and dimensionality")

print("\n📈 FREQUENCY ENCODING:")
print("  ✓ Use for: When frequency of category is meaningful")
print("  ✓ Simple and effective for some datasets")

print("\n🔨 FEATURE HASHING:")
print("  ✓ Use for: Very high cardinality data")
print("  ✓ Memory efficient, handles new categories")
print("  ✗ Information loss due to hash collisions")

print("\n=== BEST PRACTICES ===")
print("• Always consider the nature of your categorical data (ordinal vs nominal)")
print("• For tree-based models: Label encoding often works well")
print("• For linear models: One-hot encoding is usually better")
print("• Handle new categories in test data (use 'unknown' category)")
print("• Consider dimensionality impact on model performance")
print("• Validate encoding choices with cross-validation")