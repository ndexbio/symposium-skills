# Part 1 hand-off package v3: MSV000082221 (surgery and the fecal metabolome in IBD)

Created 2026-11-12. Technical and statistical hand-off only; no biological interpretation. Final report: `MSV000082221_part1_report_v3.pdf`. Decision record: `decision_log_v3.md` (v1 and v2 logs and reports are in `previous_versions/`, superseded).

## 1. Question (verbatim first prompt: `input_prompt_v1.txt`)
How surgery impacts the metabolome, initially and over time. Primary comparison: Crohn's disease (CD), 193 samples from 75 people (surgery 92 samples / 36 people, no surgery 101 / 42; 3 people change status). Baseline: surgery n=32 vs none n=39. Time points: baseline, about 6, 12, 18+ months. UC (5 surgery people, all colectomy with pouch) descriptive only.

## 2. Source information
- GNPS2 Everything Bagel task `a9552f8e5018401ba4af91934f916289` on gnps2.org (everything_bagel_workflow, server 2026.11.10, workflow 2026.11.03; fbmn; positive mode; MSV000082221). Row IDs in every file below refer to this task's `aligned_features.csv` `row ID`.
- Retrievable from the task: feature table (`feature_finding/feature_finding_results/aligned_features.csv`), consensus MS/MS (`feature_finding/aligned_features_filled.mgf`), network (`networking/filtered_pairs.tsv`, `network.graphml`, `network_singletons.graphml`), gap-fill report. GNPS2 connector was not available; files were downloaded from gnps2.org.
- Library annotations: the user's curated file `eb_curated_annotations_MSV000082221.tsv` (1,246 features, one row per feature; query_scan = row ID). The task's own library search output was downloaded but NOT used.
- Metadata: `gnps_metadata_MSV000082221.tsv` (user), run order `CMI_IBD_fecal_metadata_ms_positive.xlsx` (user), and the Qiita study metadata `11546_20230209-165600_metadata.txt` (same MSV000082221 folder; holds surgery, time point and medication fields). Linkage: MS file `PLCL<id>` = Qiita `anonymized_name` `<id>`; 324 of 334 study injections linked, 10 excluded.
- Every original input is in `user_supplied_input_files/` with `input_files_manifest.csv` (origin, source, size, note).

## 3. Data-state note (read before using any table)
- Values: EB peak areas (feature_quant = peak_area), gap-filled, raw upstream. A zero means not detected. About 75% of cells are zero; the median feature has about half of its values imputed.
- Processing (identical for the filtered and unfiltered tables): TIC (sum) normalization, with per-sample factors computed over the 11,363 final retained features and scaled to the median factor; zeros replaced by half the feature's minimum positive normalized value (per feature, over all 324 samples); log2. Gap-fill is included in detection counts; `gap_fill_report.tsv` was not used.
- Filters: blank ratio (mean of 324 study samples / mean of 33 solvent blanks) >= 5; prevalence >= 20% of samples in at least one CD surgery group; then 121 flagged features removed only by prevalence were added back (user decision; not contaminant class; testable in CD). Primary family = 11,363 features. Column `origin` in the per-feature tables: `v1_primary` or `added_back_v2`; the added-back features were selected on signal and are exploratory.
- Testability: 1,481 features are detected in fewer than 3 CD samples; their CD tests are set to missing (`testable_CD` = false). 223 flagged zero-detection features were held out.
- The unfiltered table (24,770 features) uses the same factors and imputation; retained values are identical in both (max absolute difference 0.0, `tables/unfiltered_filtered_validation_v3.json`). Unfiltered-family q is a separate column; primary q (`*_q_filtered`) is BH within the 11,363 features, per test. Removed-feature results are exploratory.
- Batch and drift correction: not possible (no pooled QCs); every `batch_corrected` value is `no`. Four plates; plate adjustment gave the same baseline effects (r = 0.997).
- Internal standards: sulfadimethoxine (resuspension) intact (feature 79); sulfamethazine (extraction) mostly absent in samples (feature 253 in 56 of 334). No IS normalization applied (user).
- No pooled QCs, no age or BMI. Surgery is prior surgery (not time since surgery); the time-since-surgery analysis was skipped by decision.

## 4. Key technical results (details in the report)
- Baseline CD: 1,540 of 11,363 features at q < 0.05 (1,228 lower and 312 higher in surgery); median log2FC about -0.44. Mixed model (surgery x month, subject random effect): surgery effect at month 0 q < 0.05 for 3,585 features; surgery x time interaction q < 0.05 for 16.
- Much of the signal is detection: 727 of 752 baseline-significant features in the 6,907 features with >= 50% imputed CD values also differ in detection frequency (same direction). PC1 tracks features detected per sample (rho about -0.82).
- Surgery type at baseline (none 39, ileocolonic 19, colectomy 11): similar shifts (per-feature r about 0.62).

## 5. Open items and next steps (all need approval)
Open: review 66 still-flagged removed features; decide on 10 spectrally supported merge pairs once chromatograms are checked in GNPS2; handle 10 unlinked samples; added-back features are exploratory. Technical next steps: plate-adjusted over-time model; within-person analysis of the 3 status-changers; re-check the extraction standard in GNPS2 chromatograms; add surgery type to the over-time model. Areas of interest for Part 2 are listed neutrally in report Section 19.

## 6. File index
| Path | Content |
|---|---|
| `MSV000082221_part1_report_v3.pdf` | Final Part 1 report (23 pages) |
| `decision_log_v3.md` | Decision log v3 (changes from v2) |
| `previous_versions/` | v1 and v2 reports and decision logs (superseded) |
| `input_prompt_v1.txt` | First prompt of the run, verbatim |
| `tables/per_feature_results_v3.csv` | Primary results, 11,363 features: effect sizes, CI, raw p, q, annotation, flags, sensitivity label, `origin`, `batch_corrected` |
| `tables/unfiltered_per_feature_results_v3.csv` | Same columns for all 24,770 features, plus retained flag, removal reason, detection counts, imputed fractions, detected-only effect, separate unfiltered-family q |
| `tables/filter_table_v3.csv` | Per-feature filter results, blank ratio, prevalence by group, rescue flag and reason |
| `tables/processed_filtered_log2_tic_v3.csv.gz`, `processed_unfiltered_log2_tic_v3.csv.gz` | Processed (normalized, imputed, log2) tables, features x 324 samples |
| `tables/sample_table_v3.csv` | Sample metadata used (subject, disease, surgery, time point, covariates, plate, run order, features detected, TIC factor) |
| `tables/unfiltered_filtered_validation_v3.json` | Validation record for the two tables |
| `tables/internal_standard_check_v3.csv` | Internal-standard check |
| `tables/feature_merge_candidates_v3.csv`, `feature_merge_map_v3.csv` (empty), `feature_merge_review_sheets_v3.pdf` | Merge recommendation files |
| `tables/batch_correction_v3_check_summary.json`, `group_by_plate_CD_v3.csv` | Batch correction check (not possible) and group-by-plate table |
| `tables/detection_rate_*_v3.csv` | Detection-rate bins, cumulative rows, per-feature table |
| `tables/network_*_v3.csv`, `compound_class_*_v3.csv` | Network summary, family sizes, families, nodes, edges, delta-mass inventory; class assignments, composition and colour key |
| `tables/unclassified_annotation_names_v3.csv` | Annotations the rule-based classifier left unclassified (193) |
| `tables/presence_absence_results_v3.csv`, `surgery_type_stratified_baseline_v3.csv` | Next-step analyses |
| `tables/interaction_q05_features_v3.csv`, `timepoint_summary_v3.csv`, `sample_level_diagnostics_by_timepoint_v3.csv` | Over-time results |
| `tables/pca_scores_CD_v3.csv`, `plsda_vip_baseline_CD_v3.csv`, `metadata_drivers_permanova_v3.csv` | Multivariate and metadata-driver tables |
| `tables/removed_feature_flags_v3.csv`, `held_out_zero_detection_features_v3.csv`, `removed_annotated_by_class_v3.csv`, `study_context_compounds_check_v3.csv` | Removed-feature review |
| `tables/sensitivity_plate_adjusted_baseline_v3.csv`, `uc_descriptive_baseline_log2FC_v3.csv` | Sensitivity and descriptive UC tables |
| `figures/` | All report figures (PNG) with source CSVs where made |
| `code/code_v1`, `code_v2`, `code_v3` | All scripts (v3 regenerates v1 and v2 scripts on the merged family) |
| `user_supplied_input_files/` | Original inputs, unchanged, with `input_files_manifest.csv` |
| `handoff_manifest_v3.csv` | List of every file in this package with size |
