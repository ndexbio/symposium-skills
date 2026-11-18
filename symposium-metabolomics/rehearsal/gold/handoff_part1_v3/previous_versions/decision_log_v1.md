# Decision log v1 (Part 1): MSV000082221, surgery and the fecal metabolome

Task: GNPS2 EB `a9552f8e5018401ba4af91934f916289` (gnps2.org, everything_bagel_workflow 2026.11.03, fbmn, positive). Date 2026-11-12. Skillset v12.

| Block | Status / decision | Detail |
|---|---|---|
| input_files | done | All originals in `user_supplied_input_files/` with `input_files_manifest.csv`. GNPS2 connector not available; files pulled from gnps2.org. Library search output downloaded but NOT used (user's `eb_curated_annotations_MSV000082221.tsv` used). Qiita metadata `11546_..._metadata.txt` (same MSV folder) used for surgery fields. |
| design | user approved | Exposure = `has_surgery` y vs n (prior surgery). Initial = baseline CD Welch test; over time = log2 ~ surgery x month + (1/subject) mixed model (all CD samples) + per-time-point Welch tests. Primary = CD (193 samples, 75 people). UC descriptive only (7 baseline surgery samples, 5 people, all colectomy+pouch). |
| sample_linkage | done | 324 of 334 study injections linked (`PLCL<id>` = Qiita `anonymized_name`). 10 unlinked excluded. |
| raw_vs_normalized | user | Raw peak areas, gap-filled. |
| internal_standards | user-provided | Sulfadimethoxine (resuspension): intact, feature 79, 332/334 samples. Sulfamethazine (extraction): feature 253 RT 2.60, 56/334 samples, 11/11 std mixes; essentially absent from samples. Metadata lists other standards (sulfamethizole, sulfachloropyridazine); not used. |
| feature_merge | user approved: none | 166 candidate pairs (5 ppm, 0.1 min); 10 spectra-supported review pairs, 139 review, 17 do not merge. No XIC available. Merge map empty. |
| batch_correction | not possible | No pooled QCs. Four plates; plate-adjusted baseline model agrees (r=0.997). |
| blank_filter | user approved | Mean(324 study samples) / mean(33 solvent blanks) >= 5. 1,183 fail. |
| prevalence_filter | user approved | Detected in >= 20% of samples in at least one CD surgery group (all time points). 11,242 retained. |
| normalization_comparison | run; applied | status: run. Recommended and applied: sum (TIC) over the retained features, scaled to the median. rCLR sensitivity. IS normalization not applied (user). |
| zeros | user approved | Zero -> half minimum positive normalized value per feature, log2. |
| unfiltered_table | on | Same samples, factors, imputation; max abs diff of retained values = 0. Separate unfiltered-family q. |
| detection_rate | on | Samples counted: 193 CD. |
| molecular_network | on | 2,928 nodes, 4,629 edges, 524 families, 5,964 singletons (nodes + singletons = 8,892 MS/MS features). |
| compound_classes | rule-based | 193 of 1,246 annotated unclassified (list provided). |
| outliers | flag only | 2 CD samples (T2 > 99.9%) kept. |
| statistics | done | Welch t, OLS adjusted (sex, steroid, TNF inhibitor, antibiotics, immunomodulator), MixedLM REML, PLS-DA (5-fold CV, 200 permutations), PERMANOVA-style R2. BH within filtered family; separate unfiltered family. Volcano cutoff raw p < 0.05 and abs(log2FC) >= 0.58. |
| removed_feature_review | done, nothing re-added | 411 flagged; awaiting user decision. |
| report | v1 | `MSV000082221_part1_report_v1.pdf` |
