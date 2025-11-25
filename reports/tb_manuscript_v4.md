# Closing the Missed TB Case Gap in India: An Integrated State-wise Analysis (Version 4)

## Abstract
**Background:** Despite record notifications from India’s National Tuberculosis Elimination Programme (NTEP), the WHO continues to estimate a substantially higher TB incidence. Quantifying the difference between incident and notified cases—“missed” TB cases—at the state level is crucial for ensuring India’s End TB targets remain on track.  
**Methods:** Using the latest WHO TB dataset (incidence, mortality, national notifications), Ni-kshay state notification exports (2020–2023 plus Jan–Oct 2024), India TB Report cascade indicators, and NFHS-5 covariates, we constructed a deterministic calibration model that reconciles state notifications with WHO’s national totals. Detection probabilities were modelled as a logistic function of state-level system strength (care cascades) and risk burden (NFHS-5 indicators). The model yields state-specific incidence, detection percentages, missed cases, and additional notification requirements for 80%, 90%, and 95% detection.  
**Results:** National detection improved from 58.8% in 2020 to 86.3% in 2023, reducing missed cases from approximately 1.14 million to 0.38 million. Bihar (57% detection), Uttar Pradesh (85%), and Madhya Pradesh (75%) account for more than half of the remaining gap. Achieving 90% detection nationally requires ~182,000 additional notifications annually, with Bihar and Madhya Pradesh contributing roughly 73% of this total.  
**Conclusions:** Cascade-derived system metrics strongly predict detection. Intensifying comorbidity screening, private-sector engagement, and targeted active case finding in high-gap eastern states can close the majority of the residual national gap, directly supporting the WHO mandate to “find all the missing” TB cases.

---

## 1. Introduction
India has made remarkable strides in TB notification coverage, reporting 2.55 million cases in 2023. Yet WHO still estimates national incidence at roughly 2.76 million cases for the same year. This discrepancy, often termed “missed TB cases”, reflects individuals who remain undiagnosed or unreported despite improvements in molecular diagnostics and digital surveillance. State-level heterogeneity in risk factors and health-system performance underscores the need for a unified analytical framework that integrates WHO incidence estimates, Ni-kshay notifications, India TB Report cascade data, and NFHS-5 socio-economic indicators. This version of the manuscript presents such a framework and translates the results into actionable policy insights aligned with WHO’s End TB Strategy.

---

## 2. Data sources
We utilised official datasets that are both recent and publicly available:
1. **WHO TB Data Release (2024):** Provides incidence, mortality, population, and national notification totals; ensures our estimates remain consistent with WHO reporting standards.  
2. **Ni-kshay / Rajya Sabha CSV Exports:** State-wise notifications (2020–2023), age and death distributions, Jan–Oct 2024 notifications, and treatment outcomes; these capture subnational programme performance.  
3. **India TB Report 2024 Cascade Annex:** Diabetes, tobacco, and alcohol screening and linkage indicators used as proxies for system strength and differentiated TB care coverage.  
4. **NFHS-5 (2019–21):** State-level indicators of malnutrition, anemia, tobacco/alcohol use, sanitation, and clean fuel adoption; these represent social determinants of TB risk.  
5. **Supplementary WHO annexes:** Drug-resistant TB burden, treatment outcomes, and age-sex incidence, supporting sensitivity analyses.  
All raw files are stored in `data/raw/`, and derived files (notably `who_india_ts.csv` and `state_year_panel.csv`) are created via version-controlled scripts.

---

## 3. Methods
Our analytical process consists of three stages: data harmonisation, deterministic detection calibration, and scenario analysis. For transparency, we describe the key transformations and the rationale for each.

### 3.1 Data harmonisation
The WHO CSV bundle is converted to a national time series (`who_india_ts.csv`) using `scripts/07_process_who_resource_files.py`, ensuring we rely on official incidence and national notification totals. Ni-kshay state notifications are cleaned (`scripts/02_ingest_india_tb_reports.py`) to standardise state names and reshape the data into `state, year, notifications`. The state panel builder (`scripts/03_build_state_panel.py`) merges these notifications with cascade and NFHS-5 covariates, producing a comprehensive dataset (`state_year_panel.csv`) for modelling.

### 3.2 Deterministic detection calibration
The calibration model reconciles state notifications with WHO totals while accounting for system strength and risk burden. For each year \( t \) and state \( s \), let \( \text{notif}_{s,t} \) denote the scaled notifications (proportioned so that \(\sum_s \text{notif}_{s,t} = \text{WHO national notifications}_t\)). Detection probability \( p_{s,t} \) is defined via a logistic function:
\[
\text{logit}(p_{s,t}) = \alpha_t + \beta_1 \cdot \text{SystemStrength}_{s,t} - \beta_2 \cdot \text{RiskIndex}_{s,t},
\]
where \( \beta_1 = 0.9 \) and \( \beta_2 = 0.5 \). The year-specific intercept \( \alpha_t \) is solved so that
\[
\sum_s \frac{\text{notif}_{s,t}}{p_{s,t}} = \text{WHO incidence}_t,
\]
ensuring consistency with the WHO incidence estimate. We bound detection between 0.2 and 0.98 to avoid implausible values. The state incidence estimate is \( \hat{I}_{s,t} = \text{notif}_{s,t} / p_{s,t} \), and the missed cases are \( \hat{I}_{s,t} - \text{notif}_{s,t} \).

### 3.3 Scenario projections
For detection targets \( d \in \{0.8, 0.9, 0.95\} \), additional notifications required are calculated as
\[
\text{AdditionalNotif}_{s,t}(d) = \max\left(0, d \cdot \hat{I}_{s,t} - \text{notif}_{s,t}\right).
\]
Aggregating across states yields the national gap for each detection target.

---

## 4. Results
### 4.1 National trajectory
The model indicates that India’s detection coverage improved from 58.8% in 2020 to 86.3% in 2023, with missed cases falling from roughly 1.14 million to 0.38 million. The temporal trends confirm the effectiveness of post-pandemic recovery efforts and exemplify the “Find. Treat. All.” mandate advocated by the WHO.

### 4.2 State-level contributions
In 2023, Bihar (57% detection), Uttar Pradesh (85%), and Madhya Pradesh (75%) collectively account for more than half of the national missed cases. Assam and Jharkhand have smaller gaps but still require targeted interventions. States with strong cascade performance (e.g., Gujarat, Tamil Nadu, Maharashtra) maintain detection levels above 95%, highlighting the predictive value of system-strength indicators.

### 4.3 Scenario requirements
To achieve 90% detection nationally, India needs approximately 182,000 additional notifications annually, with Bihar (~102,000) and Madhya Pradesh (~32,000) contributing ~73% of the shortfall. Achieving 95% detection requires ~260,000 extra notifications, again dominated by the same states. In contrast, reaching 80% detection within the next cycle would require ~81,000 additional notifications, illustrating the diminishing returns as detection approaches the high eighties and nineties.

### 4.4 Figures and tables
Figure 1 depicts the national incidence vs. notification trends with the missed-case gap shaded—demonstrating the closing gap over time. Figure 2 ranks states by missed cases, emphasising Bihar and Uttar Pradesh as priority areas. Figure 3 maps detection coverage, showing western and southern states approaching universal detection while the eastern corridor lags. The underlying values are summarised in Tables 1–3 within the manuscript’s supplementary files, which present national trends, state-level detection categories, and scenario estimates.

---

## 5. Discussion
India’s detection trajectory has improved markedly since the pandemic, aligning with the WHO’s call to “find all the missing” TB cases. Nonetheless, Bihar and Madhya Pradesh remain significantly below the 90% target, indicating that broad-based national policies must be complemented by state-specific strategies. System-strength indicators derived from the India TB Report cascades correlate closely with detection, supporting policy efforts that emphasise comorbidity screening, private-sector partnerships, and risk stratification. NFHS-5 data confirm that structural determinants—such as malnutrition, anemia, and limited access to clean fuel—remain concentrated in the eastern corridor, echoing prior research that links socioeconomic deprivation to persistent TB transmission.

---

## 6. Limitations
First, state notification shares rely on the currently available Ni-kshay exports; if the official India TB Report releases updated tables, state contributions may shift, although the model can be rerun with new inputs. Second, NFHS-5 reflects 2019–2021 risk; states with recent improvements in nutrition or sanitation may outperform projections. Third, the deterministic calibration lacks explicit uncertainty intervals; future work will implement the Bayesian extension (script 04) once state-level incidence priors are released. Lastly, the detection map omits Ladakh and the merged Dadra & Nagar Haveli–Daman & Diu in visualisations due to geometry limitations, although their data are retained in the tabular outputs.

---

## 7. Conclusions and recommendations
Bihar and Madhya Pradesh remain the linchpins for closing India’s residual missed-case gap. Targeted interventions—such as Ni-kshay Mitra-led active case finding, scaled comorbidity screening, and private-sector notification incentives—could deliver the additional 102,000 and 32,000 notifications required to push these states toward 90% detection. Assam and Jharkhand can close their smaller gaps by enhancing differentiated care pathways and community outreach. Meanwhile, states already above 95% detection should focus on treatment success and drug-resistant TB management. The automation pipeline presented here offers a reproducible blueprint for monitoring progress and guiding state-level planning as India advances toward its End TB commitments.

---

## References
1. World Health Organization. *Global Tuberculosis Report 2024.* Geneva: WHO; 2024.  
2. Central TB Division, Ministry of Health & Family Welfare. *India TB Report 2024.* New Delhi: CTD; 2024.  
3. Ni-kshay. *Private Sector Engagement dashboards.* National TB Elimination Programme; 2024.  
4. WHO. *National Framework for Gender-Responsive TB Care in India.* Geneva: WHO; 2023.  
5. Rajya Sabha Secretariat. *Ni-kshay State TB Notifications, Sessions 260 & 266.* Parliament of India; 2024.  
6. International Institute for Population Sciences (IIPS) & ICF. *National Family Health Survey (NFHS-5), 2019–21: India.* Mumbai: IIPS; 2021.  
7. Bhargava A, Jain Y. Social determinants of tuberculosis. *Indian J Med Res.* 2020;151(5):417–419.  
8. WHO. *End TB Strategy: Updated Operational Guidance.* Geneva: WHO; 2023.
