# Answers for the rehearsal run

Keep this file where the session under test cannot read it.

Taken from the skill author's session on MSV000082221 with the skill this one was built from
(28 user turns). Each row is one decision the
user made, keyed by **what it decides**, in the order it came up. Question numbers and pattern
IDs (P1, P19, ...) belong to that one session; a new run numbers things differently, so match on
the meaning and give the answer in the right-hand column.

Where a run asks something not listed here, take its recommendation and note that it did.
Where a run does not ask something listed here, note that too.

## Facts supplied in the first prompt

| What | Value |
|---|---|
| Question | How surgery impacts the metabolome, both initially and over time |
| GNPS2 Everything Bagel task | `a9552f8e5018401ba4af91934f916289` |
| Sample metadata | `gnps_metadata_MSV000082221.tsv` (user file) |
| Annotations | `eb_curated_annotations_MSV000082221.tsv` (user file). Use these, not the task's library hits |
| Run order | `CMI_IBD_fecal_metadata_ms_positive.xlsx` (user file) |
| Internal standards | sulfamethazine (extraction); sulfadimethoxine (added at resuspension) |
| Also in the input folder, not named in the prompt | `11546_20230209-165600_metadata.txt` (Qiita study 11546; holds the surgery fields) |
| Not supplied | the original paper; sequence-file batch labels beyond the run-order workbook |

## Where it publishes, and as whom

| What | Answer |
|---|---|
| Library community | the one the prompt names; its publishing member is the member set up for this rehearsal |
| Interpretation community | the one the interpret prompt names |
| The gate | the admin context set up for each community; start it watching |
| The reuse table, on a first run | nothing to reuse |
| The overlap table, on a first run | nothing there; every finding is new |
| What leaves this machine | Yes, publish the question as written, and store the four input files |

## Analysis (Part 1)

| # | What it decides | Answer |
|---|---|---|
| A1 | How "surgery" is defined | Prior surgery at the sample (yes vs no) as the exposure. "Initially" is the baseline comparison; "over time" is a surgery × timepoint model with subject as a random effect. Do not make `subsequent_surgery` the primary analysis |
| A2 | Whether the primary analysis is Crohn's disease only | First ask whether the 16 UC surgery samples come from 16 different people. Once told they are 5 people, all J-pouch: yes, CD primary, UC descriptive only, no pooling |
| A3 | Whether the feature table is raw | Yes, raw |
| A4 | Feature merges: recommend with evidence, apply only approved ones | OK |
| A5 | Report format and group colours | Accept the default: PDF, colour-blind-safe palette, surgery vs none as the main contrast |
| A6 | Molecular-network analysis on | Confirmed |
| A7 | Which merges to apply | None (the recommendation) |
| A8 | Blank filter | Solvent blanks, sample/blank mean ratio at least 5 |
| A9 | Prevalence filter | Detected in at least 20% of samples in at least one CD surgery group |
| A10 | Normalization | Sum (TIC), with rCLR as a sensitivity check. No internal-standard normalization |
| A11 | Zero handling | Replace zeros with half the feature's minimum positive value before log2 |
| A11b | How the baseline and over-time comparisons are tested | Baseline: a Welch t-test per feature, surgery vs none, on the first-visit samples. Over time: a per-feature mixed model fitted with statsmodels MixedLM (REML), log2 abundance ~ surgery x month, random intercept per subject, Wald z tests. Benjamini-Hochberg within the retained family for each term |
| A12 | Adjust for time since surgery | Ask whether it is needed and available; on hearing why it is not an ordinary covariate: skip it |
| A13 | Removed features flagged for review | Add back those removed by the prevalence filter only. Those removed by the blank filter stay out. Contaminants and additives are not added back |
| A14 | Unclassified annotations list | Fine as it is |
| A15 | Which technical next steps to run | Presence/absence models, and stratifying by surgery type. Not the within-person analysis of the three people who changed status |
| A16 | Merge the added-back features into the primary family | Yes |
| A17 | Add back any still-flagged or zero-detection features | No |
| A18 | Act on the proposed detection checks (XICs, high-prevalence subset) before going on | No, proceed |
| A20 | A sample found to be blank-like or an outlier | Keep it in the primary analysis; report the result without it as a sensitivity analysis only (the author's run flagged outliers and kept them) |
| A21 | Inconsistent person or sample records | Keep as recorded and flag |
| A19 | The draft technical report | Approve it once A13–A17 are reflected |

## Interpretation (Part 2)

| # | What it decides | Answer |
|---|---|---|
| I1 | Intake defaults (audience, sources, thresholds, all patterns evaluated, key figures, two reports) | Approve all |
| I2 | Network discovery questions on, 3 items each | Approve |
| I3 | Main report length; null results in it | 8 to 12 pages; no null results in the main report |
| I4 | Feature scope | Limit to features with MS/MS |
| I5 | Adjusted or unadjusted first | Lead with unadjusted; check adjusted for anything highlighted |
| I6 | Areas to leave out of the scan | None |
| I7 | Which patterns to pursue | Bile acids and their anatomy patterns, urobilinoids, the lipid patterns (lauroylcarnitine, N-acyl amides and the related lipid sets), and the **features-detected-per-sample pattern**. Not the PEG pattern, even if recommended |
| I8 | Plate-adjusted over-time model | Run it |
| I9 | Model separating ileal loss, colon loss and ostomy | Run it |
| I10 | Medication and diet records; DrugReadout and FoodReadout | No records. Park it; remind later |
| I11 | MASST and MassQL follow-ups | Park; remind later |
| I12 | Whether plate adjustment is valid given time and plate are collinear | Raise this when the plate-adjusted result is shown |
| I13 | Within-plate, within-person sensitivity analysis on time | Yes |
| I14 | Correction to the analysis's over-time wording ("inconclusive") | Yes |
| I15 | Exploratory antibiotic adjustment for the bile-acid and urobilinoid patterns | Yes |
| I16 | Build the reports | Yes, main and full |
| I17 | UC consistency check (UC J-pouch against CD J-pouch) with a UC limitation line | Ask why UC checks are missing; then: yes, run it and add it |
| I18 | Further analyses offered after that | Disease-activity and medication adjustment (covariate adjustment approved), and the ileal-versus-colon model with the bile-acid balance score. Not the check of other IBD datasets |
| I19 | Add those to the reports | Yes |
| I20 | PEG and presence-only checks; before-and-after analysis of the three status-changers | Wait for now |
| I21 | The draft biology report | Approve it once I13–I19 are reflected |

## What the author's run did that the answers depend on

- The GNPS2 connector was not available; files came by direct download from gnps2.org.
- The task's library-search results and gap-fill report were fetched and not used.
- Batch correction was not possible (the check ran; no correction applied).
- Every literature source was reached at summary level only.
