# Changelog — symposium-curate-data

Versions follow [semver](https://semver.org). The release tag is
`symposium-curate-data-v<version>`, and it is where the version lives — the skill carries no copy
of it. [README.md](README.md) has the release steps.

## 0.1.0 — 2026-11-11

The first release. A prose skill: one hypothesis in, a grounded corpus in a Symposium community
record out.

- **Reads a hypothesis** stated `If [Cause], then [Effect], because [Rationale]` into facets —
  entities, methods, populations, outcomes — and puts them to the user before searching anything.
- **Searches** six literature indexes and five data repositories in four query families built from
  the three clauses, one of which looks deliberately for work that contradicts the hypothesis.
- **Expands one citation hop** from the strongest results — backward into references, forward into
  citing works, sideways through co-citation — bounded by the score the starting points set.
- **Settles access** down a six-rung ladder from the publisher's open text through PMC mirrors,
  preprints, author deposits and deposited data to the abstract, triaging what each host returns
  and reaching sources the way a reader without a subscription does.
- **Curates and reviews**: identity, retraction status, independence and coverage, then a table
  the user works row by row — reject, retry, keep as a citation, add a source the search missed,
  or start over — until they approve it. Nothing reaches the record before they do.
- **Hands the corpus to the Symposium skill**, which owns the data model, the extraction SOP, the
  importer role and the gate, and publishes each source as a `ScientificPublication` with the
  passages, tables and Argument that ground on it.
- **Reaches Symposium by describing the work**, in the record's own vocabulary — a session, a
  community, a Member publishing artifacts in the `importer` publishing role — so that Symposium's
  own documents decide what needs reading. The skill names no file inside Symposium and no
  layout it does not own, and a lint rule holds that line.
- **Draws a line at what may be taken** from a source: measurements are rendered as recorded,
  sentences are bounded attributed quotation, and everything derived is written fresh.

Requires the [Symposium skill](https://github.com/ndexbio/symposium/releases) installed alongside
it.
