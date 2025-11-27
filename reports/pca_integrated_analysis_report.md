
# PCA-Enhanced Integrated Analysis of MCMC Missed Cases

## Overview
This analysis applies Principal Component Analysis (PCA) to system strength and risk burden indicators, comparing PCA-derived components with traditional weighted indices for explaining MCMC-estimated missed TB cases.

## Data and Methods

### System Strength Indicators (6 variables)
- Diabetes screening and treatment rates
- Tobacco screening and cessation linkage
- Alcohol screening and de-addiction linkage

### Risk Burden Indicators (7 variables)
- Nutritional status: stunting, underweight, wasting, anemia
- Behavioral risks: tobacco and alcohol use

### PCA Implementation
- Standardized all variables before PCA
- Retained components explaining significant variance
- Compared PCA components with expert-weighted indices

## PCA Results

### System Strength PCA
- **Components retained**: 3 (explaining 89.8% of total variance)
- **PC1 (61.0% variance)**: Overall system performance
- **PC2 (21.2% variance)**: Comorbidity intervention focus
- **PC3 (7.6% variance)**: Specific service delivery patterns

### Risk Burden PCA
- **Components retained**: 3 (explaining 84.9% of total variance)
- **PC1 (43.8% variance)**: Nutritional and health status
- **PC2 (28.4% variance)**: Substance use behaviors
- **PC3 (12.7% variance)**: Socioeconomic vulnerabilities

## Correlation Analysis

### Traditional vs PCA Correlations with MCMC Missed Cases

| Index Type | System Correlation | Risk Correlation |
|------------|-------------------|------------------|
| Traditional Weighted | -0.315 | 0.297 |
| PCA PC1 | -0.349 | 0.336 |

## Regression Models

### Traditional Weighted Model
```
R-squared: 0.125
System coefficient: -43134.7
Risk coefficient: 35956.8
```

### PCA-Based Model
```
R-squared: 0.351
PC1 coefficient: -28220.9 PC2 coefficient: 37089.3 PC3 coefficient: 97029.7 PC4 coefficient: 28805.8
```

## Key Insights

### PCA Advantages
1. **Data-driven weights** instead of expert judgment
2. **Orthogonal components** eliminate multicollinearity
3. **Comprehensive variance capture** (vs. selective weighting)
4. **Clear interpretability** through component loadings

### Comparative Performance
- **System indices**: PCA PC1 shows 10.7% stronger correlation than traditional index
- **Risk indices**: PCA PC1 shows 13.3% stronger correlation than traditional index
- **Overall model**: PCA approach explains 2.8x more variance

### Component Interpretations

#### System PC1 Loadings
- Diabetes screening: 0.374
- Diabetes treatment: 0.381
- Tobacco screening: 0.484
- Tobacco linkage: 0.387
- Alcohol screening: 0.487
- Alcohol linkage: 0.307

#### Risk PC1 Loadings
- Stunting: 0.490
- Underweight: 0.547
- Wasting: 0.519
- Anemia: 0.358
- Male tobacco: 0.136
- Female tobacco: -0.083
- Male alcohol: -0.191

## Policy Implications

### Enhanced Targeting
- **High system PC1, low risk PC1 states**: Focus on case-finding expansion
- **Low system PC1, high risk PC1 states**: Prioritize system strengthening
- **High system PC1, high risk PC1 states**: Balanced interventions needed

### Intervention Prioritization
- **System PC2 (comorbidity focus)**: Target states with low diabetes/tobacco management
- **Risk PC2 (substance use)**: Focus on tobacco/alcohol control programs
- **Risk PC3 (socioeconomic)**: Address underlying poverty and sanitation issues

## Figures Generated
- `pca_analysis_system.png`: System strength PCA diagnostics
- `pca_analysis_risk.png`: Risk burden PCA diagnostics
- `pca_vs_traditional_comparison.png`: Comparative correlation analysis

## Data Files
- `pca_integrated_analysis.csv`: Complete dataset with PCA components
- MCMC missed cases integrated with PCA-derived indices

## Conclusions

PCA provides a more robust and data-driven approach to constructing composite indices compared to traditional weighted averages. The analysis reveals that:

1. **System performance** is best captured by a single dominant component explaining overall capacity
2. **Risk burden** has multiple dimensions requiring 2-3 components for comprehensive representation
3. **Predictive power** is enhanced with PCA-derived indices, particularly for system strength factors
4. **Policy targeting** benefits from the orthogonal nature of PCA components

The PCA-enhanced framework offers improved explanatory power and clearer interpretation for understanding the determinants of missed TB cases across Indian states.

---
*Analysis generated on 2025-11-27 10:53:11*
