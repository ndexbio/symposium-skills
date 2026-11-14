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

Download `symposium-curate-data_skill-<version>.zip` from the [releases
page](https://github.com/ndexbio/symposium-skills/releases): take the latest release whose tag
begins `symposium-curate-data-v`, since the page lists other releases too. The zip holds one
folder, `symposium-curate-data/`, in the [Agent Skills](https://agentskills.io) format, and
installing it is placing that folder in the skills directory your agent reads.

**1. Find your agent's skills directory.** It applies to every session of that agent on the
machine.

| Agent | Skills directory |
|---|---|
| [Claude Code](https://code.claude.com/docs/en/skills) — terminal, IDE extensions, and local sessions in the Code tab of the Claude desktop app | `~/.claude/skills` |
| [OpenAI Codex](https://developers.openai.com/codex/skills) | `~/.agents/skills` |
| [Gemini CLI](https://geminicli.com/docs/cli/using-agent-skills/) | `~/.agents/skills` |
| [GitHub Copilot](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) — CLI, VS Code, Visual Studio | `~/.copilot/skills` |
| [Cursor](https://cursor.com/docs/skills) | `~/.agents/skills` |
| Another agent that supports Agent Skills | the directory its documentation names, commonly `~/.agents/skills` |

Each agent's name links to its own page on skills, where the directory is stated. Checked
November 2026.

For one project only, use the same directory inside the project: `.claude/skills` or
`.agents/skills`.

**2. Remove the installed copy, then unzip.** Removing it first leaves no file behind from an
earlier release. The folder holds only the skill: your sessions, keys and runs are kept
elsewhere and stay as they are.

macOS and Linux:

```sh
SKILLS_DIR=~/.claude/skills        # your agent's directory, from the table
rm -rf "${SKILLS_DIR:?}/symposium-curate-data"
mkdir -p "$SKILLS_DIR"
unzip symposium-curate-data_skill-<version>.zip -d "$SKILLS_DIR"
```

Windows (PowerShell):

```powershell
$SkillsDir = "$HOME\.claude\skills"   # your agent's directory, from the table
if (-not $SkillsDir) { throw "set SkillsDir first" }
Remove-Item -Recurse -Force "$SkillsDir\symposium-curate-data" -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force $SkillsDir | Out-Null
Expand-Archive symposium-curate-data_skill-<version>.zip -DestinationPath $SkillsDir
```

**3. Check it.** `<skills directory>/symposium-curate-data/SKILL.md` exists. Start a new session of
your agent, or reload its skills, and ask it which skills it has.

**Install each skill in one directory.** Some agents read more than one: Cursor reads
`~/.claude/skills` as well as its own, and so does Copilot in Visual Studio and in VS Code's
local sessions. Where you run two agents that share a directory, one install serves both.

**Claude desktop app.** In the **Code** tab, start a **Local** session: it runs on your machine
and loads `~/.claude/skills`, so install as above. Cloud sessions, chat and Cowork run on
Anthropic's infrastructure and take their skills from your claude.ai account, where a zip is
uploaded under Customize > Skills. This skill works on your machine — its commands, its keys and
its runs are there — so use a Local session.

This skill is developed and tested with Claude Code. The other agents' directories are the ones
their own documentation gives.

The Symposium skill this one needs installs the same way, as `symposium`, from
[its own releases page](https://github.com/ndexbio/symposium/releases).

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

---

Releases and what each changed:
[the changelog](https://github.com/ndexbio/symposium-skills/blob/main/symposium-curate-data/CHANGELOG.md).
Building and releasing this skill:
[the repository](https://github.com/ndexbio/symposium-skills#development).
