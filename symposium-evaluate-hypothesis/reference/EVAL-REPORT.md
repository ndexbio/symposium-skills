# The evaluation report

The run ends with one report. A header and eight sections, in this order, with these headings,
every time.

Someone comparing two evaluations, or returning to one, should find the part they want without
reading the rest, and that only works where every report has the same shape. Fill the skeleton; do
not redesign it.

**The record holds the reasoning, and the report is the way into it.** Each statement gives the
address of the Argument it comes from. What does not fit a section's budget is already in an
Argument, and the report gives that address in place of the prose.

## The skeleton

```markdown
# Evaluation: <the hypothesis, in a few words>

**Hypothesis** — If <cause>, then <effect>, because <rationale>.
**Eval community** — <name> · **Corpus community** — <name>
**Date** — <date> · **Evaluated by** — <model>
**Claim set and criteria** — <address> · **Verdict** — <address>

## Verdict

**<Stands | Weakened | Refuted>**, <high | moderate | low | very low> certainty.
**Basis** — <evidence for the hypothesis | no establishing evidence against it>; <n> establishing
items bear on the mechanism claims.
**Cause–effect relation** — <decided for | decided against | open>.
**Mechanism** — <decided for | decided against | open, not separated from <rival>>.
**Coverage** — <n> of <n> claims tested.

<at most three sentences a non-specialist can read: what the corpus shows, and how far>

- <strongest evidence: the claim, the source, what it showed — one line>
- <at most four of these>

Rule and judgment agree: <yes | no, and why>.

## The hypothesis as evaluated

**Cause** — <clause> · **Effect** — <clause> · **Rationale** — <clause>
**Scope** — <population, context, conditions>
**Assumptions** — <what the chain takes for granted>

## Claims and verdicts

| Claim | Type | Importance | Diagnosticity | Verdict | Certainty | Reading adopted |
|---|---|---|---|---|---|---|
| C1 <short statement> | relationship | must hold | — | <verdict> | <certainty> | <Analyst, Skeptic, Adjudicator> |

### C1 — <verdict>, <certainty>

**For** — <sources, named, and what each showed>
**Against** — <sources, named, and what each showed>
<one sentence: what this means for the claims below it> · <address of the Argument adopted>

### C2 — <verdict>, <certainty>

**For** — <sources> · **Against** — <sources> · <one sentence> · <address>

## Rival explanations

| Rival | Separating observation | Hypothesis expects | Rival expects | Tested | What the corpus showed | Standing |
|---|---|---|---|---|---|---|
| <rival> | <observation> | <result> | <result> | <yes, no> | <result, by source> | <ruled out, weakened, not separated — and the untested claim that leaves it so> |

## Certainty and limits

**Untested predictions** — <each, with the claim it belongs to>
**Corpus gaps** — <kinds of evidence the corpus does not hold>
**Caveats** — <what qualifies the verdict>

The verdict rests on: <the two or three items it is most sensitive to>.

## What would settle it

| Open point | Gap | Test, or abstention | If true | If false |
|---|---|---|---|---|
| <claim or rival> | <gap type> | <the test, or why none> | <expected> | <expected> |

<where there are more open points than rows: the address of the proposed tests>

**Recommendation** — <accept | reject | pursue | pursue to discriminate | deprioritize | abstain>

## Method and departures

<the scales, the integration rule and its floor, in three or four lines; whether roles ran in
separate contexts or in one>

**Agreed unseen** — <the claims where the Skeptic reached the Analyst's verdict before seeing it>
**Departures** — <one line each: a corrected diagnosticity, a superseded claim set, claims judged
in groups — or one line saying there were none>

## Where it is

<the eval community and how to browse it; this report's address; the working file's full path>
```

## The budget for each part

A length the agent cannot count while writing is a length it will not keep. These can be counted.

| Part | Budget |
|---|---|
| Verdict | the five fixed lines; at most 3 sentences; at most 4 bullets of one line each; the agreement line |
| The hypothesis as evaluated | at most 100 words |
| A claim block | at most 70 words |
| Rival explanations | the table alone; at most 15 words to a cell |
| Certainty and limits | at most 5 one-line items in each of the three lists; the closing line |
| What would settle it | the table alone, at most 6 rows, the most decisive first; the recommendation |
| Method and departures | at most 120 words |
| Where it is | at most 5 lines |

**The whole follows from the counts**: about 900 words, and 90 more for each claim, and 45 more
for each rival. Ten claims and eight rivals come to about 2,200.

**Count before publishing.** Go through the draft part by part against the table, cut what is
over, and publish only then. The counts stay out of the report.

**Cut by moving to an address, never by dropping a result.** A contrary finding, an untested
claim, a rival left standing: each keeps its line. What goes is explanation the Argument already
gives.

## What each part is for

**The header.** Enough to tell this evaluation from another at a glance, and the two addresses a
reader needs to check it: what was to be judged, and the judgment.

**1. Verdict.** Written last, read first. The outcome and its certainty in the fixed words. The
**basis**, because *weakened* for want of establishing evidence against the hypothesis is a
different finding from *weakened* on evidence for it, and the word alone does not say which. The
two verdicts, because *the effect is real* and *this is why* are separate findings and a reader
needs both. Coverage, because an outcome over a third of the claims is a different thing from one
over all of them. Then the bottom line in plain language, and the few items that carry it, each
naming a claim and a source.

**Say it plainly where it goes against the hypothesis.** *Refuted* and *weakened* are results, and
so is *open*. A verdict softened into agreement has spent the whole run to tell the user what they
came in believing.

**2. The hypothesis as evaluated.** What was judged, as it was read: the clauses, the scope, the
assumptions. A reader who disagrees with the verdict usually disagrees here first.

**3. Claims and verdicts.** The table for the shape, then a block per claim. The table gives the
**final** verdict on each claim and whose reading was adopted, so a claim the Adjudicator decided
against the Analyst shows as such. Each block names the sources for and against and what each
showed; the quotations are in the Argument the block gives the address of. Evidence against gets
the room evidence for gets.

**Hold the layer order**: the relationship claim, then context, then mechanism steps, then the
reversal and the premises. After the relationship claim, one sentence on what its verdict means
for everything under it; where it is untested or contradicted, the mechanism claims are
conditional and the block says so.

**Mark what is inferred.** Where the last link of the rationale is supported only through the
claims upstream of it, the block's heading says **inferred, not observed**.

**4. Rival explanations.** One row per rival named in the claim set. *Not separated* is the
honest standing for a rival whose separating observation the corpus never made, and it is the row
that most often explains an *open* mechanism. Where an untested claim is what leaves a rival
standing, the cell names that claim.

**5. Certainty and limits.** Three lists, kept apart because they are answered differently: an
untested prediction by an experiment, a corpus gap by more curation, a caveat by a reader's
judgment. Among the caveats: every quotation was checked against the corpus's copy, and whether
that copy matches the original article rests on the curator; any claim contradicted at *very low*
certainty, which the rule's floor kept from deciding the outcome; and where the roles ran in one
context. The closing line names the items the verdict would move with.

**6. What would settle it.** The open points, each with its gap and either the test that would
close it — with what to expect either way — or the reason there is none. One recommendation, in
the fixed words.

**7. Method and departures.** The scales and the rule, briefly, so the report can be read without
the skill beside it. **Agreed unseen** is evidence about the method: two judgments made apart that
arrive at the same place. Then anything that changed after the criteria were fixed. Where nothing
did, say so in a line and keep the heading: a missing section reads as an omission.

**8. Where it is.** The one place for locations: the community, how to browse it, the report's
address, and the working file by its full path, since it lives in the directory the run was
started in.

## Filling it

**Names and numbers.** *Three of four mechanism claims supported, C5 contradicted by the knockout
study* tells a reader what *the evidence is broadly favourable* withholds.

**A reason beside every rating.** A certainty with no reason cannot be argued with, and the point
of publishing the evaluation is that it can be.

**Only the fixed words** for verdicts, certainties, standings, gaps and the recommendation. Two
reports can be compared only where the same word means the same thing in both.

**Keep it about the evaluation.** How the run went, what was retried, how long the gate took: that
is the agent's experience, and it belongs in none of the eight.
