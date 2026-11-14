# Changelog — symposium-curate-data

Versions follow [semver](https://semver.org). The release tag is `symposium-curate-data-v<version>`, and it
is where the version lives: the build stamps it into the zip's name and into the skill's
frontmatter, as `metadata.version`. The repository's
[README](../README.md#building-and-releasing) has the release steps.

## 0.2.0 — 2026-11-13

Needs Symposium Skill 0.3.0, which lets a command name the member it runs as.

- **Each run has its own folder** under the user's home directory, named for its community and
  a short name drawn from the hypothesis. Runs work from any directory, several go at once on
  one machine, and a new agent session lists the runs in flight to resume.
- **Every command names the member it runs as**, taken from Symposium's listing, so a run works
  beside other runs and other Symposium work.
- **A gate watches for the whole of publishing**, started by the run under a user context that
  holds the `gate` grant.
- **Sources publish side by side** through sub-agents, each source in order within itself.
- **A readable copy is a retrieved source**: publisher HTML and a PDF with a text layer are
  quoted from, with rules for rendering them.
- **Selection follows the hypothesis**: every result that bears on a clause is taken, the
  contrary ones included, with the conditions it holds under.
- **The review shows how much of the corpus carries content**, in all and by clause.
- **The release zip is `symposium-curate-data_skill-<version>.zip`** and holds one folder in the
  Agent Skills format, with this skill's README and licence inside it. The skill's frontmatter
  holds the Agent Skills fields: `license`, and its version under `metadata`.

### Installing Skill

[Installing](README.md#installing): the skills directory for Claude Code, Codex, Gemini CLI,
GitHub Copilot and Cursor, and the commands that remove an installed copy and unzip this
release.

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
