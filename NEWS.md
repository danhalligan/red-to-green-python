# red-to-green-python 0.1.0

* Reorganise the repository around self-contained exercises. Each exercise now
  has its own folder under `exercises/<exercise>/` holding its README,
  starter code, tests, notebook (`investigate.ipynb`) and data, replacing the
  separate `problems/`, `src/pyproblems/`, `tests/` and `analysis/` directories.
  Run an exercise with `uv run pytest exercises/<exercise>/ -q`. The
  shared Against the Odds and Old Faithful / Simulation Studies notebooks are
  split into one notebook per problem. Repository checks stay in `tests/`.

* Replace "Recovering the parameters" with "A likely story", a three-stage
  likelihood exercise on simulated data: a coin's likelihood curve, a normal
  likelihood surface, and a general `fit_mle` that fits a regression and, by
  swapping in Student-t noise, a line that resists outliers. Its Old Faithful
  section is dropped; Fitting a mixture still introduces that data set.

* Merge the Standard Error, Bootstrapping and Confidence Intervals exercises
  into "Known unknowns", a single three-stage exercise on estimating uncertainty
  that shares one module and one simulation notebook. The Old Faithful parts are
  dropped in favour of simulation, `bootstrap_standard_error` gains a
  `statistic` argument, new `normal_interval` and `bootstrap_interval` functions
  build confidence intervals for any statistic, and the exercise uses them to
  bootstrap the median, which has no standard-error formula.

* Extend the Game of Life shape library with still lifes (block, beehive,
  eater), oscillators (blinker, toad, beacon, pulsar, pentadecathlon, figure
  eight, tumbler) and small long-lived patterns (R-pentomino, diehard,
  pi-heptomino, acorn), with tests that check each one's behaviour and prompts
  to explore them in the notebook.
* Add "Spinning plates", a laboratory data-science puzzle: parse an awkward
  96-well plate-reader export, build a tidy DataFrame pipeline, investigate why
  the controls fail, normalise two measurement channels and decide whether the
  recovered result can be trusted. Includes a synthetic experiment (export,
  layout and run record), starter code, tests and an investigation notebook.
* Add "The AI that makes up words", a standard-library exercise that trains a
  character bigram model on the packaged word list and samples new words from
  it, with an optional trigram extension and an investigation notebook.
* Add two optional extensions to Dawkins' weasel: a mutation-only genetic
  algorithm with tournament selection, then one-point crossover.
  Return the weasel's result as a dictionary rather than a dataclass.
* Replace the standalone Old Faithful regression with a staged Titanic
  classification investigation: majority baseline, fold-local preprocessing,
  logistic regression, a random-forest comparison, and one held-out evaluation.
  Provide preprocessing and guided notebook skeletons, keeping the focus on
  exploration, features and evaluation. Package all 1,309 labelled titanic3
  passengers without outcome-revealing fields, add scikit-learn to the science
  extra, and keep the Old Faithful regression diagnostic inside the EM
  application.
* Establish a Python-first programming and statistics exercise package.
* Add core language, inheritance, refactoring, test-first, scientific-Python,
  Sudoku, and Gaussian-mixture likelihood exercises.
* Package the survey, mystery-coordinate, and Sudoku datasets for standard
  library resource loading.
* Add learner scaffolds for sequence alignment, Sudoku solving, Game of Life,
  Gaussian-mixture EM, and Dawkins' weasel; package Old Faithful data.
* Add "Try, try again", a rugby union scoring exercise on recursion,
  memoisation, and bottom-up counting, with a test time limit that reports
  exponential growth instead of hanging.
* Add "Against the Odds", three counterintuitive probability puzzles (the
  birthday problem, waiting times for coin patterns and the 100 prisoners
  problem) with starter code, tests and an investigation notebook.
* Reframe the scientific exercises around questions to investigate, with
  explanations moved into optional "What did you discover?" sections, and give
  the Word ladder, Sudoku solver, rugby and sequence alignment exercises
  progressive collapsible hints. Drop the ordinary-least-squares exercise
  (`ols_coefficients`, with the Old Faithful regression now using any library
  straight-line fit) and put the Dawkins' weasel simulation before its optional
  probability questions.
* Make the README a pick-and-mix catalogue (size, style, hook and optional "try
  first" suggestions) with the learning routes kept as optional recommendations;
  frame the simple exercises as quick warm-ups and 99 Bottles as an optional
  test-first kata, and replace course-style prerequisites with "before you
  start" notes. Rework Gilded Rose around inheriting awkward legacy code, make
  the Gosper glider gun the payoff of Game of Life (with provided `place_shape`
  and `animate_boards` helpers), and add an evolution-versus-guessing comparison
  to the weasel.
