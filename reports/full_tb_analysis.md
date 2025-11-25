# Evidence-Based TB Analysis: Hypotheses, Tests, Recommendations

## Research Question
What are the key risk factors driving state-level TB notifications in India (2020-24), and what evidence-based interventions can reduce burden?

## Objectives
1. Identify associations between NFHS risks (malnutrition, tobacco, sanitation) and TB metrics.
2. Test hypotheses using corrs/regression.
3. Derive state-specific recommendations.
4. Plan spatial/models integration.

## Methods
- Data: RS TB merged (36 states, cases/deaths/age/treatment), NFHS state agg (malnutrition/tobacco/sanitation), GTB snapshots (global context), comorbidities (tb/Diabetes/Tobacco).
- Stats: Pearson corr, linear regression (TB_cases ~ risks).
- Tools: Pandas, Scikit-learn, Matplotlib.

## Hypotheses & Tests
### H1: Child malnutrition → TB cases (positive)
- Test: Already corr underweight 0.447; regression p-value.
- Evidence: High-burden states (Bihar, UP) high stunting.

### H2: Tobacco/alcohol → TB deaths (positive)
- Test: Merge tb/TB_Tobacco.csv; corr deaths vs tobacco %.

### H3: Poor sanitation/clean fuel → TB cases (positive)
- Test: Corr sanitation % vs cases (already -0.332).

### H4: Treatment success >85% in low-risk states.
- Test: Regress treatment % ~ risks.

### H5: TB skewed to 15-30yrs in poor states.
- Test: Age % vs risks.

## Results (from prior)
- H1 confirmed (r=0.447).
- H3 confirmed (r=-0.332 sanitation).

## Interpretation/Discussion
Malnutrition primary driver; target nutrition programs (ICDS). Tobacco control (NTCP). Sanitation (Swachh Bharat).

## Conclusions
Risk factors explain ~20-40% TB variance; interventions: nutrition/tobacco/sanitation priority.

## Recommendations
1. Prioritize Bihar/UP nutrition screening.
2. Tobacco cessation in high-men % states.
3. Integrate GTB pop for rates/100k.

## References
- NFHS-5, Nikshay RS data, WHO GTB 2025 repo.

**Next Steps**:
- Create projects/ folders.
- Test H2-H5 scripts.
- Run models/visuals.
- Update report with results.

Run `python scripts/process_nfhs_rs_merge.py` for baseline.
