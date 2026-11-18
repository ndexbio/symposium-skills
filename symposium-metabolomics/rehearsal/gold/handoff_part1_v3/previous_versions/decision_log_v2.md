# Decision log v2 (Part 1): MSV000082221. Changes from v1; v1 files are unchanged.

| Block | Status / decision | Detail |
|---|---|---|
| flagged_features_add_back | user decision, applied | Of 411 flagged in v1: 344 were removed by the prevalence filter only; 67 involved the blank filter (kept out, as instructed). Contaminants and additives class: 0 of the 344. 223 of the 344 have zero CD detections (not testable) and were held out; 121 added back. |
| rescued_family | analyst default (user can change) | Rescued features analyzed as a separate family (selected on signal, optimistic p). Primary q (11,242) unchanged. Per-feature table has q_rescued_family and q_combined_family. Normalization factors, PCA, PLS-DA not recomputed. |
| correction_of_v1 | error found | 1,481 features with fewer than 3 CD detections have constant imputed CD values; v1 reported spurious mixed-model p-values and unfiltered-family q for them (flag list: 224 of 411 affected; unfiltered-family baseline q<0.05: 2,222 in v1, 1,270 corrected). v2 sets their CD tests to missing (`testable_CD` = false). Primary results unaffected. |
| unclassified_annotations | user: acceptable | 193 of 1,246 left unclassified. |
| time_since_surgery | user: skipped | Not run. |
| presence_absence | next step 1, done | 6,907 retained features with at least 50% imputed CD values and at least 3 detections. Fisher exact (baseline), detected-only Welch, GEE logistic over time. |
| surgery_type_stratified | next step 2, done | Baseline CD: none 39, ileocolonic 19, colectomy 11; 2 samples excluded (partial colectomy; surgery_type none). Welch on 11,242 primary features. |
| report | v2 | `MSV000082221_part1_report_v2.pdf` |
