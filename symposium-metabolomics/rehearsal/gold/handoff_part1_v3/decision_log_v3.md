# Decision log v3 (Part 1): MSV000082221. Changes from v2; v1 and v2 files and reports are unchanged.

| Block | Status / decision | Detail |
|---|---|---|
| rescued_features_family | user decision, applied | The 121 added-back features (flagged, prevalence-only, testable in CD, not contaminants) are merged into the primary family. Final primary family = 11,363 features (11,242 + 121). Column `origin` in `per_feature_results_v3.csv` = `v1_primary` or `added_back_v2`. |
| q_values | recomputed | BH q recomputed within the 11,363 features for every test (columns `*_q_filtered`). Baseline q < 0.05: 1,552 (v1, v2) -> 1,540. Only 4 of the 121 added-back features keep baseline q < 0.05 in the merged family (v2's separate-family q of 121 of 121 was misleading). |
| normalization | recomputed | TIC factors recomputed on the 11,363 final features; same factors applied to the unfiltered table (max |log2 change| in any sample 0.04, median 0.0006). Normalization comparison (Section 7) not rerun (run on the 11,242-feature set). |
| analyses_rerun | done | Zero imputation, Welch, adjusted OLS, mixed models, rCLR sensitivity, PCA, PLS-DA, PERMANOVA-style drivers, plate-adjusted model, network node/class tables and volcano figures, presence/absence (Fisher, GEE), surgery-type stratification. |
| testability_correction | carried from v2 | Features with fewer than 3 CD detections (1,481) have CD test results set to missing; unfiltered-family q recomputed. 223 flagged zero-detection features held out (not testable). |
| removed_feature_review | updated | 13,407 features removed; 66 remain flagged (30 exploratory baseline signal, 37 annotated removed by the blank filter, 0 mixed-model-only). None re-added beyond the 121. |
| report | v3 | `MSV000082221_part1_report_v3.pdf` |
