import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Create a simple sample dataset
np.random.seed(42)
data = {
    'age': [25, 30, 35, np.nan, 45, 28, 52, 33],
    'salary': [50000, 60000, 75000, 80000, np.nan, 55000, 90000, 65000],
    'department': ['IT', 'HR', 'IT', 'Finance', 'HR', 'IT', 'Finance', 'HR'],
    'experience': [2, 5, 8, 12, np.nan, 3, 15, 6],
    'performance': ['Good', 'Excellent', 'Average', 'Good', 'Excellent', 'Average', 'Good', 'Excellent']
}

df = pd.DataFrame(data)

print("=== DATA EXPLORATION AND UNDERSTANDING ===")
print("\n1. BASIC INFORMATION")
print("-" * 30)
print(f"Dataset shape: {df.shape}")
print(f"Number of rows: {df.shape[0]}")
print(f"Number of columns: {df.shape[1]}")

print(f"\n2. FIRST FEW ROWS")
print("-" * 30)
print(df.head())

print(f"\n3. DATA TYPES")
print("-" * 30)
print(df.dtypes)

print(f"\n4. BASIC STATISTICS")
print("-" * 30)
print(df.describe())

print(f"\n5. MISSING VALUES")
print("-" * 30)
print("Missing count per column:")
print(df.isnull().sum())
print(f"\nMissing percentage per column:")
print((df.isnull().sum() / len(df)) * 100)

print(f"\n6. UNIQUE VALUES IN CATEGORICAL COLUMNS")
print("-" * 30)
categorical_cols = df.select_dtypes(include=['object']).columns
for col in categorical_cols:
    print(f"{col}: {df[col].unique()}")
    print(f"  Count: {len(df[col].unique())}")

print(f"\n7. DATA DISTRIBUTION")
print("-" * 30)
numerical_cols = df.select_dtypes(include=[np.number]).columns
for col in numerical_cols:
    print(f"\n{col}:")
    print(f"  Mean: {df[col].mean():.2f}")
    print(f"  Median: {df[col].median():.2f}")
    print(f"  Min: {df[col].min():.2f}")
    print(f"  Max: {df[col].max():.2f}")

print(f"\n8. MEMORY USAGE")
print("-" * 30)
print(df.info(memory_usage='deep'))

# Key Takeaways
print(f"\n9. KEY INSIGHTS")
print("-" * 30)
print("✓ We have 8 employees with 5 features")
print("✓ 3 numerical columns: age, salary, experience")
print("✓ 2 categorical columns: department, performance")
print("✓ Missing values in: age (1), salary (1), experience (1)")
print("✓ Departments: IT, HR, Finance")
print("✓ Performance levels: Good, Excellent, Average")
print("✓ Age range: 25-52 years")
print("✓ Salary range: $50K-$90K")

print(f"\n=== WHAT THIS STEP TELLS US ===")
print("• Data quality: We have some missing values to handle")
print("• Data types: Mixed numerical and categorical data")
print("• Scale differences: Salary is in thousands, age in tens")
print("• Categories: All categorical values seem valid")
print("• Next steps: Handle missing values, possibly scale features")