"""Penguin parade: reconcile field and laboratory records, then summarise them."""

import pandas as pd


def reconcile_samples(field: pd.DataFrame, lab: pd.DataFrame) -> pd.DataFrame:
    """Attach each penguin's laboratory isotope results to its field record.

    The result has one row per field observation, in the field table's order,
    with every field column plus the laboratory's ``delta15n`` and ``delta13c``.
    Penguins with no laboratory result keep their row, with missing isotopes.

    Raise ``ValueError`` rather than return a wrong table if a penguin could
    match more than one record, or if a laboratory result matches no field
    observation. Do not modify ``field`` or ``lab``.
    """
    raise NotImplementedError


def summarise_isotopes(data: pd.DataFrame) -> pd.DataFrame:
    """Summarise isotope measurements for each species.

    ``data`` has ``species``, ``delta15n`` and ``delta13c`` columns, and any
    value may be missing. Return one row per species, sorted by species, with
    ``species`` as an ordinary column followed by:

    - ``n_observations``: the number of rows for the species;
    - ``n_delta15n`` and ``n_delta13c``: how many valid measurements it has;
    - ``mean_delta15n`` and ``mean_delta13c``: the means of the valid values;
    - ``sd_delta15n`` and ``sd_delta13c``: their sample standard deviations.

    Missing values are neither counted nor treated as zero. A species stays in
    the result even if it has no valid measurements. Do not modify ``data``.
    """
    raise NotImplementedError
