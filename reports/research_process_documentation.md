# Comprehensive Research Narrative: State-wise Missed TB Cases in India

This document explains each component of the automation project that estimates “missed” tuberculosis (TB) cases (incidence minus notifications) for India’s states and union territories. It is intended for reviewers who need a clear understanding of data provenance, processing logic, statistical reasoning, assumptions, validation checks, and interpretation of outputs.

---

## 1. Study overview

- **Objective:** Quantify annual missed TB cases at national and state levels, classify states by gap magnitude, and identify the notification improvements required to meet detection targets (80%, 90%, 95%).
- **Design:** Secondary-data modeling using official WHO CSV exports, Ni-kshay notifications, India TB Report cascade indicators, and NFHS-5 covariates. The deterministic calibration ensures national totals align with WHO incidence and notification numbers.
- **Outputs:** Harmonized CSV panels (`data/processed/state_year_panel.csv` and `output/tables/state_detection_panel.csv`), scenario tables, figures, `reports/analysis_summary.md`, the full manuscript (`reports/tb_manuscript.md`), and this methodology narrative.

---

## 2. Data assets

| Source | File(s) in repo | Key fields used | Notes |
| --- | --- | --- | --- |
| WHO TB portal (Nov 2025 downloads) | `TB_burden_countries_2025-11-23.csv`, `TB_notifications_2025-11-23.csv` (converted via `scripts/07_process_who_resource_files.py` to `data/processed/who_india_ts.csv`) | Incidence estimates, mortality, population, `c_newinc` notifications, case detection ratio (CDR) | Official estimates through 2024. |
| Ni-kshay / India TB Report (Rajya Sabha exports) | `RS_Session_260_AU_618_A_to_B_i.csv`, `RS_Session_266_AU_2024.csv`, `RS_Session_266_AU_1736_A_to_C_3 (1).csv`, `RS_Session_266_AU_1736_A_to_C_4.csv`, `RS_Session_267_AU_3467_1.csv` | State notifications 2020–2023; Jan–Oct 2024 notifications & deaths; age and death distributions; treatment outcomes | 2024 file replaces 2511_1.csv to reflect the latest partial year counts. |
| India TB Report 2024 cascade annex | `2.10_TB_Diabetes.csv`, `2.11_TB_Tobacco.csv`, `2.12_TB_Alcohol.csv` | Screening coverage, diagnosis yield, and treatment initiation fractions for DM, tobacco, and alcohol comorbidities | Act as proxies for system strength. |
| NFHS-5 (2019–21) | `nfhs5_state_agg.csv` | Stunting, underweight, wasting, anemia, tobacco, alcohol, sanitation, clean fuel | Provide risk-factor context. |
| Derived outputs | `data/processed/state_year_panel.csv`, `output/tables/state_detection_panel.csv`, `output/tables/state_detection_scenarios.csv`, `output/figures/*` | Final indicators for manuscript and policy briefs | Regenerated whenever scripts run. |

All files are stored in `data/raw/` and versioned CSVs are in `SOURCES DATA/` for traceability.

---

## 3. Pipeline steps

1. **WHO ingestion (`scripts/07_process_who_resource_files.py`):** Converts the large WHO CSVs into a clean India time series with incidence, mortality, population, and notification totals for 2000–2024.

2. **Ni-kshay ingestion (`scripts/02_ingest_india_tb_reports.py`):** Harmonizes the Rajya Sabha export, standardizes state names, melts year columns, and outputs `data/processed/india_tb_state_notif.csv`.

3. **State panel builder (`scripts/03_build_state_panel.py`):** Merges notifications, NFHS-5 covariates, cascade priors, and (optionally) census data. Derives `missed = incidence_est – notifications` and `detection_cov = notifications / incidence_est` for states with available incidence estimates.

4. **Deterministic calibration (`scripts/06_state_gap_analysis.py`):**
   - Constructs **system-strength z-scores** from cascade coverage and **risk z-scores** from NFHS-5 indicators.
   - Scales state notifications so that each year’s sum equals WHO’s `c_newinc`.
   - Solves for detection probabilities using a logistic model `logit(p_s,t) = α_t + β1 * system_z – β2 * risk_z` constrained so Σ (notifications_s,t / p_s,t) = WHO incidence_t.
   - Computes `incidence_est`, `missed`, detection categories, scenario tables, and updates figures plus Markdown reports.

5. **Reporting (`reports/analysis_summary.md`, `reports/tb_manuscript.md`, `reports/tb_manuscript.docx`):** Updated automatically after each run.

The process is fully reproducible—running scripts 07 → 02 → 03 → 06 regenerates all analytics.

---

## 4. Statistical principles & assumptions

1. **Incidence anchoring:** WHO’s incidence estimates are treated as true national totals. State-level incidence is therefore determined by the detection probabilities derived from notifications.

2. **Notification scaling:** The Rajya Sabha export undercounts some providers; scaling each state’s notifications to match WHO `c_newinc` ensures consistency with official national totals. The relative state shares follow Ni-kshay data; absolute totals align with WHO.

3. **Detection probability model:**  
   - Baseline logistic intercept `α_t` varies by year.  
   - System strength increases detection (β1 = +0.9), risk burden decreases detection (β2 = –0.5). Coefficients were chosen to keep detection probabilities within a plausible 20–98% range and can be tuned if new validation data become available.

4. **Scenario projections:** Additional notifications = `max(0, target * incidence_est – notifications)`; this assumes incidence remains constant while detection improves and does not account for incidence reduction from prevention interventions.

5. **Temporal alignment:** NFHS-5 covariates (2019–2021) represent baseline risk. Cascade indicators come from the latest India TB Report (2023 data). We assume these proxies reasonably describe 2023 system readiness.

6. **Uncertainty:** Current outputs are deterministic. A Bayesian extension (`scripts/04_fit_bayesian_model.py`) is included for future posterior estimation once state-level incidence priors are available.

---

## 5. Quality checks & validation

| Check | Description |
| --- | --- |
| **National totals** | Confirm Σ state notifications (after scaling) equals WHO `c_newinc` for each year; Σ state incidences equals WHO incidence. |
| **Non-negativity** | `missed` is clipped at ≥0; detection is bounded between 0.2 and 0.98. |
| **Covariate completeness** | NFHS/cascade values are median-imputed only when missing; logs warn about absent states. |
| **Scenario sanity** | Additional notifications drop to zero for states already above the target detection. |
| **Narrative consistency** | Figures (`output/figures/national_trend.png`, `top_states_missed.png`, `state_detection_map.png`) are reviewed after each run to ensure text matches visuals. |

Peer reviewers can reproduce the entire pipeline by running the scripts in order; Git history records each change to inputs and code.

---

## 6. Interpretation of current results (run date: 23 Nov 2025)

- **National trend:** Detection increased from 58.8% (2020) to 86.3% (2023). Missed cases dropped from 1.14 million to 0.38 million.
- **High-gap states (2023):** Bihar (57% detection), Uttar Pradesh (85%), Madhya Pradesh (75%), Assam (78%), Jharkhand (81%)—collectively 53% of national missed cases.
- **Scenario needs:** Achieving 90% detection requires ~182k extra notifications annually, with Bihar contributing ~102k and Madhya Pradesh ~32k. Moving to 95% detection raises the requirement to ~260k, still dominated by the same states.
- **Policy note:** Focused investments in cascade coverage and private-sector reporting in Bihar/Madhya Pradesh provide the highest return; most other states are within 5–10 percentage points of the 90% target.

These interpretations align with `output/tables/state_detection_panel.csv` and `state_detection_scenarios.csv`, ensuring traceability.

---

## 7. Reproducibility guidance

1. **Environment:** Python ≥ 3.11 recommended. Install dependencies via `pip install -r requirements.txt` (numpy, pandas, seaborn, matplotlib, plotly, kaleido, pdfplumber, python-docx, etc.).
2. **Data placement:** Drop new WHO CSVs and Ni-kshay exports into `data/raw/`. For updated India TB Report annexes, place them in the same folder and rerun script 02.
3. **Script order:**  
   `python scripts/07_process_who_resource_files.py`  
   `python scripts/02_ingest_india_tb_reports.py`  
   `python scripts/03_build_state_panel.py`  
   `python scripts/06_state_gap_analysis.py`
4. **Outputs:** Check `reports/analysis_summary.md`, `reports/tb_manuscript.md`, and `output/figures/` after reruns. Optional conversion to DOCX is available via the helper script used to create `reports/tb_manuscript.docx` and can be reused for this document.
5. **Version control:** All scripts and generated files reside in the repo; keep a log of run dates and input versions for peer reviewers.

---

## 8. Supplementary materials

- **`reports/tb_manuscript.md` & `.docx`:** Full academic manuscript with tables and figures ready for submission.
- **`reports/analysis_summary.md`:** Snapshot of the latest run for quick briefing.
- **`output/tables/*.csv`:** Machine-readable tables for reproducibility or downstream dashboards.
- **Conversion scripts:** The Python snippet used to convert Markdown to DOCX (via `python-docx`) is available in the commit history, enabling reviewers to regenerate Word versions of this document and the manuscript.

---

By following the steps above, reviewers can validate each transformation, rerun the analysis with newer data releases, and verify that the conclusions in the manuscript are directly traceable to the underlying code and datasets.
