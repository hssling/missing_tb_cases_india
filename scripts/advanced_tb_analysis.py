import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy.stats import pearsonr, linregress
import seaborn as sns
import matplotlib.pyplot as plt
import os

os.makedirs('output/tables', exist_ok=True)
os.makedirs('output/figures', exist_ok=True)

df = pd.read_csv('data/processed/nfhs_rs_tb_merged.csv')

# Prep
numeric_df = df.select_dtypes(include=[np.number]).dropna()
X = numeric_df.drop(['2023'], axis=1)  # risks
y = numeric_df['2023']  # TB cases 2023

# Corrs
corrs = df.corr(numeric_only=True)['2023'].sort_values(ascending=False)
corrs_df = pd.DataFrame({'corr': corrs}).round(3)
corrs_df.to_csv('output/tables/advanced_corrs.csv')

# OLS Reg
from sklearn.linear_model import LinearRegression
model = LinearRegression().fit(X, y)
r2 = model.score(X, y)
reg_df = pd.DataFrame({'coef': model.coef_, 'feature': X.columns}).round(3)
reg_df['r2'] = r2
reg_df.to_csv('output/tables/advanced_reg.csv', index=False)

# RF Feature Importance
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X, y)
importance = pd.DataFrame({'feature': X.columns, 'importance': rf.feature_importances_}).sort_values('importance', ascending=False)
importance.to_csv('output/tables/rf_importance.csv', index=False)

# KMeans Clustering
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(X_scaled)
cluster_summary = df.groupby('cluster')[['2023']].mean()
cluster_summary.to_csv('output/tables/cluster_summary.csv')

# Plots
plt.figure(figsize=(10,8))
sns.heatmap(corrs.to_frame(), annot=True, cmap='RdBu_r', center=0)
plt.title('TB Cases 2023 Correlations')
plt.savefig('output/figures/advanced_corr_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

plt.figure(figsize=(10,6))
sns.barplot(data=importance.head(10), x='importance', y='feature')
plt.title('RF Feature Importance')
plt.savefig('output/figures/rf_importance.png', dpi=300, bbox_inches='tight')
plt.close()

print('Advanced analysis complete. Check output/tables/ figures/.')
print(corrs.head(10))
print('R2 OLS:', r2)
print(importance.head())
print(cluster_summary)
