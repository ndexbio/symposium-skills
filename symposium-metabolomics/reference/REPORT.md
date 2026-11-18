# The Reports

A mode ends in a report. Analyze ends in one **technical report**; interpret ends in a short
**main report** and a **full report**. This document says what each contains and how it looks,
and then how a mode concludes: the report as a published artifact, the report file built from
it, and the closing message (Section 2).

You arrive here with the mode's work done in the run's folder. You draft the report there, show
it, revise it as the user asks, and publish it last, once the user has approved the draft and
everything it links to has been accepted.

## Purpose

Build clear, reproducible reports in one of two distinct modes: the **technical report** that closes the analysis (technical and statistical only; no abstract and no biological interpretation) or the **interpretation reports** (biology-led, a short main report and a full report). Use the mode of the run in hand and never mix their purposes.

**Which sections apply.** Section 0B is the technical report only. Sections 0A, 1, 6, 6A, 7, 8, 10, 11 and the Section 12 checklist are interpretation only. Sections 2, 3, 4, 4A, 4B, 4C, 5 and 9 apply to both modes; in the technical report, read "KEY BIOLOGICAL IDEA" as "KEY TECHNICAL TAKEAWAY" and omit the abstract and biological-interpretation boxes.

---

# 0\. Rules (read first)

0. **Identify the report mode first.** The technical report follows Section 0B; the interpretation reports follow Sections 0A and 1 onward.  
1. **Keep the technical report technical.** Do not discuss biological meaning, pathways, mechanisms, candidate biological states, or biological hypotheses in a the analysis report. Report only data quality, analytical decisions, statistical results, sensitivity, uncertainty, limitations, and technical next steps.  
2. **No abstract in the technical report.** Start with the title/byline, the QUESTION box, the plain-language summary (rule 14; it is a technical summary, not an abstract), then the key comparison and dataset scope, a “Key technical takeaway” and the “At a glance” findings table.  
3. **Interpretation first applies only to the interpretation reports.** Each of their sections opens with its key biological interpretation directly under the heading.  
4. **Two reports applies only to interpretation.** A short main report and a full report must agree (Section 1). The analysis has one technical report unless the user requests otherwise.  
5. **Draft, then publish.** The draft is revised in the run's folder as often as the user asks. The report is published once, when the user approves it; a later change is a report that supersedes it (Section 2).  
6. **Numbered pages, figures and sections** (Section 3).  
7. **Interpretation only:** every key biological finding gets an interpretation schematic (and as many data figures as needed), in the style Section 7 sets out.  
8. **Match the reference visual style** (Section 4).  
9. **Be brief.** Short sentences, one idea per paragraph, no repetition across sections (Section 9).  
10. **Tag every claim** as Observed, Inferred or Speculative, and show raw p with q (Section 5).  
11. **Run the pre-delivery checklist** before sending (Section 12).  
12. **Put the question at the top of every report.** What the user asked, verbatim, in a box at the top of page 1 of every report (Section 4B).  
13. **The technical report includes the internal-standard check, the feature-merge recommendation, the detection-rate section and the molecular-network section** with their tables and figures (Section 0B; [ANALYZE.md](ANALYZE.md), Sections 13B and 13C), or state that no network was available. The interpretation reports include the Molecular-network discovery questions section when approved and a network was available (Section 6A).
14. **Put a plain-language summary under the question of every report** (Section 4C): what was asked, what was found, how far to trust it. The interpretation reports add how the findings fit the literature, cited as numbered references, and a Key references box on page 1. The technical report's summary is technical only: no biology and no literature.

---

# 0A. Report Intake (ask once, at the beginning)

Before building any figure or report, ask the user the questions below, in one short block. Use answers already recorded in the working file ([INTERPRET.md](INTERPRET.md), Section 3A) and do not ask again. Record the answers and apply them to every draft.

| Decision | Recommendation to offer | User decides |
| :---- | :---- | :---- |
| Null results in the main report | Leave out (they are always in the full report); include only the ones the user names | Yes |
| Group colors | Offer a colorblind-safe suggestion, but do not assume one | Yes |

If the user changes an answer later, update the working file and apply it to the next draft. Do not re-ask answered questions.

---

# 0B. The Technical Report

Use this section when building the **technical report** that closes the analysis. Do not apply the interpretation reports' intake or content rules unless the user explicitly asks for a combined report.

## Intake

Before preparing the report, establish or confirm the following. Reuse information already supplied; ask only for decisions that are missing and necessary.

| Decision | Rule |
| :---- | :---- |
| Comparison and scope | State the groups, sample sizes, data source/task IDs, ionization mode, and feature scope. |
| Analysis decisions | Use the decisions and approvals recorded in the working file, as each stage's procedure will state them. Clearly distinguish user-approved choices, recommendations accepted, and deviations. |
| Group colors | Use consistent, distinguishable group colors across figures. Ask only if a choice is needed; do not use the interpretation reports' biological-tier colors to imply group identity. |

## Required structure

1. **Title and scope:** report title, requester, date, and key comparison. **Do not include an abstract.** Directly under the title and byline, the **QUESTION box** (Section 4B), then the **SUMMARY IN PLAIN LANGUAGE box** (Section 4C). The summary is not an abstract.  
2. **At a glance:** a concise **KEY TECHNICAL TAKEAWAY** and a findings table with columns such as *Finding*, *Where*, *Group comparison*, and *How solid*. Include relevant effect sizes, raw p-values, q-values, sample sizes, and sensitivity caveats.  
3. **Source block:** the task and its host, the library community, each input with where it came from (a GNPS2 location, a connector call, a file the user supplied), the versions of the documents and of the batch-correction script the analysis followed, and, where this report supersedes an earlier one, what changed.  
4. **Contents:** include a compact contents list when the report spans multiple sections/pages and it improves navigation.  
5. **Technical sections:** adapt to the dataset, using sections for study design/data, decision workflow, QC assessment, filtering and unfiltered-table preservation, normalization/transformation, sample-level diagnostics, group results, sensitivity analyses, review of flagged/removed features, limitations, open items/technical next steps, deviations, change log, and appendix as applicable.  
6. **Section opening:** begin each numbered section with a short **KEY TECHNICAL TAKEAWAY**. Use **OBSERVED**, **INFERRED (technical)**, and **LIMITS** boxes when they improve clarity. Do not use biological interpretation callouts.  
7. **Figures and tables:** include only items that support a technical or statistical result. Number and cite each figure/table consistently; provide captions, source data, and code where available.  
8. **Detection-rate section (required):** from [ANALYZE.md](ANALYZE.md), Section 13B. Table 1 (bins with features, MS/MS rate and library match rate, per bin and cumulative at more than 1% and more than 50% of samples) and Figure 1 (stacked bars and grouped bars of numbers of features). Under the table, link the three detection-rate tables (bins, cumulative, per feature) by address.  
9. **Molecular-network section (required when a network is available):** from [ANALYZE.md](ANALYZE.md), Section 13C. Table 2 (network summary) and the figures in this order: family sizes, delta-mass inventory, compound-class composition (the master class color key), volcano by class overview, volcano by class faceted. List the `network_*` and `compound_class_*` CSV files under the figures. If no network was available, write one line saying so and why, and name the sections or figures that were therefore not made. Table and figure numbers follow report order (Section 3).  
10. **Internal-standard section (when standards were provided):** from [ANALYZE.md](ANALYZE.md), Section 3.8. A table of each standard with status (intact, split, missing), number of rows, detected samples, RT range and QC CV, and one figure of RT and area across injection order (rows of a split standard in different colors, with a graphical legend). If the user did not know the standards, write one line saying so.  
11. **Feature-merge section:** from [ANALYZE.md](ANALYZE.md), Section 3.9. A table of candidate counts by m/z and RT window, a table of pairs per class (recommend merge, review, do not merge), the user's decision, and example review sheets as figures (mirror plot, chromatogram overlay and library annotation names for each pair; the first lines say which class each example shows). Under the section, link the merge candidates, the merge map, the internal-standard check and the review sheets by address. If no merge was applied, say so and why.  
12. **Batch-and-drift-correction section (when the check or the correction was run):** from [ANALYZE.md](ANALYZE.md), Section 3.10. State the method as QCRSC with its three citations and say that the code is a Python implementation validated against QC:MXP on one dataset, not QC:MXP. Then: the check table (eligible features, share affected, shift size, drift, the recommendation and who decided), the thresholds and the statement that they are first defaults calibrated on one dataset, and the held-out validation table (features with a batch effect before and after, median QC %RSD before and after, features significantly improved and worse, features corrected, partly corrected and not corrected). Figures, in this order: the four-panel necessity figure (PCA before and after, batch R² boxplots, drift boxplots), the one-feature before-and-after figure, the forest plot, and the internal-standard evidence figure when standards were provided. Every QC statistic is labelled held-out or in-sample. Link the batch-correction tables by address under the section, and the group-by-batch table with a sentence on confounding when a group is absent from a batch. If the input was already corrected, name its source and settings and state that QC-based diagnostics of a corrected table are near zero by construction. If the step was skipped, give the check result in one line.  
13. **Normalization-comparison section (required):** from [ANALYZE.md](ANALYZE.md), Section 7.4. A table of the candidate methods with the diagnostics, the recommendation, the user's choice and the method applied, plus the comparison figures with a graphical color key. If the comparison was not run, write one line saying so and why (input already normalized and no raw table provided, or switched off by the user) and name the normalization that was used, if any. If the user named a method, say that the comparison ran as a sensitivity check and whether the methods disagreed.
14. **Hand-off note:** identify outputs, unresolved technical decisions, sensitivity-dependent results, and potential areas for downstream review using neutral feature-level language only.

## Content boundaries

- No abstract, biological interpretation, pathways, mechanisms, biological hypotheses, biological schematics, or claims about biological meaning.  
- Describe what was measured, how it was processed/tested, what the data show, how robust the result is, and what technical limitations remain.  
- If feature names or annotations are shown, treat them only as supplied annotations or identifiers; do not infer biological relevance from them.  
- Distinguish a non-significant result from evidence of no effect, and report power or design limitations where relevant.  
- Report raw p-values alongside q-values or clearly state the multiple-testing family and number of tests. Include effect sizes, confidence intervals where available, and sample sizes.  
- Preserve unfiltered data and document filter criteria, removed features, and reasons where available. When prevalence filtering is discussed, **warn that rare but potentially important features may be lost**, and state where the unfiltered table and removed-feature list are retained.  
- Do not invent analyses or results. Label analyses not run, unavailable inputs, deviations from the planned workflow, and recommendations not yet approved.  
- In the detection-rate and network sections, describe counts, structure, mass differences, class membership and statistics only. A compound class, a molecular family or a delta-mass label is a descriptive grouping, not a statement about biology ([ANALYZE.md](ANALYZE.md), Section 13C.11).

## Pre-delivery checks

- [ ] No abstract is present (the plain-language summary under the question is required and is not an abstract).  
- [ ] Plain-language summary present under the QUESTION box (Section 4C): the four lead-ins, technical only (no biology, no literature), every number matches the report body, and it names the main limits.  
- [ ] No biological interpretation or biological schematics are present.  
- [ ] Every section opens with a technical takeaway.  
- [ ] Reported values agree across text, tables, figures, and source outputs.  
- [ ] Raw p, q/multiple-testing context, effect sizes, and n are reported where applicable.  
- [ ] User decisions, accepted recommendations, and deviations are distinguished.  
- [ ] Filtered and unfiltered tables and removed-feature records are accounted for.  
- [ ] Limitations, unresolved decisions, and analyses not run are explicit.  
- [ ] Figure/table numbering, captions, and page numbering are checked.  
- [ ] Source data and code are included or their absence is stated.  
- [ ] Batch-correction section present with the method, citations, check table, thresholds statement, held-out validation table and the four figures, or a one-line skip statement; every QC statistic is labelled held-out or in-sample; the `batch_corrected` counts agree between text, table and CSV.  
- [ ] Internal-standard section present with its table and figure, or a one-line "standards not provided" statement; feature-merge section present with its count tables, class counts, user decision, review-sheet figures and file list.  
- [ ] The QUESTION box is at the top of page 1 and matches the goal word for word (Section 4B).  
- [ ] Normalization-comparison section present with its table, recommendation, user choice and figures, or a one-line statement of why it was not run; the decision log `normalization_comparison.status` agrees with the report.  
- [ ] Detection-rate section present with Table 1, Figure 1 and its three CSV files; cumulative rows (more than 1% and more than 50% of samples) agree between table, figure and CSV.  
- [ ] Molecular-network section present with Table 2 and the five figures, or a one-line "no network available" statement; network CSV files are listed; nodes + singletons equal MS/MS features.  
- [ ] Every figure page has a footer defining the abbreviations used on that page and the significance cutoff (Section 4, figure standards).  
- [ ] Compound-class colors, shapes and labels are the same in every figure ([ANALYZE.md](ANALYZE.md), Section 13C.6).  
- [ ] Every figure has its 1 to 2 sentence "How to read this figure" line (Section 4, Figures), in plain language, with no result stated in it.  
- [ ] The source block lists every input the analysis used, with where it came from, and names none that was fetched and set aside without saying so.  

---

# 1\. Two Reports

|  | Main report (short) | Full report |
| :---- | :---- | :---- |
| Audience | Anyone who needs the findings quickly | Reviewer, collaborator, future self |
| Length | Per intake (8 to 12 pages recommended) | As long as needed, still concise |
| Contents | One-page summary and findings table; key findings (one section each); contradictory evidence and limits that matter; what it means for the question; testable predictions and next tests; sources | Everything in the main report, plus every pattern investigated (including all nulls), filter-loss review, multi-level class analyses, unannotated feature report, biological pattern summary, exploratory hypotheses, additional analyses, alternative explanations, diet and medication assessment, complete follow-up, methods appendix |
| Figures | The data figures each key finding needs, plus its interpretation schematic | All figures, including supporting and null results |
| Null results | Not included unless the user requested them at intake | Always included |
| Question and molecular-network discovery questions | QUESTION box on page 1; discovery section with up to 3 items per question (Section 6A, if approved) | QUESTION box on page 1; discovery section with every item (if approved) |
| Interpretation | Directly under every heading | Directly under every heading |

**Consistency rules**

* Every number, figure and conclusion in the main report appears identically in the full report.  
* A figure in both reports keeps the same figure number, or the main report says "full report, Fig. N".  
* The main report links onward: each key finding ends with a one-line pointer to the full-report section.  
* Both reports are built from the one published report (Section 2), so they cannot disagree on a number.

---

# 2\. How a Mode Concludes

A mode's last act is its report: published as an artifact, built into a file, and shown.

## 2.1 The report is an artifact

The record holds the report, and the report is the way into the record. Publish it last, as one artifact that orients a reader and that nothing is argued from:

* **Its text is the report, in Markdown**, in the structure this document requires for its mode (Section 0B for the technical report; Sections 1 and 6 onward for interpretation). For interpretation the text is the **full report**; the main report is a selection from it (Section 1).
* **Every statement links to where the record holds it.** A number links to the table it is read from; a finding links to the artifact that argues it; a decision links to the analysis whose procedure states it; the question is quoted from the goal and links to it. The report asserts nothing the record does not already hold.
* **Its tables** — the findings table, the decision workflow table, Table 1 and Table 2 — are in the text, and are also declared so a reader can navigate to a row. Nobody argues from them.
* **Its figures** are named in the text where they belong, each by the address of the table it plots and the figure held beside it, with its "How to read this figure" line.
* **It names the goal it serves.**

It is published after the user has approved the draft and after everything it links to has been accepted, because a link to something not yet in the record is refused.

## 2.2 The order

1. The user approves the draft.
2. Publish everything the report links to, and wait for each to be accepted.
3. Replace each reference in the draft with the address it now has. Publish the report, and wait for it to be accepted.
4. Sync, and read the accepted report from the record. It carries the time it was accepted; the draft does not.
5. Build the report file (Section 2.3), from the accepted report.
6. Record the file's full path in the working file as `report_pdf`, and only then mark the mode done.
7. Send the closing message (Section 2.4).

**Where the gate refuses the report**, there is no report file: report what the gate said, and stop.

**Where a run is resumed**: the record holds an accepted report and the working file has no `report_pdf`, or names a file that is gone — take up at step 4. `report_pdf` names a file that is there — show the report again, and its path.

**Where the user asks for a change after approval**, the changed report is a new artifact that supersedes the earlier one and says what changed and why, in its own words and in a "What changed" line under the summary. Its acceptance time is its own, so its file is a new file; `report_pdf` moves to it, and the earlier file stays. Numbers are never silently replaced.

## 2.3 The report file

A PDF, in the run's folder, beside the working file, laid out as Sections 3 to 4C require, with every figure.

| Mode | File | Holds |
| :---- | :---- | :---- |
| analyze | `<short name>_analysis_<accepted>_<library community>.pdf` | the technical report |
| interpret | `<short name>_interpretation_<accepted>_<interpretation community>.pdf` | the main report |
| interpret | `<short name>_interpretation_full_<accepted>_<interpretation community>.pdf` | the full report |

* `<short name>` is the run's short name, as the working file holds it.
* `<accepted>` is the time the record gives for the accepted report, in UTC, to the second, written `YYYYMMDDTHHMMSSZ`.
* The community is the one the report was published to.

Every part of the name comes from the record and the working file, so building it again gives the same file.

Build the file from the accepted report and from the figures and tables in the run's folder that the report names. Take every number from the accepted report; do not recompute one while laying out a page. Check the pages visually before showing anything (Sections 0B and 12).

Put a **source block** on the first page: the date the report was accepted, the requester, the report type (technical, main or full), the task and its host, the community, the report's address, and the versions of the documents followed.

## 2.4 The closing message

Two things, and only these:

1. **The report, in full, as Markdown** the user reads directly, in the message itself, outside any code block: the accepted report's text, section for section. For interpretation, the main report. Each figure is shown where the text names it, with its "How to read this figure" line.
2. **The last line**: `Report file: <the file's full path>`, written whole, the way the host platform spells it, so the user can copy it. For interpretation, the line before it is `Full report file: <the file's full path>`.

Analyze's message says, directly before those lines, that interpretation is available on request.

Where the host has its own way to hand a file to the user, hand the report file over that way as well.

---

# 3\. Numbering

* **Pages:** footer "Page X of Y" on every page, centered.  
* **Figures:** numbered sequentially through the whole report ("Figure 1", "Figure 2", ...). Every figure is cited in the text before it appears, and every figure number in the text exists. Do not restart numbering by section.  
* **Sections:** numbered headings (1, 2, 3, ...). Sub-headings are unnumbered or use 1.1 only when the report is long.  
* **Tables:** "Table 1", "Table 2", numbered sequentially, separately from figures.  
* **Schematics:** count as figures and are numbered in the same sequence.  
* In the full report, add a short **Contents** list (section, page) after the summary page. The main report does not need one.

---

# 4\. Visual Style (match the reference reports)

**Page and type**

* Letter or A4 portrait, generous margins, clean sans-serif font, short paragraphs.  
* Footer: "Page X of Y". No header clutter.

**Title block (page 1\)**

* Report title; byline line with author or requester and date; then the **QUESTION box** (Section 4B); then the **SUMMARY IN PLAIN LANGUAGE box** (Section 4C); then a one-line definition of the key comparison (for example, how a responder is defined, which arms, sample sizes).  
* Interpretation only: the old 3 to 5 sentence abstract paragraph is replaced by the plain-language summary (Section 4C); do not add both. The **Key references box** (Section 4C.5) sits at the bottom of page 1.  
* **At a glance** section (technical report: a **KEY TECHNICAL TAKEAWAY** box instead; interpretation: an **Overall biological interpretation** box), then a findings table with columns **Finding \| Where \| Group comparison \| How solid**, one row per finding, with effect size and raw p. Add the legend line: effect-size units, and the tag legend (**OBSERVED** direct result, **INFERRED** follows from results, **SPECULATIVE** cannot be tested here).

**Study and patients page**

* A short design paragraph, a definition paragraph for the groups, a compact group-size and clinical-characteristics table, and a **Terms used** box defining ln, composite, mixed model, trend, interaction, SE/SD, MS/MS (adapt to the study). Put this on page 2 of the full report; in the main report keep it to half a page.

**Section headers**

* A thin accent rule (blush rose, `#D4789C`) above each numbered section heading, then the heading in bold dark text, with the number.  
* Directly under the heading: the **KEY BIOLOGICAL IDEA** callout (blush box `#FBEAF1`, small rose caps label `#B03A6F`, bold plum text `#5B1F43`, rounded corners, one to two sentences). This is the interpretation of the section. Required for every section.

**Tagged evidence boxes** (tinted boxes with a small rounded tag)

* **OBSERVED**: soft green box (`#EAF4EC`, text `#2F6B4A`). Bullets with the numbers (effect size, raw p, q, n).  
* **INFERRED**: soft blue box (`#EAEFF8`, text `#3E5A94`). What follows from the observations, with the alternatives.  
* **SPECULATIVE**: soft amber box (`#FDF1E1`, text `#85561A`). Hypotheses that cannot be tested with these data. State the test that would decide it.  
* **LIMITS**: soft mauve-grey box (`#F6F0F3`, text `#6B5A63`), at the end of a section or the report. Sample size, missing records, unadjusted covariates, annotation confidence.  
* Hypothesis cards (white box, rounded border): title, SPECULATIVE tag, then **Supports**, **Gap**, **Predicts** on three short lines.

**Figures**

* Figure number and caption below, in grey: "Figure N. What it shows. How to read it (symbols, bars, brackets)."  
* **"How to read this figure" line (every figure, both modes, main and full reports):** directly under each figure, before or inside the caption block, add a 1 to 2 sentence plain-language description of how to read it: what the axes, colors, symbols, boxes or bars mean, and what to look for (for example "Each dot is one feature; features to the right are higher in group B. Dots above the dashed line pass raw p < 0.05."). Write it for a reader who has not seen this type of plot. It is separate from the caption (which says what the figure shows, n, test and source) and from the finding (it never states the result). Panels of a multi-panel figure share one line unless the panels are different plot types. Figures in the appendix and in the the analysis report (including the detection-rate, network, internal-standard, feature-merge, batch-correction and normalization figures) get it too.  
* Use the group colors the user chose at intake, the same for the same groups in every figure. Keep them constant between chat figures, main report and full report, and check that they remain distinguishable for color-vision deficiency. Do not assume a scheme. (The green and orange in the reference PDF are only an example of one study's choice.)  
* Show individual samples or patients when n is small; bars as mean ± SE; state the test in the caption.  
* **Class balance figures** ([INTERPRET.md](INTERPRET.md), Section 13B): a boxplot per group with one point per sample. The axis label states the orientation (group of interest as the numerator for data-driven variants; stated numerator and denominator sets for a chemistry ratio). The panel shows n, raw p, and the permutation p; the caption says which variant (pre-specified, data-driven, VIP above 1, VIP-weighted) it is and how many features were in each set.  
* Panel titles state the comparison and n. Raw p on the panel; q in the caption or table.  
* No decorative figures.

**Figure standards (all figures, both modes)**

* Every figure includes a graphical color key or legend drawn on the figure (swatches for each group, color, or symbol), not only a text explanation in the caption.
* Show p-values directly on the plot, and give them their own color key (for example, a swatch scale for raw p or q thresholds).
* Use full feature names on the figure (for example "Metformin-pyruvic acid"), not only the partner name or an ID. Add the annotation confidence label where space allows.
* Make figures easy to parse: state on the figure itself what each group is and what a boxplot shows (center line, box, whiskers, points), so the reader needs no caption to read it.
* **Footer on every figure page:** define the abbreviations used on that page (where they first appear, not in a final glossary page) and state the significance cutoff used on that page (for example "Significant = raw Mann-Whitney U p < 0.05 and |log2FC| >= 0.58").
* **p-value keys:** show significance levels with a labeled key (dot size or ring tiers for p < 0.05, 0.01 and 0.001, and labeled threshold lines). Do not use shaded bands or contour lines for p-value levels.
* **Class color keys ([ANALYZE.md](ANALYZE.md), Section 13C.6):** one hue per compound-class group, one shade and marker shape per fine class, the same in every figure; unannotated features in neutral grey. A class key is drawn on each figure that uses it.

**Color for interpretation tiers**

* Observed \= green, Inferred \= blue, Speculative \= amber, Limits \= mauve-grey, using the hex values in Section 4A. Use these consistently everywhere, including in schematics.

---

# 4A. Report Color Theme: Blush and Plum (fixed for all reports)

The report theme is fixed. (Group colors in figures are not part of theme and are asked per project at intake.)

| Element | Hex |
| :---- | :---- |
| Page background | `#FFFFFF` |
| Section accent rule | `#D4789C` (blush rose) |
| Headings | `#4A2340` (deep plum) |
| Body text (suggested) | `#2E2430` |
| Captions and secondary text (suggested) | `#7A6F76` |
| Page and box hairlines (suggested) | `#E4E1E6` |
| KEY BIOLOGICAL IDEA callout: fill / label / text | `#FBEAF1` / `#B03A6F` / `#5B1F43` |
| OBSERVED box: fill / text | `#EAF4EC` / `#2F6B4A` |
| INFERRED box: fill / text | `#EAEFF8` / `#3E5A94` |
| SPECULATIVE box: fill / text | `#FDF1E1` / `#85561A` |
| LIMITS box: fill / text | `#F6F0F3` / `#6B5A63` |

**Rules**

* Rounded corners on boxes and callouts (about 8 px); accent rule about 4 px thick with rounded ends.  
* Schematics: solid-outline boxes use the Observed colors; dashed-outline boxes use the Inferred or Speculative colors, matching the tier of the claim; arrows and labels in plum or `#7A6F76`. Never use plum or rose fills to mean a result tier.  
* Do not use rose or plum as group colors in data figures unless the user chooses them at intake, so theme does not clash with the data.  
* Text on any colored box uses the box's own dark text color above, never black or grey.  
* Keep a minimum text contrast suitable for print and screen. Check headings and box text before delivery.  
* Hex values marked "suggested" were not in the approved mock-up; they may be adjusted for legibility without asking.

---

# 4B. The Question Box (all reports, both modes)

Every report starts with the **question**: what the user asked, copied **verbatim** from the goal the run serves. It lets the reader judge the findings against what was asked, and it is the reference text for the molecular-network discovery questions in interpretation ([INTERPRET.md](INTERPRET.md), Section 5B).

* **What:** the user's request as the goal holds it, unedited: the task, the question and any stated hypothesis. Keep the wording, line breaks, spelling and punctuation. Do not paraphrase, summarize, correct or shorten it. Below it, list the names of the files the user supplied (names only). If the request states no question, show it as it is and add a line "Question as confirmed at intake:" quoting the user's answer in their own words. In an interpretation report, where the user's request for interpretation named a question of its own, show that, and under it the question the analysis served.  
* **Where:** top of page 1, directly under the title and byline line, before the key-comparison paragraph and *At a glance*. It appears in the technical report and in both interpretation reports (main and full). It is not numbered and is not a figure. The plain-language summary (Section 4C) follows it directly.  
* **Look:** white box with a 1 px hairline border (`#E4E1E6`) and rounded corners; a small-caps label "QUESTION" in `#7A6F76`; body text in `#2E2430`, slightly smaller than the body text, left-aligned. No tier colors or tags (it is not a claim). If the text is longer than half a page, set it smaller but keep it whole.  
* **If the question changes:** the goal is revised in the record, and the report shows both: the original in the box, and one line "Update to the question (date):" with the new wording.  
* **Privacy check:** the question is published word for word. If it contains credentials or access tokens, stop and ask the user before including it; confirm paths and names with the user before publishing.

---

# 4C. Plain-Language Summary Box (all reports, both modes)

Every report has a short summary written for a reader who does not work in metabolomics. It answers the question that was asked, in the words of the question, and says how far the result can be trusted.

## 4C.1 Placement and look

* **Where:** top of page 1, directly under the QUESTION box (Section 4B), before the key-comparison paragraph. Both interpretation reports (main and full) and every the analysis report have it. It is not numbered and is not a figure. In interpretation it replaces the old abstract paragraph.
* **Look:** a box with a small-caps label "SUMMARY IN PLAIN LANGUAGE", a pale tint of the report accent color and a 1.5 px border in the report's dark accent, so it reads as different from the white QUESTION box and from the rose KEY callout. No evidence tags inside it (the findings table below carries them).

## 4C.2 Wording rules

* Plain language: no unexplained abbreviations or statistical jargon. Name a technical term only if the reader needs it, and give it a short gloss the first time (for example, "glucuronic acid tag").
* Every number and claim in the box must also appear in the report body or tables, with the same value and the same hedging. Nothing appears only in the summary.
* Frame it against the question: the first line restates the question in one sentence (including an "Update to the question" if there is one). Order the findings by how directly they answer it.
* Say plainly what is not known, what is unadjusted or exploratory, and which limits matter most. Do not overstate: a trend is a trend, a nominal result is nominal.
* No recommendations to the reader and no causal wording the report does not support.

## 4C.3 Technical report content (technical only)

Fixed bold lead-ins, in this order, about 150 words in total:

1. **You asked:** the question, with the groups and sample sizes.
2. **What we found:** the main technical results in plain words, including the largest caveat on them (for example, a technical confound that inflates raw counts) and the most robust result.
3. **How far to trust it:** group size and power, inputs that were not available (batch or injection order, internal standards, blanks), annotation level (library matches are not confirmed identities), and whether the normalization choice mattered.
4. **Next step:** one line (for example, that interpretation is available on request).

No biology, no pathways, no mechanisms and no literature, as in the content boundaries (Section 0B).

## 4C.4 Interpretation report content (biology and literature)

Fixed bold lead-ins, in this order, about 250 words plus the literature bullets:

1. **You asked:** the question, with the groups and sample sizes.
2. **What we found:** the main findings, strongest first, in plain words with the key counts.
3. **How this fits the literature:** one bullet per key finding that the literature bears on. Each bullet carries numbered citations, such as [1] or [2, 3], that point to the Key references box. Each bullet says plainly which of these is true: the literature supports the finding, the literature does not address it, the literature points the other way or is not yet reconciled with it, or no study was found. Say what the cited work did not examine (for example, a different compound, a different comparison or design). Never present a source as saying more than it showed, and keep the claim within what was read: for a source read only as an abstract or summary, say that. If literature searches found nothing relevant, say so in one line, and omit the Key references box.
4. **What it may mean:** the leading interpretation and the alternatives the data cannot separate, hedged as in the report body.
5. **How sure we are:** the main limits in one or two sentences (group size, multiple-testing adjustment, annotation dependence, detection-driven signal, missing covariates).

## 4C.5 Key references box (interpretation only)

* **Where:** bottom of page 1, below the findings table, in both interpretation reports.
* **What:** a numbered list of the sources cited in the summary, in order of first citation (so the first [n] in the box is [1]). Each entry has authors, title or journal, year and **access level** (full text, abstract only, summary only). Typically 3 to 6 entries. The full list stays in the Sources section (Section 10).
* **Rules:** list only sources actually retrieved in this run; never cite from memory without an access level. Every [n] in the summary resolves to an entry; every entry is cited in the summary. Author, year and access level match the Sources list word for word. A tool or method cited only as a tool belongs in the next-tests section, not here, unless the summary relies on it.
* **Fit:** page 1 has to hold the summary, the key callout, the findings table and this box. If it overflows, first move the source block line to page 2 and shorten the tag legend, then tighten the findings table. Shorten the summary only as a last step and never by dropping the literature bullets that disagree with the findings.

---

# 5\. Statistics Notation in Reports

* Always show raw p with q (or the family count) for every feature or family result. Never q alone.  
* State effect-size units on first use (for example "0.61 ln \= 1.8-fold").  
* Label tiers ([INTERPRET.md](INTERPRET.md), Section 6A) in the findings table: Established, Nominal, Family trend, Directional coherence.  
* Show how many families or levels were tested, so the reader sees the multiple-testing context.  
* Give sample sizes (patients and samples) for every comparison.  
* State what "significant" means (the cutoff) on every page that uses the word, in the page footer (Section 4, figure standards).  
* In the full report, show null results in the findings table, marked "Null", with their numbers. In the main report, show only the null results the user asked for.

---

# 6\. Section Pattern for Each Key Finding

Use this order. Keep each part to a few lines.

1. **Heading** (numbered) with the blush-rose accent rule above it.  
2. **KEY BIOLOGICAL IDEA** callout (the interpretation).  
3. One sentence stating what was measured and compared.  
4. **Key data figure** (with number and caption).  
5. **OBSERVED** box: the numbers.  
6. **INFERRED** box: what follows, with the alternatives.  
7. **SPECULATIVE** box: causes and consequences, and the test that would distinguish them.  
8. **Interpretation schematic** (Section 7), unless the finding is a null.  
9. For the full report only: multi-level class analysis, FBMN context, unannotated features, literature, and contradictory evidence, each short and under a small sub-heading.  
10. A one-line **Why it is useful** (marker, question answered, what would decide between explanations).

If a section is a null result, it belongs in the full report (and in the main report only if the user asked for it). Say so in the callout (for example, "Plasma dipeptides do not differ"), show the figure, and keep the section to half a page.

---

# 6A. Molecular-Network Discovery Questions Section (interpretation)

When the user approved the molecular-network discovery questions at intake ([INTERPRET.md](INTERPRET.md), Sections 3A and 5B) and a molecular network was available, every interpretation report (main and full) has a numbered section called **Molecular-network discovery questions**, directly after *At a glance* and before the key-finding sections. It is Section 1; the key findings follow as Sections 2, 3, and so on. It answers the three questions of Section 5B against the QUESTION box on page 1 (Section 4B). If the user declined, or no network was available, omit the section and say so in one line in the version block.

**Layout**

1. Section heading with the accent rule, then a KEY BIOLOGICAL IDEA callout (one to two sentences naming the most important network lead across the three questions).  
2. Three sub-headings, with the questions word for word: "What is most interesting in the molecular network in relation to the question?", "What is most unexpected in the molecular network in relation to the question?", "What is more interesting in the molecular network that is not relevant to the question?".  
3. Under each sub-heading, the items (main report: up to 3 per question; full report: every item). An item is a molecular family, an annotated-to-unannotated link with its delta mass, a compound class, or a set of connected nodes. Each item has a bold one-line title naming the family or component ID and its annotated members (full feature names), its tag (OBSERVED, INFERRED or SPECULATIVE), one line of evidence (family size, members moving the same way, raw p, q, n), a small network or class-colored figure where it helps, and a pointer ("see Figure N" or "see Section N") to where it is developed. An item that has its own key-finding section is not repeated here.  
4. For the second question add an **Expectation** line (what was expected and why) and a **Checked** line (the technical explanations ruled out). For the third add a **Why it is outside the prompt** line.  
5. If a question has no answer, write one line saying so and what was checked.  
6. Check that every figure and section pointer resolves (Section 12).

The technical report does not have this section.

---

# 6B. Emerging-Patterns Summary Section (interpretation)

Both interpretation reports carry the result of the Phase 1 scan ([INTERPRET.md](INTERPRET.md), Section 5A) in a numbered section called **Emerging patterns evaluated**, placed after the Molecular-network discovery questions section (Section 6A) when present, otherwise directly after *At a glance*, and before the key-finding sections. It contains:

1. The total number of patterns evaluated and the counts by evidence tier and by tag (Observed, Inferred, Speculative). No pattern is left out because of how many there are.
2. The summary table of all patterns, as in the chat summary: ID, pattern, key features or family, evidence tier, one-line meaning, verdict. In the main report the table may be abbreviated to the patterns the user chose to pursue plus a count of the rest, with the full table in the full report.
3. The one or two summary figures from the scan, each with a graphical key, number, caption and "How to read this figure" line (Section 4).
4. A pointer from each pattern ID to the key-finding section that develops it, or a statement that it was evaluated and not pursued, with the reason.

Pattern IDs stay the same from the chat summary through both reports.

---

# 7\. Interpretation Schematics

Every key finding gets a schematic of the biological interpretation.

**Style**

* A left-to-right chain of rounded boxes joined by arrows: **observation → candidate state → possible route to the phenotype**.  
* **Solid boxes** for observed results, **dashed boxes** for interpretation or hypothesis. State this in the caption ("Dashed boxes: interpretation, not tested here").  
* Box text: a short bold title and one grey line of detail (a statistic, a mechanism, or a citation).  
* A separate bottom row or side box for the intervention or perturbation (for example how the diet may act) and for what happens when it is removed (for example rebound).  
* A small label above the chain: "What it may mean (speculative)" or "Overall: observed, candidate state, route to the outcome".  
* Use the tier colors from Section 4 for box fills and borders.

**Content rules**

* Include the possible causes and the possible consequences, not only the favored route.  
* Show the main alternative explanation as a branch or a second chain if it is plausible.  
* No box states a mechanism as fact. Every dashed box is a hypothesis.  
* Cite sources in the box detail line (author, year) when a step relies on literature.

**Overview schematic**

* In the "What this means" section, include one overview schematic joining all key findings: observed in the groups → candidate states → possible routes to the outcome.  
* Number it as a figure.

**Making them**

* Draw as vector graphics (SVG or equivalent) and export an image for the PDF. Keep the source so a later draft can edit the text.

---

# 8\. Interpretation Position Rules

* QUESTION box at the top of page 1, under the title and byline (Section 4B).  
* Overall interpretation box on page 1, in **At a glance**.  
* **Molecular-network discovery questions** section directly after *At a glance* (Section 6A, when approved and a network exists), before the key-finding sections.  
* A KEY BIOLOGICAL IDEA callout directly under every section heading, in both reports.  
* The interpretation of a figure is in the text next to it, not several pages later.  
* The "What this means" section near the end synthesizes. It does not introduce new interpretation for the first time.  
* No section ends with unexplained numbers or tables. Close each section with its INFERRED or SPECULATIVE box.

---

# 9\. Brevity

* Short sentences. Plain words. Define a term once, in the Terms box, and use it consistently.  
* One idea per paragraph, three to five lines.  
* No paragraph restates the callout above it.  
* Do not repeat the same statistic in the callout, the table, the figure and the text more than twice.  
* Use a table only to compare items across the same attributes. Use a bullet list only for parallel items.  
* Hard limits for the main report: callouts one to two sentences; each OBSERVED box at most five bullets; each SPECULATIVE box at most four bullets. There is no cap on the number of figures per finding, but every figure must carry a result (no decoration).  
* Move secondary detail to the full report and point to it.  
* Do not pad. If a section has nothing to say beyond a null, keep it short.

---

# 10\. Sources and Access

* **Sources** list on the last page: authors, journal, year, and the access level used (full text, abstract only, news summary).  
* Mark any source read only as an abstract or summary, and say that the full paper was not accessed. If the full text would change a claim, flag it and ask the user to upload the PDF.  
* Mark background statements that are not taken from a cited source as "general background".  
* Every source in the page-1 Key references box (Section 4C.5) appears here with the same access level, and every numbered citation in the plain-language summary resolves.  
* Do not cite a paper for a claim it does not make. Observation in a paper is not mechanism.  
* Include repository accessions and search dates where repository evidence is used.

---

# 11\. Additional Items Worth Including

These were not in the request but make the reports more useful and less error-prone.

1. **Source block, and a "What changed" line where the report supersedes an earlier one** (Section 2), so readers know which numbers are current.  
2. **Limits box** in every report, listing sample size, missing diet and medication records, unadjusted covariates, annotation confidence, and exploratory status.  
3. **Next tests box** at the end of the main report: the three to five most informative next analyses or measurements, each with the result that would support or reject the hypothesis. Include DrugReadout and FoodReadout when intake data are missing ([INTERPRET.md](INTERPRET.md), Section 13A). Repeat each pattern's "Ways to dig further" menu here. Where a next test is one of the follow-up tools of Section 13C (MASST family, MassQL, Conjugated Metabolome Explorer), give its link, the exact input block or MassQL query, and the result that would support or reject the hypothesis; list only tools the user approved or that are marked as proposed.  
4. **Testable predictions** stated in the form "If X is true, then Y should be seen in Z."  
5. **Annotation confidence labels** wherever a molecule name appears (for example library match, mass-difference candidate, formula only), so a reader never mistakes a candidate for an identification.  
6. **Multi-level class panel** (broad class versus sub-class) wherever the sub-class result changes the interpretation ([INTERPRET.md](INTERPRET.md), Section 7A).  
7. **Null results** shown in the full report, not hidden; in the main report only if requested.  
8. **Source data and code** for every figure, published with it, so a figure can be regenerated.  
9. **Figure alt text** (one line per figure) for accessibility and for the file index.  
10. **Glossary** in the Terms box, written for a general scientific audience, defined once.  
11. **Group-size table** on page 2, with the definition of the key comparison, so the reader always knows who is being compared.  
12. **Cross-references**: "see Figure N", "see full report, Section N", resolved and checked.  
13. **Colorblind-checked palette**, chosen by the user, constant across chat figures, main report and full report.  
14. **A "What changed" line** in the summary of any report that supersedes an earlier one.  
15. **Reproducibility note** (full report appendix): software versions, task IDs, parameters, random seeds for permutation tests.

---

# 12\. Pre-Delivery Checklist (interpretation reports)

For the technical report use the checks at the end of Section 0B. Before showing both interpretation drafts for approval, and again on the built files:

- [ ] Both report files built from the one accepted report; an earlier report's files left in place  
- [ ] Page numbers "X of Y" present on every page; figure, table and section numbers sequential  
- [ ] Every figure cited in the text; every cited figure exists  
- [ ] Every figure has its 1 to 2 sentence "How to read this figure" line (Section 4, Figures)  
- [ ] Emerging-patterns summary section present (Section 6B) with the total number of patterns evaluated, the summary table covering every pattern, and one or two summary figures; numbers agree with the chat summary  
- [ ] Every section has a KEY BIOLOGICAL IDEA callout directly under its heading  
- [ ] QUESTION box at the top of page 1, matching the goal word for word (Section 4B)  
- [ ] Plain-language summary directly under the QUESTION box (Section 4C) in both reports, with the five lead-ins; it replaces the old abstract paragraph; every number and claim matches the report body  
- [ ] Literature bullets in the summary carry numbered citations; every [n] resolves to the Key references box on page 1; every box entry is cited and matches the Sources list (authors, year, access level); abstract-only and summary-only sources are labelled as such; findings the literature does not support or contradicts are stated, not omitted  
- [ ] Molecular-network discovery questions section present after *At a glance* with the three questions worded as in Section 6A and every pointer resolving, or its omission (declined, or no network) stated in the source block
- [ ] Overall interpretation present on page 1  
- [ ] Every key finding has its data figure(s) and an interpretation schematic (nulls excepted)  
- [ ] Intake answers (format, length, nulls in main report, colors) applied and logged  
- [ ] Every claim tagged Observed, Inferred or Speculative  
- [ ] Raw p shown with q (or family count) for every result; n shown for every comparison  
- [ ] Numbers identical between the main report and the full report  
- [ ] Numbers in the text match the figures and tables  
- [ ] Limits box present; contradictory evidence shown  
- [ ] Sources list complete, with access level; abstract-only sources flagged  
- [ ] Group colors are the ones the user chose, consistent across all figures  
- [ ] Main report contains no null results except those the user requested  
- [ ] Main report within the length the user chose; no section repeats another  
- [ ] Everything the report links to is ready to publish: figures with their source data, tables, findings, the question and code  
- [ ] Diet and medication gaps addressed ([INTERPRET.md](INTERPRET.md), Section 13A)