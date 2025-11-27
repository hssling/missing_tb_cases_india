# Integrated Multi-Source Assessment of Missed Tuberculosis Cases in India

**Latest Version: MCMC Bayesian Analysis with System-Risk Integration**

This repository provides a comprehensive framework for estimating "missed" TB cases in India using advanced Bayesian MCMC methods, integrated with system-strength and epidemiological risk indices. The pipeline combines WHO Global TB Reports, Ni-kshay notifications, India TB Report cascade indicators, and NFHS-5 socio-demographic data to produce uncertainty-quantified estimates and policy-relevant insights.

**Key Innovation:** Bayesian MCMC estimation with integrated system-risk analysis providing robust uncertainty quantification and deeper insights into TB detection determinants.

---

## Repository Layout (Updated)

```
.
├── data/
│   ├── raw/         # WHO CSVs, Ni-kshay exports, NFHS aggregates, cascade tables
│   └── processed/   # Auto-generated panels and integrated datasets
├── lit/             # PubMed search results
├── models/          # MCMC traces and Bayesian model outputs
├── output/
│   ├── figures/     # All generated plots including MCMC and integrated analysis
│   ├── tables/      # Scenario summaries, detection panels, MCMC results
│   └── dashboards/  # Files ready for BI tooling
├── reports/
│   ├── protocol_draft.md
│   ├── analysis_summary.md (auto-generated)
│   ├── tb_manuscript_v13_comprehensive_integrated_final.md
│   ├── tb_manuscript_v13_comprehensive_with_figures.docx
│   ├── integrated_mcmc_system_risk_analysis.md
│   └── state_profiles/ (optional)
├── scripts/
│   ├── 01-07/       # Original pipeline scripts
│   ├── 14_final_mcmc_docx_complete.py
│   ├── 15_integrated_mcmc_system_risk_analysis.py
│   ├── 16_build_v13_integrated_docx.py
│   └── 17_build_comprehensive_v13_docx.py
└── README_v2.md     # This updated documentation
```

---

## Latest Features & Capabilities

### 🔬 **Advanced MCMC Bayesian Analysis**
- **Markov Chain Monte Carlo** estimation with Metropolis-Hastings sampling
- **Uncertainty quantification** with 95% credible intervals
- **National estimate**: 2.8 million missed cases (95% CI: 2.0-3.3 million) in 2023
- **State-level estimates** with proper uncertainty bounds

### 📊 **Integrated System-Risk Analysis**
- **System Strength Index**: Composite from diabetes screening (40%), tobacco linkage (30%), alcohol linkage (30%)
- **Epidemiological Risk Index**: NFHS-5 indicators (stunting, underweight, anemia, tobacco/alcohol use)
- **Correlation Analysis**:
  - System strength vs MCMC missed cases: r = -0.315 (p < 0.05)
  - Risk burden vs MCMC missed cases: r = +0.300 (p < 0.05)
- **Multivariate Regression**: R² = 0.126 explaining variation in missed cases

### 📈 **Comprehensive Visualizations**
- **Figure 1**: National TB trends with missed case gaps
- **Figure 2**: MCMC state estimates with credible intervals
- **Figure 3**: Geospatial detection coverage map
- **Figure 4**: Integrated scatter plots (system vs risk correlations)
- **Figure 5**: Sensitivity analysis under different scenarios

### 📄 **Publication-Ready Outputs**
- **Comprehensive manuscript** with embedded figures
- **Academic formatting** suitable for peer-reviewed journals
- **Complete tables** with MCMC estimates and integrated analysis
- **Executive summary** with key policy implications

---

## Required Inputs (`data/raw/`)

| File | Description | Latest Update |
| --- | --- | --- |
| `TB_burden_countries_2025-11-23.csv` | WHO TB burden extract with incidence/mortality | 2025 |
| `TB_notifications_2025-11-23.csv` | WHO notification extract with c_newinc totals | 2025 |
| `RS_Session_260_AU_618_A_to_B_i.csv` | Ni-kshay state notifications (2020–2023) | 2024 |
| `RS_Session_266_AU_1736_A_to_C_3.csv` | Age/death distributions | 2024 |
| `RS_Session_266_AU_2511_1.csv` | 2024 year-to-date notifications | 2024 |
| `2.10_TB_Diabetes.csv`, `2.11_TB_Tobacco.csv`, `2.12_TB_Alcohol.csv` | India TB Report cascade indicators | 2024 |
| `nfhs5_state_agg.csv` | NFHS-5 state-level risk indicators | 2019-21 |

---

## Environment Setup

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

**Key Dependencies:**
- `pandas`, `numpy` for data processing
- `matplotlib`, `seaborn`, `plotly` for visualizations
- `python-docx` for manuscript generation
- `scikit-learn` for statistical analysis
- `pymc` (optional) for Bayesian modeling

---

## Enhanced Pipeline (Latest Version)

### Core Analysis Pipeline
1. **Data Ingestion** – Scripts 01-03: Process WHO, Ni-kshay, and NFHS data
2. **MCMC Bayesian Modeling** – `mcmc_bayesian_analysis.py`: Generate uncertainty-quantified estimates
3. **Integrated Analysis** – `scripts/15_integrated_mcmc_system_risk_analysis.py`: Correlate MCMC results with system-risk indices
4. **Manuscript Generation** – `scripts/17_build_comprehensive_v13_docx.py`: Create publication-ready document with figures

### Key Analysis Scripts

#### `scripts/15_integrated_mcmc_system_risk_analysis.py`
- Loads MCMC missed case estimates
- Computes system strength and risk burden indices
- Performs correlation and regression analysis
- Generates integrated visualizations
- Outputs: `reports/integrated_mcmc_system_risk_analysis.md`

#### `scripts/17_build_comprehensive_v13_docx.py`
- Creates comprehensive manuscript with embedded figures
- Includes all MCMC results and integrated analysis
- Professional academic formatting
- Outputs: `reports/tb_manuscript_v13_comprehensive_with_figures.docx`

### Quick Start Commands

```bash
# Run integrated analysis
python scripts/15_integrated_mcmc_system_risk_analysis.py

# Generate comprehensive manuscript with figures
python scripts/17_build_comprehensive_v13_docx.py

# View results
start reports/tb_manuscript_v13_comprehensive_with_figures.docx
```

---

## Key Findings Summary

### MCMC Bayesian Estimates (2023)
- **National**: 2,818,000 missed cases (95% CI: 2,048,000-3,340,000)
- **Bihar**: 1,099,000 missed cases (highest burden state)
- **Uttar Pradesh**: 15,100 missed cases
- **Madhya Pradesh**: 2,510 missed cases

### Integrated System-Risk Insights
- **System Strength**: Stronger health systems reduce missed cases by ~40K per standard deviation
- **Risk Burden**: Higher epidemiological risk increases missed cases by ~35K per standard deviation
- **Policy Implication**: States need BOTH system strengthening AND risk mitigation strategies

### Scenario Analysis
- **90% Detection Target**: Requires 182,000 additional annual notifications
- **Detection Rate Improvement**: 20% increase reduces missed cases by 75%
- **Population Coverage**: Minimal impact compared to detection improvements

---

## File Outputs

### Manuscripts & Reports
- `reports/tb_manuscript_v13_comprehensive_integrated_final.md` - Markdown manuscript
- `reports/tb_manuscript_v13_comprehensive_with_figures.docx` - Word document with figures
- `reports/integrated_mcmc_system_risk_analysis.md` - Analysis report

### Data & Tables
- `output/tables/integrated_mcmc_system_risk.csv` - Merged analysis dataset
- `output/mcmc_missed_cases_sensitivity_results.json` - MCMC results
- `output/bayesian_results.json` - Additional Bayesian outputs

### Figures
- `output/figures/integrated_mcmc_system_risk.png` - System-risk correlations
- `output/figures/mcmc_state_incidence_complete.png` - MCMC state estimates
- `output/figures/sensitivity_analysis_missed_cases.png` - Scenario analysis
- `output/figures/national_trend.png` - National trends
- `output/figures/state_detection_map.png` - Detection coverage map

---

## Methodology Overview

### MCMC Bayesian Framework
```
Likelihood: Notifications ~ Poisson(μ)
μ = True Incidence × Detection Rate
True Incidence = Missed Cases + Notifications
Priors: WHO incidence estimates + state random effects
```

### System-Risk Integration
```
System Score = 0.4×DM_screening + 0.3×Tobacco_linkage + 0.3×Alcohol_linkage
Risk Score = 0.25×Stunting + 0.25×Underweight + 0.2×Anemia + 0.15×Tobacco + 0.1×Alcohol
                                      - 0.05×Sanitation - 0.05×Clean_fuel
```

### Statistical Analysis
- **Correlations**: Pearson r with p-values
- **Regression**: OLS with system and risk predictors
- **Uncertainty**: MCMC credible intervals (95% CI)

---

## Citation & Usage

**Recommended Citation:**
```
H S Siddalingaiah. Integrated Multi-Source Assessment of Missed Tuberculosis Cases in India:
Bayesian MCMC and System-Risk Integration. 2025.
```

**Usage Guidelines:**
- Cite WHO, Ni-kshay, NFHS-5, and India TB Report sources
- Use for research and policy analysis
- Contact author for collaboration opportunities

**Repository Status:** Active development with regular updates for new WHO data releases and methodological improvements.

---

*This README documents the latest version with MCMC Bayesian analysis and integrated system-risk modeling. For the original deterministic pipeline, see README.md.*