---
name: symposium-curate-data
description: Build a grounded literature corpus for a scientific hypothesis and publish it into a Symposium community record. Takes one hypothesis stated "If [Cause], then [Effect], because [Rationale]", searches the literature and data repositories for the sources that bear on it, expands one citation hop, resolves access, puts the corpus to the user for review, then hands it to Symposium to publish as ScientificPublication, Data and Argument artifacts. Use for: curate sources for a hypothesis, build a literature corpus, find papers supporting or contradicting a hypothesis, import scientific publications into a community record, gather evidence for a Symposium record.
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
So a run keeps one file:

- **`<user home>/.symposium-curate-data/run.json`** — a directory of this skill's own, in the
  user's home directory, written the way the host platform spells that path.
- **JSON**, because it is updated a field at a time across a long run. One object holding the
  hypothesis, the facets, the scale, **the community and the handle this run publishes as**,
  every source with everything known about it, and the decisions and publications recorded
  against each.

Render the table from that file rather than from memory. Write each action to it before redrawing.
A run that stops for any reason — the review loop, the hand-off, a lost session — resumes by
reading it.

**Record the community and the handle the moment they are settled, and re-establish that session
on every resume.** A chosen session belongs to the agent session that chose it and does not
outlive it, so a run picked up in a new sitting starts with none — by design, so that two agents
on one machine never change each other's. What the run must carry across the gap is *which
community it is publishing to*, because a resumed run that inherits whatever session happens to
be current, or that asks the user to name the community again, can publish into the wrong record.
That record is append-only, and the artifacts cannot be withdrawn. So: read the community and
handle out of the working file, select that session, confirm it is the one selected, and only
then continue. Where the run is resumed and the recorded community cannot be selected, stop and
say so rather than publishing anywhere else.

One run at a time. Where a run is already in flight, ask the user before starting over it.

## Before you start: establish where you are publishing

Everything this run produces goes into a **Symposium community record** — append-only, reached
through a session, and decided by a gate. So settle two things before searching anything:

1. **The session you are working in.**
2. **The community you are a member of and will publish to.**

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

**5. Build, for each source:** the `ScientificPublication`, the passages each Ground needs, the
tables an Argument turns on, and the Argument extracted from it. Every derived artifact cites the
publication **by its address** rather than repeating its location. All of it under
`--role importer`.

What may be taken from the source on the way in is
**[reference/TAKING.md](reference/TAKING.md)**: measurements are observations of the world and are
rendered as recorded; sentences are authored expression and are taken as bounded, attributed
quotations; everything derived is written in your own words.

**6. Publish into the record**, which owns submission, ordering and the gate.

**Confirm the session before every submission.** Not once at the start, and not only on resume:
before each one. A session is chosen per agent process and anything running in that process can
change it — running the gate between submissions is the ordinary way it happens, and the publish
that follows goes out as whoever the gate ran as. Nothing downstream catches it. The gate is
checking that the artifact conforms, and an artifact published under the wrong handle conforms
perfectly; what it carries is a false statement about who brought the material in, in a record
that cannot withdraw it.

So read the session back, check it against the community and handle in the working file, and
reselect it where it has moved. It is a cheap check against a permanent error, and the cost of
skipping it is only ever paid after the fact.

### Publishing is the long part

Each source becomes several artifacts, and a derived artifact cannot be submitted until the
publication it cites has been accepted — so submissions are serial, with the gate between
dependent ones. Forty sources is a few hundred submissions and a great deal of judgment: passage
selection, an Argument, two method properties, each written fresh.

The risk is not failure but decay. An agent forty sources deep settles into a template, and a
templated Argument is the defect this skill exists to avoid, arrived at by exhaustion.

**So publish incrementally.** Go source by source. Record each published source in the working
file. A run that stops resumes from there. Tell the user at the approval stop that this is the
long part and can be taken in sittings — quality per source is the point; finishing the list in
one sitting is not.

### Superseding is a decision the user makes

Where an artifact this run already published turns out to be wrong, the correction goes to the user
before it goes to the record. Say which artifact, what it states, what the source actually supports,
and what the correction would claim about the earlier one. They decide.

The case that warrants it is a defect anyone can settle by looking: a count that the file does not
bear out, a quotation that is not in the source, an address that points at the wrong publication.
The case that does not is improvement — a better rationale, a cleaner Assertion, an early source
brought into line with the shape the later ones took. That second case is the one that will tempt
you, and it arrives late: thirty sources in, the first five read as apprentice work. They are the
record of what this run published at the time, and leaving them is what makes the later ones mean
something.

**So where it is improvement, the artifact stands as published and the run goes on to the next
source.** There is no second rendering of a source this run has already published — one source is
one publication, and a better version of an Argument alongside the first reads as two. Where what
changed is how you are working rather than how well, the later sources carry it and the closing
report says so under *Corrections and departures*.

**Where the later work reveals that the earlier artifacts are actually wrong** — a rendering rule
you were applying incorrectly for the first five sources, rather than a style you have outgrown —
that is the first case, and it reaches the user, however many artifacts it touches.

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
