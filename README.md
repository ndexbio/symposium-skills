# symposium-skills

Agent skills built on [Symposium](https://github.com/ndexbio/symposium), a specification and
toolchain for a community record: an append-only graph in which members of a scientific community
publish immutable artifacts, each connected to the material it rests on.

Each skill here does work that happens *around* a record — before it, beside it, after it — and
leaves the record itself to the Symposium skill. Every skill in this repository therefore requires
the Symposium skill installed alongside it.

| Skill | What it does |
|---|---|
| [`symposium-curate-data`](symposium-curate-data/README.md) | Takes one hypothesis, finds the scientific sources that bear on it, and publishes them into a community record as a grounded corpus |
| [`symposium-evaluate-hypothesis`](symposium-evaluate-hypothesis/README.md) | Takes one hypothesis and the community holding its corpus, evaluates the hypothesis against that corpus with a team of members, and publishes the claims, the arguments, the verdict and a report into a second community record |

## Installing a skill

Download the skill's zip from a release and unzip it into a skills directory:

```sh
unzip -o symposium-curate-data_skill.zip -d ~/.claude/skills/
```

That lands the skill folder at `~/.claude/skills/<skill>/`, where an agent finds it. Unzipping
into a project's `.claude/skills/` instead scopes the skill to that project. Install Symposium the
same way, from [its releases](https://github.com/ndexbio/symposium/releases).

---

# Development

## The skeleton

A skill folder holds two kinds of file, and the line between them is what ships:

```
<skill>/
├── README.md       what the skill does and how to install it          ·  repository only
├── REHEARSAL.md    what a correct run of it looks like                ·  repository only
├── Makefile        lint ← build ← deploy-local                        ·  repository only
├── SKILL.md        ┐
└── reference/      │  shipped in the zip
    └── *.md        ┘
```

`SKILL.md` and `reference/` are all an installed skill has. Everything else is a
repository concern — how the skill is described, tested and built — and `make build` keeps it out
of the zip.

Because the two kinds sit in one folder, `make lint` holds one rule that is easy to break by
accident: **a shipped document links only to shipped documents.** A link from `SKILL.md` to
`README.md` resolves here and dangles for everyone who installed the zip. A repository-only
document may link anywhere.

## Adding a skill

1. A folder with the shape above.
2. A job in [`.github/workflows/ci.yml`](.github/workflows/ci.yml) running `make -C <skill> build`.
3. A job in [`.github/workflows/release.yml`](.github/workflows/release.yml) under the tag prefix
   `<skill>-v`, copied from the one that is there.
4. Its own `README.md` and `REHEARSAL.md`.

## Building and releasing

```sh
make -C <skill> lint            # frontmatter, foreign references, links, orphans
make -C <skill> build           # lint, then dist/<skill>_skill.zip
make -C <skill> deploy-local    # build, then install from the zip into ~/.claude/skills
```

`deploy-local` installs what the zip holds, replacing any copy already there, and installs nothing
where the checks fail. `SKILLS=<dir>` sends it to another skills directory.

The zip holds one folder named for the skill, with `SKILL.md` and `reference/` inside it.

A release is a GitHub release tagged `<skill>-v<semver>` — `symposium-curate-data-v1.0.0`. The
prefix selects the job and the rest is the version, which lives in the tag: the job passes it to
`make build`, which writes it into the skill's frontmatter on the way into the zip. So a release is
named in one place, an installed skill can still say which one it came from, and there is nothing
in the repository to keep in step. A local `make build` stamps `0.0.0-dev`.

Publishing the release is the trigger; a pushed tag on its own leaves the workflow idle.

## Testing a skill: its rehearsal

Skills are prose, so what is checkable about them is whether an agent reading them does the right
thing. CI answers whether a skill is well formed. A skill's `REHEARSAL.md` answers whether it
works, and it is **the expected outcomes for that skill's prose as it stands**.

Run one like this:

```sh
make -C <skill> deploy-local SKILLS=~/dev/qa-<skill>/.claude/skills
cd ~/dev/qa-<skill> && claude
```

Then paste the rehearsal's prompt — **only the prompt** — and drive the run from there, reading the
rest of `REHEARSAL.md` yourself to judge what comes back.

Two things about that recipe carry the whole method:

**A fresh session.** A session that has been discussing the prose fills its gaps from memory
without noticing, and the gaps are the thing being looked for. A session holding only the installed
documents has no choice but to show where they are thin. It also tests two things nothing else
reaches: whether the skill's `description` routes a real user's phrasing to it at all, and whether
the release zip installs and loads.

**Only the prompt.** The rehearsal states what is supposed to happen; an agent that reads it
performs those expectations rather than revealing whether the skill produces them unaided. The
document is for you, not for the agent under test.

### Reading the result

A rehearsal marks which of its expectations hold still. A departure from one of those is a
regression. Results that vary run to run — which papers a search returns, which of them are open,
which fail to retrieve — vary because the world does, and mean nothing.

### Keeping it worth having

**A change that intentionally alters behaviour updates that skill's rehearsal in the same commit.**
Expectations left to rot describe a skill that no longer exists, and a run against them fails for
reasons nobody can tell apart from defects.
