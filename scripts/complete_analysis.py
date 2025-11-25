import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, linregress
import os

os.makedirs('output/tables', exist_ok=True)
os.makedirs('output/figures', exist_ok=True)

# Load merged data
df = pd.read_csv('data/processed/nfhs_rs_tb_merged.csv')

# TB target
tb_cases = df['2023']

# Key indicators from prior
indicators = [
    'Children under 5 years who are stunted (height-for-age)18 (%)',
    'Children under 5 years who are underweight (weight-for-age)18 (%)',
    'Children under 5 years who are wasted (weight-for-height)18 (%)',
    'Children age 6-59 months who are anaemic (<11.0 g/dl)22 (%)',
    'Men age 15 years and above who use any kind of tobacco (%)',
    'Women age 15 years and above who use any kind of tobacco (%)',
    'Men age 15 years and above who consume alcohol (%)',
    'Population living in households that use an improved sanitation facility2 (%)',
    'Households using clean fuel for cooking3 (%)',
]

# Corrs
corrs = {}
for ind in indicators:
    if ind in df.columns:
        corr, p = pearsonr(df[ind], tb_cases.dropna())
        corrs[ind] = (corr, p)

corrs_df = pd.DataFrame(corrs).T
corrs_df.columns = ['corr', 'p_value']
corrs_df.to_csv('output/tables/corrs_real.csv')
print("Corrs saved to output/tables/corrs_real.csv")
print(corrs_df)

# Regression (multi)
X = df[[ind for ind in indicators if ind in df.columns]].dropna()
y = tb_cases.reindex(X.index)
from sklearn.linear_model import LinearRegression
model = LinearRegression().fit(X, y)
r2 = model.score(X, y)
print(f"R2: {r2:.3f}")

reg_results = pd.DataFrame({
    'feature': X.columns,
    'coef': model.coef_,
    'r2': r2
})
reg_results.to_csv('output/tables/reg_real.csv', index=False)

# Plots
plt.figure(figsize=(10,8))
sns.heatmap(corrs_df['corr'].to_frame().T, annot=True, cmap='RdBu_r')
plt.title('TB Cases 2023 vs NFHS Indicators Corr')
plt.savefig('output/figures/corr_heatmap_real.png')
plt.close()

plt.figure(figsize=(8,6))
plt.scatter(df['Children under 5 years who are underweight (weight-for-age)18 (%)'], tb_cases)
plt.xlabel('Underweight %')
plt.ylabel('TB Cases 2023')
slope, intercept, r_value, p_value, std_err = linregress(df['Children under 5 years who are underweight (weight-for-age)18 (%)'], tb_cases)
plt.plot(df['Children under 5 years who are underweight (weight-for-age)18 (%)'], slope * df['Children under 5 years who are underweight (weight-for-age)18 (%)'] + intercept, 'r')
plt.title(f'TB vs Underweight (r={r_value:.3f})')
plt.savefig('output/figures/tb_underweight_real.png')
plt.close()

print("Analysis complete. Files saved.")
