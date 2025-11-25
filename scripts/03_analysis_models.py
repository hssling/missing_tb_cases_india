import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Paths
processed_dir = 'data/processed'
output_dir = 'output'
tables_dir = Path(output_dir) / 'tables'
figures_dir = Path(output_dir) / 'figures'
os.makedirs(tables_dir, exist_ok=True)
os.makedirs(figures_dir, exist_ok=True)

# Load data
data_path = Path(processed_dir) / 'district_tb_district_determinants.csv'
df = pd.read_csv(data_path)
print(f"Loaded data: {df.shape[0]} districts")
print(df.columns.tolist())

# Ensure numeric columns
numeric_cols = ['tb_rate', 'stunting_pct', 'wasting_pct', 'underweight_pct', 'crowding_pct',
                'smoking_men_pct', 'alcohol_men_pct', 'diabetes_women_pct', 'diabetes_men_pct',
                'population', 'literacy_rate', 'urban_pct', 'density', 'tb_cases_total']
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Drop rows with NaN in key vars
key_vars = ['tb_rate', 'tb_cases_total', 'log_population'] + [col for col in numeric_cols if 'pct' in col or col in ['literacy_rate', 'urban_pct', 'density']]
df = df.dropna(subset=key_vars)
print(f"After dropping NaN: {df.shape[0]} districts")

# 1. EDA: Summary statistics
summary_cols = ['tb_rate'] + [col for col in df.columns if any(ind in col.lower() for ind in ['stunt', 'wast', 'underw', 'crowd', 'smok', 'alcohol', 'diabet', 'liter', 'urban', 'dens'])]
summary_stats = df[summary_cols].describe()
summary_stats.to_csv(tables_dir / 'summary_stats.csv')
print("\nSummary statistics saved to output/tables/summary_stats.csv")

# Correlation matrix (Pearson)
corr_cols = summary_cols
corr_matrix = df[corr_cols].corr(method='pearson')
corr_matrix.to_csv(tables_dir / 'correlation_matrix.csv')
print("Correlation matrix saved to output/tables/correlation_matrix.csv")

# 2. EDA Plots
plt.style.use('seaborn-v0_8')
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Histogram of TB rate
axs[0, 0].hist(df['tb_rate'], bins=30, alpha=0.7, edgecolor='black')
axs[0, 0].set_title('Histogram of TB Notification Rate')
axs[0, 0].set_xlabel('TB Rate (per 100,000)')
axs[0, 0].set_ylabel('Frequency')

# Boxplot by region
sns.boxplot(data=df, x='region', y='tb_rate', ax=axs[0, 1])
axs[0, 1].set_title('TB Rate by Region')
axs[0, 1].tick_params(axis='x', rotation=45)

# Scatterplots for key predictors (select first 4 for subplot)
key_predictors = ['stunting_pct', 'crowding_pct', 'diabetes_women_pct', 'literacy_rate']
for i, pred in enumerate(key_predictors):
    if pred in df.columns:
        row = i // 2
        col = i % 2
        axs[row, col + 1 if row == 0 else col].scatter(df[pred], df['tb_rate'], alpha=0.6)
        axs[row, col + 1 if row == 0 else col].set_xlabel(pred.replace('_pct', ' (%)'))
        axs[row, col + 1 if row == 0 else col].set_ylabel('TB Rate')
        axs[row, col + 1 if row == 0 else col].set_title(f'TB Rate vs {pred.replace("_pct", "")}')

plt.tight_layout()
plt.savefig(figures_dir / 'eda_plots.png', dpi=300, bbox_inches='tight')
plt.close()
print("EDA plots saved to output/figures/eda_plots.png")

# 3. Negative Binomial Regression
# Prepare formula (adjust predictors based on available columns)
predictors = ['stunting_pct', 'crowding_pct', 'smoking_men_pct', 'alcohol_men_pct',
              'diabetes_women_pct', 'literacy_rate', 'urban_pct', 'density', 'C(region)']
avail_pred = [p for p in predictors if p in df.columns or (p.startswith('C(') and p[2:-1] in df.columns)]
formula_nb = 'tb_cases_total ~ ' + ' + '.join(avail_pred) + ' + offset(log_population)'

try:
    model_nb = smf.glm(formula=formula_nb, data=df, family=sm.families.NegativeBinomial()).fit()
    print(model_nb.summary())
    
    # Get IRR and CI
    coef = model_nb.params
    conf = model_nb.conf_int()
    irr = np.exp(coef)
    irr_ci_lower = np.exp(conf[0])
    irr_ci_upper = np.exp(conf[1])
    
    results_nb = pd.DataFrame({
        'IRR': irr,
        'CI_lower': irr_ci_lower,
        'CI_upper': irr_ci_upper,
        'p_value': model_nb.pvalues
    })
    results_nb.to_csv(tables_dir / 'model_nb_main.csv')
    print("NB model results (IRR) saved to output/tables/model_nb_main.csv")
    
    # Diagnostics: overdispersion (alpha should be >0 for NB)
    print(f"Overdispersion alpha: {model_nb.scale:.4f}")
    
except Exception as e:
    print(f"Error fitting NB model: {e}")

# 4. Sensitivity: Linear regression on log(TB rate)
df['log_tb_rate'] = np.log(df['tb_rate'] + 1)  # +1 to handle zeros
formula_lm = 'log_tb_rate ~ ' + ' + '.join([p for p in avail_pred if not p.startswith('C(')] + ['C(region)'])

try:
    model_lm = smf.ols(formula=formula_lm, data=df).fit()
    print(model_lm.summary())
    
    results_lm = pd.DataFrame({
        'coef': model_lm.params,
        'std_err': model_lm.bse,
        'p_value': model_lm.pvalues,
        'CI_lower': model_lm.conf_int()[0],
        'CI_upper': model_lm.conf_int()[1]
    })
    results_lm.to_csv(tables_dir / 'model_lm_sensitivity.csv')
    print("LM sensitivity results saved to output/tables/model_lm_sensitivity.csv")
    
except Exception as e:
    print(f"Error fitting LM model: {e}")

print("Analysis and models completed. Check output/tables and output/figures.")
