# Sequence alignment 🧬

> **Difficulty:** 🌶️🌶️🌶️
>
> **Before you start:** basic Python.
>
> **Recommended first:** [Try, try again](../try_try_again/README.md), which introduces
> dynamic programming in one dimension.
>
> **You’ll practise:** generators and recursion, brute-force search, dynamic
> programming, two-dimensional tables, and tracing back through a table to
> recover a solution.
>
> **Check:** `uv run pytest exercises/sequence_alignment/ -q`. For the brute-force
> part only, add `-k "score_alignment or all_alignments or brute_force_finds"`.

**In this exercise:** [Naive brute force](#naive-brute-force) ·
[Dynamic programming & Needleman-Wunsch](#dynamic-programming--needleman-wunsch)

## Naive brute force

We're going to explore how to find an optimal "global" sequence alignment (one
that aligns both sequences from beginning to end) of two DNA sequences.
Throughout this exercise, a matching pair scores +1, a mismatch scores -1, and a
character aligned with a gap scores -1. Our optimal alignment is then defined as
the arrangement of the two sequences with the highest score. Our job is to find
this.

For example:

```
ATAGTC-AC-AT
AAA-TCGACAAA
```

The score is the sum across columns: equal characters contribute +1 and every
other column contributes -1.

The simplest way to find the best alignment is to try them all. In
[alignment.py](alignment.py), implement
`score_alignment(aligned_first, aligned_second)`, which scores a pair of
already-aligned strings, and `all_alignments(first, second)`, which yields every
possible alignment of two sequences. The best score is then the
maximum over all alignments. Stuck? There are 💡 hints.

<details>
<summary>💡 Hint 1: a nudge</summary>

Think about the first character of each sequence. What are the ways they can be
lined up against each other, or against a gap?

</details>

<details>
<summary>💡 Hint 2: a strategy</summary>

Either the first character of `first` is aligned with a gap, or the first
character of `second` is aligned with a gap, or the two are aligned with each
other. Whichever you choose, what remains is a smaller alignment problem, so a
recursive generator is a natural fit. A column that is a gap in both rows is
never allowed.

</details>

How far does this get you? Unfortunately, the number of possible alignments
grows **very** quickly: for two sequences of length $n = 3$ there are 63;
for $n = 7$ this grows to 48,639 and there are over eight million at $n=10$!

Time your function as the sequences get longer, then think about the 10 and 11
base example above. How long do you think it would take for two 1,000 base
sequences?

## Dynamic programming & Needleman-Wunsch

If you have completed [Try, try again](../try_try_again/README.md), you have already met dynamic
programming. This problem extends that idea from counting possibilities in one
dimension to finding optimal alignments in two dimensions.

Brute force repeats a great deal of work, because many alignments share the same
beginnings. *Dynamic programming* removes the repetition. It is a technique for
solving a big problem by solving smaller, overlapping subproblems once each and
storing the answers in a table so they can be reused rather than recomputed.
Here the subproblems are the best alignments of the beginnings (prefixes) of the
two sequences, and the table is filled in from short prefixes up to the full
sequences.

> [!NOTE]
> Despite the name, dynamic programming is not about changing data or code that
> adapts as it runs, and "programming" here means planning (as in "linear
> programming"), not writing code.

The Needleman-Wunsch algorithm is a dynamic-programming method for *global*
alignment: it aligns both sequences from beginning to end, inserting gaps
where useful. This models the idea that the sequences share an overall extent,
even if insertions or deletions have shifted later characters. It is used in
bioinformatics to compare DNA, RNA, or protein sequences.

Use a dynamic-programming table whose entry
$D_{i,j}$ is the best score for aligning the first $i$ characters of the first
sequence with the first $j$ characters of the second.
Initialise the first row and column with the cost of aligning that many
characters to gaps. Each later cell chooses the best of a match/mismatch
diagonal, a gap in the first sequence, or a gap in the second:

$$
D_{i,j}=\max\begin{cases}
D_{i-1,j-1}+s(a_i,b_j),\\
D_{i-1,j}-1,\\
D_{i,j-1}-1,
\end{cases}
\qquad
s(a_i,b_j)=\begin{cases}
+1 & a_i=b_j,\\
-1 & a_i\ne b_j.
\end{cases}
$$

Implement `needleman_wunsch_score(first, second)`, which needs only the best
score in the final cell, and `needleman_wunsch_alignment(first, second)`, which
traces back through the table to recover one optimal pair of strings. The
starter code shares a helper, `_alignment_table`, between these functions. It
allocates the table, initialises its boundaries, and supplies the traversal
loops. Your first task is to replace its scoring TODO. Think of each candidate
as "the best score for a smaller problem, plus the score for one new column".

Here is the structure in pseudocode; the scoring decisions are yours to fill in:

```text
create D with (length(first) + 1) rows and (length(second) + 1) columns
set D[0, 0] to zero
initialise the first column and first row with cumulative gap costs
for each row i from 1 to length(first):
  for each column j from 1 to length(second):
    consider ending with both characters, or with a gap in either sequence
    TODO: calculate the three candidate scores using already-filled cells
    TODO: store the best candidate in D[i, j]
return D
```

The extra row and column matter: `D[0, j]` aligns an empty first sequence with
`j` characters of the second. Table indices count characters, while Python
string indices start at zero, so the characters at cell `(i, j)` are
`first[i - 1]` and `second[j - 1]`. A diagonal move adds both characters, an
upward move adds a character from `first` against a gap, and a leftward move
adds a gap against a character from `second`. Row-by-row traversal ensures all
three neighbours have already been filled. Try drawing the table for `"A"`
and `"AA"` before tackling longer inputs.

Once the score tests pass, complete the traceback TODO. After the table is
filled, `needleman_wunsch_alignment` must recover one optimal pair of strings by
tracing back through it. The skeleton handles the boundary moves and reverses
the output for you. Stuck? There are 💡 hints.

<details>
<summary>💡 Hint 1: a nudge</summary>

Every cell's value came from one of three neighbours, plus the score of one new
column. Standing at the bottom-right cell, which move produced the value you
are looking at?

</details>

<details>
<summary>💡 Hint 2: a strategy</summary>

Walk backwards from the bottom-right cell to the top-left, at each cell choosing
a move whose neighbour score plus column score equals the current cell's score.
Do not simply choose the neighbour with the largest stored score: the score of
the new alignment column matters too. If several moves explain the current
score, choose any one. Stop at the top-left cell, not as soon as one sequence
runs out; the remaining characters must be aligned with gaps.

</details>

<details>
<summary>💡 Hint 3: an outline</summary>

```text
start at the bottom-right cell with two empty character lists
while either sequence still has characters left:
  if on the top row or left column, only a gap move is possible
  otherwise:
    TODO: choose a move whose neighbour score plus column score
        equals the current cell's score
    append that move's character/gap pair to the lists
    move to that neighbour
reverse both lists and join each into a string
```

</details>

The docstrings give the details. Check both functions against your brute-force
version on short sequences. The longer DNA fixture checks that the same
algorithm scales beyond the small worked example.
