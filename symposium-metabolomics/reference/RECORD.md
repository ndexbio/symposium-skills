# What each mode publishes

Every run of a mode publishes the same artifacts, under the same names, with the same tables
inside them. A reader of the record, a later interpretation, the reuse table and a lab library
holding many runs then find each thing by its name rather than by reading descriptions.

This document fixes what must be there and what it is called. It does not limit what more a run
says: extra properties, extra columns and the wording of every description and procedure are the
run's own. Where it and another document of this skill disagree on a name, this one is right.
What each artifact type is, and how it is built, is Symposium's to say.

## Names

```
<account>_<role>_<short name>_<topic>_v<N>
```

- `<account>` and `<role>`: the publishing member and the publishing role, as Symposium sets out.
- `<short name>`: the run's. Where an artifact name the run would publish is already in the
  community, the short name takes the lowest numeric suffix that frees every name of the run:
  `ibd_surgery_metabolome_2`. Decide it before publishing anything, and record it.
- `<topic>`: fixed below for every artifact. Where a topic carries a `<key>`, the key is lowercase
  words joined by underscores.
- `_v<N>`: `_v1`, then a correction as `_v2` that supersedes it.

Within an artifact, a table held in a property is reached through a Content named
`<property>_csv`; a file through a Content named `<name>_download`; a figure through
`<name>_figure_download`; the code an Analysis ran through `code_download`.

## The goal identifies the run

Each mode opens with one ResearchGoal, role `principal`, topic `goal`. Beside its text, the
question word for word, it carries these properties:

| Property | Analyze | Interpret |
|---|---|---|
| `skill` | `symposium-metabolomics` | `symposium-metabolomics` |
| `mode` | `analyze` | `interpret` |
| `short_name` | the run's short name | the run's short name |
| `task` | the GNPS2 task ID and host | the task of the analysis it interprets |
| `library` | — | the library community and its data server |
| `analysis` | — | the data-server location of the library's `technical_report` it starts from |

Every other artifact of the run names the goal in `serves_goals`.

A run's artifacts are then found two ways:

- **What the run published**: every artifact whose `serves_goals` names its goal.
- **What the run rests on**: those, and everything they cite, followed through `inputs`,
  `produced_by`, Grounds and links in prose, and for interpret through each pointer's `download`
  location into the library and on from there. It includes what another run published and this
  run reused.

## Analyze

Role `importer` for the imports, `analyst` for every Analysis and its outputs, `scout` for the
hand-off note and the report.

### Imports

One Data artifact per input the analysis used, topic `input_<key>`:

| Key | Input |
|---|---|
| `feature_table` | the task's quantification table, all features |
| `msms_spectra` | the consensus MS/MS spectra |
| `network_pairs` | the network's filtered pairs list |
| `library_hits` | the task's library annotations, where used |
| `gap_fill` | the gap-fill report, where used |
| `rt_bounds` | the per-sample retention-time bounds, where used |
| `task_parameters` | the task's status page: workflow, version, parameters |
| `<user file key>` | each file the user supplied, keyed by what it holds: `sample_metadata`, `curated_annotations`, `run_order`, `clinical_metadata` |

### Stages

One Analysis per stage, topic `analysis_<stage>`, its `procedure` stating the stage's block of
[ANALYZE.md](ANALYZE.md), Section 14. Its outputs follow, each `produced_by` it. A stage the
reuse table reuses is not published again; the run's later Analyses cite its outputs.

| Stage | Output topic | Tables (properties; files) |
|---|---|---|
| `qc_standards` | `data_qc_standards` | `internal_standards`, `qc_summary`; file `sample_table` |
| `merges` | `data_merges` | `counts`, `candidates`, `merge_map` (published empty when none was applied); file `review_sheets` |
| `batch` | `data_batch` | `check_summary`; files for the corrected tables, where corrected |
| `processing` | `data_processing` | `normalization_comparison`; files `filter_table`, `processed_filtered`, `processed_unfiltered` |
| `statistics` | `data_statistics` | `counts`; files `results`, `results_unfiltered` |
| `sensitivity` | `data_sensitivity` | `summary` |
| `multivariate` | `data_multivariate` | `summary` |
| `detection_rate` | `data_detection_rate` | `bins`, `cumulative`; file `per_feature` |
| `network_classes` | `data_network_classes` | `summary`, `family_sizes`, `families`, `delta_masses`, `composition`, `color_key`, `unclassified`; files `nodes`, `edges`, `class_assignments` |
| `removed_review` | `data_removed_review` | `flagged`, `added_back` |
| `followup_<key>` | `data_followup_<key>` | one per follow-up the user approved: `summary`; files as it needs |

Then the hand-off note, topic `handoff`, and the report, topic `technical_report`.

### The columns that are always there

| Table | Columns, by these names |
|---|---|
| `results` and `results_unfiltered` | `row_id`, `mz`, `rt_min`, `retained`, `added_back`, `removed_by`, `primary_log2fc`, `primary_p`, `primary_q`; and, where an over-time model ran, `group_beta`, `group_p`, `group_q`, `time_beta`, `time_p`, `time_q`, `interaction_beta`, `interaction_p`, `interaction_q`. `primary_*` is the primary comparison; `q` is within the primary family, empty for a feature outside it |
| `filter_table` | `row_id`, `retained`, `added_back`, `removed_by` |
| `bins`, `cumulative` | `bin`, `features`, `features_with_msms`, `features_with_library_match` |
| `summary` of `network_classes` | `item`, `value`, with the items `nodes`, `edges`, `families`, `singletons`, `msms_features`, `largest_family`, `delta_same_mass`, `delta_assigned`, `delta_unassigned` |
| `family_sizes` | `bin`, `families` |
| `delta_masses` | `label`, `mass`, `edges` (one row per label; the totals are items of `summary`) |
| `composition` | `class_group`, `fine_class`, `annotated`, `networked`, `tested`, `significant` |
| `candidates` | `row_id_a`, `row_id_b`, `class`, `decision` |
| `check_summary` | `item`, `value`, with the item `status`: `not possible`, `not needed`, `corrected` or `input already corrected` |

## Interpret

Role `importer` for pointers, `researcher` for additional analyses and findings, `hypothesize`
for conjectures, `scout` for the report.

| Artifact | Topic | Holds |
|---|---|---|
| ResearchGoal | `goal` | as above |
| Pointer to a library table | `pointer_<library topic>` | the rows a finding or analysis turns on, reproduced exactly, as a property with a groundable `rows_csv` |
| Pointer to a literature source | `source_<key>` | the passages a finding grounds on, reproduced exactly, with a groundable `passages_text_span`; its authors and identifier |
| Additional analysis | `analysis_<key>`, output `data_<key>` | as for analyze |
| Finding | `finding_<key>` | an Argument; its schematic as `schematic_figure_download` |
| Conjecture | `conjecture_<key>` | a NonGroundable, with what would confirm it and what would refute it |
| Report | `report` | the full report; the overview schematic as `overview_figure_download` |

Every pointer carries a `download` Content, not groundable, whose `location` is the library
artifact on its data server, `<server>/v1/communities/<library>/artifacts/<artifact name>`, with
an `access_method` saying a reader with read access to the library fetches it there; and an
`import_method` naming that artifact and which rows or passages were taken. A Ground cites the
pointer's reproduced content. The run compares the copy with the library's before submitting.

`<key>` for a finding, conjecture or pointer is a few words of what it is about: `finding_bile_acid_split`,
`pointer_data_statistics`, `source_hall_2024_bilirubin_reductase`.
