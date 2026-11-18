# Rehearsal — symposium-metabolomics

What a correct run looks like, end to end, and how to tell that a change to this skill's prose
has not broken it.

This is the baseline a change is read against. The repository's [README](../README.md) says how
a rehearsal is run and read in general; the short version is: build, install into a directory of
its own, open a **fresh** session there, paste **only** the prompt, answer its stops from the
answers file, and compare what it published against the expectations here.

> Keep this document, and everything under [`rehearsal/`](rehearsal/), where the session under
> test cannot read it. They say what is supposed to happen, so an agent that reads them performs
> these expectations instead of showing whether the skill produces them unaided. A session reads
> the folder it is started in: start it in the QA directory, and keep this repository, the
> answers and the gold fixture outside that directory.

Nothing below restates what Symposium documents. Standing up a data server, founding a
community, joining it and running the gate are Symposium's, and whether an agent gets there from
Symposium's own documentation is part of what this rehearsal tests.

## What it is checked against

The skill this one was built from kept everything as local files. Its author ran it on one study
and kept the whole output; that run is the **gold standard**, and it is in this repository as a
fixture, so a rehearsal runs this skill only.

| In [`rehearsal/`](rehearsal/) | What it is |
|---|---|
| [`prompt.txt`](rehearsal/prompt.txt) | the first prompt, which starts analyze |
| [`prompt-interpret.txt`](rehearsal/prompt-interpret.txt) | the request that starts interpret |
| [`answers.md`](rehearsal/answers.md) | the answer to give at each stop, keyed by what it decides |
| [`inputs/`](rehearsal/inputs/) | the four files the user supplied (1.5 MB) |
| [`gold/`](rehearsal/gold/) | the gold run's small outputs as it wrote them: decision logs, preferences, hypothesis record, pattern summary, tables under 50 KB |
| [`gold-manifest.json`](rehearsal/gold-manifest.json) | every file of the gold run with its size, its digest and what it becomes in a record |
| [`gold-facts.json`](rehearsal/gold-facts.json), [`gold-per-feature.csv`](rehearsal/gold-per-feature.csv) | every value an assertion reads, extracted from the gold run |
| [`variation.json`](rehearsal/variation.json) | how far the original skill sat from itself when run twice, which sets each tolerance |
| [`extract_record.py`](rehearsal/extract_record.py) | reads this skill's records and writes the same facts for a run |
| [`extract_local.py`](rehearsal/extract_local.py) | the same for a folder the original skill wrote; how the gold facts were made |
| [`compare.py`](rehearsal/compare.py) | prints the assertion table for a run |

**The study**: MassIVE MSV000082221, IBD stool, positive mode. **The task**: GNPS2 Everything
Bagel `a9552f8e5018401ba4af91934f916289` on gnps2.org, served without login. **The question**:
how surgery impacts the metabolome, initially and over time.

**The tolerances are measured, not chosen.** The original skill was run a second time on the same
task with the same decisions. What came out identical is asserted exactly; what came out close is
asserted within the band the two runs showed; what the original skill itself did not reproduce —
how many patterns, how compound classes were counted, what the tables were called — is not
asserted at all. `variation.json` has the numbers.

## 1. What you need in place

| | How to check |
|---|---|
| A container runtime | `docker info` or `podman info` answers |
| The Symposium skill, in a release that says how a skill built on it keeps a run | `ls <skills>/symposium/reference/RUNS.md` |
| This skill installed in the QA directory | `ls ~/dev/qa-metabolomics/.claude/skills/symposium-metabolomics/SKILL.md` |
| Python with the libraries | `python3 -c "import numpy, pandas, scipy, matplotlib, reportlab, statsmodels, sklearn, openpyxl, networkx"` in the environment the session will use |
| Network access to gnps2.org | `curl -s -o /dev/null -w "%{http_code}\n" -H "Range: bytes=0-400" "https://gnps2.org/resultfile?task=a9552f8e5018401ba4af91934f916289&file=nf_output/networking/filtered_pairs.tsv"` prints `206` |
| The four input files, in a folder the session can read | copy [`rehearsal/inputs/`](rehearsal/inputs/) into the QA directory as `input/` |
| A data server, and for each community an admin and a publishing member on this machine | found the communities before the run; Symposium's documents say how |

```sh
make -C symposium-metabolomics deploy-local SKILLS=$HOME/dev/qa-metabolomics/.claude/skills
```

Use a data server and communities made for the rehearsal. A record is append-only: **each run
needs a community nothing has been published to.**

**Run the session under test on Opus 5.x or a smaller model**, named when the session is
started (`claude --model <model>`), to keep the cost of each run down. Allow about an hour and a
half of the agent's time for each mode.

## 2. The run: two loops

The two modes are rehearsed apart, so a change to how interpretation is written does not cost a
second analysis.

**Analyze.** Found a new library community. In a fresh session in the QA directory, paste
[`prompt.txt`](rehearsal/prompt.txt) with `<INPUTS>` and `<LIBRARY>` filled in, and nothing
else. Answer each stop from [`answers.md`](rehearsal/answers.md), by what the stop decides: the
skill numbers its questions and its patterns as it finds them, so match on meaning and not on
position. Compare (section 4). Repeat, in a new library each time, until every row passes.

**Interpret.** Keep the library that passed. Found a new interpretation community. In a fresh
session, paste [`prompt-interpret.txt`](rehearsal/prompt-interpret.txt) with `<LIBRARY>` and
`<INTERPRETATION>` filled in. Answer from the same file. Compare. Repeat, in a new
interpretation community each time against the same library, until every row passes.

A change to [reference/INTERPRET.md](reference/INTERPRET.md) or to the interpretation half of
[reference/REPORT.md](reference/REPORT.md) re-runs interpret only. A change to anything analyze
reads re-runs both.

## 3. The expectations

Each row is **exact** (a departure is a regression), **tolerance** (it passes within the band
`variation.json` records) or **judged** (a person reads both sides against what is written here).

### Analyze

| Row | Expectation | Kind |
|---|---|---|
| Activation | The prompt gives a task and a biological question. Analyze starts, says in one line that it is analyze, and nothing of interpretation runs. Its closing message says interpretation is available. | judged |
| Inputs | Every input the analysis's numbers rest on is an import in the library whose digest equals gold's: the quantification table, the MGF, the pairs list, and the four user-supplied files. The GNPS2 files are cited at gnps2.org; the four user files are stored with the community. Whether the network GraphML files are fetched is not compared (the network can be built from the pairs list and the feature table), nor are inputs that hold no data or the task's status page. | exact |
| Inputs set aside | The task's own library hits are fetched and not imported, since the prompt says to use the user's annotations. | judged |
| Decisions | Every decision in `answers.md` is stated in an Analysis's procedure, with its parameters and who made it: surgery defined as prior surgery at the sample; Crohn's primary and UC descriptive; no merges; solvent blanks at ratio 5; prevalence 20% in at least one Crohn's surgery group; sum (TIC) with rCLR as sensitivity and no internal-standard normalization; zeros to half the minimum; the add-back rule; the two follow-ups. | judged |
| Counts | 24,770 features in; 166 merge candidates; no merge applied. Features retained within 1% of 11,363. | exact / tolerance |
| Add-back | The user's add-back rule is applied to the features the review flagged: those removed by prevalence alone are added back into the primary family, those removed by the blank filter stay out, and no contaminant or additive is added. How many are flagged depends on the review's own criteria, so the count is not compared. | judged |
| Batch correction | The check runs and reports that correction is not possible, because there are no pooled QC samples. Sum (TIC) normalization is applied. | exact |
| Statistics | Per-feature effect size and q rank-correlate with gold at 0.99 or more. Baseline hits at q < 0.05 within 5% of 1,540, overlapping gold's at Jaccard 0.90 or more, with direction agreeing for 99% or more. 16 features with a surgery × time interaction. | tolerance |
| Detection rate | The five bins hold 420, 10,495, 4,043, 4,337 and 5,475 features. | exact |
| Network | 2,928 nodes, 4,629 edges, 524 families, 5,964 singletons, 8,892 MS/MS features, largest family 96; family-size bins 287, 140, 78, 19; the delta-mass edge counts. The same compound-class scheme as gold; the count in each class is not compared. | exact |
| Report | Every number in the gold technical report's summary and findings table appears in the report artifact, within its band. | judged |
| Publish timing | Nothing is in the library before the user approves the draft. A revision asked for before approval publishes nothing. | exact |
| Completeness | Every file in `gold-manifest.json` whose `becomes` begins `library:` has its counterpart: an artifact, or a file an artifact cites. Nothing the run produced is local only, apart from its own folder. | judged |
| Conclusion | The report artifact is accepted. The closing message is that report in Markdown. Its last line is `Report file:` and a full path, and a PDF is at that path, in the run's folder. | exact |

### Interpret

| Row | Expectation | Kind |
|---|---|---|
| Activation | Asked against a library holding no accepted analysis, interpret says so and offers analyze. Asked against the library that passed, it names the analysis it starts from and confirms the question before anything else. | judged |
| Themes | Each of these is a finding, with this direction: bile acids split by microbial processing (primary and conjugated higher with surgery, microbially processed lower); urobilinoids lower; acylcarnitines higher; N-acyl lipids differ; fewer features detected per sample; over time inconclusive, because time point and plate are confounded. How many patterns the scan reports is not compared. | judged |
| Findings | Each gold hypothesis (`rehearsal/gold/…/hypothesis_record_v3.yaml`) has an Argument or a conjecture making the same claim at the same confidence. The approved follow-ups are published with their tables: the anatomy model, the plate-adjusted and within-plate time models, the antibiotic and the disease-activity adjustments, the bile-acid balance score, the UC check. No finding contradicts gold. | judged |
| Literature | Every source a finding cites is in the library. The two sources both gold runs cited are among them: the bilirubin reductase paper (PMID 38172624) and the published study of this cohort. | exact |
| Placement | No Argument is in the library. Every source is in the library. Every Ground cites a pointer whose rows or text equal the library's, character for character. | exact |
| Report | Every number in the gold main report's summary and findings table appears in the report artifact, within its band. | judged |
| Publish timing | Nothing is in the interpretation community before the user approves the drafts. | exact |
| Completeness | Every file in `gold-manifest.json` whose `becomes` begins `interpretation:` has its counterpart. | judged |
| Conclusion | As for analyze, with the main report shown, and `Full report file:` on the line before `Report file:`. | exact |

### Checked once, when the skill's handling of what is already there changes

| Row | How | Expectation |
|---|---|---|
| Reuse | Run the mode a second time on the same task and question, into the same community. | It publishes no input, source, pointer or analysis the community already holds. Analyze shows the existing technical report and publishes nothing. |
| Reuse table | Start analyze a second time on the same task with another comparison, and stop at its intake. | Every input and every stage that does not turn on the question is listed as reused, and the statistics as new. |
| Overlap | Run interpret a second time on the same analysis and question. | It shows an overlap table matching each hypothesis to the finding already there, and publishes no Argument or conjecture restating one. |

## 4. Reading the result

Sync each community as its publishing member, fetch the files its record cites into one folder
(each saved as `<artifact name>.<content name>`), and then:

```sh
python3 rehearsal/extract_record.py \
    --library <library record dir> --interpretation <interpretation record dir> \
    --files <fetched files> --run-json <analyze run.json> --run-json <interpret run.json> \
    --closing <analyze last message> --closing <interpret last message> \
    --out facts.json --per-feature per-feature.csv
python3 rehearsal/compare.py facts.json --per-feature per-feature.csv --mode analyze
```

`--mode interpret` for the second loop. The exit code is 0 when every exact and tolerance row
passes. Rows marked `?` are the judged ones: read what the script prints for both sides against
section 3.

**Read `absent` first.** `extract_record.py` finds a table by what its title and description
say, and prints what it could not find. A table the run published under words the extractor does
not look for reads as a missing table, and that is a fault in the extractor to fix, not in the
skill. Check that list before reading any failure.

To confirm the fixture and the script agree with each other, the gold facts pass against
themselves:

```sh
python3 rehearsal/compare.py rehearsal/gold-facts.json \
    --per-feature rehearsal/gold-per-feature.csv --mode analyze --science-only
```

**A regression** is an exact row that differs, or a tolerance row outside its band. **Not a
regression**: anything `variation.json` lists under `varies_and_is_not_asserted`; a paper found
or not found; a different number of patterns; a table under another name.

## 5. When a row fails

One failing row, one cause. For each:

1. Show the row, what gold holds and what the run holds.
2. Find the prose that produced it: which sentence of which document the session followed, or
   which it had no sentence for.
3. Propose the change: the file, the prose as it stands, the prose proposed, the row it answers.
4. A person approves the change before it is made.
5. Deploy, and run that mode again in a new community. A person approves the run before it
   starts; each one costs what section 1 says.

Do not widen a tolerance to pass a row. A band is what the original skill showed; a run outside
it is doing something the original did not.

## 6. Keeping it worth having

**A change that intentionally alters what the skill produces updates this document and the
fixture with it**, and says so in [CHANGELOG.md](CHANGELOG.md). The gold run itself does not
change: `gold/`, `gold-manifest.json` and what `extract_local.py` reads from the author's run
stay as they are. What changes is the expectation in section 3, with the reason beside it.

Where the GNPS2 task is no longer served, the digests in `gold-facts.json` are still the
reference, and the Inputs row can be checked only against files someone kept.

## 7. Clearing a run

A run's state is under `~/.symposium-metabolomics/`: `runs/<community>-<short name>/` for each
run, and `current/` for which session holds which. Remove the folder of a run you are discarding,
and its pointer. The communities it published to are on the data server, and stay.
