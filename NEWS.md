# pyproblems 0.1.0

* Replace the standalone Old Faithful regression with a staged Titanic
  classification investigation: majority baseline, fold-local preprocessing,
  logistic regression, a random-forest comparison, and one held-out evaluation.
  Provide preprocessing and guided notebook skeletons, keeping the focus on
  exploration, features and evaluation. Package all 1,309 labelled titanic3
  passengers without outcome-revealing fields, add scikit-learn to the science extra, and keep the
  Old Faithful regression diagnostic inside the EM application.
* Establish a Python-first programming and statistics exercise package.
* Add core language, inheritance, refactoring, test-first, scientific-Python,
  Sudoku, and optional Gaussian-mixture exercises.
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
* Make the README a pick-and-mix catalogue (size, style, hook and optional
  "try first" suggestions) with the learning routes kept as optional
  recommendations; frame the simple exercises as quick warm-ups and 99 Bottles as
  an optional test-first kata, and replace course-style prerequisites with
  "before you start" notes. Rework Gilded Rose around inheriting awkward legacy
  code, make the Gosper glider gun the payoff of Game of Life (with provided
  `place_shape` and `animate_boards` helpers), and add an evolution-versus-guessing
  comparison to the weasel.
