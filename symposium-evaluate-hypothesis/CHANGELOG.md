# Changelog — symposium-evaluate-hypothesis

Versions follow [semver](https://semver.org). The release tag is
`symposium-evaluate-hypothesis-v<version>`, and it is where the version lives — the skill carries
no copy of it. [README.md](README.md) has the release steps.

## 0.2.0 — 2026-11-13

Needs Symposium Skill 0.3.0, which lets a command name the member it runs as.

- **Checks what the corpus can test before reading it through**: for each claim the hypothesis
  stands on, whether any source runs the contrast and reads the readout the claim names. The
  coverage stop asks the user where none does.
- **The verdict word gives the direction of the evidence and the certainty its strength**, fixed
  in the criteria. A premise the rationale stands on can be rated *must hold*.
- **Pointers reproduce what the corpus embeds, exactly**, and keep a `download` Content locating
  the original, so the gate checks every quotation. The content is copied by script and compared,
  each quotation is tested against its pointer before submission, each artifact is validated
  first, and the first of a kind is accepted before the rest are released.
- **The Skeptic judges each claim unseen** and publishes a challenge only where it disagrees. A
  defect that looking settles goes in a Message, and a diagnosticity rating the evidence
  disproved gets a criteria correction before the verdict.
- **The verdict grounds on the reading it adopts for each claim** and carries a table of final
  verdicts. A claim contradicted at very low certainty is a caveat and leaves the outcome as it
  is. The verdict states what the outcome rests on and what each untested claim leaves standing.
- **The report keeps to a budget for each part** that the agent counts before publishing.
- **Asks before taking up an earlier evaluation** of the same hypothesis in the chosen community:
  adopt it, or start separately.
- **Keeps a folder per run** under the user's home directory, so runs work from any directory,
  several go at once on one machine, and a new agent session lists the runs in flight to resume.
- **Works in parallel**: sub-agents collect, appraise, judge, challenge and publish side by side,
  each command naming the member it runs as, in layers released as the gate accepts what each
  cites. A gate watches for the whole run under the community admin or a gate-keeper.

## 0.1.0 — 2026-11-12

The first release. A prose skill: one hypothesis and a corpus community in, an evaluation in a
second Symposium community record out.

- **Takes three inputs**: a hypothesis stated `If [Cause], then [Effect], because [Rationale]`; a
  corpus community and a handle that reads it; and an eval community, chosen from the ones the
  user administers or founded new on a local or remote data server.
- **Stands up a team of six members**, one per scientific role — Lead, Methodologist, Librarian,
  Analyst, Skeptic, Adjudicator — each publishing under one of Symposium's publishing roles, with
  the community admin running the gate.
- **Reads the corpus from the session's own copy of the record**, indexed once, and takes as
  evidence what that record embeds.
- **Cites the corpus through pointers**: an artifact in the eval community whose `download`
  Content locates the corpus artifact, carrying the passage or cells a verdict turns on.
- **Fixes the judgment before the evidence**: typed claims with importance and diagnosticity,
  named rivals with the observation that separates each, a four-question audit, and the scales
  and integration rule, all published before anything is read.
- **Collects and appraises in parallel**, with sub-agents that read and draft while the one agent
  holding the session publishes, in layers, with the gate between.
- **Judges each claim** in an Argument, behind a testability gate, and has a Skeptic challenge
  each one from the evidence alone.
- **Integrates by an ordered rule** into *stands*, *weakened* or *refuted*, with coverage and two
  verdicts: whether the cause–effect relation is decided, and whether the mechanism is.
- **Says what would settle the open points**, proposing a test only where it is targeted,
  diagnostic, feasible and decision-bearing, and abstaining with a reason otherwise.
- **Ends in one report**, a header and eight sections, the same shape for every hypothesis.
- **Keeps one working file per run**, at `.symposium-evaluate-hypothesis/run.json` in the directory
  the session is started in, so separate directories run side by side on one machine.
- **Stops for the user three times**, each as a review display with its choices: the roster, the
  claim set and criteria, and corpus coverage.

Requires the [Symposium skill](https://github.com/ndexbio/symposium/releases) installed alongside
it, and a corpus community such as [`symposium-curate-data`](../symposium-curate-data/README.md)
publishes.
