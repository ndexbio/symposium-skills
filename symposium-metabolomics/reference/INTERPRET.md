# AI-Assisted Biological Interpretation of Metabolomic Data

You arrive here with the library community, the analysis in it to interpret, the interpretation
community, and the question. You leave with every pattern evaluated, the findings the user chose
pursued, challenged and refined in the run's folder, and draft reports ([REPORT.md](REPORT.md)).
Nothing is published until the user approves those drafts.

The analysis is read from the library's record, as its publisher left it: the question it
served, each stage's procedure, the result tables, the hand-off note and the technical report.
[ANALYZE.md](ANALYZE.md) says what each of those holds.

## Purpose

This document sets out biological interpretation of metabolomic data following completion of the analytical decision-making and statistical analysis workflow.

The goal is not simply to identify significant metabolites or assign pathway names. The goal is to identify, investigate, and contextualize **biologically meaningful patterns** emerging from:

* statistical results  
* molecular networking / FBMN structure  
* annotated and unannotated features  
* molecular families  
* coordinated changes across chemically distinct features  
* sample metadata  
* repository-level evidence  
* peer-reviewed literature  
* known biochemical and physiological relationships

The skill should reason from individual observations toward broader biological patterns while remaining explicit about the strength and limitations of the evidence.

Potential interpretations may range from well-established biology to plausible but incompletely established mechanisms to highly exploratory hypotheses.

The skill must never present an AI-generated hypothesis as an established biological conclusion.

---

# 0\. Operating Rules (read first)

These rules apply to every response, not only the final report.

1. **Biological interpretation is the point of every response.** Each finding is presented as what it might mean biologically, what could cause it, and what it could lead to (see Section 24A). Statistics support the biology and are shown in one compact line; they do not lead.  
2. **Run Intake before any analysis** (Section 3A). Do not begin until the user has accepted or changed the defaults.  
3. **Review what filtering removed** (Section 4A) before interpreting, using the unfiltered table and results the analysis published. Filtering decisions are never changed silently.  
4. **Pause after the first scan.** The first output is the evaluation of all emerging patterns, summarized clearly with one or two summary figures, not a report (Section 5A). Do not cap the number of patterns.  
5. **Do not limit interpretation to FDR-passing features.** Raw p-values and trends count as evidence, labelled by tier (Section 6A). Always report the raw p-value and the q-value together.  
6. **Coherent direction is evidence.** If most members of a network component, molecular family,  biological class, or metabolic pathway move the same way, investigate it even when few or no members are individually significant.  
7. **Every response ends with "Things I need from you":** recommendations plus questions.  
8. **Never repeat a question the user has already answered**, and do not re-raise items the user has parked or deferred. Record them in the working file (Section 3A).  
9. **Show key figures in chat.** Every pattern or finding discussed in chat comes with its key figure, rendered inline, so the user sees the result as it is discussed and not only in the final reports (Section 24B).  
10. **State the biological interpretation and hypotheses unprompted, every time**, in chat and in both reports: what it might mean, possible causes, possible consequences, and the competing explanations. The user should never have to ask for them. Put the interpretation first (directly under the finding's heading), not at the end.  
11. **Look at every class at more than one level.** Test a broad class and its sub-classes (for example all fatty acids and medium-chain fatty acids; all acylcarnitines and oxidized acylcarnitines). A signal that is diluted at the broad level is often sharp at the narrow level (Section 7A).  
12. **When a finding needs dietary-intake or medication information that the user does not have, recommend the MetaboApps DrugReadout and FoodReadout** (Section 13A).  
13. **Deliver two reports:** a short main report with the key findings and a full report (Section 31).  
14. **Answer the three molecular-network discovery questions with the emerging patterns, once the user has approved this default at intake**, against the question (in the user's words, verbatim): what is most interesting in the molecular network in relation to it, what is most unexpected in the molecular network in relation to it, and what is more interesting in the molecular network that is not relevant to it. Do this in the Phase 1 checkpoint and in both reports (Section 5B). Skip with a one-line note if no network is available.

---

# 1\. Scope

This skill begins **after** the analytical decision-making skill has completed its workflow.

The analytical skill determines:

> **What does the dataset robustly show?**

This biological interpretation skill determines:

> **What biological processes, states, mechanisms, or exposures could explain the observed patterns, and what evidence supports those interpretations?**

The biological interpretation skill should not silently modify the analytical workflow, statistical results, filtering decisions, normalization, or experimental design.

However, biological interpretation may reveal questions that cannot be answered using the existing analytical output. In these cases, the skill may **propose additional analyses**.

Additional analyses follow an explicit user-controlled loop:

> **Identify information gap → propose analysis → explain rationale → obtain user approval → execute → record result → incorporate evidence → refine hypothesis**

The skill must not automatically perform new analyses without user approval.

---

# 2\. Core Principles

## 2.1 Interpret patterns, not just metabolites

The primary unit of interpretation is a **biological pattern**, not an individual statistically significant feature.

Individual metabolites may provide evidence for a biological interpretation, but broader patterns should be actively sought across multiple patterns, including but not limited to:

* individual features  
* molecular families  
* chemical classes  
* chemically related but differently annotated features  
* unannotated network nodes  
* multiple molecular families  
* metabolic pathways  
* coordinated abundance changes  
* metadata associations  
* cross-cohort recurrence  
* repository recurrence

A biological interpretation may therefore emerge even when no single metabolite provides definitive evidence.

---

## 2.2 Unannotated features are evidence

Unannotated features must not automatically be discarded from biological interpretation.

An unknown feature can provide useful evidence based on:

* molecular-network position  
* MS/MS similarity  
* neighboring annotations  
* molecular-family membership  
* mass differences  
* homologous relationships  
* coordinated abundance changes  
* metadata associations  
* recurrence in public datasets  
* association with annotated features  
* chemical context

The skill should explicitly search for biologically informative **unknowns**.

For example:

> Unknown feature → molecular family → chemically related annotated metabolites → coordinated phenotype association → biological hypothesis

The inability to determine a definitive molecular structure does not mean that the feature has no interpretive value.

The skill may attempt to determine structures for unknowns. This is encouraged when it can be supported, using:

* MS/MS fragmentation, including diagnostic fragments and neutral losses shared with annotated relatives  
* spectral-library matches, including partial or analog matches  
* molecular-formula prediction (for example BUDDY or SIRIUS), reporting rank and estimated FDR  
* mass differences to annotated network neighbors  
* retention-time behavior relative to related features  
* in silico structure prediction

Every proposed structure must be reported with its evidence basis, a confidence level (for example the annotation level the analysis used), and the plausible alternatives. A formula-only match is not a structure. The skill must not adopt a structure merely because it would make a biological interpretation more coherent, and must not carry a tentative structure forward as if it were identified. Features with no supporting evidence remain explicitly labelled as unknowns.

---

## 2.3 Do not restrict interpretation to chemical classes

The skill should not limit biological interpretation to statements such as:

* altered lipid metabolism  
* altered amino-acid metabolism  
* altered bile acids

Instead, it should actively search for **higher-order biological patterns** that may span multiple chemical classes.

Examples include but are not limited to:

* inflammation  
* immune activation  
* oxidative stress  
* cellular stress  
* altered nutrient availability  
* dietary exposure  
* microbial metabolism  
* altered host–microbe interactions  
* tissue injury  
* altered energy metabolism  
* altered lipid remodeling  
* xenobiotic exposure  
* medication effects  
* hormonal signaling  
* psychological stress  
* intestinal barrier dysfunction  
* hypoxia  
* altered proliferation  
* detoxification

These are hypotheses to investigate, not labels to assign automatically.

The skill should also be capable of identifying biological patterns that are not represented in any predefined list.

---

## 2.4 Use bottom-up and top-down reasoning

Biological interpretation should proceed in both directions.

### Bottom-up reasoning

Start with observations:

> Feature → molecular family → chemical pattern → metabolic process → biological process → physiological phenotype

### Top-down reasoning

Start with a possible biological pattern:

> Candidate biological process → predicted metabolomic consequences → search the dataset/FBMN for supporting or contradictory evidence

The two approaches should converge.

A biological interpretation should become stronger when a proposed process predicts additional observations that are actually present in the dataset.

---

## 2.5 Distinguish observation from interpretation

Every biological finding should distinguish:

### Observation

What is directly supported by the analytical output.

### Interpretation

What biological process might explain the observation.

### Evidence

Why the interpretation is reasonable.

### Uncertainty

What remains unresolved.

The skill must never collapse these four categories into a single statement of fact.

---

## 2.6 Biological interpretation is iterative

The skill should not operate as a single pass from statistical results to narrative.

A biological hypothesis may reveal a question requiring:

* additional FBMN interrogation  
* additional literature searches  
* repository searches  
* examination of existing metadata  
* a new statistical analysis  
* a targeted feature analysis  
* cross-cohort analysis  
* structural annotation  
* another form of computational investigation

The skill should therefore maintain an explicit iterative investigation loop.

---

# 3\. Inputs

Read everything the analysis published in the library, and work from the library's own tables. A table the library holds as a file is fetched into the run's folder; nothing is recomputed that the analysis already computed.

Required inputs include:

* processed feature table  
* feature identifiers  
* sample metadata  
* statistical results  
* effect sizes  
* p-values  
* multiple-testing results  
* model information  
* covariate-adjusted results where available  
* sensitivity analyses  
* unfiltered processed feature table (all input features, same samples, same normalization, imputation, and transformation as the filtered table; [ANALYZE.md](ANALYZE.md), Section 13A)  
* unfiltered per-feature results (same model as the primary results, with retained flag, filters that removed each feature, detection counts per group, imputed fraction, detected-only effect size, and the labelled unfiltered-family q)  
* removed-feature review  
* normalization/transformation decisions  
* QC findings  
* filtering decisions  
* technical limitations  
* molecular networking / FBMN outputs  
* the **question** the analysis served, verbatim, from its goal; and the question the user asked when requesting interpretation, which is the reference for the discovery questions (Section 5B)  
* the **internal-standard check** and the **feature-merge tables** ([ANALYZE.md](ANALYZE.md), Sections 3.8 and 3.9), when they exist; if merges were applied, feature IDs in the results are the representative IDs and the merge map gives the original IDs  
* the **batch-correction tables** ([ANALYZE.md](ANALYZE.md), Section 3.10.7) and the `batch_corrected` flag in the per-feature tables, when batch correction was run; features flagged `no`, `partial` or `reverted` are not fully corrected and are described that way, and the corrected unfiltered table comes from the same run
* the **detection-rate tables** ([ANALYZE.md](ANALYZE.md), Section 13B.5) and the **molecular-network tables** with the compound-class color key ([ANALYZE.md](ANALYZE.md), Sections 13C.6 and 13C.8), when they exist  
* feature annotations  
* annotation confidence/tier  
* GNPS2 task information  
* relevant source files or task identifiers  
* each stage's procedure (the decisions made, by whom, with what parameters)  
* the hand-off note and the technical report

Optional inputs may include:

* SIRIUS annotations  
* predicted molecular formulas  
* in silico structural annotations  
* MS/MS spectra  
* MassQL results  
* MASST results  
* ReDU results  
* additional cohorts  
* validation datasets  
* targeted measurements  
* external biological metadata

The skill should first determine what information is actually available rather than assuming every input exists.

---

# 3A. Intake and Standing Preferences

Before any analysis, state the defaults below in a short block and ask the user whether they are acceptable. Ask once. Record the answers in the working file and apply them for the rest of the run, across sittings, without asking again.

**Defaults to confirm**

| Setting | Default |
| :---- | :---- |
| Audience | General scientific audience |
| Role of uploaded or cited papers | Context only; the goal is biology not already reported in them |
| Acceptable sources | Any source, always cited |
| Additional analyses | Proposed in groups, one approval per group |
| Covariate adjustment and stratification | Never without explicit approval; within-cohort correlations and descriptive sub-comparisons are labelled exploratory |
| Single-feature evidence | Raw p \< 0.05 (q always shown) |
| Family / network / class trend evidence | Raw p \< 0.1 (q or family count always shown) |
| Emerging patterns in the first scan | **All** patterns the scan finds are evaluated (no cap), then summarized clearly in chat with one or two summary figures (Section 5A) |
| Molecular-network discovery questions (Section 5B) | **On**, delivered with the emerging patterns; three questions about the network, against the question, up to 3 items each. **Ask the user to approve this default.** |
| Unannotated features | Structures may be proposed with evidence and confidence |
| Report restrictions | None (for example, an option to include only features with MS/MS in a highlights report) |
| Key figures in chat | On: one key figure per pattern or finding discussed |
| Reports | Two: short main report (key findings) and full report |
| Report format | PDF, built from the report once it is accepted ([REPORT.md](REPORT.md)) |
| Main report length | 8 to 12 pages recommended; **ask the user** |
| Null results in the main report | Not included; included only if the user requests them (always included in the full report) |
| Group colors in figures | **Ask the user** (no fixed convention); keep the chosen colors for the whole session and both reports |
| Class depth | Broad class plus sub-classes (Section 7A) |
| Diet and medication gaps | Recommend DrugReadout and FoodReadout when intake data are missing |
| Items to defer or park | None |

&nbsp;

Ask the user explicitly, in this same intake and before any figure or report is made, whether 8 to 12 pages is acceptable for the main report, whether any null results should appear in the main report, and which colors to use for the groups. Do not assume answers; record them in the log. Ask also whether they approve the molecular-network discovery questions (Section 5B) as a default alongside the emerging patterns, and whether 3 items per question is right. Tell them that every emerging pattern the scan finds will be evaluated (no cap on the number) and then summarized, and ask only whether any area should be left out. Ask also whether the p-value thresholds above are acceptable, and whether they want to limit to features with MS/MS (recommended). If applicable, ask the user if they want to focus on adjusted or unadjusted data first, or look at both at the same time.

If the user changes a default, update the working file. If the user parks or defers an item, do not raise it again unless the user does.

---

# 4\. Reading the Analysis

Before interpreting biology, read what the analysis published.

Determine:

1. What was measured?  
2. What is the experimental question?  
3. What groups or phenotypes are being compared?  
4. What statistical models were used?  
5. Which features survived filtering?  
6. Which features are statistically associated with the primary question?  
7. Which associations are robust to sensitivity analyses?  
8. Which metadata variables explain substantial variation?  
9. Which findings change after covariate adjustment?  
10. What molecular-network information is available?  
11. Which features are annotated?  
12. Which features are unannotated?  
13. What technical limitations remain?  
14. Which conclusions are explicitly unsupported by the analytical workflow?  
15. Did the analysis publish the unfiltered table and its results, and did the validation pass (same samples, retained values identical, same operations)?  
16. Which filters removed the most features, and which removed features have a notable pattern in the unfiltered results?
17. Did the analysis publish the detection-rate and molecular-network tables ([ANALYZE.md](ANALYZE.md), Sections 13B and 13C: tables, class color key)? If no network was available, say so. Were feature merges applied (Section 3.9), and is the merge map published? Were internal standards provided and checked (Section 3.8)? Was batch correction run, skipped after a check, or supplied already corrected (Section 3.10), and does every per-feature table carry the `batch_corrected` flag?
18. What is the question? Quote it; it frames the molecular-network discovery questions (Section 5B).
19. What does the interpretation community already hold that rests on this analysis? List each finding there with its features or families and its direction; the overlap table (Section 5A) is drawn against this list.

Do not begin biological interpretation until the skill understands the analytical context.

---

# 4A. Filter-Loss Review

Filtering decisions made upstream (prevalence, retention-time window, blank ratio, in-source-fragment flag, intensity, replicate filters) can remove important biology. Before interpreting, review what each filter removed.

This is a **read-only review**. It does not change the analytical workflow. It is not a "new filtering decision" under Section 13\.

**Source of the statistics.** Use the unfiltered processed table and its per-feature results as the analysis published them ([ANALYZE.md](ANALYZE.md), Section 13A). They were produced with the same normalization, transformation, and statistical model as the retained features, so retained and removed features are directly comparable. Do not re-normalize or re-model. If the library lacks them, say so and ask the user whether to return to the analysis to produce them (recommended). As a read-only fallback only, compute the statistics using the same per-sample normalization factors, and label them as such.

**For each filter:**

* read the group statistics (effect size, raw p, direction) for the removed features from the unfiltered results  
* identify removed features that are directional, coherent within a molecular family or network component, or annotated to known biology  
* identify removed features that belong to families whose retained members show a signal

**Specifically look for:**

* **Asymmetric presence.** A feature detected in one group and rarely in the other fails a prevalence rule in the group where it is absent, even though its presence or absence is the signal. Compare detection counts per group (the per-feature detection rates are in the detection-rate table per feature, [ANALYZE.md](ANALYZE.md), Section 13B.5), and report detected-only effect sizes separately from all-sample effect sizes.  
* **Retention-time edges.** Early-eluting polar compounds and late-eluting lipids are often excluded by the RT window.  
* **In-source-fragment flags.** Flagged features may still carry real biology (for example a true metabolite flagged as a fragment of another ion). Check those with MS/MS before accepting the flag.  
* **Blank-ratio exclusions.** Features removed for a high blank ratio may still be endogenous at lower levels; report them as uncertain rather than discarding.

**Report** a short table: filter, number removed, number of removed features with a notable pattern, and the most biologically relevant examples. Features that would change an interpretation are written up as a proposal to add them back (Section 14). The user approves. Rescued features are always labelled as rescued, and the original retained set is never altered. Removed features are outside the primary multiple-testing family: report their raw p with the labelled unfiltered-family q the analysis published, label them exploratory, and never merge them into the primary q.

---

# 5\. Core Iterative Workflow

The core workflow is:

```
INTAKE: CONFIRM DEFAULTS WITH USER (Section 3A)
        ↓
READ THE ANALYSIS
        ↓
FILTER-LOSS REVIEW (read-only, Section 4A)
        ↓
IDENTIFY INTERESTING SIGNALS (raw p and trends included, Section 6A)
        ↓
PHASE 1 CHECKPOINT: ALL EMERGING PATTERNS EVALUATED, SUMMARIZED WITH SUMMARY FIGURES + THREE MOLECULAR-NETWORK DISCOVERY QUESTIONS (if approved), THEN PAUSE (Sections 5A and 5B)
        ↓
USER SELECTS PATTERNS TO PURSUE
        ↓
IDENTIFY INTERESTING SIGNALS
        ↓
GROUP SIGNALS INTO BIOLOGICAL / CHEMICAL PATTERNS
        ↓
INTERROGATE FBMN
        ↓
GENERATE BIOLOGICAL HYPOTHESES
        ↓
SEEK LITERATURE / REPOSITORY EVIDENCE
        ↓
CHALLENGE HYPOTHESES
        ↓
IDENTIFY INFORMATION GAPS
        ↓
 ┌───────────────────────────────────────┐
 │ Is existing information sufficient?   │
 └───────────────────────────────────────┘
          ↓ NO                 ↓ YES
   PROPOSE ADDITIONAL       REFINE /
       ANALYSIS             PRIORITIZE
          ↓
   EXPLAIN RATIONALE
          ↓
   ASK USER APPROVAL
          ↓
   EXECUTE APPROVED ANALYSIS
          ↓
   RECORD RESULT
          ↓
   INCORPORATE NEW EVIDENCE
          ↓
   REFINE HYPOTHESIS
          ↓
   RETURN TO FBMN / EVIDENCE
          ↓
   REPEAT UNTIL STOPPING CRITERIA
          ↓
FINAL EVIDENCE-WEIGHTED INTERPRETATION
```

&nbsp;

The skill should be able to move backward through this workflow whenever new evidence creates a new question.

**Iteration is a core feature of the skill, not an optional extension.**

---

# 5A. Phase 1 — Emerging Patterns Checkpoint

The first output of an interpretation is **not a report**. It is a clear summary of **all** emerging patterns, each evaluated, followed by a pause. There is no default cap on the number of patterns and no pre-selection of the "best" ones.

**Before and during the scan**

* State in plain language what is about to be run (for example: filter-loss review, family-level direction tests, network-component checks, formula and annotation review, background literature checks).  
* Do not run a long hidden analysis. If a step takes a long time, say what it is.

**What the scan includes**

* the filter-loss review (Section 4A)  
* feature-level and family-level screening using the tiers in Section 6A  
* coherent-direction checks within network components and chemical or biological classes  
* informative unknowns (Section 2.2)  
* targeted literature searches to test the emerging patterns against known biology (cited inline)

**What the output is**

**Evaluate every emerging pattern.** Collect every pattern the scan surfaces (from the feature-level and family-level screening, the coherent-direction checks, the informative unknowns and the filter-loss review). Give each a pattern ID (P1, P2, ...) and run the same evaluation on all of them: the evidence in brief, the evidence tier (Section 6A), the biological meaning, a targeted literature check and the competing explanations. Do not drop a pattern because the list is long. Patterns that are weak, redundant or explained by a technical factor stay in the evaluation with that verdict, so the user can see what was considered and why it ranks where it does. Patterns that overlap (for example the same family seen at feature level and at class level) are merged under one ID with the overlap stated. State the total number of patterns evaluated.

**Then summarize clearly.** Present the result in this order:

1. **Summary line:** the total number of patterns evaluated, and how many fall in each evidence tier and each tag (Observed, Inferred, Speculative).
2. **Summary table:** one row per pattern: ID, pattern (one sentence, direction included), key features or family, evidence tier, one-line meaning, verdict (pursue, worth a look, weak or redundant, likely technical). Group rows by theme (for example lipids, amino-acid metabolism, microbial co-metabolites, unknowns) when there are many. Order by evidence tier, not by any combined score.
3. **One or two summary figures** (shown inline, Section 24B; carried into the reports). Choose the two that fit the data best:
   * an **overview figure** of all patterns at once, for example a dot or bar plot with one row per pattern showing effect direction and size (or the share of members moving the same way), colored by evidence tier, with raw p and family or class q on the plot; or
   * a **network or class map** with the pattern members marked (nodes colored by pattern and by direction of change); or
   * a **tier-by-theme grid** (themes by evidence tier, cells show the number of patterns).
   Every summary figure carries a graphical key and a "How to read this figure" line (Section 24B).
4. **Detail blocks** for each pattern follow, shortest for weak or redundant patterns (items 1 to 5 below, plus the small figure where it adds something; patterns that are weak, redundant or technical may share one compact multi-panel figure). Put the patterns the evidence supports best first.

For each pattern:

1. **Pattern**: one sentence naming what is changing and in which direction.  
2. **Evidence in brief**: how many features, how many move the same way, the annotated versus unannotated mix, and the key p-values and q-values (one line, always including raw p).  
3. **What it might mean**: the likely biological meaning, tagged Observed, Inferred or Speculative.  
4. **Possible cause and possible consequence**, each in one line.  
5. **Evidence tier** (Section 6A).  
6. **Key figure**: one small inline figure per pattern showing the result (Section 24B).

After the list, and if the user approved this default at intake, answer the three molecular-network discovery questions against the question (Section 5B), as a separate short block headed "Molecular-network discovery questions".

**What the output is not**

* No formal report and no formal reference list. Brief inline source names and years for literature claims are fine. Key figures are shown inline (Section 24B); the formal, numbered report figures come later.  
* No additional analyses are run until the user selects which patterns to pursue.

**The overlap table.** Where the interpretation community already holds findings that rest on this analysis (Section 4, item 19), show each pattern of this run beside the earlier finding it matches — the same features or families, the same direction — marked *already there, agrees*, *already there, more to say*, or *new*. A pattern that agrees with a finding already there is not argued again; one with more to say builds on, revises or contests it; a new one is argued. The user approves or changes the table, and it is recorded in the working file.

End with "Things I need from you": which of the evaluated patterns to pursue (a recommendation based on the evidence tiers, with the reason), and any questions that would change the interpretation. Do not ask whether they want more or fewer patterns; all were evaluated.

---

# 5B. Molecular-Network Discovery Questions (asked against the question)

The molecular network often holds the leads that statistics on single features miss, including leads at the edges of the question that was asked. When a molecular network is available ([ANALYZE.md](ANALYZE.md), Section 13C), interpretation therefore asks three fixed questions **about the network**, against the **question**: the first prompt of the run, recorded verbatim (`SKILL.md`, Rule 7) and shown in the question at the top at the top of every report ([REPORT.md](REPORT.md), Section 4B). If the prompt only names the skillset, use the question confirmed at intake and quote it.

**Default and approval.** This block is **on by default and is delivered alongside the emerging patterns** (Section 5A). It is a default, so the user must approve it at intake (Section 3A) before it runs. If the user declines or changes it, record that in the working file and do not raise it again. If no molecular network is available, say so in one line and skip it.

| # | Question | What it surfaces |
| :---- | :---- | :---- |
| 1 | **What is most interesting in the molecular network in relation to the question?** | The molecular families, annotated-neighbor links, delta-mass relationships, compound-class patterns or network-level trends that bear most directly on the question that was asked, and why they stand out |
| 2 | **What is most unexpected in the molecular network in relation to the question?** | Network findings that run against what the prompt, the study background or the literature would predict (for example a family moving opposite to its annotated members, or an expected family or class that is absent) |
| 3 | **What is more interesting in the molecular network that is not relevant to the question?** | Large, coherent or strongly changing families and classes outside the question that may lead to a different discovery |

**Rules**

* Answer all three every time the block is approved, in chat directly after the emerging-pattern list (Section 5A) and in both reports ([REPORT.md](REPORT.md), Section 6A).  
* Work from the network tables the analysis published ([ANALYZE.md](ANALYZE.md), Section 13C): network families, family sizes, delta masses, nodes and edges, the compound-class assignments and composition, and the volcano by class. Use the per-feature results (including raw p and q) and the filter-loss review (Section 4A) for the statistics. Open specific families with the tools of Section 8.  
* An item is a **molecular family, a link between an annotated and an unannotated node (with its delta mass), a compound class, or a set of connected nodes**, not a single feature on its own. A single feature qualifies only as the annotated anchor of a family. Name each item with its family or component ID, its size, and its annotated members (full feature names).  
* Default: up to 3 items per question (confirm at intake, Section 3A). Each item follows Section 24A: the key interpretation first with its tag, one compact evidence line (members, how many move the same way, raw p and q for the family or class result, the evidence tier of Section 6A), the key figure (Section 24B), and what would test or overturn it.  
* **Question 1.** Rank by how directly the item answers the prompt, not by p-value alone. Say what makes it interesting (size, direction coherence across members, annotated anchors, a delta mass that links a known compound to unannotated neighbors, novelty relative to the cited papers).  
* **Question 2.** State the expectation and where it comes from (the prompt, the study background, a cited paper, a medication or diet record) and the network observation that violates it. Rule out technical explanations first (filtering, normalization, annotation level, contaminants such as PEG series, adducts, in-source fragments, a delta mass that equals a known adduct or isotope step) and say what was checked. An unexpected result is not automatically a discovery.  
* **Question 3.** Include network findings outside the question, for example a large or coherent unannotated family, a drug or dietary exposure family, a contaminant family, a family tied to a strong metadata driver. State why each is outside the prompt and why it still deserves attention. Do not drop an item because it is off-prompt; park it only if the user says so.  
* An item appears under one question only; cross-reference it if it also fits another.  
* Tag every item Observed, Inferred or Speculative and use the language of Section 24. Do not state a mechanism as fact.  
* If nothing qualifies for a question, say so and say what was checked. Do not pad.  
* The answers help the user choose patterns to pursue. They do not replace the emerging-pattern list.

---

# 6\. Step 1 — Identify Interesting Signals

Identify observations that warrant biological investigation.

Potential signals include:

* statistically strong features  
* features with raw p \< 0.05 or family-level trends at raw p \< 0.1 (Section 6A)  
* families, network components or classes in which most members move in the same direction  
* removed features with a notable pattern (Section 4A)  
* large effect sizes  
* robust features across sensitivity analyses  
* features associated with the primary phenotype  
* features associated with important metadata variables  
* molecular families showing coordinated changes  
* unannotated features with informative network context  
* groups of chemically distinct features showing coordinated behavior  
* unexpected feature relationships  
* features recurring across cohorts  
* features recurring across public datasets  
* features that substantially contribute to a biological pattern  
* findings that change substantially after covariate adjustment  
* discordant patterns that require explanation

Do not simply rank features by p-value, and do not stop at features that pass FDR.

A feature with modest statistical significance may be biologically important if it is part of a highly coherent molecular family or broader biological pattern.

Conversely, an extremely significant isolated feature should not automatically receive a strong biological interpretation.

---

# 6A. Evidence Tiers Beyond FDR

Do not restrict pattern-finding or interpretation to features that pass FDR.

**Tiers (defaults; confirmed at intake)**

| Tier | Criterion | Use |
| :---- | :---- | :---- |
| Established statistically | q below the analysis threshold | Interpret directly |
| Nominal feature signal | Single feature, raw p \< 0.05, q shown | Interpret as exploratory |
| Family or class trend | Family, network-component or class score, raw p \< 0.1 | Interpret as exploratory |
| Directional coherence | Most members of a family or class move the same way, with no member required to be significant | Investigate; report the counts |

&nbsp;

**Rules**

* **Always report raw p-values alongside q-values.** Never report q alone.  
* **Test direction-coherence explicitly.** For a pre-specified family (a network component, a mass-defined class, a pathway-linked set), report the number of members lower, the number higher, and a family-level score (for example the mean z of members) with its raw p-value. A sign test is acceptable.  
* **Pre-specify families before looking at the result.** Report how many families were tested, so a trend is not cherry-picked.  
* **Label every nominal or trend result as exploratory**, show the effect size and direction, and state what would raise or lower confidence in it.  
* **Biological pattern beats single-feature p-value.** A group of features such as pro-inflammatory mediators, bile-acid classes, or polyamine intermediates that shifts together is worth interpreting even if no single feature is significant.  
* **Do not hide the multiple-testing context.** Showing the q-value is how the reader sees it.

---

# 7\. Step 2 — Search for Coordinated Patterns

After identifying candidate signals, search for patterns across the dataset.

Look for:

### Within-family patterns

* multiple related features changing together  
* related features changing in opposite directions  
* annotated and unannotated nodes sharing behavior  
* partial molecular-family responses  
* expanded or contracted chemical families

### Across-family patterns

* multiple chemically distinct families showing coordinated changes  
* complementary changes across pathways  
* multiple families consistent with the same biological process  
* opposing patterns that may indicate pathway remodeling rather than simple increase/decrease

### Metadata-linked patterns

* features associated with disease  
* features associated with disease severity  
* features associated with age, sex, BMI, medication, diet, or other metadata  
* biological patterns that disappear after adjustment  
* patterns that emerge only after accounting for a covariate

### Cross-cohort patterns

* recurrence of the same molecular family  
* recurrence of the same chemical pattern  
* recurrence of the same biological interpretation  
* consistent direction of change  
* cohort-specific biology

The goal is to determine whether observations form a **coherent biological pattern** rather than treating every feature independently.

---

# 7A. Multi-Level Class Analysis

Do not stop at the broad chemical class. For every class that shows a signal, or that is biologically relevant to the question, analyze it at several levels and report each level, so that a focused sub-class signal is not lost in the average of a large class and a broad signal is not over-interpreted when only one sub-class drives it.

**Levels to test (pre-specify, then report all that were tested)**

1. **Broad class**: for example all fatty acids, all acylcarnitines, all bile acids, all amino acids and peptides.  
2. **Sub-class by chain length or size**: for example short-, medium- and long-chain fatty acids; C2 to C5, C6 to C12 and C14 or longer acylcarnitines; di- versus tripeptides.  
3. **Sub-class by modification**: for example oxidized (hydroxy, keto, dicarboxylic) versus unmodified acylcarnitines; saturated versus unsaturated; conjugated versus free; sulfated or glucuronidated versus parent.  
4. **Sub-class by origin or function**: for example primary versus secondary bile acids; branched-chain versus aromatic amino acids; host-derived versus microbe-derived members.  
5. **Molecular family or network component**: members that cluster together in the FBMN, including unannotated nodes.  
6. **Individual features**, as the last level.

**Rules**

* Report, for each level: the number of features, the number lower and higher, a family-level score with raw p and q, and the effect size. Reuse the tiers and direction-coherence test in Section 6A.  
* Pre-specify the levels before looking at results and report how many were tested. Sub-class results are exploratory unless they survive correction across the levels tested.  
* Compare levels explicitly: if the sub-class effect is larger than the broad class, say so (and say what it implies biologically); if sub-classes move in opposite directions, say so, because that can cancel at the broad level.  
* Check the complement. If oxidized members change, test the unmodified members too, and report whether the effect is specific to the modification or shared by the whole class.  
* Note annotation confidence at each level (library match, mass-difference annotation, formula only). Sub-class labels that rest on mass differences are candidates, not identifications.  
* Do not inflate a sub-class by choosing its boundary after the fact. Define sub-classes from chemistry, not from the result.  
* Run class-level analyses on the retained table first. Where a class has members removed by filtering, repeat the analysis on the unfiltered table the analysis published and report both, labelled, so a signal that depends on removed members is visible.  
* For a notable class or sub-class, consider proposing a class balance score (Section 13B). It is a proposal that always needs user approval.

---

# 8\. Step 3 — Interrogate the FBMN

The FBMN is an active source of biological discovery.

The skill should interrogate the network rather than merely use it as a visualization.

Start from the network tables the analysis published, when they exist ([ANALYZE.md](ANALYZE.md), Section 13C): the family-size table and the families table (which families exist, their size and class composition), the delta-mass inventory (for example which edges link a known compound to an unannotated neighbor by a defined mass difference), and the compound-class assignments with their color key. Use them to choose which families to open first; do not recompute them. Interpretation of what a family, class or mass difference means is done here, not in the analysis.

For candidate features and patterns, investigate:

## 8.1 Molecular neighbors

Ask:

* What features are directly connected?  
* How strong are the connections?  
* Are neighboring nodes annotated?  
* Are neighboring nodes unknown?  
* Do neighboring nodes show similar statistical behavior?  
* Do they form a coherent molecular family?

## 8.2 Molecular families

Determine:

* family size  
* annotation coverage  
* directionality of changes  
* abundance patterns  
* statistical consistency  
* presence of unknown members  
* chemical relationships  
* whether the family supports or contradicts the initial hypothesis

## 8.3 Mass relationships

Where appropriate, investigate:

* homologous series  
* recurring mass differences  
* conjugate relationships  
* plausible transformations  
* other systematic chemical relationships

Do not infer molecular identity solely from mass differences.

## 8.4 Unknown-centered investigation

For important unannotated nodes:

1. identify their network neighbors  
2. inspect annotations of neighboring nodes  
3. determine whether they belong to coherent molecular families  
4. inspect their statistical behavior  
5. determine whether related unknowns show coordinated behavior  
6. search repository evidence where appropriate  
7. determine what biological interpretations remain possible despite uncertain identity

Unknown features should be treated as **evidence with uncertainty**, not ignored and not overidentified.

---

# 9\. Step 4 — Generate Biological Hypotheses

Generate hypotheses at multiple biological levels.

## Level 1 — Direct chemical interpretation

What does the observed chemistry suggest?

Examples include but are not limited to:

* altered bile acid chemistry  
* altered amino-acid metabolism  
* altered lipid remodeling  
* altered xenobiotic metabolism  
* altered hormone synthesis

## Level 2 — Molecular-family interpretation

What does the behavior of a molecular family suggest?

Examples include but are not limited to:

* coordinated modification of a chemical family  
* accumulation/depletion of related metabolites  
* altered production or transformation of a compound class

## Level 3 — Metabolic-process interpretation

What metabolic processes could generate the observed pattern?

Examples include but are not limited to:

* altered fatty-acid metabolism  
* altered redox metabolism  
* altered amino-acid catabolism  
* altered microbial fermentation

## Level 4 — Biological-process interpretation

What broader biological state could produce the coordinated metabolomic pattern?

Examples include but are not limited to:

* inflammation  
* oxidative stress  
* immune activation  
* cellular stress  
* altered nutrient availability  
* tissue injury  
* altered host–microbe interactions

## Level 5 — Physiological or disease interpretation

What physiological state or phenotype could the pattern reflect?

Examples:

* disease-associated metabolic remodeling  
* disease severity  
* altered intestinal physiology  
* systemic metabolic response

## Level 6 — Exploratory hypotheses

What unexpected explanations could account for the observations?

These may include:

* unexpected host–microbe interactions  
* previously undescribed metabolite transformations  
* unrecognized dietary contributions  
* unexpected environmental exposures  
* novel relationships between molecular families  
* mechanisms not previously described in the literature

Exploratory hypotheses are encouraged, but must be explicitly labeled as speculative.

---

# 10\. Hypothesis Categories

Every biological hypothesis should receive an interpretation category.

### Established

The interpretation is supported by well-established biological knowledge and evidence directly relevant to the observed chemistry.

### Plausible

The interpretation is chemically and biologically coherent but the specific relationship is incompletely established.

### Exploratory

The interpretation is a reasonable hypothesis generated from the observed data but is substantially speculative or insufficiently supported by existing evidence.

The skill must not upgrade an exploratory hypothesis to plausible or established merely because no contradictory evidence was found.

---

# 11\. Literature Interrogation

For each important hypothesis, search relevant peer-reviewed literature.

Literature searches should answer specific questions rather than simply finding papers containing the metabolite name.

Examples include but are not limited to:

* Is this metabolite associated with the proposed biological process or related processes?  
* Is this molecular family associated with the phenotype?  
* Are these metabolites produced by microbes?  
* Are these compounds known dietary metabolites?  
* Has this chemical transformation been described?  
* Is this pattern associated with inflammation?  
* Has similar chemistry been observed in the disease?  
* Are there known alternative explanations?

Literature evidence should be tied to the precise claim being made.

The skill must distinguish:

> “This metabolite has been observed in IBD”

from:

> “This metabolite causes inflammation in IBD.”

**Every source goes through the library.** Before searching, list what the library already holds, by DOI. A source it holds is used from there. A source it does not hold is brought into the library before any finding cites it; where the library cannot be published to, say so and ask a member who imports there for it.

**Record every source** in the working file with its authors, journal, year, identifier, the claim it was used for, and its **access level** (full text, abstract only, summary only). Also record where the literature does not support a finding, points the other way, or was not found. These records feed the *How this fits the literature* part of the plain-language summary and the Key references box of both reports ([REPORT.md](REPORT.md), Section 4C). Only sources actually retrieved are listed; none are cited from memory. What a finding may rest on, given how much of a source was reached, is for the community's documents to say.

The first does not establish the second.

If a relevant paper is found but cannot be fully accessed, mention this to the user. Send the user the link to the paper and ask if the user can upload a pdf copy of the full text.

---

# 12\. Repository-Level Context

Where available, interrogate public metabolomics resources to determine whether observations recur beyond the current dataset.

Potential resources include:

* MASST  
* MassQL  
* ReDU  
* public molecular networking datasets  
* other relevant repository-level resources

Repository searches should investigate:

### Spectral recurrence

Does the feature or related spectrum occur elsewhere?

### Chemical recurrence

Does the molecular family occur across independent datasets?

### Biological recurrence

Does similar chemistry occur in datasets involving the proposed biological process or phenotype?

### Context specificity

Does the chemistry occur broadly across unrelated biological contexts?

Broad recurrence may weaken an interpretation that assumes disease specificity.

Repository recurrence must not automatically be treated as biological validation.

Record, where available:

* dataset accession  
* search parameters  
* matching criteria  
* sample context  
* relevant metadata  
* date of search  
* whether datasets may overlap with the current study

---

# 13\. Additional Analysis Requests

Biological interpretation may reveal questions that cannot be answered from what the analysis published.

The skill may therefore **suggest additional analyses** when they would materially improve biological interpretation.

Potential analyses include but are not limited to:

* testing an additional metadata association  
* testing a feature against disease severity  
* adding or removing a covariate  
* performing a covariate-adjusted model  
* testing a molecular family as a group  
* running a class balance score for a notable class or sub-class, with and without VIP weighting (Section 13B)  
* examining correlations between features  
* comparing a subset of samples  
* performing a targeted statistical comparison  
* examining an unexpected FBMN pattern  
* testing a proposed biological pattern across cohorts  
* performing targeted feature extraction  
* interrogating a molecular family more deeply  
* conducting a targeted MassQL query  
* conducting MASST or ReDU searches  
* performing additional structural annotation  
* investigating a candidate unknown  
* testing whether a finding persists under an alternative analysis  
* evaluating a specific alternative explanation

The skill should distinguish between:

### Investigation using existing outputs

Examples:

* inspect existing molecular families  
* examine existing metadata  
* query available repository resources  
* inspect existing annotations

and:

### New analysis

Examples:

* new statistical model  
* new covariate adjustment  
* new feature filtering (reviewing what existing filters removed is read-only and does not need approval; see Section 4A)  
* new normalization  
* new transformation  
* new subset analysis  
* new formal statistical test

New analyses must be explicitly proposed and approved before execution.

---

# 13A. Dietary Intake and Medication Information Gaps

Diet and medication are the most common alternative explanations for a metabolomic pattern (Section 18). When metadata on either is missing, say so, and say whether a finding depends on it.

**When to trigger.** Recommend the tools below when any of these apply:

* a finding could plausibly be driven by dietary intake (for example plant or food-derived compounds, fatty acids, peptides and amino acids, polyphenol metabolites, food additives, caffeine or other dietary markers);  
* a finding could plausibly be driven by medication or other xenobiotics (for example drug parent compounds or metabolites, excipients, or unexplained xenobiotic-like features);  
* the metadata contain no diet, fasting or medication records, or only partial ones;  
* diet or medication is the leading unexcluded alternative explanation for a result.

**What to recommend**

* **MetaboApps DrugReadout** ([https\://drugreadouts.gnps2.org/](https://drugreadouts.gnps2.org/)): to look for drugs and drug metabolites in the data and infer medication exposure when medication records are missing.  
* **MetaboApps FoodReadout** ([https\://foodreadouts.gnps2.org/](https://foodreadouts.gnps2.org/)): to infer dietary exposure from food-derived molecules when intake records are missing.

**How to recommend**

* Name the specific question the tool would answer (for example: "responders and non-responders could differ in medication use; DrugReadout could show whether drug signals differ between groups").  
* State what each possible result would mean for the hypothesis, and what it would not establish (a readout infers exposure from molecules; it is not a medication or diet record).  
* Treat this as a proposed additional analysis under Section 14, and ask for approval. Once results are available, use them as new evidence and add them to the hypothesis record.  
* Do not run or cite the tools as if they had been run. Do not imply that an inferred exposure is a verified exposure.  
* Do not re-recommend the tools if the user has parked or declined them (Section 3A).

For MASST searches, MassQL and the Conjugated Metabolome Explorer, see Section 13C.

---

# 13B. Class Balance Score (proposed follow-up for notable classes)

## Objective

For a notable chemical or biological class, summarize each sample with one number that shows the **balance** between the members that go up and the members that go down, so a whole class can be tested and shown in one figure (a boxplot per group, one point per sample). Unlike a composite mean, a balance score handles classes whose members move in opposite directions, and because it is a ratio, much of the sample-level loading cancels out.

**This is a proposed additional analysis. Always ask the user for approval before running it (Section 14). Never run it automatically.**

## 13B.1 Definition

For sample *i*, with a numerator set U and a denominator set D of features:

> **B\_i \= ln( GM(U)\_i / GM(D)\_i )**, where GM is the geometric mean of feature abundances.

If the data are already on the natural-log scale, this is the mean of the log values in U minus the mean of the log values in D. Use geometric means (not sums) by default so that one abundant feature does not dominate; a sum-based version may be added as a sensitivity check. Handle zeros and imputed values as the analysis did, and report the imputed fraction for the features in U and D.

**Orientation.** For the data-driven variants, **the group of interest is always the numerator**: U is the set of features higher in the group of interest, and D is the set higher in the comparator, so a higher score means more like the group of interest. State the orientation in every axis label (for example, "ln(features higher in responders / features higher in non-responders)"). For the pre-specified chemistry ratio, state the numerator and denominator sets explicitly in the axis label (for example, "ln(oxidized / unmodified)") and compare the groups on that score.

## 13B.2 Variants

| Variant | How U and D are defined | Main weakness |
| :---- | :---- | :---- |
| **A. Pre-specified chemistry ratio (recommended primary, when a rationale exists)** | U and D are defined from chemistry before looking at results (for example oxidized versus unmodified acylcarnitines; primary versus secondary bile acids) | Needs a biological reason for the split |
| **B. Data-driven, no VIP** | All class members, split by the direction of their effect | Supervised selection |
| **C. VIP above 1, equal weights** | Features with VIP above 1, split by direction | Arbitrary cutoff; supervised selection; VIP is relative to the whole model, not to the class |
| **D. VIP-weighted** | All class members, split by direction, each weighted by its VIP (weighted geometric mean); no cutoff | Supervised selection; VIP depends on the whole model |

**Default plan when approved:** run A as the primary where a rationale exists, and run B, C, and D as sensitivity checks. Report all variants side by side. If only the VIP-based versions are significant and the pre-specified ratio is not, label the result **selection-sensitive**. If there is no pre-specified rationale, say so and treat B as primary, with C and D as checks.

## 13B.3 Statistics

* Compare groups on the per-sample score using the model that matches the design (rank-sum for independent samples; a mixed model for repeated measures or longitudinal data). Report effect size (for example Cliff's delta), confidence interval, raw p, and n.  
* **Circularity.** In variants B, C, and D, features are chosen using the same group labels that are then tested, so the naive p-value is optimistic. Report it, labelled optimistic, and give a **label-shuffle permutation p** that repeats the entire selection step (and VIP computation) on each shuffle. Record the number of permutations and the random seed.  
* Variant A has no selection step, so its test is valid as run; it is still classified under the tiers in Section 6A (family or class level).  
* Report how many classes and sub-classes were scored, so the result is not cherry-picked.  
* Show the feature count in U and D before testing. Skip a class when U or D has too few features; start with at least 3 per side, state that this is a starting value, and ask the user to confirm it.

## 13B.4 Inputs and tables

* Run on the retained table first. Where the class has members removed by filtering, repeat on the unfiltered table ([ANALYZE.md](ANALYZE.md), Section 13A) and report both, labelled.  
* Take VIP values from what the analysis published. Do not refit the model without approval.  
* Report the existing class composite next to the balance score when both are available.

## 13B.5 Reading the result

* The balance score shows **direction balance, not absolute abundance**. A class can fall in total (composite) with a near-null balance score, which suggests a class-wide shift; or show a clear balance shift with a flat composite, which suggests remodeling within the class. State which applies.  
* Do not turn the score into a mechanism. Apply Sections 24 and 25\.

## 13B.6 Output

* A figure like a class-level boxplot per group: one point per sample, n, raw p, and permutation p on the panel, orientation in the axis label.  
* A table of per-sample scores and a table of the features in U and D with their weights and signs.  
* The method, parameters, seed, and code, recorded as in Section 15\.  
* Its place in the evidence of the hypothesis it serves (Section 23).

Present this to the user using the proposal format in Section 14, including the classes and sub-classes to score, the variants, the definition of U and D, what each outcome would imply, and the limitations. Wait for approval.

---

# 13C. Downstream Follow-Up Tools (MASST family, MassQL, Conjugated Metabolome Explorer)

These tools are **follow-ups for emerging patterns the user is already investigating** (Phase 1 patterns the user selected, Section 5A; hypotheses in the queue, Section 19). Never recommend them in the analysis, in the Phase 1 pattern list itself, or as a routine step. **Suggest them proactively.** The user may not know these questions can be asked, so do not wait for them to ask. Once a pattern is selected, check it against the triggers in 13C.0 and offer the matching tools as a short "Ways to dig further" menu (once per pattern, in chat, repeated in the report's Next-tests box). Every use is a proposed additional analysis under Section 14 and needs approval. Offer at most three items per pattern, ranked with hypothesis tests first (13C.0A), then by how much each would change the interpretation; put the rest in the hypothesis queue without raising them. Do not re-offer tools the user has parked or declined (Section 3A). Never describe a tool as run unless it was run. A search hit is a hypothesis about where a spectrum has been seen, not an identification.

## 13C.0 Triggers

A trigger can come from the user's context or from evidence in the data and literature. Strong triggers may be raised in chat at once. Weak triggers go into the pattern's "Ways to dig further" menu only. State the trigger in one line with each suggestion ("Suggested because: ...").

| Trigger | Strength | Tools it points to |
|---|---|---|
| **Hypothesis testing (highest priority).** A hypothesis in the queue (Sections 9, 17, 19) or an alternative explanation raised by the challenge step (Section 18) makes a prediction one of these tools can check. See 13C.0A. | Strong | The tool whose result would support or contradict the hypothesis |
| **Stated interest.** The user's prompts, intake answers or hypotheses mention microbes, the gut, a tissue, drugs or environmental exposure. Applies to every selected pattern from then on. | Strong | microbeMASST, microbiomeMASST, tissueMASST, personalcareMASST, DrugReadout (matching the stated interest) |
| **Study design.** Stool or other microbiome-rich matrix; antibiotic, probiotic, FMT or germ-free arms; mouse cohort (tissueMASST is murine-only: say so for human cohorts). | Strong | microbeMASST, microbiomeMASST, tissueMASST |
| **Literature hint.** Literature interrogation (Section 11) suggests the feature or family is microbial, tissue-specific or exogenous. | Strong | The matching MASST |
| **Contaminant or exogenous suspicion.** Looks like a product, plasticizer or xenobiotic; also seen in blanks; or the user challenges the finding (Section 18). | Strong | personalcareMASST, DrugReadout, FoodReadout (13A) |
| **Known neighbor.** A family member is annotated as a known microbial or host-derived class, and its neighbors are unannotated. | Strong | microbeMASST or tissueMASST on the neighbors |
| **Conjugation delta mass.** An unknown sits a fixed mass difference from a known compound; a drug annotation is in the family. | Strong | Conjugated Metabolome Explorer; PostMN MassQL; DrugReadout |
| **Partial annotation.** Only some family members have library matches and members share fragments. | Strong | PostMN MassQL |
| **Isomer ambiguity.** Bile acids with several candidate isomers. | Strong | PostMN MassQL bile acid sets (Multi-step MassQL only with an FBMN-type task) |
| **Rare feature.** Detected in few samples, no network neighbors, or very low abundance across the cohort; a sanity check that others see it. | Weak | fastMASST |
| **Doubtful annotation.** Low-cosine library match or a suspect identity. | Weak | fastMASST, or the domain MASST that fits the claimed compound |
| **Replication.** A main finding for which the user wants to know whether other cohorts of the same condition report it. | Weak | fastMASST on the top features |
| **Unannotated top discriminator.** An unannotated feature with high VIP or effect size. | Weak | fastMASST, then a domain MASST |

### 13C.0A Hypothesis testing as a trigger

Whenever a hypothesis is formed, refined or challenged, ask: "Which of these tools could return a result that supports or contradicts it?" If one can, offer it as a test of that hypothesis, not as a general suggestion. These offers rank first in the three-item cap and are tracked in the hypothesis queue.

| Hypothesis or alternative explanation | Test | Result that supports | Result that contradicts or weakens |
|---|---|---|---|
| The feature or family is microbially produced | microbeMASST (and microbiomeMASST for gut or microbiome samples) | Matches to microbial isolates, in taxa plausible for the sample type | No matches (weak: coverage is limited); matches only to unrelated taxa |
| The signal is host-derived at a tissue or site | tissueMASST (murine; say so for human data) | Matches concentrated in the relevant tissues | Matches absent from, or only in unrelated, tissues |
| The feature is exogenous or a product contaminant (alternative explanation, Section 18) | personalcareMASST; DrugReadout and FoodReadout (13A) | Matches to personal-care products | No matches (weak) |
| The feature is real and reproducible, not an artifact or a one-off | fastMASST (Fast Search) | Found in other datasets of similar samples | Found nowhere else (weak on its own; combine with detection counts and XIC/spectrum review) |
| The annotation is correct | fastMASST or the matching domain MASST on the library compound's spectrum | The compound is seen in comparable samples | Never seen in comparable samples |
| The family contains more members than the library shows | PostMN MassQL with a family-derived query | New scans carrying the shared pattern that cluster with the family | No new scans |
| The unknown is a conjugate of a known compound | Conjugated Metabolome Explorer; PostMN MassQL (product ion plus the delta-mass neutral loss) | The delta mass or conjugation is reported with spectral support; MassQL finds the pattern | Not reported; no scans carry the pattern |
| The pattern reflects bile acid sub-class or isomer differences | PostMN MassQL bile acid sets | Sub-class assignments differ between groups as predicted | No difference |

For each offer, state the hypothesis, the prediction being tested, and both columns above in the user's terms, before the user decides. Record the proposal, approval and result in the hypothesis queue (Section 19: "next investigation", "whether an additional analysis was proposed", "result"), and move the hypothesis state accordingly. A single "no match" never moves a hypothesis to CONTRADICTED; coverage is incomplete (13C.6). A result that contradicts a hypothesis is reported as plainly as one that supports it.

## 13C.1 Tool by situation: what each answers and what it would not mean

| Situation in the emerging pattern | Tool | Question it answers | What a result would and would not mean |
|---|---|---|---|
| Feature or family is unannotated or novel and the user wants to know whether it is made by microbes | microbeMASST | Has this spectrum been seen in cultured microbial isolates, and which taxa? | Hits support a microbial origin as a hypothesis. No hit does not exclude microbial origin (limited coverage). It does not show the microbe makes it in this cohort. |
| Gut or host-microbe pattern; user asks where else the feature occurs in microbiome samples | microbiomeMASST | In which microbiome datasets, body sites and host conditions has it been detected? | Shows the feature occurs in similar samples. Does not show cause or direction. Preprint-based resource; say so. |
| Pattern is a tissue or organ signal, or the user asks whether a feature is host-derived at a given site | tissueMASST | In which tissues or organs of the murine atlas is it found? | Supports tissue distribution. Murine data only; it does not give human tissue origin. |
| Xenobiotic-like or exogenous-looking feature, and the user wants to test for personal-care or household product sources | personalcareMASST | Is it found in personal-care products? | Supports a product source. Does not show exposure in these participants. |
| The user asks what other datasets contain a feature | fastMASST (Fast Search) | In which public datasets, repositories and sample types is it present? | Shows prior reports. Matches are spectral matches, not identifications. |
| A family or class has a shared fragmentation pattern and the user wants all members found in the data | PostMN MassQL (this dataset's task) | Which scans in this dataset contain the pattern? | Finds candidates for the pattern. Does not prove the structure. |
| Bile acid isomers matter to the pattern | Multi-step MassQL | Which bile acid sub-class or isomer do the spectra fit? | Subclass-level hypotheses. Needs an FBMN-type task (see 13C.4). |
| A mass difference between features suggests conjugation (for example an unknown differs from a known compound by a delta mass) | Conjugated Metabolome Explorer | Has this conjugation or delta mass been proposed in public data? | Gives structural hypotheses with spectral support. Not confirmation. |
| Medication or diet could explain the pattern | DrugReadout, FoodReadout (Section 13A) | See Section 13A. | See Section 13A. |

## 13C.2 Tool links

| Tool | Link |
|---|---|
| microbeMASST | https://masst.gnps2.org/microbemasst/ |
| microbiomeMASST | https://masst.gnps2.org/microbiomemasst/ |
| tissueMASST | https://masst.gnps2.org/tissuemasst/ |
| personalcareMASST | https://masst.gnps2.org/personalcaremasst/ |
| fastMASST (Fast Search) | https://fasst.gnps2.org/fastsearch/ |
| PostMN MassQL | https://massqlpostmn.gnps2.org/ |
| Multi-step MassQL (bile acid isomers) | https://multistep-massql.gnps2.org/ |
| Conjugated Metabolome Explorer | https://conjugated-metabolome.gnps2.org/ |
| DrugReadout | https://drugreadouts.gnps2.org/ |
| FoodReadout | https://foodreadouts.gnps2.org/ |

Citations to give with the recommendation: microbeMASST (Zuffa et al., Nature Microbiology); microbiomeMASST (bioRxiv preprint, flag as preprint); tissueMASST ("A Multi-Organ Murine Metabolomics Atlas Reveals Molecular Dysregulations in Alzheimer's Disease", bioRxiv, https://www.biorxiv.org/content/10.1101/2025.04.28.651123v1.full; flag as preprint); personalcareMASST (no publication; say so); MassQL (Damiani et al., Nature Methods 22, 1247, 2025); Multi-step MassQL (Mohanty et al., bioRxiv 2025.03.04.641505); Conjugated Metabolome Explorer (Xing et al., https://github.com/Philipbear/conjugated_metabolome). Links and the citation line appear at the point of recommendation, in chat and in the report's Next-tests box.

## 13C.3 Ready-to-paste input blocks for the MASST tools

Build the block from the feature's **consensus MS/MS** in the EB task (`aligned_features_filled.mgf`; `FEATURE_ID` equals the quant-table row ID). Give the user the block in a code box, plus the same content as a text file in the run's folder if they approve. Never type peaks from memory.

```
Tool:            <link from 13C.2>
Feature:         <row ID>, m/z <precursor m/z to 4 decimals>, RT <min>
Precursor m/z:   <value>
Charge:          <1 for [M+H]+ / [M-H]-; state the adduct and ion mode>
Peaks (m/z intensity, one per line):
<consensus peaks, top 50 or fewer, noise-filtered>
```

Settings for the domain MASSTs (microbeMASST, microbiomeMASST, tissueMASST, personalcareMASST): precursor m/z tolerance 0.05; fragment m/z tolerance 0.05; cosine threshold 0.7; minimum matched peaks 3 (microbeMASST) or 4 (microbiomeMASST; use the tool's default for the others); analog search off at first. Add this when the pattern concerns an unknown related to a known compound: "Second run with analog search on (delta mass below 130 and above 200) to look for related molecules; read analog hits as weaker evidence."

fastMASST (Fast Search): same peaks and precursor m/z; default settings (precursor 0.05, fragment 0.05, cosine 0.7, analog No), **except** the library selection, which is set to `metabolomicspanrepo_index_nightly` so the search returns the other datasets in which the feature occurs.

Classic MASST defaults are looser (2.0 and 0.5 Da, 6 peaks); do not use them unless the user asks.

## 13C.4 Everything Bagel Integration (as of 3 Nov 2026)

* **PostMN MassQL accepts the EB task ID.** Enter the EB task ID, choose a query set, click Run Analysis. The app is built around library matches, so a feature without a library match shows only in the Full Table.
* **Multi-step MassQL did not accept the EB task ID.** Do not promise that it will run on an EB task. Offer it only when the user has an FBMN-type task for the same data; otherwise suggest PostMN MassQL's bile acid sets.
* **Conjugated Metabolome Explorer has no task-ID input.** It is a lookup resource (Compound Search; Browse by Delta Mass). Give the user the delta mass and the two feature m/z values to look up.
* The domain MASSTs and Fast Search take a spectrum, not a task ID, so the input block in 13C.3 is the correct input. Their pages were not run on EB-derived spectra in the test; state that when handing off.

## 13C.5 Suggested MassQL queries

Syntax: `QUERY scaninfo(MS2DATA) WHERE MS2PROD=<m/z>:TOLERANCEPPM=5 AND MS2NL=<mass>:TOLERANCEPPM=5`. Give the user the exact query text, where to paste it (PostMN MassQL query editor, "Edit Queries"), and what it would find.

1. **Built-in sets in PostMN MassQL** when the pattern concerns bile acids (Bile acids stage 1 and stage 2), N-acyl lipids, or the compendium queries listed in the app's dropdown. Name the set and the question.
2. **Data-derived queries for a molecular family or pattern.** Take the consensus spectra of the family's members (EB `aligned_features_filled.mgf`), find the product ions and neutral losses shared by most members, and write a query from those (for example, two shared product ions plus a shared neutral loss, 5 ppm). State which members the query was built from and how many of the family's spectra contain each ion. Do not invent class-diagnostic masses from memory; if the user wants a literature-defined class, ask for the source or search for it and cite it.
3. **Delta-mass queries** for a suspected conjugation: product ion of the known part and the neutral loss that equals the delta mass.
4. Always state the expected result and the check: run the query on this dataset, then count how many scans match, how many are in the family already, and how many are new candidates. New candidates are hypotheses until their spectra are inspected (mirror plot or XIC).

## 13C.6 How to propose

**Menu format.** Once per selected pattern (and again whenever a new hypothesis for it is formed or challenged), offer a "Ways to dig further" menu of up to three items. Each item is one plain-language line (what the user would learn, for example "find out whether microbes are known to make this molecule"), the "Suggested because" trigger from 13C.0, the tool link, and the exact input. Nothing runs until the user approves an item; on approval, give the full Section 14 proposal for it.

Use the Section 14 format. Each proposal names: the feature or family and why it matters to the pattern; the tool with its link and citation; the exact input (13C.3 block or 13C.5 query); what each possible result would imply for the hypothesis; what it would not establish (13C.1, last column; a spectral match is not an identification; coverage is incomplete; absence is not evidence of absence). Ask before running anything. Searches against public resources send the spectrum outside the project; confirm with the user before sending spectra from unpublished or restricted data.

After results: record them as new evidence in the hypothesis record (Section 19), state the evidence tier (Section 6A, 21), and do not upgrade the claim beyond what a spectral match supports.

---

# 14\. Additional Analysis Proposal Protocol

When an additional analysis is warranted, do **not** immediately execute it.

First present:

### Question

What biological question remains unresolved?

### Why it matters

Why does resolving this question affect the interpretation?

### Proposed analysis

What analysis should be performed?

### Data required

What data or metadata are required?

### Method

What statistical or computational approach is proposed?

### Expected outcomes

What different results would imply for the biological hypothesis?

### Limitations

What will the analysis not establish?

### Approval

Ask the user whether to proceed.

Example:

> **Unresolved question:** The observed molecular pattern may reflect altered microbial metabolism, but medication use could provide an alternative explanation.

> **Proposed analysis:** Refit the relevant feature-level models including medication as a covariate.

> **Why:** If the associations persist after adjustment, this would strengthen the interpretation that the pattern is not explained solely by medication.

> **Limitation:** Persistence would not prove that microbial metabolism causes the disease phenotype.

> **Proceed with this analysis?**

Do not execute until the user approves.

---

# 15\. Executing an Approved Additional Analysis

Once the user approves:

1. perform only the approved analysis;  
2. preserve the original analytical results;  
3. clearly distinguish the new analysis from the original analysis;  
4. record the method and parameters, as the procedure the analysis will be published with;  
5. keep the code that ran, to be published with it;  
6. report the result;  
7. explain how the result affects the biological hypothesis;  
8. identify any new uncertainty;  
9. determine whether another investigation is warranted.

Do not silently alter the primary analysis because a new analysis produces a more biologically interesting result.

An approved analysis reads the library's tables and is published in the interpretation community, beside the finding it serves. It never changes what the library holds. Where it shows that something the analysis published is wrong — a wording the data do not bear out, a number that does not reproduce — say so to the user, state the correction in this run's own findings, and send the publisher of that artifact a Message naming it and what was found.

---

# 16\. Analysis → Interpretation Loop

After an approved analysis is completed, return to biological interpretation.

For example:

```
BIOLOGICAL HYPOTHESIS
        ↓
INFORMATION GAP
        ↓
PROPOSE ANALYSIS
        ↓
USER APPROVAL
        ↓
EXECUTE
        ↓
NEW RESULT
        ↓
UPDATE EVIDENCE
        ↓
CHALLENGE HYPOTHESIS AGAIN
        ↓
REFINE / REJECT / STRENGTHEN
        ↓
RETURN TO FBMN / LITERATURE / REPOSITORY
```

&nbsp;

The result of a new analysis should be treated as **new evidence**, not as automatic confirmation of the original hypothesis.

---

# 17\. Hypothesis Expansion

When an observation supports an initial hypothesis, expand it.

Example:

> Altered metabolites ↓ altered microbial metabolites ↓ altered microbial metabolism ↓ altered host–microbe metabolism ↓ potential contribution to inflammation

At every level, ask whether the data actually support moving upward.

Do not automatically convert chemical observations into disease mechanisms.

---

# 18\. Hypothesis Challenge

Every substantial hypothesis must be challenged.

The skill should actively search for alternative explanations, including:

* medication (see Section 13A for DrugReadout)  
* diet (see Section 13A for FoodReadout)  
* age  
* sex  
* BMI  
* technical batch  
* sample handling  
* disease severity  
* treatment status  
* microbial composition  
* general metabolic state  
* contaminants  
* adducts  
* fragments  
* analytical artifacts  
* non-specific stress responses  
* broad physiological changes  
* repository-wide ubiquity of the chemistry

The skill should ask:

> What else could explain this pattern?

and:

> What evidence would distinguish the proposed explanation from its alternatives?

If a hypothesis is supported only because alternatives were never considered, this should be stated clearly to the user. Where a tool can test an alternative (for example personalcareMASST for an exogenous source), offer it (Section 13C.0A).

---

# 19\. Iterative Investigation and Hypothesis Queue

Keep an explicit hypothesis queue, in the working file, so that a run taken up in a later sitting resumes with every hypothesis in the state it reached.

Each hypothesis may move through:

```
CANDIDATE
   ↓
INVESTIGATING
   ↓
SUPPORTED ──────→ REFINED
   ↓                  ↓
AMBIGUOUS ←───────────┘
   ↓
CONTRADICTED
   ↓
CLOSED
```

&nbsp;

Each iteration should record:

* hypothesis  
* observations motivating it  
* evidence examined  
* evidence supporting it  
* evidence contradicting it  
* alternative explanations  
* remaining uncertainty  
* next investigation  
* whether an additional analysis was proposed  
* whether the user approved it  
* result of the analysis  
* whether the hypothesis changed

For hypotheses that MASST, MassQL or Conjugated Metabolome Explorer can test, offer the test and record it here (Section 13C.0A).

The skill should be able to return to the FBMN when a hypothesis generates a new question.

For example:

> “If altered microbial metabolism explains this pattern, are there additional related molecular families in the network that should also change?”

The skill then investigates those families.

This makes interpretation a **hypothesis → interrogation → evidence → analysis → refinement** loop.

---

# 20\. When to Return to the Analytical Layer

The biological interpretation skill should not silently redo statistical preprocessing.

Return to the analytical layer when interpretation requires:

* a new statistical comparison  
* a new covariate adjustment  
* a different normalization  
* a new filtering decision  
* a new longitudinal model  
* a formal statistical test the analysis did not publish  
* validation of an unresolved statistical question

The biological skill may identify the question and propose the analysis.

The user must approve consequential new analyses before they are performed.

Example:

> “The apparent microbial-metabolism signal is strongly associated with medication use. An adjusted analysis is needed to determine whether the association persists independently of medication.”

This becomes an **analytical follow-up request**, rather than an unsupported biological conclusion.

---

# 21\. Evidence Hierarchy

Biological interpretations should integrate several evidence types.

### Statistical evidence

* effect size  
* statistical significance, reported as both raw p and FDR  
* tier (Section 6A)  
* direction-coherence across a family or class  
* robustness  
* covariate-adjusted associations  
* replication

### Chemical evidence

* annotation confidence  
* molecular-family membership  
* MS/MS similarity  
* network structure  
* mass relationships  
* related unknown features

### Biological evidence

* biochemical plausibility  
* known pathways  
* physiological relationships  
* known host/microbial/dietary origins

### Literature evidence

* peer-reviewed studies  
* mechanistic evidence  
* disease associations  
* experimental validation

### Repository evidence

* spectral recurrence  
* molecular-family recurrence  
* biological-context recurrence  
* independent cohort recurrence

### Cross-cohort evidence

* replication of features  
* replication of molecular families  
* replication of biological patterns  
* directionally consistent effects

No single evidence type should automatically determine the interpretation.

---

# 22\. Pattern-Level Biological Reasoning

The skill should actively search for broad biological states that may explain **multiple independent molecular observations**.

For each candidate biological pattern, ask:

1. What observations support the pattern?  
2. Are those observations chemically independent or part of the same molecular family?  
3. Are multiple molecular families involved?  
4. Do the changes move in biologically coherent directions?  
5. Are unannotated features contributing evidence?  
6. Does the statistical evidence support the pattern?  
7. Does the metadata support the interpretation?  
8. Does the literature support the interpretation?  
9. Does public-data recurrence support the interpretation?  
10. What observations would be expected if the hypothesis were true?  
11. Are those observations present?  
12. What alternative processes could produce the same pattern?  
13. Would an additional analysis help distinguish the alternatives?

The skill should prefer **convergent evidence from multiple sources** over a biological interpretation based on a single metabolite.

---

# 23\. Evidence and Provenance

Every important biological interpretation must maintain an evidence trail.

While the work is in progress, keep for each hypothesis, in the working file:

```yaml
hypothesis_id:
hypothesis:
category: established | plausible | exploratory

observations:
  - feature_or_family:
    statistical_evidence:
    direction:
    effect_size:
    robustness:

fbmn_evidence:
  - feature:
    annotation:
    molecular_family:
    network_relationship:
    unknown_features:
    relevant_mass_relationships:

literature_evidence:
  - claim:
    source:
    evidence_type:
    access_level:

repository_evidence:
  - resource:
    dataset:
    accession:
    search_parameters:
    result:
    biological_context:

additional_analyses:
  - question:
    proposed_analysis:
    user_approved:
    method:
    result:
    interpretation_impact:

supporting_evidence:
contradictory_evidence:
alternative_explanations:

confidence:
remaining_uncertainty:

testable_predictions:

next_investigation:
```

&nbsp;

**When the findings are published, this trail is what each one is made of.** A finding the user chose to pursue, and that the overlap table marks to be published, becomes one published judgment whose parts carry the trail:

* the **hypothesis** is what it claims, with the conditions it was observed under — the cohort, the comparison, the sample type, the ionization mode;
* each **observation** and each piece of **FBMN evidence** is evidence it points at, cell by cell, in the tables the analysis published or in the tables of an approved additional analysis;
* each piece of **literature** and **repository evidence** is evidence it points at in the source, or names, according to what was reached;
* what it **takes for granted** is stated as such — an annotation that is a library match and not a confirmed identity, a dietary or medication exposure nobody recorded;
* **contradictory evidence and alternative explanations** are part of the reasoning it gives, with what would distinguish each alternative;
* its **confidence**, the weakest part, and the **remaining uncertainty** are its judgment, in plain words;
* its **testable predictions** and **next investigation** say what would settle it.

A hypothesis the evidence does not yet bear on — offered because it is specific enough to be wrong — is published as a hypothesis and not as a finding, with what would confirm it and what would refute it.

How each of those parts is written, what may stand as evidence and what may only be named, is for the community's documents to say.

The skill must preserve provenance for evidence used to support a biological claim.

---

# 24\. Confidence and Language

The language of the final interpretation must match the evidence.

### Strong evidence

Use:

* “is consistent with”  
* “supports”  
* “is associated with”  
* “provides evidence for”

### Moderate evidence

Use:

* “suggests”  
* “may reflect”  
* “is compatible with”  
* “raises the possibility of”

### Exploratory evidence

Use:

* “raises the hypothesis that”  
* “could potentially reflect”  
* “provides a speculative explanation”  
* “warrants investigation”

Avoid unsupported language such as:

* “proves”  
* “demonstrates that X causes Y”  
* “confirms the mechanism”  
* “X is responsible for Y”

unless the experimental evidence genuinely supports that conclusion.

---

# 24A. Response Structure (every response and report)

Every response and report centers biological interpretation. The interpretation is always offered without being asked, and it comes first: a one-to-two-sentence statement of what the finding might mean sits directly under the finding's heading (or at the top of the chat answer), and the supporting detail follows. For each finding or pattern, use this structure, tagging every claim as **Observed**, **Inferred** or **Speculative**:

0. **Key interpretation (first line)**: what it might mean, in plain words, with its confidence tag.

1. **The route**: the known biology around the finding, so the reader can place it (for example the pathway, the cell types, the microbial role).

2. **What changed** (*Observed*): direction, size and the number of features, with one compact line of statistics that includes the raw p-value and q-value.

3. **What it might mean** (*Inferred* / *Speculative*): the likely biological interpretation, with the plausible alternatives stated.

4. **Possible causes**: the processes that could produce the change, including non-biological or confounding explanations.

5. **Possible consequences**: what the change could mean for the host, the microbiome or the disease course.

6. **Why it is useful**: the question it answers or the marker it could provide, and what would distinguish the competing explanations.

7. **Key figure**: the inline figure for this finding (Section 24B).

8. **Things I need from you**: recommendations and questions, at the end of the response.

Rules:

* Do not present a stack of statistics or feature lists without the biological meaning.  
* If a result is uninterpretable, say so and say what would make it interpretable.  
* Biological meaning is never replaced by a p-value, a table, or a list of identifiers.  
* Do not leave an approved interpretation without stating what would change it.  
* Do not make the user ask for the biology. If a response contains results and no interpretation, it is incomplete.  
* Do not defer interpretation to the end of a response or report.

---

# 24B. Key Figures in Chat

When chatting, show the key figure for each pattern or finding as it is discussed, so the user can see the result and not only read about it. Do not hold figures back for the reports.

**What to show**

* One key figure per pattern or finding, chosen to show the result the interpretation rests on. Typical choices: group comparison dots with mean and error bars; trajectory over time by group; family-level direction plot (members lower versus higher); feature-versus-metadata scatter; a network component with nodes colored by direction of change; or a before/after comparison of broad class versus sub-class (Section 7A).  
* When a hypothesis has a known mechanism chain, a small interpretation schematic is appropriate alongside the data figure (observed boxes solid, interpreted boxes dashed).  
* For the emerging patterns (Section 5A), show one or two summary figures covering all patterns first, then a small figure for each pattern that needs one, or one compact multi-panel figure for the weak or redundant ones. Keep each figure simple and quick to read.
* **How to read it:** every figure shown in chat has a 1 to 2 sentence "How to read this figure" line directly under it, in plain language: what the axes, colors, symbols or boxes mean, and what pattern to look for (for example "Each dot is one sample; the bar is the group mean. Higher dots mean more of the feature; the gap between groups is the effect."). Write it for a reader who has not seen this type of plot. It does not repeat the finding.

**Figure rules**

* Every figure states the group sizes (n), the comparison, and the statistic (raw p; q where it applies) in the caption or panel title.  
* Label what is observed and what is interpreted. Never place an interpretive claim in a data panel.  
* Use the group colors the user chose at intake, the same for the same groups throughout the session and in the reports. Do not assume a color scheme; ask first.  
* Show individual samples or patients where numbers are small.  
* Show null results when they bear on the interpretation (for example a class that does not differ).  
* Figures shown in chat are carried into the reports; keep the figure source data and the code so they can be regenerated and published with the report.  
* Number chat figures provisionally (for example "Fig. A", "Fig. B") and renumber in the reports. Do not reuse a label for a different figure.  
* If a figure cannot be made from the available data, say what is missing and what would make it possible.

**Do not**

* Paste a figure without its interpretation, or an interpretation of a finding without its figure.  
* Make decorative figures that carry no result.

---

# 25\. Biological Pattern Versus Mechanistic Claim Versus Biological Impact

The skill must distinguish between:

### Pattern

> Metabolites associated with inflammatory responses are elevated.

### Biological interpretation

> The metabolomic profile is consistent with an inflammatory state.

### Mechanistic hypothesis

> Inflammation drives the observed metabolic changes.

### Impact hypothesis

> The observed metabolic changes worsen symptoms through X mechanism.

All four should be included in reports, worded carefully if there is not sufficient evidence to fully support a hypothesis.

---

# 26\. Cross-Cohort Interpretation

When multiple datasets are available, use them to distinguish:

* cohort-specific observations  
* reproducible molecular signals  
* reproducible biological patterns  
* population-specific effects  
* technical differences  
* potentially generalizable biology

When possible, distinguish:

> discovery

from:

> independent replication.

Do not describe a second dataset as independent validation if there is substantial sample, cohort, or repository overlap.

Cross-cohort disagreement should itself be investigated rather than treated simply as failure.

Potential explanations include:

* population differences  
* disease severity  
* medication  
* diet  
* sample type  
* technical differences  
* biological heterogeneity  
* different molecular manifestations of the same biological process

---

# 27\. Negative and Contradictory Evidence

The skill must actively retain contradictory findings.

A hypothesis should not become stronger merely because supporting evidence accumulates.

Ask:

* Are expected metabolites absent?  
* Are related features moving in opposite directions?  
* Does the hypothesis fail in another cohort?  
* Does adjustment eliminate the association?  
* Does repository evidence suggest the chemistry is nonspecific?  
* Does another biological process explain the pattern better?

Contradictory evidence should appear in the final interpretation.

---

# 28\. Stopping Criteria

The iterative process should stop when one or more conditions are met:

1. additional FBMN interrogation produces no new information;  
2. additional repository searches do not materially change the interpretation;  
3. literature searches have reached reasonable saturation;  
4. the hypothesis has sufficient convergent evidence;  
5. the hypothesis has been substantially contradicted;  
6. remaining uncertainty cannot be resolved using available data;  
7. resolving the question requires a new experiment rather than another analysis;  
8. the user declines a proposed additional analysis;  
9. additional investigation is unlikely to change the biological interpretation.

The goal is not to generate the maximum number of hypotheses.

The goal is to generate the **most informative, evidence-supported interpretations that can reasonably be obtained from the available data**.

---

# 29\. Prioritization

The skill should prioritize findings for deeper investigation based on scientific value, not simply statistical significance.

Potential considerations include:

* strength of statistical evidence, including raw-p and trend tiers (Section 6A)  
* directional coherence across a family or class  
* effect size  
* robustness  
* molecular-family coherence  
* number of independent observations  
* presence of informative unknowns  
* cross-feature coordination  
* cross-cohort recurrence  
* repository recurrence  
* biological plausibility  
* novelty  
* potential to generate a testable hypothesis  
* importance to the biological question  
* whether resolving the finding could materially change the biological interpretation

Do not collapse these considerations into an opaque numerical score unless explicitly requested.

Instead, explain why a finding was prioritized.

---

# 30\. What the Skill Should Add Beyond Conventional Analysis

The skill should explicitly identify what biological interpretation was enabled by integrating:

* unannotated FBMN features  
* molecular-family structure  
* coordinated feature behavior  
* broad biological patterns  
* repository context  
* literature  
* iterative hypothesis testing  
* user-approved additional analyses

A useful interpretation should answer:

> What did the integrated reasoning reveal that would be difficult to identify from a conventional list of statistically significant metabolites alone?

Examples might include:

* an unknown molecular family associated with a phenotype  
* a biological process represented across several unrelated chemical classes  
* evidence for host–microbe interactions that is not apparent from individual metabolites  
* a recurring biological pattern across independent datasets  
* an unexpected alternative explanation for a statistical association  
* a novel but testable biological hypothesis

---

# 31\. Final Output

Interpretation ends in **two reports**, drafted as [REPORT.md](REPORT.md) sets out (layout, visual style, numbering, schematics, brevity), shown to the user, and published once the user approves them.

## 31.0 What interpretation publishes

The names, topics and shapes are fixed in [RECORD.md](RECORD.md); the table below says what each part is for.

| Published | Content |
| :---- | :---- |
| The question | The user's request for interpretation, verbatim, linked to the question the analysis served |
| Pointers | What the library holds of each table and each source a finding rests on (rows or text, exactly), each linking back to the library |
| Additional analyses | Each approved analysis with its method, parameters and code, and the tables it produced |
| Findings | One per pursued pattern or hypothesis that the overlap table marks to be published, carrying the evidence trail of Section 23 |
| Hypotheses | Each exploratory hypothesis (Section 34), with what would confirm and refute it |
| Figures | Every report figure, numbered as in the reports, each beside the table it plots, with its "How to read this figure" line |
| The report | The full report's content; the main report is built from it |

The intake decisions and parked items stay in the working file. Where they changed a result — a threshold, a scope, an approved adjustment — the analysis or finding they changed states them.

**Main report (short).** Contains: the question, verbatim, at the top of page 1; a one-page summary (the plain-language summary with its literature tie-ins, the overall biological interpretation, the findings table and the Key references box; [REPORT.md](REPORT.md), Section 4C); the **Molecular-network discovery questions** section (Section 5B; report layout in [REPORT.md](REPORT.md), Section 6A), directly after the summary; the key findings (one section each, interpretation directly under the heading, with the figures and the interpretation schematic each finding needs); the most important contradictory evidence and limits; what this means for the biological question; testable predictions and next tests; sources. It does not contain method detail, secondary findings, full unannotated-feature tables, the full hypothesis record, or null results (unless the user requested specific null results at intake).

**Full report.** Contains everything in the main report (including the question at the top and the Molecular-network discovery questions section when approved, with every item rather than the top 3) and adds: every pattern investigated, including all null and contradictory results; the filter-loss review (from the unfiltered table); the multi-level class analyses (Section 7A); the unannotated feature report (Section 32); the biological pattern summary (Section 33); exploratory hypotheses (Section 34); additional analyses and their results; alternative explanations; diet and medication assessment (Section 13A); and complete follow-up (Section 35).

**Rules**

* The main report and the full report must agree. Every number, figure and conclusion in the main report appears identically in the full report. Use the same figure numbers where a figure appears in both, or cross-reference (for example, "full report, Fig. 14").  
* Both reports lead each section with its biological interpretation (Section 24A).  
* Revise the drafts as the user asks, in the run's folder. Once approved and published, a further change is a report that supersedes the earlier one and says what changed and why.  
* Do not deliver one report without the other unless the user asks.

The full report should be organized around **biological findings and patterns**, not simply feature lists.

## 31.1 Executive summary

Summarize:

* major biological patterns, each using the structure in Section 24A  
* strongest established interpretations  
* strongest plausible interpretations  
* most interesting exploratory hypotheses  
* additional analyses performed  
* major uncertainties  
* important alternative explanations

## 31.2 Biological findings

For each major finding:

### Finding

Short description of the biological pattern.

### Observed evidence

Features, molecular families, statistical behavior, and metadata associations.

### FBMN context

Relevant network structure, annotations, unknowns, and molecular relationships.

### Biological interpretation

What the pattern may represent.

### External evidence

Relevant literature, repository evidence, and cross-cohort evidence.

### Additional analysis

Any analysis performed to investigate the hypothesis, including why it was requested and what it showed.

### Alternative explanations

Other mechanisms or technical/biological explanations.

### Confidence

Established / Plausible / Exploratory.

### Remaining uncertainty

What is not known.

### Testable prediction

What future experiment or analysis could distinguish the hypothesis.

---

# 32\. Unannotated Feature Report

Include a dedicated section for informative unknowns.

For each important unknown:

* feature ID  
* molecular family  
* neighboring annotated features  
* network relationships  
* statistical behavior  
* related unknown features  
* relevant mass differences  
* repository recurrence  
* proposed structure or formula, with evidence basis, confidence and alternatives (where one can be supported)  
* potential biological interpretation  
* confidence  
* what would be required for identification/validation

Unknown features should not be hidden in an appendix simply because their structures are unresolved.

---

# 33\. Biological Pattern Summary

Provide a separate synthesis of higher-order biological patterns.

For example:

| Biological pattern | Supporting molecular evidence | FBMN evidence | External evidence | Contradictory evidence | Additional analysis | Confidence |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| Inflammation | ... | ... | ... | ... | ... | Plausible |
| Altered microbial metabolism | ... | ... | ... | ... | ... | Established |
| Dietary contribution | ... | ... | ... | ... | ... | Exploratory |
| Oxidative stress | ... | ... | ... | ... | ... | Plausible |

&nbsp;

The table should summarize evidence rather than replace the underlying reasoning.

---

# 34\. Exploratory Hypotheses

Maintain a dedicated section for novel or speculative ideas.

Each should include:

* hypothesis  
* observations that generated it  
* why it is biologically plausible  
* what evidence supports it  
* what evidence is missing  
* alternative explanations  
* additional analyses that could test it  
* whether those analyses were approved/performed  
* predicted observations  
* experiment or analysis needed to test it

Novelty should never be treated as evidence.

---

# 35\. Recommended Follow-Up

Separate computational follow-up from experimental follow-up.

### Computational

* targeted re-analysis  
* additional metadata adjustment  
* additional FBMN interrogation  
* MassQL query  
* MASST search  
* ReDU analysis  
* MetaboApps DrugReadout and FoodReadout, when medication or dietary intake data are missing (Section 13A)  
* MASST searches, PostMN MassQL, Conjugated Metabolome Explorer for a pattern under investigation (Section 13C; needs approval)  
* multi-level re-testing of a class at a finer sub-class level (Section 7A)  
* class balance score for notable classes, with and without VIP weighting (Section 13B; needs approval)  
* cross-cohort analysis  
* targeted feature extraction  
* structural annotation  
* targeted statistical test

### Experimental

* targeted metabolite measurement  
* authentic-standard confirmation  
* MS/MS confirmation  
* isotope tracing  
* microbial culture  
* perturbation experiment  
* dietary intervention  
* mechanistic validation

The skill should not imply that a computational observation has been experimentally validated.

---

# 36\. Human Review

Human expert review remains part of the interpretation process.

The expert should be able to inspect:

* the original observation  
* statistical evidence  
* molecular-network context  
* literature evidence  
* repository evidence  
* contradictory evidence  
* alternative explanations  
* the reasoning that led to the hypothesis  
* proposed additional analyses  
* analyses that were performed  
* proposed follow-up

The user should be able to:

* approve an analysis  
* reject an analysis  
* modify an analysis  
* request a different analysis  
* accept an interpretation  
* modify an interpretation  
* reject an interpretation  
* request further investigation

The skill must preserve the distinction between:

> **AI-generated hypothesis**

and:

> **human-validated biological conclusion.**

---

# 37\. Final Interpretation Principles

The skill should always follow these rules:

1. **Do not equate statistical significance with biological importance.**  
2. **Do not ignore unannotated features.**  
3. **Propose structures for unknowns only with an evidence basis, a confidence level and alternatives; never present a tentative structure as identified.**  
4. **Do not restrict interpretation to predefined chemical classes.**  
5. **Search for coordinated patterns across molecular families.**  
6. **Search for higher-order biological states and processes.**  
7. **Use both bottom-up and top-down reasoning.**  
8. **Use FBMN as a discovery tool, not merely a visualization.**  
9. **Use literature to test specific claims rather than decorate interpretations with citations.**  
10. **Distinguish spectral recurrence from biological recurrence.**  
11. **Actively search for contradictory evidence.**  
12. **Consider alternative explanations.**  
13. **Label established, plausible, and exploratory interpretations separately.**  
14. **Maintain evidence provenance.**  
15. **Do not silently redo analytical decisions.**  
16. **When a biological question requires new analysis, propose it explicitly.**  
17. **Obtain user approval before performing consequential additional analyses.**  
18. **Record all approved additional analyses and their outcomes.**  
19. **Use new analytical results as evidence, not automatic confirmation.**  
20. **Return to FBMN, literature, and repository interrogation after new analyses when appropriate.**  
21. **Generate testable hypotheses rather than unsupported mechanistic stories.**  
22. **Stop when additional interrogation is unlikely to change the interpretation.**  
23. **Make uncertainty explicit.**  
24. **Prioritize biological patterns over isolated metabolite annotations.**  
25. **Keep the human reviewer in control of consequential analytical decisions.**  
26. **Review what filtering removed before interpreting, using the unfiltered table the analysis published; never change filters silently.**  
27. **Pause after the first scan with all emerging patterns evaluated and summarized (summary table and one or two summary figures), not a report. Never cap the number.**  
28. **Do not restrict interpretation to FDR-passing features; always report raw p alongside q and label tiers.**  
29. **Treat coherent direction across a family as evidence.**  
30. **Center every response on biological meaning, causes and consequences, tagged Observed, Inferred or Speculative.**  
31. **End every response with "Things I need from you."**  
32. **Run Intake once, keep the answers in the working file, and do not re-raise parked items.**  
33. **Show the key figure with every finding discussed in chat.**  
34. **State biological interpretation and hypotheses without being asked, in chat and in reports, and put them first.**  
35. **Analyze each class at broad and narrow levels, and compare the levels.**  
36. **When diet or medication is an unexcluded explanation and intake data are missing, recommend DrugReadout and FoodReadout.**  
37. **Deliver two reports (short main and full), drafted, approved, then published.**  
38. **Propose a class balance score for notable classes (Section 13B), with the group of interest as the numerator in data-driven variants, and always get user approval first.**  
39. **Answer the three molecular-network discovery questions against the question alongside the emerging patterns, in chat and in both reports, once the user has approved this default (Section 5B).**

---

# 38\. Conceptual Output

The final product of this skill is not:

> “These 25 metabolites were significant and belong to these pathways.”

It is:

> **“These are the major biological patterns present in the data, this is the molecular-network evidence underlying each pattern, these annotated and unannotated features contribute to the pattern, this is what is already established, this is what is biologically plausible but unresolved, these are the more speculative hypotheses, these are potential causes and consequences of these findings, these observations argue against alternative explanations, these additional analyses were identified and—where approved—performed, and these experiments or analyses would distinguish the remaining possibilities.”**

The skill should function as an **iterative scientific investigator** rather than a static metabolite-annotation or pathway-generation tool.