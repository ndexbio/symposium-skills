---
name: symposium-evaluate-hypothesis
description: Evaluate a scientific hypothesis against a curated corpus held in a Symposium community, and publish the evaluation into a second Symposium community record. Takes one hypothesis stated "If [Cause], then [Effect], because [Rationale]", a corpus community to read, and a community to evaluate in. A team of members decomposes the hypothesis into testable claims, names rival explanations, fixes the judging criteria, collects and appraises evidence from the corpus, judges each claim, challenges the judgments, integrates a verdict, proposes what would settle the open points, and writes a fixed-format assessment report. Use for: evaluate a hypothesis, test a hypothesis against the literature, assess the evidence for a hypothesis, hypothesis verdict, does the corpus support this hypothesis, hypothesis evaluation report, evaluate a hypothesis in Symposium.
license: MIT
metadata:
  version: "0.0.0-dev"
---

# Evaluating a hypothesis

One hypothesis and a corpus in. An evaluation in a Symposium community record out: the claims the
hypothesis stands on, an Argument judging each against the corpus, the challenges to those
judgments, a verdict, and a report.

The science is this skill's work, and
**[reference/HYP-EVAL.md](reference/HYP-EVAL.md)** is where it is set out. This document gathers
what that process needs before it can start — three inputs, a team, and a record to publish to —
and says how the work reaches Symposium.

## Terms

Three documents share this vocabulary. It is fixed here.

| Term | Means |
|---|---|
| **hypothesis** | one statement of the form `If [Cause], then [Effect], because [Rationale]` |
| **clause** | one of its three parts: cause, effect, rationale |
| **corpus community** | the Symposium community holding the sources gathered for this hypothesis; this run reads it |
| **eval community** | the Symposium community this run publishes the evaluation into |
| **agent session** | one agent process and everything it starts, sub-agents included, as Symposium defines and reports it |
| **user context** | one user's session on this machine, named as Symposium's listing prints it; every command the run issues names one |
| **corpus reader** | the user context this run reads the corpus community as |
| **the corpus copy** | the corpus reader's own copy of that community's record, on this machine |
| **claim** | one testable statement the hypothesis stands on, with what would count against it |
| **rival** | another explanation of the same observations |
| **criteria** | the verdict scale, the certainty scale and the integration rule, fixed before evidence is read |
| **item** | one place where one corpus source bears on one claim |
| **pointer** | an artifact in the eval community that reproduces what the corpus holds of one source and links back to it, so a Ground can cite it |
| **role** | one of the team's six scientific jobs: Lead, Methodologist, Librarian, Analyst, Skeptic, Adjudicator |
| **publishing role** | the Symposium role a member publishes under |
| **roster** | which member holds which role |
| **review display** | a table, a line of synopsis and the choices, drawn at each stop |
| **address** | a Symposium artifact reference, written `@name` |

## The working file

A run spans many submissions and more than one sitting. So a run keeps one folder of its own, and
one file in it:

- **`<user home>/.symposium-evaluate-hypothesis/runs/<run>/run.json`** — under a directory of
  this skill's own in the user's home directory, written the way the host platform spells that
  path. `<run>` is the eval community and the run's **short name**, joined by a hyphen. The
  short name is a few of the hypothesis's key words, lowercase, joined by underscores; it also
  goes in the topic part of every artifact name the run publishes.
- **The scratch folder** is `scratch/` in that same folder: the corpus index, the drafts, and
  what each sub-agent returns.
- **JSON**, updated a field at a time. One object holding the hypothesis; the short name; **the
  user context of every part in the run** — the corpus reader, the six team members, the gate —
  each as Symposium printed it; the phase reached; and the address of everything the gate has
  accepted.

Write each decision and each accepted artifact to it as it happens. A run that stops for any
reason resumes by reading it, then syncing and taking what has been accepted from the record
itself.

**You are the one writer of that file.** A sub-agent returns what it did as a file of its own in
the scratch folder, named for the artifact, and you record it.

### Which run this agent session is working

Runs belong to the machine, and an agent session works one of them. An **agent session** is what
Symposium defines it to be, and Symposium reports the two values that identify it: `pid` and
`started`. Ask Symposium for them; work nothing out yourself.

The choice is kept in **`<user home>/.symposium-evaluate-hypothesis/current/<pid>.json`**,
holding the run's name and `started`. At the start of every sitting:

1. Ask Symposium for this agent session.
2. Read your own pointer. Where it names a run and carries this agent session's `started`, that
   is your run: carry on with it.
3. Otherwise read the run folders and the other pointers. A pointer holds its run **in use**
   while Symposium reports the agent session it names as running, with the same `started`.
   Remove a pointer whose agent session has ended.
4. Put the choice to the user as a list: each run that is free, named by its hypothesis, its
   eval community and the phase it reached, to resume; and a new run. Show a run in use with
   the agent session that holds it; it is another agent's to work.
5. Write your pointer.

Where Symposium reports no agent session, keep no pointer and put the list to the user at each
start.

**A run belongs to the machine it was started on.** Its folder is there and it is resumed there.
Two machines working one run, or a run folder on a drive they share, is unsafe: nothing
coordinates them.

## Before you start: establish that a record is reachable

This run reads one **Symposium community record** and publishes into another — both append-only,
both reached through a session, the second decided by a gate.

**Where nothing in this environment can act on a Symposium community record** — no session, no
community, no way to reach a data server — the **Symposium skill** is missing, and it is required.
Say so, and point the user at **https://github.com/ndexbio/symposium/releases** to install it
alongside this one.

Asking Symposium which user contexts this machine holds is the whole of the check, and it is the
first thing the inputs below need.

**The Symposium in place has to let a command name its user context**, with `--user-context`, and
has to report the agent session. Its own help says whether it does. Where it does not, tell the
user to update it from the same releases page before going on.

### Who a command runs as

A run works as eight user contexts: the corpus reader, six team members, and the one its gate
runs as. **Every Symposium command this run issues names the user context it runs as**, with
`--user-context`. That is the one way a run chooses who acts, so the run works whatever the agent
session's current context is, and sub-agents work as different members side by side.

- **A value comes from Symposium's listing of the user contexts this machine holds**, where each
  entry prints it as `user_context`. Record it in the working file against the part it plays,
  and pass it back as it was printed. A value from anywhere else is a guess, and Symposium
  refuses it.
- **Read `session` in each command's report** to confirm it ran as the context you named.
- **Where a command is refused for a context this machine does not hold**, the refusal carries
  the listing. Correct the working file from it and tell the user what changed.
- **Listing the contexts changes nothing.** Joining a member and founding a community are done as
  Symposium provides them, and each makes its session the agent session's current one; the run
  carries on unaffected, because each of its commands names its own.

## Input 1 — The hypothesis

A hypothesis states all three clauses: `If [Cause], then [Effect], because [Rationale]`.

Where one is missing, say which, and work with the user to state it. The rationale is the one
people leave out, and it is the clause the mechanism claims are drawn from: an evaluation of a
hypothesis with no rationale can say whether the effect follows the cause and nothing about why.

## Input 2 — The corpus community

The community a curation run published the sources into, and a handle that can read it.

Have Symposium refresh what access each user context on this machine holds, then list them and
let the user choose one in the corpus community. Any access that reads the record will do. Record
its `user_context` as the **corpus reader**.

**This run reads that community.** Sync once as the corpus reader and work from the corpus copy.
Evidence is what that record embeds — passages, tables, extracted Arguments.

## Input 3 — The eval community

Where the evaluation is carried out and published. Offer two ways in.

**An existing community.** List the user contexts on this machine that hold the
**community-admin** access role, each by its `user_context`, and let the user choose one. Admin
access is what the run needs to invite the team, and it holds the `gate` grant the run's gate
needs.

**Where the chosen community already holds an evaluation of this hypothesis**, sync it, show the
user what is there — the artifacts, who published them, the short name they carry — and offer the
choices as a list:

- **Adopt** — carry that evaluation on, under its short name. What the gate has accepted is done,
  and the run takes up at the first phase with nothing accepted.
- **Start separately** — a new short name. The earlier artifacts stay as they are and this run
  cites none of them.
- **Cancel**.

Record the choice in the working file. An evaluation taken up without asking merges two runs the
short name exists to keep apart.

**A new community.** Ask three things:

1. **Where** — a data server on this machine, or one elsewhere. For one elsewhere, the user gives
   its URL and the handle of a **server-level** user whose invite this machine has already
   accepted; founding a community is a server-level act, and that acceptance is what makes it
   possible from here. For one on this machine, a running local data server and its server-level
   user are needed; where there is none yet, standing one up is a path Symposium documents, and
   you take the user through it.
2. **Its name** — offer a default drawn from the hypothesis: a few of its key words, lowercase,
   joined by underscores, within the length and characters Symposium allows a community name.
3. **Its admin's handle.**

Then found the community with that admin and with the team's members named for invitation, and
join the admin and each member on this machine. Take each one's `user_context` from Symposium's
listing afterward. Keys and invites move as files; a key, a
passphrase or an invite belongs in a file, and the chat is somewhere it may not go.

Record all three inputs in the working file. The run now has what it needs.

## How this work reaches Symposium

The eval community defines how reasoning becomes artifacts — completely, in its own documents.
Naming its concepts here makes this skill legible; it stands in for none of that reading.

**1. Say what you are doing, and let the community's documents answer.** You are acting as each of
several **Members of the eval community**, **publishing artifacts into its record**,
each under one **publishing role**: `principal` to set the goal, `hypothesize` to state claims and
propose tests, `importer` to bring corpus sources within reach, `researcher` to argue from
evidence and to give the verdict, `critic` to contest, `scout` to write the report.

**2. Read, before building anything:** the **operating instructions for a Member**; the
**charter of each of those six publishing roles**; the **standing policies** on what may be
embedded from a source, on what a rendering may change, and on how Members contest one another;
and the community's account of **the canonical form of an artifact**. Follow every onward
reference they make.

**3. Check you arrived.** Before you build, say in your own words:

| What you must be able to say | Which means you reached |
|---|---|
| what an Artifact, an Assertion, a Ground and an Assumption are; what an Argument's verdict, rationale and scope hold; how one artifact addresses another | the specification |
| what a goal is, why nothing may ground on it, and why the account that sets it stays apart from the gate | the principal's charter |
| what a conjecture may be published as, and what it must state to be testable | the hypothesizer's charter |
| what `import_method` has to state, and how content held outside the record is described and cited | the importer's charter and the canonical form |
| what a researcher may and may not ground on | the researcher's charter |
| what contesting an Argument amounts to, and what it leaves standing | the critic's charter and the discourse policy |
| what a survey may say, and why it grounds nothing | the scout's charter |
| what may be embedded from a source, and what a rendering may change | the embedding and fidelity policies |

Where you cannot say one of them, you have read too little: go back and find what covers it. None
of it is restated here, and where this skill and the community's own documents disagree, **the
community's documents are right.**

**4. Sync and read the eval record first.** It is append-only. Where it already holds an
evaluation of another hypothesis, this run's artifacts carry their own short name and stay apart
from it. Where it holds one of this hypothesis, the user has already chosen, at the third input,
whether this run adopts it.

## Who acts, and the gate

**Each command names its member.** You and your sub-agents validate and publish, each as the
member whose role authors the artifact, by that member's user context. Nobody switches the agent
session's current context during a run.

**You decide the order.** An artifact cites only what the gate has accepted, so you release a
layer of work to sub-agents once what it cites is in the record.

**A gate watches for the whole run.** You start it once, in the background, under the user
context the working file records for the gate, and Symposium keeps exactly one deciding for the
community on this machine.

[reference/HYP-EVAL.md](reference/HYP-EVAL.md) sets out who does what in parallel, what goes in a
sub-agent's brief, and how a decision is read.

## Carry out the evaluation

→ **[reference/HYP-EVAL.md](reference/HYP-EVAL.md)**

Settle the roster and stand up the team. Read the corpus once and index it. Then eleven phases:
frame, decompose, claims and criteria, coverage, collect, appraise, judge, challenge, integrate,
what would settle it, report. Each ends in something published, in layers, each layer released
once the gate has accepted what it cites.

### When it is done: the evaluation report

→ **[reference/EVAL-REPORT.md](reference/EVAL-REPORT.md)**

One report, a header and eight sections, the same shape for every hypothesis. Fill the skeleton it
carries rather than composing one. Publish it and show it to the user.

### If the gate refuses

Report what the gate said, and stop there. What to change is the user's decision.

## Where this stops and asks

After the three inputs, three places, each drawn as a review display:

1. **The roster**, before any member is invited — approve, change, or cancel.
2. **The claim set and criteria**, before they are published and before evidence is read —
   approve, revise, regenerate, or cancel.
3. **Corpus coverage**, only where no source in the corpus runs the test that a claim the
   hypothesis stands on needs — continue, revise the claims, or cancel.

Everything else runs through.

## On scripts

This skill is prose. Code written in the moment — indexing the corpus copy, tallying items by
claim, copying a source's content into its pointer and comparing the two, testing that every
quotation appears in the pointer it cites — is ordinary work; write it, use it, discard it.

A script that *decides* something is a different matter. Where you find yourself writing one that
rates an item, rules on a claim or picks a verdict, stop: that judgment is a member's, made in
words a reader can contest, and compiling it into code leaves the record holding a number where
the reasoning should be.
