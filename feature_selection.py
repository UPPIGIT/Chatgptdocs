import pandas as pd
import numpy as np
from sklearn.feature_selection import (
    SelectKBest, SelectPercentile, f_classif, f_regression, chi2,
    RFE, RFECV, SelectFromModel, VarianceThreshold
)
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, Lasso
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt

# Create dataset with relevant and irrelevant features
np.random.seed(42)
n_samples = 1000

# Create target variable
target = np.random.choice([0, 1], n_samples)

# Create relevant features (correlated with target)
relevant_1 = target * 2 + np.random.normal(0, 0.5, n_samples)
relevant_2 = target * -1.5 + np.random.normal(0, 0.3, n_samples)
relevant_3 = target * 3 + np.random.normal(0, 0.8, n_samples)

# Create irrelevant features (random noise)
irrelevant_1 = np.random.normal(0, 1, n_samples)
irrelevant_2 = np.random.normal(0, 1, n_samples)
irrelevant_3 = np.random.normal(0, 1, n_samples)

# Create correlated features (redundant information)
correlated_1 = relevant_1 + np.random.normal(0, 0.1, n_samples)
correlated_2 = relevant_2 * 0.8 + np.random.normal(0, 0.2, n_samples)

# Create constant and low-variance features
constant_feature = np.ones(n_samples) * 5
low_variance = np.random.choice([1, 2], n_samples, p=[0.95, 0.05])

df = pd.DataFrame({
    'relevant_1': relevant_1,
    'relevant_2': relevant_2,
    'relevant_3': relevant_3,
    'irrelevant_1': irrelevant_1,
    'irrelevant_2': irrelevant_2,
    'irrelevant_3': irrelevant_3,
    'correlated_1': correlated_1,
    'correlated_2': correlated_2,
    'constant': constant_feature,
    'low_variance': low_variance,
    'target': target
})

print("=== FEATURE SELECTION ===")
print("\n1. ORIGINAL DATASET")
print("-" * 40)
print(f"Dataset shape: {df.shape}")
print(f"Features: {df.columns.tolist()}")
print(f"\nFirst few rows:")
print(df.head())

# Separate features and target
X = df.drop('target', axis=1)
y = df['target']

print(f"\nFeature correlations with target:")
correlations = X.corrwith(y).sort_values(key=abs, ascending=False)
print(correlations)

# METHOD 1: VARIANCE THRESHOLD
print("\n2. METHOD 1: VARIANCE THRESHOLD")
print("-" * 40)

# Remove constant and low-variance features
print("Feature variances:")
for col in X.columns:
    print(f"{col:<15}: {X[col].var():.4f}")

# Remove features with variance below threshold
variance_selector = VarianceThreshold(threshold=0.01)
X_variance_selected = variance_selector.fit_transform(X)
selected_features_var = X.columns[variance_selector.get_support()]

print(f"\nFeatures removed due to low variance:")
removed_features = X.columns[~variance_selector.get_support()]
print(removed_features.tolist())

print(f"\nRemaining features: {selected_features_var.tolist()}")
print(f"Original features: {X.shape[1]}, After variance threshold: {X_variance_selected.shape[1]}")

# METHOD 2: UNIVARIATE STATISTICAL TESTS
print("\n3. METHOD 2: UNIVARIATE STATISTICAL TESTS")
print("-" * 40)

# SelectKBest with f_classif for classification
print("SelectKBest with f_classif (ANOVA F-test):")
k_best_selector = SelectKBest(score_func=f_classif, k=5)
X_k_best = k_best_selector.fit_transform(X, y)

# Get scores and selected features
feature_scores = k_best_selector.scores_
feature_pvalues = k_best_selector.pvalues_
selected_features_k = X.columns[k_best_selector.get_support()]

print(f"\nFeature scores and p-values:")
score_df = pd.DataFrame({
    'Feature': X.columns,
    'Score': feature_scores,
    'P-value': feature_pvalues,
    'Selected': k_best_selector.get_support()
}).sort_values('Score', ascending=False)

print(score_df)
print(f"\nSelected features: {selected_features_k.tolist()}")

# SelectPercentile
print(f"\nSelectPercentile (top 50%):")
percentile_selector = SelectPercentile(score_func=f_classif, percentile=50)
X_percentile = percentile_selector.fit_transform(X, y)
selected_features_perc = X.columns[percentile_selector.get_support()]
print(f"Selected features: {selected_features_perc.tolist()}")

# METHOD 3: RECURSIVE FEATURE ELIMINATION (RFE)
print("\n4. METHOD 3: RECURSIVE FEATURE ELIMINATION")
print("-" * 40)

# RFE with LogisticRegression
estimator = LogisticRegression(random_state=42, max_iter=1000)
rfe_selector = RFE(estimator=estimator, n_features_to_select=5)
X_rfe = rfe_selector.fit_transform(X, y)

selected_features_rfe = X.columns[rfe_selector.get_support()]
feature_rankings = rfe_selector.ranking_

print("RFE with Logistic Regression:")
print(f"Selected features: {selected_features_rfe.tolist()}")

rfe_df = pd.DataFrame({
    'Feature': X.columns,
    'Ranking': feature_rankings,
    'Selected': rfe_selector.get_support()
}).sort_values('Ranking')

print(f"\nFeature rankings (1 = best):")
print(rfe_df)

# RFECV (RFE with Cross-Validation)
print(f"\nRFECV (finds optimal number of features):")
rfecv_selector = RFECV(estimator=estimator, cv=5, scoring='accuracy')
X_rfecv = rfecv_selector.fit_transform(X, y)

print(f"Optimal number of features: {rfecv_selector.n_features_}")
print(f"Selected features: {X.columns[rfecv_selector.get_support()].tolist()}")

# Plot RFECV scores
scores = rfecv_selector.cv_results_['mean_test_score']
print(f"Cross-validation scores by number of features:")
for i, score in enumerate(scores, 1):
    print(f"  {i} features: {score:.4f}")

# METHOD 4: MODEL-BASED SELECTION
print("\n5. METHOD 4: MODEL-BASED SELECTION")
print("-" * 40)

# SelectFromModel with Random Forest
print("SelectFromModel with Random Forest:")
rf_selector = RandomForestClassifier(n_estimators=100, random_state=42)
model_selector_rf = SelectFromModel(rf_selector)
X_model_rf = model_selector_rf.fit_transform(X, y)

selected_features_rf = X.columns[model_selector_rf.get_support()]
feature_importances_rf = rf_selector.fit(X, y).feature_importances_

print(f"Selected features: {selected_features_rf.tolist()}")

importance_df = pd.DataFrame({
    'Feature': X.columns,
    'Importance': feature_importances_rf,
    'Selected': model_selector_rf.get_support()
}).sort_values('Importance', ascending=False)

print(f"\nFeature importances:")
print(importance_df)

# SelectFromModel with Lasso (L1 regularization)
print(f"\nSelectFromModel with Lasso (L1 regularization):")
lasso_selector = Lasso(alpha=0.01, random_state=42)
model_selector_lasso = SelectFromModel(lasso_selector)
X_model_lasso = model_selector_lasso.fit_transform(X, y)

selected_features_lasso = X.columns[model_selector_lasso.get_support()]
lasso_coefs = lasso_selector.fit(X, y).coef_

print(f"Selected features: {selected_features_lasso.tolist()}")

lasso_df = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': lasso_coefs,
    'Abs_Coefficient': np.abs(lasso_coefs),
    'Selected': model_selector_lasso.get_support()
}).sort_values('Abs_Coefficient', ascending=False)

print(f"\nLasso coefficients:")
print(lasso_df)

# METHOD 5: CORRELATION-BASED SELECTION
print("\n6. METHOD 5: CORRELATION-BASED SELECTION")
print("-" * 40)

# Remove highly correlated features
corr_matrix = X.corr()
print("Correlation matrix (first 5 features):")
print(corr_matrix.iloc[:5, :5])

# Find highly correlated feature pairs
def find_correlated_features(corr_matrix, threshold=0.9):
    corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            if abs(corr_matrix.iloc[i, j]) > threshold:
                corr_pairs.append((
                    corr_matrix.columns[i],
                    corr_matrix.columns[j],
                    corr_matrix.iloc[i, j]
                ))
    return corr_pairs

high_corr_pairs = find_correlated_features(corr_matrix, threshold=0.8)
print(f"\nHighly correlated feature pairs (>0.8):")
for pair in high_corr_pairs:
    print(f"  {pair[0]} - {pair[1]}: {pair[2]:.3f}")

# Remove one feature from each highly correlated pair
features_to_remove = set()
for pair in high_corr_pairs:
    # Remove the second feature