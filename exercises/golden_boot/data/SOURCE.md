# Source of the Golden Boot data

`premier_league_2017_18.csv` has one row for each player in each Premier League
match of the 2017/18 season (380 matches, 10,350 player-matches).

## Where it comes from

The data are derived from the Wyscout public soccer match event dataset:

Pappalardo, L., Cintia, P., Rossi, A. *et al.* (2019). A public data set of
spatio-temporal match events in soccer competitions. *Scientific Data* 6, 236.
<https://www.nature.com/articles/s41597-019-0247-7>

The files are published on figshare (collection 4415000) under the
[Creative Commons Attribution 4.0 International licence](https://creativecommons.org/licenses/by/4.0/)
(CC BY 4.0). This table is a derived work: it keeps only match, player, minutes,
goal and shot counts from the Events, Matches, Players and Teams files. We
changed the form of the data and added nothing to it. It is shared under the same
licence, with credit to the original authors and to Wyscout.

## What each column means

| Column | Meaning |
|---|---|
| `player_id` | The source's player identifier. Names are not unique, so group by this. |
| `player_name` | The source's short name, such as `H. Kane`. |
| `role` | The player's role code in the source: `FW`, `MD`, `DF` or `GK`. It is one fixed code for the whole season, not a per-match position. |
| `team` | The player's team in that match. |
| `match_number` | The team's *n*-th league match, from 1 to 38. |
| `minutes` | Approximate minutes played (see below). |
| `goals` | Goals scored, including penalties and free kicks, excluding own goals. |
| `penalty_goals` | Goals scored from penalties. |
| `non_penalty_goals` | `goals` minus `penalty_goals`. |
| `shots` | Shots excluding penalties, including blocked ones and direct free kicks. |

## How the table was made

- Goals are shot events (and free-kick shots) with the source's goal tag.
  Penalties are the source's penalty events. Own goals are excluded.
- Minutes come from lineups and substitutions: a starter plays 90 minutes unless
  substituted or sent off, and a substitute plays 90 minus the minute they came
  on. Stoppage time is ignored, so minutes are approximate and a few exceed 90.
  A substitute with a shot but no minutes by this rule is credited with one
  minute.
- The source stores some accents as literal escape sequences (for example
  `Ag\u00fcero`); these are decoded.
- Rows are kept only for players who played.

## Limits

- It is one league in one season.
- Totals match the published records for most players: Salah 32 goals, Agüero 21,
  Vardy 20, Sterling 18, Lukaku 16 and Firmino 15. The data give Harry Kane 29
  goals, one fewer than the 30 usually published.
- The roles are the source's own and are not checked.
- The steps above are everything that was done to the source data.
