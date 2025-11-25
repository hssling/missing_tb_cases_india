# Peer Review & Validation Companion (Version 2)

This document complements the main manuscript by detailing the factors that drive the system-strength composite score, system-strength z-scores, risk z-scores, and the epidemiological risk burden used in the deterministic calibration of detection probabilities. It is designed for reviewers who wish to understand exactly how the latent constructs were derived and how reproducibility is ensured.

---

## 1. System-strength composite score
We operationalised “system strength” using indicators drawn from the India TB Report 2024 cascade annex. For each state–year, we extracted the following components:
- **Diabetes-TB screening coverage:** Percentage of notified TB patients with known diabetes status.  
- **Diabetes-TB treatment initiation:** Percentage of TB-DM patients started on anti-diabetic therapy.  
- **Tobacco use screening among TB patients:** Percentage of TB patients screened for tobacco use.  
- **Tobacco cessation linkage:** Percentage of identified tobacco users linked to cessation services.  
- **Alcohol use screening among TB patients:** Percentage of TB patients screened for alcohol use.  
- **Alcohol de-addiction linkage:** Percentage of identified alcohol users linked to de-addiction centres.

Each component was scaled to the 0–1 interval (dividing percentages by 100). The composite score was then computed as:
```text
SystemStrength = 0.30·(DM screening) + 0.15·(DM treatment initiation)
                + 0.20·(Tobacco screening) + 0.10·(Tobacco linkage)
                + 0.15·(Alcohol screening) + 0.10·(Alcohol linkage)
```
Weights reflect the relative emphasis on upstream screening (DM/tobacco) and downstream linkage. The resulting score captures the overall cascade readiness of each state.

### 1.1 System-strength z-scores
To make the composite comparable across states, we computed:
```text
SystemStrength_z = (SystemStrength – mean(SystemStrength)) / std(SystemStrength)
```
where the mean and standard deviation are calculated across all states in the latest year. This z-score enters the logistic detection model as a positive predictor (β₁ = 0.9).

---

## 2. Risk z-scores and epidemiological risk burden
NFHS-5 (2019–2021) provides state-level indicators of TB risk factors. We used:
- Childhood stunting, underweight, and wasting (% under five).  
- Childhood anemia (6–59 months).  
- Adult tobacco use (men and women).  
- Adult alcohol consumption (men).  
- Household sanitation coverage (% with improved facilities).  
- Household clean cooking fuel (%).

Each indicator was standardised (subtracting the mean and dividing by the standard deviation). The epidemiological risk burden score was defined as:
```text
Risk = mean(z_stunting, z_underweight, z_wasting, z_anemia,
            z_tobacco_men, z_tobacco_women, z_alcohol_men)
       – mean(z_sanitation, z_clean_fuel)
```
### 2.1 Risk z-scores
As with system strength, the composite was z-standardised:
```text
Risk_z = (Risk – mean(Risk)) / std(Risk)
```
This z-score captures the relative risk burden per state and enters the logistic model with a negative coefficient (β₂ = 0.5), reflecting that higher burden reduces detection probability.

---

## 3. Detection model recap
- **Scaled notifications:** Ni-kshay state notifications are scaled so that yearly sums match WHO national totals.  
- **Detection link:**  
  **`logit(p_{s,t}) = α_t + 0.9·SystemStrength_z – 0.5·Risk_z`**  
- **Incidence constraint:**  
  **`Σ_s [ notif_{s,t} / p_{s,t} ] = WHO incidence_t`**  
- **State incidence:**  
  **`Î_{s,t} = notif_{s,t} / p_{s,t}`**  
- **Missed cases:**  
  **`Missed_{s,t} = Î_{s,t} – notif_{s,t}`**

The intercept αₜ is solved iteratively, ensuring national incidence matches WHO estimates. Detection probabilities are kept between 0.20 and 0.98.

---

## 4. Reproducibility checklist
1. **Data placement:** WHO CSVs, Ni-kshay exports, cascade tables, and NFHS-5 aggregates must reside in `data/raw/`.  
2. **Scripts:** Run `07_process_who_resource_files.py`, `02_ingest_india_tb_reports.py`, `03_build_state_panel.py`, and `06_state_gap_analysis.py` sequentially to reproduce outputs.  
3. **Outputs:** Check `output/tables/state_detection_panel.csv` for the per-state indicators and `output/figures/` for visualisations.  
4. **Documentation:** The main manuscript (`reports/tb_manuscript_v5.md`), this validation note, and the DOCX with embedded figures provide a comprehensive audit trail.

---

With these details, peer reviewers can verify how the system-strength and risk composites feed into the detection model and replicate the results end-to-end using the scripted workflow.
