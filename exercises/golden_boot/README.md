# Golden Boot ⚽

> **Difficulty:** 🌶️
>
> **Before you start:** basic Python, simple probability distributions, and the
> optional scientific stack (`uv sync --all-groups --extra science`).
> [A likely story](../a_likely_story/README.md) is useful background on
> likelihood, but not required.
>
> **You’ll practise:** Bayesian updating of a rate with a Gamma prior, posterior
> means and credible intervals, and comparing players by posterior probabilities.
>
> **Check:** `uv run pytest exercises/golden_boot/ -q` checks the functions you
> write. Your notebook's tables, plots and explanations check the investigation.

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
shots. See the [source note](data/SOURCE.md) for the columns, the
credit, and what the data can and cannot tell us.

## Stage 1: Who's the best goalscorer?

In [notebook section 1](investigate.ipynb#1.-Who's-the-best-goalscorer?), build
season totals for the forwards and calculate non-penalty goals per 90 minutes.
Sort the list. Who tops it, and how many minutes did they play? Would you give
them the Golden Boot?

## Stage 2: Before the first kick

In [notebook section 2](investigate.ipynb#2.-Before-the-first-kick), meet the
prior.

### The model for this exercise

The number of goals a forward scores in 90 minutes can be modelled with a
Poisson distribution, whose one parameter $\lambda$ is the average number of
goals per 90 minutes: the forward's *scoring rate*.

We don't know the value of $\lambda$, but we can describe the values it might
take by modelling it with another distribution. A **Gamma** distribution is a
good choice, and describes the possible values of $\lambda$ with two parameters:
a shape $\alpha$ and a *rate* $\beta$.

<details>
<summary>📖 Background: Bayesian updating</summary>

### The idea: prior + data = posterior

Bayesian inference is a way of updating what you believe when evidence arrives.
It has three parts:

- A **prior**: what you believe about the unknown *before* looking at this
  player's data.
- The **data**: what you observe, here a player's goals and minutes.
- A **posterior**: what you believe *after* combining the two.

In short, **prior + data = posterior**. The posterior is a whole distribution,
not one number, so it says both what the unknown is likely to be and how unsure
we still are. It can also serve as the prior for the next piece of data.

You already reason this way. A new striker joins your club and scores in his
first match. Before you saw him play, you expected something like a typical
forward (your prior). One goal is encouraging, but it is one match, so you only
nudge that expectation upwards. After thirty matches, the evidence has taken
over. Bayes' rule is the arithmetic for how far to move, given how strong the
prior is and how much data there is.

### Where does the prior come from?

From information that is not in this player's own data: earlier seasons, other
leagues, or simply what we know about the job. Forwards usually score about a
goal every three games, and nobody expects one to score five a game. When we know
little, we can choose a deliberately vague prior instead. Either way the prior is
a choice made by the analyst, so it should be stated openly and justified.

### Isn't that making up data?

A fair worry. There are four answers.

- **The prior is not data.** It is never added to the table. It is an assumption
  about which values are plausible before looking, written as a distribution.
- **Every analysis makes assumptions.** Sorting by raw goals per 90 assumes a
  player's record, however short, is the best guide to their true rate. Stage 1
  shows how well that works. A prior states what to do with short records
  instead, and anyone can disagree with it and change it.
- **The data can overrule the prior.** A short record is pulled strongly towards
  the prior and a long one much less, and with enough data the prior stops
  mattering. One season is not enough to ignore it, which is a reason to be open
  about it.
- **You can check.** Repeat the analysis with a different prior. If a conclusion
  survives, it does not rest on the prior; if it changes, say so. In Stage 5,
  try your shortlist with $\mathrm{Gamma}(0.6, 1.8)$ and
  $\mathrm{Gamma}(60, 180)$, which have the same mean but are worth about
  2 and 180 matches. Which conclusions change?

</details>

Here we use $\mathrm{Gamma}(6, 18)$ for a forward's scoring rate in goals
per 90 minutes. This is equivalent to "6 goals in 18 matches". Its mean is $6/18
= 1/3$ of a goal per 90 minutes, about what we would expect for a typical
forward. Its strength is a judgement: strong enough that a one-match record does
not dominate, weak enough that a full season of evidence still counts. It is an
illustrative modelling choice, not an established fact.

Plot our choice of prior: $\mathrm{Gamma}(6, 18)$ . What does it say about
a typical forward?

> [!WARNING]
> SciPy's `gamma` is parameterised by a `scale`, which is $1/\beta$, not the
> rate $\beta$!

## Stage 3: Updating the evidence

> **Check:** `uv run pytest exercises/golden_boot/test_scoring_rates.py -k update
> -q`

If a forward scores $g$ goals in $e$ units of 90 minutes (so 270 minutes is
$e = 3$), and goals arrive at rate $\lambda$, then $g \mid \lambda \sim
\mathrm{Poisson}(\lambda e)$. 

We can update our prior with the observed data to get a *posterior*
distribution. For a Gamma prior, this is simple to calculate

$$\lambda \mid g \sim \mathrm{Gamma}(\alpha + g,\ \beta + e).$$

Implement `update_gamma` in [scoring_rates.py](scoring_rates.py) to return the
two parameters of the posterior.

<details>
<summary>💡 Hint 1: updating a Gamma prior</summary>

Goals increase the first Gamma parameter, and time increases the second. How
much time has passed, in the units the rate is measured in?

</details>

## Stage 4: How good is this player?

> **Check:** `uv run pytest exercises/golden_boot/test_scoring_rates.py -k
> summary -q`

Implement `posterior_summary` in [scoring_rates.py](scoring_rates.py). It
returns the posterior mean rate and the ends of the central 95% **credible
interval**: a range that contains the rate with posterior probability 95%, given
the model, prior and data.

The mean of a Gamma($a$, $b$) distribution is $a/b$. For the interval, use
`scipy.stats.gamma.ppf([0.025, 0.975], a, scale=1 / b)`.

Then, in [notebook section 3](investigate.ipynb#3.-Updating-the-evidence),
compare two records: A. Mitrović (one goal in 90 minutes) and Mohamed Salah.
Plot the prior and both posteriors. How does each record move the prior? Why is
Salah's posterior so much narrower?

## Stage 5: The Golden Boot shortlist

In [notebook section 4](investigate.ipynb#4.-The-Golden-Boot-shortlist), make a
table for ten recognisable forwards, with the raw rate, the posterior mean and
the 95% credible interval, ranked by posterior mean. Has the ranking changed?
Which players have the most precise estimates? Does a wide interval mean a
player is worse?

## Stage 6: How confident are you?

> **Check:** `uv run pytest exercises/golden_boot/test_scoring_rates.py -k
> probability_greater -q`

In [notebook section 5](investigate.ipynb#5.-How-confident-are-you?), Salah has
a higher posterior mean than Kane. Does that make him the better scorer? Answer
it with a probability: how likely is it that Salah's *true rate* is higher than
Kane's? Each rate is uncertain, and each has its own posterior, so we cannot
read the answer from the two means.

Implement `probability_greater` in [scoring_rates.py](scoring_rates.py). It
takes two Gamma posteriors, as `(shape, rate)` pairs, and returns the estimated
probability that the first rate exceeds the second.

<details>
<summary>💡 Hint 1: a probability about two uncertain numbers</summary>

If you could draw a possible rate for each player from their posterior, you
could ask which is larger. Do that many times. What fraction of draws favours
the first player?

</details>

<details>
<summary>💡 Hint 2: drawing from a Gamma posterior</summary>

`rng = np.random.default_rng()` makes a random generator, and
`rng.gamma(shape, scale, size)` draws from a Gamma distribution with a *scale*
of $1/\text{rate}$.

</details>

Then compare Salah with Kane, Kane with Agüero, and Agüero with Vardy. How does
the answer relate to the gap between the means and the width of the intervals?
