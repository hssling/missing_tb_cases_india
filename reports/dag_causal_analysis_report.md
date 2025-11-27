
# Causal DAG Analysis: TB Missed Cases System-Risk Interactions

## Overview
This Directed Acyclic Graph (DAG) represents the causal relationships between health system factors, epidemiological risk factors, and TB detection outcomes. The DAG provides a framework for understanding intervention pathways and identifying confounding relationships.

## DAG Structure

### Node Categories (26 total nodes)

**Exogenous Factors** (4 nodes):
Root causes that influence both system capacity and risk burden:
- Socioeconomic Status
- Geographic Isolation
- Population Density
- Healthcare Infrastructure

**Health System Factors** (6 nodes):
Interventions and capacities that affect detection probability:
- Diabetes Screening Capacity
- Tobacco Linkage Systems
- Alcohol Deaddiction Services
- Laboratory Network
- Healthcare Workforce
- Supply Chain Efficiency

**Risk Factors** (6 nodes):
Epidemiological determinants that increase TB incidence:
- Malnutrition Prevalence
- Substance Use Rates
- Comorbidity Burden
- Poverty Level
- Sanitation Access
- Clean Fuel Access

**Intermediate Factors** (5 nodes):
Mechanistic variables in the causal pathway:
- True Incidence Rate
- Detection Probability
- Notification Rate
- Treatment Initiation
- Treatment Completion

**Outcome Variables** (5 nodes):
Final health and economic impacts:
- Reported Cases
- Missed Cases
- Transmission Rate
- Mortality Rate
- Economic Burden

## Key Causal Pathways

### Primary Intervention Pathways
1. **System Strengthening → Detection → Reduced Missed Cases**
   - Healthcare_Infrastructure -> Laboratory_Network -> Detection_Probability -> Missed_Cases DOWN
   - Diabetes_Screening_Capacity -> Detection_Probability -> Reported_Cases UP

2. **Risk Mitigation → Incidence Reduction**
   - Socioeconomic_Status -> Malnutrition_Prevalence DOWN -> True_Incidence_Rate DOWN
   - Poverty_Level -> Substance_Use_Rates DOWN -> True_Incidence_Rate DOWN

### Confounding Relationships
- **Socioeconomic_Status** affects both Healthcare_Infrastructure and Poverty_Level
- **Geographic_Isolation** influences both Healthcare_Infrastructure and Sanitation_Access
- These confounders must be controlled for in statistical analyses

## Evidence Strength Classification

### Strong Evidence Links (19 links)
Well-established causal relationships supported by multiple studies:
- Socioeconomic Status -> Healthcare Infrastructure
- Socioeconomic Status -> Healthcare Workforce
- Socioeconomic Status -> Malnutrition Prevalence
- Socioeconomic Status -> Poverty Level
- Diabetes Screening Capacity -> Detection Probability
- Laboratory Network -> Detection Probability
- Healthcare Workforce -> Detection Probability
- Supply Chain Efficiency -> Treatment Initiation
- Malnutrition Prevalence -> True Incidence Rate
- Comorbidity Burden -> True Incidence Rate
- True Incidence Rate -> Reported Cases
- Detection Probability -> Reported Cases
- Detection Probability -> Notification Rate
- Notification Rate -> Treatment Initiation
- Treatment Initiation -> Treatment Completion
- True Incidence Rate -> Missed Cases
- Detection Probability -> Missed Cases
- Missed Cases -> Transmission Rate
- Treatment Completion -> Mortality Rate

### Moderate Evidence Links (14 links)
Supported by epidemiological studies but may have alternative explanations:
- Geographic Isolation -> Healthcare Infrastructure
- Population Density -> Laboratory Network
- Socioeconomic Status -> Substance Use Rates
- Geographic Isolation -> Sanitation Access
- Geographic Isolation -> Clean Fuel Access
- Tobacco Linkage Systems -> Detection Probability
- Alcohol Deaddiction Services -> Detection Probability
- Supply Chain Efficiency -> Treatment Completion
- Substance Use Rates -> True Incidence Rate
- Poverty Level -> True Incidence Rate
- Poverty Level -> Healthcare Infrastructure
- Reported Cases -> Transmission Rate
- Transmission Rate -> Economic Burden
- Mortality Rate -> Economic Burden

### Weak Evidence Links (3 links)
Hypothesized relationships requiring further investigation:
- Sanitation Access -> True Incidence Rate
- Clean Fuel Access -> True Incidence Rate
- Malnutrition Prevalence -> Healthcare Workforce

## Statistical Implications

### Variables Requiring Control
When analyzing the effect of system interventions on detection:
- Control for: Socioeconomic_Status, Geographic_Isolation
- These variables confound the system → detection relationship

### Mediation Analysis Opportunities
- **Detection_Probability** mediates the effect of system factors on Missed_Cases
- **True_Incidence_Rate** mediates the effect of risk factors on Transmission_Rate
- **Treatment_Completion** mediates the effect of system factors on Mortality_Rate

### Collider Bias Considerations
- **Reported_Cases** is a collider between True_Incidence_Rate and Detection_Probability
- Conditioning on Reported_Cases may induce spurious associations

## Policy Intervention Pathways

### Direct Interventions (Strong Evidence)
1. **Laboratory Network Expansion** -> Detection_Probability UP -> Missed_Cases DOWN
2. **Diabetes Screening Scale-up** -> Detection_Probability UP -> Reported_Cases UP
3. **Supply Chain Strengthening** -> Treatment_Initiation UP -> Treatment_Completion UP

### Upstream Interventions (Moderate Evidence)
1. **Socioeconomic Development** -> Healthcare_Infrastructure UP -> System Factors UP
2. **Nutrition Programs** -> Malnutrition_Prevalence DOWN -> True_Incidence_Rate DOWN
3. **Sanitation Improvements** -> True_Incidence_Rate DOWN -> Transmission_Rate DOWN

### Combined Strategies (System + Risk Integration)
- **High System Capacity + High Risk Areas**: Focus on detection + prevention
- **Low System Capacity + Low Risk Areas**: Build system capacity first
- **Moderate Combinations**: Balanced system strengthening + risk mitigation

## DAG Validation and Sensitivity

### Structural Assumptions
1. **No cycles**: All relationships are acyclic (no feedback loops)
2. **No unobserved confounding**: All common causes are included
3. **Correct direction**: Arrows represent true causal direction
4. **Sufficiency**: All relevant variables are represented

### Sensitivity to Missing Variables
- **Genetic Factors**: Not included (minimal TB heritability)
- **Climate Factors**: Not included (secondary importance)
- **Migration Patterns**: Not included (could be additional confounder)

## Applications for Analysis

### Regression Model Specification
```python
# Corrected model controlling for confounders
missed_cases ~ system_factors + risk_factors + socioeconomic_status + geographic_isolation

# Mediation analysis
detection_prob ~ system_factors
missed_cases ~ detection_prob + system_factors  # Detection as mediator
```

### PCA Interpretation Through DAG
- **System PC1**: Captures overall system capacity pathway
- **System PC2**: Represents comorbidity intervention specialization
- **Risk PC1**: Nutritional vulnerability pathway
- **Risk PC2**: Substance use behavioral pathway

## Conclusion

This DAG provides a comprehensive causal framework for understanding TB detection determinants in India. The graph highlights:

1. **Multiple intervention pathways** from system strengthening to improved outcomes
2. **Complex confounding structures** requiring careful statistical control
3. **Opportunities for mediation analysis** to understand mechanism-specific effects
4. **Policy targeting guidance** based on causal pathway strength

The DAG serves as both a conceptual model for understanding TB epidemiology and a practical guide for designing effective intervention strategies.

## References
- Greenland S, et al. Causal diagrams for epidemiologic research. Epidemiology. 1999
- Hernán MA, Robins JM. Causal Inference: What If. Boca Raton: Chapman & Hall; 2020
- Pearl J. Causality: Models, Reasoning, and Inference. Cambridge University Press; 2009

---
*DAG Analysis generated on 2025-11-27 11:07:57*
*Evidence strength based on WHO TB reports, systematic reviews, and epidemiological studies*
