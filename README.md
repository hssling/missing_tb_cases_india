# Advanced TB Analysis Repository - Multi-Method Framework

**Version 4.0: Complete MCMC-PCA-DAG Integration**

This repository contains the most advanced multi-method framework for analyzing missed tuberculosis cases in India, featuring MCMC Bayesian estimation, Principal Component Analysis (PCA), and Directed Acyclic Graph (DAG) causal modeling.

---

## 📊 **Complete Analysis Versions Timeline**

### Manuscript Evolution
- **v9**: Original Bayesian hierarchical analysis (system-risk integration)
- **v12**: MCMC Bayesian missed cases estimation
- **v13**: MCMC + system-risk indices integration
- **v14**: PCA-enhanced dimensionality reduction
- **v15**: **Complete MCMC-PCA-DAG integration** (current)

### Analytical Methods Added
- **MCMC Bayesian**: Uncertainty quantification (scripts 12-14)
- **PCA Analysis**: Data-driven composite indices (scripts 15-19)
- **DAG Modeling**: Causal inference framework (script 20)
- **Integrated Framework**: Multi-method synthesis (script 21)

---

## 🎯 **Final Comprehensive Analysis: MCMC + PCA + DAG**

### **Core Innovation**
This repository pioneers the **first comprehensive application** of three advanced analytical methods to TB detection determinants:

1. **MCMC Bayesian Estimation** - Uncertainty quantification through probabilistic modeling
2. **Principal Component Analysis** - Data-driven dimensionality reduction and composite index construction
3. **Directed Acyclic Graph Modeling** - Causal pathway identification and confounding control

### **Key Results Summary**

| **Method** | **National Missed Cases** | **Uncertainty Bounds** | **Explanatory Power** | **Key Insights** |
|------------|--------------------------|----------------------|---------------------|------------------|
| **MCMC Bayesian** | 2.8 million | 95% CI: 2.0-3.3M | Base estimates | Proper uncertainty quantification |
| **PCA Enhanced** | - | - | R² = 0.351 (2.8× improvement) | Data-driven indices superior |
| **DAG Integrated** | - | - | 36 causal relationships | Confounding control framework |
| **Multi-Method** | **2.8M missed cases** | **95% CI: 2.0-3.3M** | **35.1% variance explained** | **Actionable policy framework** |

---

## 🛠️ **Complete Pipeline (Version 4.0)**

### **Data Processing (Scripts 01-07)**
- WHO Global TB Report 2024 integration
- Ni-kshay notifications (2020-2023) processing
- India TB Report cascade indicators
- NFHS-5 risk factor aggregation
- State-level data harmonization

### **Advanced Analysis Methods**

#### **MCMC Bayesian Framework (Scripts 12-14)**
```python
# Hierarchical Bayesian model
True_Incidence ~ Poisson(μ_incidence)
Notifications ~ Binomial(True_Incidence, Detection_Rate)
Detection_Rate ~ Beta(α, β) with state effects

# Results: 2.8M missed cases (95% CI: 2.0-3.3M)
```

#### **PCA Dimensionality Reduction (Scripts 15-19)**
```python
# System Strength PCA: 3 components, 89.8% variance
PC1 (61.0%): Overall system capacity
PC2 (21.2%): Comorbidity specialization
PC3 (7.6%): Service delivery patterns

# Risk Burden PCA: 3 components, 84.9% variance
PC1 (43.8%): Nutritional vulnerabilities
PC2 (28.4%): Substance use behaviors
PC3 (12.7%): Socioeconomic factors
```

#### **DAG Causal Modeling (Script 20)**
```python
# 26 nodes, 36 causal links
G = nx.DiGraph()
# Evidence strength: Strong (19), Moderate (14), Weak (3)

# Key pathways identified:
# System: Socioeconomic_Status → Healthcare_Infrastructure → Detection_Probability → Missed_Cases ↓
# Risk: Socioeconomic_Status → Malnutrition_Prevalence ↓ → True_Incidence_Rate ↓
```

### **Integrated Synthesis (Script 21)**
- Multi-method validation and cross-verification
- State-specific prioritization matrix
- Policy intervention frameworks
- Publication-ready comprehensive manuscript

---

## 📈 **Major Findings & Insights**

### **1. MCMC Bayesian Uncertainty Quantification**
- **National Estimate**: 2.8 million missed TB cases in 2023
- **Uncertainty Range**: 95% credible interval of 2.0-3.3 million
- **State Variability**: Bihar (1.1M), UP (15K), MP (2.5K) missed cases
- **Policy Impact**: Proper uncertainty bounds for resource allocation

### **2. PCA Superiority Over Traditional Indices**
- **Performance Improvement**: 2.8× increase in explanatory power (R²: 0.125 → 0.351)
- **System Strength**: Single dominant dimension (PC1: 61.0% variance)
- **Risk Burden**: Multi-dimensional structure requiring 3 components
- **New Insights**: System PC3 emerges as significant predictor (p=0.041)

### **3. DAG Causal Pathways**
- **36 Causal Relationships** across 26 variables
- **Confounding Control**: Socioeconomic status affects both system and risk factors
- **Mediation Analysis**: Detection probability mediates system effects
- **Intervention Pathways**: Multiple routes from causes to outcomes

### **4. State-Specific Policy Framework**

| **State Priority** | **MCMC Missed Cases** | **System PC1** | **Risk PC1** | **DAG-Guided Strategy** |
|-------------------|----------------------|---------------|-------------|-------------------------|
| **Bihar** | 1,099,000 | -2.1σ | +2.3σ | Integrated system-risk interventions |
| **Uttar Pradesh** | 15,100 | -1.8σ | +1.9σ | Healthcare infrastructure focus |
| **Madhya Pradesh** | 2,510 | -1.5σ | +1.7σ | Balanced system strengthening |
| **Rajasthan** | 220,526 | -1.2σ | +1.4σ | Risk mitigation priority |
| **Maharashtra** | 83,612 | +0.8σ | -0.5σ | Case-finding expansion |

---

## 📊 **Generated Outputs**

### **Manuscripts & Reports**
1. **`tb_manuscript_v15_comprehensive_mcmc_pca_dag_final.docx`** - Complete integrated analysis (25+ pages)
2. **`dag_causal_analysis_report.md`** - Detailed DAG interpretation
3. **`pca_integrated_analysis_report.md`** - PCA methodology and results
4. **`integrated_mcmc_system_risk_analysis.md`** - MCMC-system integration

### **Visualizations**
1. **`dag_causal_tb_analysis.png`** - Full DAG with 26 nodes, 36 causal links
2. **`pca_vs_traditional_comparison.png`** - Comparative performance analysis
3. **`pca_analysis_system.png`** - System strength PCA diagnostics
4. **`pca_analysis_risk.png`** - Risk burden PCA diagnostics
5. **`integrated_mcmc_system_risk.png`** - MCMC-system correlation plots

### **Data Products**
- **`pca_integrated_analysis.csv`** - Complete merged dataset with PCA components
- **`mcmc_missed_cases_sensitivity_results.json`** - Full MCMC uncertainty analysis
- **State-level prioritization matrices** with multi-method integration

---

## 🚀 **Quick Start Guide**

### **For Complete Multi-Method Analysis**
```bash
# Install enhanced dependencies
pip install -r requirements_v2.txt

# Run comprehensive analysis pipeline
python scripts/21_build_comprehensive_dag_manuscript.py

# View final results
start reports/tb_manuscript_v15_comprehensive_mcmc_pca_dag_final.docx
start output/figures/dag_causal_tb_analysis.png
```

### **For Individual Method Analysis**
```bash
# MCMC Bayesian analysis
python scripts/12_mcmc_bayesian_analysis.py

# PCA analysis
python scripts/18_pca_integrated_analysis.py

# DAG visualization
python scripts/20_dag_causal_analysis.py
```

---

## 📚 **Methodological Contributions**

### **Innovation Highlights**
1. **First MCMC-PCA-DAG Integration** for TB epidemiological analysis
2. **Uncertainty-Aware Causal Inference** through Bayesian-DAG synthesis
3. **Data-Driven Policy Targeting** with multi-dimensional state profiling
4. **Comprehensive Framework** for complex health system evaluation

### **Statistical Rigor**
- **MCMC Convergence**: R-hat < 1.1, ESS > 1,000 across all parameters
- **PCA Validation**: Eigenvalues > 1.0, cumulative variance > 80%
- **DAG Assumptions**: Acyclic, minimal unobserved confounding
- **Cross-Method Validation**: Internal consistency across all three methods

### **Reproducibility**
- **Version Control**: All outputs timestamped and versioned
- **Documentation**: Complete methodological details in all reports
- **Code Modularity**: Independent scripts for each analytical method
- **Data Preservation**: Raw and processed data archived

---

## 🎯 **Impact & Applications**

### **Research Contributions**
- **Methodological Innovation**: Multi-method framework for complex public health phenomena
- **Uncertainty Quantification**: Proper probabilistic bounds for epidemiological estimates
- **Causal Clarity**: DAG-based confounding control in health systems analysis
- **Dimensionality Insights**: PCA reveals true structure of composite health indices

### **Policy Applications**
- **State Targeting**: Component-based resource allocation for TB elimination
- **Intervention Design**: Causal pathway-informed strategy development
- **Monitoring Framework**: Multi-dimensional progress tracking toward End TB targets
- **Risk Communication**: Uncertainty-aware policy recommendations

### **Global Health Implications**
- **Framework Scalability**: Applicable to other diseases (HIV, malaria, COVID-19)
- **LMIC Relevance**: Advanced methods accessible for resource-constrained settings
- **Capacity Building**: Training framework for next-generation health researchers
- **International Standards**: New benchmarks for complex epidemiological analysis

---

## 📋 **File Organization (Complete)**

```
├── scripts/
│   ├── 01-07/          # Original data processing pipeline
│   ├── 12-14/          # MCMC Bayesian analysis
│   ├── 15-17/          # MCMC-system integration
│   ├── 18-19/          # PCA analysis and manuscripts
│   └── 20-21/          # DAG analysis and comprehensive synthesis
├── output/
│   ├── tables/
│   │   ├── pca_integrated_analysis.csv
│   │   └── integrated_mcmc_system_risk.csv
│   └── figures/
│       ├── dag_causal_tb_analysis.png          # DAG visualization
│       ├── pca_vs_traditional_comparison.png   # Comparative analysis
│       ├── pca_analysis_system.png            # System PCA
│       ├── pca_analysis_risk.png              # Risk PCA
│       └── [existing figures]
├── reports/
│   ├── tb_manuscript_v15_comprehensive_mcmc_pca_dag_final.docx
│   ├── dag_causal_analysis_report.md
│   ├── pca_integrated_analysis_report.md
│   ├── integrated_mcmc_system_risk_analysis.md
│   └── README_v4.md (this file)
├── requirements_v2.txt  # Enhanced dependencies
└── data/               # Processed datasets
```

---

## 🔗 **Version History & Evolution**

- **v1.0**: Basic deterministic analysis pipeline
- **v2.0**: Bayesian hierarchical modeling integration
- **v3.0**: PCA-enhanced dimensionality reduction
- **v4.0**: Complete MCMC-PCA-DAG multi-method framework (current)

### **Key Milestones**
- **2024**: Initial system-risk integration (v9)
- **2025**: MCMC Bayesian uncertainty quantification (v12)
- **2025**: PCA data-driven indices (v14)
- **2025**: DAG causal inference and multi-method synthesis (v15)

---

## 📖 **Citation & Usage**

### **Recommended Citations**
```
Complete Multi-Method Framework:
H S Siddalingaiah. Advanced Multi-Method Analysis of Missed Tuberculosis Cases in India:
MCMC Bayesian Estimation, Principal Component Analysis, and Causal Directed Acyclic Graphs. 2025.

DAG Causal Analysis:
H S Siddalingaiah. Causal DAG Analysis of TB Detection Determinants:
System-Risk Interactions with Evidence-Based Link Strengths. 2025.

PCA Enhancement:
H S Siddalingaiah. Principal Component Analysis of TB System-Risk Indices:
Data-Driven Dimensionality Reduction for Epidemiological Modeling. 2025.
```

### **Usage Guidelines**
- Cite WHO, Ni-kshay, NFHS-5, and India TB Report sources
- Use for research, policy analysis, and academic publications
- Contact author for methodological collaborations
- Framework extensible to other health systems and diseases

---

## ⚡ **Technical Specifications**

### **Dependencies**
- **Python 3.8+** with scientific computing stack
- **NetworkX** for graph theory and DAG visualization
- **PyMC** for Bayesian MCMC estimation
- **scikit-learn** for PCA implementation
- **matplotlib/seaborn** for advanced visualizations

### **Computational Requirements**
- **MCMC Sampling**: 2,000 iterations × 4 chains (computationally intensive)
- **PCA Analysis**: Fast linear algebra operations
- **DAG Construction**: Graph theory algorithms
- **Memory**: ~2GB RAM for full pipeline execution

### **Data Requirements**
- State-level TB notifications and cascade indicators
- Socio-demographic risk factor data
- WHO burden estimates for priors
- Compatible with most LMIC health information systems

---

## 🎉 **Achievement Summary**

This repository represents a **state-of-the-art multi-method framework** for TB epidemiological analysis, featuring:

✅ **MCMC Bayesian uncertainty quantification** with proper credible intervals
✅ **PCA dimensionality reduction** revealing true structure of health indices
✅ **DAG causal inference** with evidence-based link strengths
✅ **Complete integration** of all three methods for comprehensive analysis
✅ **Policy-ready outputs** with state-specific intervention strategies
✅ **Publication-quality manuscripts** with embedded professional visualizations
✅ **Reproducible code** with comprehensive documentation
✅ **Scalable framework** applicable to other diseases and health systems

**Impact**: Provides unprecedented insight into India's TB detection determinants, offering clear guidance for achieving WHO End TB Strategy targets by 2030.

---

*This README documents the complete multi-method framework. For earlier versions, see README.md, README_v2.md, and README_v3.md.*