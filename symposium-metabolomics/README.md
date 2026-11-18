# symposium-metabolomics

An agent skill that takes an untargeted LC-MS/MS metabolomics study from a
[GNPS2](https://gnps2.org) Everything Bagel task to biological findings, and keeps all of it in
[Symposium](https://github.com/ndexbio/symposium) community records.

It works in two modes, and each ends in a record.

**Analyze** takes one GNPS2 task and a question. It fetches the task's feature table, spectra,
annotations and molecular network; checks internal standards, feature merges and batch effects;
filters, normalizes and tests; and describes detection rates and the molecular network. Every
decision that matters is put to you with a recommendation. It leaves in a **library community**
the inputs, each analysis with the decisions it made, the result tables and figures, and a
technical report. It stays technical: no biology.

**Interpret** takes an analysis a library holds. It evaluates every pattern in it, stops for you
to choose which to pursue, then follows each through the molecular network, the literature and
further analyses you approve, and challenges what it finds. It leaves in an **interpretation
community** each finding as an Argument anyone can check or contest, and two reports, a short
main one and a full one.

A lab analyses a task once. Any member can then interpret it, any number of times, without
fetching or processing the data again, and what each interpretation finds in the literature is
added to the library for the next.

## System requirements

| What | Needed for | How to check |
|---|---|---|
| The **Symposium skill**, installed alongside this one, in a release that says how a skill built on it keeps a run | both modes | `ls ~/.claude/skills/symposium/reference/RUNS.md` (or the same path under your agent's skills directory). Releases: [ndexbio/symposium](https://github.com/ndexbio/symposium/releases) |
| **Python 3.9 or later** with **numpy**, **pandas**, **scipy 1.10 or later**, a plotting library and a PDF library | both modes | `python3 -c "import numpy, pandas, scipy, matplotlib, reportlab; print(scipy.__version__)"` |
| statsmodels, scikit-learn, openpyxl, networkx | most studies' models, and spreadsheet inputs | `python3 -c "import statsmodels, sklearn, openpyxl, networkx"` |
| **Network access to gnps2.org** | analyze | `curl -s -o /dev/null -w "%{http_code}\n" https://gnps2.org/` prints `200` |
| A reachable **Symposium data server** | both modes | the Symposium skill reports the sessions this machine holds |
| A **library community** you can publish to | analyze; interpret, to add the literature it finds | you hold a member's session in it |
| An **interpretation community** you can publish to | interpret | you hold a member's session in it, or can found one |
| The **GNPS2 connector**, optional | chromatograms and per-feature spectra | the skill says in its first message whether it is connected |

Install the Python libraries with:

```sh
python3 -m pip install numpy pandas "scipy>=1.10" matplotlib reportlab statsmodels scikit-learn openpyxl networkx
```

Where there is no data server or community yet, the Symposium skill takes you through standing
one up, founding a community and joining it.

## Installing

Download `symposium-metabolomics_skill-<version>.zip` from this repository's
[releases](https://github.com/ndexbio/symposium-skills/releases) and unzip it into your agent's
skills directory, beside the Symposium skill:

```sh
unzip symposium-metabolomics_skill-<version>.zip -d ~/.claude/skills
```

Use `~/.agents/skills` for an agent other than Claude, or `<folder>/.claude/skills` to install
it for one folder only.

## Starting a mode

You start a mode by asking for what you want, in your own words. The skill says which mode it is
starting, in one line, before it does anything.

| You | Mode that starts | Example prompt |
|---|---|---|
| give a GNPS2 task and ask for it to be processed, analysed or checked | analyze | *Analyze GNPS2 Everything Bagel task `a9552f8e5018401ba4af91934f916289` into our library `ibd_library`: how does surgery affect the stool metabolome?* |
| ask what an analysis means, for hypotheses, or for interpretation, naming an analysis a library already holds | interpret | *Interpret the surgery analysis in `ibd_library` and publish the findings into `ibd_surgery`.* |
| give a task and ask a biological question in one request | analyze, then it stops | *Investigate this IBD study, task `a9552f8e…`: how does surgery affect the metabolome, initially and over time?* |
| say neither clearly | it asks | a list: each run you can resume, a new analysis, a new interpretation |

Three things hold whichever way you ask:

- **Analyze never runs on into interpretation.** It closes by telling you interpretation is
  available, and waits to be asked.
- **Interpret needs an analysis that is in a library.** If the library holds none, it says so
  and offers to run analyze. If it holds several, it lists them and you pick.
- **Nothing is published until you approve it.** Each mode works in a folder of its own on your
  machine, shows you its draft report, and changes it as often as you ask.

### Worked example: analyze

```
You    Analyze GNPS2 Everything Bagel task a9552f8e5018401ba4af91934f916289 into our library
       ibd_library. I want to know how surgery impacts the metabolome, both initially and over
       time. Metadata is in ~/ibd/gnps_metadata.tsv, run order in ~/ibd/run_order.xlsx.
       Internal standards were sulfamethazine and sulfadimethoxine.

Skill  Starting analyze: GNPS2 task a9552f8e… into the library community ibd_library.
```

It then stops for you at these points, and at each one tells you what it recommends and what the
alternatives would change:

| Stop | What you are asked | A typical answer |
|---|---|---|
| Reuse | only where the library already holds work on this task: which stages to reuse and which to redo | *Approved.* |
| Design and data | how the comparison is defined, which samples are in scope, whether the table is raw, which files to use | *1. Approved. 2. Crohn's only. 3. Yes, it is raw.* |
| Processing | merges, blank filter, prevalence filter, normalization, how zeros are handled | *Go with your recommendations; no internal-standard normalization.* |
| Review | features removed that may deserve adding back; which technical follow-ups to run | *Add back those removed by the prevalence filter only. Run the first two follow-ups.* |
| Draft report | the technical report, shown in full; ask for any change | *Approved.* |
| What leaves this machine | your question as it will be published, and each file of yours that will be stored with the community | *Yes, publish.* |

When you approve, it publishes to the library and closes:

```
Skill  # Technical report: surgery and the stool metabolome (MSV000082221)
       …the report, in full…

       Interpretation of this analysis is available when you ask for it.
       Report file: /Users/you/.symposium-metabolomics/runs/ibd_library-ibd_surgery_metabolome/ibd_surgery_metabolome_analysis_20261117T181502Z_ibd_library.pdf
```

### Worked example: interpret

```
You    Interpret the surgery analysis in ibd_library and publish the findings into ibd_surgery.

Skill  Starting interpret: the analysis "surgery and the stool metabolome" (task a9552f8e…,
       accepted 17 Nov 2026) in ibd_library, publishing into ibd_surgery. The question stands
       as: how does surgery impact the metabolome, both initially and over time?
```

| Stop | What you are asked | A typical answer |
|---|---|---|
| Intake | the defaults: audience, evidence thresholds, feature scope, report length, the three molecular-network questions | *Approved for all.* |
| Pattern checkpoint | every pattern it found, each evaluated; which to pursue; where the community already holds findings on this analysis, how each new one relates to them | *Go with your recommendations, and pursue the detection pattern too.* |
| Further analyses | each group of analyses a hypothesis calls for, with what each outcome would mean | *Yes to the plate-adjusted model and the anatomy model.* |
| Draft reports | the main report, shown in full, and the full report; ask for any change | *Approved.* |
| What leaves this machine | your request as it will be published | *Yes, publish.* |

It closes the same way, with the main report in full and two last lines:

```
       Full report file: /Users/you/.symposium-metabolomics/runs/ibd_surgery-ibd_surgery_metabolome/ibd_surgery_metabolome_interpretation_full_20261118T093011Z_ibd_surgery.pdf
       Report file: /Users/you/.symposium-metabolomics/runs/ibd_surgery-ibd_surgery_metabolome/ibd_surgery_metabolome_interpretation_20261118T093011Z_ibd_surgery.pdf
```

## From analysis to interpretation

- **In the same session:** when analyze closes, say *interpret it* (and name the interpretation
  community). It starts a new run with the library already known.
- **In a later session:** ask to interpret the analysis and name the library. It finds the
  analysis in the library's record.
- **A colleague's analysis:** you need a session that can read the library, and one that can
  publish to an interpretation community. Access that can also publish to the library lets the
  run add the papers it finds there; without it, it tells you which papers it could not add
  and asks a member of the library to bring them in.
- **A second question on the same data:** ask analyze for it. It shows you which stages it will
  reuse from the library and which it will run again for the new comparison, and publishes only
  what is new.
- **A second interpretation of the same analysis:** it shows you each of its patterns beside
  the finding already in the community that it matches, and publishes only what adds something.

## When things are not straightforward

| What happens | What the skill does |
|---|---|
| Your request could mean either mode | asks, with a list |
| The library holds no analysis | says so, and offers to run analyze |
| The analysis you are interpreting has since been superseded | tells you when the run is next taken up, and asks whether to carry on or start from the newer one |
| A session ends partway | the next session lists the runs on this machine, each with the stage it reached; pick one to resume |
| Another session is working the run | lists it as in use; it is that session's to work |
| gnps2.org is not reachable | says so, tries the browser, then asks you to attach the files |
| There are no pooled QC samples | reports that batch correction is not possible, and why |
| The gate refuses something | tells you what the gate said, and stops; what to change is your decision |
| You want a change after publishing | publishes a correction that supersedes the earlier artifact and says what changed |

## What ends up where

| | Where |
|---|---|
| Inputs held at gnps2.org | cited at gnps2.org from the library, with the digest of what was fetched |
| Inputs you supplied | stored with the library, with your confirmation |
| Each analysis and its decisions | the library |
| Result tables and figures | the library; large tables as files the record cites |
| Literature sources | the library |
| Findings, and the analyses a hypothesis called for | the interpretation community |
| Reports | the community of the mode that wrote them, and a PDF on your machine |
| Work in progress and drafts | `~/.symposium-metabolomics/` on your machine |

## Batch and drift correction

Where a study has pooled QC samples, injection order and batch labels, analyze checks whether
correction is needed and corrects only if it is, with `scripts/qcrsc.py`: a Python
implementation of QC-based robust spline signal correction (Dunn et al. 2011, Nat Protoc 6:1060;
Broadhurst et al. 2018, Metabolomics 14:72), validated against QC:MXP on one dataset. It is not
QC:MXP. It scores every QC with a model that never saw it, so the numbers it reports are
held-out.

```sh
python3 scripts/qcrsc.py selftest
```

## Licence

MIT. See `LICENSE`.
