"""Plate-reader data: parse an awkward export, tidy it, check it and normalise it."""

import re
from collections.abc import Callable, Iterable, Sequence

import numpy as np
import pandas as pd

ROWS = "ABCDEFGH"
N_COLUMNS = 12
# The columns that hold a well's readings, as opposed to who or where it is.
MEASUREMENT_COLUMNS = ("biomarker", "reference", "biomarker_flag", "reference_flag")


def split_well(well: str) -> tuple[str, int]:
    """Split a well name such as "C03" into its row letter and column number."""
    match = re.fullmatch(r"([A-Z])(\d{1,2})", well.strip())
    if match is None:
        raise ValueError(f"Not a well name: {well!r}")
    return match[1], int(match[2])


def well_name(row: str, column: int) -> str:
    """Build a well name such as "C03" from a row letter and column number."""
    return f"{row}{column:02d}"


def parse_plate_reader(text: str) -> pd.DataFrame:
    """Parse a plate-reader export into one row per well per channel.

    The export is a text file of sections, each starting with a header such as
    `[Run Information]`. This function needs three things from it:

    - the `Plate ID:` line in the run information;
    - every measurement section, whose header looks like `[Biomarker (RFU)]`
      (the channel is the lowercased name before "(RFU)"). It holds a `Well`
      header row of column numbers, then one row per plate row: the row letter
      followed by one reading per column;
    - the `[Instrument Notes]` section, where a line such as
      `G11  Reference  Low signal warning` flags a reading that is present.
      Notes that do not start with a well are not about a reading: ignore them.

    Return columns plate_id, well (e.g. "C03"), row ("C"), column (3, an int),
    channel ("biomarker" or "reference"), signal (a float) and qc_flag.
    qc_flag is "ok", "saturated" (reading `OVER`), "missing" (any other
    non-numeric reading, such as `---`) or "low_signal" (a numeric reading with
    a low-signal note). Saturated and missing readings keep their row, with
    signal NaN. Never drop a well silently.

    Raise ValueError if there is no Plate ID or no measurement section.
    """
    # TODO: parse the text into the tidy DataFrame described above.
    raise NotImplementedError


def validate_plate(
    readings: pd.DataFrame, rows: str = ROWS, n_columns: int = N_COLUMNS
) -> None:
    """Raise ValueError unless every channel has each expected well exactly once.

    The expected wells are every row letter in `rows` with every column from 1
    to `n_columns` (96 wells by default). Report duplicated, missing and
    unexpected wells in the error message. Return None if the plate is valid.
    """
    # TODO: check the wells of each channel.
    raise NotImplementedError


def pivot_channels(readings: pd.DataFrame) -> pd.DataFrame:
    """Reshape tidy readings into one row per well.

    Return columns plate_id, well, row, column, then one column of signals per
    channel (in the order the channels first appear: "biomarker", "reference"),
    then one `<channel>_flag` column of qc flags per channel. The signal columns
    must be floats. Rows are in plate order (by row letter, then column
    number) with a fresh 0..n-1 index. The input is not modified.
    """
    # TODO: pivot the signals and qc flags so each well is a single row.
    raise NotImplementedError


def join_layout(wells: pd.DataFrame, layout: pd.DataFrame) -> pd.DataFrame:
    """Attach each well's layout columns to the one-row-per-well table.

    Join on `well`. Return every column of `wells` followed by the layout's
    other columns, with the rows of `wells` in their original order.

    The join must neither lose nor duplicate wells: raise ValueError if either
    table lists a well more than once, if a well has no layout entry, or if the
    layout lists a well that was never read.
    """
    # TODO: merge on the well, rejecting joins that lose or duplicate wells.
    raise NotImplementedError


def remap_readings(
    wells: pd.DataFrame,
    mapping: Callable[[str], str],
    columns: Sequence[str] = MEASUREMENT_COLUMNS,
) -> pd.DataFrame:
    """Reassign readings to different wells.

    `mapping` takes a well name and returns the well whose reading should be
    used for it: the result's row for well `w` holds the `columns` values of the
    input's row for well `mapping(w)`. Every other column (including the well
    itself and any layout columns) stays where it is.

    The mapping must be a permutation of the wells: raise ValueError if the
    wells are not unique, if it returns a well that is not in the table, or if
    two wells map to the same source. The input is not modified.
    """
    # TODO: look up each well's source well and copy its readings across.
    raise NotImplementedError


def z_prime(high: Iterable[float], low: Iterable[float]) -> float:
    """Return the Z'-factor separating two control groups.

    Z' = 1 - 3 * (sd_high + sd_low) / |mean_high - mean_low|, using sample
    standard deviations and ignoring NaN. Above about 0.5 is an excellent assay;
    near zero or negative means the controls overlap.
    """
    # TODO: compute the Z'-factor.
    raise NotImplementedError


def mark_usable(
    wells: pd.DataFrame, exclude_flags: Iterable[str] = ("saturated", "missing")
) -> pd.DataFrame:
    """Add a boolean `usable` column: no `*_flag` column holds an excluded flag.

    This is the QC policy. By default saturated and missing readings are
    excluded, and low-signal warnings are kept. Other columns are unchanged.
    """
    # TODO: apply the QC policy.
    raise NotImplementedError


def subtract_blank(wells: pd.DataFrame) -> pd.DataFrame:
    """Subtract each channel's blank level, adding `biomarker_net` and `reference_net`.

    The blank level for a channel is the mean of its raw readings in usable wells
    whose sample_type is "blank". Net values are NaN for wells that are not
    usable. Raise ValueError if there are no usable blank wells. The raw columns
    are left unchanged.
    """
    # TODO: estimate the blank level and subtract it, keeping the raw columns.
    raise NotImplementedError


def normalise_to_reference(
    wells: pd.DataFrame, min_reference: float = 100.0
) -> pd.DataFrame:
    """Add `normalised`: `biomarker_net` divided by `reference_net`.

    The reference channel stands in for the amount of cellular material in the
    well. Where `reference_net` is below `min_reference` the ratio is
    meaningless (it would blow up), so `normalised` is NaN there.
    """
    # TODO: divide by the reference, guarding against near-zero values.
    raise NotImplementedError


def percent_of_vehicle(wells: pd.DataFrame, column: str) -> pd.Series:
    """Express `column` as a percentage of the mean for the vehicle controls.

    The vehicle mean uses wells whose sample_type is "vehicle", ignoring NaN.
    Return a Series aligned with `wells`. Raise ValueError if no vehicle well
    has a value.
    """
    # TODO: scale the column so the vehicle controls average 100.
    raise NotImplementedError


def summarise_replicates(wells: pd.DataFrame, column: str) -> pd.DataFrame:
    """Summarise treatment replicates by compound and concentration.

    Use only wells whose sample_type is "treatment". Return one row per
    compound and concentration_um (sorted) with columns compound,
    concentration_um, n (how many replicates have a value), mean, sd (sample
    standard deviation) and sem (standard error of the mean), all ignoring NaN.
    """
    # TODO: group the treatment wells and summarise each group.
    raise NotImplementedError


def plate_heatmap(wells: pd.DataFrame, column: str, ax=None, title=None, **kwargs):
    """Draw `column` as a plate: row A at the top, columns 1 to 12 across.

    Numeric columns are coloured by value; other columns (such as sample_type)
    get one colour per category. Extra keyword arguments go to `imshow`, for
    example cmap="viridis". Returns the Axes.
    """
    import matplotlib.pyplot as plt

    ax = ax or plt.gca()
    values = wells[column]
    labels = None
    if not pd.api.types.is_numeric_dtype(values):
        codes, labels = pd.factorize(values, sort=True)
        values = pd.Series(np.where(codes >= 0, codes, np.nan), index=wells.index)
    grid = np.full((len(ROWS), N_COLUMNS), np.nan)
    for row, number, value in zip(wells["row"], wells["column"], values, strict=True):
        grid[ROWS.index(row), number - 1] = value
    image = ax.imshow(grid, **kwargs)
    ax.set_xticks(range(N_COLUMNS), labels=[str(n) for n in range(1, N_COLUMNS + 1)])
    ax.set_yticks(range(len(ROWS)), labels=list(ROWS))
    colorbar = ax.figure.colorbar(image, ax=ax, shrink=0.8)
    if labels is not None:
        colorbar.set_ticks(range(len(labels)), labels=[str(label) for label in labels])
    ax.set_title(title or column)
    return ax


def plot_concentration_response(summary: pd.DataFrame, ax=None, title=None):
    """Plot mean +/- sem against concentration (log axis), one line per compound.

    `summary` is the output of `summarise_replicates`. Returns the Axes.
    """
    import matplotlib.pyplot as plt

    ax = ax or plt.gca()
    for compound, group in summary.groupby("compound"):
        ax.errorbar(
            group["concentration_um"],
            group["mean"],
            yerr=group["sem"],
            marker="o",
            capsize=3,
            label=compound,
        )
    ax.set_xscale("log")
    ax.set_xlabel("Concentration (µM)")
    ax.legend()
    if title:
        ax.set_title(title)
    return ax
