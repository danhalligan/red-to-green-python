# Penguin parade 🐧

> **Difficulty:** 🌶️
>
> **Before you start:** [Python Fundamentals](../python_fundamentals/README.md),
> a little pandas (reading a CSV and selecting columns), and the optional
> scientific stack (`uv sync --all-groups --extra science`).
>
> **You’ll practise:** inspecting messy tables, choosing a reliable join key,
> validated merges, missing values, `groupby`, and checking a result before
> trusting it.
>
> **Check:** `uv run pytest exercises/penguin_parade/ -q` checks the two
> functions. Your notebook's plot and explanations check the investigation.

> You've joined an Antarctic ecology project studying three species of penguin.
>
> The field team has measured hundreds of birds. A separate laboratory has
> returned blood-isotope results that might say something about what they eat.
>
> Your colleague has asked you to combine the records and find out whether the
> species differ.
>
> There's just one problem. Your first attempt at joining the files has produced
> rather more penguins than the researchers remember sampling.
>
> Where did the extra penguins come from?

The data are real: Adélie, Chinstrap and Gentoo penguins sampled on islands near
Palmer Station, Antarctica over three seasons. They come from the
[Palmer Penguins](https://allisonhorst.github.io/palmerpenguins/) data. The
original is a single table, so we have split it into two files to stand in for
the field team's records and the laboratory's. See the
[source note](data/SOURCE.md) for exactly what was done. Nothing was invented,
and the missing values and identifiers are as they were recorded.

| File | What it holds |
|---|---|
| `field_observations.csv` | One row per sampled penguin: season (`study_name`), `sample_number`, `individual_id`, `species`, `island`, `sex`, bill, flipper and body measurements, and the team's `comments` |
| `isotope_results.csv` | The laboratory's blood-isotope results, `delta15n` and `delta13c`, labelled with the season, sample number and individual ID from the sample sheet |

Isotope ratios in blood are a chemical record of what an animal has been eating.
Roughly, δ15N rises with a higher place in the food web, and δ13C reflects where
the food was found. You don't need to know more than that.

Work through the [notebook](investigate.ipynb) alongside the stages below.

## Stage 1: Meet the penguins

Load both files and look at them properly before you join anything: shapes,
column types, missing values, and which columns could identify a penguin. How
many penguins were sampled? How many have usable blood-isotope measurements? Are
those necessarily the same number?

## Stage 2: Where did the extra penguins come from?

> **Check:** `uv run pytest exercises/penguin_parade/test_penguins.py -k reconcile -q`

In [notebook section 2](investigate.ipynb#2.-Where-did-the-extra-penguins-come-from?),
merge the two tables on the most obvious column and count the rows. Then try
others. A merge that runs without an error is not necessarily a merge that is
right.

Once you know which columns identify a penguin, implement `reconcile_samples` in
[penguins.py](penguins.py). It should return one row per field observation, in
the field table's order, with the isotope results attached. A penguin with no
laboratory result keeps its row, with missing isotopes. It should raise a
`ValueError` rather than return a wrong table if a penguin could match more than
one record, or if a laboratory result belongs to no field observation, and it
should not change its inputs.

<details>
<summary>💡 Hint 1: something isn't unique</summary>

Could an identifier that looks unique within one season also appear in another?
And could a number that counts samples start again somewhere?

</details>

<details>
<summary>💡 Hint 2: think about what identifies a record</summary>

Which combination of columns picks out exactly one penguin? Check that a
combination is unique in *both* tables before you merge on it.

</details>

<details>
<summary>💡 Hint 3: check the join contract</summary>

Merging on more than one column takes a list for `on=`. `validate=` tells pandas
the relationship you expect between the tables, and raises an error if the data
disagree. It checks the key you chose, but it cannot tell you which key to
choose. `indicator=True` shows which side each row came from. Compare the number
of rows before and after.

</details>

## Stage 3: Who's missing?

In [notebook section 3](investigate.ipynb#3.-Who's-missing?), find the penguins
with no isotope results and read their comments. Are the missing results
failures, or something else? Then count penguins by `sex`. Do the counts add up
to the number of penguins? Compare `groupby("sex")` with
`groupby("sex", dropna=False)`.

Choose how to deal with missing values deliberately, for example by dropping rows
only for the columns an analysis needs, instead of deleting every row that has a
gap anywhere.

## Stage 4: What does the blood tell us?

> **Check:** `uv run pytest exercises/penguin_parade/test_penguins.py -k summarise -q`

Implement `summarise_isotopes` in [penguins.py](penguins.py): one row per
species, with the number of observations, the number of valid measurements of
each isotope, and the mean and standard deviation of each. A missing value is
neither counted nor treated as zero.

Then, in [notebook section 4](investigate.ipynb#4.-What-does-the-blood-tell-us?),
draw a scatter plot of δ13C against δ15N, coloured by species. Do the species
occupy different regions? How much do they overlap? What might that suggest about
how they feed, and what can you not conclude from these data?

<details>
<summary>💡 Hint: drawing the scatter plot</summary>

A penguin needs both isotopes to be plotted, but only one to contribute to a
mean. Select the complete pairs for the plot, without throwing away the rest of
the table. Looping over `groupby("species")` and calling `ax.scatter` once per
group makes a legend easy.

</details>

## Stage 5: Before you go

Your colleague wants to reuse your analysis for another season. What checks would
you build into the pipeline so that a future join can't silently duplicate or
lose penguins? Write down two or three.

**Extension 🚀:** species or place? Cross-tabulate species against island. What
do you notice, and why does it make the species comparison harder to interpret?
Only one species lives on all three islands. Compare its isotope summaries across
islands.

<details>
<summary>What did you discover?</summary>

**The extra penguins.** Individual IDs are labels such as `N1A1`, which look like
a nest number and an adult number. They are reused every season, so most appear
more than once (114 of the 190
distinct IDs are in more than one season). Sample numbers count samples within a
species, so they start again for each species. A merge on either one alone
quietly matches a penguin with every other penguin that shares its label:
merging on `individual_id` gives 703 rows from 344 field records, and on
`sample_number` gives 826. Even the season plus the sample number gives 619. The
season plus the individual ID is unique in both tables, and gives exactly 344.
Other combinations work too, but only if they are unique in both tables.

pandas did not complain because a many-to-many merge is a legitimate operation.
It is `validate="one_to_one"` that turns a wrong assumption into an error. It
checks the relationship, but you have to supply the right key.

**The missing penguins.** Thirteen penguins have no isotope results at all, and
every one has a comment saying why: usually not enough blood, or no sample taken.
One more has only δ13C ("No delta15N data received from lab"). These are
different kinds of missing, and treating them alike would hide that. Eleven
penguins have no recorded sex; `groupby("sex")` leaves them out unless you pass
`dropna=False`.

**The blood.** The species differ, with overlap. Chinstraps have the highest
δ13C (about −24.6) and δ15N (about 9.4), Adélies are in between (about −25.8 and
8.9), and Gentoos have the lowest δ15N (about 8.3). Chinstraps stand apart most
clearly on δ13C, and Adélies and Gentoos overlap on it. That is consistent with
different feeding habits, but isotopes alone do not prove what a species eats or
where.

**Species or place?** Every Chinstrap was sampled on Dream and every Gentoo on
Biscoe, so a species difference could in part be a difference between islands.
Adélies live on all three islands, and their isotope values barely differ between
them (δ15N 8.79–8.95, δ13C −25.92 to −25.75). That suggests the species differences
are not just the islands, though it does not prove it.

**Trustworthy data.** A join that runs is not a join that is right. Useful checks
for a pipeline are: confirm keys are unique before merging, assert the row count
afterwards, report unmatched records on both sides, and keep the source and
transformations documented.

</details>

## Source

Penguin data: Gorman KB, Williams TD, Fraser WR (2014), *PLoS ONE* 9(3): e90081,
and Horst AM, Hill AP, Gorman KB (2020), *palmerpenguins*. Released under CC0; see
the [source note](data/SOURCE.md) for the exact version and how the two files
were made.
