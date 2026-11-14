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

**A community** you are a member of, joined on this machine. Symposium owns the membership, and
this skill asks it which ones the machine holds.

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

**A look at the content line.** Under the review table it says how many sources will enter the
record with something readable, in all and for each clause. A corpus is only as useful as that
number: a source kept as a citation can be cited and carries no evidence.

**Time for the publishing.** Each source becomes several artifacts, published in order within
the source, with a gate watching throughout and sources going side by side where the agent has
sub-agents. Forty sources is a long stretch, and it is meant to be taken in sittings: the run
records what it has published and resumes where it stopped.

## Where a run keeps its state

Each run has a folder of its own, **`~/.symposium-curate-data/runs/<run>/`**, named for the
community it publishes to and a short name drawn from the hypothesis. Its working file,
`run.json`, is how a run survives being stopped: it holds the hypothesis, who it publishes as,
every source, and what has been decided and published so far.

- **Runs belong to the machine, and work from any directory.** Start the agent wherever you
  like.
- **Several runs go at once.** Each agent session works one run, and a run is worked by one
  agent session at a time. `~/.symposium-curate-data/current/` records which agent session has
  which.
- **Resuming.** A new agent session lists the runs in flight and asks which to carry on, or
  whether to start a new one. A run another agent session is working shows as in use.
- **One machine.** A run is resumed on the machine it was started on. Two machines working one
  run, or a run folder on a drive they share, is unsafe: nothing coordinates them.
- **It holds names, and no keys.** Communities and handles are in it; credentials stay with
  Symposium.
- **Deleting a run's folder forgets the run.** What the run published stays in the record.

## Working in parallel

Several agents can curate on one machine at the same time, and one agent publishes several
sources at once through its sub-agents. Every command the skill issues names the member it runs
as, so runs do not disturb each other or whatever else you are doing with Symposium. One gate
decides for a community at a time; the skill starts one and Symposium keeps exactly one working.
The Symposium skill's "Agent runtime" section has the full rules, including what is unsafe
across machines.

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
4. **Watch the job.** It builds the skill with that semver and attaches
   `symposium-curate-data_skill.zip` to the release, which is the file a user installs.

The tag is where the version lives, so there is nothing to set beforehand and nothing that can
disagree with the tag you cut. The build writes it into `SKILL.md`'s frontmatter on the way into
the zip, which is how an installed skill can say which release it came from. Your own
`make build` stamps `0.0.0-dev`, so a copy installed from this working tree stays distinguishable
from a released one; `make build VERSION=<semver>` stamps whatever you give it.

The trigger is a **published release**, so a pushed tag on its own leaves the workflow idle. Create
the release in the GitHub UI, or with `gh release create symposium-curate-data-v<semver>`.

Each skill in this repository releases on its own prefix, so a tag naming one leaves the others
alone.

---

Developing this skill: the repository's [README](../README.md),
[REHEARSAL.md](REHEARSAL.md) for what a correct run looks like, and
[CHANGELOG.md](CHANGELOG.md) for what each release changed.
