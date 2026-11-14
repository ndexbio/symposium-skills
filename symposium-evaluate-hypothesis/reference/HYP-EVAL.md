# Evaluating the hypothesis

The scientific process, start to finish, and the housekeeping that lets a team carry it out in a
community record.

You arrive here with a hypothesis, a corpus community and the handle that reads it, and an eval
community with its admin. You leave with a verdict the record can show its reasons for, and a
report.

## Four rules stand for the whole run

**Evidence comes from the corpus.** What the corpus record embeds — quoted passages, data tables,
extracted Arguments — is the evidence base. A location that leads outside the data server stays
unfollowed, and a search of the web or of your own recall adds nothing an Argument may rest on. An
evaluation is a statement about what this body of evidence supports, and it only means that while
the body is fixed.

**The corpus community is read.** Sync it as the corpus reader and read that copy. Everything this
run publishes, and every Message it sends, goes to the eval community.

**Every command names its member.** You and your sub-agents act on Symposium as the member whose
role the work belongs to, by that member's user context.
[Who acts, and as whom](#who-acts-and-as-whom) sets it out.

**The record carries the reasoning.** Each phase ends in something published, by the member whose
role it is. A conclusion that exists only in the conversation is one a reader cannot contest.

## What the process rests on

Each phase below applies one of these. They are stated once so the phases can be short.

| Principle | Tradition | What it makes you do |
|---|---|---|
| A prediction that held supports weakly; one that failed can rule out | Hypothetico-deductive method | State, for every claim, what would count against it, and look for it |
| A prediction follows from the hypothesis plus assumptions | Duhem; critiques of the method | Name the assumptions first, and assign a failed prediction to the hypothesis or to a named assumption |
| Decide how to judge before looking | Preregistration | Publish claims and criteria before reading evidence; label later additions exploratory |
| Evidence counts as far as it separates the hypothesis from its rivals | Strong inference; analysis of competing hypotheses; the likelihood ratio | Name the rivals and what each predicts differently; rate diagnosticity |
| Agreement is evidence only where the check could have failed | Severe testing | Ask of each supporting item whether it would have looked different were the claim false |
| Weigh reliability, relevance and consistency | Weight-of-evidence frameworks; GRADE | Appraise in fixed domains and give a reason for every rating |
| Agreement across methods with unrelated biases outweighs repetition | Triangulation | Group sources by independence and by kind of evidence |
| Causal claims have known probes | Bradford Hill's viewpoints | Put them to each causal claim as questions |
| Say how sure, in fixed words | Calibrated language | Use the two scales below, and only those words |

## The team

Six members of the eval community, one per scientific role, and the account its gate runs as.

| Member | Publishing role | Does | Publishes |
|---|---|---|---|
| **Lead** | `principal` | Frames the evaluation: the question, the scope, the corpus as evidence base, what a complete result is | the `ResearchGoal` |
| **Methodologist** | `hypothesize` | Decomposes the hypothesis; writes claims, rivals and criteria; later proposes what would settle the open points | `NonGroundable`: the claim set and criteria; a criteria correction, where one is needed; the proposed tests |
| **Librarian** | `importer` | Makes the pointers | `ScientificPublication` and `Data` pointers |
| **Analyst** | `researcher` | Collects and appraises evidence, and judges each claim | one `Argument` per claim |
| **Skeptic** | `critic` | Judges each claim unseen, then challenges the Analyst's Argument where it disagrees | Arguments that contest or qualify; Messages reporting a defect |
| **Adjudicator** | `researcher`, then `scout` | Decides, claim by claim, whose reading stands; integrates them into the overall verdict; writes the report | the verdict `Argument`; an `Argument` on a claim where it adopts neither reading; the report, a `NonGroundable` |

The **gate** runs as a user context that holds the `gate` grant — the community admin from the
third input, or a gate-keeper — and that account authors nothing. The Lead and the gate's account
are different: setting what is investigated and deciding what is accepted are two hands.

**The separation is the method.** The Methodologist fixes the criteria before the Analyst reads
evidence. The Skeptic reaches its own verdict from a claim and its evidence alone, before it sees
the Analyst's. The Adjudicator judges between them, and writes on a claim only where it can adopt
neither reading. With sub-agents, each role reasons in a context of its own. With
a single agent the separation is procedural, and you say so in the report: the order in which the
gate accepted things is then the proof that the criteria came before the evidence.

### Settle the roster with the user

This is the run's first stop. Draw it as a [review display](#the-review-display):

- **Table** — role · publishing role · handle · *existing* or *to invite*.
- **Synopsis** — how many members exist already and how many will be invited.
- **Choices** — **Approve** · **Change** (rename a handle, or give a role to a member the
  community already has) · **Cancel**.

Handles default to the role names in lowercase letters: `lead`, `methodologist`, `librarian`,
`analyst`, `skeptic`, `adjudicator`. Where the community already has members with user contexts
on this machine, offer them against the roles and invite only what is missing.

Then, as the community admin, invite each missing member with the access a member needs to publish
to every collection, and join each on this machine. Invites and keys move as files. Take each
member's `user_context` from Symposium's listing, and write the roster — role, handle, publishing
role, user context — into the working file the moment it is settled, with the gate's user
context beside it.

## Who acts, and as whom

Symposium runs a command as the user context named on it, so one agent session works as every
member of the team at once.

**Name the member on every command.** Each Symposium command carries the user context of the
member whose role the work belongs to, exactly as the roster records it. Read `session` in the
report to confirm it. Nobody changes the agent session's current context during a run.

**Sub-agents read, draft, validate and publish, and you should use them.** Give a sub-agent:

- its role's brief, and the one user context and publishing role it acts as;
- the names of the artifacts it owns, so that no two publish one name;
- the corpus index, the paths of the files it reads, and the scratch folder, every one as an
  absolute path.

Put this in every brief, in these words or close to them: *name your user context on every
Symposium command, and use no other; publish only the artifacts named here; return a file per
artifact saying what you submitted and what became of it.*

**You hold the order and the record of the run.** An artifact cites only what the gate has
accepted, so release a layer to sub-agents once what it cites is in the record. You are the one
writer of the working file: a sub-agent returns a file, and you record it.

**Where the work fans out, fan it out.** Five kinds of work are wide and independent, and running
them serially is the slowest way to get the same answer:

- **collecting** — one sub-agent per batch of at most five sources, each reading its sources
  against every claim;
- **appraising** — the same batches, in the same pass or a second;
- **pointers** — the Librarian's, a batch of sources to a sub-agent, each published as it is
  made;
- **judging** — one analyst per claim, given that claim's items and their appraisal, publishing
  its claim's Argument;
- **challenging** — one skeptic per claim, given the claim, its items and their appraisal, and
  nothing of the Analyst's reasoning until its own verdict is filed.

**One claim to a sub-agent** in judging and in challenging, so that a verdict on one claim is not
read into the next. Where claims are grouped to save time, the brief says to finish and file one
before reading the next, and the report says they were grouped.

**With a single agent**, do each role's work in turn, naming that role's user context on each
command.

## Read the corpus once

1. Sync as the corpus reader.
2. Take the folder of the corpus reader's copy of the record from Symposium's listing of the
   user contexts on this machine. Each accepted artifact is one file there, in the community's
   canonical form; the community's documents define that form, and you read them for it rather
   than inferring it.
3. Build **one index** in the scratch folder: name, type, title, authors, what each Argument and
   each data artifact cites, and which artifact supersedes which. Where one supersedes another, the
   index keeps the superseding one.
4. Hand sub-agents the index and the paths they own. Nobody scans the copy twice.

A source the corpus holds as a citation alone, or whose narrative it declares ungroundable, carries
no evidence. Enter it in the index as a **corpus gap**.

Follow addresses inside the copy to walk from an extracted Argument to the publication it was read
out of. The corpus's Arguments are a guide to what each source claims and where; what you rest a
judgment on is the passage or the table they point to.

## Citing the corpus

A Ground cites an address in its own record, and the corpus is another record. The bridge is a
**pointer**: an artifact in the eval community that stands for one corpus source and carries what
the corpus embeds of it.

**Make a pointer for each corpus source a judgment relies on.** The Librarian publishes it, as the
same type the corpus gave it. It carries:

- **the content, reproduced exactly** — the quoted text or the data values the corpus artifact
  embeds, character for character, as content a Ground may cite. Where that content is larger than
  the size at which the community's embedding policy asks for review, carry the passages and the
  cells the judgments rely on, each exactly as the corpus has it;
- a `download` Content, marked as one a Ground may not cite, whose `location` is the URL at which
  the corpus community's data server serves that artifact — take the form of that URL from the
  server's own description of its interface — and whose `access_method` says how a reader with
  access to that community fetches it. This is the pointer's provenance;
- the authors, and the publication's own identifier, so a reader holding no access to the corpus
  can still tell which work it is;
- an `import_method` saying that the content is reproduced from an artifact in the corpus
  community, which artifact, and whether whole or in part.

**Copy by script, and compare.** Have a short script read the content out of the corpus
artifact's file in your copy of that record and write it into the pointer. Then compare the two,
byte for byte, before submitting. A passage retyped is a passage in which a dash, a space or a
Greek letter can change, and a pointer one character off is a different text under the corpus's
name.

**Grounds cite the reproduced content**, by the exact words or the exact cells. The gate then
checks every quotation against the pointer, and a reader who follows one arrives at the corpus's
own words.

**Write the corpus's artifact names as literals.** Text carried over from the corpus may name
other artifacts of that record, and may link to them. Here those names resolve to nothing, and a
link to one is a citation the gate refuses. Put each such name in a code span, and say once in the
`import_method` that names written that way belong to the corpus community.

**Where a pointer carries part of a source and a later judgment needs more**, the Librarian
publishes a superseding pointer with the further passage, and the judgment cites that one.

**What stays on trust** is whether the curator's rendering matches the original article. No record
can check that. The report says so under *Certainty and limits*.

## Publish in layers

An artifact may cite only what the gate has already accepted. So the run publishes in layers:

**goal → claim set and criteria → pointers → claim Arguments → challenges and defect Messages →
revisions and criteria corrections → the Adjudicator's own claim Arguments, where there are any →
verdict → proposed tests → report.**

A layer goes out once the layer it cites is accepted. Inside a layer nothing waits on anything
else, so its artifacts are published side by side: every pointer, every claim Argument, every
challenge.

Every artifact names the goal in `serves_goals`, and carries the run's short name in the topic part
of its artifact name, so that two evaluations in one community stay apart.

**A gate watches for the whole run.** Before the goal is submitted, start Symposium's watching
gate as a background command, under the gate's user context from the working file, and leave it
running; Symposium's own instructions for commands that keep running say how to follow it.
Symposium keeps one gate deciding for a community on a machine: where another is already
watching, yours stands by and watches from the moment that one ends, so start yours without
looking for another. A community's gate runs from one machine; where the user says it already
runs elsewhere, start none here.

**Read each decision by the artifact's name.** Accepted, the artifact is in its member's copy of
the record after a sync. Rejected, it is among the gate's replies to that member, which Symposium
lists in full on request, each with the artifact it is about. Several sub-agents publish as one
member, and each finds its own decision this way.

**Validate before every submission.** Symposium checks an artifact where it sits, before
anything is sent, with the gate's own checks against the same record. Run that check on each one,
read its findings, and submit only what passes. A pointer or an Argument with the wrong shape
then fails on this machine, where it costs nothing, and the record never sees it. The findings
the gate would print are the ones this check prints.

**Send the first of a kind alone.** Submit the first pointer by itself and wait for it to be
accepted. Do the same with the first claim Argument, and confirm that validation checked its
quotations against the pointer. Then release the rest of the layer. A fault in how pointers are
made, or in how Grounds cite them, is then met once and corrected, and the rest are built right.
Both are real artifacts of the run; nothing is published only to test.

**Where the gate refuses, report what it said and stop.** What to change is the user's decision.

## The review display

The run stops for the user three times, and each stop is drawn the same way: **a table, one line of
synopsis, then the choices**, listed last so they sit nearest the cursor.

**Offer the choices rather than printing their syntax.** Where the environment can put a list in
front of the user and take a selection, use it. Where it cannot, fall back to a short typed form.
Name each choice and what it does in a few words.

**Draw it again after every action** that is neither *Approve* nor *Cancel*. The user is about to
agree to something the record will keep, and what they agree to has to be what is in front of them.

**Cancel** ends the run where it stands. What is published stays published, the working file
stays, and you say in two or three lines what was left undone.

The three stops are the roster, above; the claim set, in phase 3; and corpus coverage, in phase 4.

---

## Phase 1 — Frame

**Lead.** Publish the goal: the hypothesis as stated; the scope it is asserted in — population,
context, conditions; the corpus community as the evidence base; and what a complete result is.

**Say that a bounded negative is a complete result.** A goal that names only the question invites
an answer whether or not the corpus can give one. *The corpus does not carry this claim* is a
finding, and the goal says so in advance.

## Phase 2 — Decompose

**Methodologist.** Split the hypothesis into its three clauses. Then write the **causal chain** the
rationale implies, link by link: the cause brings about a state; the state, through each step of
the mechanism, brings about the effect.

**List the assumptions each link needs.** A prediction follows from the hypothesis together with
things it takes for granted — that a marker reports what it is said to, that a model stands for the
population. Named now, an assumption is something a failed prediction can be assigned to. Named
afterwards, it is a rescue.

## Phase 3 — Claims, rivals, criteria

**Methodologist.** This phase fixes how the hypothesis will be judged, and it closes before anyone
reads evidence.

### Name the rivals

For this hypothesis, what else would produce the same observations? Chance; bias in how the
evidence was gathered; a confounder driving both cause and effect; the effect producing the cause;
a different mechanism between the same cause and effect. Name the ones that are live here, and for
each write **the observation on which it and the hypothesis disagree.** A rival with no such
observation cannot be separated by this evaluation; say so now.

### Write the claims

Five to ten, typed:

| Type | States | How many | May be |
|---|---|---|---|
| **Relationship** | the cause produces the effect — always `C1` | exactly one | must hold |
| **Context** | the state or condition the cause brings about | at least one | must hold, should hold |
| **Mechanism step** | one link of the rationale, as a contrast with and without the cause | at least three | must hold, should hold, nice to hold |
| **Reversal** | removing the mechanism removes the effect | at most one | must hold, should hold, nice to hold |
| **Premise** | background the hypothesis takes for granted | at most two | must hold, should hold, nice to hold |

Each claim carries: an id; its type; the statement; its scope; **what should be observed if it is
true**; **what would count against it**; the claim it builds on; and its **importance** — *must
hold* where the hypothesis fails without it, *should hold* where it is weakened, *nice to hold*
where it is only context.

Each mechanism step and reversal also carries the **rival it separates from** and a
**diagnosticity** — *high*, *moderate* or *low* — with one line of reason: how much more expected
is the predicted observation under the hypothesis than under that rival?

**Rate a premise by what the hypothesis loses without it.** Background the rationale merely
mentions is *nice to hold*. A fact the rationale stands on — that the agent it names acts in the
way it says — is a premise that *must hold*, and rating it lower puts the foundation of the
hypothesis where the integration rule cannot reach it.

**Add a claim only where it raises diagnosticity.** Ten claims that all pass under every rival
tell a reader less than three that could each have failed.

### Audit the claim set

Answer each. All four pass before the set goes to the user.

1. **Scope stripped.** Take the scope off each mechanism claim. Does what remains fail to stand as
   a plain textbook fact? A claim that is true everywhere tests nothing here.
2. **Discrimination.** Does each mechanism claim separate the hypothesis from at least one rival?
3. **Fail state.** Were every *nice to hold* claim to hold and every mechanism claim to fail, would
   you decline to call the hypothesis right?
4. **Diagnosticity.** Is at least one mechanism claim high?

Where one fails, rewrite the claims and audit again.

### Fix the criteria

Write down, in the claim set itself, the scales and the rule the run will judge by:

- **claim verdict** — *supported*, *partially supported*, *contradicted*, *mixed*, *not tested*;
- **certainty** — *high*, *moderate*, *low*, *very low*;
- **the integration rule** of [phase 9](#phase-9--integrate), word for word, with its floor.

**The verdict word gives the direction, and the certainty gives the strength.** Write this into
the criteria too, because two readers who split on it reach different outcomes from the same
evidence:

| Word | The evidence |
|---|---|
| *supported* | runs for the claim, and shows the whole of what the claim predicts |
| *partially supported* | runs for the claim, and shows part of it, or shows it by proxy |
| *contradicted* | runs against the claim |
| *mixed* | carries comparable weight for and against |
| *not tested* | nothing in the corpus could have observed what the claim predicts |

Thin evidence against a claim is *contradicted* at *low* or *very low* certainty. It is never
softened to *mixed*: the word would then be doing the certainty's work, and the rule reads the
word.

### Stop: the claim set

Before it is published, and before any evidence is read. Draw the review display:

- **Table** — claim · type · importance · diagnosticity · statement · what counts against it.
  Under it, the rivals with their separating observations, and the criteria.
- **Synopsis** — the count by type, and the audit: four passes.
- **Choices** — **Approve** · **Revise** (the user says what to change; redraft, audit again) ·
  **Regenerate** (a fresh draft from the hypothesis) · **Cancel**.

On approval, publish the claim set and criteria and let the gate accept it. From here, a change to
a claim or a criterion is a superseding artifact and a line in the report's *Method and
departures*.

## Phase 4 — Survey coverage

**Analyst.** Mark for each claim which corpus sources could bear on it. This is a map, made before
the reading, of where the corpus can speak.

**From the index, for every claim**: the sources whose subject touches it. A claim with none is
recorded **not tested**, with the gap type *corpus gap*.

**From a short read, for each must-hold and each high-diagnosticity claim**: open its candidate
sources and answer one question — *does any source run the contrast this claim names and read the
readout it names?* The answer is yes, with the source, or no. A source on the right subject that
never ran the contrast cannot test the claim, and a title does not tell the two apart. Keep the
read to that one question; collecting is phase 5. Where there are sub-agents, give each one claim.

### Stop: corpus coverage

Only where the answer is **no** for a must-hold or a high-diagnosticity claim. A corpus that
cannot test the claims the hypothesis stands on may have been gathered for a different one, and
the user should know before the run spends itself. Draw the review display:

- **Table** — claim · importance · diagnosticity · the sources that could bear on it · whether
  any runs its contrast and reads its readout.
- **Synopsis** — claims with a source, out of the total; the claims no source can test.
- **Choices** — **Continue** (those claims are expected to end *not tested*) · **Revise claims**
  (back to phase 3; the new set supersedes the old, and the report records it as a departure) ·
  **Cancel**.

## Phase 5 — Collect

**Analyst**, across sub-agents. Read what the corpus embeds for each source against **every**
claim, and for each place a source bears on a claim record one **item**:

- the claim, and the source;
- the direction — *for*, *against*, *neutral*;
- the kind of evidence — experimental, observational, mechanistic, a review's summary;
- the passage or the value, as the corpus recorded it, and where in the artifact it sits.

**Record what the source shows. Judge nothing yet.** A collector that also rules on the claim
reads the next source through its ruling. Verdicts are applied in phase 7, by the fixed rule, to
items that were gathered without one.

**Look for the contrary on purpose.** For each claim, ask which sources would be expected to show
the observation that counts against it, and read those first.

The Librarian publishes a pointer for each source that yielded an item, as the Librarian's user
context, a batch of sources to a sub-agent.

## Phase 6 — Appraise

**Analyst**, across sub-agents. Rate each item, with a reason for each rating.

**The domains.** Limitations of the study as the source reports them. Directness: how closely its
population, intervention and readout match the claim and its scope. Consistency with the other
items on the claim. Precision. Selective reporting. An item rates up for a large effect, for a
dose–response gradient, or where the plausible biases would have run against what it found.

**Two fixed labels.**

- **Tier** — *establishing*, where the item observes the readout the claim names, in the context
  the claim names; *supporting only*, where it shows an association, a context, or a reviewer's
  assertion.
- **Contrast** — whether the item compares with and without the cause, or observes one condition;
  and whether, in the population it studied, the effect could have been seen at all.

**Severity.** Would this item have come out differently were the claim false? An observation that
would have appeared either way is agreement without a test.

**Independence.** Group items that share a laboratory, a cohort or a dataset. Three papers on one
cohort are one line of evidence, and the claim's Argument says so.

**Retraction and correction**, as the corpus records them, go on the item.

## Phase 7 — Judge each claim

**Analyst.** One Argument per claim. Its primary Assertion is the claim; its scope is the claim's
scope; its Grounds are the pointers; what it takes for granted goes in as Assumptions.

**Apply the testability gate first.** A negative counts against a claim only where the study could
have observed the readout **and** the contrast. Where it could not — the wrong readout, a single
condition, a population in which the effect cannot appear — the item is uninformative, and a claim
with only such items is **not tested**. An untested claim counts neither for the hypothesis nor
against it. It does leave something standing: where the claim was to separate the hypothesis from
a rival, the Argument names that rival and says it remains unseparated.

**Then interrogate the support.** Was the full discriminating prediction observed, or the half of
it that every rival also predicts? Did the support come from an item that observes the claimed
readout, or from a proxy? **Supporting-only evidence does not carry a must-hold claim**: such a
claim is at most *partially supported*.

**Write the reasoning, then the rating.** The Argument's rationale walks the items, for and
against, and arrives at the verdict. Its verdict holds the fixed words: one of the five claim
verdicts and one of the four certainties, with the reasons certainty was rated down or up.

**Judge each claim on its own.** A strong first claim is no evidence for the third.

**Check every quotation before the Argument is submitted.** A script takes each quoted span in
the draft and tests that it appears, character for character, in the content of the pointer it
cites. On a miss the draft goes back to whoever wrote it, to take the words again from the
pointer. Do not mend a quotation to make it match: the author decides what the source said. The
same check runs on the Skeptic's Arguments and on any the Adjudicator writes.

## Phase 8 — Challenge

**Skeptic**, one per claim. Each receives the claim, its items and their appraisal.

**Judge first, unseen.** Before opening the Analyst's Argument, the Skeptic writes its own verdict
on the claim — the word, the certainty and the reasons — to a file in the scratch folder. The
brief names where the Analyst's Argument is and says to open it only once that file is written.
The questions it works through:

- **Across the rivals.** Take each item and ask of every rival: is this observation equally
  expected there? An item every rival predicts supports none of them.
- **Sensitivity.** Find the two or three items the verdict rests on. What becomes of it where one
  is wrong, retracted or dependent on another?
- **Causal probes.** For a causal claim, put Hill's viewpoints as questions — is the association
  strong, consistent across settings, in the right order in time, graded with dose, plausible,
  shown by experiment?
- **Rescue.** Has a failed prediction been absorbed by an assumption that phase 2 never named?

**Then compare, and publish only a disagreement.**

- **The two agree** in verdict and in reasoning. The Skeptic publishes nothing for that claim.
  Agreement reached unseen is a result, and a stronger one than a contest written to fill a slot.
  The sub-agent says so in the file it returns, and you record it in the working file; the
  Adjudicator names those claims in the verdict and the report.
- **They differ on the judgment.** The Skeptic publishes an Argument that contests or qualifies,
  in the manner the community's discourse policy and the critic's charter set out.
- **The Analyst's Argument holds a defect that looking settles** — a value misread, a figure
  reported as absent that is there. That is a defect report, and it goes in a Message.

The Analyst then answers each in one of two ways: supersede the claim's Argument, saying what
changed and why; or let it stand. Where both stand, the disagreement is the record's, and the
Adjudicator decides it.

**Where the evidence shows a diagnosticity rating was wrong** — a rival turns out to predict the
very observation a claim was rated *high* for — the Methodologist publishes a **criteria
correction** before the verdict: the claim, the rating as fixed, the corrected rating, and the
item that showed it. The claim set stays as it was accepted. The correction is a departure, and
the report lists it.

## Phase 9 — Integrate

**Adjudicator.** One Argument whose primary Assertion is the hypothesis.

**Decide each claim first, and ground on the reading you adopt.** For every claim there is the
Analyst's Argument and, where the Skeptic disagreed, the Skeptic's. Adopt one, and ground the
verdict on that Argument's primary Assertion; grounding on it is how the record shows it was
accepted. Where you can adopt neither, publish an Argument of your own on that claim, let the gate
accept it, and ground on that. A final verdict on a claim that exists only in your rationale
leaves the claim's own Argument saying something else, and a reader who starts there never learns
it was overturned.

**Put the decisions in a table** in the verdict: claim · final verdict · final certainty · the
address of the Argument adopted · whether the Skeptic agreed unseen.

**The rule, in order; the first that applies decides.**

1. A must-hold claim is *contradicted* on establishing evidence → the hypothesis is **refuted**.
2. A should-hold claim is *contradicted*, or a must-hold claim is contradicted on supporting-only
   or low-certainty evidence → **weakened**.
3. Otherwise → **stands**.

**The floor.** A claim contradicted at *very low* certainty triggers neither limb. Name it in the
verdict as a caveat. Without the floor a single weak item against any claim would decide the
outcome, and the outcome would stop telling hypotheses apart.

**Apply the rule to the corrected criteria.** Where a diagnosticity rating was corrected in phase
8, the verdict takes no strength from the rating as first fixed.

Certainty in the outcome is no higher than the lowest certainty among the must-hold claims.

**State the basis.** The first limb needs establishing evidence, and a corpus drawn from published
papers often holds none against a mechanism claim: the measurements are in another tissue, on
another agent, or by proxy. A hypothesis can then be contradicted on every mechanism claim and
come out *weakened*. So say which it is — the outcome rests on **evidence for the hypothesis**, or
on there being **no establishing evidence against it** — and give the number of establishing items
that bear on the mechanism claims.

**Report coverage**: claims tested, out of the total. *Stands* at three claims tested of nine is a
different statement from *stands* at nine of nine, and the verdict says which.

**Say what each untested claim leaves standing.** For every high-diagnosticity claim that ended
*not tested*, name the rival it was to separate and the evidence that rival has in the corpus. A
rival with its own necessity evidence and no test against it is the main finding about the
mechanism, and *not tested* alone hides it.

**Give two verdicts.** Is the **cause–effect relation** decided — does the relationship claim hold
or fail on establishing evidence? Is the **mechanism** decided — are the high-diagnosticity claims
supported and the live rivals ruled out? *The effect is real and the mechanism is not yet
separated from a rival* is a common and correct result; state it as one.

**Where your judgment departs from the rule, say so and why**, in the rationale. The ordinary
reasons: every supported claim passed on evidence its rival also predicts; the relationship claim
is itself untested, so everything below it is conditional; the one observation that would separate
the mechanism from a rival was never made.

## Phase 10 — What would settle it

**Methodologist.** For each claim that is not tested, low in certainty, or contested, name the
**gap**:

*not tested* · *partial coverage* · *must-hold claim contradicted* · *proxy only* · *rival not
separated* · *supporting only* · *low diagnosticity* · *premise unverified* · *conflicting
evidence* · *corpus gap*.

**Propose a test only where all four hold.**

1. **Targeted** — it names the claim or the rival it addresses.
2. **Diagnostic** — its outcomes differ between the hypothesis and a rival. A test that can only
   confirm is short of this.
3. **Feasible** — a concrete system, intervention and readout that exist.
4. **Decision-bearing** — the rule for reading the result is written now: what is expected if the
   hypothesis is true, what if it is false, and which rival the result would rule out.

**Otherwise abstain**, and say why — no feasible system, the hypothesis and the rival predict the
same under every feasible test, the claim itself is ill-posed, the point is already decided — and
what would change that. An abstention with its reason is a result.

**Rank** by how much rests on the claim and how far the outcome would move the verdict. Cost breaks
ties. *Nothing further is needed* is a valid list.

**End with one recommendation**: *accept* · *reject* · *pursue* · *pursue to discriminate* ·
*deprioritize* · *abstain*.

A corpus gap has its own remedy: the sources that would fill it, named as kinds of study, for a
further curation of the corpus.

## Phase 11 — Report

**Adjudicator.** → **[EVAL-REPORT.md](EVAL-REPORT.md)**

Fill the skeleton it carries. Every statement in the report links to the Argument it comes from;
the report asserts nothing the record does not already hold. Publish it, and show it to the user in
full.
