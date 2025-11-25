# Protocol: State-wise Missed Tuberculosis Cases in India

## Title
State-wise missed tuberculosis cases in India: an automated multi-source modelling study using WHO, Ni-kshay, and prevalence survey data

## Background & Rationale
India contributes the largest absolute number of tuberculosis (TB) cases worldwide. Despite expansion of molecular diagnostics and the Ni-kshay electronic notification platform, a sizeable proportion of incident TB remains undiagnosed or unreported every year. Quantifying this “missed” burden, understanding its drivers, and tracking state-level progress toward WHO’s 90% detection benchmark are essential for achieving India’s End TB 2025 targets. Multiple official datasets now exist (WHO TB burden CSVs, state notification tables, NFHS-5 risk indicators, the National TB Prevalence Survey), but a unified, reproducible pipeline that synthesizes them is still lacking.

## Aim
To build an automated surveillance and modelling system that estimates annual missed TB cases for each Indian state/UT, partitions gaps into under-diagnosis vs. under-reporting, and evaluates scenario trajectories against national and global detection targets.

## Specific Objectives
1. Assemble a 2015–2024 state-year dataset combining WHO incidence and notification series, India TB Report/Ni-kshay state notifications, and socio-demographic covariates.
2. Derive priors on detection probability from literature (inventory/capture–recapture studies and the National TB Prevalence Survey care cascade).
3. Fit deterministic and (optionally) Bayesian models for state-level incidence and notification processes to obtain missed-case estimates with uncertainty.
4. Classify states into low, moderate, and high missed-case categories and explore predictors (private sector share, poverty, lab density, risk-factor burden).
5. Generate policy scenarios estimating the additional notifications required for each state to reach 80%, 90%, and 95% detection coverage.

## Data Sources
- **WHO TB burden CSV (2025 extract):** Provides national incidence, mortality, population, and case detection ratio (`who_india_ts.csv`).
- **WHO TB notifications CSV (2025 extract):** Supplies national `c_newinc` totals used to scale state notifications annually.
- **Ni-kshay / India TB Reports:** Annual state-wise notifications, age/death distributions, treatment outcomes, and private/public splits.
- **National TB Prevalence Survey 2019–2021:** Bacteriological prevalence, care cascade transitions (symptom recognition → care seeking → testing → diagnosis → registration).
- **NFHS-5 (2019–21):** State-level indicators for malnutrition, anemia, tobacco/alcohol use, sanitation, and clean cooking.
- **Census 2011 / socio-economic datasets:** Population denominators, urbanization, literacy, poverty proxies (optional).
- **Literature-derived priors:** Inventory studies, capture–recapture analyses, and cascade modelling papers collected via scripts/00_lit_search.py.

## Study Design & Methods
- **Design:** Secondary data modelling and evidence synthesis.
- **Scale:** India, state/UT level, annual (initially 2020–2023 with option to extend).
- **Core indicators:** `incidence_est`, `notifications`, `missed`, `detection_cov`, `under_diagnosis`, `diagnosed_not_notified`.

### Analytical Strategy
1. **Data engineering:** Scripts standardize state names, align calendar years, and merge covariates into a unified panel (`state_year_panel.csv`).
2. **System-strength & risk indices:** Cascade indicators (DM/Tobacco/Alcohol) and NFHS-5 variables are converted to standardized indices used to inform detection probabilities.
3. **Calibration model:** Deterministic logistic calibration treats incidence as fixed by WHO estimates, scales state notifications to WHO `c_newinc`, and solves for detection probabilities `p_s,t`.
4. **Bayesian extension (optional):** scripts/04_fit_bayesian_model.py can be activated once state-level incidence priors are released, producing posterior draws stored in `models/`.
5. **Scenario modelling:** For each state-year, compute incremental notifications required to reach 80/90/95% detection coverage, feeding dashboards and policy briefs.

## Outputs & Dissemination
- `output/tables/state_detection_panel.csv` – state-year incidence, detection, and missed-case estimates.
- `output/tables/state_detection_scenarios.csv` – incremental notifications required by scenario.
- `output/figures/*` – national trends, top-state bar charts, and detection choropleths.
- `reports/analysis_summary.md` and `reports/tb_manuscript.md` – living documents for policymakers and journals.

## Limitations & Risk Mitigation
- **Data availability:** Some state-level incidence priors (indigenous burden model) remain unpublished; WHO national totals are used as constraints and the model flags gaps.
- **Notification completeness:** Rajya Sabha/Ni-kshay CSVs omit certain providers; scaling to WHO’s `c_newinc` totals reduces but does not eliminate bias.
- **Temporal mismatch:** NFHS-5 indicators represent 2019–21 conditions; scenario analyses are rerunnable as new NFHS waves emerge.
- **Geo coverage:** Available GeoJSON excludes Ladakh and the merged Dadra & Nagar Haveli–Daman & Diu UT; these jurisdictions are treated separately in tables but not maps.

## Ethical Considerations
All data are aggregated, publicly available, or officially published. No individual-level identifiers are processed. Analyses align with public health surveillance objectives and use only secondary data.
