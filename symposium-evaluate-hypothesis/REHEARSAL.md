# Rehearsal — symposium-evaluate-hypothesis

What a correct run looks like, end to end.

This is the baseline a change to this skill's prose is read against. The repository's
[README](../README.md) says how to run one and how to read the result; the short version is:
build, install into a directory of its own, open a **fresh** session there, paste **only** the
prompts below, one at a time, and compare what happens against the expectations here.

> Keep this document to yourself. It says what is supposed to happen, so an agent that reads it
> performs these expectations instead of showing whether the skill produces them unaided.

Nothing below restates what Symposium documents. Standing up a data server, founding a community,
joining it and running the gate are all Symposium's, and whether an agent gets there from
Symposium's own documentation is part of what this rehearsal tests.

A rehearsal here is two runs. An evaluation needs a corpus to read, so the first prompt has the
curation skill build one, and the second evaluates against it.

## 1. What you need in place

| | How to check |
|---|---|
| A container runtime | `docker info` or `podman info` answers |
| The Symposium skill installed | `ls ~/.claude/skills/symposium/SKILL.md` |
| The curation skill installed in the QA directory | `ls ~/dev/qa-symposium-evaluate-hypothesis/.claude/skills/symposium-curate-data/SKILL.md` |
| This skill installed in the QA directory | `ls ~/dev/qa-symposium-evaluate-hypothesis/.claude/skills/symposium-evaluate-hypothesis/SKILL.md` |
| Network access | the first run queries public indexes; the second needs none beyond the data server |

Both zips go into the one QA directory: `make -C symposium-curate-data build` and
`make -C symposium-evaluate-hypothesis build`, then unzip each into its `.claude/skills/`.

Set aside an evening for the first run and an hour or two for the second.

## 2. Prerequisite: populate a corpus

Paste this, and nothing else:

```
I want to build a literature corpus for this hypothesis and publish it into Symposium:

If chronic exposure to a high-fat diet alters the gut microbiome's bile acid
metabolism, then colonic epithelial cells show increased proliferation markers,
because secondary bile acids act as FXR antagonists in the colonic epithelium.
```

This is the curation skill's own rehearsal, and
[its REHEARSAL.md](../symposium-curate-data/REHEARSAL.md) is the full account of what to expect.
For the purpose here, the short form:

- **A session and a community come first.** With neither in place it takes you through standing
  up a local data server and founding a community. Name the community `corpus_bile_fxr` and note
  the handle you give; the second run needs both.
- **At the scale stop**, answer small:

  ```
  4 origins, 12 sources
  ```

- **At the review table**, approve once there is at least one retrieved source bearing on each of
  the three clauses. Reject nothing on the way; a thin corpus is what exercises the coverage stop
  in the second run.
- **Let it publish to the end** and read its closing report. Note which clause it says the corpus
  carries least well.

Leave the data server running. Open a **new** session in the same QA directory for the next part.

## 3. The evaluation prompt

Paste this, and nothing else:

```
Evaluate this hypothesis against the corpus in the corpus_bile_fxr community in Symposium,
and publish the evaluation into a new community on the local data server:

If chronic exposure to a high-fat diet alters the gut microbiome's bile acid
metabolism, then colonic epithelial cells show increased proliferation markers,
because secondary bile acids act as FXR antagonists in the colonic epithelium.
```

## 4. What to expect, and what to answer

**Which of these hold still.** The *shape* of a run is the baseline — what the skill asks, in what
order, who publishes what, and the form of the report. Which claims it writes, which sources bear
on them and what the verdict is differ with the corpus and from run to run, and differ without
meaning anything. Judge the shape.

**The skill is reached at all.** The prompt names no skill. It should be routed here on the
strength of its description. An agent that starts reading papers from the web is the first
finding, and it is a `description` problem.

**The three inputs, in order.** The hypothesis is complete, so it should pass without a question.
For the corpus community it should list the communities and handles this machine holds and let
you choose; pick `corpus_bile_fxr` and the handle from the first run. For the eval community it
should offer an existing one you administer or a new one; choose new, on the local data server.
Expect a suggested name drawn from the hypothesis, within Symposium's limits for a community
name, and a question for the admin's handle. Accept the name; answer `evaladmin`.

**It reads before it builds.** Before any artifact exists, expect it to say in its own words what
an Argument's verdict, rationale and scope hold, what each of the six publishing roles may
publish, how content held outside the record is cited, and what contesting an Argument amounts
to. An agent that starts writing artifact JSON without having gone for the role charters is the
finding.

**Stop one: the roster.** A table of six roles — Lead, Methodologist, Librarian, Analyst, Skeptic,
Adjudicator — each with a publishing role and a handle, all *to invite*, and the choices approve,
change, cancel, offered as a list. Choose **change**, rename `skeptic` to `critic1`, and expect
the whole display again with the new handle. Then **approve**. Six members should be invited and
joined, and the Lead should not be the admin.

**The corpus is read once.** Expect one sync of the corpus session, a return to the eval session,
and an index built in a scratch folder. No web search, and no fetch of a publisher's page, at any
point in this run. Either is a finding.

**A goal is published first**, by the Lead, and it says a bounded negative is a complete result.

**Stop two: the claim set and criteria.** Before any evidence is read. A table of five to ten
claims with type, importance, diagnosticity, the statement and what counts against it: exactly
one relationship claim, at least one context claim, at least three mechanism steps. Under it the
rivals, each with the observation that separates it, then the three scales and the integration
rule, and the audit showing four passes. Choices: approve, revise, regenerate, cancel.

Claims that are the hypothesis's three clauses copied across are a finding. So is a mechanism
step with no rival named.

Choose **revise** and say:

```
Add a reversal claim: restoring FXR signalling should reduce the proliferation markers.
```

Expect the display again with the claim added and the audit re-run. Then **approve**.

**Stop three: corpus coverage — perhaps.** It appears only where a must-hold claim has no source.
With a twelve-source corpus it often does. Where it appears, expect a table of claims against the
sources that could bear on them and the choices continue, revise claims, cancel; choose
**continue**. Where every must-hold claim is covered, the run goes straight on, and that is
correct.

**Reading fans out.** Where the environment has sub-agents, expect collecting and appraising to
run across several at once, and one skeptic per claim. Expect all publishing to come from the main
agent, one submission at a time, with the session read back before each. A sub-agent that selects
a session or publishes is the most important finding this rehearsal can produce.

**The gate gets run between layers**, as the admin, and the member is reselected after it.

**The report**, shown in full at the end: the header, then *Verdict*, *The hypothesis as
evaluated*, *Claims and verdicts*, *Rival explanations*, *Certainty and limits*, *What would
settle it*, *Method and departures*, *Where it is* — those headings, that order. About two pages.

**The working file is in the QA directory**, at `.symposium-evaluate-hypothesis/run.json`, with
the scratch folder beside it. Nothing of the run's is written under your home directory.

**It resumes.** Stop it during the claim Arguments and start a new session in the same directory
with *carry on with the evaluation*. It should read the working file, reselect and confirm the session, and pick up at
the next unpublished claim.

## 5. What to read in the record afterward

Browse the eval community's record and check:

- **the order the gate accepted things**: goal, then claim set and criteria, then pointers, then
  claim Arguments, challenges, any revisions, the verdict, proposed tests, the report. The claim
  set's `created` is earlier than every claim Argument's
- **each artifact is published by the member whose role it is**, and names the goal in
  `serves_goals`
- **pointers**: one per corpus source relied on, each a `ScientificPublication` or `Data` with a
  `download` Content whose location leads to the artifact in `corpus_bile_fxr`, and an
  `import_method` saying so. Where a verdict quotes a passage, the pointer carries that passage
- **every Ground in a claim Argument cites a pointer**, by address. A URL in a Ground's place, or
  a claim resting on something that is in neither community, is the defect this skill is built to
  avoid
- **claim Arguments read as reasoning**: the rationale walks evidence for and against and arrives
  at the verdict, and the verdict uses the fixed words. Open three. Where they share a shape with
  the nouns swapped, the judging degraded
- **the testability gate was applied**: a claim whose only evidence could not have observed the
  readout is *not tested*, never *contradicted*
- **challenges exist**, one per claim, published by the Skeptic's handle, and each either drew a
  superseding Argument or was left standing and weighed in the verdict
- **the verdict Argument** grounds on the claim Arguments, states coverage, and gives both
  verdicts — the relation and the mechanism
- **the report** asserts nothing the Arguments do not, links each statement to its Argument, and
  says plainly where the corpus goes against the hypothesis
- **the corpus community is as the first run left it**: same artifacts, same members

## 6. Teardown

Stop the data server container and remove its state directory. Remove both throwaway communities'
sessions under `~/.symposium/`, and the two working folders in the QA directory,
`.symposium-curate-data/` and `.symposium-evaluate-hypothesis/`.
