---
name: symposium-curate-data
description: Build a grounded literature corpus for a scientific hypothesis and publish it into a Symposium community record. Takes one hypothesis stated "If [Cause], then [Effect], because [Rationale]", searches the literature and data repositories for the sources that bear on it, expands one citation hop, resolves access, puts the corpus to the user for review, then hands it to Symposium to publish as ScientificPublication, Data and Argument artifacts. Use for: curate sources for a hypothesis, build a literature corpus, find papers supporting or contradicting a hypothesis, import scientific publications into a community record, gather evidence for a Symposium record.
version: 0.1.0
---

# Curating data for a hypothesis

One hypothesis in. A grounded corpus in a Symposium community record out: one
`ScientificPublication` per source, the passages and tables that ground on it, and an Argument
extracted from each.

Finding those sources is this skill's work, and it is most of this document. Turning them into
artifacts is Symposium's work, and step 7 hands it over.

## Terms

Five documents share this vocabulary. It is fixed here.

| Term | Means |
|---|---|
| **hypothesis** | one statement of the form `If [Cause], then [Effect], because [Rationale]` |
| **clause** | one of its three parts: cause, effect, rationale |
| **facet** | a concept drawn out of a clause — an entity, method, population or outcome — and the vocabulary a run searches with |
| **index** | a service queried for works: OpenAlex, Europe PMC, Crossref, PubMed, bioRxiv, Semantic Scholar |
| **repository** | a service holding deposited data: MassIVE, GNPS, MetaboLights, Metabolomics Workbench, PRIDE |
| **hit** | one result an index returned, before identity is resolved |
| **work** | what identity resolves a set of hits to — a preprint and its published version are one work |
| **origin** | a work the search kept as a direct answer to the hypothesis, and a starting point for traversal |
| **source** | a work that is in the corpus |
| **corpus** | the sources this run will publish |
| **row** | a source as the review table shows it |
| **location** | a URL, DOI or accession where a document lives |
| **address** | a Symposium artifact reference, written `@name` |
| **the record** | the Symposium community record being published to |

## The working file

A run holds more than fits in a conversation, and the review table is redrawn after every action.
So a run keeps one folder of its own, and one file in it:

- **`<user home>/.symposium-curate-data/runs/<run>/run.json`** — under a directory of this
  skill's own in the user's home directory, written the way the host platform spells that path.
  `<run>` is the community the run publishes to and the run's **short name**, joined by a
  hyphen. The short name is a few of the hypothesis's key words, lowercase, joined by
  underscores; it also goes in the topic part of every artifact name the run publishes, so two
  runs in one community stay apart. Anything else the run keeps — fetched copies, drafts, what a
  sub-agent returns — goes in that folder beside the file.
- **JSON**, because it is updated a field at a time across a long run. One object holding the
  hypothesis, the short name, the facets, the scale, **the user context this run publishes as
  and the one its gate runs as**, every source with everything known about it, and the decisions
  and publications recorded against each.

Render the table from that file rather than from memory. Write each action to it before redrawing.
A run that stops for any reason — the review loop, the hand-off, a lost session — resumes by
reading it.

**You are the one writer of that file.** A sub-agent returns what it did as a file of its own in
the run's folder, named for the artifact, and you record it.

### Which run this agent session is working

Runs belong to the machine, and an agent session works one of them. An **agent session** is what
Symposium defines it to be, and Symposium reports the two values that identify it: `pid` and
`started`. Ask Symposium for them; work nothing out yourself.

The choice is kept in **`<user home>/.symposium-curate-data/current/<pid>.json`**, holding the
run's name and `started`. At the start of every sitting:

1. Ask Symposium for this agent session.
2. Read your own pointer. Where it names a run and carries this agent session's `started`, that
   is your run: carry on with it.
3. Otherwise read the run folders and the other pointers. A pointer holds its run **in use**
   while Symposium reports the agent session it names as running, with the same `started`.
   Remove a pointer whose agent session has ended.
4. Put the choice to the user as a list: each run that is free, named by its hypothesis, its
   community and the stage it reached, to resume; and a new run. Show a run in use with the
   agent session that holds it; it is another agent's to work.
5. Write your pointer.

Where Symposium reports no agent session, keep no pointer and put the list to the user at each
start.

**A run belongs to the machine it was started on.** Its folder is there and it is resumed there.
Two machines working one run, or a run folder on a drive they share, is unsafe: nothing
coordinates them.

## Before you start: establish where you are publishing

Everything this run produces goes into a **Symposium community record** — append-only, reached
through a session, and decided by a gate. So settle two things before searching anything:

1. **The community you are a member of and will publish to.**
2. **The user context you publish as**: a session this machine holds in that community, taken
   from Symposium's listing of them and recorded in the working file exactly as it is printed
   there.

Where there is no community yet, there is a path through it: standing up a data server, founding a
community with a `community.json`, and joining it with an invite file. Take the user through that
path rather than working around it. Keys and invites move as files; a key, a passphrase or an
invite belongs in a file, and the chat is somewhere it may not go.

**Where nothing in this environment can act on a Symposium community record** — no session, no
community, no way to reach a data server — the **Symposium skill** is missing, and it is required.
Say so, and point the user at **https://github.com/ndexbio/symposium/releases** to install it
alongside this one. Searching and curating still work if they want the corpus now and the record
later; step 7 waits until it is there.

That attempt is the whole of the check. Asking for a session and a community is work this run
needs regardless, and what comes back — or what fails to — says whether the record is reachable.

**The Symposium in place has to let a command name its user context**, with `--user-context`, and
has to report the agent session. Its own help says whether it does. Where it does not, tell the
user to update it from the same releases page before going on.

### Who a command runs as

**Every Symposium command this run issues names the user context it runs as**, with
`--user-context`. That is the one way a run chooses who acts, so the run works whatever the agent
session's current context is, and several runs and sub-agents work side by side.

- **A value comes from Symposium's listing of the user contexts this machine holds**, where each
  entry prints it as `user_context`. Record it in the working file and pass it back as it was
  printed. A value from anywhere else is a guess, and Symposium refuses it.
- **Read `session` in each command's report** to confirm it ran as the context you named.
- **Where a command is refused for a context this machine does not hold**, the refusal carries
  the listing. Correct the working file from it and tell the user what changed.
- **Listing the contexts changes nothing.** Joining a community and founding one are done as
  Symposium provides them, and each makes its session the agent session's current one; the run
  carries on unaffected, because each of its commands names its own.

## Step 1 — Read the hypothesis

A hypothesis states all three clauses: `If [Cause], then [Effect], because [Rationale]`.

Where one is missing, say which, and work with the user to state it. The rationale is the one
people leave out, and it is the clause that decides what a third of the search looks for.

Then decompose each clause into **facets** — entities, methods, populations, outcomes. These are
the run's vocabulary: every query is built from them, every source is scored against them, and the
threshold that bounds traversal is measured in them.

**Show the user the facets before searching anything.** A wrong facet is cheap to fix now and
expensive after forty sources have been gathered around it.

## Step 2 — Agree the scale

Two numbers, and they are the only knobs a user turns.

**Say what each number counts, in the user's words, before naming it.** *Origin* and *source* are
this document's vocabulary, and the scale question is where a user meets them for the first time.
A label on its own tells them what the number is called rather than what it does, and a figure
nobody understands is a figure nobody changes. So lead with the plain description and keep the
term as a parenthetical.

**Max Origins** — the works the search keeps as its best direct answers to the hypothesis, and the
starting points everything else grows out from. The search turns up hundreds of candidates; this
is how many of the strongest it holds on to. More of them reach into parts of the literature that
cite nobody in common; fewer give a tighter, deeper cluster around the strongest work. Default
**10**.

**Max Sources** — the size of the finished corpus: every work that reaches the review table and
the record. It is the origins plus everything one citation hop away that scored high enough to
keep, after duplicates collapse. It is the budget for everything downstream, since each source is
fetched, triaged, shown as a row, and published. Default **40**.

Put both with what they cost — roughly how long the run takes, and how many rows the user will
read. Something along these lines, adapted to the hypothesis in hand:

> Two numbers set how wide this runs.
>
> **Starting papers (Max Origins)** — the strongest direct answers to your hypothesis. I search
> outward from these. Default 10.
>
> **Total papers (Max Sources)** — how big the finished corpus gets: those starting papers plus
> the ones their citations lead to. Each becomes a row you review and a set of artifacts in the
> record. Default 40 — about 40 rows to read, and a few hundred submissions to publish.

Start searching once they answer, whether they took the defaults or named their own.

## Step 3 — Search

→ **[reference/SEARCHING.md](reference/SEARCHING.md)**

Four query families out of the three clauses, each calibrated before it is spent. The best hits
across all four become the origins.

## Step 4 — Expand one hop

→ **[reference/TRAVERSING.md](reference/TRAVERSING.md)**

Backward, forward and sideways from the origins, with the origin threshold as the hop's
definition.

## Step 5 — Settle access

→ **[reference/ACCESS.md](reference/ACCESS.md)**

Descend the ladder for each source, triage what comes back, and leave each one carrying a status
and a note.

## Step 6 — Curate, and review with the user

→ **[reference/CURATING.md](reference/CURATING.md)**

Identity, retraction status, independence and coverage. Then the review loop: a table of every
source with its status, which the user works over row by row until they approve it.

Nothing is published before they do.

## Step 7 — Hand the corpus to Symposium

The community defines how a source becomes artifacts — completely, in its own documents. Naming
its concepts here is what makes this step legible; it is not a substitute for going and reading
them. So:

**1. Say what you are doing, and let the community's documents answer.** You are acting as a
**Member of this community**, **publishing artifacts into its record**, in the **`importer`
publishing role**: importing outside material so the community can ground on it, and extracting
the arguments the sources make.

**2. Read, before building anything:** the **operating instructions for a Member**; the
**charter of the `importer` publishing role**; the **standing policies** on what may be embedded
from a source and on what a rendering may change on the way in; and the **procedure for
extracting a paper's argument**. Follow every onward reference they make. They route to each
other, and the one furthest down the chain carries the rules you are most likely to break.

**3. Check you arrived.** Progressive disclosure fails quietly: an agent reads the first document,
feels oriented, and starts building. So before you build, say in your own words:

| What you must be able to say | Which means you reached |
|---|---|
| what an Artifact, an Assertion, a Ground and an Assumption are, and how one artifact addresses another | the specification |
| what the importer may publish, what `import_method` has to state, and what the role does where a source resists preservation | the importer's charter |
| why extraction is two acts, which one comes first, and what happens between them | the extraction procedure |
| what may be embedded from a source, and what stays behind a `download` | the embedding policy |
| what a rendering may change on the way in | the fidelity policy |

Where you cannot say one of them, you have read too little: go back and find what covers that
topic. None of it is restated here, and where this skill and the community's own documents
disagree, **the community's documents are right.**

**4. Sync and read the record first.** It is append-only, so anything it already holds is cited by
address rather than published again.

**5. Build, for each source:** the `ScientificPublication`, the passages and tables that carry
every result bearing on the hypothesis, and the Argument extracted from it. Every derived artifact
cites the publication **by its address** rather than repeating its location. All of it under
`--role importer`.

What may be taken from the source on the way in is
**[reference/TAKING.md](reference/TAKING.md)**: measurements are observations of the world and are
rendered as recorded; sentences are authored expression and are taken as bounded, attributed
quotations; everything derived is written in your own words. It also says how much to take —
every result that bears on a clause, the contrary ones included, because whoever evaluates the
hypothesis against this record has only what was taken — and how to render a source that arrived
as plain HTML or a flat PDF.

**6. Publish into the record**, which owns submission, ordering and the gate.

**Name the publishing context on every command**, as [who a command runs as](#who-a-command-runs-as)
sets out, and read `session` in the report. An artifact published under the wrong handle conforms
perfectly; what it carries is a false statement about who brought the material in, in a record
that cannot withdraw it.

**A gate watches for the whole of publishing.** Before the first submission, start Symposium's
watching gate as a background command, under a user context that holds the `gate` grant, and
leave it running; Symposium's own instructions for commands that keep running say how to follow
it. Symposium keeps one gate deciding for a community on a machine: where another is already
watching, yours stands by and watches from the moment that one ends, so start yours without
looking for another.

- **Which context**: from Symposium's listing, the contexts in the publishing community whose
  roles are `community-admin` or `gate-keeper`. One: use it, and record it. Several: ask the
  user, as a pick list. None: the gate runs from another machine; say so, publish, and wait for
  its decisions.
- **A community's gate runs from one machine.** Where the user says it already runs elsewhere,
  start none here.

**Read each decision by the artifact's name.** Accepted, the artifact is in the publishing
context's copy of the record after a sync. Rejected, it is among the gate's replies to that
context, which Symposium lists in full on request, each with the artifact it is about. What the
gate will find, the publishing check finds first: validate before submitting and read its
findings there.

### Publishing is the long part

Each source becomes several artifacts, and a derived artifact cannot be submitted until the
publication it cites has been accepted. So **within a source the order is fixed**: the
publication, then its passages and tables, then its Argument, each after the gate has accepted
what it cites. **Across sources nothing waits**: forty sources is a few hundred submissions and a
great deal of judgment — passage selection, an Argument, two method properties, each written
fresh.

**Where the environment has sub-agents, publish sources side by side.** Give each sub-agent a
few sources, the publishing user context exactly as recorded, the `importer` publishing role, and
the artifact names it owns. It builds, validates and publishes its sources in order, and returns
a file per source saying what was accepted. You record those in the working file. One sub-agent
to a source: two working one source publish the same name twice, and the second is refused.

The risk is not failure but decay. An agent forty sources deep settles into a template, and a
templated Argument is the defect this skill exists to avoid, arrived at by exhaustion. A fresh
sub-agent per handful of sources is also the remedy for that.

**So publish incrementally.** Record each published source in the working file as it lands. A run
that stops resumes from there. Tell the user at the approval stop that this is the long part and
can be taken in sittings — quality per source is the point; finishing the list in one sitting is
not.

### Correcting something already published

Where an artifact this run already published turns out to be wrong, the correction is yours to
make, under the test below. The record expects a Member to correct a defect in their own work, and
a run of forty sources that stopped to ask about each one would spend the user's attention on the
part of the decision that needs none.

The case that warrants it is a defect anyone can settle by looking: a count that the file does not
bear out, a quotation that is not in the source, an address that points at the wrong publication.
The case that does not is improvement — a better rationale, a cleaner Assertion, an early source
brought into line with the shape the later ones took. That second case is the one that will tempt
you, and it arrives late: thirty sources in, the first five read as apprentice work. They are the
record of what this run published at the time, and leaving them is what makes the later ones mean
something.

**The test is whether two quotes settle it.** Put what the artifact states beside what the source
says. Where the mismatch is visible in the pair, it is a defect: supersede it, write the rationale
for the record's readers rather than for the run — what the earlier artifact got wrong and what
this one does about it — and go on. Where settling it would take a judgment instead, whether a
passage really carries the Assertion, whether the scope is drawn wider than the evidence, it is not
a defect and superseding is the wrong instrument. That is a disagreement the record settles with an
Argument, made by someone who means to make it. Leave the artifact as published and record it under
*Loose ends*.

**So where it is improvement, the artifact stands as published and the run goes on to the next
source.** There is no second rendering of a source this run has already published — one source is
one publication, and a better version of an Argument alongside the first reads as two. Where what
changed is how you are working rather than how well, the later sources carry it and the closing
report says so under *Corrections and departures*.

**The second time the same defect appears, stop and tell the user.** One is a slip. Two of a kind
is a method that is wrong, and then the artifacts that need attention include the ones you have not
rechecked and the ones you have not published yet. Correcting each in place as you meet it hides
the one thing the user needs to see. Say what the defect is, where it has turned up, and what it
implies for the rest of the run, and let them decide how far back it reaches.

Every supersession, with its reason, goes in **Corrections and departures** in the closing report.

### When it is done: the closing report

→ **[reference/CLOSING-REPORT.md](reference/CLOSING-REPORT.md)**

One report, six sections, the same shape every run. Fill the skeleton it carries rather than
composing one.

### If the gate refuses

Report what the gate said, and stop there. What to change is the user's decision: amending an
artifact to satisfy a finding, or resubmitting it, is a judgment about the record, and a record
cannot withdraw what it has accepted.

## Where this stops and asks

Two places:

1. **The scale**, in step 2, before anything is searched.
2. **The review table**, in step 6, before any of the corpus becomes artifacts.

## On scripts

This skill is prose. Code written in the moment — paginating an index, folding DOI case over a few
hundred rows, diffing two lists — is ordinary work; write it, use it, discard it.

A script that *decides* something is a different matter. Where you find yourself writing one that
selects passages, judges a source primary or secondary, or settles what an Argument claims, stop:
that judgment belongs to the community's own procedures and policies, read in step 7, and
compiling it into code replaces their reasoning with your guess at it.
