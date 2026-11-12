# Searching

How to turn a hypothesis's facets into queries, and which services answer them.

You arrive here with the facets from step 1 and the scale from step 2. You leave with the
**origins**: the works the search kept as its best direct answers to the hypothesis, up to Max
Origins, each carrying a record of how it was found.

## Four query families

One query over the hypothesis as written finds almost nothing, because a hypothesis worth testing
has rarely been stated before. Search the clauses apart. Each family answers a different question
and feeds a different part of the eventual record:

**The conjunction** — the cause facets with the effect facets. This finds work that already
tested the link. It returns few hits, and they are the ones that change what the corpus is for: if
three groups have tested this and two found nothing, the corpus has a different job than you
thought.

**The arms** — the cause with the outcome vocabulary, and separately the effect with the
population. These find the evidence each half of the hypothesis stands on, and this is where most
of your grounding passages will come from. A hypothesis is usually novel as a conjunction and
well-studied as two halves.

**The rationale** — the proposed mechanism. This finds the work that explains *why*, which is what
Assumptions rest on. A mechanism nobody has written about is a finding worth telling the user.

**The method** — the assay, instrument, cohort or measurement named anywhere in the hypothesis.
This finds whoever can measure this at all, and it is the path to deposited data: groups with the
method have deposits, and deposits are often open when their papers are closed.

Run all four. The best hits across all of them become the origins, and a corpus whose origins come
from only one family is narrower than the hypothesis.

## Expand the vocabulary before spending the budget

A facet term as the user wrote it is one lexicalization among several, and an index matches
strings. Before querying in earnest, widen each facet across:

- the **controlled term** — MeSH for clinical and biomedical concepts, ChEBI and HMDB for
  metabolites, NCBI Taxonomy for organisms, UniProt for proteins, MONDO or DOID for diseases
- **synonyms and superseded names**, which matter most for genes, where symbols are renamed and
  the old symbol is what the older literature used
- a metabolite's **common name, IUPAC name and InChIKey**, which partition the literature between
  chemists and biologists
- **British and American spellings**, and an **abbreviation with its expansion**

There is a cheaper idiom than listing synonyms yourself: **run the query and read what the index
mapped it to.** PubMed returns its own translation of your query, showing which MeSH terms it
expanded into. OpenAlex returns the concepts and topics it assigned to each hit. Both are free
vocabulary built from the literature itself, and feeding them back into the next query is the
difference between a corpus and a keyword match.

## Query an index's structure, not its text box

Every index here exposes structured filters, and filtering is sharper than any string: concept and
topic identifiers, publication year, work type, open-access status, institution.

Where a work carries open full text, **search inside its sections**. This matters more here than
in ordinary literature search, because the thing this skill needs — a number, a measured effect, a
comparison — lives in Results or Methods and rarely in the abstract. A query scoped to a section
finds papers whose abstract never mentions what you are looking for. Treat section-scoped and
field-scoped search as the default rather than the advanced move.

Read each index's current field list from its own documentation rather than trusting a list
written here; these change, and a stale field name fails quietly by matching nothing.

### The services

**Indexes**, for works:

| Index | Good for |
|---|---|
| OpenAlex | the broadest coverage, concept and topic filters, references and citations in one place |
| Europe PMC | full-text search including section scoping, and open full text for a large fraction of biomedicine |
| Crossref | authoritative metadata, licences, and the update relations that reveal retractions |
| PubMed / PMC | MeSH, publication types, and its query translation |
| bioRxiv / medRxiv | the current frontier, twelve to eighteen months ahead of the journals, with the published version linked once it exists |
| Semantic Scholar | citation context and relatedness where the others are thin |

**Repositories**, for deposited data: MassIVE and GNPS, MetaboLights, Metabolomics Workbench,
PRIDE.

## Calibrate before committing

Every index returns a hit count for free, before you fetch anything. Use it.

Three hits means the query is too narrow — usually one facet is over-specified, or a synonym is
missing. Forty thousand means it is too broad, and ranking will hand you the most-cited work in
the field rather than the work about this hypothesis. Tune toward a band of roughly **fifty to
five hundred** before fetching a single record. One request buys the calibration, and the whole
run rests on these queries being the right ones.

## Start from a known item where one exists

If the user names a paper, a lab, a dataset or an assay, start there rather than with a query.
Relatedness computed over citation structure beats relatedness computed over words, so one
known-good work expands better than any phrasing you could construct. Make it an origin, and let
[traversal](TRAVERSING.md) do the rest.

## Search for the contrary deliberately

A corpus assembled only from supporting work is an advocacy file, and the record it produces reads
as one to everyone who comes after.

So query for the contrary by name: null results, failed replications, the reviews that dispute the
mechanism, the cohorts where the effect did not appear. Terms like "no association", "failed to
replicate", "contrary to" find work that a facet query ranks low precisely because it disagrees.

Symposium's Arguments carry verdicts. A corpus that can only produce one verdict has decided the
hypothesis before it was tested.

## Vary the origins, not just the ranks

Ten hits from one group are one piece of evidence wearing ten hats.

So vary deliberately across **research group**, **organism or system**, and **method**. Evidence
that is not independent at search is not independent in the record either — and Symposium's gate
raises an independence review on an Argument whose Grounds all trace to one lab. That review is
decided here, in what you choose to keep, long before anyone sees it.

## Reaching deposited data

Two directions, and both are worth running:

**Forward, from papers.** Read the data availability statement of every origin and pull the
accessions out of it. A paper's deposit is the primary object its figures were made from, and it
is frequently open when the paper is closed.

**Directly, at the repositories.** Query them on organism, instrument, assay and sample type.
This surfaces deposits whose paper never appears in a literature query — because it is in press,
because it is in a journal the indexes cover poorly, or because there is no paper.

## Etiquette, and one rule that overrides the indexes' own advice

OpenAlex, Crossref and NCBI each invite a contact email in exchange for a faster rate-limit pool.
**Supply a generic client token and no contact details**, in any header or parameter. The slower
pool is the cost, and it is a small one. Where an index declines to answer without an address,
tell the user that it did, and move on to the others.

Beyond that: pace the requests, honour `Retry-After` when you receive it, page with cursors rather
than deep offsets, and request only the fields you are going to read.

## Record how a work was found

Every hit keeps the **query family**, the **index** and the **query string** that found it.
[Traversal](TRAVERSING.md) adds the origin and direction for anything reached by the hop.

This is what makes a corpus reproducible, it is what the review table's note is built from, and it
is what lets a user looking at a surprising entry ask how it got there and get an answer.

---

Next: [traversal](TRAVERSING.md), which expands one hop from the origins.
