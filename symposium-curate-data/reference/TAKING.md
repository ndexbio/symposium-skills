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
rendered to CSV and published as recorded, for the tables that report a result bearing on the
hypothesis rather than every table a paper carries. Symposium's import-fidelity policy governs the
rendering, and it is strict about losing nothing and writing down what the translation cost.

**3. A prose passage is published as a quotation.** Selected because it states a result that bears
on the hypothesis — one the extracted Argument grounds on, or one a later Argument in this record
will need — bounded to the sentences that state it, with the paper's authors in `authors` and
`import_method` stating what was taken and what was left behind. A few paragraphs standing in for a
named claim is citation; a chapter is a copy.

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

## Take what the hypothesis needs

The corpus is built to be evaluated against, and whoever evaluates it reads this record, with the
source out of reach. **A result left in the source is a result the record cannot be asked about.**
So selection follows the hypothesis, across the whole of a source's results, and the Argument you
extract is one use of what you took among several.

Go through each retrieved source's results and take every one that bears on a clause:

- **each experimental arm** that changes the cause, or a step of the rationale, and reads the
  effect — the sentence that says what was compared with what, and the sentence that gives the
  readout. A paper with a diet arm, a transfer arm and a drug arm has three, and one taken does
  not stand for the others;
- **the arms that came out against the hypothesis, or null**, with the care given to the ones
  that came out for it;
- **the conditions** each result holds under — species or model, tissue, the agent and its dose,
  the duration. These decide whether a later reader may apply the result to the hypothesis at all;
- **the measurements**, as a table, where the source reports them as one.

Rule 3 still bounds each selection: the sentences that state the result, and no more. Where a
bearing result stays behind — it is carried only by a figure, or a licence closes it off — name it
in `import_method`, so the record shows that the source holds more than was taken.

## Rendering from HTML or a flat PDF

A passage from a publisher's page or a PDF's text layer is as quotable as one from structured
text. The community's fidelity policy governs what a rendering may change; these are the places
an unstructured copy goes wrong on the way.

- **Take the words of the article body**, as a reader sees them. Navigation, banners, reference
  markers and markup are the page's, and stay behind. The words are left exactly as they are.
- **A PDF's text layer breaks lines where the page did.** Rejoin a word hyphenated at a line end,
  keep columns in reading order, and leave out running heads and page numbers. A figure caption
  is its own passage, and does not run on from the paragraph above it.
- **Check the passage against the copy you fetched** before it is published. It appears there,
  word for word.
- **Render a table only where its rows and columns can be recovered without guessing.** Where
  they cannot, quote the sentence that reports the numbers and say in `import_method` that the
  table was left unrendered.
- **Say what it was taken from** in `import_method`: publisher HTML or a PDF text layer, and how
  the text was obtained from it.
- **A copy with no text layer yields no quotation.** Say so in the note; the source stays a
  citation until a readable copy is added.
