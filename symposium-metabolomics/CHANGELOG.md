# Changelog — symposium-metabolomics

Versions follow [semver](https://semver.org). The release tag is `symposium-metabolomics-v<version>`, and it
is where the version lives: the build stamps it into the zip's name and into the skill's
frontmatter, as `metadata.version`. The repository's
[README](../README.md#building-and-releasing) has the release steps.

## 0.1.0 — 2026-11-17

The first version. Built from the metabolomics interpretation skillset (v12, package v4.3),
which kept its work as versioned local files; this skill keeps it in Symposium community records.

### What it provides

- **Analyze**: one GNPS2 Everything Bagel task and a question into a library community — the
  inputs, each stage of the analysis with the decisions it made, the result tables and figures, a
  hand-off note and a technical report.
- **Interpret**: an analysis a library holds into an interpretation community — pointers to what
  the library holds, the analyses a hypothesis calls for, findings as Arguments, and a main and a
  full report.
- **A mode works in its own folder and publishes on approval.** Drafts are revised as often as
  the user asks; nothing reaches a record before the user approves it.
- **What a community already holds is reused**: inputs and literature sources by identity,
  analysis stages by their recorded procedure (the reuse table), and findings one by one (the
  overlap table).
- **Literature goes through the library**, so each interpretation finds what earlier ones read.
- **A mode closes** with its report accepted in the record, shown in full, and built as a PDF in
  the run's folder, whose path is the last line.
- `scripts/qcrsc.py`, the batch and drift correction the original shipped, unchanged.

### What changed from the skillset it was built from

- The input folder and its manifest are imports; the decision log is each Analysis's procedure;
  the versioned table and figure folders are the outputs of those Analyses; the hypothesis record
  is the findings; the standing-preferences log is the run's working file.
- Versions of a delivered report are drafts revised before approval. A change after approval
  supersedes.
- The report format is PDF.
- It starts on a request for analysis or interpretation, not on a fixed phrase.

### Requires

The Symposium skill, in a release that says how a skill built on it keeps a run (0.4.2 or
later). Python with numpy, pandas, scipy 1.10 or later, a plotting library and a PDF library.

[Install Skill Instructions](../README.md#installing-skill)
