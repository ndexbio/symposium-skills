# symposium-evaluate-hypothesis

An agent skill that evaluates one scientific hypothesis against a curated corpus and publishes the
evaluation into a [Symposium](https://github.com/ndexbio/symposium) community record.

Give it a hypothesis stated `If [Cause], then [Effect], because [Rationale]`, the community that
holds the corpus for it, and a community to evaluate in. A team of six members breaks the
hypothesis into testable claims, fixes how they will be judged, reads the corpus against them,
argues each claim, challenges those arguments, and reaches a verdict. It ends with a report in a
fixed format, the same for every hypothesis.

## What you need

**The Symposium skill**, installed alongside this one, from
[its releases](https://github.com/ndexbio/symposium/releases). Everything this skill reads and
publishes goes through Symposium: the sessions, the memberships, the validation, the publishing
and the gate.

**A corpus community**, and a handle on this machine that can read it. The
[`symposium-curate-data`](../symposium-curate-data/README.md) skill builds one from a hypothesis.

**Somewhere to evaluate**: a community you administer, or a data server you can found one on.
Symposium will take you through standing up a local data server if you have not got one.

## Installing

```sh
unzip -o symposium-evaluate-hypothesis_skill.zip -d ~/.claude/skills/
```

Or into a project's `.claude/skills/` to scope it to that project.

## What a run looks like

Say what you want — a hypothesis, where its corpus is, and that you want it evaluated in Symposium.

1. **It takes three inputs**: the hypothesis; the corpus community and a handle that reads it,
   chosen from the ones this machine holds; and the community to evaluate in, chosen from the ones
   you administer or founded new.
2. **It shows you the team** — Lead, Methodologist, Librarian, Analyst, Skeptic, Adjudicator — and
   the handle each will publish as. You approve or change it, and it invites the members.
3. **It frames the evaluation** as a goal in the record.
4. **It breaks the hypothesis into claims**, names the rival explanations, and fixes the scales
   and the rule it will judge by. You see all of it before any evidence is read.
5. **It reads the corpus** against every claim, in parallel where it can, and appraises what it
   finds.
6. **It judges each claim** in an Argument grounded on the corpus sources.
7. **It judges each claim a second time, unseen**, and publishes a challenge wherever the second
   judgment differs from the first.
8. **It reaches a verdict** — stands, weakened or refuted — with how certain, what the outcome
   rests on, and how much of the hypothesis the corpus could test. Claim by claim, the record
   shows whose reading was adopted.
9. **It says what would settle the open points**, or why nothing would.
10. **It writes the report**, publishes it, and shows it to you.

## The three places it stops

**The team**, before anyone is invited. **The claims and criteria**, before evidence is read.
**Corpus coverage**, only where no source in the corpus runs the test that a claim the hypothesis
depends on needs. Each stop offers its choices as a list.

Where the community you choose already holds an evaluation of the same hypothesis, it also asks
whether to carry that one on or start a separate one.

## What it asks of you

**A hypothesis with all three clauses.** The rationale is what the mechanism claims are drawn
from.

**Attention at the claims.** How a hypothesis is split into claims decides what the evaluation
can find, and the record is append-only.

**A corpus gathered for this hypothesis.** The evaluation says what that body of evidence
supports. Where the corpus cannot reach a claim, the report says so.

## Where a run keeps its state

A run writes one working file, **`.symposium-evaluate-hypothesis/run.json`, in the directory you
start the agent in**. It is how a run survives being stopped: it holds the hypothesis, the two
communities, the team, and what has been decided and published so far.

- **One run to a directory.** Start the agent in a different directory and you get a separate
  run, so several can go at once on one machine.
- **Resume from the same directory.** A session opened anywhere else finds no run and offers to
  start a new one.
- **It holds names, and no keys.** Communities and handles are in it; credentials stay with
  Symposium. Where the directory is a git repository, add `.symposium-evaluate-hypothesis/` to its
  `.gitignore`.
- **Deleting the folder forgets the run.** What the run published stays in the record.

## What it reads, and where it publishes

It reads the corpus community's record through a copy Symposium keeps on your machine, and
publishes into the eval community. The corpus is the whole of its evidence. Each source it relies
on is copied into the eval community exactly as the corpus holds it, with a link back, so every
quotation in the evaluation can be checked there.

## Release steps

A release is what puts an installable zip in front of a user, and it is driven entirely by the tag.

1. **Add the release's section to [CHANGELOG.md](CHANGELOG.md)** and commit it.
2. **Check it builds**: `make build`. That is the same command the workflow runs.
3. **Publish a GitHub release** whose tag is `symposium-evaluate-hypothesis-v<semver>` — for
   example `symposium-evaluate-hypothesis-v0.1.0`. The prefix is how
   [release.yml](../.github/workflows/release.yml) selects the job, and the semver after it is the
   version being released.
4. **Watch the job.** It builds the skill with that semver and attaches
   `symposium-evaluate-hypothesis_skill.zip` to the release, which is the file a user installs.

The tag is where the version lives, so there is nothing to set beforehand and nothing that can
disagree with the tag you cut. The build writes it into `SKILL.md`'s frontmatter on the way into
the zip, which is how an installed skill can say which release it came from. Your own
`make build` stamps `0.0.0-dev`, so a copy installed from this working tree stays distinguishable
from a released one; `make build VERSION=<semver>` stamps whatever you give it.

The trigger is a **published release**, so a pushed tag on its own leaves the workflow idle. Create
the release in the GitHub UI, or with
`gh release create symposium-evaluate-hypothesis-v<semver>`.

Each skill in this repository releases on its own prefix, so a tag naming one leaves the others
alone.

---

Developing this skill: the repository's [README](../README.md),
[REHEARSAL.md](REHEARSAL.md) for what a correct run looks like, and
[CHANGELOG.md](CHANGELOG.md) for what each release changed.
