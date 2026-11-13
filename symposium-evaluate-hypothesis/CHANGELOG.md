# Changelog — symposium-evaluate-hypothesis

Versions follow [semver](https://semver.org). The release tag is
`symposium-evaluate-hypothesis-v<version>`, and it is where the version lives — the skill carries
no copy of it. [README.md](README.md) has the release steps.

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
- **Stops for the user three times**, each as a review display with its choices: the roster, the
  claim set and criteria, and corpus coverage.

Requires the [Symposium skill](https://github.com/ndexbio/symposium/releases) installed alongside
it, and a corpus community such as [`symposium-curate-data`](../symposium-curate-data/README.md)
publishes.
