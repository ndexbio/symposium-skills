# The evaluation report

The run ends with one report. A header and eight sections, in this order, with these headings,
every time.

Someone comparing two evaluations, or returning to one, should find the part they want without
reading the rest, and that only works where every report has the same shape. Fill the skeleton; do
not redesign it.

**It fits on about two pages.** The record holds the full reasoning, and the report is the way
into it. Each statement links to the Argument it comes from.

## The skeleton

```markdown
# Evaluation: <the hypothesis, in a few words>

**Hypothesis** — If <cause>, then <effect>, because <rationale>.
**Eval community** — <name> · **Corpus community** — <name>
**Date** — <date> · **Evaluated by** — <model>
**Claim set and criteria** — <address> · **Verdict** — <address>

## Verdict

**<Stands | Weakened | Refuted>**, <high | moderate | low | very low> certainty.
**Cause–effect relation** — <decided for | decided against | open>.
**Mechanism** — <decided for | decided against | open, not separated from <rival>>.
**Coverage** — <n> of <n> claims tested.

<two or three sentences a non-specialist can read: what the corpus shows, and how far>

- <strongest evidence: the claim, the source, what it showed>
- <two to four of these>

Rule and judgment agree: <yes | no, and why>.

## The hypothesis as evaluated

**Cause** — <clause> · **Effect** — <clause> · **Rationale** — <clause>
**Scope** — <population, context, conditions>
**Assumptions** — <what the chain takes for granted>

## Claims and verdicts

| Claim | Type | Importance | Diagnosticity | Verdict | Certainty |
|---|---|---|---|---|---|
| C1 <short statement> | relationship | must hold | — | <verdict> | <certainty> |

### C1 — <verdict>, <certainty>

<the reasoning, quoting the source's words, arriving at the verdict>
**For** — <sources, named> · **Against** — <sources, named>
<one sentence: what this means for the claims below it>

### C2 — <verdict>, <certainty>

<reasoning> · **For** — <sources> · **Against** — <sources> · <one-sentence summary>

## Rival explanations

| Rival | Separating observation | Hypothesis expects | Rival expects | Tested | What the corpus showed | Standing |
|---|---|---|---|---|---|---|
| <rival> | <observation> | <result> | <result> | <yes, no> | <result, by source> | <ruled out, weakened, not separated> |

## Certainty and limits

**Untested predictions** — <each, with the claim it belongs to>
**Corpus gaps** — <kinds of evidence the corpus does not hold>
**Caveats** — <what qualifies the verdict>

The verdict rests on: <the two or three items it is most sensitive to>.

## What would settle it

| Open point | Gap | Test, or abstention | If true | If false |
|---|---|---|---|---|
| <claim or rival> | <gap type> | <the test, or why none> | <expected> | <expected> |

**Recommendation** — <accept | reject | pursue | pursue to discriminate | deprioritize | abstain>

## Method and departures

<the scales and the integration rule, in three or four lines; whether roles ran in separate
contexts or in one>

<what changed after the criteria were fixed, and why — or one line saying nothing did>

## Where it is

<the eval community and how to browse it; this report's address; the working file's full path>
```

## What each part is for

**The header.** Enough to tell this evaluation from another at a glance, and the two addresses a
reader needs to check it: what was to be judged, and the judgment.

**1. Verdict.** Written last, read first. The outcome and its certainty in the fixed words; the
two verdicts, because *the effect is real* and *this is why* are separate findings and a reader
needs both; coverage, because an outcome over a third of the claims is a different thing from one
over all of them. Then the bottom line in plain language, and the few items that carry it, each
naming a claim and a source.

**Say it plainly where it goes against the hypothesis.** *Refuted* and *weakened* are results, and
so is *open*. A verdict softened into agreement has spent the whole run to tell the user what they
came in believing.

**2. The hypothesis as evaluated.** What was judged, as it was read: the clauses, the scope, the
assumptions. A reader who disagrees with the verdict usually disagrees here first.

**3. Claims and verdicts.** The table for the shape, then a block per claim of **five lines at
most**. In each block the reasoning comes before the rating, and quotes the source's own words.
Evidence against gets the room evidence for gets.

**Hold the layer order**: the relationship claim, then context, then mechanism steps, then the
reversal and the premises. After the relationship claim, one sentence on what its verdict means
for everything under it; where it is untested or contradicted, the mechanism claims are
conditional and the block says so.

**Mark what is inferred.** Where the last link of the rationale is supported only through the
claims upstream of it, the block says **inferred, not observed**.

**4. Rival explanations.** One row per rival named in the claim set. *Not separated* is the
honest standing for a rival whose separating observation the corpus never made, and it is the row
that most often explains an *open* mechanism.

**5. Certainty and limits.** Three lists, kept apart because they are answered differently: an
untested prediction by an experiment, a corpus gap by more curation, a caveat by a reader's
judgment. Among the caveats, say that Grounds resting on pointers rest on trust in the corpus, and
say where the roles ran in one context. The closing line names the items the verdict would move
with.

**6. What would settle it.** The open points, each with its gap and either the test that would
close it — with what to expect either way — or the reason there is none. One recommendation, in
the fixed words.

**7. Method and departures.** The scales and the rule, briefly, so the report can be read without
the skill beside it. Then anything that changed after the criteria were fixed. Where nothing did,
say so in a line and keep the heading: a missing section reads as an omission.

**8. Where it is.** The one place for locations: the community, how to browse it, the report's
address, and the working file by its full path, since it lives in the directory the run was started
in.

## Filling it

**Names and numbers.** *Three of four mechanism claims supported, C5 contradicted by the knockout
study* tells a reader what *the evidence is broadly favourable* withholds.

**A reason beside every rating.** A certainty with no reason cannot be argued with, and the point
of publishing the evaluation is that it can be.

**Only the fixed words** for verdicts, certainties, standings, gaps and the recommendation. Two
reports can be compared only where the same word means the same thing in both.

**Keep it about the evaluation.** How the run went, what was retried, how long the gate took: that
is the agent's experience, and it belongs in none of the eight.
