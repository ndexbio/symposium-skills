# Rehearsal — symposium-curate-data

What a correct run looks like, end to end.

This is the baseline a change to this skill's prose is read against. The repository's
[README](../README.md) says how to run one and how to read the result; the short version is:
build, install into a directory of its own, open a **fresh** session there, paste **only** the
prompt below, and compare what happens against the expectations here.

> Keep this document to yourself. It says what is supposed to happen, so an agent that reads it
> performs these expectations instead of showing whether the skill produces them unaided.

Nothing below restates what Symposium documents. Standing up a data server, founding a community,
joining it and running the gate are all Symposium's, and whether an agent gets there from
Symposium's own documentation is part of what this rehearsal tests.

## 1. What you need in place

| | How to check |
|---|---|
| A container runtime | `docker info` or `podman info` answers |
| The Symposium skill installed | `ls ~/.claude/skills/symposium/SKILL.md` |
| This skill installed in the QA directory | `ls ~/dev/qa-curate/.claude/skills/symposium-curate-data/SKILL.md` |
| Network access | the indexes are public, and the run queries several |

Set aside an evening. The search is minutes; the publishing is not.

## 2. The prompt

Paste this, and nothing else:

```
I want to build a literature corpus for this hypothesis and publish it into Symposium:

If chronic exposure to a high-fat diet alters the gut microbiome's bile acid
metabolism, then colonic epithelial cells show increased proliferation markers,
because secondary bile acids act as FXR antagonists in the colonic epithelium.
```

That hypothesis is chosen for the rehearsal rather than for science: its literature is large,
heavily open-access, and well deposited, so a run finishes and exercises every status in the
table. Any hypothesis with those properties will do.

## 3. What to expect, and what to answer

**Which of these hold still.** The *shape* of a run is the baseline — what the skill asks, in what
order, and what it produces. Which papers come back, how many are open, and which fail to retrieve
differ on every run as the literature and the indexes move, and differ without meaning anything.
Judge the shape.

**The skill is reached at all.** The prompt names no skill. It should be routed here on the
strength of its description. An agent that starts searching the web by hand is the first finding,
and it is a `description` problem.

**Symposium comes first.** Before searching, it should establish a community and the user context
it publishes as through the Symposium skill, and with neither in place it should take you through
Symposium's own path to standing up a local data server and founding one. Expect to be asked for a
handle and a community name. The community is a throwaway; part 5 removes it.

**The facets, before anything is searched.** You should see the hypothesis decomposed — entities
like bile acids, FXR, colonic epithelium; a population; an outcome; a method — and be able to
correct them. Facets that are just the hypothesis's words copied across are a finding.

**The scale question, with both numbers explained.** Max Origins and Max Sources, with what each
costs. Answer small so the table fits a screen:

```
4 origins, 12 sources
```

**The table.** One row per source, numbered, failed rows at the top, then abstract, then
retrieved. Columns for what it bears on, its stance, its type, its status and a note. Under it, a
coverage synopsis: counts per clause, counts per stance, independence groups, access tally, and
a content line saying how many sources will enter the record with content, in all and by clause.

A healthy run on this hypothesis gives you a row of each status — something retrieved as
structured full text from a PMC mirror, something retrieved as a flat PDF, something abstract-only
behind a publisher, and something failed. If everything retrieved cleanly, the access ladder was
not exercised; say so rather than counting it a pass.

**Work the table.** Taken in order, these exercise every choice once:

| Do this | And expect |
|---|---|
| reject a row | it leaves, the synopsis recounts |
| retry a failed row | the ladder runs again against the location it already holds |
| keep a closed row as citation only | its status becomes *citation only* |
| add a source by URL | identified from the URL, triaged, placed as a new row |
| add a source from a local PDF you have | identified from the document itself, and **if it is the paper that failed, it collapses into that row** rather than making a second |

Then approve.

**It goes and reads before it builds.** The hand-off is where this skill stops and the community's
own documents take over, and it routes by describing the work rather than by naming files. So
expect the agent, after you approve the table and before any artifact JSON exists, to say in its
own words what an Artifact and a Ground are, what the importer role may publish and what
`import_method` has to state, why extraction is two acts, what may be embedded from a source, and
what a rendering may change on the way in. Five topics, in its words.

An agent that starts writing artifact JSON without having gone for the importer role is the
finding — the routing failed, and everything downstream is improvised. An agent that recites the
topics as headings with nothing under them is the same finding wearing a hat.

**A gate watches throughout.** Before the first submission, expect one watching gate started in
the background under the community admin's user context, and left running. A run that stalls at
submission waiting for something to accept it is a finding to report, not something to rescue by
hand.

**Every command names its user context.** Expect `--user-context` on each Symposium command the
run issues, with a value it took from Symposium's listing, and no switching of the current
session during publishing. A command that goes out with no context named is a finding.

**Publishing is incremental, and wide.** Expect it to tell you at the approval stop that this is
the long part. Where the environment has sub-agents, expect several sources published side by
side, each in order within itself, and decisions read by artifact name.

**The working file is under your home directory**, at
`~/.symposium-curate-data/runs/<community>-<short name>/run.json`, with a pointer for the agent
session in `~/.symposium-curate-data/current/`. Nothing of the run's is written in the QA
directory.

**It resumes from anywhere.** Stop it halfway, start a new session in any directory, and say
*carry on with the curation*. Expect it to list the runs in flight and ask which. Start a second
session while the first is still running: the run should show as in use there.

## 4. What to read in the record afterward

Browse the record and check:

- **one `ScientificPublication` per source**, each with a `download` Content carrying its location
  and a hash
- **passages and tables** where the source allowed them, and none where it did not. A source
  that was free to read as publisher HTML or a flat PDF has passages; one left as a citation with
  a readable copy named in its own `import_method` is a finding
- **a source's passages cover its results, not one of them**: open a paper with several
  experimental arms bearing on the hypothesis and check each is there, with what was compared and
  the readout, including an arm that came out against. Arms left behind are named in
  `import_method`
- **every derived artifact cites its publication by address** — `@name` — rather than repeating
  the URL. A URL repeated across three artifacts is the defect this skill is built to avoid
- **citation-only sources are present and ground nothing**: a publication, no passages, no
  Argument
- **Arguments read as someone's reasoning**, not as a template. Open three from different sources.
  If their Assertions have the same shape with the nouns swapped, the hand-off degraded, and that
  is the most important finding this rehearsal can produce
- **`import_method` on the source you supplied** says the bytes came from a file you provided,
  while the `download` Content still points at the canonical location
- **the preserved passages**, against the originals. They should be verbatim, with hedges intact,
  and a figure caption should not be fused onto the end of the paragraph before it
- **the findings validation printed before each submission**, including any independence
  review, and whether it was answered or waved past

## 5. Teardown

Stop the data server container and remove its state directory. Remove the throwaway community's
session under `~/.symposium/`, and the skill's folder under your home directory,
`~/.symposium-curate-data/`.
