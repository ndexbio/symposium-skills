# GNPS2 task files

Where each output of a GNPS2 Everything Bagel (EB) task lives, the cheapest reliable way to get it, and how each file the analysis uses enters the library. Scope: finding, fetching and importing files. Nothing here merges, filters, screens or analyzes them.

You arrive here with the task ID, the question and the library community. You leave with every file the analysis needs fetched into the run's folder, each with its location and digest recorded, and a list of what the library already holds. Verified on a real EB task (workflow `everything_bagel_workflow`, mode fbmn, host gnps2.org, server 2026.10.08 / workflow 2026.10.26).

## Start
1. Get the EB task ID (one per job if the user gives several).
2. Check that the GNPS2 connector is available. The GNPS2 tools are deferred, so run ToolSearch with `select:mcp__gnps2__prewarm_eb_task,mcp__gnps2__list_eb_features,mcp__gnps2__get_eb_features_msms,mcp__gnps2__get_eb_xic,mcp__gnps2__get_eb_xics,mcp__gnps2__prewarm_network_task,mcp__gnps2__list_network_components,mcp__gnps2__show_network_component,mcp__gnps2__list_spectral_libraries,mcp__gnps2__search_libraries,mcp__gnps2__get_library_spectrum` (one call). Load the browser tools the session prefers in one call too.
   - If the GNPS2 tools load: continue.
   - If they do not exist: the person has not connected the GNPS2 connector. Run SearchMcpRegistry with keywords `["gnps2"]`. If a `gnps2` connector is returned and not connected, call SuggestConnectors with its directoryUuid so the person sees the one-click connect card, and say in one sentence that connecting it enables the tool routes (it is a hosted connector, nothing to install locally, and it asks the person to sign in). If it is connected in the registry but its tools are not enabled in this chat, say so and point to their connector settings. If the registry returns nothing for gnps2, the connector is not in the directory. Tell the person it can be added as a custom connector with the address `https://remote-mcp.gnps2.org/` (claude.ai: Settings, Connectors, Add custom connector; on Team or Enterprise plans an admin may need to allow custom connectors first; it asks the person to sign in, and the tools load only in a new chat). This address comes from the GNPS2 team; do not guess any other address.
   - Do not wait on the connection. Continue with the next route below, and use the tool routes once the connector is available.
   - **Say the connector status in the first message** in one line (for example "GNPS2 connector: not connected; registry search returned nothing; custom connector address given"), so it is visible that this step ran.
3. If the tools are available, call `prewarm_eb_task` (host, feature count, sample labels) and `prewarm_network_task` (nodes, edges, annotated count, top components). Tell the user what came back.
4. Shell downloads (curl, wget, Python requests) from gnps2.org work only if `gnps2.org` is on the sandbox network allowlist. Test once with a small request (`Range: bytes=0-400` on a `/resultfile` URL). If the allowlist refuses it, do not retry or look for workarounds; move to the next route, and tell the person they can allow the domain (claude.ai: Settings, Capabilities, code execution network access; an admin controls this on Team and Enterprise plans). WebFetch cannot read task results.
5. **Check whether a molecular network exists** (nodes and edges from `prewarm_network_task`, or the `pairslist` and `graphml` views below). If it does, the molecular-network analysis runs by default and needs the files listed in "Files the analysis needs for Sections 13B and 13C". Tell the user in one line whether a network is available. If it is not (for example the networking step was not run), say so; The analysis then reports the detection-rate section only and states that no network was available ([ANALYZE.md](ANALYZE.md), Section 13C.1).
6. **Check whether the quantification table is raw.** The normalization comparison needs a raw feature table ([ANALYZE.md](ANALYZE.md), Sections 2.2 and 7.4.2). From the task parameters and the table itself, say in one line whether the quantification table looks raw or already normalized, or that this cannot be told. If the user's data are already normalized, tell them upfront that the comparison is not applicable and ask for a raw table.

## Routes, in order
1. A GNPS2 MCP tool covers it: use it.
2. Direct download in the shell, when `gnps2.org` is allowed (Start step 4). Use the `/resultfile` and `/result?...&json` URL patterns below and save each file straight into the run's folder. Large files never pass through the conversation.
3. Browser on a gnps2.org tab (the task status page is public, no login). Inside the page, `fetch` relative URLs. Keep big payloads in `window` variables or stream and count; never page large tables through the conversation. Request only a header with `Range: bytes=0-400` to inspect a file. If the browser pane has closed, reopen it on any gnps2.org task URL first.
4. Ask the user to attach the file.

## Read the library first

Sync the library and list what it holds of this task before fetching anything: every import
whose `import_method` names this task ID, with the file it rendered and the digest it recorded.
A file the library already holds, with the same digest as the bytes you fetch, is cited by its
address and not imported again. Where the bytes at the same location now differ, say so: it is a
new import, and its `import_method` names the earlier one.

## Every file the analysis uses is an input

Fetch each file into the run's folder unchanged, and compute its digest on arrival. Do not edit,
filter, re-sort or rename-and-modify a fetched file; what the analysis makes of it is the
analysis's output. For a connector tool that returns parsed rows, keep the rows as returned and
say so.

Record for each file, in the working file: its name; where it came from (a GNPS2 connector tool
and its call, a gnps2.org location, a browser fetch, a file the user supplied and the name they
gave it); the task ID, for a GNPS2 file; the date retrieved; its size; its digest; and a note
where one is needed, for example "header only: no metadata was supplied to the task". A file
that could not be retrieved is recorded with the reason.

When the mode publishes, each file **the analysis used** becomes one import, and what was
recorded for it is what its `import_method` states:

- **A file held at gnps2.org is cited where it is held**: its location is the `/resultfile` or
  `/result` address it was fetched from. The community keeps no copy.
- **A file the user supplied has no location of its own**, so it is stored with the community
  and cited there. Confirm with the user before storing it.
- **A file fetched and not used is not imported.** Say in the report that it was fetched and
  why it was set aside.
- **The task itself is described once**: the status page's workflow, version and parameters,
  as the import of the task's parameters.

What an import of a file held elsewhere must declare, and what an inventory of a task's files
is and is not, are in the community's documents.

## URL patterns that work without login
- View: `/result?task=<ID>&viewname=<view>&resultdisplay_type=task` (download views return the file; table views return an HTML shell).
- Table as JSON: `/result?task=<ID>&viewname=<view>&json` (an array of row objects) for the table views below.
- Any published file: `/resultfile?task=<ID>&file=<URL-encoded nf_output path>` (supports Range).
- Not usable: `/filebrowser/files/nf_tasks/<ID>/...` redirects to a login page. Do not enter credentials; the other routes cover everything below.

## Where things live (verified on an EB task)
| Need | View name | File under `nf_output/` | Notes |
|---|---|---|---|
| Quant table, ALL features | `quantificationdownload` | `feature_finding/feature_finding_results/aligned_features.csv` | 140 columns in the test task: row ID, row m/z, row retention time, Gaussian_similarity, noise_score, FWHM, total_scans, has_ms2, isotope, charge, adduct_source_id, parent_mass, adduct, is_default_adduct, adduct_rep_file, is_isf, then one `<file>.mzML Peak area` column per sample. Includes features without MS/MS (17,730 rows vs 11,951 with MS/MS in the test task), so use `has_ms2` to tell them apart. |
| Quant table, MS/MS features only | `featurefindingresultsms2` (`&json`) | `feature_finding/feature_finding_results/aligned_features_ms2.csv` | same columns |
| Consensus MS/MS (MGF) | `specms` | `feature_finding/aligned_features_filled.mgf` | blocks carry `FEATURE_ID=<row ID>`, `SOURCE_FEATURE_ID`, `SOURCE_FILE`, `PEPMASS`, `RTINSECONDS`, `COLLISION_ENERGY`. `FEATURE_ID` equals the quant `row ID`. |
| All MS/MS scans per feature | `featurems2scans` (`&json`) | `feature_finding/feature_finding_results/aligned_feature_ms2_scans.tsv` | aligned_feature_ID, source_file, scan_id, precursor_mz, rt_seconds, n_peaks, origin (204,492 rows in the test task) |
| Per-sample m/z | `featuremz` (`&json`) | `feature_finding/feature_finding_results/aligned_mz.csv` | large |
| Per-sample RT bounds | `featurertbounds` (`&json`) | `feature_finding/feature_finding_results/aligned_rt_bounds.csv` | very large (hundreds of MB as JSON); read the CSV via /resultfile and parse in the page |
| Gap-fill report | `featuregapfillreport` (`&json`) | `feature_finding/feature_finding_results/gap_fill_report.tsv` | per feature x sample: filled, was_detected, filled_area |
| Library annotations (exact match) | `featurelibrarysearchresults` (`&json`) | `feature_library_search/merged_feature_library_search_results.tsv` | 34 columns (a reduced header): query_idx, `query_scan` (= quant `row ID`), query_file, query_precursor_mz, library_idx, library_scan, `library_filename` (the source library, not the compound), library_precursor_mz, cosine, matched_peaks, delta_mz, CHARGE, then library metadata including `NAME` (the annotation), SMILES, INCHI, INCHIAUX, ORGANISM, IONMODE, LIBRARYQUALITY, SPECTRUMID, USI. One row per hit; the task param `topk` sets hits per feature (1 in the test task, so one row per feature). Split TSVs on tabs only. |
| Library annotations (analog / delta-mass) | `featureanalogsearchresults` (`&json`) | `feature_analog_library_search/merged_feature_analog_library_search_results.tsv` | same columns |
| Network (nodes + edges) | `graphml` | `networking/network.graphml` | GraphML, tens of MB; the `prewarm_network_task` / `list_network_components` tools read and cache it |
| Network incl. singletons | `graphmlsingletons` | `networking/network_singletons.graphml` | |
| Compound network | `compoundnetworkgraphml` | `networking/compound_network.graphml` | |
| Pairs, filtered (the edges) | `pairslist` (`&json`) | `networking/filtered_pairs.tsv` | CLUSTERID1, CLUSTERID2, DeltaMZ, Cosine, ComponentIndex |
| Pairs, unfiltered | `unfilteredpairslist` (`&json`) | `networking/merged_pairs.tsv` | adds MinRatio, AlignScore2, AlignScore3; large |
| Compound pairs | `compoundpairs` (`&json`) | `networking/compound_pairs.tsv` | compound_id_a, compound_id_b, n_supporting_pairs |
| Sample metadata | `metadatadownload` | `metadata/merged_metadata.tsv` | If the task param `metadata_file` was empty, the file holds only a `filename` header. That is not a fetch failure: no metadata was supplied. |
| Input file list | n/a | `file_list/input_spectra_list.tsv` | listed on the File Exports page |
| Run summary text | n/a | `workflow_summary.txt` | listed on the File Exports page |
| Formula prediction | n/a | `formula_prediction/formula_consensus.tsv`, `formula_candidates.tsv` | listed on the File Exports page; probably empty when `formula_prediction_method` is `none` (not tested) |
| Index of all published outputs | `fileexports` | `visualizations/file_exports.html` | fetch `/resultfile?...&file=nf_output/visualizations/file_exports.html` and read the `nf_output/...` paths in it. This is the substitute for the login-gated file browser. |

Tools (no URL needed): `list_eb_features` (filters mz, rt, ms2_only, min_area, adduct, annotation_network), `get_eb_features_msms` (max 200 row IDs per call), `get_eb_xic` / `get_eb_xics`, `list_network_components`, `show_network_component`, `get_library_spectrum`, `search_libraries`, `list_spectral_libraries`. Counts differ by source: `prewarm_eb_task` counts MS/MS features only (11,951 in the test task), the quant download has every feature (17,730), and the network has fewer nodes still (8,003).

## Files the analysis needs for Sections 13B and 13C
The analysis uses the files below for the detection-rate table ([ANALYZE.md](ANALYZE.md), Section 13B) and the molecular-network analysis (Section 13C). Fetch them from the **same task**, because row IDs only line up within one task.

| the analysis needs | Source (table above) | Check before use |
| :---- | :---- | :---- |
| Peak areas per sample and the `has_ms2` flag for **all** features | `quantificationdownload` (`aligned_features.csv`) | Use this table, not the MS/MS-only table, so that the denominator is every feature. Sample columns end in `.mzML Peak area`. Zero means not detected in that sample (gap-fill caveat: see Section 13B.1). |
| Library match per feature | `featurelibrarysearchresults` | `query_scan` = quant `row ID`. One row per feature when `topk` is 1 (read `topk` on the status page); if `topk` is larger, keep the best-cosine hit and say so. Split on tabs only. |
| Edges and family membership | `pairslist` (`filtered_pairs.tsv`) | Columns CLUSTERID1, CLUSTERID2, DeltaMZ, Cosine, ComponentIndex. The number of distinct `ComponentIndex` values is the number of molecular families. |
| Nodes, singletons | `graphml` and `graphmlsingletons`, or `prewarm_network_task` | Networked nodes should all have MS/MS. Singletons = features with MS/MS that are not in any edge. Nodes + singletons must equal the number of MS/MS features ([ANALYZE.md](ANALYZE.md), Section 13C.10); if not, report the difference and do not adjust it. |
| Sample metadata (group labels) | `metadatadownload` | An empty file (header only) means no metadata was supplied; ask the user for the group assignment. |
| Task parameters (libraries, `library_min_similarity`, `topk`) | status page | Report the libraries and thresholds in the technical report; the library match rate depends on them. |

If a file cannot be fetched, say which one, name the table or figure that cannot be made, and continue with the rest. Do not estimate values.

## Files the analysis needs for Sections 3.8 and 3.9
The analysis uses these for the internal-standard check ([ANALYZE.md](ANALYZE.md), Section 3.8) and the feature-merge recommendation (Section 3.9). Fetch them from the **same task**.

| the analysis needs | Source (table above) | Check before use |
| :---- | :---- | :---- |
| m/z, RT, `FWHM`, `isotope` (keep `M+0`), `has_ms2`, sample areas | `quantificationdownload` (`aligned_features.csv`) | Use all features. Sample columns end in `.mzML Peak area`. |
| Consensus MS/MS spectra for the mirror plots | `specms` (`aligned_features_filled.mgf`), or `get_eb_features_msms` (max 200 row IDs per call) | Match on `FEATURE_ID` = quant `row ID`. Use only features with `has_ms2` true. |
| Chromatograms for the overlays | `get_eb_xics` (one m/z, several samples, or several row IDs on one sample) | The trace follows the m/z window, not one feature: two features with the same m/z give the same trace. Mark each feature's RT on it. |
| Library annotation names for both rows | `featurelibrarysearchresults` | `NAME` is the annotation; `query_scan` = quant `row ID`; report the library (`library_filename`) and cosine. Features with no row are unannotated. |
| Which cells were gap-filled | `featuregapfillreport` (`gap_fill_report.tsv`) | The report lists **only filled cells** (`was_detected` is false for all of them in the test task); a detected value is a nonzero area that is not in this list. Optional: use it to choose an XIC sample where a feature was truly detected. |
| Injection order and batch | metadata (`metadatadownload`) or the user | Needed for RT-versus-injection-order plots of the standards (Section 3.8.3). If missing, ask the user; do not infer it from file names. |

## What the run used
The task status page (`/status?task=<ID>`) shows the workflow version, description, status, and a Workflow Task Parameters table (input spectra, `input_spectral_library` list, `library_min_similarity`, `library_min_matched_peaks`, `topk`, `pm_tolerance`, `fragment_tolerance`, `gap_fill`, `feature_finder_engine`, `metadata_file`, `formula_prediction_method`, `mode`). Read it to report which libraries and thresholds the run used. The status page also lists every view; get the exact link targets with:
`[...document.querySelectorAll('a[href]')].map(a=>[a.textContent.trim(),a.getAttribute('href')])`

## Not found or not available
- `nf_output/filesummary/summaryresult.tsv` returns HTTP 500 on EB tasks. Do not use it for directory listings.
- The file browser (`/filebrowser/...`) needs a login.
- `insilicosearchresults`, `insilicosearchresultsallhits`, `librarysearchresults` returned an HTML shell for `&json` in the test task, probably because those searches were not run. Check the task parameters before assuming a failure.
- The 'no-gap-fill' quant table mentioned on the File Exports page: its path was not identified.
- Host: a task may be staged on gnps2.org or beta.gnps2.org; `prewarm_eb_task` reports which.

## Reporting
Say which route returned each file and which failed and why, and record the same in the working file. If a route fails, move to the next; do not estimate or recall values instead. Row IDs only line up between files from the SAME task, so name the task each file came from.
