import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Create dataset with outliers
np.random.seed(42)
normal_salaries = np.random.normal(60000, 15000, 95)  # Normal salaries
outlier_salaries = [200000, 250000, 300000, 15000, 10000]  # Add some outliers
salaries = np.concatenate([normal_salaries, outlier_salaries])

normal_ages = np.random.normal(35, 8, 95)  # Normal ages
outlier_ages = [90, 95, 12, 8, 85]  # Add some outliers
ages = np.concatenate([normal_ages, outlier_ages])

df = pd.DataFrame({
    'salary': salaries,
    'age': ages,
    'employee_id': range(1, 101)
})

print("=== HANDLING OUTLIERS ===")
print("\n1. ORIGINAL DATASET STATISTICS")
print("-" * 40)
print(df.describe())

# METHOD 1: DETECT OUTLIERS USING IQR
print("\n2. METHOD 1: IQR (INTERQUARTILE RANGE) METHOD")
print("-" * 40)

def detect_outliers_iqr(data, column):
    """Detect outliers using IQR method"""
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    
    print(f"\n{column} outlier detection:")
    print(f"  Q1 (25th percentile): {Q1:.2f}")
    print(f"  Q3 (75th percentile): {Q3:.2f}")
    print(f"  IQR: {IQR:.2f}")
    print(f"  Lower bound: {lower_bound:.2f}")
    print(f"  Upper bound: {upper_bound:.2f}")
    print(f"  Number of outliers: {len(outliers)}")
    
    if len(outliers) > 0:
        print(f"  Outlier values: {sorted(outliers[column].values)}")
    
    return outliers, lower_bound, upper_bound

# Detect outliers for salary
salary_outliers, sal_lower, sal_upper = detect_outliers_iqr(df, 'salary')

# Detect outliers for age
age_outliers, age_lower, age_upper = detect_outliers_iqr(df, 'age')

# METHOD 2: DETECT OUTLIERS USING Z-SCORE
print("\n3. METHOD 2: Z-SCORE METHOD")
print("-" * 40)

def detect_outliers_zscore(data, column, threshold=3):
    """Detect outliers using Z-score method"""
    z_scores = np.abs(stats.zscore(data[column]))
    outliers = data[z_scores > threshold]
    
    print(f"\n{column} outlier detection (Z-score > {threshold}):")
    print(f"  Mean: {data[column].mean():.2f}")
    print(f"  Std: {data[column].std():.2f}")
    print(f"  Number of outliers: {len(outliers)}")
    
    if len(outliers) > 0:
        outlier_zscores = z_scores[z_scores > threshold]
        print(f"  Outlier Z-scores: {sorted(outlier_zscores)}")
        print(f"  Outlier values: {sorted(outliers[column].values)}")
    
    return outliers

# Detect outliers using Z-score
salary_outliers_z = detect_outliers_zscore(df, 'salary')
age_outliers_z = detect_outliers_zscore(df, 'age')

# METHOD 3: REMOVE OUTLIERS
print("\n4. METHOD 3: REMOVE OUTLIERS")
print("-" * 40)

# Remove using IQR method
df_no_outliers_iqr = df.copy()

# Remove salary outliers
df_no_outliers_iqr = df_no_outliers_iqr[
    (df_no_outliers_iqr['salary'] >= sal_lower) & 
    (df_no_outliers_iqr['salary'] <= sal_upper)
]

# Remove age outliers
df_no_outliers_iqr = df_no_outliers_iqr[
    (df_no_outliers_iqr['age'] >= age_lower) & 
    (df_no_outliers_iqr['age'] <= age_upper)
]

print(f"Original dataset size: {len(df)}")
print(f"After removing outliers: {len(df_no_outliers_iqr)}")
print(f"Rows removed: {len(df) - len(df_no_outliers_iqr)}")

print(f"\nStatistics after outlier removal:")
print(df_no_outliers_iqr.describe())

# METHOD 4: CAP OUTLIERS (WINSORIZING)
print("\n5. METHOD 4: CAP OUTLIERS (WINSORIZING)")
print("-" * 40)

df_capped = df.copy()

# Cap salary outliers
df_capped['salary'] = np.where(df_capped['salary'] > sal_upper, sal_upper, df_capped['salary'])
df_capped['salary'] = np.where(df_capped['salary'] < sal_lower, sal_lower, df_capped['salary'])

# Cap age outliers  
df_capped['age'] = np.where(df_capped['age'] > age_upper, age_upper, df_capped['age'])
df_capped['age'] = np.where(df_capped['age'] < age_lower, age_lower, df_capped['age'])

print("Outliers capped to boundary values:")
print(f"Salary range: {df_capped['salary'].min():.2f} - {df_capped['salary'].max():.2f}")
print(f"Age range: {df_capped['age'].min():.2f} - {df_capped['age'].max():.2f}")

print(f"\nStatistics after capping:")
print(df_capped.describe())

# METHOD 5: TRANSFORM DATA TO REDUCE OUTLIER IMPACT
print("\n6. METHOD 5: TRANSFORM DATA")
print("-" * 40)

df_transformed = df.copy()

# Log transformation for salary (right-skewed data)
df_transformed['salary_log'] = np.log1p(df_transformed['salary'])  # log1p = log(1+x)

# Square root transformation
df_transformed['salary_sqrt'] = np.sqrt(df_transformed['salary'])

print("Transformation effects on outliers:")
print(f"Original salary std: {df['salary'].std():.2f}")
print(f"Log-transformed std: {df_transformed['salary_log'].std():.2f}")
print(f"Sqrt-transformed std: {df_transformed['salary_sqrt'].std():.2f}")

# METHOD 6: USING PERCENTILE CAPPING
print("\n7. METHOD 6: PERCENTILE CAPPING")
print("-" * 40)

df_percentile = df.copy()

# Cap at 5th and 95th percentiles
sal_5th = df['salary'].quantile(0.05)
sal_95th = df['salary'].quantile(0.95)

age_5th = df['age'].quantile(0.05)
age_95th = df['age'].quantile(0.95)

df_percentile['salary'] = df_percentile['salary'].clip(sal_5th, sal_95th)
df_percentile['age'] = df_percentile['age'].clip(age_5th, age_95th)

print(f"Salary capped between {sal_5th:.2f} and {sal_95th:.2f}")
print(f"Age capped between {age_5th:.2f} and {age_95th:.2f}")

# METHOD 7: ISOLATION FOREST (ADVANCED)
print("\n8. METHOD 7: ISOLATION FOREST")
print("-" * 40)

from sklearn.ensemble import IsolationForest

# Use Isolation Forest for multivariate outlier detection
iso_forest = IsolationForest(contamination=0.1, random_state=42)  # Expect 10% outliers
outlier_labels = iso_forest.fit_predict(df[['salary', 'age']])

# -1 indicates outlier, 1 indicates normal
df_iso = df.copy()
df_iso['is_outlier'] = outlier_labels
outliers_iso = df_iso[df_iso['is_outlier'] == -1]

print(f"Isolation Forest detected {len(outliers_iso)} outliers")
print("Sample outliers:")
print(outliers_iso[['salary', 'age', 'employee_id']].head())

# COMPARISON OF METHODS
print("\n9. COMPARISON OF METHODS")
print("-" * 40)

methods_comparison = {
    'Method': ['Original', 'Remove IQR', 'Cap IQR', 'Log Transform', 'Percentile Cap', 'Isolation Forest'],
    'Dataset Size': [
        len(df),
        len(df_no_outliers_iqr),
        len(df_capped),
        len(df_transformed),
        len(df_percentile),
        len(df_iso[df_iso['is_outlier'] == 1])
    ],
    'Salary Mean': [
        df['salary'].mean(),
        df_no_outliers_iqr['salary'].mean(),
        df_capped['salary'].mean(),
        df['salary'].mean(),  # Original scale
        df_percentile['salary'].mean(),
        df_iso[df_iso['is_outlier'] == 1]['salary'].mean()
    ],
    'Salary Std': [
        df['salary'].std(),
        df_no_outliers_iqr['salary'].std(),
        df_capped['salary'].std(),
        df['salary'].std(),  # Original scale
        df_percentile['salary'].std(),
        df_iso[df_iso['is_outlier'] == 1]['salary'].std()
    ]
}

comparison_df = pd.DataFrame(methods_comparison)
print(comparison_df)

print("\n=== WHEN TO USE EACH METHOD ===")
print("• IQR Detection: Good general-purpose method, works well for normal distributions")
print("• Z-Score: Best for normally distributed data, sensitive to extreme outliers")
print("• Remove: When outliers are clearly errors or not representative")
print("• Capping: When you want to keep all data points but limit extreme values")
print("• Transform: When data is skewed, helps normalize distribution")
print("• Percentile: More robust than IQR, good for any distribution")
print("• Isolation Forest: Advanced method for multivariate outliers")

print("\n=== IMPORTANT CONSIDERATIONS ===")
print("• Always visualize your data before deciding on outlier treatment")
print("• Consider domain knowledge - some 'outliers' might be valid")
print("• Document your outlier handling decisions")
print("• Test model performance with and without outlier treatment")