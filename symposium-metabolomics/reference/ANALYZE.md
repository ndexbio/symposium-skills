# Analytical Decision Framework

You arrive here with the task's files fetched ([GNPS2-FILES.md](GNPS2-FILES.md)), the question, and
the reuse table approved where the library already held work on this task. You leave with every
stage worked in the run's folder, its decisions recorded, and a draft technical report
([REPORT.md](REPORT.md)). Nothing is published until the user approves that draft.

Each stage below ends in what it publishes: an Analysis whose `procedure` states what Section 14
lists for that stage, and the tables it produced as that Analysis's outputs. A stage the reuse
table marks as reused is not run again; its outputs are taken as inputs by address.

This document stays technical and statistical. Biological meaning belongs to
[INTERPRET.md](INTERPRET.md).

## Purpose

This document defines the analytical decision-making framework for preprocessing and first-pass statistical analysis.

The framework is designed to support flexible, dataset-specific analysis rather than enforce a single universal metabolomics workflow.

The skill should:

1. Inspect the available data and experimental design.  
2. Identify analytical decisions that materially affect interpretation.  
3. Explain relevant options and tradeoffs to the user.  
4. Recommend approaches based on the observed dataset and study design.  
5. Allow the user to select or override recommendations.  
6. Execute the selected analysis.  
7. Record the decision, rationale, parameters, and resulting changes.  
8. Assess the sensitivity of important findings to major analytical decisions when appropriate.  
9. Review the features removed during filtering and flag any that may have been removed incorrectly.  
10. Draft the technical report (Section 16).  
11. Write a hand-off note with open items, recommended technical next steps, and areas of potential interest for follow-up (Section 17).  
12. Process the unfiltered feature table with the same transformations, normalizations, and analyses as the final filtered table, and publish it beside the filtered one (Section 13A).
13. Report the detection-rate bins with MS/MS and library match rates, for every run (Section 13B), as tables of its own and a figure in the technical report.
14. When a molecular network is available, run the molecular-network analysis by default (Section 13C): network summary, delta-mass inventory, compound classes with a fixed color key, and the volcano plot by class, each as tables of its own with figures in the technical report.
15. Ask which internal standards were used (skip if the user does not know) and check them in the feature table (Section 3.8).
16. Recommend merges for features that an aligner may have split, show the evidence, and apply only the merges the user approves (Section 3.9).
17. Check whether batch and drift correction is needed and, when it is, correct with QCRSC (cited), validate on held-out QCs, and correct the unfiltered table in the same run (Section 3.10).

The skill must distinguish between:

* **Analytical recommendations:** what the skill suggests.  
* **User decisions:** what the user selects or overrides.  
* **Analytical execution:** what was actually performed.  
* **Analytical validation:** whether the requested operation was successfully and appropriately executed.

The skill should never silently substitute one analytical method for another.

---

# 1\. General Decision Framework

For every major analytical decision, follow this sequence:

### 1.1 Detect

Determine whether the analytical issue is relevant to the dataset.

### 1.2 Assess

Inspect the available data and experimental design to characterize the issue.

### 1.3 Recommend

Present appropriate options to the user, including a preferred option when the available information supports one.

### 1.4 Explain

Briefly explain:

* Why the decision matters.  
* What assumptions each option makes.  
* What effect the choice may have on downstream interpretation.

Do not overwhelm the user with methodological alternatives that are irrelevant to the dataset.

### 1.5 Select

Allow the user to select, modify, or reject the recommendation.

**Required chat format.** Whenever decisions are presented in the chat, use two parts in this order:

1. **Breakdown:** what the data show, the patterns observed, why each decision matters, the options, and the recommendation for each.  
2. **Things I need from you:** a closing list that restates, in one place, every recommendation to approve (with the recommended default and the main alternative) and every question that must be answered before execution.

The closing list is in addition to the breakdown, never a replacement for it. Do not proceed to execution until the items in the list have been answered or approved.

### 1.6 Execute

Perform the selected operation using executable code or an appropriate analytical tool.

### 1.7 Validate

Verify that the operation was performed as specified and that the resulting data are internally consistent.

### 1.8 Record

Record:

* Method  
* Parameters  
* Rationale  
* Input dimensions  
* Output dimensions  
* Features/samples removed  
* Relevant warnings  
* Software/code used

---

# 2\. Dataset and Experimental Design Assessment

Before recommending preprocessing or statistical methods, inspect the dataset.

## 2.1 Identify available inputs

Determine whether the user has provided:

* Feature abundance table  
* Sample metadata  
* Feature metadata  
* Blank samples  
* Pooled QC samples  
* Technical replicates  
* Internal standards (ask the user which were used; Section 3.8)  
* Retention times  
* MS/MS spectra  
* FBMN output  
* Library annotations  
* SIRIUS or other annotation results  
* Batch information  
* Injection order  
* Experimental groups  
* Repeated-measure identifiers

If important information is unavailable, identify the limitation before proceeding.

## 2.2 Determine data representation

Determine, when possible:

* Raw versus processed feature abundances  
* Peak areas versus intensities  
* Whether values have already been normalized  
* Whether values have already been transformed  
* Whether missing values and zeros are distinguished  
* Whether features represent chromatographic peaks, molecular formulas, library annotations, or other entities

Do not apply preprocessing steps that duplicate transformations already performed upstream unless explicitly requested.

If the preprocessing history is unknown, flag this uncertainty.

**Ask about normalization upfront.** At intake, ask whether the feature table is raw (peak areas or intensities with no normalization applied) or has already been normalized. The normalization comparison (Section 7.4.1) needs a raw table. If the table has already been normalized, say so in one line, tell the user that the comparison is not applicable to it, and ask them to upload a raw feature table (Section 7.4.2). Ask once; do not re-ask in later stages. If the user cannot say, flag the preprocessing history as unknown and treat the table as possibly normalized (Section 7.4.2).

## 2.3 Determine experimental structure

Identify:

* Primary comparison  
* Number of groups  
* Sample sizes  
* Independent versus paired samples  
* Repeated measurements  
* Technical versus biological replicates  
* Batch structure  
* Relevant covariates

The experimental design should determine the downstream statistical framework.

Do not assume that samples are independent simply because each sample appears as a separate row in a feature table.

---

# 3\. Quality Control Assessment

## Objective

Assess whether the analytical dataset is sufficiently reliable for downstream interpretation and identify technical sources of variation that may require attention.

## 3.1 Determine available QC information

Identify whether the dataset contains:

* Procedural blanks  
* Solvent blanks  
* Extraction blanks  
* Pooled QC samples  
* Technical replicates  
* Internal standards (ask the user; Section 3.8)  
* Injection order (from the sequence files if it is not in the metadata; Section 3.10.1)  
* Batch identifiers (same)

If no QC information is available, report this explicitly.

Absence of QC data should not automatically prevent analysis, but should reduce confidence in conclusions about technical robustness.

## 3.2 Inspect pooled QC samples

When pooled QCs are available, assess:

* Number of pooled QC injections  
* Feature detection across QCs  
* Feature-level variability  
* Overall QC signal distribution  
* Drift across injection order  
* Batch differences  
* Outlying QC injections  
* Number of features with excessive variability

For feature-level reproducibility, calculate an appropriate variability metric such as coefficient of variation (CV/RSD):

$$
CV = \frac{SD(\text{QC abundance})}{Mean(\text{QC abundance})} \times 100
$$

&nbsp;

The data used for this calculation must be explicitly identified.

For example, distinguish between:

* **Pre-correction QC variability:** assesses analytical reproducibility before normalization or batch correction.  
* **Post-correction QC variability:** assesses whether a correction procedure improved technical reproducibility.

Do not describe these as equivalent measurements.

Do not calculate CV for features with insufficient usable QC observations or effectively zero mean signal without first addressing the resulting instability.

## 3.3 Assess QC variability in context

Before applying a QC-based feature filter, inspect the distribution of QC variability.

At minimum, summarize:

* Median CV  
* Relevant quantiles  
* Proportion of features below candidate thresholds  
* Proportion of features above candidate thresholds  
* Relationship between QC CV and feature abundance

If high CV is concentrated among low-abundance features, determine whether this is consistent with measurements approaching the detection limit before interpreting high CV as evidence of poor analytical performance.

The skill should not assume that every high-CV feature is an artifact.

## 3.4 QC-based feature filtering

When pooled QCs are available and the user wishes to filter features based on analytical reproducibility:

### Step 1: Establish the filtering target

Determine whether the goal is to remove features with poor analytical reproducibility based on:

* QC CV/RSD  
* Detection frequency in QCs  
* Another explicitly specified QC metric

The metric must be defined before filtering.

### Step 2: Establish the data state

Record whether QC variability is being assessed on:

* Raw/pre-normalization abundances  
* Normalized abundances  
* Transformed abundances  
* Post-batch-correction abundances

If batch correction was run (Section 3.10), assess QC variability on the **held-out** QC values, not on the QCs the correction was fitted to, and log the data state as `post-batch-correction, held-out QCs`. QC variability measured on the fitted QCs after a flexible correction is not a reproducibility measure.

The choice should correspond to the analytical question being asked.

### Step 3: Inspect candidate thresholds

If the user has specified a threshold, use it.

If no threshold has been specified:

1. Show the observed QC variability distribution.  
2. Report retention/removal at several reasonable candidate thresholds.  
3. Consider the number of pooled QCs, platform, study design, abundance distribution, and intended downstream analysis.  
4. Recommend a starting threshold if the available evidence supports one.  
5. Explain the tradeoff between removing poorly reproducible features and retaining potentially informative low-abundance features.  
6. Ask the user to confirm the threshold before execution.

Candidate thresholds such as 20%, 30%, or 40% may be evaluated as sensitivity points, but they must not be treated as universal standards.

### Step 4: Execute the filter

For the selected threshold:

* Calculate the QC variability metric for each eligible feature.  
* Remove features exceeding the threshold.  
* Report the number and percentage of features removed.  
* Preserve the complete pre-filter feature list.  
* Preserve the QC metric for every feature.  
* Record the exact threshold and calculation method.

### Step 5: Evaluate consequences

After filtering, assess whether removed features are disproportionately associated with:

* Low abundance  
* Specific molecular families  
* Particular annotation classes  
* Particular sample groups  
* Specific batches

When annotation information is available, flag substantial chemical or biological enrichment among removed features.

### Step 6: Perform sensitivity analysis when warranted

If QC filtering substantially changes the number or identity of significant findings, compare results using reasonable alternative thresholds.

A finding that appears only under one aggressive QC threshold should be flagged as **QC-filter-sensitive**.

A finding that persists across reasonable thresholds may be described as **QC-filter-robust**, provided the comparison was appropriately performed.

### Required output

The QC filtering report should contain:

* Number of pooled QCs  
* QC metric used  
* Data state used for calculation  
* Distribution of QC variability  
* Selected threshold  
* Candidate thresholds considered, when applicable  
* Number of features before filtering  
* Number removed  
* Number retained  
* Relationship between QC variability and abundance  
* Batch/drift concerns  
* Chemical or biological patterns among removed features  
* Sensitivity of significant findings, when assessed

## 3.5 Identify analytical drift

When injection order is available, assess whether feature abundances change systematically with run order.

Distinguish:

* Global drift  
* Feature-specific drift  
* Batch-specific shifts  
* Random technical variability

If drift is substantial, recommend an appropriate correction strategy when one is available.

Do not automatically remove features solely because they exhibit drift. First determine whether the drift is technical and whether correction is appropriate.

If correction is applied, evaluate whether QC behavior improves after correction. Section 3.10 sets out how: it checks first whether correction is needed, applies QCRSC when it is, and judges the result on held-out QCs.

## 3.6 Identify problematic QC injections

Inspect pooled QC samples for evidence of individual injections that behave anomalously.

Potential evidence includes:

* Strong separation in PCA or another multivariate representation  
* Unusually low or high total signal  
* Broad deviation across features  
* Abnormal internal-standard behavior

Do not remove a QC injection solely because it is visually separated.

Before excluding a QC, identify the evidence supporting exclusion and record the decision.

## 3.7 QC conclusions

Classify QC status using descriptive categories such as:

* Good  
* Acceptable with limitations  
* Concerning  
* Insufficient information

The classification must be accompanied by quantitative evidence.

Do not use QC status as a substitute for quantitative reporting.

**This step is mandatory.** Always report the QC classification (reproducibility, and drift/batch) with its quantitative evidence, even when QC information is limited or absent. In that case classify as "Insufficient information" and state what is missing. Report it before proceeding to downstream decisions, record it in the decision record, and include it in the final report. Do not skip this step.

## 3.8 Internal standards

> Companion sections: the standards also feed normalization (Sections 7.2 and 7.3) and the feature-merge recommendation (Section 3.9). Report layout: [REPORT.md](REPORT.md), Section 0B.

### 3.8.1 Ask the user

In the first decision breakdown, ask once: **"Which internal standards were used?"** For each standard, ask for the name, the expected m/z (or formula and adduct), the expected retention time if known, and where it was added (before extraction or before injection, and to which samples). Accept a list or a file.

* If the user does not know, or no standards were used, **skip Sections 3.8.2 to 3.8.6**, record `not provided` in the decision record, say in the QC classification (Section 3.7) that internal-standard evidence is missing, and do not ask again.  
* Never infer which features are standards from names or patterns in the feature table (for example labeled or deuterated names), and never assume a standard is present.

### 3.8.2 Find the standards in the feature table

For each standard, list every M+0 feature whose m/z is within the ppm tolerance of Section 3.9.1 of the expected m/z (also check the expected adducts) and whose RT is within 0.2 min of the expected RT (or, if no RT was given, within 0.2 min of the most abundant match). Keep all matching rows; do not choose one yet.

### 3.8.3 Checks (per standard)

* **Rows found:** one row (intact), more than one row (**split**), or none (**missing**; state the expected m/z and adducts searched).  
* **Detection:** number of samples with a detected peak, by sample type (study samples, pooled QCs, blanks).  
* **RT behavior:** RT of the standard across injection order, its range, and any trend or batch step (an RT drift is a common reason for a split).  
* **Area behavior:** peak area across injection order, and the CV in the pooled QCs and in the study samples.  
* **If split:** make a mirror plot of the rows' MS/MS (if available), an extracted-ion chromatogram overlay in samples where each row was detected, and a table showing which samples fall into which row (the review-sheet layout of Section 3.9.4).

### 3.8.4 What a split means

A split standard shows that the aligner divides one compound into several rows in that part of the run, for example because of RT drift or a small m/z shift. Treat this as **supporting context**: raise the priority of the feature-merge recommendation (Section 3.9), and report the RT range where the split happened. Each candidate pair is still judged by its own evidence. An intact standard does not show that other regions are free of splits, because one standard covers one m/z and RT region.

### 3.8.5 Use for normalization

The standards inform, but do not choose, the normalization (Sections 7.2 and 7.3). If a standard is split, the user decides whether to merge its rows (Section 3.9) **before** normalization factors are computed; compute factors from the merged standard signal and say so. Which standard normalizes which features (one standard, the nearest-RT standard, or the mean of several) is a user decision recorded in the log. Batch correction (Section 3.10) is applied after the merge and before the normalization factors are computed.

### 3.8.6 What this stage publishes

* **The internal-standard check**, a table: one row per standard and matched feature (standard name, expected m/z and RT, feature ID, m/z, RT, detected samples, RT range, area CV in pooled QCs, status: intact, split or missing).  
* One figure in the technical report: RT and area of each standard across injection order, rows of a split standard in different colors, with a graphical legend.  
* What the stage's procedure states: block `internal_standards` (Section 14).

## 3.9 Feature-merge recommendation (alignment splits)

> Companion sections: [GNPS2-FILES.md](GNPS2-FILES.md) ("Files the analysis needs for Sections 3.8 and 3.9"), Section 3.8 (internal standards), Section 4 onward (filters run after any approved merge), Section 13A (the unfiltered table gets the same merge), [REPORT.md](REPORT.md), Section 0B.

### Objective

Aligners sometimes divide one compound into several feature rows. A split lowers each row's prevalence, inflates the feature count and spreads one signal over several tests. This step **finds candidate pairs, shows the evidence, and recommends** which to merge. It never merges anything without the user's approval. It is **on by default as a recommendation** and runs before the blank and prevalence filters (Sections 4 and 5), because merging changes blank ratios, prevalence and QC CVs.

Sample co-detection (how many samples two features share) is deliberately **not** used as a rule: in a test on one dataset it was only weakly related to spectral similarity and was uninformative when detection counts were low. The evidence is the spectrum, the chromatogram and the library annotation.

### 3.9.1 Candidate pairs

* **Scope:** M+0 features only. Isotope, adduct and in-source-fragment rows are different relationships and are not merged by this step.  
* **m/z window:** default 5 ppm for Orbitrap-class data. Adjust to the observed mass error (for example from the internal standards in Section 3.8 or from annotated features) and state the value.  
* **RT window:** default 0.1 min.  
* **Sensitivity of the count:** report the number of pairs and of features involved at several windows (for example 2, 5 and 10 ppm by 0.05, 0.1 and 0.2 min) so the user sees how fast the count rises. The count usually rises steeply with the RT window.  
* **Groups:** merge groups are bounded. Every member must be within both windows of the group's most abundant feature. Do not chain (A near B and B near C does not put A and C together).

### 3.9.2 Evidence for each pair

1. **MS/MS mirror plot and cosine** (consensus spectra; cosine on peaks above 1% of the base peak, fragment tolerance 0.02 Da, precursor region removed). Default: cosine 0.7 or higher supports "same compound". Flag spectra with fewer than 5 peaks or near-equal peak intensities as **noise-like**: their cosine is not informative and does not veto a merge.  
2. **Extracted-ion chromatogram overlay** of the pair m/z. Use a sample where both features are detected (not gap-filled) if one exists; otherwise show each feature in a sample where it was detected. A **single peak whose apex shifts between injections** points to an alignment split. **Two partly resolved peaks in one injection**, with a dip between the apexes, point to two compounds (for example isomers): do not merge.  
3. **Library annotation of both rows** (name, library, cosine; from the library search table). The same name supports a merge. **Different names** mean do not merge. One or no annotation is noted.  
4. **Internal-standard context** (Section 3.8), if a standard in that RT region was split.

### 3.9.3 Classification

| Class | Rule |
| :---- | :---- |
| **Recommend merge** | MS/MS on both rows, cosine 0.7 or higher, XIC consistent with one shifting peak, and no conflicting library names |
| **Review** | Any evidence missing or conflicting: no MS/MS on one or both rows, cosine below 0.7, noise-like spectra, only one annotated, or an XIC that cannot be read |
| **Do not merge** | Two resolved peaks in one injection, different library names, or dissimilar spectra (cosine below 0.3) that are not noise-like |

Pairs without MS/MS on both rows are listed under **Review** and are never recommended on m/z and RT alone.

### 3.9.4 Present and ask

Before any merge, show: the candidate-count table (Section 3.9.1), the number of pairs per class, and **review sheets** for every recommended pair and for a sample of Review pairs (at least 10, or all if fewer; offer more). A review sheet has, for one pair: the mirror plot, the XIC overlay, the library annotation names, the m/z and ppm difference, the RT difference and the detection counts. Ask the user to approve all recommended merges, some of them, or none, and whether any Review pairs should be merged. Record the answer.

### 3.9.5 Applying approved merges

* Apply before the filters of Sections 4 and 5, and recompute QC CVs and blank ratios afterwards.  
* **Area per sample:** the larger of the two rows' areas (this avoids double counting gap-filled values; when only one row has a value, it is that value). If the user prefers the sum, record it.  
* **Representative row:** the row with more detected samples. It keeps its ID, MS/MS spectrum and annotation. Keep every original ID in the mapping table.  
* Apply the same merge to the unfiltered table (Section 13A).  
* The molecular network and library results (Sections 13B and 13C) stay on the original IDs and use the mapping table. Do not re-run the network.  
* The detection-rate table (Section 13B) states whether it was counted before or after the merge and the number of features in each case.

### 3.9.6 Sensitivity and validation

* Compare the key results with and without the approved merges (features whose effect size, raw p or q changed materially).  
* Report the number of merge groups and the group-size distribution.  
* Validate: features after the merge equal features before minus merged members; every merged ID appears once in the mapping table; areas of non-merged features are unchanged; the unfiltered table received the same merge.

### 3.9.7 What this stage publishes

* **The merge candidates**, a table: one row per candidate pair (IDs, m/z, ppm difference, RTs, RT difference, cosine, matched peaks, noise-like flags, library names, XIC call, class, user decision).  
* **The merge map**, a table: approved merges only (original ID, representative ID, group ID). Published even when it is empty, so a reader sees that none was applied.  
* **The review sheets**, as a file held beside the candidates table.  
* In the technical report: the candidate-count table, the class counts, and example review sheets as figures.  
* What the stage's procedure states: block `feature_merge` (Section 14).

## 3.10 Batch and drift correction (QCRSC)

> Companion sections: Sections 3.2, 3.5 and 3.6 (QC inspection, drift, problem QC injections), Sections 3.8 and 3.9 (standards and merges come first), Section 3.4 (the QC filter uses the corrected data), Sections 4, 5 and 7 (filters and normalization run after correction), Section 13A (the unfiltered table is corrected in the same run). Code: [`scripts/qcrsc.py`](../scripts/qcrsc.py). Example figures: `examples/batch_correction_example_fig*.png`, beside this document. Report layout: [REPORT.md](REPORT.md), Section 0B.

### Objective

Instrument signal changes between batches and drifts within a batch. This step **checks whether that matters for this dataset, and corrects it only when it does**. It removes no features. It is **check-first**: the check runs on every dataset that has pooled QCs, injection order and batch labels, and the correction runs only when the check recommends it or the user asks for it.

**Method (state this in the first decision breakdown and in the report).** The correction is **QCRSC** (QC-based robust spline signal correction; also called QC-RLSC). For every feature and every batch, a smoothing spline is fitted to the pooled-QC signal against injection order (log scale, smoothing chosen by 5-fold cross-validation). Every injection is multiplied by the QC median divided by the fitted trend, and the batches are then aligned on their QC medians. Study samples and blanks never enter a fit. Cite:

* Dunn WB et al. (2011) Nat Protoc 6:1060-1083, doi:10.1038/nprot.2011.335 (QC-based signal correction for large LC-MS studies).  
* Broadhurst D et al. (2018) Metabolomics 14:72, doi:10.1007/s11306-018-1367-3 (guidelines for QC-based correction and data cleaning).  
* Broadhurst DI. QC:MXP v3.2 (2025), doi:10.5281/zenodo.11101541 (the reference implementation, a Matlab desktop application).

The skillset's code is a Python implementation of the same approach, `scripts/qcrsc.py`. **It is not QC:MXP.** On one dataset (301 features, GNPS2 Everything Bagel task 9b80f45b, six batches, 172 pooled QCs) its corrected study-sample values agreed with QC:MXP (median Spearman 0.996 across features; QC:MXP run with the settings matched: spline, 5-fold cross-validation, no outlier removal, no prefilter), and its in-sample QC %RSD agreed with QC:MXP's (median 9.8% against 10.1%). Say "validated against QC:MXP on one dataset", never "equivalent to QC:MXP".

### 3.10.1 Inputs

* **Pooled QCs, injection order and batch are required.** Injection order and batch are usually not in the feature table or the metadata. Ask the user for the instrument sequence files (or any file with run order and batch); if there are none, report `batch correction not possible: no injection order or batch information`, record it in the decision record and in the QC classification (Section 3.7), and stop this step.  
* **Injection table:** one row per injection with `SampleID` (the column name in the feature table), `SampleType` (QC, Blank or Sample), `Order` (numeric, increasing over the whole run) and `Batch`. This is also the QC:MXP data-table format, so a QC:MXP input file can be used as it is. Optional group column (for example site) for the group-by-batch table.  
* **Batch** means a period over which instrument conditions were held. Use the sequence file or plate set when the user confirms it; ask when unclear (column change, cleaning, recalibration, or a long pause). State the definition used.  
* **QC injections:** use all pooled QCs unless Section 3.6 excluded some. Make those exclusions **before** this step and apply them to every table. Do not drop lead-in or lead-out QCs unless Section 3.6 says so.  
* **Already corrected input.** The user may supply a QC:MXP output or any other batch-corrected table instead. Ask which tool, version and settings produced it (a QC:MXP configuration `.json` is ideal). Do not correct it again. Run the check on it, and record the source in the decision record. Read the result with care: QC-based correction fits the QCs themselves, so QC-based diagnostics of a corrected table are near zero by construction and cannot show that the correction was good. Judge by the study samples instead: PCA coloured by batch, the share of each feature's sample variance explained by batch (Fig. 3 style), and the group-by-batch table. If the raw table is also available, compare the two on the same plots.

### 3.10.2 Order of operations

1. Internal-standard check (Section 3.8) and approved feature merges (Section 3.9).  
2. QC-injection decisions (Section 3.6), applied to every table.  
3. **Check** (Section 3.10.3). Decide whether to correct.  
4. **Correct once, on the full unfiltered table** (Section 3.10.5). The filtered table takes its values from that result; nothing is corrected twice. Per-feature correction does not depend on which other features are present, so correcting first and filtering later gives the same values as the reverse.  
5. QC-based feature filter (Section 3.4), using the held-out QC %RSD.  
6. Blank filter (Section 4), prevalence filter (Section 5), then missing values, normalization and the rest (Sections 6 onward) on the corrected values.

### 3.10.3 Step 1: Check

Run `python scripts/qcrsc.py check --quant <quant.csv> --injections <injections.csv> --out <dir> --prefix batch_correction [--group-col Site]`. It changes no values. First run `python scripts/qcrsc.py selftest`; if it fails, stop and report that (Section 3.10.8).

**Eligible features.** A feature is eligible when it is detected (value above zero) in at least 80% of pooled QCs and in at least 10 pooled QCs. Eligibility is about whether a QC-based statement is possible, not about the feature's biology. Report the number of eligible features and how many of all input features that is. In sparse datasets most features are ineligible; say so.

**Per eligible feature, on the pooled QCs:**

| Measure | Definition |
| :---- | :---- |
| Batch effect (R², q) | One-way ANOVA of log10 QC signal by batch; R² is the share of QC variance explained by batch; q is Benjamini-Hochberg across eligible features |
| **Affected** | q below 0.05 **and** R² of at least 0.14 |
| Shift size | Fold range of the batch QC medians (largest over smallest) |
| Within-batch drift | Spearman rho of QC signal against injection order inside each batch (batches with at least 8 positive QCs); flagged when |rho| is at least 0.3 with p below 0.05 in any batch |

**Dataset decision (share of eligible features that are affected):**

| Share affected | Decision |
| :---- | :---- |
| 10% or more | **Recommend correction** and run it unless the user declines |
| 2% to under 10% | Show the diagnostics and **ask** |
| Under 2% | **Skip**; record the evidence and the decision in the log |
| Fewer than 20 eligible features | Ask; too few to judge |
| One batch only | The decision uses the drift flag alone and is labelled exploratory |

The user may override either way (record it). If the user asks for correction when the check says skip, warn that correcting data without a batch effect adds noise: in the script's own no-effect self-test, correction raised the held-out QC %RSD.

### 3.10.4 Thresholds and where they come from

All thresholds are first defaults, calibrated on **one** dataset (the 301-feature pilot named above). State this wherever they are used, and change them only with a stated reason that goes into the log.

| Threshold | Value | Evidence on the calibration dataset |
| :---- | :---- | :---- |
| Affected feature | q < 0.05 and R² ≥ 0.14 | 76% of eligible features before correction, 0% after (held-out QCs). Shuffling the batch labels gave about 0% (largest 0.7%). Significance alone flagged about 6% on average and up to 27% in one shuffle, because features are not independent; the R² condition is what controls false alarms. The shuffles break the time order inside batches, so they are a test of the batch test, not of drift |
| Dataset trigger | 10% recommend, 2% ask | Set well above the shuffle result and well below the observed 76% |
| Shift size | fold range ≥ 1.2 | Correction lowered the QC %RSD of 84% of features with a 1.2 to 1.5-fold range and of 91% with 1.5-fold or more, but of only 21% below 1.1-fold. Reported, not used as a gate |
| Drift | \|rho\| ≥ 0.3 and p < 0.05 in any batch | 91% of eligible features flagged before correction, 0% after. Exploratory; reported, not used as a gate |
| Eligibility | ≥ 80% of QCs and ≥ 10 positive QCs | The calibration run applied only the 10-positive-QC condition (301 of 303 features); the 80% condition was not tested there. Within a batch, 5 to 9 positive QCs use a straight line and fewer than 5 leave that batch uncorrected |
| Correction worked | held-out affected features under 5% and median held-out QC %RSD at or below 20% | Calibration dataset: 0% and 14.3% (from 21.2% uncorrected) |

### 3.10.5 Step 2: Correct

Run `python scripts/qcrsc.py correct` with the same arguments (add `--workers N` for many features; the run time grows with the number of eligible features). Rules:

* **Correct once, on the full unfiltered table** (all input features, after the merges of Section 3.9 and the QC-injection decisions of Section 3.6). The filtered table is derived from the corrected result. Check that every retained feature's values equal its row in the corrected unfiltered table (Section 3.10.8).  
* **Nothing is removed.** Features that cannot be corrected stay in both tables with their raw values and a `batch_corrected` column: `yes`, `partial` (at least one batch had fewer than 5 positive QCs and was left uncorrected) or `no`, with a reason (`fewer_than_10_positive_QCs`, `qc_detection_below_80%`). Carry `batch_corrected` and its reason into the per-feature results, the filter table and the unfiltered results, so interpretation never treats an uncorrected feature as corrected. State in the report how many features were corrected, partly corrected and not corrected.  
* **Zeros and missing values are never changed**, so detection counts and prevalence (Section 5) are the same before and after.  
* **Validation uses held-out QCs only.** The script scores each QC with a model trained on the other half of that batch's QCs. A flexible spline always fits the QCs it was trained on, so QC %RSD or batch R² computed on the training QCs is not evidence that the correction worked; never report it as such. Label every QC statistic **held-out** or **in-sample**. Report the held-out %RSD before and after and the number of features with a batch effect before and after.  
* **Features that got worse.** The script reports the features whose held-out QC %RSD is significantly higher after correction (bootstrap, raw p below 0.05). Report their number and list them. Revert them to the raw values (flag `reverted`) only if the user approves. On the calibration dataset 22 of 301 were worse and 200 were improved.  
* **If the correction did not work** (the criteria in Section 3.10.4 are not met), say so, show the evidence, and ask whether to continue with the corrected table, the raw table, or another approach. Do not proceed silently.  
* **Group-by-batch table.** When a group variable exists, `--group-col` writes the number of study samples per group and batch. If any group is absent from one or more batches, report that group and batch are partly confounded. QC-based correction does not use group labels, so it does not remove group differences, but it cannot separate batch from group where they coincide; name this as a limitation and list it as an open item (Section 17.1).  
* **Downstream data states.** The QC filter (Section 3.4) uses the **held-out** QC %RSD (log the data state as `post-batch-correction, held-out QCs`). The blank filter (Section 4) uses the corrected study-sample values against the blanks (blanks are not corrected); log which data state it used. Normalization (Section 7) and later steps use the corrected values. If internal-standard normalization is chosen as well, record that both were applied and in which order.  
* **Keep the raw table.** The raw and the corrected tables are both delivered and both labelled.

### 3.10.6 Figures (technical report)

Draw these from the script's CSV files. Examples from the calibration dataset are in `examples/`, beside this document; follow their layout, but take every number from the current data. All figures follow the standing preferences: a graphical colour key, raw p-values printed on the plot with a colour key for them, full feature names (m/z and RT or the annotation name, never a bare row ID), plain-language statement of what every box, line, star and dot represents, and no fold-change cutoff. Figure numbers follow report order ([REPORT.md](REPORT.md), Section 3). When the decision was **skip**, show only panels A, C and D of the first figure (before correction) and one line saying correction was not run.

1. **Was correction necessary (four panels).** A: PCA of all injections before correction; B: after correction. Study samples as small dots, pooled QCs as stars, coloured by batch, with a colour key; each panel states the pooled-QC spread as a share of the sample spread and the share of sample PC2 explained by batch. PCA on features detected in at least 90% of study samples (log10, zeros set to half the feature minimum, autoscaled). **In B, plot the held-out QCs.** C: boxplots of per-feature batch R² of the pooled QCs, uncorrected and corrected (held-out), with the median and the share of features with a significant batch effect (BH q below 0.05) and with the full affected rule, printed above each box. D: boxplots of per-feature within-batch drift (mean |Spearman| of QC against injection order across batches), uncorrected and corrected. Under C and D, a line explaining the box convention (box = middle 50% of features, line = median, whiskers = 1.5 times the interquartile range, outliers hidden).  
2. **One feature, before and after.** Two features side by side, each with an "original" and a "corrected" panel over injection order (log10 peak area): study samples, pooled QCs, blanks, batch starts, the QC trend (original) and QC median (corrected), and above the panels the held-out %RSD, %D-ratio (SD of QCs over SD of study samples times 100) and %blank ratio (median blank over median study sample times 100), before and after. Features: the internal standard when provided, and the feature with the **median** held-out improvement among eligible features (a representative case; not the best case). Say how the features were chosen under the figure.  
3. **Forest plot of the change in QC %RSD.** One row per shown feature (full names): square at the before-minus-after %RSD with a 95% bootstrap interval (1,000 resamples of the QCs, unweighted), square area growing with the %RSD after correction. Colour by raw two-sided bootstrap p (red: significantly improved, blue: not significant, grey: significantly worse) with a colour key, and the pooled mean with its interval at the top. With many features, show every k-th by effect size plus the internal standard and say so. Clip the axis for extreme features with a labelled arrow. State that p-values are raw and that the smallest reportable p is 0.001.  
4. **Internal-standard evidence (when standards were provided).** For the standard: A, its pooled-QC area against injection order before correction with the batch medians drawn as lines; B, the same after correction (held-out); each with the batch ANOVA p and R² and the Kruskal-Wallis p printed on the panel. C: Spearman rho of QC area against order for each batch, before and after, filled markers where p is below 0.05, with a colour key and the p-value beside each marker. Say that the standard's own QC CV can look acceptable while the batch shift is the flag, and give the standard's R² rank among eligible features so it is not over-read.

### 3.10.7 What this stage publishes

The script writes its files into the run's folder under the prefix given with `--prefix`. Each is published as an output of this stage:

* **The corrected table**, in the input layout (features-in-rows tables also carry `batch_corrected` and `batch_corrected_reason`).  
* **The per-feature correction table**: one row per feature: eligibility and reason, QC detection, positive QCs per batch, raw and held-out batch R², p, q and affected flag, fold range, drift, QC %RSD before and after (held-out), bootstrap change with interval and p, significantly better or worse, and `batch_corrected`.  
* **The held-out corrected QC values** (for the PCA and the feature figures).  
* **The summary**: dataset-level numbers, thresholds, recommendation, held-out result, script and library versions, seed.  
* **The group-by-batch table**, when a group variable exists.  
* **The check's per-feature table and summary**, when the check was run alone, or on an already corrected file. Where correction is not possible or not needed, the check's summary is still published, with the reason.  
* The figures above, each beside the table it plots.  
* What the stage's procedure states: block `batch_correction` (Section 14).

### 3.10.8 Validate

Before delivery, check and record that:

* `python scripts/qcrsc.py selftest` passed in this session (it simulates a known batch shift and drift, and a no-effect dataset). If it fails or the libraries are missing (`numpy`, `pandas`, `scipy` 1.10 or later), stop and report. Only if the user agrees may the procedure of Section 3.10 be re-implemented, and the result is then labelled **re-implementation, not validated**.  
* Every input feature appears once in the corrected table; non-eligible features are unchanged; zeros are unchanged; sample order and IDs match the input.  
* Retained features in the filtered table equal their rows in the corrected unfiltered table (maximum absolute difference zero or within a stated tolerance).  
* The held-out criteria of Section 3.10.4 were evaluated and the result stated.  
* Every QC statistic in the report is labelled held-out or in-sample.  
* The figures' numbers agree with the CSV files and the summary.

### 3.10.9 Boundaries

* The check and the correction describe technical variation only. Do not interpret a batch effect biologically.  
* Do not substitute another correction (batch median, ComBat, or a tool the user did not name) without saying so and recording it; those are different methods with different assumptions.  
* QCRSC needs pooled QCs that are the same material throughout the run. If the QCs were prepared in separate pools per batch, say that between-batch alignment is then not supported by the QCs and ask the user how to proceed.

---

# 4\. Blank Filtering

## Objective

Identify features whose observed signal may primarily originate from analytical background, contamination, solvents, reagents, or other non-biological sources.

## 4.1 Identify blank types

Determine whether blanks are:

* Solvent blanks  
* Extraction blanks  
* Procedural blanks  
* Other negative controls

Do not assume that all blank types are equivalent.

When multiple blank types exist, consider them separately.

## 4.2 Determine available blank comparisons

For each feature, assess when possible:

* Presence/absence in blanks  
* Abundance in blanks  
* Abundance in biological samples  
* Frequency across biological samples  
* Number of blank replicates

The preferred comparison depends on the structure and quality of the blank data.

## 4.3 User-configurable filtering criteria

Potential approaches include:

### Sample-to-blank abundance ratio

Retain a feature when biological sample abundance exceeds blank abundance by a user-defined ratio.

Example:

> Retain features with sample/blank ratio ≥5.

The ratio threshold must be explicitly recorded.

### Blank prevalence

Consider removing features that occur consistently across blanks.

### Combined criteria

A feature may be retained or removed using both abundance and prevalence criteria.

The skill should explain the selected criterion before execution.

## 4.4 Default behavior

Do not impose a universal blank ratio.

If blanks are available but the user has not specified a threshold:

1. Explain why blank filtering may be appropriate.  
2. Characterize the blank/sample signal distribution.  
3. Evaluate candidate ratio and/or prevalence thresholds.  
4. Recommend a starting criterion based on the observed data and study objective.  
5. Explain the tradeoff between removing background and retaining genuine low-abundance metabolites.  
6. Ask the user to confirm or modify the criterion.

## 4.5 Special considerations

Do not automatically remove a feature simply because it appears in blanks.

Some metabolites may genuinely occur in both blanks and biological samples.

Consider:

* Relative abundance  
* Prevalence  
* Magnitude of biological signal  
* Blank composition  
* Chemical plausibility  
* Known contaminants

## 4.6 Report

Record:

* Blank type  
* Number of blank samples  
* Filtering method  
* Threshold  
* Number of features removed  
* Number retained  
* Features with ambiguous blank behavior  
* Data state of the sample abundances used (raw or batch-corrected; Section 3.10.5). Blanks are never batch-corrected; compare them with the corrected study samples when correction was run

---

# 5\. Prevalence Filtering

## Objective

Remove features that occur too infrequently to support reliable biological interpretation while avoiding unnecessary loss of biologically meaningful low-prevalence metabolites.

## 5.1 Determine prevalence

Calculate feature prevalence as the proportion of samples containing a measurable signal according to the dataset's representation.

Clarify whether zero and missing values represent:

* True absence  
* Values below detection  
* Missing measurements  
* Unprocessed data

Do not treat missing values as biological zeros without justification.

## 5.2 Determine filtering scope

Potential scopes include:

### Overall prevalence

Require a feature to be present in a specified proportion of all samples.

Example:

> Retain features present in ≥70% of all samples.

### Group-specific prevalence

Require a feature to meet the prevalence threshold within at least one or more biological groups.

Example:

> Retain features present in ≥70% of samples in at least one group.

### All-group prevalence

Require the feature to meet the threshold in every relevant biological group.

This is more stringent and may remove disease-specific metabolites.

### Metadata-aware prevalence

Retain a feature if it passes the standard prevalence rule or is concentrated in a metadata subgroup (see 5.7).

Recommend this option only when the available metadata make it sensible.

## 5.3 Recommended decision process

Before selecting a prevalence threshold, inspect:

* Group sizes  
* Distribution of feature prevalence  
* Number of low-prevalence features  
* Whether rare features are biologically relevant to the research question  
* Whether the analysis seeks broadly distributed metabolites or disease-associated features  
* The detection-rate table of Section 13B (how many features sit in each detection tier, and what share of each tier has MS/MS and a library match)

Do not recommend a prevalence threshold without considering group sizes and the study objective.

## 5.4 User-configurable parameters

The user should be able to specify:

* Threshold  
* Scope  
* Whether filtering is calculated across all samples or within groups  
* Whether technical replicates are collapsed before calculating prevalence

Example:

> Use 70% prevalence in at least one biological group.

Record the exact interpretation.

## 5.5 Sensitivity analysis

When prevalence filtering materially affects the number or identity of significant findings, consider comparing results across reasonable thresholds.

For example:

* 50%  
* 70%  
* 80%

The purpose is not to identify a universally optimal threshold but to determine whether major biological conclusions are robust to reasonable preprocessing choices.

## 5.6 Report

Record:

* Prevalence definition  
* Threshold  
* Scope  
* Number of features removed  
* Number retained  
* Major findings affected by the filter

## 5.7 Metadata-aware prevalence filtering

### Why it is helpful

A standard prevalence filter evaluates prevalence in the whole sample or in the primary comparison groups. Features that occur almost only in a metadata subgroup (for example, drug metabolites present only in patients receiving a particular medication) cannot reach the threshold in the full group and are removed, even though they may be real and important. A metadata-aware filter protects such features.

### When to recommend it

Recommend it only if the metadata contain variables that define subgroups plausibly linked to specific features (treatment or medication, sex, age bands, site, diet, and similar) and at least some subgroups are large enough to assess. Do not recommend it when no such metadata exist or all subgroups are too small, and say so explicitly.

When presenting prevalence options, always list the alternatives with their trade-offs: overall prevalence, group-specific (at least one group), all-group, threshold variants, and, when the metadata allow it, the metadata-aware option.

### Why not a plain "present in at least X% of any subgroup" rule

In small subgroups a feature reaches X% by chance. A plain rule therefore admits mostly chance features. Test any rule against random same-size groups before adopting it.

### Recommended procedure

1. Candidates are features that pass all other filters but fail the standard prevalence rule.  
2. For each metadata group (every level of each variable), define a comparison population. For variables that exist only within a subset (for example treatments among patients), compare within that subset; otherwise compare with all other samples. Exclude samples with missing values for the variable.  
3. Admit a feature when it is present in at least a minimum share of the group, exceeds the comparison population by a minimum difference in prevalence, and is detected in at least half of the group.  
4. Calibrate every group. Estimate how many features a random group of the same size, drawn from the same comparison population, would admit, using many random draws. A group contributes only if the expected chance admissions are a small fraction of the observed admissions. Report observed and expected numbers for every group, and report groups that are too small as "too small to assess".  
5. Flag every rescued feature with the group that rescued it.  
6. Thresholds are not universal. Propose starting values (minimum in-group prevalence 50%, difference of 60 percentage points, chance-to-observed ratio of 10% or less, at least 300 random draws), state that they are starting values, and ask the user to confirm or change them before execution.  
7. Ask the user whether rescued features join the main multiple-testing family or are analyzed separately, and state the trade-off: features chosen on subgroup data have optimistic p-values for the primary contrast if merged.

### Record

* Variables scanned  
* Comparison populations  
* Parameters  
* Observed and expected counts per group  
* Number of rescued features  
* Which group rescued each feature

&nbsp;

## 5.8 Prevalence filter warning

Whenever recommending or discussing a prevalence filter, **always display a bold warning that prevalence filtering can remove rare but biologically important features. This risk is particularly relevant to drugs, antibiotics, dietary biomarkers, environmental exposures, and features associated with personalized or precision medicine, where a genuine signal may occur in only a subset of samples.**

Explain that rare features are not necessarily biologically meaningful, but their low prevalence alone is not sufficient evidence that they should be removed.

Before recommending a threshold, consider whether prevalence should be assessed across all samples, within experimental groups, or within other scientifically relevant subgroups. Explain the trade-offs associated with the proposed threshold and obtain the user's approval before applying the filter.

If the user proceeds, keep the unfiltered feature table and publish it alongside the filtered table. Also record the filtering criteria and parameters, identify which features were removed, and document the reason for each removal where available. This allows rare features to be revisited for targeted biological interpretation or follow-up analysis.

Do not silently reintroduce filtered features into the primary analysis. If removed features appear potentially important during downstream interpretation, flag them for user review and propose an appropriate follow-up analysis.

---

# 6\. Missing Values

## Objective

Distinguish technical missingness from biological absence and determine whether missing values require filtering, imputation, or another treatment.

## 6.1 Characterize missingness

Determine:

* Overall missingness  
* Feature-level missingness  
* Sample-level missingness  
* Group-specific missingness  
* Whether missing values are represented as NA, blank, zero, or another value  
* Whether missingness appears related to abundance

Do not assume that zero values and missing values have the same meaning.

## 6.2 Determine whether filtering should precede imputation

When a feature has substantial missingness, consider whether it should be removed before imputation.

The decision should depend on:

* Research question  
* Sample size  
* Group structure  
* Detection characteristics  
* Expected missingness mechanism

Avoid imputing highly sparse features simply to retain them for downstream analysis.

## 6.3 Identify potential group-dependent missingness

Determine whether missingness differs substantially between biological groups.

A feature that is frequently observed in one group and absent in another may represent meaningful biological or detection-related information.

Do not automatically convert such patterns into numerical abundance values without considering the underlying measurement process.

## 6.4 User-configurable imputation

If imputation is appropriate, the user should be able to select the method.

Potential approaches may include:

* Minimum-value or half-minimum substitution  
* Group-aware imputation  
* K-nearest-neighbor methods  
* Model-based approaches  
* Other validated methods

The skill should not recommend a specific imputation method solely because it is commonly used.

The recommendation should consider the missingness pattern and downstream analysis.

## 6.5 Report

Record:

* Missing-value representation  
* Missingness statistics  
* Filtering decisions  
* Imputation method  
* Parameters  
* Number of affected values  
* Sensitivity of important findings to the missing-value strategy, when appropriate

---

# 7\. Normalization

## Objective

Determine whether systematic differences in sample-level signal require normalization and select an approach appropriate to the data and analytical objective.

## 7.1 Determine whether normalization is necessary

Inspect:

* Total feature signal per sample  
* Feature count per sample  
* Internal-standard behavior  
* Sample preparation structure  
* Instrumental/batch effects  
* Whether the input has already been normalized  
* Whether biological differences in total signal could themselves be meaningful

Do not automatically normalize every feature table. Deciding whether normalization is necessary does not replace the comparison in Section 7.4.1; "no additional normalization" is itself a candidate in that comparison and has to be tested against the others.

Normalization can remove biologically meaningful variation if total signal or compositional structure differs because of the biology being studied.

## 7.2 Identify available normalization information

Determine whether the dataset contains:

* Internal standards  
* Pooled QC measurements  
* Sample-volume information  
* Biomass/cell-count information  
* Dilution factors  
* Known loading factors  
* Batch information

Prefer experimentally justified normalization factors when available.

Internal-standard information comes from Section 3.8 (the user's list, the check, and any merged standard rows). If no standards were provided, internal-standard normalization is not available.

Batch information is used by the correction of Section 3.10. Normalization runs on the corrected values, and the order of the two steps is logged.

## 7.3 Candidate normalization approaches

Depending on the dataset, consider:

* Internal-standard normalization (needs the standards of Section 3.8; use merged standard rows if the check found a split and the user approved the merge)  
* Sample-total or sum normalization  
* Median-based normalization  
* Probabilistic quotient normalization
* robust centered log-ratio transformation (rCLR) normalization   
* Other established normalization methods  
* No additional normalization

Do not treat these methods as interchangeable.

The recommendation should consider:

* Data generation process  
* Expected compositional effects  
* Presence of technical dilution differences  
* Internal standards  
* Study objective  
* Whether the data have already undergone normalization

## 7.4 Assess normalization before execution

The normalization comparison (Section 7.4.1) runs on every run in which the input is a raw feature table. It runs whether or not a normalization method has been specified:

* **No method specified:** run the comparison, give a recommendation, and let the user select or override it (steps below).
* **The user named a method:** apply the named method as specified. Include it as one of the candidates, run the same comparison alongside it as a sensitivity check, and report any disagreement in the decision record and the report. Never substitute a different method silently.
* **The input is already normalized:** the comparison is not applicable (Section 7.4.2).
* **The user switches the comparison off:** record that in the decision record (`normalization_comparison.status: user_switched_off`) and in the report.

Steps for the comparison:

1. Characterize sample-level signal distributions.  
2. Identify evidence of technical dilution or loading differences.  
3. Determine whether internal standards or other experimentally justified factors are available.  
4. Identify whether the proposed normalization could remove biological signal.  
5. Present the most appropriate options.  
6. Recommend comparing several candidate methods (see 7.4.1) instead of recommending a single method in advance. If an experimentally justified factor (internal standard, mass, volume) exists, include it as a candidate.  
7. Present the comparison data to the user, give a recommendation based on that evidence, and allow the user to select or override it.

### 7.4.1 Normalization comparison (required)

Do not recommend a single normalization method in advance. Check several candidates and present the resulting data so the user can decide. The comparison itself is automatic and changes no data; the method that is applied is chosen by the user. Figures follow the report figure standards (a graphical color key for methods and groups, p-values shown on the plot with a key, and a note on the figure saying what each box or group represents).

* Candidates: use those relevant to the data, for example no normalization with transformation only, a sum-based method, a median- or quotient-based method, a compositional log-ratio method when appropriate, an rCLR normalization when appropriate, and an internal-standard or other experimentally justified factor when available.  
* Define the diagnostics before looking at group results. For example: association of sample-level technical variables (total signal, number of detected features, contaminant fraction, internal standard) with the data before and after normalization; whether the correction applied to each sample differs between groups; QC stability; the mean-variance relationship; recovery of any known positive-control features; calibration under label permutation (false discoveries when group labels are shuffled); and agreement of effect sizes between methods.  
* When methods disagree strongly, determine whether the difference comes from the normalization itself or from a coupled step such as zero handling or transformation, and report which.  
* Present the results as a table plus figures, state what each diagnostic can and cannot show, and give a recommendation. The user selects the method.  
* If the feature set changes after the comparison (for example after a rescue step), validate the chosen method on the final feature set (7.5).

Do not choose a normalization method solely because it is commonly used in metabolomics.

### 7.4.2 Input already normalized: comparison not applicable

If the feature table has already been normalized (Section 2.2), the comparison cannot be run on it: a normalization cannot be reliably undone, and normalizing on top of it can introduce artifacts.

1. Tell the user, upfront and in one line, that the normalization comparison is not applicable to a table that has already been normalized, and ask them to upload a raw feature table (peak areas or intensities before normalization). For an Everything Bagel task, check first whether the raw quantification table is available from the task ([GNPS2-FILES.md](GNPS2-FILES.md)).
2. If a raw table is provided, run the analysis on the raw table and run the comparison as in 7.4.1. The existing normalization may be included as a candidate only if it can be reproduced from the raw table.
3. If no raw table can be provided, continue with the table as supplied. Do not apply any further normalization unless the user explicitly asks for it. Record `normalization_comparison.status: not_applicable_input_already_normalized`, the existing normalization (method and who applied it, or `unknown`), and that the comparison was not run. State this in the technical report as a limitation.
4. If the user does not know whether the table was normalized, flag the history as unknown, ask once for the raw table, and follow step 3 if none is available.

## 7.5 Validate normalization

After normalization, assess whether:

* Sample-level signal differences were reduced as intended.  
* QC behavior improved or remained acceptable.  
* Known biological structure was preserved.  
* Extreme sample values were introduced.  
* The normalization produced unexpected distributions.

If normalization substantially changes the biological findings, flag this for sensitivity analysis.

## 7.6 Report

Record:

* Whether normalization was applied  
* Normalization method  
* Normalization factor  
* Data state before normalization  
* Data state after normalization  
* QC behavior before/after  
* Number of samples affected  
* Important findings changed by normalization

---

# 8\. Transformation and Scaling

## Objective

Determine whether transformation or scaling is needed to make the data more appropriate for downstream statistical analysis and visualization.

## 8.1 Assess the abundance distribution

Inspect:

* Right-skew  
* Dynamic range  
* Extreme values  
* Heteroscedasticity  
* Distribution of feature abundances  
* Distribution after normalization

Do not assume that all metabolomic feature tables require the same transformation.

## 8.2 Transformation

Potential transformations include:

* Log transformation  
* Log2 transformation  
* Cube-root or other monotonic transformations  
* No transformation

The choice should depend on the abundance distribution and downstream statistical method.

If zero or negative values are present, identify how they will be handled before applying a transformation that cannot accommodate them.

Do not add arbitrary pseudocounts without recording and justifying the choice.

## 8.3 Scaling

Distinguish transformation from multivariate scaling.

Potential scaling approaches include:

* No scaling  
* Autoscaling  
* Pareto scaling  
* Range scaling  
* Other method appropriate to the analysis

Scaling should be selected based on the intended analysis.

For example, scaling that is useful for PCA or PLS-DA is not automatically appropriate for feature-level differential abundance testing.

## 8.4 Decision process

Before transformation or scaling:

1. Inspect the data distribution.  
2. Identify the downstream analysis.  
3. Determine whether the statistical method assumes or benefits from a particular data representation.  
4. Present relevant options.  
5. Recommend an approach when justified.  
6. Allow user selection or override.  
7. Record the exact transformation/scaling operation.

## 8.5 Validate

After transformation or scaling, assess:

* Distributional changes  
* Extreme values  
* Feature/sample structure  
* QC behavior  
* Compatibility with the planned statistical analysis

Do not describe transformed values as directly comparable to untransformed values without qualification.

---

# 9\. Outlier Assessment

## Objective

Identify observations that may disproportionately influence downstream analyses without automatically treating unusual observations as erroneous.

## 9.1 Distinguish sample-level and feature-level outliers

Assess separately:

* Sample-level outliers  
* Feature-level extreme values  
* QC outliers  
* Group-specific outliers

A sample can be unusual without being erroneous.

## 9.2 Detect potential outliers

Use multiple sources of evidence where appropriate:

* Overall signal  
* PCA or other multivariate structure  
* Feature-level distributions  
* QC behavior  
* Metadata  
* Technical records  
* Statistical influence diagnostics

Do not exclude an observation based solely on a single visualization.

## 9.3 Determine whether an outlier is technical or biological

Before exclusion, investigate:

* Sample processing problems  
* Instrument/QC evidence  
* Metadata inconsistencies  
* Known biological characteristics  
* Whether the observation is plausible for the study population

An unusual biological sample should not be removed simply because it weakens a statistical association.

## 9.4 User decision

When an observation is flagged:

1. Show the evidence supporting the flag.  
2. Identify whether a documented technical reason exists.  
3. Explain the consequences of exclusion.  
4. Ask the user whether to exclude, retain, or perform sensitivity analysis.

Do not silently remove samples.

## 9.5 Sensitivity analysis

When exclusion is scientifically plausible but uncertain, compare the primary analysis with and without the observation.

Report whether the major finding:

* Persists  
* Weakens  
* Disappears  
* Changes direction

Describe the finding as **outlier-sensitive** when appropriate.

---

# 10\. Statistical Analysis Selection

## Objective

Select statistical analyses that match the experimental design, data structure, research question, and assumptions.

The skill should determine the appropriate statistical framework before testing individual features.

## 10.1 Define the statistical question

Identify whether the user is asking about:

* Differences between groups  
* Associations with a continuous variable  
* Associations with categorical metadata  
* Longitudinal change  
* Paired differences  
* Interactions  
* Covariate-adjusted associations  
* Overall multivariate differences  
* Relationships among metabolites

Do not select a statistical test until the scientific question is defined.

## 10.2 Respect experimental design

Determine whether observations are:

* Independent  
* Paired  
* Repeated measures  
* Nested  
* Clustered  
* Technical replicates

Do not use a test that assumes independent observations when the design contains within-subject or other correlated observations.

Technical replicates should not automatically be treated as independent biological observations.

## 10.3 Select the model family

Choose a statistical model based on:

* Outcome type  
* Predictor type  
* Number of groups  
* Independence structure  
* Repeated measures  
* Covariates  
* Distributional characteristics  
* Sample size

Examples include:

* Two-group comparisons  
* Multi-group comparisons  
* Correlation/association analyses  
* Linear models  
* Generalized linear models  
* Mixed-effects models  
* Multivariate methods

Choose the exact implementation from the design and data, and record the model, software and parameters in the decision record. No separate statistical reference file is bundled with this skill.

## 10.4 Assess model assumptions

Before interpreting results, evaluate assumptions relevant to the selected method.

Potential considerations include:

* Independence  
* Residual structure  
* Variance structure  
* Distribution of residuals  
* Linearity  
* Influential observations  
* Sample size  
* Separation or convergence problems for applicable models

If assumptions are substantially violated, consider an alternative model or analysis.

Do not automatically switch methods without recording the reason.

## 10.5 Effect size and uncertainty

For every primary statistical finding, report more than statistical significance.

When applicable, report:

* Effect size  
* Direction of effect  
* Confidence interval  
* Raw p-value  
* Multiple-testing-adjusted p-value  
* Sample size  
* Model or test used

Avoid ranking findings using p-value alone.

## 10.6 Multiple testing

When many features are tested simultaneously:

1. Define the family of hypotheses.  
2. Apply an appropriate multiple-testing procedure.  
3. Report both raw and adjusted significance measures.  
4. Distinguish statistical significance from biological importance.

## 10.7 Multivariate analysis

Recommend always running multivariate analysis (PCA, PLS-DA, etc) in addition to other univariate analyses. The VIP values can be used later on.

## 10.8 Feature-level versus multivariate analysis

Distinguish between:

* **Feature-level analysis:** identifies individual features associated with the outcome.  
* **Multivariate analysis:** evaluates coordinated variation across features.

A feature that is not individually significant should not automatically be considered biologically irrelevant, but multivariate significance should not be presented as evidence that every contributing feature is significant.

## 10.9 Sensitivity analysis

When a statistical decision is uncertain or potentially influential, compare results across scientifically reasonable analytical specifications.

Examples include:

* Alternative normalization  
* Alternative transformation  
* Covariate-adjusted versus unadjusted models  
* Alternative outlier handling  
* Alternative missing-value treatment

Significant findings that depend strongly on one analytical specification should be flagged as **analysis-sensitive**.

---

# 11\. Covariate Assessment and Adjustment

## Objective

Determine whether variables other than the primary exposure/group may explain, confound, or otherwise influence observed metabolomic associations.

## 11.1 Identify available metadata

Inspect available variables such as:

* Age  
* Sex  
* BMI  
* Medication  
* Batch  
* Disease activity  
* Clinical measurements  
* Demographic variables  
* Sample collection variables

Do not assume that every available metadata variable should be included in the statistical model.

## 11.2 Distinguish covariate roles

Consider whether a variable is:

* Potential confounder  
* Technical variable  
* Effect modifier  
* Mediator  
* Consequence of disease  
* Variable of primary scientific interest

Avoid automatically adjusting for variables that may lie on the biological pathway being investigated.

## 11.3 Identify candidate covariates

Candidate covariates should be considered based on:

* Study design  
* Scientific rationale  
* Known confounding relationships  
* Association with the primary exposure  
* Association with the metabolomic outcome  
* Data completeness  
* Sample size

Do not select covariates solely because they are statistically associated with the outcome.

## 11.4 Compare adjusted and unadjusted analyses

When covariate adjustment is scientifically justified, consider comparing:

* Unadjusted model  
* Covariate-adjusted model

Record changes in:

* Effect size  
* Direction  
* p-value  
* FDR  
* Feature ranking

A finding that disappears after adjustment should be identified as potentially explained by the covariate rather than simply labeled “not significant.”

## 11.5 Metadata driver analysis

When the objective includes discovering major sources of metabolomic variation beyond the primary comparison, the skill may perform a systematic metadata screen.

This may include:

* Association between metadata variables and individual features  
* Correlation of metadata variables with multivariate structure  
* PERMANOVA or related multivariate approaches  
* Comparison of variance explained by major metadata variables

The purpose is exploratory identification of potentially important drivers, not automatic causal inference.

---

# 12\. Analytical Robustness and Sensitivity

## Objective

Determine whether significant findings depend strongly on analytical choices.

## 12.1 Identify influential decisions

Consider sensitivity analysis when findings may reasonably be affected by:

* QC filtering  
* Blank filtering  
* Prevalence filtering  
* Missing-value handling  
* Normalization  
* Transformation  
* Scaling  
* Outlier exclusion  
* Covariate adjustment  
* Statistical model selection

## 12.2 Define robustness

A finding may be considered more robust when it:

* Persists across reasonable preprocessing choices.  
* Maintains direction of effect.  
* Maintains a similar magnitude of effect.  
* Remains statistically supported where appropriate.

Do not require identical p-values or rankings across analyses.

## 12.3 Define sensitivity

Flag a finding as analysis-sensitive when a reasonable analytical decision:

* Reverses its direction.  
* Removes statistical support.  
* Substantially changes its effect size.  
* Changes its interpretation.  
* Causes it to disappear entirely.

Sensitivity should be reported as information about uncertainty, not necessarily as evidence that the finding is invalid.

---

# 13\. General Rule for Preprocessing Decisions

Preprocessing choices should be treated as analytical assumptions rather than invisible technical steps.

For every major preprocessing decision, the final report should allow the reader to answer:

> What did the analyst do, why did they do it, what alternatives were considered, and would the major biological conclusions change if the decision were different?

The framework should not impose a universal order for preprocessing operations.

Instead, the skill should determine the appropriate order based on:

* Data representation  
* Existing preprocessing  
* QC structure  
* Missingness  
* Study design  
* Statistical assumptions  
* The specific analytical objective

If one preprocessing step depends on the result of another, that dependency should be made explicit.

When a preprocessing choice materially changes a biological conclusion, the finding should be flagged as **preprocessing-sensitive**.

When a finding persists across reasonable preprocessing choices, it may be described as **preprocessing-robust**, provided that the comparison was appropriately performed.

---

# 13A. Parallel Unfiltered Table

## Objective

Process the **unfiltered** feature table with the same operations as the final filtered table, analyze it the same way, and publish it beside the filtered one. This lets the filter-loss review in interpretation ([INTERPRET.md](INTERPRET.md), Section 4A) and this analysis's own review (Section 15\) compare retained and removed features on equal terms, without recomputing anything.

This is **on by default**. Mention it in the first decision breakdown. The user may switch it off; if so, record that in the decision record and warn that interpretation will not have the unfiltered table.

## 13A.1 Definition

* **Unfiltered table:** every feature in the input feature table, before any feature-removal filter (QC, blank, prevalence, in-source-fragment flag, retention-time window, intensity, replicate, or other). Feature-level flags are kept as columns; no feature is dropped.  
* **Same samples:** the sample set is identical to the final analysis, including the same sample and QC-injection exclusions. Sample-level decisions are never different between the two tables.

## 13A.2 Same operations

Apply to the unfiltered table the same operations, in the same order, as the final filtered table:

* **Normalization:** the same method, using the **same per-sample normalization factors that were derived for the final filtered table**. Do not recompute factors on the larger feature set. This keeps the values of retained features **identical** in both tables, so the unfiltered table is a strict superset. If a method's factor depends on the feature set (for example sum or quotient-based factors), say so, use the filtered-table factors, and record that choice.  
* **Zero and missing-value handling, and imputation:** the same method and parameters.  
* **Transformation and pseudocount:** the same.  
* **Scaling:** the same, where scaling is used.  
* **Batch correction:** corrected once on the full unfiltered table (Section 3.10.5); the filtered table takes its values from that result. Features that could not be corrected keep their raw values and carry the `batch_corrected` flag.  
* Record any operation that cannot be applied identically, what was done instead, and why. Do not substitute silently.

## 13A.3 Same analyses

Run the same analyses on the unfiltered table as on the final filtered table:

* the same primary statistical model, covariates, and repeated-measure structure;  
* the same effect size, confidence interval, and raw p-value;  
* the same multivariate analyses (for example PCA and PLS-DA, including VIP);  
* sensitivity analyses on the filtered table are not repeated on the unfiltered table unless the user asks.

**Multiple testing.** The primary q-values stay as computed within the filtered family and are never changed. For the unfiltered table, report the same raw p and the primary q (for retained features), plus a **separate, labelled unfiltered-family q** for all features. Features that were removed are outside the primary family and their results are exploratory. Never merge the two families silently. Rescued features follow the user's decision in Section 5.7, step 7\.

## 13A.4 Sparse and asymmetric features

Imputation does not make a highly sparse feature reliable (Section 6.2). For every feature in the unfiltered results, also report:

* detection count and prevalence per group;  
* the fraction of values that were imputed;  
* the effect size from detected samples only, next to the all-sample effect size.

Flag features whose result rests mostly on imputed values, and features detected in one group and rarely in the other (the presence or absence may itself be the signal).

## 13A.5 Per-feature flags

Every row in the unfiltered results carries: retained (yes or no); every filter that removed it (all that apply, not only the first); the filter metrics (QC CV, blank ratio, prevalence by group); the rescue flag and the group that rescued it; the annotation tier and name; and `batch_corrected` (yes, partial, no or reverted) with its reason (Section 3.10.5).

## 13A.6 Validate

Before delivery, check and record that:

* the unfiltered table has every feature from the input and the same samples, in the same order, as the filtered table;  
* retained plus removed features equals the total number of input features;  
* for retained features, values in the two tables are identical (maximum absolute difference is zero, or within a stated numeric tolerance);  
* batch-corrected values of retained features are identical in both tables, and every feature in the unfiltered table carries a `batch_corrected` flag;  
* the same transformation, imputation, and normalization factors were applied;  
* the same models and settings were used.

If a filter is re-run after an add-back decision (Section 15.3), regenerate the unfiltered outputs so the retained flags stay consistent.

## 13A.7 Labelling

Label unfiltered results as **"unfiltered table"** in every table and figure. Results for removed features are exploratory. The unfiltered results never replace the primary results. Report this section's outputs descriptively only; interpretation belongs to the deeper analysis skill.

---

# 13B. Detection-Rate Bins and MS/MS Match Rate

> Companion sections: the feature table comes from [GNPS2-FILES.md](GNPS2-FILES.md) (quantification table, library annotations); the report layout is in [REPORT.md](REPORT.md) (Section 0B); the table feeds the prevalence decision in Section 5.3.

## Objective

Show how many features are detected in how many samples, and how much of each detection tier has MS/MS spectra and library matches. This answers the question: **of the features seen in more than 1% of samples, and of those seen in more than 50% of samples, what share has MS/MS and what share has a library match?**

This is a descriptive technical summary. It removes no feature and recommends no threshold. It is **on by default for every run** and is mentioned in the first decision breakdown (together with Section 13A). The user may switch it off; record that in the decision record.

## 13B.1 Definitions

* **Feature universe:** the **unfiltered** feature table (every feature in the quantification table, before any feature-removal filter). State the number of features and name the file. If feature merges were approved (Section 3.9), state whether the count is before or after the merge and give both feature numbers.  
* **Samples counted:** the biological samples of the primary comparison (for example HC and PT). Exclude blanks, pooled QCs and other controls. State the number of samples and, if groups exist, the number per group.  
* **Detected:** peak area above zero in that sample. Zeros encode "not detected" in EB tables; say so in the report. State whether gap-filled areas are counted as detected (the delivered table includes gap-filled areas; `gap_fill_report.tsv` marks which values were filled). If gap-fill is on, add a one-line check using the `was_detected` flag, or say it was not run.  
* **Detection rate:** detected samples divided by samples counted (as a percentage).  
* **MS/MS feature:** `has_ms2` is true in the quantification table (a consensus MS/MS spectrum exists).  
* **Library match:** the feature has at least one hit in the library search results (`query_scan` equals the quantification-table row ID). Report the library settings used (libraries, minimum cosine, minimum matched peaks, `topk`).  
* **MS/MS match rate:** share of features in a bin (or above a cut-off) that have MS/MS.  
* **Library match rate:** share of features with a library match, reported twice: as a share of **all** features and as a share of the **MS/MS features** (a library match needs MS/MS, so the second number is the fairer match rate).  
* **Cut-offs in samples:** convert every percentage cut-off to a number of samples and state it (for example, more than 1% of 56 samples means at least 1 sample, so the ">1%" row equals "detected anywhere"). When this happens, say so.

## 13B.2 Bins and cut-offs

Default bins (the user may change them; record any change):

| Bin | Definition |
| :---- | :---- |
| Not detected | Detected in no counted sample (area zero in all) |
| >0 to <10% | Detection rate above 0% and below 10% |
| 10 to <25% | 10% up to but not including 25% |
| 25 to 50% | 25% up to and including 50% |
| >50% | Above 50% |

Required cumulative rows: **features detected in more than 1% of samples** and **features detected in more than 50% of samples**. Optional: the same table within each group (detection rate computed inside the group), when groups are defined.

## 13B.3 Table (Table 1 in the technical report)

Columns: bin or cut-off; features; features with MS/MS; MS/MS rate (%); features with library match; library match rate, all features (%); library match rate, MS/MS features (%). The bin rows and the two cumulative rows share one table.

## 13B.4 Reading the result

* Describe what the table shows (for example whether MS/MS coverage rises with detection rate). Do not recommend a prevalence threshold from it; use it as one input to Section 5.3.  
* A low match rate in low-detection bins is expected (low-abundance features trigger fewer MS/MS events). State that this is descriptive and not a quality judgment.  
* Do not interpret annotated compounds biologically (the analysis's boundary).

## 13B.5 What this stage publishes (tables of its own)

| Table | Content |
| :---- | :---- |
| Detection-rate bins | One row per bin: bin, lower and upper rate, features, features with MS/MS, MS/MS rate, features with library match, library match rate (all), library match rate (MS/MS features) |
| Detection-rate cumulative | The ">1% of samples" and ">50% of samples" rows with the same columns, plus the cut-off expressed in number of samples |
| Detection rate per feature | One row per feature in the unfiltered table: row ID, m/z, retention time, samples detected, detection rate, rate per group, bin, `has_ms2`, library match (yes or no), annotation name and source library when matched, in network (yes or no), retained after filtering (yes or no) |

Never merge these into one table or into the per-feature results table. What the stage's procedure states: block `detection_rate` (Section 14).

## 13B.6 Figure (carried into the technical report)

One figure with two panels sharing the bin axis:

* **Left:** stacked bars of the features per bin, split into library match, MS/MS without library match, and no MS/MS; total printed above each bar; graphical legend on the figure.  
* **Right:** grouped bars of the **number of features** per bin (y-axis: "Number of features") with MS/MS and with library match; each bar labeled with its count and, in brackets, the percentage of the bin; graphical legend on the figure.  
* Subtitle: the two cumulative rows (more than 1% and more than 50% of samples) with the features, MS/MS rate and library match rate.  
* Footer (see [REPORT.md](REPORT.md), Section 4, figure standards): the abbreviations used and the samples counted.

## 13B.7 Validate

* Bin counts add up to the number of features in the unfiltered table.  
* The MS/MS count equals the number of `has_ms2` rows; the library count equals the number of distinct library-matched row IDs.  
* The cut-off rows equal the sum of the bins they contain.  
* Table, figure and CSV agree.

---

# 13C. Molecular-Network Analysis

> Companion sections: network files and view names are in [GNPS2-FILES.md](GNPS2-FILES.md) (network rows of the file table and the analysis's file list); detection rates come from Section 13B; the volcano uses the primary results from Section 10; layout and numbering are in [REPORT.md](REPORT.md) (Section 0B and Section 4). Interpretation reads the Section 13C.8 tables ([INTERPRET.md](INTERPRET.md), Sections 3 and 8).

## Objective

Describe the molecular network itself: how many nodes and molecular families it has, which mass differences link nodes next to known compounds, and which compound classes the annotated features belong to, with the classes color-coded and shown with the same colors on the volcano plot. This section is technical and descriptive. It makes no biological claim; the patterns it exposes go to interpretation.

## 13C.1 Availability and default behavior

* **When a molecular network is available, this analysis is a default analysis and runs without being requested, and its results are added to the technical report.** Mention it in the first decision breakdown (with Sections 13A and 13B). The user may switch it off; record that in the decision record.  
* A network is available when the filtered pairs list returns edges (or `prewarm_network_task` reports nodes and edges). If no network was produced, say so in one line, skip this section, and state in the report that no network was available.  
* Row IDs match across the quantification table, library results and network only within the same task. Name the task.

## 13C.2 Inputs

Filtered pairs list (edges with `DeltaMZ`, `Cosine`, `ComponentIndex`; the network stays on the original feature IDs, and approved merges (Section 3.9) are applied through the merge map); the quantification table (for `has_ms2` and sample areas); library search results; the primary results table (effect size, raw p, q) from Section 10; the detection rates from Section 13B; the network parameters from the task page (minimum cosine, minimum matched peaks, library settings).

## 13C.3 Network summary

Report, as a table (Table 2):

* **Nodes:** features with at least one edge.  
* **Edges:** rows of the filtered pairs list.  
* **Molecular families:** connected components (distinct `ComponentIndex` values; confirm the count by recomputing components from the edge list).  
* **Singletons:** MS/MS features with no edge. Before subtracting, confirm that every networked node is an MS/MS feature; if not, say so and count them separately.  
* **Largest family** (nodes), and the family-size distribution in four bins: 2 nodes, 3 to 5, 6 to 20, more than 20.  
* **Annotated nodes:** library-matched features that are networked, and library-matched features that are singletons.  
* Network parameters used (minimum cosine, minimum matched peaks).

## 13C.4 Delta-mass inventory next to known compounds

For every edge, compare the absolute `DeltaMZ` with the table below.

**Rules**

* Tolerance: 0.01 Da by default (the user may change it; record it).  
* Edges with an absolute `DeltaMZ` below 0.1 Da are reported separately as **same-mass pairs** (isomers or near-identical features); they are not counted as assigned or unassigned.  
* Count the remaining edges as **assigned** (one label) or **unassigned**. Report the totals so that same-mass + assigned + unassigned equals the number of edges.  
* For each label report: the number of edges, **one example annotated compound** at one end of an edge (state "none annotated" when neither end has a library match), and a plain-language **explanation** of the mass difference.  
* A mass difference is a candidate relationship, not an identification. Do not infer molecular identity from it (see [INTERPRET.md](INTERPRET.md), Section 8.3).  
* Polyethylene glycol (PEG) steps (44.026 Da, 88.052 Da, and 22.013 Da for doubly charged ions) are flagged as likely polymer contamination and drawn with a hatch pattern.  
* The user may add labels. Record added labels in the decision record.

**Default label table**

| Label | Change | Mass (Da) | Plain-language explanation |
| :---- | :---- | :---- | :---- |
| CH2 | methylation or chain-length step | 14.0157 | One carbon added or removed |
| C2H4O | ethoxy unit | 44.0262 | PEG repeat unit (contamination) |
| H2O | dehydration or hydration | 18.0106 | Water lost or gained |
| H2 | dehydrogenation or saturation | 2.0157 | Double bond formed or reduced |
| C2H4 | ethyl or two-carbon chain step | 28.0313 | Two carbons added or removed |
| O | hydroxylation or oxidation | 15.9949 | One oxygen added |
| 2x C2H4O | PEG | 88.0524 | Two PEG repeat units |
| NH3 | ammonia | 17.0265 | Amine gained or lost |
| C2H4O at z=2 | PEG, doubly charged | 22.0131 | PEG unit seen at charge 2 |
| CH2O | formaldehyde unit | 30.0106 | One carbon and one oxygen |
| C2H2 | unsaturation | 26.0157 | Two carbons, one double bond |
| C4H8 | four-carbon chain step | 56.0626 | Longer or shorter chain |
| C2H2O | acetylation | 42.0106 | Acetyl group added |
| CO2 | carboxylation | 43.9898 | Carboxyl group added or lost |
| SO3 | sulfation | 79.9568 | Sulfate added |
| Gly conjugation | glycine conjugate (C2H3NO) | 57.0215 | Glycine attached |
| Hexose | hexose sugar | 162.0528 | Hexose attached |
| Taurine conjugation | taurine conjugate | 107.0041 | Taurine attached |
| Glucuronic acid | glucuronidation | 176.0321 | Glucuronic acid attached |

## 13C.5 Compound classification of the annotated features

Classify every library-matched feature into a **class group** and a **fine class** (two levels). Unannotated features are not classified.

**Method (record which was used, per feature, in `class_method`)**

1. **Structure-based** when a SMILES or InChI is available and an ontology tool (NPClassifier or ClassyFire) can be run for all features: map the ontology result to the group and fine class below.  
2. **Rule-based** on the annotation name and the source library when structure-based classification is not available or leaves a feature unclassified. Clean the name first (remove collision energies, adduct brackets and library-source suffixes).  
3. List the annotation names that remain unclassified and show them to the user. Do not leave a silent "other".

**Rules**

* Define classes from chemistry and before looking at the volcano. Do not move a feature between classes because of its group result.  
* Class labels describe the annotation chemistry only. They are not a biological claim (the analysis's boundary), and they are as reliable as the library match behind them.  
* Report, per fine class: annotated features, networked, tested in the primary analysis, significant.

**Default scheme (8 groups, 32 fine classes; the user may edit it)**

| Group | Fine classes |
| :---- | :---- |
| Bile acids | Free / keto bile acids; Amino acid–conjugated bile acids; Bile acid–amine/aldehyde adducts |
| Amino acid conjugates & peptides | Di- & tripeptides; N-acyl amino acids; Amine–carbonyl adducts; N-acetyl amino acids |
| Lipids | Oxylipins; Fatty acids & esters; Fatty amides & N-acyl ethanolamines; Acylcarnitines; Glycerolipids & lysophospholipids; Sphingolipids & long-chain bases |
| Diet & plant metabolites | Flavonoids & isoflavones; Piperamides & capsaicinoids; Steroidal alkaloids & saponins; Terpenoids & polyketide natural products; Phenylpropanoids & polyphenols; Vitamins & cofactors |
| Drugs & agrochemicals | Antimicrobials & agrochemicals; Anti-inflammatory & steroid drugs; Other drugs & drug-like |
| Small host & microbial metabolites | Amino acids & derivatives; Purines & nucleosides; Sugars & glycosides; Polyamines & acetylated amines; Indoles & tryptophan metabolites; Tetrapyrroles |
| Contaminants & additives | PEG & polymer additives; Surfactants, plasticizers & other additives |
| Synthetic & unclassified | Synthetic heterocycles & screening-library entries; Other annotated (unclassified) |

## 13C.6 Class colors (one key for every figure and CSV)

* **One hue per group, one shade per fine class** (darkest first within the group) and **one marker shape per fine class** (circle, square, triangle, diamond, inverted triangle, plus, cross, hexagon, in that order within a group). Shape is required as the second encoding.  
* Default group hues: Bile acids `#eb6834`; Amino acid conjugates & peptides `#2a78d6`; Lipids `#1baf7a`; Diet & plant metabolites `#8e5bd0`; Drugs & agrochemicals `#d1478f`; Small host & microbial metabolites `#b8860b`; Contaminants & additives `#6b6a66`; Synthetic & unclassified `#8a5a3b`. Unannotated features: light gray `#c9c8c2`. Only the first three hues were checked for color-vision deficiency; for the others, rely on shape and the group label, and do not use color alone.  
* These are **class colors**, separate from the group (comparison) colors asked for at intake in [REPORT.md](REPORT.md). Do not reuse a class hue as a comparison-group color in the same figure.  
* Write `class_group`, `fine_class`, `class_color` and `class_marker` into the CSV files so every later figure reuses them.

## 13C.7 Volcano plot by class

Built from the primary results (Section 10): x-axis the effect size on the primary scale (default log2 fold change), y-axis the negative log10 of the raw p-value.

* Draw each **annotated, tested** feature with its fine-class color and marker. Faded dot = not significant; **larger dot with a ring = more significant** (p below 0.05: plain; below 0.01: thin dark ring; below 0.001: thick black ring). Draw labeled horizontal lines at p = 0.05, 0.01 and 0.001 and vertical lines at the effect-size cut-off. Do not use background shading or density contours for p-values.  
* **Significance cut-off:** default raw p below 0.05 and an absolute log2 fold change of at least 0.58 (1.5-fold), unless Section 10 set another rule. State the cut-off on every page that uses the word "significant". Always state whether multiple-testing correction was applied and give q in the table.  
* Features not annotated are not drawn; state in the caption how many unannotated features were tested and how many were significant.  
* Label the most significant feature of each group with its **full feature name and raw p-value**.  
* Two versions: an **overview** (all classes, one legend listing every fine class with tested and significant counts) and a **faceted version** (one panel per group, fine classes as shades and shapes).  
* Graphical color key for classes and a graphical p-value key (dot size and ring) on the figure; the group sizes (n) and the comparison direction on the axes ("higher in A / higher in B").

## 13C.8 What this stage publishes (tables of its own)

| Table | Content |
| :---- | :---- |
| Network summary | The Table 2 rows: nodes, edges, families, singletons, largest family, annotated networked and singleton, parameters |
| Network family sizes | Family-size bins and counts |
| Network families | One row per molecular family: family ID, nodes, annotated nodes, edges, group with most annotated members, significant members |
| Network nodes | One row per MS/MS feature: row ID, family ID (blank for singletons), degree, annotation name and source library, `class_group`, `fine_class`, `class_method`, `class_color`, `class_marker`, detection rate, effect size, raw p, q, significant flag |
| Network edges | One row per edge: node 1, node 2, cosine, `DeltaMZ`, delta label (blank when unassigned), status (assigned, same-mass, unassigned) |
| Network delta masses | The inventory: label, mass, edges, example annotated compound, explanation, PEG flag; plus the three totals |
| Compound-class assignments | One row per annotated feature: row ID, annotation, source library, SMILES when present, group, fine class, method |
| Compound-class composition | One row per fine class: annotated, networked, tested, significant |
| Compound-class color key | One row per class: group, fine class, color, marker (Section 13C.6) |

Never merge these into one table or into the per-feature results table. What the stage's procedure states: block `molecular_network` (Section 14).

## 13C.9 Figures (carried into the technical report)

1. **Family sizes:** bars of the family-size bins and a summary box (nodes, edges, families, singletons, largest family).  
2. **Delta-mass inventory:** horizontal bars per label with the example annotated compound beside each bar; PEG labels hatched.  
3. **Class composition:** annotated features per fine class, grouped by group, solid for networked and pale for singletons, with tested and significant counts. This is the master class color key.  
4. **Volcano by class, overview** (Section 13C.7).  
5. **Volcano by class, faceted** (Section 13C.7).

An optional figure of example families colored by class may be made on request; it is not part of the standard report.

Every figure page carries a footer that defines the abbreviations used **on that page** and the significance cut-off (see [REPORT.md](REPORT.md), Section 4, figure standards).

## 13C.10 Validate

* Nodes + singletons equals the number of MS/MS features.  
* Same-mass + assigned + unassigned edges equals the number of edges; the delta table sums to the assigned count.  
* Component count from the edge list equals the number of distinct `ComponentIndex` values.  
* Annotated features per fine class sum to the number of library-matched features; tested and significant counts match the primary results table.  
* Table, figures and CSV files agree.

## 13C.11 Boundaries

Report counts, structure, mass differences, class membership and statistics only. Do not discuss what a class, family or mass difference means biologically; flag coherent families and classes in the areas-of-interest list (Section 17.3) using neutral feature-level language, and leave interpretation to interpretation.

---

---

# 14\. What Each Stage Records

Every stage's Analysis states, in its `procedure`, what the block below lists for it. A block is one stage; where the reuse table groups several stages into one Analysis, its procedure carries each of their blocks. `dataset` and `experimental_design` are stated once, in the first Analysis of the run, and the goal carries the question.

Record each field as it is decided, in the working file, so a run that stops loses none. Where a field does not apply, say so and why; an absent field reads as one nobody considered.

```yaml
dataset:
  name:
  version:
  input_files:

experimental_design:
  primary_comparison:
  independent_samples:
  repeated_measures:
  batches:
  covariates:

qc:
  pooled_qc_available:
  number_pooled_qcs:
  qc_metric:
  qc_data_state:
  qc_filtering:
  qc_threshold:
  drift_assessment:
  excluded_qcs:
  qc_status_reproducibility:
  qc_status_drift_batch:

internal_standards:
  provided_by_user:
  standards:
  matching_ppm:
  status_per_standard:
  rt_range_min:
  split_standards:
  used_for_normalization:

feature_merge:
  enabled:
  ppm_window:
  rt_window_min:
  candidate_pairs:
  recommended:
  review:
  do_not_merge:
  user_decision:
  merges_applied:
  area_rule:
  validation_passed:

batch_correction:
  check_run:
  sequence_files_source:
  batch_definition:
  qc_injections_excluded:
  input_already_corrected:
  source_tool_and_settings:
  method: QCRSC
  citations:
  script_version:
  selftest_passed:
  eligible_features:
  features_total:
  share_affected_raw:
  median_batch_r2_raw:
  share_shift_ge_1_2:
  share_drift_flag:
  recommendation:
  user_decision:
  corrected:
  corrected_on: full unfiltered table
  features_corrected_yes:
  features_corrected_partial:
  features_not_corrected:
  heldout_share_affected_after:
  heldout_median_qc_rsd_before:
  heldout_median_qc_rsd_after:
  features_significantly_worse:
  reverted_features:
  correction_worked:
  group_by_batch_confounded:
  thresholds_source: calibrated on one dataset
  validation_passed:

blank_filter:
  enabled:
  method:
  threshold:
  blank_type:
  data_state:

prevalence_filter:
  enabled:
  threshold:
  scope:
  metadata_aware:

missing_values:
  representation:
  filtering:
  imputation:

normalization:
  input_state:                 # raw | already_normalized | unknown
  method:
  normalization_factor:
  data_state:
  methods_compared:

normalization_comparison:      # required in every run, even when not run
  status:                      # run | not_applicable_input_already_normalized | user_switched_off
  reason_if_not_run:
  raw_table_requested:         # yes/no, and the user's answer
  user_specified_method:       # none, or the method the user named
  candidates:
  diagnostics:
  recommendation:
  user_choice:
  method_applied:
  methods_disagree:            # yes/no, with the cause if yes (normalization itself or a coupled step)

transformation:
  method:
  parameters:

scaling:
  method:
  parameters:

outliers:
  assessment:
  excluded_samples:
  rationale:

statistics:
  scientific_question:
  primary_model:
  covariates:
  multiple_testing:
  effect_size:
  confidence_intervals:

sensitivity:
  analyses_performed:
  findings_affected:

unfiltered_parallel_table:
  enabled:
  features_in_input:
  features_retained:
  features_removed:
  normalization_factors_source:
  operations_applied_identically:
  deviations:
  validation_passed:
  unfiltered_family_q_method:

detection_rate:
  enabled:
  samples_counted:
  zero_treated_as_not_detected:
  bins:
  features_gt_1pct_samples:
  features_gt_50pct_samples:
  ms2_rate_gt_1pct:
  library_match_rate_gt_1pct:
  ms2_rate_gt_50pct:
  library_match_rate_gt_50pct:
  validation_passed:

molecular_network:
  available:
  enabled:
  source_task_id:
  nodes:
  edges:
  families:
  singletons:
  delta_mass_tolerance_da:
  classification_method:
  significance_rule:
  validation_passed:
  not_available_reason:

removed_feature_review:
  performed:
  features_flagged:
  user_decision:

provenance:
  skill_version:
  analysis_date:
  code_version:
```

&nbsp;

A study may need fields this list does not have; add them.

A procedure states what was **actually executed**, not merely what was recommended, and for each decision who made it: the user, or a recommendation the user accepted.

---

# 15\. Post-Analysis Review of Filtered-Out Features

## Objective

After the final analysis, check which features were removed by filtering and flag any that may be biologically important and should not have been removed. This review is flag-only: it raises candidates for the user to review and does not interpret their biology.

## 15.1 Compile

Use the preserved pre-filter feature list (with each filter's result) and the parallel unfiltered table and results (Section 13A) to list every removed feature, the filter that removed it, and its annotation (tier or class), abundance, prevalence by group, and blank/QC metrics.

## 15.2 Assess

* Annotated features removed, by filter and by annotation tier or class. Flag disproportionate removal of chemical classes, tiers, abundance ranges, or sample groups.  
* Features expected to matter from the study context: compounds implied by the metadata (for example medications), positive controls, and markers named in the study background or literature. Check whether each was retained.  
* Group signal among removed features: take the group statistics of removed features from the parallel unfiltered results (Section 13A), which use the same normalization, transformation, model, and effect-size measure as the primary analysis. Report this as exploratory and outside the multiple-testing family, and interpret it knowing that the filters (for example prevalence) change what can be detected.  
* Features removed by rules that are fallible by design (for example in-source-fragment or blank flags) that carry high-confidence annotations or strong group effects.  
* Where one filter's removals look suspicious, check the underlying evidence (for example co-eluting parent ions for fragment flags, or intensity in blanks) before judging.

## 15.3 Report and decide

Produce a list of features that may have been removed incorrectly, with the evidence and the filter responsible. Do not silently re-add any feature. Ask the user whether to add specific features or rules back, and if so rerun the affected steps and record the change. Summarize the result in the final report even when nothing is flagged.

---

# 16\. The Technical Report

At the end of the analysis, draft the technical report as [REPORT.md](REPORT.md) sets out, show it to the user, and stop. It is published, and its file built, once the user has approved it.

The report opens with the question, verbatim, followed directly by the plain-language summary (technical only, no biology or literature). It then contains:

* Summary of findings and cautions (the Key technical takeaway and the findings table)  
* Study design and data, including preprocessing history, data representation, and available QC and blanks  
* Decision workflow table: the executed choice for each decision and who made it  
* QC assessment, including the Section 3.7 classification  
* Filtering, with feature counts and the effect on annotated features  
* Parallel unfiltered table: the operations applied, the validation (Section 13A.6), and a summary of the unfiltered results, labelled as such  
* Internal-standard check (Section 3.8), or a line saying no standards were provided  
* Feature-merge recommendation (Section 3.9): candidate counts, class counts, example review sheets, and the merges the user approved  
* Batch and drift correction (Section 3.10): the check result and decision, the method with its citations, the held-out validation, the four figures, and the numbers of features corrected, partly corrected and not corrected; or the reason the step was skipped  
* Detection-rate bins with MS/MS and library match rates (Section 13B): Table 1 and its figure  
* Molecular-network analysis (Section 13C): network summary table, family sizes, delta-mass inventory, compound-class composition, and the volcano plot by class (overview and faceted), or a one-line statement that no molecular network was available  
* Normalization comparison, the chosen method, and its validation. This line is always present: if the comparison was not run, state that and why (input already normalized, or switched off by the user) and name the normalization that was used, if any  
* Results with effect sizes, confidence intervals, raw p-values, and adjusted q-values  
* Sensitivity analyses and labels  
* Post-analysis review of removed features (Section 15\)  
* Limitations  
* Open items, recommended next steps, and areas of potential interest for follow-up (Section 17\)  
* Deviations from this framework and their status  
* Appendix: parameters, software versions, random seeds, and the list of what was published

Include figures where they aid interpretation (for example QC, filtering, normalization, key results, sensitivity). The report must describe what was executed and agree with what each stage's procedure states.

Report results descriptively. Leave biological interpretation (pathways, mechanisms, literature comparison, molecular-family context) to [INTERPRET.md](INTERPRET.md).

---

# 17\. The Hand-Off Note and Next Steps

## Objective

Give interpretation everything it needs, and make explicit what is unresolved. Sections 17.1 to 17.3 are published together as one hand-off note; it orients a reader and nothing is argued from it. This section stays technical and statistical and makes no biological claims.

## 17.1 Open items

List the pending decisions and unresolved limitations from this run, each with the evidence behind it (for example confounding, unassessed drift, gap-filled data, pending add-back decisions, groups too small to assess).

## 17.2 Recommended next steps

List recommended technical and statistical follow-up analyses. Each one must:

* Be tied to a documented limitation, open decision, or diagnostic from this run, and state that trigger.  
* Be a statistical or data-quality action (for example a covariate-adjusted model, a stratified comparison, a threshold sensitivity analysis, a rerun after an add-back decision).

These are recommendations only. None runs without the user's approval. Do not include biological follow-up (pathways, mechanisms, literature comparison, validation experiments); that belongs to interpretation.

## 17.3 Areas of potential interest for follow-up

List patterns that stood out during the run and may merit further investigation by interpretation. Examples include groups of features with strong, robust differences, features tied to a metadata variable, and features that behaved unexpectedly under filtering, QC, or normalization.

* Describe each by what the data show: feature identifiers, annotation tier, effect sizes, robustness labels, and why it stood out.  
* Point to the table or file that holds the evidence.  
* Do not explain the biology, rank the areas, or combine them into a score. Interpretation decides what to pursue.

## 17.4 What the library holds when the analysis is published

Interpretation starts from the library's record, so what the analysis publishes is what interpretation has. Publish, each as the output of the stage that produced it:

* The per-feature results table (effect sizes, confidence intervals, raw p-values, adjusted q-values, annotation tier and name, flags, sensitivity labels), not sorted by any priority score.  
* The filter table for every feature (result of each filter, QC CV, blank ratio, prevalence, rescue flag), the removed-feature review, and the flagged-feature list.  
* The metadata-driver and other diagnostic tables.  
* The **processed unfiltered feature table** (all input features, same samples, same normalization, imputation, and transformation as the filtered table), the **processed filtered feature table**, and the **unfiltered per-feature results table** (same columns as the primary results, plus retained flag, every filter that removed the feature, detection counts per group, imputed fraction, detected-only effect size, and the labelled unfiltered-family q), not sorted by any priority score.  
* The validation record for the two tables (Section 13A.6).  
* The **sample table**: one row per sample with its group, subject, time point, batch and every covariate a model used.  
* The **internal-standard check** (Section 3.8.6), or a statement that no standards were provided.  
* The **feature-merge tables and review sheets** (Section 3.9.7).  
* The **batch-correction tables** (Section 3.10.7): the raw and the corrected tables, the corrected unfiltered table, and the `batch_corrected` flag in the per-feature tables; or the check result when correction was skipped, not possible, or the input was already corrected.  
* The **detection-rate tables** (Section 13B.5).  
* The **molecular-network tables** and the class color key (Sections 13C.6 and 13C.8), or a statement that no network was available.  
* **Each input the analysis used**, as its import ([GNPS2-FILES.md](GNPS2-FILES.md)): the feature table, MGF, pairs list, GraphML, metadata, sequence files, internal-standard list, and whatever else the user supplied. The source information a later reader needs — the GNPS2 task ID and host, and where the feature table, MS/MS spectra and molecular network are retrieved — is what those imports state.  
* **The question**, verbatim, as the goal.  
* **Figures:** every figure has a 1 to 2 sentence "How to read this figure" line, in plain language (what the axes, colors, symbols or bars mean and what to look for; no result stated), in the conversation, in the technical report and in the description the figure is published with ([REPORT.md](REPORT.md), Section 4, Figures). Applies to the detection-rate, molecular-network, internal-standard, feature-merge, batch-correction, normalization and QC figures alike.  
* The code that generated each result, with the stage it carried out.  
* **The hand-off note** (Sections 17.1 to 17.3), and the technical report.

A table a reader can read is embedded. A larger one is described — its rows, its columns, how many of each, how a row is addressed — and held as a file. Which tables a finding will turn on is not known yet, so none of a large table's rows is embedded here.
