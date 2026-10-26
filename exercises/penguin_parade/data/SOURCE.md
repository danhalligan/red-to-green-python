# Penguin parade data

A reconstruction from one real table, not how the original project distributed
its data.

**Source:** `penguins_raw.csv` from
[palmerpenguins](https://github.com/allisonhorst/palmerpenguins), pinned to
commit `8db8ef55e61d9a36b81e39833655410ace199e37` (SHA-256 of the file:
`144f623143c9360fd77322a4f86acb06dc198814dbd2669724c63e6457b907bd`). Released
under [CC0](https://creativecommons.org/publicdomain/zero/1.0/). The data were
collected by Dr Kristen Gorman and the Palmer Station Long Term Ecological
Research programme:

- Gorman KB, Williams TD, Fraser WR (2014). *PLoS ONE* 9(3): e90081.
  <https://doi.org/10.1371/journal.pone.0090081>
- Horst AM, Hill AP, Gorman KB (2020). *palmerpenguins.*
  <https://doi.org/10.5281/zenodo.3960218>

**What was done:** the table was split into a field file (all 344 rows) and a
laboratory file (the 331 rows with at least one isotope value), both shuffled
with a fixed seed. Some columns were renamed or left out, and `species` was
shortened to its first word. No value was changed or invented; identifiers and
missing values are as recorded.
