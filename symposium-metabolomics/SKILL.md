---
name: symposium-metabolomics
description: Analyze an untargeted LC-MS/MS metabolomics study from a GNPS2 Everything Bagel (feature-based molecular networking) task and publish the analysis into a Symposium library community, or interpret an analysis held in a library community biologically and publish the findings into a second Symposium community. Analyze fetches the task's feature table, spectra, annotations and molecular network, runs quality control, filtering, normalization, statistics, detection-rate and network analysis, and publishes inputs, analyses, result tables and a technical report. Interpret reads that analysis, evaluates every emerging pattern, forms and challenges biological hypotheses against the literature, and publishes findings as Arguments with a report. Use for: analyze a GNPS2 task, metabolomics preliminary analysis, feature table to statistics, FBMN analysis in Symposium, interpret a metabolomics analysis, biological interpretation of metabolomics results, metabolomics hypotheses, what does this metabolomics analysis mean.
license: MIT
metadata:
  version: "0.0.0-dev"
---

# Metabolomics in a Symposium community

Two pieces of work, each ending in a Symposium community record.

**Analyze** takes one GNPS2 Everything Bagel task and a question, and leaves in a **library
community** the task's inputs, every analysis run on them, the result tables and a technical
report. **Interpret** takes an analysis a library holds, and leaves in an **interpretation
community** the biological findings it supports, as Arguments, with a report.

The science is this skill's work, and four documents set it out. This document says which mode
a request starts, what each mode gathers before it begins, and how the work reaches Symposium.

## Terms

Five documents share this vocabulary. It is fixed here.

| Term | Means |
|---|---|
| **task** | one GNPS2 Everything Bagel job, named by its task ID and host |
| **feature** | one row of the task's quantification table: an m/z, a retention time and an area per sample |
| **question** | what the user wants to know from the study, in their own words |
| **mode** | analyze or interpret |
| **run** | one mode's work on one question, from its inputs to its accepted report |
| **library community** | the Symposium community that holds inputs, analyses and literature sources; analyze publishes into it and interpret reads it |
| **interpretation community** | the Symposium community interpret publishes its findings into |
| **stage** | one step of the analysis that ends in something published: quality control, filtering, normalization, statistics and so on |
| **pattern** | a set of features that move together with the comparison, evaluated as one thing |
| **finding** | a pattern or hypothesis the user chose to pursue, published as an Argument or a conjecture |
| **pointer** | an artifact in the interpretation community that reproduces what the library holds of one table or source and links back to it, so a Ground can cite it |
| **draft** | a mode's results and report as they stand in the run's folder, before the user approves them |
| **reuse table** | at analyze's intake: each stage, what the library already holds for it, and whether this run reuses or redoes it |
| **overlap table** | at interpret's pattern checkpoint: each pattern and hypothesis of this run beside the finding already in the interpretation community that it matches |
| **address** | a Symposium artifact reference, written `@name` |

## Which mode a request starts

Choose the mode from what the user asked for and supplied. Say which mode is starting, in one
line, before doing anything else. Start nothing silently.

| The user | Mode |
|---|---|
| gives a GNPS2 task and asks for it to be processed, analysed or checked | analyze |
| asks what an analysis means, for hypotheses, or for interpretation, naming or implying an analysis a library already holds | interpret |
| gives a task and asks a biological question in one request | analyze, and stop when it closes |
| says neither clearly | ask, with a list: each free run to resume, a new analysis, a new interpretation |

**Analyze never starts interpret.** Its closing message ends by saying interpretation is
available. Interpret starts when the user asks for it, in this session or a later one. Asked in
the session that ran the analysis, it begins a new run with the library already known.

**Interpret starts from an analysis the library's record holds.** Sync the library and look for
an accepted technical report. Where there is none, say so and offer to run analyze. Where there
are several, put them to the user as a list, each named by its task, its question and the date
it was accepted. An analysis still in draft is in no record, so there is nothing to start from
until its user has approved it.

**The question interpret works to** is what the user says when asking for interpretation. Where
that states no question, the analysis's question stands; confirm it with the user before
starting.

## The run, and its working file

A run is kept as Symposium sets out for a skill built on it: its folder, its working file, which
run this agent session is working, who each command runs as, and the gate. Read that before
anything else, and follow it as written. What is this skill's own:

- **The skill's directory** is `<user home>/.symposium-metabolomics/`.
- **A run is one mode.** An analyze run publishes to the library community; an interpret run to
  the interpretation community. Each is named for that community and its short name.
- **The short name** is a few key words of the study and the question, lowercase, joined by
  underscores.
- **The working file holds**, beyond what every run's does: the mode; the task ID and host; the
  question, verbatim; every intake answer and every decision the user made, each with what it
  decides; the stage reached; for analyze, the reuse table as approved; for interpret, the
  address of the technical report it started from, the patterns with their state, and the
  overlap table as approved; the time the user approved the draft, in UTC, as
  `draft_approved_at`; and, once it is built, the report file's full path as `report_pdf`.
- **The run's folder holds** fetched copies of the inputs, the tables, figures and code as they
  are worked, the draft report, and the report file.
- **The parts a run plays.** Analyze: the member who publishes to the library, and the context
  its gate runs as. Interpret: the member who reads the library; the member who publishes to
  the interpretation community; the context that community's gate runs as; and, where this
  machine holds one, the context the library's gate runs as.
- **A finished run** is one that holds its report file. Choosing it shows the report again.
- **On resuming an interpret run**, sync the library. Where the analysis it started from has
  been superseded, tell the user and ask whether to carry on from the one it started on or
  start again from the newer one.

Record each answer the user gives once, and reuse it. Ask nothing twice.

## Before you start

**Where nothing in this environment can act on a Symposium community record** — no session, no
community, no way to reach a data server — the **Symposium skill** is missing, and it is
required. Say so, and point the user at **https://github.com/ndexbio/symposium/releases** to
install it alongside this one.

**The Symposium in place has to say how a skill built on it keeps a run.** Its own routing of
what to read says whether it does. Where it does not, tell the user to update it from the same
releases page before going on.

**Python**, with numpy, pandas, scipy 1.10 or later, a plotting library and a library that
writes PDF. Check by importing them. Where one is missing, say which and how to install it, and
wait.

**Network access to gnps2.org**, for analyze.
[reference/GNPS2-FILES.md](reference/GNPS2-FILES.md) says how to test it and what to do where
it is refused.

## What analyze gathers

1. **The task** — its ID, and its host where the user gives one.
2. **The question.**
3. **The library community**, and a member of it this machine holds who can publish. Have
   Symposium list the user contexts on this machine and let the user choose. Where there is no
   community yet, standing up a data server, founding a community and joining it are paths
   Symposium documents; take the user through them.
4. **Files the task does not hold** — sample metadata, annotations the user prefers to the
   task's own, the injection order and batch of each run, the internal standards used. Ask for
   each once, where the analysis needs it and the task lacks it.

## What interpret gathers

1. **The library community**, and a user context that reads it. Any access that reads the
   record will do. Access that publishes there as well lets the run add the literature it
   finds; say which the chosen context has.
2. **The analysis** in it to interpret, chosen as above.
3. **The interpretation community**, and a member of it who can publish. Offer the communities
   this machine can publish to, and a new one. For a new one, founding it and joining it are
   paths Symposium documents.
4. **The question.**

Record them in the working file. The run now has what it needs.

## How this work reaches Symposium

A community defines how work becomes artifacts — completely, in its own documents. Naming its
concepts here makes this skill legible; it stands in for none of that reading.

**1. Say what you are doing, and let the community's documents answer.** You are acting as a
**Member of a community**, **publishing artifacts into its record**, each under one
**publishing role**:

| Publishing role | For |
|---|---|
| `principal` | the goal: the question the run serves, in the user's words |
| `importer` | each input brought in from GNPS2 or from the user; each literature source; each pointer |
| `analyst` | each stage of the analysis, and each table it produces |
| `researcher` | each finding argued from the tables, and the analyses a hypothesis calls for |
| `hypothesize` | a hypothesis offered before the evidence is in |
| `scout` | the hand-off note and the report |

**2. Read, before building anything:** the **operating instructions for a Member**; the
**charter of each publishing role** the mode uses; the **standing policies** on where a result
lives, on what is embedded and what is held as a file, on what a rendering may change on the
way in, and on how Members write for one another; and the community's account of **the
canonical form of an artifact**. Follow every onward reference they make.

**3. Check you arrived.** Before you build, say in your own words:

| What you must be able to say | Which means you reached |
|---|---|
| what an Artifact, an Assertion, a Ground and an Assumption are; how one artifact addresses another; why an artifact cites only what is already accepted | the specification |
| what `import_method` has to state; how content held outside the record is described and cited; what an inventory is and is not | the importer's charter and the canonical form |
| why an Analysis is published before its outputs; what `procedure` and `inputs` hold; why a number computed belongs in an artifact | the analyst's charter and the results policy |
| what is embedded, what is held as a file, at what size, and how a figure is held | the embedding policy |
| what a researcher may and may not ground on; what a verdict, a scope and a purpose hold | the researcher's charter |
| what a conjecture is published as, and what it must state | the hypothesizer's charter |
| what a survey may say, and why it grounds nothing | the scout's charter |
| what a goal is, and why nothing may ground on it | the principal's charter |

Where you cannot say one of them, you have read too little: go back and find what covers it.
None of it is restated here, and where this skill and the community's own documents disagree,
**the community's documents are right.**

**4. Sync and read the record first**, both communities for interpret. A record is append-only,
so what it already holds is cited by address and never published again.

## What is already there is reused

Read a community before writing to it. What follows says when two things are the same thing.

| Thing | The same when | Then |
|---|---|---|
| an input from GNPS2 | the same task and file, and the bytes fetched have the digest the import records | cite the import |
| an input from GNPS2 whose bytes have changed | the same task and file, another digest | a new import that names the earlier one |
| an input the user supplied | the same digest | cite the import; the file is stored once |
| a stage of the analysis | the same inputs by address, and its recorded procedure makes the decisions this run would make | cite its outputs as this run's inputs |
| a literature source | the same DOI; without one, the same PMID or location | point at it |
| a pointer | the interpretation community already points at that library artifact | cite it; where more of the source is needed, a pointer that supersedes it and carries the rest |
| an analysis a hypothesis called for | the same pointers as inputs and the same procedure | cite its outputs |

**The reuse table.** Where the library already holds work on this task, analyze shows at intake
each stage, the artifact already there, whether this run reuses it or redoes it, and why. The
stages that do not turn on the question — quality control, internal standards, feature merges,
batch correction, detection rate, the molecular network, compound classes — are reused where
their decisions still hold. The stages that do — group-aware filtering, the statistics for this
comparison, covariates, sensitivity — are run for this question, taking the reused outputs as
inputs. The user approves or changes the table before any work starts. Where it shows every
stage reused, show the existing technical report and publish nothing.

**The overlap table.** A finding is a judgment, with no identifier to match on, so a second
interpretation would say the first again in other words. Before interpret publishes anything,
at the pattern checkpoint, show each pattern and hypothesis of this run beside the finding
already in the interpretation community that it matches — the same features or families, the
same direction — marked one of:

| Mark | Means | This run publishes |
|---|---|---|
| already there, agrees | the same finding on the same evidence | nothing; its report links the earlier finding |
| already there, more to say | new evidence, another scope, or another judgment | one artifact that builds on, revises or contests the earlier finding, as the community's documents set out |
| new | no earlier finding covers it | the finding |

The user approves or changes the table. Only what it marks is published.

**What this cannot catch.** A paper with no identifier, a preprint and its published version, or
two members publishing at one moment can each leave two artifacts for one thing. Where you find
such a pair, cite the earlier, and name the pair in the report so a reader does not take one
source for two.

## Carry out the mode

**Analyze**

1. → **[reference/GNPS2-FILES.md](reference/GNPS2-FILES.md)** — find and fetch the task's
   files.
2. → **[reference/ANALYZE.md](reference/ANALYZE.md)** — the analysis, stage by stage, each
   decision put to the user with a recommendation.
3. → **[reference/REPORT.md](reference/REPORT.md)** — the technical report.

**Interpret**

1. → **[reference/INTERPRET.md](reference/INTERPRET.md)** — read the analysis, evaluate every
   emerging pattern, stop for the user to choose, then pursue, challenge and refine.
2. → **[reference/REPORT.md](reference/REPORT.md)** — the main and the full report.

Batch and drift correction is the one computation this skill ships as code:
[scripts/qcrsc.py](scripts/qcrsc.py). [reference/ANALYZE.md](reference/ANALYZE.md) says when it
runs.

## A mode works in its folder, and publishes on approval

A record keeps everything it accepts, and a user who sees a result usually wants it changed. So
a mode keeps its work out of the record until the user has approved it.

1. **Work in the run's folder.** Inputs fetched, tables, figures, code, the draft report.
   Record each decision in the working file as it is made.
2. **Show the draft report** in the conversation, as Markdown, and stop. The user revises as
   often as they like. Every revision is made in the run's folder and shown again.
3. **Confirm what leaves this machine**, before storing or publishing anything: the question as
   it will be published, word for word, since it may hold paths and names; and each file the
   user supplied that will be stored with the community, since it may describe study subjects.
   Where the question holds a credential, stop and ask.
4. **On approval, publish**, in the order the addresses require: the goal; the inputs; each
   Analysis, then its outputs; then what stands on them; the report last. Validate each before
   submitting it. Send the first of a kind alone, and release the rest of that kind once it is
   accepted.
5. **A change asked for after approval** is a new artifact that supersedes the one it corrects,
   with what changed and why, and the mode closes again.

**Where each thing is kept** follows from what Symposium's documents say of embedding and of
files. In this skill's terms:

- **An input held at gnps2.org is cited there.** Its import carries the location it was fetched
  from, and states the task, the file, the date, the size and the digest computed on fetch.
- **An input the user supplied, which has no location of its own, is stored with the
  community** and cited from its import.
- **An input fetched and not used is not imported.**
- **A stage's decisions are its Analysis's procedure**: the method, the parameters, the
  rationale, what went in and what came out, what was removed, what the user decided and what
  was recommended.
- **A table is a stage's output.** One a reader can read is embedded. A larger one is described
  and held as a file; analyze cannot know which of its rows a later finding will turn on, so it
  embeds none.
- **A figure** is held beside the table it plots, with a line saying how to read it that states
  no result.
- **Code that ran** is held as a file and cited from the Analysis whose procedure it carried
  out.
- **A file stored with a community carries the run's short name in its own name.**
- **A request to someone who is not at this terminal** — a file only they have, a source the
  library should hold, a correction to an analysis they published — is a Message to them.

## Interpret cites the library through pointers

A Ground cites an address in its own record, and the library is another record. For each
library table a finding or an analysis uses, and each literature source a finding cites,
publish a pointer in the interpretation community, as the same type the library gave it:

- **the content, reproduced exactly** — the rows or the text. Where the library embeds the
  content, reproduce what it embeds. Where the library holds a table as a file, fetch the file
  and carry the rows the finding turns on, each exactly as the file has it;
- a link back: the location at which the library community's data server serves that artifact,
  marked as one a Ground may not cite, with how a reader who has access to the library fetches
  it;
- for a literature source, its authors and its own identifier;
- an `import_method` saying the content is reproduced from an artifact in the library
  community, which one, which rows or passages, and that names written as literals belong to
  that community.

**Copy by script, and compare** the pointer's content with its source, byte for byte, before
submitting. Grounds cite the reproduced content, by the exact cells or the exact words.

## Literature goes through the library

Interpret searches the literature as [reference/INTERPRET.md](reference/INTERPRET.md) sets out,
in the course of the work. Every source it finds lives in the library, so the next
interpretation finds it there.

1. Sync the library, and list its sources by DOI.
2. **A source the library holds:** point at it. Where a finding needs more of it than the
   library holds, add to the library an artifact that carries the rest and cites the source.
3. **A source the library does not hold:** bring it into the library, wait for the library's
   gate to accept it, then point at it. Sync immediately before publishing it.
4. **The library's gate.** Where this machine holds a context that can run it, start it
   watching. Where it does not, say that the library's gate decides elsewhere, and wait for its
   decision.
5. **Where the member reading the library cannot publish there**, say that the source could not
   be added, send a Message to a member of the library who imports asking for it, and list it
   in the report.

How a source is brought in — what it becomes, what of it is embedded, what may be grounded on —
is the community's documents' to say, and they are read in
[How this work reaches Symposium](#how-this-work-reaches-symposium). This skill adds nothing to
them.

## When a mode is done

→ **[reference/REPORT.md](reference/REPORT.md)**

The report is published last, as an artifact. Once the gate has accepted it, build the report
file from the accepted artifact, as a PDF, in the run's folder. Close the mode by showing the
report in full in the conversation, with the report file's full path as the last line. The same
document fixes the report's skeleton, the file's name and the closing message.

Analyze's closing message says, before that last line, that interpretation is available.

### If the gate refuses

Report what the gate said, and stop there. What to change is the user's decision.

## Where this stops and asks

**Analyze**

1. **The reuse table**, where the library already holds work on this task.
2. **Each decision the analysis turns on**, gathered into as few stops as the analysis allows,
   each with a recommendation, the alternatives and what each would change.
3. **The draft technical report.**
4. **What leaves this machine**, before publishing.

**Interpret**

1. **Intake**: the defaults, accepted or changed.
2. **The pattern checkpoint**: every pattern evaluated, the overlap table, and the choice of
   what to pursue.
3. **Each group of further analyses**, before it runs.
4. **The draft reports.**
5. **What leaves this machine**, before publishing.

Every stop ends by saying what is needed from the user: the recommendations, and the questions.

## On scripts

The analysis is code written for the study in hand — loading the tables, filtering, fitting
models, drawing figures, building the report. Write it, keep it in the run's folder, and
publish what ran with the Analysis it carried out. [scripts/qcrsc.py](scripts/qcrsc.py) is the
one piece shipped, because a correction validated against a reference implementation should not
be rewritten each time.

A script computes; it does not decide. Where you find yourself writing one that chooses a
threshold nobody approved, rules a pattern real, or settles what a finding claims, stop: a
threshold is the user's, put to them with a recommendation, and a finding is a member's
judgment, made in words a reader can contest.
