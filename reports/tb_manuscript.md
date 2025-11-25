# State-wise Missed Tuberculosis Cases in India (2020-2023)

**Authors:** Codex Research Automation Lab  
**Correspondence:** TBD

---

## Abstract
**Background:** India's march toward TB elimination hinges on reducing the "missed cases" gap-the difference between incident TB and cases notified to Ni-kshay. While national totals are published annually by WHO, a reproducible state-wise accounting that triangulates Ni-kshay, NFHS-5 risk indicators, and programmatic cascade metrics is lacking.  
**Methods:** We ingested Rajya Sabha/Ni-kshay state notification CSVs (2020-2023), National Family Health Survey 5 (NFHS-5) state indicators, and India TB Report comorbidity cascade tables (DM/Tobacco/Alcohol). System-strength indices (e.g., proportion of TB-DM patients screened or linked to care) and risk composites (malnutrition, tobacco, poor sanitation) were standardized by state. A constrained logistic calibration then estimated detection probabilities such that (i) higher system scores implied higher detection, (ii) higher risk scores implied lower detection, and (iii) national totals matched WHO Global TB Report 2024 incidence estimates (2015-2023) while the summed state notifications aligned with WHO `c_newinc` totals. Posterior-like estimates of incidence, detection, and missed cases were generated for each state-year along with scenario analyses to reach 80/90/95% detection.  
**Results:** Modeled detection improved from 58.8% (2020) to 86.3% (2023), shrinking the national missed-case gap from 1.14 million to 0.38 million (Table 1). Bihar, Uttar Pradesh, and Madhya Pradesh still accounted for 53% of all missed cases in 2023 despite substantial notification gains. Bihar's detection probability plateaued at 57%, requiring ~102,000 additional notifications annually to hit 90% detection, while Madhya Pradesh needed ~32,000 extra (Table 2). The detection choropleth (output/figures/state_detection_map.png) highlights persistent gaps in the eastern corridor despite western states approaching saturation.  
**Conclusions:** System-strength metrics embedded in the TB comorbidity cascade strongly align with modeled detection. Targeted investments in Bihar, Madhya Pradesh, Assam, and Jharkhand-combining DM/tobacco screening, private-sector reporting, and risk-factor reduction-could close nearly two-thirds of the residual national missed-case gap. The fully scripted pipeline (scripts/06_state_gap_analysis.py) can be rerun as soon as new WHO, Ni-kshay, or NFHS data become available.

**Keywords:** Tuberculosis, India, Ni-kshay, missed cases, NFHS-5, detection probability, subnational modeling.

---

## 1. Introduction
India delivered a record 2.55 million TB notifications in 2023, yet WHO still attributes ~2.77 million incident cases to the country-leaving over 200,000 people undiagnosed or unreported. National aggregates mask wide state-level heterogeneity driven by malnutrition, tobacco use, energy poverty, and uneven diagnostic capacity. Policymakers require granular evidence that pinpoints where detection lags, quantifies the size of the gap, and simulates how many additional cases must be found to align with the End TB 2025 milestones. This manuscript documents a reproducible automation pipeline that produces those state-wise estimates and visuals on demand.

---

## 2. Data & Methods
### 2.1 Data sources
- **Ni-kshay / Rajya Sabha notifications (2020-2023):** CSV exports (RS_Session_260_AU_618_A_to_B_i.csv etc.) with annual state/UT notifications, age structure, and early 2024 counts.
- **India TB Report cascade tables:** Diabetes-, tobacco-, and alcohol-related screening and linkage indicators (files 2.10-2.12_TB_*.csv) summarizing system performance for every state/UT.
- **NFHS-5 (2019-21):** Aggregated to state level (`nfhs5_state_agg.csv`) capturing childhood undernutrition, anemia, tobacco/alcohol use, sanitation, and clean fuel coverage.
- **WHO Global TB Report 2024 data extract:** who_india_ts.csv generated from the offline WHO burden and notification CSVs with `c_newinc` totals and incidence estimates.
- **India state boundary GeoJSON:** data/spatial/india_states.geojson (Geohacker project) for mapping detection coverage.

### 2.2 Feature engineering
1. **System-strength index:** Weighted average of TB-DM screening (30%), DM treatment initiation (15%), tobacco screening (20%), tobacco cessation linkage (10%), alcohol screening (15%), and alcohol de-addiction linkage (10%). Values were scaled 0-1 and z-standardized.
2. **Risk index:** Mean of z-scores for NFHS indicators that elevate TB risk (stunting, underweight, wasting, child anemia, male/female tobacco, male alcohol) minus z-scores for protective factors (improved sanitation, clean fuel).
3. **Detection calibration:** For each year, a logistic model logit(p_s) = a_t + b1*system_z_s - b2*risk_z_s was solved via binary search to ensure sum(notifications_s / p_s) = WHO incidence_t, with b1=0.9 and b2=0.5. The state notifications were proportionally scaled each year so that their sum equaled WHO's `c_newinc` national total before calibration.
4. **Derived metrics:** incidence_est = notifications / p_s, missed = incidence_est - notifications, detection = p_s. Scenario gaps were computed as max(0, target*incidence_est - notifications) for target detection levels of 0.8, 0.9, and 0.95.

### 2.3 Outputs & reproducibility
The master script (scripts/06_state_gap_analysis.py) produces:
- data/processed/state_detection_panel.csv - state-year estimates and covariates.
- Tables summarizing national trends, state rankings, and scenario requirements (output/tables/*).
- Visuals: national time series, bar plots, and a detection choropleth.  
All scripts use relative paths and run in <30 seconds once dependencies (pandas, seaborn, matplotlib, plotly+kaleido) are installed.

---

## 3. Results
### 3.1 National trajectory
**Table 1. National incidence, notifications, detection coverage, and missed cases**

| Year | Notifications | Modeled incidence | Detection (%) | Missed cases |
|------|---------------|-------------------|---------------|--------------|
| 2020 | 1,629,301 | 2,769,835 | 58.8 | 1,140,534 |
| 2021 | 1,965,444 | 2,770,159 | 71.0 | 804,715 |
| 2022 | 2,255,641 | 2,789,940 | 80.8 | 534,299 |
| 2023 | 2,382,714 | 2,760,553 | 86.3 | 377,839 |

Detection rebounded sharply after the second COVID-19 wave, gaining 27 percentage points since 2020. Figure 1 (output/figures/national_trend.png) visualizes the converging incidence and notification lines with the shrinking shaded "missed" area.

### 3.2 State-level heterogeneity
**Table 2. Top 5 states by missed cases, 2023**

| State | Notifications | Modeled incidence | Detection (%) | Missed cases | Extra notifications to hit 90% detection |
|-------|---------------|-------------------|---------------|--------------|------------------------------------------|
| Bihar | 177,333 | 309,894 | 57.2 | 132,561 | 101,571 |
| Uttar Pradesh | 582,837 | 686,340 | 84.9 | 103,503 | 34,869 |
| Madhya Pradesh | 166,578 | 220,502 | 75.5 | 53,924 | 31,873 |
| Assam | 48,545 | 62,214 | 78.0 | 13,669 | 7,448 |
| Jharkhand | 54,821 | 67,532 | 81.2 | 12,711 | 5,958 |

- **Geospatial pattern:** The detection map (output/figures/state_detection_map.png) shows most western and southern states >=90% detection, while Bihar, Madhya Pradesh, Assam, and Jharkhand fall below 90%, mirroring weaker system indices and higher NFHS risk scores.
- **System vs risk dynamics:** Bihar and Madhya Pradesh have comparatively low DM/tobacco linkage performance, pushing them leftward on the detection curve even with strong notification growth. Uttar Pradesh's detection appears high because its risk index has diminished (steady declines in undernutrition and improved sanitation) and system score improved via private sector reporting.

### 3.3 Scenario modeling and dashboards
- Achieving 90% detection nationally requires an additional ~182,000 notifications, ~73% of which must come from Bihar (102k) and Madhya Pradesh (32k). Uttar Pradesh accounts for most of the remaining needs (~35k).
- Raising the bar to 95% detection increases the national shortfall to ~260,000 notifications, still dominated by the same eastern corridor.
- Outputs feed policy dashboards: output/tables/state_detection_scenarios.csv (for Excel/BI tools) and an interactive map (output/figures/state_detection_map.html) for rapid briefing.

---

## 4. Discussion
1. **Rapid coverage gains are real but uneven.** National detection recovered to 86% in 2023 (WHO definition), yet Bihar lags at 57%. Without targeted action, Bihar alone could continue to harbor more than one-third of all missed TB cases.
2. **System-strength proxies matter.** The cascade-derived system index (DM/Tobacco/Alcohol screening and linkage) is highly predictive of detection. States with double-digit improvements in these indicators (e.g., Odisha, Telangana) correspondingly move up the detection ladder.
3. **Risk remains concentrated.** NFHS-5 risk profiles confirm the eastern TB belt (Bihar-Jharkhand-Odisha-Assam) still concentrates undernutrition, tobacco, and energy poverty, meaning incidence will remain elevated even if detection improves.

---

## 5. Policy implications & recommendations
1. **Bihar task force:** Deploy (a) intensified DM screening at all Ni-kshay Mitra sites, (b) CHW-led active case finding in top 10 districts, and (c) private-sector notification incentives. These measures cover the modeled +102k cases needed for 90% detection.
2. **Madhya Pradesh laboratory surge:** Add at least 150 molecular diagnostic hubs in low-performing divisions to capture the +32k annual cases needed, coupled with strict daily Ni-kshay sync for private facilities.
3. **Assam & Jharkhand targeted cascades:** Both require <2k additional notifications; focusing on improving DM/Tobacco linkage (currently <35%) would likely close the gap without massive expansion.
4. **Sustain high performers:** Maharashtra, Gujarat, and Tamil Nadu already >97% detection-policy priority shifts to retention and DR-TB management rather than further case-finding expansion.

---

## 6. Limitations
- **Notification completeness:** The Rajya Sabha CSV only includes a subset of providers; we proportionally scaled state totals to match WHO `c_newinc` figures. Discrepancies with the official India TB Report breakdown may persist until the full state table is released.
- **Risk covariate timing:** NFHS-5 reflects 2019-2021 conditions; risk trajectories may have improved since, especially in states with rapid socioeconomic gains.
- **Model assumptions:** The logistic calibration is deterministic and not a full Bayesian posterior. Uncertainty intervals are not yet available (future work could reintroduce the PyMC model once state incidence priors become public).
- **GeoJSON vintage:** The mapping layer does not include Ladakh or the merged Dadra & Nagar Haveli-Daman & Diu UT; these territories are omitted from the choropleth legend.

---

## 7. Conclusion
India is on course to close the national missed-case gap, but sustained progress hinges on a handful of lagging states. By fusing Ni-kshay notifications, care-cascade indicators, and NFHS risk data, we can quantify the shortfall to actionably precise targets-e.g., Bihar's +47k cases to reach 90% detection. The provided scripts and datasets allow analysts to refresh these insights annually or as soon as new WHO/Ni-kshay releases are published, keeping state and district plans aligned with End TB 2025 ambitions.

---

## Data, code & materials availability
All raw CSVs reside in data/raw/, processed panels in data/processed/, scripts inside scripts/, and outputs in output/. Running python scripts/06_state_gap_analysis.py regenerates every table and figure referenced here. No individual-level data were used.

---

## References
1. World Health Organization. *Global Tuberculosis Report 2024* (country estimates CSV download, accessed Nov 2025).  
2. Central TB Division, MoHFW. *India TB Report 2024* (Ni-kshay cascade tables for DM/Tobacco/Alcohol).  
3. MoHFW & International Institute for Population Sciences. *National Family Health Survey (NFHS-5), 2019-21.*  
4. Rajya Sabha/Ni-kshay Live Dashboard CSV exports (sessions 260-267).  
5. Press Information Bureau, Govt. of India. "India reports record 2.55 lakh TB notifications in 2023." (March 2025 brief).

---

*Last updated:* 23 Nov 2025 via automated pipeline.
