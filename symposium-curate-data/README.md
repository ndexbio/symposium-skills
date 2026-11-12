# symposium-curate-data

An agent skill that takes one scientific hypothesis and builds a grounded corpus for it in a
[Symposium](https://github.com/ndexbio/symposium) community record.

Give it a hypothesis stated `If [Cause], then [Effect], because [Rationale]`. It searches the
literature and the data repositories for the works that bear on it, expands one citation hop,
works out what it can actually retrieve, shows you the result, and — once you approve — publishes
each source as a `ScientificPublication` with the passages, tables and Argument that ground on it.

## What you need

**The Symposium skill**, installed alongside this one, from
[its releases](https://github.com/ndexbio/symposium/releases). Everything this skill produces
reaches a record through Symposium: the session, the community membership, the validation, the
publishing and the gate. Symposium will also take you through standing up a data server and
founding a community if you have not got one.

**A session and a community** you are a member of. Symposium owns both, and this skill asks it.

## Installing

```sh
unzip -o symposium-curate-data_skill.zip -d ~/.claude/skills/
```

Or into a project's `.claude/skills/` to scope it to that project.

## What a run looks like

Say what you want — a hypothesis, and that you want a corpus for it in Symposium.

1. **It reads the hypothesis** into facets: the entities, methods, populations and outcomes that
   become the run's search vocabulary. You see them before anything is searched.
2. **It asks for the scale.** Two numbers — how many works to keep as starting points, and how
   many the finished corpus should hold. Defaults are 10 and 40.
3. **It searches**, in four query families built from the three clauses, including a deliberate
   search for work that contradicts the hypothesis.
4. **It expands one hop** from those starting points — backward into references, forward into
   citations, sideways through co-citation.
5. **It works out access** for each source, descending from the publisher's open text through
   mirrors, preprints, author deposits and deposited data.
6. **It shows you the corpus** as a table, one row per source, with what it could retrieve and
   what it could not. You work the table until you are happy: reject rows, retry them, keep closed
   ones as citations, add sources it missed, or start over.
7. **It hands the corpus to Symposium**, which publishes it.

## The two places it stops

**The scale**, before anything is searched. **The table**, before anything is published. Nothing
reaches the record until you approve that table.

## What it asks of you

**A hypothesis with all three clauses.** The rationale is the one people leave out, and it is what
a third of the search looks for.

**Attention at the table.** It is the only review gate, and the record is append-only — what gets
published cannot be withdrawn.

**Time for the publishing.** Each source becomes several artifacts, and Symposium submits them
serially with the gate between dependent ones. Forty sources is a long stretch, and it is meant to
be taken in sittings: the run records what it has published and resumes where it stopped.

## Where it draws a line

It reaches sources the way any reader without a subscription does — the open copy, a mirror, the
preprint, an author's deposit, the data, or the abstract — and it leaves a host alone when the
host has asked automated clients to stay away. Credentials, institutional proxies and ways around
a paywall are outside what it does.

Where you have lawful access to something it could not reach, the table tells you which sources
those are, and you can add a copy you obtained yourself. It records that provenance on the
artifact.

## Release steps

A release is what puts an installable zip in front of a user, and it is driven entirely by the tag.

1. **Add the release's section to [CHANGELOG.md](CHANGELOG.md)** and commit it.
2. **Check it builds**: `make build`. That is the same command the workflow runs.
3. **Publish a GitHub release** whose tag is `symposium-curate-data-v<semver>` — for example
   `symposium-curate-data-v0.1.0`. The prefix is how [release.yml](../.github/workflows/release.yml)
   selects the job, and the semver after it is the version being released.
4. **Watch the job.** It builds the skill and attaches `symposium-curate-data_skill.zip` to the
   release, which is the file a user installs.

The tag is where the version lives, and the skill holds no copy of it — so there is nothing to set
beforehand and nothing that can disagree with the tag you cut.

The trigger is a **published release**, so a pushed tag on its own leaves the workflow idle. Create
the release in the GitHub UI, or with `gh release create symposium-curate-data-v<semver>`.

Each skill in this repository releases on its own prefix, so a tag naming one leaves the others
alone.

---

Developing this skill: the repository's [README](../README.md),
[REHEARSAL.md](REHEARSAL.md) for what a correct run looks like, and
[CHANGELOG.md](CHANGELOG.md) for what each release changed.
