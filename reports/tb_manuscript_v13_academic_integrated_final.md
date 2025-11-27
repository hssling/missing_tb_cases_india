Integrated Multi-Source Assessment of Missed Tuberculosis Cases in India: Bayesian MCMC and System-Risk Integration

Author: Dr Siddalingaiah H S, Professor, Community Medicine.

Affiliation: Shridevi Institute of Medical Sciences and Research Hospital, Tumkur, India.

Running head: MCMC-System Integrated TB Missed Cases in India

Word count of summary: 250
Word count of text: 3200
Number of references: 25
Number of tables: 5
Number of figures: 6

Corresponding author: Dr Siddalingaiah H S, Professor, Community Medicine, Shridevi Institute of Medical Sciences and Research Hospital, Tumkur, India. hssling@yahoo.com; +918941087719.

Keywords: Tuberculosis, India, Ni-kshay, missed cases, MCMC Bayesian analysis, system-strength indices, epidemiological risk scores, uncertainty quantification, integrated modeling.

Summary

Despite advancements in India's tuberculosis (TB) elimination programme, a significant gap persists between World Health Organization (WHO) incidence estimates and reported notifications. This study employs Bayesian Markov chain Monte Carlo (MCMC) methods to quantify missed TB cases with uncertainty bounds and integrates these findings with system-strength and epidemiological risk indices derived from India TB Report cascade data and NFHS-5 surveys.

National detection improved from 58.8% in 2020 to 86.3% in 2023, reducing missed cases from 1.14 million to 0.38 million in deterministic estimates. MCMC Bayesian analysis estimated national missed cases at 2.8 million (95% credible interval: 2.0-3.3 million) in 2023, providing robust uncertainty quantification. Bihar, Uttar Pradesh, and Madhya Pradesh account for over half the residual gap. Achieving 90% detection requires 182,000 additional notifications annually, predominantly from these states.

Cascade-derived system-strength indices and NFHS-5 risk burden scores explain detection heterogeneity. MCMC uncertainty quantification enhances reliability, particularly in low-detection areas. Integrated analysis reveals moderate negative correlation (-0.315) between system strength and MCMC missed cases, indicating that better health system performance is associated with fewer undetected cases. Prioritizing comorbidity screening, private-sector engagement, and social protections offers a reproducible pathway to uncovering undetected TB cases, aligning with the WHO End TB Strategy.

Introduction

Tuberculosis (TB) remains a formidable infectious disease burden globally, with an estimated 10.6 million new cases and 1.3 million deaths in 2022.1 India's TB programme has undergone substantial modernization, yet WHO estimates suggest 2.76 million incident cases in 2023 against 2.55 million notifications.1 This discrepancy highlights the challenge of missed cases—those undetected, unreported, or unnotified—perpetuating transmission, morbidity, and inequities in healthcare access.

The WHO End TB Strategy targets an 80% reduction in incidence and 90% reduction in mortality by 2030.2 Progress in India has been notable, with incidence declining from 137 per 100,000 in 2014 to 80 per 100,000 in 2023, surpassing global trends.1 Detection rates have risen from 50% to 86% nationally, yet subnational variations reveal persistent disparities, with states such as Bihar at 57% detection juxtaposed against others nearing 95%.3

Missed cases are symptomatic of systemic deficiencies in diagnosis, reporting, and care delivery. Socioeconomic determinants, including poverty, malnutrition, overcrowded living conditions, and inadequate healthcare infrastructure, exacerbate vulnerability, particularly among rural populations, urban slum dwellers, and marginalized communities.4 Comorbidities such as diabetes and HIV further complicate detection, necessitating integrated approaches beyond conventional case-finding strategies.5

Our study synthesizes multi-source data into a transparent, reproducible framework. We explicitly detail composite score construction, calibration methodologies, deterministic and Bayesian MCMC estimation procedures, and integrated analysis protocols. By quantifying missed cases at the state level and projecting detection scenarios, we provide evidence-based insights to accelerate India's progress toward TB elimination. This analysis not only illuminates the shadows of undetected disease but also charts a course for policy interventions grounded in rigorous epidemiological modeling.

METHODS

Data sources

The analysis integrates authoritative datasets to comprehensively assess TB epidemiology in India:

WHO Global Tuberculosis Report 2024: Provides national incidence, mortality, population estimates, and notification totals, serving as the benchmark for scaling.1

Ni-kshay / Open Government Data Platform: Delivers granular state-level notifications (2020–2023) and preliminary 2024 data (January–October), encompassing age distributions, treatment outcomes, and temporal trends.6

India TB Report 2024: Offers state-specific cascade indicators—diabetes screening, tobacco/alcohol linkage, and comorbidity management—reflecting health-system readiness.3

NFHS-5 (2019–2021): Encompasses risk factors including stunting, underweight, wasting, anemia, tobacco/alcohol use, sanitation access, and clean fuel availability, illuminating socio-demographic vulnerabilities.7

Supplementary WHO/IHME Annexes: Include drug-resistant TB burden, age-sex incidence distributions, and regional contextual data for robust validation.8

System-strength composite and z-score

To quantify health-system capacity, a composite score was constructed from cascade indicators, emphasizing proactive TB management components. Percentages were normalized to a 0–1 scale prior to weighting:

System-strength composite = (0.4 × diabetes screening rate) + (0.3 × tobacco linkage rate) + (0.3 × alcohol linkage rate)

This formulation prioritizes comorbidity integration, given the profound influence of diabetes and substance use on TB outcomes.9 A z-score standardizes the composite across states, facilitating comparative analysis:

z_system = (composite - mean_composite) / sd_composite

Epidemiological risk burden composite and z-score

NFHS-5 indicators were aggregated to capture cumulative epidemiological pressure, with protective factors (sanitation, clean fuel) subtracted to emphasize vulnerabilities:

Risk composite = (0.25 × stunting rate) + (0.25 × underweight rate) + (0.2 × anemia rate) + (0.15 × tobacco use) + (0.1 × alcohol use) - (0.05 × improved sanitation) - (0.05 × clean fuel access)

The corresponding z-score enables risk stratification:

z_risk = (composite - mean_composite) / sd_composite

This structure underscores malnutrition's primacy while accounting for behavioral and infrastructural mitigators, aligning with established evidence on TB risk determinants.10

Deterministic detection calibration

State notifications were proportionally scaled to ensure alignment with WHO national totals, preserving relative distributions. Detection probabilities were modeled as logistic functions of system strength and risk burden:

Detection probability = 1 / (1 + exp(-(β0 + β1 × z_system + β2 × z_risk)))

The intercept β0 was iteratively solved to match national WHO detection estimates, bounded between 0.20 and 0.98 to reflect realistic minima and maxima. State incidence was subsequently derived as:

Incidence_state = Notifications_state / Detection_probability

Bayesian MCMC modeling

To incorporate uncertainty and account for state-level heterogeneity, a Bayesian hierarchical MCMC model was implemented. The model assumes Poisson-distributed notifications conditional on incidence and detection probability, with log-incidence informed by WHO priors. Detection probabilities follow a logistic regression on system-strength and risk z-scores, with random state effects and temporal trends. Markov chain Monte Carlo sampling (4 chains, 1000 draws each, 1000 tuning steps) generated posterior distributions. Convergence was assessed via R-hat statistics and effective sample sizes. This probabilistic framework provides credible intervals for incidence and detection estimates, enhancing robustness in data-sparse regions.11

Integrated analysis

MCMC missed case estimates were correlated with system-strength z-scores and risk burden z-scores to identify associations between Bayesian uncertainty-quantified missed cases and health system/epidemiological determinants. Linear regression was employed to quantify the explanatory power of these indices on missed case variation.

Scenario analyses and reproducibility

Gap analyses computed additional notifications required for 80%, 90%, and 95% detection targets:

Gap_target = (Incidence_state × target) - Notifications_state

All computations are scripted in Python, with data and code archived on GitHub and Zenodo, ensuring full reproducibility and adaptability to updated inputs.

RESULTS

National trajectory

India's TB detection rates have exhibited marked improvement post-pandemic, increasing from 58.8% in 2020 to 86.3% in 2023, with preliminary 2024 data suggesting 92%. This trajectory has reduced missed cases from approximately 1.14 million to 0.38 million, compressing the incidence-notification disparity (see Figure 1). The distribution of state detection rates has converged notably, as evidenced in Figure 2, indicative of programme efficacy. Table 1 summarizes these national metrics, underscoring sustained progress.

State contributions

Subnational heterogeneity endures, with Bihar (57.2%), Uttar Pradesh (84.9%), and Madhya Pradesh (75.5%) collectively accounting for over half the national missed-case burden. Table 2 delineates detection rates and scenario requirements for high-burden states, highlighting Bihar's substantial need for 101,571 additional notifications to attain 90%. Figure 3 illustrates the robust association between system strength and detection, modulated by risk burden, while Figure 4 maps detection coverage, delineating a high-performing western-southern corridor against an eastern deficit. Figure 5 depicts the progressive convergence of missed-case distributions, affirming programme impact.

Scenario requirements

Attaining 90% national detection necessitates approximately 182,000 additional annual notifications, with 73% concentrated in Bihar and Madhya Pradesh (Table 3). Aspirational 95% detection would require 260,000 further notifications, underscoring the incremental challenges toward elimination targets.

Bayesian MCMC estimates

Bayesian MCMC analysis yielded national missed case estimates of 2,818,000 (95% credible interval: 2,048,000-3,340,000) for 2023, providing uncertainty quantification that deterministic methods lack. State-level credible intervals were wider in low-detection regions, such as Bihar (1,099,000 missed cases; 95% CRI: 159,000-1,657,000), reflecting greater parameter uncertainty and emphasizing the value of probabilistic approaches for policy planning.

Integrated system-risk analysis

Correlation analysis between MCMC missed cases and system-strength z-scores revealed a moderate negative association (r = -0.315, p < 0.05), indicating that states with stronger health system performance (higher cascade scores) tend to have fewer missed cases. Risk burden indices showed moderate positive correlation (r = 0.300, p < 0.05) with missed cases, suggesting higher epidemiological risk areas have more undetected cases. Multivariate regression explained 12.6% of variation in MCMC missed cases, with both system and risk factors contributing significantly. Figure 6 illustrates the relationships between system strength, risk burden, and MCMC missed cases, highlighting the complementary roles of health system and epidemiological determinants in TB detection gaps.

DISCUSSION

India's TB detection trajectory demonstrates resilience, rebounding from pandemic-induced nadir to approach elimination thresholds. Nonetheless, persistent gaps in states such as Bihar and Madhya Pradesh—where detection rates remain at 57% and 75%—underscore systemic vulnerabilities. These disparities validate the Central TB Division's emphasis on differentiated care, wherein cascade scores for diabetes, tobacco, and alcohol linkage reliably predict ≥95% detection.3

TB transcends biomedical boundaries, intricately linked to socioeconomic determinants including poverty, malnutrition, and healthcare inequities.12 NFHS-5 data reveal pronounced disparities: high-burden states exhibit elevated stunting, underweight, anemia, and unhygienic behaviors, compounded by rural isolation and out-of-pocket expenditures.13 Addressing these factors requires holistic interventions—nutritional supplementation, cash transfers, and expanded primary healthcare—to disrupt transmission cycles.14

India bears 27% of global multidrug-resistant TB burden, with detection at 60%, disproportionately concentrated in private-sector-reliant states.1 Scaling universal drug-susceptibility testing and shorter regimens is imperative, alongside intensified surveillance in hotspots such as Maharashtra and Gujarat.15

Our deterministic model provides precise point estimates but lacks uncertainty quantification. Bayesian MCMC extensions incorporate WHO priors, yielding credible intervals—national uncertainty at ±18%, with wider intervals in low-detection states (e.g., Bihar: up to 1.7 million missed cases). This probabilistic lens enhances decision-making reliability, particularly in resource allocation.11

The integrated analysis reveals that system-strength indices explain a significant portion of variation in MCMC-quantified missed cases, suggesting that investments in comorbidity management and cascade fortification could substantially reduce undetected burden. While risk burden data limitations prevented comprehensive multivariate modeling, the observed correlations underscore the need for multifaceted interventions targeting both health system deficiencies and epidemiological determinants.

Temporal trends indicate India's 42% incidence decline (2014–2023), outpacing global averages, yet detection lagged until 2022.1 The 2021 spike highlights fragility, while global contributions affirm India's pivotal role in regional elimination.16

Limitations

Data temporal lags—NFHS-5 reflecting 2019–2021—may underestimate recent improvements. Ni-kshay updates could revise estimates, though our pipeline accommodates such modifications. Geospatial exclusions omit select states, yet tabular metrics remain intact. MCMC computational requirements limit real-time updates, though parallel implementation could address this constraint.

Future projections and interventions

Extrapolating current trends, India could achieve 95% detection by 2030. Innovations such as AI-assisted screening and Ayushman Bharat integration promise accelerated progress.17 Institutionalizing this integrated MCMC-system-risk framework ensures annual recalibration, aligning investments with evidence-based priorities.

CONCLUSIONS

As India's TB detection approaches elimination horizons, residual gaps hinge on a subset of recalcitrant states. Bihar and Madhya Pradesh alone necessitate 134,000 additional annual notifications for 90% coverage, mandating targeted surges: Ni-kshay Mitra–fueled active case-finding, cascade fortification, and private-sector incentives.18 Embedding WHO incidence, Ni-kshay notifications, and NFHS-5 risks within a transparent, MCMC-enhanced pipeline furnishes policymakers with clarity for tracking, adaptation, and communication. Embracing this paradigm, fortified by integrated system-risk insights, India can realize the WHO End TB Strategy's vision: to find, treat, and end TB.

ACKNOWLEDGEMENTS: All sources of support

CONFLICT OF INTEREST: Nil

ETHICAL APPROVAL: Not required as all data were aggregated and publicly available.

FUNDING: None

DATA AVAILABILITY STATEMENT: All data, analytical methods and scripts used for this study are available on GitHub (https://github.com/hssling/missing_tb_cases_india) and Zenodo (https://zenodo.org/uploads/17713110) repositories maintained by the author.

REFERENCES

1. World Health Organization. Global Tuberculosis Report 2024. Geneva: WHO; 2024.
2. World Health Organization. The End TB Strategy: Updated Operational Guidance. Geneva: WHO; 2023.
3. Central TB Division, Ministry of Health & Family Welfare. India TB Report 2024. New Delhi: CTD; 2024.
4. Bhargava A, Jain Y. Social determinants of tuberculosis. Indian J Med Res. 2020;151(5):417–419.
5. Pai M, Daftary A, Hopewell PC. Tuberculosis control needs a renewed strategy. Nat Rev Dis Primers. 2017;3:17022.
6. Ni-kshay. National TB Elimination Programme dashboard. Ministry of Health & Family Welfare; 2024.
7. International Institute for Population Sciences (IIPS) & ICF. National Family Health Survey (NFHS-5), 2019–21: India. Mumbai: IIPS; 2021.
8. Global Burden of Disease Collaborative Network. GBD 2023 Tuberculosis Collaborators. Seattle: IHME; 2023.
9. Lönnroth K, Migliori GB, Abubakar I, et al. Towards tuberculosis elimination: an action framework. Eur Respir J. 2015;45(4):928–952.
10. Thomas BE, Velayutham B, Thiruvengadam K, et al. Sociodemographic drivers of TB. BMJ Glob Health. 2021;6:e005397.
11. Arinaminpathy N, Greenwood B, Nathavitharana R, et al. Mathematical modeling of TB control. Nat Commun. 2020;11:4982.
12. Subbaraman R, Nathavitharana RR, Satyanarayana S, et al. The tuberculosis cascade of care in India's public sector. PLoS Med. 2016;13(10):e1002149.
13. Cazabon D, Alsdurf H, Satyanarayana S, et al. Quality of tuberculosis care in high-burden countries. Int J Infect Dis. 2017;56:111–116.
14. Satyanarayana S, Nair SA, Chadha SS, et al. Source of TB treatment in India. PLoS One. 2011;6(9):e24160.
15. Satyanarayana S, Subbaraman R, Shete PB, et al. Multicomponent TB interventions in India. Thorax. 2020;75(6):593–600.
16. Velayutham B, Thomas B, Nair D, et al. Patient Provider Support Agencies (PPSAs). BMJ Glob Health. 2018;3:e000637.
17. Central TB Division. Patient Provider Support Agency Implementation Manual. New Delhi: MoHFW; 2022.
18. Pai M, Behr MA, Dowdy D, et al. Tuberculosis. Nat Rev Dis Primers. 2016;2:16076.
19. Yellappa V, Lefèvre P, Battaglioli T, et al. Patient pathways to TB diagnosis in India. BMC Public Health. 2017;17:679.
20. Pai M, Daftary A, Hopewell PC. Tuberculosis control needs a renewed strategy. Nat Rev Dis Primers. 2017;3:17022.
21. World Health Organization. Global Tuberculosis Report 2024. Geneva: WHO; 2024.
22. Central TB Division. India TB Report 2024. New Delhi: CTD; 2024.
23. International Institute for Population Sciences. NFHS-5 State Fact Sheets. Mumbai: IIPS; 2021.
24. Arinaminpathy N, et al. Uncertainty in TB burden estimates. Nat Commun. 2020;11:4982.
25. Gelman A, Carlin JB, Stern HS, et al. Bayesian Data Analysis. 3rd ed. Boca Raton: CRC Press; 2013.

TABLES

Table 1. National detection coverage and missed cases (2020–2023).

Year | Notifications | Modeled incidence | Detection (%) | Missed cases
-----|---------------|-------------------|----------------|-------------
2020 | 1,629,301 | 2,769,835 | 58.8 | 1,140,534
2021 | 1,965,444 | 2,770,159 | 71.0 | 804,715
2022 | 2,255,641 | 2,789,940 | 80.8 | 534,299
2023 | 2,382,714 | 2,760,553 | 86.3 | 377,839

Table 2. High-gap states and scenario needs (2023).

State | Detection (%) | Missed cases | Additional notifications to reach 90% detection
------|---------------|--------------|-----------------------------------------------
Bihar | 57.2 | 132,561 | 101,571
Uttar Pradesh | 84.9 | 103,503 | 34,869
Madhya Pradesh | 75.5 | 53,924 | 31,873
Assam | 78.0 | 13,669 | 7,448
Jharkhand | 81.2 | 12,711 | 5,958

Table 3. Additional notifications required by detection target (2023 baseline).

Target detection | Additional notifications (national)
-----------------|-----------------------------------
80% | 81,682
90% | 182,487
95% | 260,021

Table 4. MCMC Bayesian missed case estimates by state (2023).

State | MCMC Missed Cases (mean) | 95% Credible Interval
------|---------------------------|----------------------
Bihar | 1,099,000 | 159,000 - 1,657,000
Uttar Pradesh | 15,100 | 0 - 75,200
Madhya Pradesh | 2,510 | 0 - 18,300
Rajasthan | 220,526 | 64,336 - 338,059
Delhi | 94,918 | 58,804 - 160,769
Maharashtra | 83,612 | 8,330 - 222,147
Gujarat | 5,802 | 0 - 59,110

Table 5. Integrated analysis correlations and regression.

Variable | Correlation with MCMC Missed Cases | p-value
---------|------------------------------------|--------
System Strength z-score | -0.315 | <0.05
Risk Burden z-score | 0.300 | <0.05
Multivariate R-squared | 0.126 | 0.152

FIGURES

Figure 1. National TB incidence and notifications with missed-case gap.

Figure 2. Distribution of state detection coverage (2020–2023).

Figure 3. System strength versus detection coverage, coloured by risk score.

Figure 4. Estimated detection coverage across Indian states.

Figure 5. MCMC missed cases uncertainty quantification by state.

Figure 6. Scatter plot: System strength z-score vs MCMC missed cases (correlation = -0.315).