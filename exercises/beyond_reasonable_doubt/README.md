# Beyond reasonable doubt ⚖️

> **Difficulty:** 🌶️🌶️
>
> **Before you start:** basic Python and probability, and the optional
> scientific stack (`uv sync --all-groups --extra science`).
> [A likely story](../a_likely_story/README.md) is useful background on
> likelihood, but not required.
>
> **You’ll practise:** Bayesian updating with a Beta prior, posterior
> probabilities, credible intervals, numerical integration, and checking how much
> a conclusion depends on its assumptions.
>
> **Check:** `uv run pytest exercises/beyond_reasonable_doubt/ -q` checks the two
> functions. Your notebook's plots and explanations check the investigation.

A clinical trial has finished, and the results are in.

The new treatment reduced observed mortality from about 46% to about 35%. That
sounds promising. But the trial reported a p-value of 0.09, and ≈. Another insists it works and should
become standard practice. Both seem rather confident.

You have been asked to look at the evidence and decide what we can actually
conclude.

The treatment is extracorporeal membrane oxygenation (ECMO), an intensive and
invasive form of life support: blood is pumped out of the body, loaded with
oxygen and returned, giving failing lungs time to recover. The trial, called
EOLIA, enrolled patients with very severe acute respiratory distress syndrome
(ARDS), and randomly assigned them to one of two strategies:

- **Early ECMO:** start ECMO immediately.
- **Conventional care:** continue standard treatment with a ventilator, with
  ECMO available as a rescue if a patient's condition became desperate.

So this is not ECMO against no ECMO; it is a strategy of starting early against
a strategy of waiting, where some of the waiting patients still got ECMO. No
clinical knowledge is needed beyond that.

The data are the real published counts. They are a pair of rows, and that is all
the analysis needs. See the [source note](data/SOURCE.md) for the citations and
for what the data can and cannot tell us.

| `group` | `patients` | `deaths` by day 60 |
|---|---:|---:|
| `early_ecmo` | 124 | 44 |
| `conventional_care` | 125 | 57 |

Work through the [notebook](investigate.ipynb) alongside the stages below.

## Stage 1: Did the trial fail?

In [notebook section 1](investigate.ipynb#1.-Did-the-trial-fail?), load the
counts and calculate the observed mortality in each group, the absolute
difference in percentage points, and the relative risk. The trial reported
$P = 0.09$. Does missing the conventional threshold of $P < 0.05$ show that the
two strategies are equivalent? What does the p-value actually answer, and what
question would you rather ask?

To see how much a p-value depends on the test, also run a simple one yourself
on the 2×2 table of deaths and survivors, with `scipy.stats.chi2_contingency`
(try `correction=False` and the default) or `scipy.stats.fisher_exact`. Do the
p-values agree with each other, and with 0.09?

> [!NOTE]
> A simple test on these counts will not return exactly 0.09. The trial
> monitored its results with a sequential design, a triangular test, and its
> published relative risk, confidence interval and P value were corrected for
> it. This exercise does not repeat that analysis.

## Stage 2: Before seeing the evidence

In [notebook section 2](investigate.ipynb#2.-Before-seeing-the-evidence), meet
the prior. Let $p$ be the probability that a patient in one group dies by day
60. A likelihood, as in [A likely story](../a_likely_story/README.md), says
which values of $p$ make the observed counts plausible. To say how *probable*
each value of $p$ is, we also need to say what we believed before we saw the
data. A **prior** is a probability distribution over $p$, and **Bayes' rule**
combines it with the likelihood:

$$\text{posterior} \propto \text{likelihood} \times \text{prior}.$$

We use the Beta distribution, a flexible family of distributions for a
probability, and start with $\operatorname{Beta}(1,1)$, which is uniform: every
mortality between 0 and 1 is equally plausible. Plot it. What does it say? Is it
a reasonable thing to believe about the death rate in very severe ARDS?

## Stage 3: Updating the evidence

> **Check:** `uv run pytest exercises/beyond_reasonable_doubt/test_bayes_trial.py
> -k update -q`

For a Beta prior and a binomial count of deaths, the Bayesian update has a
closed form. If $d$ of $n$ patients die and $p \sim \operatorname{Beta}(\alpha,
\beta)$ before the data, then afterwards

$$p \mid d \sim \operatorname{Beta}(\alpha + d,\ \beta + n - d).$$

Implement `update_posterior` in [bayes_trial.py](bayes_trial.py). It returns the
two Beta parameters, and it should reject counts that cannot be real, and priors
that are not valid.

<details>
<summary>💡 Hint 1: what is uncertain?</summary>

The observed proportion of deaths is not necessarily the underlying probability
of death. Another trial with the same strategy would see different counts.

</details>

<details>
<summary>💡 Hint 2: updating a Beta prior</summary>

Deaths increase the first Beta parameter, and survivors increase the second. How
many survivors are there?

</details>

Then, in [notebook section 3](investigate.ipynb#3.-Updating-the-evidence),
calculate the posterior for each group, and plot the prior and both posteriors
with the supplied `plot_mortality_distributions`. How uncertain are we about each
group's mortality? Do the two posteriors overlap? SciPy's `beta.pdf`,
`beta.mean` and `beta.ppf` are all you need.

A **95% credible interval** is a range that contains the parameter with
posterior probability 95%, given the model, prior and data. This differs from a
frequentist confidence interval, which describes how often a *procedure* would
capture the truth across repeated trials, not the probability for one interval.
For example, `beta.ppf([0.025, 0.975], a, b)` gives the central 95% interval.

## Stage 4: Beyond reasonable doubt?

> **Check:** `uv run pytest exercises/beyond_reasonable_doubt/test_bayes_trial.py
> -k probability_of_benefit -q`

Let $p_E$ and $p_C$ be the mortality probabilities with early ECMO and
conventional care. The treatment effect is the **absolute mortality
reduction**

$$\Delta = p_C - p_E,$$

in percentage points when multiplied by 100. A positive $\Delta$ favours early
ECMO. This is not the same as a *relative* reduction: lowering mortality from
46% to 35% is about 10 percentage points, but a relative reduction of about a
fifth.

Each $p_g$ now has its own posterior. They are independent, so the probability
that $\Delta$ exceeds a threshold $t \ge 0$ is an integral over the possible
values $x$ of ECMO mortality: weigh each $x$ by how plausible it is, and by the
probability that control mortality is more than $t$ above it:

$$P(\Delta > t \mid D) = \int_0^{1-t} f_E(x)\,\bigl[1 - F_C(x + t)\bigr]\,dx,$$

where $f_E$ is the ECMO posterior density and $F_C$ the control posterior's
cumulative distribution function. No simulation is needed: the integral can be
evaluated numerically.

Implement `probability_of_benefit` in [bayes_trial.py](bayes_trial.py).

<details>
<summary>💡 Hint 1: comparing two distributions</summary>

The relevant quantity is not the difference between the two posterior means. We
need the probability that one *uncertain* mortality exceeds the other by at
least $t$.

</details>

<details>
<summary>💡 Hint 2: the SciPy tools</summary>

`scipy.stats.beta.pdf(x, a, b)` is $f_E$, and `scipy.stats.beta.sf(x, a, b)` is
$1 - F_C$ (the survival function), so $1 - F_C(x + t)$ is `beta.sf(x + t, a, b)`.
`scipy.integrate.quad(function, low, high)` returns the integral and an error
estimate as a pair.

</details>

<details>
<summary>💡 Hint 3: checking yourself</summary>

Two uniform posteriors give $P(\Delta > t) = (1 - t)^2 / 2$, because the
difference of two uniform variables has a triangular distribution. Identical
posteriors should give exactly one half at $t = 0$.

</details>

Numerical integration is a tool here, not the point of the exercise. Now use it:
in [notebook section 4](investigate.ipynb#4.-Beyond-reasonable-doubt?), predict
the posterior probability that early ECMO reduces mortality *at all*, then
calculate it. Next find the probability of a reduction of at least 2, 5, 10 and
20 percentage points. How can we be fairly confident that there is some benefit,
and much less confident that the benefit is large?

> [!NOTE]
> These thresholds are illustrative questions, not clinical guidelines.

## Stage 5: How much benefit is enough?

In [notebook section 5](investigate.ipynb#5.-How-much-benefit-is-enough?), plot
the posterior probability of exceeding each reduction, from 0 to 25 percentage
points. (These are evaluations of the posterior on a grid, not simulated data.)
Where does the curve start, and how fast does it fall?

Then separate three things that are easy to confuse: *evidence that a treatment
is beneficial*, *evidence that the benefit is clinically meaningful*, and *a
decision to adopt the treatment*. The third has to weigh costs, harms,
feasibility and the alternatives, which a probability of benefit cannot do.

## Stage 6: Does your prior matter?

*Optional, but important for interpretation.*

In [notebook section 6](investigate.ipynb#6.-Does-your-prior-matter?), repeat the
analysis with other priors, applied identically to both groups:

- $\operatorname{Beta}(1,1)$: the baseline above.
- $\operatorname{Beta}(0.5,0.5)$: another weak prior.
- $\operatorname{Beta}(40,60)$: an illustrative stronger prior centred on 40%
  mortality in each arm. It carries about as much weight as 100 patients, so it
  pulls both posterior means towards 40% and towards each other: it is
  sceptical about big differences.

These are illustrative assumptions, not priors derived from independent
clinical evidence. Which of your conclusions stay put when the prior changes,
and which move?

## Stage 7: Would you recommend ECMO?

In [notebook section 7](investigate.ipynb#7.-Would-you-recommend-ECMO?), play
the evidence-review committee. You have estimated how probable it is that early
ECMO improves mortality, and how large the benefit might be. The treatment is
invasive, expensive and associated with complications. The trial also stopped
early, and some control patients received rescue ECMO. Write a short,
evidence-based recommendation. There is no single right answer, and no
posterior probability is a universal threshold for approving a treatment.

## What the analysis can and cannot say

- **The comparison.** The two groups are *assigned to* early ECMO and *assigned
  to* conventional care with rescue ECMO available. The data cannot tell us the
  effect of receiving ECMO against never receiving it.
- **Early stopping.** The trial had planned interim analyses and stopped early,
  and its published P value was corrected for that design. Our model treats the
  final counts as simple binomial samples and ignores the design.
- **Crossover.** Control patients who received rescue ECMO stay in the control
  group, as randomised. These counts cannot support an as-treated analysis.
- **A simplified model.** We assume independent binomial outcomes and
  independent Beta priors. We do not adjust for centres, patient
  characteristics, crossover or timing. This is an explicit analysis of
  aggregate counts, not a full clinical reanalysis.
- **Probabilities are conditional.** "95% probable" means 95% under this model,
  these priors and these data. It is not proof that the treatment works, nor a
  prediction that 95% of future trials will show a benefit.
- **Mortality is not the whole decision.** The trial also reported more bleeding
  and more severe thrombocytopenia with early ECMO. This exercise is not
  medical advice.

## Optional extension: compare with the published analysis

Only after completing your own analysis, read Goligher et al.'s Bayesian
reanalysis of the same trial (see below). Their posterior probabilities are
similar to yours, but not identical. Why might that be? Compare their priors,
what they modelled, and what you assumed.

## References

- Combes A, et al. (2018). Extracorporeal Membrane Oxygenation for Severe Acute
  Respiratory Distress Syndrome. *New England Journal of Medicine* 378:
  1965–1975. <https://doi.org/10.1056/NEJMoa1800385>
- Goligher EC, et al. (2018). Extracorporeal Membrane Oxygenation for Severe
  Acute Respiratory Distress Syndrome and Posterior Probability of Mortality
  Benefit in a Post Hoc Bayesian Analysis of a Randomized Clinical Trial. *JAMA*
  320: 2251–2259. <https://doi.org/10.1001/jama.2018.14276>

This exercise is an independent, simplified analysis of the published aggregate
counts. It does not reproduce the JAMA analysis, which used different models and
priors, and its results need not match.
