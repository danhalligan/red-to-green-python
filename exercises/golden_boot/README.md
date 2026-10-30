# Golden Boot ⚽

> **Difficulty:** 🌶️
>
> **Before you start:** basic Python, simple probability distributions, and the
> optional scientific stack (`uv sync --all-groups --extra science`).
> [A likely story](../a_likely_story/README.md) is useful background on
> likelihood, but not required.
>
> **You’ll practise:** Bayesian updating of a rate with a Gamma prior, posterior
> means and credible intervals, comparing players by posterior probabilities, and
> checking an estimate against what happened next.
>
> **Check:** `uv run pytest exercises/golden_boot/ -q` checks the two functions.
> Your notebook's tables, plots and explanations check the investigation.

Mohamed Salah scored 32 Premier League goals in 2017/18, a record for a 38-game
season. Harry Kane wasn't far behind.

Meanwhile one striker scored once in 90 minutes. On a per-game basis he beats
them all.

Who is the best goalscorer in the league? And how sure are you?

You have been given every player's minutes and goals from that season. Football
is full of short records and lucky streaks, so the answer needs more care than
sorting a column. Work through the [notebook](investigate.ipynb) alongside the
stages below.

## The data

The table has one row for each player in each Premier League match of the
2017/18 season: minutes played, goals, penalty goals, non-penalty goals and
shots. It comes from the Wyscout public soccer match event dataset, shared under
a CC BY 4.0 licence. See the [source note](data/SOURCE.md) for the columns, the
credit, and what the data can and cannot tell us. Minutes are approximate.

## Stage 1: Who's the best goalscorer?

In [notebook section 1](investigate.ipynb#1.-Who's-the-best-goalscorer?), build
season totals for the forwards and calculate non-penalty goals per 90 minutes.
Sort the list. Who tops it, and how many minutes did they play? Would you give
them the Golden Boot?

Notice why we count non-penalty goals: a player who takes the team's penalties
can add several goals that depend on the manager's choice, not on open play.

## Stage 2: Before the first kick

In [notebook section 2](investigate.ipynb#2.-Before-the-first-kick), meet the
prior. Let $\lambda$ be a forward's scoring rate in goals per 90 minutes. We do
not know $\lambda$, so we describe what we believe about it before looking at
that player with a **prior**, a probability distribution. A **Gamma**
distribution is a flexible family for a positive rate, with a shape $\alpha$ and
a *rate* $\beta$. We use $\operatorname{Gamma}(6, 18)$, which has mean
$6/18 = 1/3$ of a goal per 90 minutes.

The rate parameter acts like an exposure: this prior is as informative as 18
full matches of evidence, although those matches are not real records. It is an
illustrative modelling choice, not an established fact. Plot it. What does it say
about a typical forward? Why use a distribution instead of one assumed rate?

> [!NOTE]
> SciPy's `gamma` is parameterised by a `scale`, which is $1/\beta$, not the
> rate $\beta$.

## Stage 3: Updating the evidence

> **Check:** `uv run pytest exercises/golden_boot/test_scoring_rates.py -k update
> -q`

If a forward scores $g$ goals in $e$ units of 90 minutes (so 270 minutes is
$e = 3$), and goals arrive at rate $\lambda$, then $g \mid \lambda \sim
\operatorname{Poisson}(\lambda e)$. For a Gamma prior the update has a closed
form:

$$\lambda \mid g \sim \operatorname{Gamma}(\alpha + g,\ \beta + e).$$

Implement `update_gamma` in [scoring_rates.py](scoring_rates.py). It returns the
two parameters of the posterior, and it should reject counts and exposures that
cannot be real, and priors that are not valid.

<details>
<summary>💡 Hint 1: what is uncertain?</summary>

A rate of 1.00 goals per 90 is not the same evidence after one match as after
thirty. What does the prior need to know about how long we watched?

</details>

<details>
<summary>💡 Hint 2: updating a Gamma prior</summary>

Goals increase the first Gamma parameter, and time increases the second. How
much time has passed, in the units the rate is measured in?

</details>

## Stage 4: How good is this player?

> **Check:** `uv run pytest exercises/golden_boot/test_scoring_rates.py -k
> summary -q`

Implement `posterior_summary` in [scoring_rates.py](scoring_rates.py). It
returns the posterior mean rate and the ends of the central 95% **credible
interval**: a range that contains the rate with posterior probability 95%, given
the model, prior and data. This differs from a frequentist confidence interval,
which describes how often a *procedure* would capture the truth over repeated
samples, not the probability for one interval.

<details>
<summary>💡 Hint 3: the posterior summary</summary>

The mean of a Gamma($a$, $b$) distribution is $a/b$. For the interval, use
`scipy.stats.gamma.ppf([0.025, 0.975], a, scale=1 / b)`.

</details>

Then, in [notebook section 3](investigate.ipynb#3.-Updating-the-evidence),
compare two records: A. Mitrović (one goal in 90 minutes) and Mohamed Salah. Plot
the prior and both posteriors with `plot_rate_distributions`. How does each
record move the prior? Why is Salah's posterior so much narrower?

## Stage 5: The Golden Boot shortlist

In [notebook section 4](investigate.ipynb#4.-The-Golden-Boot-shortlist), make a
table for ten recognisable forwards, with the raw rate, the posterior mean and
the 95% credible interval, ranked by posterior mean. Has the ranking changed?
Which players have the most precise estimates? Does a wide interval mean a player
is worse?

## Stage 6: How confident are you?

In [notebook section 5](investigate.ipynb#5.-How-confident-are-you?), Salah has
a higher posterior mean than Kane. Does that make him the better scorer?
The supplied `probability_greater` estimates the probability that one player's
*rate* exceeds another's, from simulated draws of the two posteriors. Compare
Salah with Kane, Kane with Agüero, and Agüero with Vardy. How does the answer
relate to the gap between the means and the width of the intervals?

> [!NOTE]
> The draws describe our uncertainty about the rates. They are not simulated
> goals.

## Stage 7: Does it work?

In [notebook section 6](investigate.ipynb#6.-Does-it-work?), check the idea
against what happened next. Split the season at match 19. Using each forward's
first-half record only, take the 20 with the highest raw rate. How many goals
would their raw rates predict for the second half? How many would their posterior
means predict? How many did they actually score? Explain the gap.

## What the analysis can and cannot say

- **One season of one league.** The estimates describe 2017/18 and say nothing
  about how a player will score next year.
- **A constant rate.** We assume goals arrive at a steady rate per minute,
  independent of opponent, tactics, injuries and teammates. A player's rate
  changes through a season.
- **A shared prior.** One prior is used for every forward. It is close to a Gamma
  fitted to the forwards in this same season, so it is not independent of the
  data. A stronger or weaker prior would change the estimates.
- **Approximate minutes.** Stoppage time is ignored, and a player's role is one
  fixed code from the source.
- **Rankings versus rates.** For forwards, the Bayesian estimates predict the rest
  of the season better than the raw rates, but a Bayesian top ten is not
  noticeably a better list of future scorers than a raw one. The gain is in the
  rates.
- **Selection.** Players who play more minutes are chosen by managers. These
  are descriptive estimates, not controlled comparisons, and not a verdict on any
  player.

## Optional extension 🚀: shots or finishing?

A forward's goals are the product of two things: how many shots they take, and
how often those shots go in. Use the `shots` column.

1. Calculate each forward's conversion (non-penalty goals per shot) for forwards
   with at least 20 shots, and compare Vardy with Kane.
2. Shrink conversion with the supplied `beta_posterior_summary`, using a
   $\operatorname{Beta}(15, 85)$ prior (a mean of 15%, worth 100 shots). This is
   the same idea as before, for a probability and a count of shots. How far does
   Vardy's conversion move?
3. Split the season at match 19. For forwards with at least 15 shots in each half,
   see how well each quantity in the first half predicts the second: goals per
   90, shots per 90 and conversion.

Which of the three is most repeatable? Is conversion a skill, or mostly luck?
These data have no measure of shot quality, so what does "conversion" actually
measure?

## References

- Pappalardo L, Cintia P, Rossi A, *et al.* (2019). A public data set of
  spatio-temporal match events in soccer competitions. *Scientific Data* 6: 236.
  <https://www.nature.com/articles/s41597-019-0247-7>

The data are shared under the
[CC BY 4.0 licence](https://creativecommons.org/licenses/by/4.0/); see the
[source note](data/SOURCE.md). This exercise is an independent, simplified
analysis of one season.
