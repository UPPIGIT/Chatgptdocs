import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, MaxAbsScaler, Normalizer
from sklearn.preprocessing import QuantileTransformer, PowerTransformer
import matplotlib.pyplot as plt

# Create dataset with different scales
np.random.seed(42)
data = {
    'age': np.random.normal(35, 10, 100),           # Scale: ~15-55
    'salary': np.random.normal(65000, 20000, 100),  # Scale: ~25K-105K
    'experience': np.random.normal(8, 4, 100),      # Scale: ~0-16
    'score': np.random.normal(75, 15, 100),         # Scale: ~30-120
    'distance_km': np.random.exponential(10, 100),  # Scale: ~0-50 (skewed)
}

df = pd.DataFrame(data)
# Ensure no negative values for some columns
df['age'] = np.abs(df['age'])
df['experience'] = np.abs(df['experience'])

print("=== FEATURE SCALING AND NORMALIZATION ===")
print("\n1. ORIGINAL DATASET STATISTICS")
print("-" * 40)
print("Dataset shape:", df.shape)
print(df.describe())

print(f"\nScale differences:")
for col in df.columns:
    print(f"{col:12}: Range = {df[col].min():.2f} to {df[col].max():.2f}, "
          f"Mean = {df[col].mean():.2f}, Std = {df[col].std():.2f}")

# METHOD 1: STANDARDIZATION (Z-SCORE NORMALIZATION)
print("\n2. METHOD 1: STANDARDIZATION (Z-SCORE)")
print("-" * 40)

scaler_standard = StandardScaler()
df_standardized = pd.DataFrame(
    scaler_standard.fit_transform(df),
    columns=df.columns
)

print("After Standardization (mean=0, std=1):")
print(df_standardized.describe())

print(f"\nStandardization formula: (x - mean) / std")
print(f"Example for salary:")
original_salary = df['salary'].iloc[0]
standardized_salary = (original_salary - df['salary'].mean()) / df['salary'].std()
print(f"  Original: {original_salary:.2f}")
print(f"  Standardized: {standardized_salary:.2f}")
print(f"  Sklearn result: {df_standardized['salary'].iloc[0]:.2f}")

# METHOD 2: MIN-MAX NORMALIZATION
print("\n3. METHOD 2: MIN-MAX NORMALIZATION")
print("-" * 40)

scaler_minmax = MinMaxScaler()
df_minmax = pd.DataFrame(
    scaler_minmax.fit_transform(df),
    columns=df.columns
)

print("After Min-Max Normalization (range: 0-1):")
print(df_minmax.describe())

print(f"\nMin-Max formula: (x - min) / (max - min)")
print(f"Example for age:")
original_age = df['age'].iloc[0]
minmax_age = (original_age - df['age'].min()) / (df['age'].max() - df['age'].min())
print(f"  Original: {original_age:.2f}")
print(f"  Min-Max: {minmax_age:.2f}")
print(f"  Sklearn result: {df_minmax['age'].iloc[0]:.2f}")

# METHOD 3: ROBUST SCALING
print("\n4. METHOD 3: ROBUST SCALING")
print("-" * 40)

scaler_robust = RobustScaler()
df_robust = pd.DataFrame(
    scaler_robust.fit_transform(df),
    columns=df.columns
)

print("After Robust Scaling (uses median and IQR):")
print(df_robust.describe())

print(f"\nRobust scaling formula: (x - median) / IQR")
print(f"Example for salary:")
salary_median = df['salary'].median()
salary_q1 = df['salary'].quantile(0.25)
salary_q3 = df['salary'].quantile(0.75)
salary_iqr = salary_q3 - salary_q1
robust_salary = (original_salary - salary_median) / salary_iqr
print(f"  Original: {original_salary:.2f}")
print(f"  Median: {salary_median:.2f}, IQR: {salary_iqr:.2f}")
print(f"  Robust scaled: {robust_salary:.2f}")
print(f"  Sklearn result: {df_robust['salary'].iloc[0]:.2f}")

# METHOD 4: MAX ABSOLUTE SCALING
print("\n5. METHOD 4: MAX ABSOLUTE SCALING")
print("-" * 40)

scaler_maxabs = MaxAbsScaler()
df_maxabs = pd.DataFrame(
    scaler_maxabs.fit_transform(df),
    columns=df.columns
)

print("After Max Absolute Scaling (range: -1 to 1):")
print(df_maxabs.describe())

print(f"\nMax Absolute formula: x / max(|x|)")
print(f"Example for experience:")
original_exp = df['experience'].iloc[0]
max_abs_exp = np.max(np.abs(df['experience']))
maxabs_exp = original_exp / max_abs_exp
print(f"  Original: {original_exp:.2f}")
print(f"  Max absolute value: {max_abs_exp:.2f}")
print(f"  Scaled: {maxabs_exp:.2f}")

# METHOD 5: UNIT VECTOR SCALING (NORMALIZATION)
print("\n6. METHOD 5: UNIT VECTOR SCALING")
print("-" * 40)

normalizer = Normalizer(norm='l2')  # L2 norm (Euclidean)
df_normalized = pd.DataFrame(
    normalizer.fit_transform(df),
    columns=df.columns
)

print("After Unit Vector Scaling (L2 norm):")
print(df_normalized.describe())

# Check if rows have unit norm
row_norms = np.sqrt((df_normalized ** 2).sum(axis=1))
print(f"\nRow norms (should be ~1.0): {row_norms[:5].values}")
print(f"Unit vector scaling: scales each sample (row) to have unit norm")

# METHOD 6: QUANTILE TRANSFORMATION
print("\n7. METHOD 6: QUANTILE TRANSFORMATION")
print("-" * 40)

# Uniform quantile transformation
qt_uniform = QuantileTransformer(output_distribution='uniform', random_state=42)
df_qt_uniform = pd.DataFrame(
    qt_uniform.fit_transform(df),
    columns=df.columns
)

print("After Quantile Transformation (Uniform):")
print(df_qt_uniform.describe())

# Normal quantile transformation
qt_normal = QuantileTransformer(output_distribution='normal', random_state=42)
df_qt_normal = pd.DataFrame(
    qt_normal.fit_transform(df),
    columns=df.columns
)

print("\nAfter Quantile Transformation (Normal):")
print(df_qt_normal.describe())

# METHOD 7: POWER TRANSFORMATION
print("\n8. METHOD 7: POWER TRANSFORMATION")
print("-" * 40)

# Yeo-Johnson transformation (handles negative values)
pt_yeo = PowerTransformer(method='yeo-johnson', standardize=True)
df_pt_yeo = pd.DataFrame(
    pt_yeo.fit_transform(df),
    columns=df.columns
)

print("After Yeo-Johnson Power Transformation:")
print(df_pt_yeo.describe())

# Box-Cox transformation (requires positive values)
df_positive = df.copy()
df_positive = df_positive + abs(df_positive.min()) + 1  # Make all values positive

pt_box = PowerTransformer(method='box-cox', standardize=True)
df_pt_box = pd.DataFrame(
    pt_box.fit_transform(df_positive),
    columns=df.columns
)

print("\nAfter Box-Cox Power Transformation:")
print(df_pt_box.describe())

# COMPARISON WITH OUTLIERS
print("\n9. HANDLING OUTLIERS WITH DIFFERENT SCALERS")
print("-" * 40)

# Add some outliers to demonstrate robustness
df_with_outliers = df.copy()
df_with_outliers.loc[0, 'salary'] = 500000  # Extreme outlier
df_with_outliers.loc[1, 'age'] = 90         # Age outlier

print("Dataset with outliers:")
print(df_with_outliers.describe())

# Compare how different scalers handle outliers
scalers = {
    'StandardScaler': StandardScaler(),
    'MinMaxScaler': MinMaxScaler(),
    'RobustScaler': RobustScaler()
}

print(f"\nEffect of outliers on different scalers (salary column):")
print(f"{'Method':<15} {'Min':<10} {'Max':<10} {'Mean':<10} {'Std':<10}")
print("-" * 50)

for name, scaler in scalers.items():
    scaled_data = scaler.fit_transform(df_with_outliers)
    salary_idx = df_with_outliers.columns.get_loc('salary')
    scaled_salary = scaled_data[:, salary_idx]
    
    print(f"{name:<15} {scaled_salary.min():<10.2f} {scaled_salary.max():<10.2f} "
          f"{scaled_salary.mean():<10.2f} {scaled_salary.std():<10.2f}")

# CHOOSING THE RIGHT SCALER
print("\n10. CHOOSING THE RIGHT SCALER")
print("-" * 40)

scaling_guide = {
    'Method': ['StandardScaler', 'MinMaxScaler', 'RobustScaler', 'MaxAbsScaler', 
               'Normalizer', 'QuantileTransformer', 'PowerTransformer'],
    'Best_For': [
        'Normally distributed data',
        'Known min/max bounds needed',
        'Data with outliers',
        'Sparse data, already centered',
        'Text/document data (TF-IDF)',
        'Non-linear transformations',
        'Skewed data normalization'
    ],
    'Output_Range': [
        'Mean=0, Std=1',
        '[0, 1]',
        'Median=0, robust spread',
        '[-1, 1]',
        'Unit norm per sample',
        '[0, 1] or Normal',
        'Normalized distribution'
    ],
    'Outlier_Robust': [
        'No', 'No', 'Yes', 'No', 'No', 'Yes', 'Moderate'
    ]
}

guide_df = pd.DataFrame(scaling_guide)
print(guide_df.to_string(index=False))

# PRACTICAL EXAMPLE: BEFORE AND AFTER
print("\n11. PRACTICAL EXAMPLE: IMPACT ON MODEL")
print("-" * 40)

# Simulate distance calculation (relevant for KNN, clustering)
print("Example: Distance between first two samples")
print("(Important for KNN, K-means, SVM with RBF kernel)")

sample1 = df.iloc[0].values
sample2 = df.iloc[1].values

# Euclidean distance without scaling
dist_original = np.sqrt(np.sum((sample1 - sample2) ** 2))

# Distance after standardization
sample1_std = df_standardized.iloc[0].values
sample2_std = df_standardized.iloc[1].values
dist_standardized = np.sqrt(np.sum((sample1_std - sample2_std) ** 2))

print(f"Original distance: {dist_original:.2f}")
print(f"Standardized distance: {dist_standardized:.2f}")
print(f"Without scaling, salary dominates due to large scale!")

# Show feature contribution to distance
feature_contrib_orig = (sample1 - sample2) ** 2
feature_contrib_std = (sample1_std - sample2_std) ** 2

print(f"\nFeature contribution to squared distance:")
print(f"{'Feature':<12} {'Original':<12} {'Standardized':<12}")
print("-" * 36)
for i, col in enumerate(df.columns):
    print(f"{col:<12} {feature_contrib_orig[i]:<12.2f} {feature_contrib_std[i]:<12.2f}")

print("\n=== SCALING BEST PRACTICES ===")
print("🎯 Always split data before scaling (avoid data leakage)")
print("📊 Fit scaler on training data only, transform train & test")
print("🔍 Consider data distribution when choosing scaler")
print("⚠️  Remember to inverse transform predictions if needed")
print("🧪 Test different scalers with cross-validation")
print("📈 Tree-based models (Random Forest, XGBoost) often don't need scaling")
print("🎲 Distance-based models (KNN, SVM, Neural Networks) usually need scaling")