# The wordsmith 🤖

*The AI that makes up words*

> **Difficulty:** 🌶️🌶️
>
> **Before you start:** basic Python. No scientific packages are needed, and the
> optional investigation notebook uses only the standard library.
>
> **You’ll practise:** dictionaries and `collections.Counter`, weighted random
> sampling, reproducible randomness, and judging the output of a generative
> model.
>
> **Check:** `uv run pytest exercises/generative_models/wordsmith/test_wordsmith.py -k "not trigram" -q` for the
> two core stages, or `uv run pytest exercises/generative_models/wordsmith/ -q` to include the
> extension.

You've been hired to invent names for a collection of fantasy creatures.
Unfortunately, your imagination has run dry.

Fortunately, you have a computer and thousands of English words. What if you
could build a machine that learns how English words are constructed, then uses
what it has learned to invent entirely new ones?

Your machine doesn't know what words mean. It doesn't understand grammar. It
doesn't even know what a syllable is.

**Can it still produce something that sounds convincing?**

You will train it on the packaged word list from `load_words()` in
[loaders.py](../../_shared/loaders.py), the same common English words (derived
from [SCOWL](http://wordlist.aspell.net/)) used in [Word ladder](../../algorithms/word_ladder/README.md),
which is not required first. The code goes in
[wordsmith.py](wordsmith.py). Stuck at any point? There are
three 💡 hints after Stage 2, each giving a little more away.

## Stage 1: learning to spell (sort of)

Our wordsmith will learn from one simple question: given the character I have
just written, which character tends to come next? This is a **character bigram
model**. Implement `train_model(words)`, which returns a dictionary that maps
each character to a `Counter` of the characters that have followed it, with
counts rather than a mere list of what is possible.

Words also begin and end somewhere, and the model should learn that too. Use `^`
as a marker for the beginning of a word and `$` as a marker for its end
(`START` and `END` in the module).

Try the tiny word list `cat`, `car` and `dog`. Your model should learn that:

- two words begin with `c` and one with `d`;
- `c` is always followed by `a`;
- `a` is followed once by `t` and once by `r`;
- `t`, `r` and `g` each end a word.

Convert each word to lowercase, and skip any entry that is empty or contains
anything but the letters `a` to `z`. Each entry counts once. The docstring gives
the details, including the optional `context_size` argument for the extension, which
you can ignore for now.

```bash
uv run pytest exercises/generative_models/wordsmith/test_wordsmith.py -k "train_model and not trigram"
```

## Stage 2: invent some words

Now put the model to work. Implement `generate_word(model)`. Start from the
beginning-of-word marker. At each step, pick the next character at random, so
that a common transition is more likely than a rare one. Stop when the
end-of-word marker comes up, and return the letters without any markers.

The word comes from the transitions the model has learned, never from the
dictionary itself. Use the `random` module, so that calling `random.seed` first
gives the same word every time. A model can wander forever, so there is a
`max_length`; return `None` when an attempt fails. The docstring spells out what
counts as a failure, and you can simply discard those attempts when you make
several words.

```bash
uv run pytest exercises/generative_models/wordsmith/test_wordsmith.py -k "not train_model and not trigram"
```

<details>
<summary>💡 Hint 1: think in transitions</summary>

A word is a sequence of steps from one character to the next. What would you
need to know to predict which characters might follow a given one? And how would
you know when to stop?

</details>

<details>
<summary>💡 Hint 2: counting and sampling</summary>

`collections.Counter` is made for recording how often things happen, and
`random.choices(options, weights)` picks from a list using weights. Choosing
uniformly among the possible next letters would throw away exactly what the
model has learned: that some letters are far more common than others. Remember
that a set, and a `Counter` that was built in a different order, can list things
in a different order: sort the options so the same seed always gives the same
word.

</details>

<details>
<summary>💡 Hint 3: boundaries and generation</summary>

The start marker is the first "previous character", and the end marker is a
character that the model can choose like any other. Generate a word by sampling
the next character from the counts for the current one, appending it, and
repeating until the end marker appears (or you reach the length limit). For the
trigram extension, keep the last *two* characters as the context instead, and
begin with two start markers.

</details>

## Investigation: what does it invent?

Use the [wordsmith notebook](investigate.ipynb) to train a model on
the whole word list and generate 100 words with a fixed random seed. Which ones
look convincing, and which are ridiculous? Are any of them real English words?
Can you find ten plausible new words that weren't in your original dictionary?
(The dictionary is a set, so you can check whether a word is already known.)

Please judge the words yourself: the tests check the model and the sampling, not
whether the words are amusing or pronounceable.

## Extension 🚀: a slightly longer memory

A bigram model only knows the previous character. But consider the letter `t`:
it could be followed by almost anything. If we know that the previous two
characters are `th`, we have far more information about what might come next.

> Your wordsmith has a one-character memory. What happens if you give it a
> two-character memory? Can it produce more convincing words? Or does it start
> copying its training examples?

Extend `train_model` and `generate_word` to work with the previous **two**
characters (a trigram model), using `train_model(words, context_size=2)`.
Contexts are then keys of two characters, and a word starts with two `^` markers
and ends with a single `$`. Aim for a small generalisation of your existing
code, not a second copy of it: `generate_word` can tell the context size from
the keys of the model.

```bash
uv run pytest exercises/generative_models/wordsmith/test_wordsmith.py -k trigram
```

### Which model is better?

Train both models on the same dictionary and generate 100 words from each, with
the same generation rules. Compare them:

1. Which words look more plausibly English?
2. What percentage of generated words already exist in the dictionary?
3. Does the distribution of word lengths change?
4. Does the trigram model produce fewer obviously implausible letter
   combinations?

For a fun final experiment, generate twenty *novel* words from each model and
mix them together without labels. Pick the ten most convincing inventions. Which
model produced more of their favourites? Get your favourite LLM model to write
definitions for your words and try to slip them into conversations!

Report what you find as experimental results. How plausibility, novelty and
copying the training words trade off is for the experiments to show.

## What is going on here?

Your model learned probabilities from examples, then generated new sequences by
repeatedly predicting and sampling the next character. That is a fundamental
idea behind generative language models. Modern large language models also
generate one token at a time, conditional on the previous context, but they use
different tokenisation schemes, learn far richer relationships than "which
character follows which", and are vastly more expressive models. A character
bigram model is not a tiny version of one: it counts, it doesn't understand.

Your model can invent words that look English without knowing what any of them
mean. How much can you learn about language simply by trying to predict what
comes next?
