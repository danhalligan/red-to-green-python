# Spinning plates 🧪

> **Difficulty:** 🌶️🌶️, with optional advanced investigations
>
> **Before you start:** basic Python and pandas, and the optional scientific
> stack (`uv sync --all-groups --extra science`).
>
> **You’ll practise:** parsing awkward text files, tidy data, validated joins,
> quality control, normalisation, plotting, and deciding how far to trust a
> result.
>
> **Check:** `uv run pytest exercises/spinning_plates/ -q` checks the
> data-processing functions. Your notebook's plots and explanations check the
> investigation; there is no single right answer to the final question.

Lab scientists often have to keep several tasks, projects and responsibilities
going at the same time, and there always seem to be 96-well plates all over the
place. One of them is now yours.

![Performers balancing many spinning plates on long sticks](data/plate-spinning.jpg)

<sub>Plate spinning, 24 November 1972. Photo: unknown, Correio da Manhã Fund,
[Arquivo Nacional](https://commons.wikimedia.org/wiki/File:Correio_da_Manh%C3%A3_AN_052.jpg)
(public domain), via Wikimedia Commons, resized.</sub>

> **From:** Dr Pippa Petts  
> **To:** The Data Science Team  
> **Subject:** HELP!!! Plate EXP-042 is gaslighting me (urgent-ish, mostly urgent)
>
> Hi!
>
> I'm so sorry to bother you. I know you're busy, but I am currently juggling
> three projects, a grant deadline and a cell culture that needs feeding every
> four hours, so I am officially out of hands.
>
> I finally ran my compound screen on EXP-042, and I was SO excited. Then I tried
> to open the plate reader's export in Excel and it just... won't load. It sits
> there. Judging me. I eventually pasted bits of it into a spreadsheet by hand,
> and now I've been staring at the numbers for hours and something looks *off*.
> The controls, the one thing that is supposed to behave, are not behaving. My
> blanks are glowing, my "high" wells are not, and none of my compounds seems
> to do anything at all?? (The layout is in a separate file. Don't ask.)
>
> I need a data scientist ASAP to get to the bottom of this. Did the experiment
> work? Can I trust any of it? Please help!!!
>
> Thank you thank you thank you,  
> Pippa
>
> P.S. There's a run record somewhere in there too. I wrote down what I could
> remember. It has been a very long week.

**Can you find out what happened and if the experiment worked?**

Work in the [Spinning plates notebook](investigate.ipynb). It
calls the functions you will write in
[spinning_plates.py](spinning_plates.py), which also supplies two
plotting helpers (`plate_heatmap` and `plot_concentration_response`) so you can
spend your time on the data rather than on Matplotlib.

## The experiment

A 96-well plate has eight rows (A–H) and twelve columns (1–12), so wells are
named `A01` to `H12`. Cells were grown in the wells and treated with three
compounds, each at four concentrations (in µM) with four replicate wells per
concentration. The remaining wells are controls:

| `sample_type` | What is in the well | Biomarker signal | Reference signal |
| --- | --- | --- | --- |
| `treatment` | cells and one of Compounds A, B or C | depends on the compound | cells |
| `vehicle` | cells and the solvent (DMSO) only | high: nothing is inhibiting it | cells |
| `inhibitor` | cells and a reference inhibitor | strongly reduced | cells |
| `blank` | medium only, no cells | background only | background only |

Each well was read in two **channels**. The *biomarker* channel measures the
biological process under investigation. The *reference* channel is roughly
proportional to the amount of cellular material in the well. Both channels also
have a background level, and neither can be trusted beyond the instrument's
limits.

Three files describe the run. They are in
[`data/`](data/), and reading them
is part of the job. Open the export and the layout in an editor, then load them
in the notebook (its setup gives you `data_dir`, the folder that holds them).

- **The plate-reader export**
  ([plate_reader_export.txt](data/plate_reader_export.txt)):
  the instrument's text file, with run details, settings, one 96-well matrix per
  channel and a short list of instrument notes.
- **The plate layout**
  ([plate_layout.csv](data/plate_layout.csv)): the
  experiment as designed, with the `sample_type`, `compound`, `concentration_um`
  and `replicate` of every well.
- **The run record**
  ([plate_run_record.json](data/plate_run_record.json)):
  who ran the plate, on which instrument, and a short log of what happened.

You will build a pipeline: parse the export, reshape it, validate it, join the
layout, apply quality control, correct for background, normalise, and summarise.
You should keep any raw readings unchanged and put derived values in new columns.

> [!IMPORTANT]
> The layout is the plate *as designed*, and nobody has deliberately corrupted
> it. Treat it as correct unless the evidence says otherwise.

## 1. Excel failed, python to the rescue 🦸

The export is not a table. Open it and look at what a parser would have to
handle: sections, header rows, matrices, instrument notes, and readings that are
not numbers at all. Implement two functions in
[spinning_plates.py](spinning_plates.py):

- `parse_plate_reader(text)` turns the export into **one row per well per
  channel**, with columns `plate_id`, `well`, `row`, `column`, `channel`,
  `signal` and `qc_flag`.
- `validate_plate(readings)` raises `ValueError` unless every channel has each
  expected well exactly once.

Handle invalid readings explicitly. Every well must still appear in your table:
never silently discard data. A reading that the instrument could not report gets
a missing `signal` and a flag that says why.

<details>
<summary>💡 Hint 1: finding your way around the file</summary>

The file is a list of sections, each starting with a line like `[Run Information]`
and ending at the next one. Decide what each section is for and ignore the rest.
Blank lines are separators, not data.

</details>

<details>
<summary>💡 Hint 2: reading one matrix</summary>

Within a measurement section, the first line gives the column numbers and each
later line starts with a row letter. Pair each reading with its row letter and
column number to build the well name. `float()` raises `ValueError` for text
such as `OVER` or `---`: decide what each of those should become. The instrument
notes are matched by well and channel, so parse the matrices first and apply the
notes afterwards.

</details>

Check your work with
`uv run pytest exercises/spinning_plates/test_spinning_plates.py -k "parse or validate" -q`.

How many readings carry a flag? Which of them would you trust?

## 2. One well, one row

[Tidy data](https://byuidatascience.github.io/python4ds/tidy-data.html) has
**one observation per row and one variable per column**. The export might be
readable by eye, being laid out in the plate arrangement, but for an analysis
pipline you need one row per *well*, with both channels side by side and
everything known about the well alongside, so you can operate on all
measurements of one type by applying a function to a column.

Implement:

- `pivot_channels(readings)` reshapes the tidy readings to one row per well,
  with a column of signals and a column of QC flags for each channel.
- `join_layout(wells, layout)` attaches the layout to those wells by well name.

A join that quietly loses or duplicates wells is a classic way to analyse the
wrong experiment. Make `join_layout` raise `ValueError` when a well is missing
from either table or listed twice, rather than hoping the data are clean.

<details>
<summary>💡 Hint: reshaping and joining</summary>

`DataFrame.pivot` turns the values of one column into new columns, and
`DataFrame.merge` joins tables on a key. `merge` can check the relationship
between the two tables for you with its `validate` argument, but it will not
notice a well that is absent from one side, so compare the sets of wells too.

</details>

Check your work with
`uv run pytest exercises/spinning_plates/test_spinning_plates.py -k "pivot or join" -q`.

## 3. Loss of control

Build the analysis table in the notebook and compare it with what the briefing
says each control should do.

A plate heatmap shows measurements in the same layout as they would be on a 
plate, which makes spatial problems far easier to see. The notebook draws the
intended layout beside the two channels.

The control measurements may look reasonable one at a time, but it looks like
they fail to match the wells they were supposedly in! What could explain this?
How would you tell the competing explanations apart? Write your explanations
down before you test them.

A helper is available for testing explanations:

- `remap_readings(wells, mapping)` reassigns readings to different wells. A
  mapping is a function that takes a well name and returns the name of the well
  whose reading belongs to it. It must send every well to a different source
  well.

Check it with
`uv run pytest exercises/spinning_plates/test_spinning_plates.py -k remap -q`.

Then investigate in the notebook. You must **provide evidence** for the
explanation you choose: say what you tested, what you found, and how decisive it
is.

> [!IMPORTANT]
> Decide between explanations *before* you look at what each one does to the
> compounds' dose-response curves. If you choose whichever one makes your
> compounds look best, the curves cannot tell you anything afterwards.

Take a look at the run record. Does anything support your hypothesis?

<details>
<summary>💡 Hint 1: look at the controls</summary>

Compare the expected locations of each control type with the observed signals.
Does the spatial pattern make sense? Look at both channels: different controls
may be more easily distinguished in one channel than the other.

</details>

<details>
<summary>💡 Hint 2: question the mapping</summary>

Perhaps all the readings are attached to the wrong wells in the same systematic
way? Consider simple geometrical transformations of the plate, and be prepared
to test several. A good test says clearly which wells should be high and which
low, and asks whether the measurements agree.

</details>

<details>
<summary>💡 Hint 3: a concrete strategy</summary>

A 180° rotation of a plate reverses both the row order and the column order, so
`A01` swaps with `H12`, `A02` with `H11`, and in general row letter *r* and
column *c* swap with the opposite row letter and column 13 − *c*. Write that as
a mapping, alongside the three simpler ones (as exported, rows reversed only,
columns reversed only). For each, remap the readings and compare the result with
the layout, looking at the vehicle, inhibitor and blank wells in each channel.
Then compare the result with the run record.

</details>

## 4. The Pipeline

Process the readings with the mapping you chose by chaining functions together
in a **pipeline**: each step takes a DataFrame and returns a modified DataFrame,
which becomes the input to the next step. Small, named steps make an analysis
easy to read, test and rerun. pandas can chain them for you with
`DataFrame.pipe`, for example `data.pipe(first_step).pipe(second_step, option)`.

Implement these steps:

1. `mark_usable(wells)` applies your **QC policy** by adding a `usable` column.
  Decide which flags exclude a well, and say why.
2. `subtract_blank(wells)` estimates the background in each channel from the
  usable blank wells and subtracts it, adding `biomarker_net` and
  `reference_net`.
3. `normalise_to_reference(wells)` divides the biomarker by the reference so that
  differences in the amount of cellular material cancel, adding `normalised`.
4. `percent_of_vehicle(wells, column)` expresses a column relative to the vehicle
  controls. It returns the new column rather than a whole DataFrame, so attach it
  with `assign`.
5. `summarise_replicates(wells, column)` summarises the replicate wells for each
  compound and concentration. It turns the wells into a summary table, so it is
  the last step.

`z_prime(high, low)` is a separate quality check, not a pipeline step: it takes
two groups of values and returns a single number, the
[Z′-factor](https://en.wikipedia.org/wiki/Z-factor), the standard assay-quality
measure of how well two control groups are separated. Above about 0.5 is
excellent; near zero or negative means the controls overlap. Implement it too,
and use it to check your corrected controls.

Check them with
`uv run pytest exercises/spinning_plates/test_spinning_plates.py -k "usable or blank or normalise or vehicle or summarise or z_prime or pipeline" -q`.

<details>
<summary>💡 Hint 1: background first</summary>

A blank well contains no cells, so whatever it reads is background. Estimate the
background level in each channel from the usable blank wells, and subtract it from
every well in that channel before doing anything else.

</details>

<details>
<summary>💡 Hint 2: then take a ratio</summary>

Once the background has gone, the reference should proportional to the amount of
cellular material in the well, and the biomarker is proportional to the same
material multiplied by the biological response. Their ratio removes the amount of
material and leaves the response.

</details>

<details>
<summary>💡 Hint 3: dividing by almost nothing</summary>

A ratio is only as good as its denominator. If a well's net reference signal is
close to zero, it is mostly noise, and dividing by it produces a huge, meaningless
number. Choose a sensible minimum for the net reference signal and treat the ratio
as missing below it.

</details>

Then, in the notebook, plot the concentration-response curves for each compound,
and check your corrected controls with `z_prime`: do they separate well enough to
trust the plate?

Finally, compare four analyses of the same readings: with and without your
orientation correction, and with the blank-subtracted biomarker or the
reference-normalised one. Interpret the differences rather than just drawing the
plots. How does the replicate variability (for example the SEM of each
condition) change when you normalise to the reference, and why? For each analysis
you would not show a colleague, explain how it could mislead them. Which
corrections did you need? Did any of the compounds do anything?

There is no need to fit a curve or compute an IC50. A clear picture of the
replicate means and their uncertainty is enough.

## 5. Would you sign off on this?

Your colleague wants to progress Compound A to the next stage. Would you
recommend progressing it, repeating the experiment or rejecting the result?

Write a short conclusion, supported by your plots and QC findings. Some things to
consider:

- How convincingly can you establish what if anything went wrong?
- What evidence is there for what may have happened?
- Do the controls meet reasonable QC expectations?
- Are responses consistent across replicate wells?
- What uncertainty remains about sample identities and instrument handling?
- What confirmatory experiment would you recommend?
