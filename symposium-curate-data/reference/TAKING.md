# Taking

What may be taken from a source, and what travels by reference instead.

This is the one rule set here that touches derivation, and it is here because Symposium leaves it
open. Symposium's import-fidelity policy governs how a table is rendered once you have it —
header detection, multi-tier flattening, coercion, what may be dropped — and it begins from
material you already have the right to use. This skill is the one that went out and fetched
third-party copyrighted documents, so what may be taken from them is its question to answer.

## The governing distinction

**Measurements are observations of the world; sentences are authored expression.**

That is why a results table is rendered rather than paraphrased — the numbers are the finding, and
a record that restates them in other words is worthless — while a paragraph is taken in bounded,
attributed selections, because the wording is the authors' work.

The distinction is a guide rather than a bright line. A table's selection and arrangement can
carry authorship even where its values do not; some jurisdictions protect a database as such; and
a supplementary table is, as Symposium's own fidelity policy puts it, a document rather than a
dataset. So the rule is to render what a Ground will stand on, record the licence found during
curation, and say in `import_method` what was taken — rather than treating "it is data" as a
licence to copy a publisher's compilation entire.

These are editorial rules for this corpus, not legal advice. That is why rule 7 records the
licence instead of ruling on it.

## The rules

**1. The document stays where it is.** Each source is published as a `ScientificPublication` whose
`download` Content carries its location and the hash computed on fetch. That artifact is the
source's whole representation in the record, and every other artifact derived from it reaches it
by address rather than repeating the location.

**2. A data table is published as data.** Measurements, counts, coordinates, accessions, rates —
rendered to CSV and published as recorded, for the tables an Argument turns on rather than every
table a paper carries. Symposium's import-fidelity policy governs the rendering, and it is strict
about losing nothing and writing down what the translation cost.

**3. A prose passage is published as a quotation.** Selected because a named Ground will stand on
it, bounded to what that Ground needs, with the paper's authors in `authors` and `import_method`
stating what was taken and what was left behind. A few paragraphs standing in for a named claim is
citation; a chapter is a copy.

**4. Everything derived is written in your own words.** Assertions, rationales, Assumptions, an
Argument's scope and verdict are your reading of the source, so they read as yours.

**5. Figures are reproduced by reference.** A caption is text and travels as a quotation; the
figure itself is reached through the publication's address.

**6. Deposited data is cited at its deposit.** Material in a repository was deposited for reuse
and carries its own accession, so that accession is the source's location rather than a paper's
copy of it.

**7. Record the licence you found.** Curation already read it, so it travels into the publication
artifact, and a later member can judge reuse without going back to the publisher.

**8. Where a licence closes off the selection you want,** publish the publication artifact with
its `download` and extract the Argument instead. The reasoning is yours, and it reaches the source
by address — Symposium's importer role offers this fallback for a different reason, and it serves
here too.
