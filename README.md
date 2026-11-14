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

## Installing Skill

Each Symposium skill ships as a zip file attached on a Github release:

| Skill | Zip | Releases |
|---|---|---|
| `symposium` | `symposium_skill-<version>.zip` | [ndexbio/symposium](https://github.com/ndexbio/symposium/releases) |
| `symposium-curate-data` | `symposium-curate-data_skill-<version>.zip` | [ndexbio/symposium-skills](https://github.com/ndexbio/symposium-skills/releases) |
| `symposium-evaluate-hypothesis` | `symposium-evaluate-hypothesis_skill-<version>.zip` | [ndexbio/symposium-skills](https://github.com/ndexbio/symposium-skills/releases) |

Download `<skill>_skill-<version>.zip` from the Github release of the skill you want. The zip
follows the standard [Agent Skills](https://agentskills.io) format and is usable by any skills compatible agent. 

All skills here requires the `symposium` skill be installed first as prerequisite, which installs the same way.

**Machine wide install** - Every agent running in any directory will load the skill. Unzip the skill zip file into the conventional agent sub path under your home directory - `<USER_HOME>/.agents/skills`. If using Claude, then do `<USER_HOME>/.claude/skills` instead.

**Folder only install** - only agents running in this folder will load the skill. Unzip the skill zip file into the conventional agent sub path under that folder - `<FOLDER>/.agents/skills`. If using Claude, then do `<FOLDER>/.claude/skills` instead.

Example to install for Claude:
```
 curl -fLO https://github.com/ndexbio/symposium-skills/releases/download/symposium-curate-data-v0.2.0/symposium-curate-data_skill-0.2.0.zip
 unzip symposium-curate-data_skill-0.2.0.zip -d ~/.claude/skills
```

---

# Development

## The skeleton

A skill folder holds two kinds of file, and the line between them is what ships:

```
<skill>/
├── REHEARSAL.md    what a correct run of it looks like                ·  repository only
├── CHANGELOG.md    what each release provides                         ·  repository only
├── Makefile        lint ← build ← deploy-local                        ·  repository only
├── lint.sh         the checks `make lint` runs                        ·  repository only
├── SKILL.md        ┐  what the agent reads
├── README.md       │  what the skill does, installing it, using it
└── reference/      │  shipped in the zip, with the repository's LICENSE
    └── *.md        ┘
```

`SKILL.md`, `README.md`, `reference/` and `LICENSE` are all an installed skill has. Everything
else is a repository concern — how the skill is tested, built and released — and `make build`
keeps it out of the zip.

Because the two kinds sit in one folder, `make lint` holds one rule that is easy to break by
accident: **a shipped document links only to shipped documents, or to a full web address.** A
link from `README.md` to `CHANGELOG.md` resolves here and dangles for everyone who installed the
zip. A repository-only document may link anywhere.

`SKILL.md`'s frontmatter holds the [Agent Skills](https://agentskills.io/specification) fields
and no others: `name`, `description`, `license`, and the version under `metadata`.

## Adding a skill

1. A folder with the shape above.
2. A job in [`.github/workflows/ci.yml`](.github/workflows/ci.yml) running `make -C <skill> build`.
3. A job in [`.github/workflows/release.yml`](.github/workflows/release.yml) under the tag prefix
   `<skill>-v`, copied from the one that is there.
4. Its own `README.md`, `REHEARSAL.md` and `CHANGELOG.md`.

## Building and releasing

```sh
make -C <skill> lint            # frontmatter, foreign references, links, orphans
make -C <skill> build           # lint, then dist/<skill>_skill-0.0.0-dev.zip
make -C <skill> build VERSION=<semver>    # dist/<skill>_skill-<semver>.zip
make -C <skill> deploy-local    # build, then install from the zip into ~/.claude/skills
```

`deploy-local` installs what the zip holds, replacing any copy already there, and installs nothing
where the checks fail. `SKILLS=<dir>` sends it to another skills directory.

The zip holds one folder named for the skill, with `SKILL.md`, `README.md`, `LICENSE` and
`reference/` inside it. Its name carries the version stamped inside it.

A release is a GitHub release tagged `<skill>-v<semver>` — `symposium-curate-data-v1.0.0`. The
prefix selects the job and the rest is the version, which lives in the tag: the job passes it to
`make build`, which names the zip for it and writes it into the skill's frontmatter, as
`metadata.version`, on the way in. So a release is named in one place, an installed skill says
which one it came from, and there is nothing in the repository to keep in step. A local
`make build` stamps `0.0.0-dev`, so a copy installed from a working tree stays distinguishable
from a released one.

### Release steps

1. **Add the release's section to the skill's `CHANGELOG.md`**, ending with the *Install
   Skill Instructions* link, and commit it.
2. **Check it builds**: `make -C <skill> build`. That is the command the workflow runs.
3. **Publish a GitHub release** whose tag is `<skill>-v<semver>`. The prefix is how
   [release.yml](.github/workflows/release.yml) selects the job, and the semver after it is the
   version being released.
4. **Watch the job.** It builds the skill with that semver and attaches
   `<skill>_skill-<semver>.zip` to the release, which is the file a user installs.

The trigger is a **published release**; a pushed tag on its own leaves the workflow idle. Create
the release in the GitHub UI, or with `gh release create <skill>-v<semver>`. Each skill releases
on its own prefix, so a tag naming one leaves the others alone.

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

The QA directory holds the installed skills and nothing else. A run's state lives under your home
directory, in `~/.symposium-<skill>/`, and each skill's rehearsal says how to clear it.

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
