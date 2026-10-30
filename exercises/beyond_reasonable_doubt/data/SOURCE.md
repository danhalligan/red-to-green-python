# Beyond reasonable doubt data

**File:** `eolia_60_day_mortality.csv`, the primary-outcome counts from the
EOLIA randomised clinical trial. Nothing was simulated, reconstructed or
imputed.

## Sources

- Combes A, Hajage D, Capellier G, et al. (2018). Extracorporeal Membrane
  Oxygenation for Severe Acute Respiratory Distress Syndrome. *New England
  Journal of Medicine* 378: 1965–1975. <https://doi.org/10.1056/NEJMoa1800385>
  (the trial report; ClinicalTrials.gov number NCT01470703).
- Goligher EC, Tomlinson G, Hajage D, et al. (2018). Extracorporeal Membrane
  Oxygenation for Severe Acute Respiratory Distress Syndrome and Posterior
  Probability of Mortality Benefit in a Post Hoc Bayesian Analysis of a
  Randomized Clinical Trial. *JAMA* 320: 2251–2259.
  <https://doi.org/10.1001/jama.2018.14276> (a published Bayesian reanalysis).

The exercise makes its own, simpler analysis of the aggregate counts. It does
not reproduce the JAMA reanalysis, which used different models and priors, so
the numbers will differ.

## What the data are

The primary endpoint of the trial was death by day 60 after randomisation.
The file holds the two published counts:

| `group` | Strategy | `patients` | `deaths` |
|---|---|---:|---:|
| `early_ecmo` | Immediate venovenous ECMO | 124 | 44 |
| `conventional_care` | Continued conventional lung-protective ventilation, with ECMO available as rescue therapy | 125 | 57 |

The trial reported a relative risk of 0.76 (95% confidence interval 0.55 to
1.04; P = 0.09). The paper states that these were "corrected for the triangular
test", the sequential design used to monitor the trial. A plain test of the two
proportions in the table above gives a different p-value, roughly 0.10 to 0.12
depending on the test, and a relative risk of 0.78 rather than 0.76. The
notebook gives you the published P value; you do not need to reproduce it.

**Only aggregate outcome data are available.** There are no patient-level
records, covariates or timings.

## How to read the comparison

- **Intention to treat.** Patients are analysed in the group they were
  randomly assigned to. The contrast is *assignment to immediate ECMO* against
  *assignment to conventional treatment with rescue ECMO available*. It is not
  ECMO against no ECMO.
- **Crossover.** Rescue ECMO was permitted in the control group, and 35 of the
  125 control patients (28%) received it. They stay in the control group here;
  these counts cannot support an as-treated analysis.
- **Early stopping.** The trial had prespecified interim analyses and was
  stopped early for futility, with 249 patients enrolled. A sequential design
  affects how its frequentist results are interpreted: the published relative
  risk, confidence interval and P value were corrected for it. The binomial
  model in the exercise ignores the design and treats the final counts as fixed
  samples of 124 and 125 patients.
- **Harms.** The trial also reported complications. Bleeding events leading to
  transfusion were more common with early ECMO (46% against 28%), as was severe
  thrombocytopenia (27% against 16%), while ischaemic stroke was rarer (none
  against 5%). Mortality is not the whole of a clinical decision.
