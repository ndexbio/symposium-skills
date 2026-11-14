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
publishes goes through Symposium: the memberships, the validation, the publishing and the gate.
It needs a release that lets a command name the member it runs as.

**A corpus community**, and a handle on this machine that can read it. The
[`symposium-curate-data`](https://github.com/ndexbio/symposium-skills/tree/main/symposium-curate-data)
skill builds one from a hypothesis.

**Somewhere to evaluate**: a community you administer, or a data server you can found one on.
Symposium will take you through standing up a local data server if you have not got one.

## Installing

Download `symposium-evaluate-hypothesis_skill-<version>.zip` from the [releases
page](https://github.com/ndexbio/symposium-skills/releases): take the latest release whose tag
begins `symposium-evaluate-hypothesis-v`, since the page lists other releases too. The zip holds
one folder, `symposium-evaluate-hypothesis/`, in the [Agent Skills](https://agentskills.io) format,
and installing it is placing that folder in the skills directory your agent reads.

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
rm -rf "${SKILLS_DIR:?}/symposium-evaluate-hypothesis"
mkdir -p "$SKILLS_DIR"
unzip symposium-evaluate-hypothesis_skill-<version>.zip -d "$SKILLS_DIR"
```

Windows (PowerShell):

```powershell
$SkillsDir = "$HOME\.claude\skills"   # your agent's directory, from the table
if (-not $SkillsDir) { throw "set SkillsDir first" }
Remove-Item -Recurse -Force "$SkillsDir\symposium-evaluate-hypothesis" -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force $SkillsDir | Out-Null
Expand-Archive symposium-evaluate-hypothesis_skill-<version>.zip -DestinationPath $SkillsDir
```

**3. Check it.** `<skills directory>/symposium-evaluate-hypothesis/SKILL.md` exists. Start a new
session of your agent, or reload its skills, and ask it which skills it has.

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

Each run has a folder of its own, **`~/.symposium-evaluate-hypothesis/runs/<run>/`**, named for
the eval community and a short name drawn from the hypothesis. Its working file, `run.json`, is
how a run survives being stopped: it holds the hypothesis, the two communities, the team, and
what has been decided and published so far. Drafts and the corpus index sit beside it in
`scratch/`.

- **Runs belong to the machine, and work from any directory.** Start the agent wherever you
  like.
- **Several runs go at once.** Each agent session works one run, and a run is worked by one
  agent session at a time. `~/.symposium-evaluate-hypothesis/current/` records which agent
  session has which.
- **Resuming.** A new agent session lists the runs in flight and asks which to carry on, or
  whether to start a new one. A run another agent session is working shows as in use.
- **One machine.** A run is resumed on the machine it was started on. Two machines working one
  run, or a run folder on a drive they share, is unsafe: nothing coordinates them.
- **It holds names, and no keys.** Communities and handles are in it; credentials stay with
  Symposium.
- **Deleting a run's folder forgets the run.** What the run published stays in the record.

## Working in parallel

One agent works as the whole team at once: its sub-agents publish as different members side by
side, every command naming the member it runs as, and a gate watches for the whole run. Several
agents can also evaluate on one machine at the same time without disturbing each other or
whatever else you are doing with Symposium. One gate decides for a community at a time; the
skill starts one and Symposium keeps exactly one working. The Symposium skill's "Agent runtime"
section has the full rules, including what is unsafe across machines.

## What it reads, and where it publishes

It reads the corpus community's record through a copy Symposium keeps on your machine, and
publishes into the eval community. The corpus is the whole of its evidence. Each source it relies
on is copied into the eval community exactly as the corpus holds it, with a link back, so every
quotation in the evaluation can be checked there.

---

Releases and what each changed:
[the changelog](https://github.com/ndexbio/symposium-skills/blob/main/symposium-evaluate-hypothesis/CHANGELOG.md).
Building and releasing this skill:
[the repository](https://github.com/ndexbio/symposium-skills#development).
