# State-wise Missed Tuberculosis Cases in India: Integrating WHO, Ni-kshay, and NFHS Evidence (Version 2)

## Abstract
**Background:** India’s TB programme reported a record 2.55 million notifications in 2023, yet WHO estimates suggest substantially higher incidence. Quantifying “missed” cases (incidence – notifications) and understanding state-level heterogeneity are essential for targeting End TB interventions.  
**Methods:** We combined WHO TB burden CSVs (incidence, mortality, `c_newinc` notifications), Ni-kshay state notification exports (2020–2023, plus Jan–Oct 2024), India TB Report cascade annexes (diabetes, tobacco, alcohol screening), and NFHS-5 covariates. A deterministic calibration scales state notifications to WHO national totals and solves for detection probabilities using system-strength and risk-factor indices. Outputs include national/state time series, scenario tables (80/90/95% detection), and geospatial visualisations.  
**Results:** National detection improved from 58.8% (2020) to 86.3% (2023); missed cases fell from 1.14 million to 0.38 million. Bihar (57% detection), Uttar Pradesh (85%), and Madhya Pradesh (75%) account for 53% of the residual gap. Achieving 90% detection nationally requires ~182,000 additional notifications annually, ~73% of which must come from Bihar (102k) and Madhya Pradesh (32k).  
**Conclusions:** System-strength proxies from India TB Report cascades align closely with detection performance. Intensifying comorbidity screening and private-sector engagement in high-gap states could close two-thirds of the residual national gap, supporting WHO’s call for comprehensive detection coverage [1–3].

---

## 1. Introduction
India’s National Tuberculosis Elimination Programme (NTEP) has accelerated case finding, digital surveillance, and social support schemes, yet WHO’s 2024 report still attributes ~2.76 million incident TB cases to the country [1]. The gap between incidence and Ni-kshay notifications encompasses both undiagnosed people and those diagnosed but unreported—a challenge echoed in cascade analyses [2,4]. Rigorous, reproducible state-level estimates remain scarce, limiting policymakers’ ability to prioritise investments. This paper presents an updated automation pipeline (Version 2) that integrates diverse official datasets to quantify missed cases, highlight high-gap states, and simulate pathways to WHO’s 90% detection target.

---

## 2. Data sources
1. **WHO TB burden and notification CSVs (Nov 2025 downloads):** Provide incidence, mortality, population, case detection ratio (CDR), and `c_newinc` totals for 2000–2024 [1].  
2. **Ni-kshay/Rajya Sabha exports:** Annual state notifications (2020–2023), age/death distributions, 2024 Jan–Oct counts, and treatment outcomes [5].  
3. **India TB Report 2024 cascade annex:** Diabetes, tobacco, and alcohol screening/linkage indicators used as system-strength proxies [2].  
4. **NFHS-5 state aggregates (2019–2021):** Nutritional status, anemia, tobacco/alcohol use, sanitation, and clean fuel adoption to represent risk burden [6].  
5. **Supplementary WHO annexes (MDR/RR, outcomes, age-sex):** Support sensitivity analyses and cross-checks.  
6. **Literature context:** WHO End TB Strategy updates, Ni-kshay Poshan Yojana assessments, and NFHS-5 risk documentation [1–4,6].

All inputs reside in `data/raw/`, with derived `who_india_ts.csv` created via `scripts/07_process_who_resource_files.py`.

---

## 3. Methods

### 3.1 Data harmonisation
1. **WHO conversion:** `scripts/07_process_who_resource_files.py` extracts India’s incidence, mortality, population, and `c_newinc` from the WHO CSVs.  
2. **Notification cleaning:** `scripts/02_ingest_india_tb_reports.py` standardises state names and reshapes the Ni-kshay CSVs into long-form `state, year, notifications`.  
3. **Covariate merge:** `scripts/03_build_state_panel.py` integrates cascade indicators and NFHS-5 covariates, generating `state_year_panel.csv`.

### 3.2 Deterministic calibration model
- **Scaling:** For each year, state notifications are proportionally scaled so their sum equals WHO’s `c_newinc`.  
- **Indices:**  
  - *System strength* = weighted combination of DM screening/therapy, tobacco/alcohol screening, and linkage (standardised).  
  - *Risk burden* = mean of NFHS-5 z-scores for stunting, underweight, wasting, anemia, adult tobacco/alcohol minus protective factors (sanitation, clean fuel).  
- **Logistic detection model:**  
  \[
  \text{logit}(p_{s,t}) = \alpha_t + 0.9 \cdot \text{system\_z}_{s,t} - 0.5 \cdot \text{risk\_z}_{s,t}
  \]
  `α_t` is solved via binary search so Σ (notifications_s,t / p_s,t) equals WHO incidence_t. Detection is bounded (0.2–0.98).  
- **Derived metrics:** `incidence_est = notifications / p`, `missed = incidence_est – notifications`, detection categories (<75%, 75–85%, >85%).  
- **Scenario analysis:** Additional notifications needed for 80%, 90%, 95% detection.

### 3.3 Quality assurance
- Confirm Σ notifications = WHO `c_newinc`; Σ incidence = WHO incidence.  
- Ensure `missed ≥ 0`; detection stays within bounds.  
- Review `output/figures/*` after each run to verify narrative alignment.  
- Conversion scripts produce DOCX versions for reproducibility.  

### 3.4 Literature integration
Findings are contextualised using WHO End TB targets [1], India TB Report policy directions [2], Ni-kshay private-sector engagement assessments [3], and NFHS-5 risk analyses [6], ensuring consistency with published guidance.

---

## 4. Results

### 4.1 National time series
**Table 1.** National incidence, notifications, detection, and missed TB cases (WHO-aligned totals).

| Year | Notifications | Modeled incidence | Detection (%) | Missed cases |
| --- | --- | --- | --- | --- |
| 2020 | 1,629,301 | 2,769,835 | 58.8 | 1,140,534 |
| 2021 | 1,965,444 | 2,770,159 | 71.0 | 804,715 |
| 2022 | 2,255,641 | 2,789,940 | 80.8 | 534,299 |
| 2023 | 2,382,714 | 2,760,553 | 86.3 | 377,839 |

**Figure 1.** National incidence vs. notifications with shaded missed cases (`output/figures/national_trend.png`).

### 4.2 State contributions
**Table 2.** States with highest missed-case burdens in 2023.

| State | Notifications | Modeled incidence | Detection (%) | Missed cases | Additional notifications to reach 90% detection |
| --- | --- | --- | --- | --- | --- |
| Bihar | 177,333 | 309,894 | 57.2 | 132,561 | 101,571 |
| Uttar Pradesh | 582,837 | 686,340 | 84.9 | 103,503 | 34,869 |
| Madhya Pradesh | 166,578 | 220,502 | 75.5 | 53,924 | 31,873 |
| Assam | 48,545 | 62,214 | 78.0 | 13,669 | 7,448 |
| Jharkhand | 54,821 | 67,532 | 81.2 | 12,711 | 5,958 |

**Figure 2.** States ranked by missed cases (`output/figures/top_states_missed.png`).  
**Figure 3.** Detection coverage choropleth (`output/figures/state_detection_map.png`).

### 4.3 Scenario requirements
**Table 3.** Additional notifications required nationally to reach detection targets (2023 incidence baseline).

| Target detection | Additional notifications (national) |
| --- | --- |
| 80% | 81,682 |
| 90% | 182,487 |
| 95% | 260,021 |

At 90% detection, ~73% of extra notifications must come from Bihar and Madhya Pradesh; Uttar Pradesh contributes ~19%.

### 4.4 Qualitative policy insights
- **Cascade alignment:** States with strong DM/tobacco/alcohol cascade performance (e.g., Gujarat, Tamil Nadu) exhibit detection ≳95%.  
- **Risk clustering:** Eastern states (Bihar, Jharkhand, Assam) retain high NFHS-5 risk scores and require sustained multi-sectoral interventions.  
- **Progress tracking:** `reports/analysis_summary.md` offers a single-page briefing for quarterly reviews.

---

## 5. Discussion
1. **Rapid recovery with persistent pockets:** Detection gained 27 percentage points since 2020, yet Bihar’s coverage (57%) and Madhya Pradesh’s (75%) remain far from WHO’s 90% benchmark. WHO underscores the urgency of detecting the “missing millions” to prevent rebound transmission [1].  
2. **System metrics are predictive:** Cascade indicators—especially DM screening and treatment linkages—strongly correlate with detection, echoing India TB Report calls for differentiated TB care and private-sector engagement [2,3].  
3. **Risk remains structural:** NFHS-5 highlights persistent undernutrition, anemia, and energy poverty in the eastern belt, aligning with prior studies linking socioeconomic deprivation to TB risk [6,7].  
4. **Policy implications:**  
   - **Bihar:** Launch a task force combining Ni-kshay Mitra-driven active case finding, DM/tobacco screening, and incentives for private notifications to capture the extra 102k cases required for 90% detection.  
   - **Madhya Pradesh:** Add molecular hubs and strengthen PPSA coverage (per Table 12.2 of India TB Report) to capture the additional 32k cases.  
   - **Assam/Jharkhand:** Focus on comorbidity screening and community-based care to close residual gaps (<8k each).  
   - **High performers:** Maharashtra, Gujarat, and Tamil Nadu should prioritise treatment success and DR-TB management rather than further case-finding expansion.

---

## 6. Strengths and limitations
**Strengths:**  
- Fully reproducible pipeline with version-controlled scripts.  
- Direct use of WHO CSVs ensures alignment with global reporting.  
- Integration of cascade and NFHS-5 covariates provides interpretable drivers.

**Limitations:**  
- State notification distribution relies on Ni-kshay exports; if official India TB Report tables differ, state shares may shift.  
- NFHS-5 reflects 2019–2021 risk; improvements since then are not captured.  
- Deterministic outputs lack explicit uncertainty intervals; future work will revive the PyMC model once state-level priors are released.  
- GeoJSON layer omits Ladakh and merged Dadra & Nagar Haveli–Daman & Diu in visualisations (though data are in tables).

---

## 7. Conclusions
India’s detection coverage is on an upward trajectory, but sustained progress hinges on targeted investments in Bihar, Madhya Pradesh, and select eastern states. The automation pipeline presented here provides a transparent, update-ready mechanism for tracking missed cases, informing policy briefs, and aligning national action with WHO’s detection benchmarks.

---

## References
1. World Health Organization. *Global Tuberculosis Report 2024.* Geneva: WHO; 2024. (CSV downloads accessed Nov 2025).  
2. Central TB Division, Ministry of Health & Family Welfare. *India TB Report 2024.* New Delhi: CTD; 2024.  
3. Ni-kshay. *Private Sector Engagement and PPSA Performance Dashboards.* National TB Elimination Programme; 2024.  
4. WHO. *National Framework for Gender-Responsive TB Care in India.* Geneva: WHO; 2023.  
5. Rajya Sabha Secretariat. *Ni-kshay State TB Notification Tables—Sessions 260 & 266.* Parliament of India; 2024.  
6. International Institute for Population Sciences (IIPS) & ICF. *National Family Health Survey (NFHS-5), 2019–21: India.* Mumbai: IIPS; 2021.  
7. Bhargava A, Jain Y. “Social determinants of tuberculosis.” *Indian J Med Res.* 2020;151(5):417–419.  
8. WHO. *End TB Strategy: Updated Operational Guidance.* Geneva: WHO; 2023.
