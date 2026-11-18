#!/usr/bin/env python3
"""Print the rehearsal's assertion table for one run, against the gold facts.

    compare.py <run facts.json> [--per-feature <run per-feature.csv>] [--mode analyze|interpret|both]
               [--science-only]
               [--gold gold-facts.json] [--gold-per-feature gold-per-feature.csv]
               [--variation variation.json]

`<run facts.json>` is what `extract_record.py` writes for a run of this skill (or what
`extract_local.py` writes for a run of the skill this one was built from). Each row is one of:

    exact      a departure is a regression
    tolerance  passes within the band `variation.json` records
    judged     printed with what both sides hold, for a person to read against the rubric

Exit code 0 when every exact and tolerance row passes. Judged rows never fail the run.
Needs only the standard library.
"""

import argparse
import csv
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent


def load(path):
    return json.loads(pathlib.Path(path).read_text(encoding="utf-8"))


def numbers(d):
    """The numeric values of a flat or one-level-nested mapping, in a stable order, with row and
    column labels dropped: two runs name their rows differently and count the same things."""
    out = []
    if d is None:
        return out
    for v in d.values():
        if isinstance(v, dict):
            out.extend(x for x in v.values() if isinstance(x, (int, float)) and not isinstance(x, bool))
        elif isinstance(v, (int, float)) and not isinstance(v, bool):
            out.append(v)
    return out


def first_numbers(d, n):
    return numbers(d)[:n]


def within(a, b, frac):
    if a is None or b is None:
        return False
    return abs(a - b) <= frac * max(abs(a), abs(b), 1)


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2.0
        i = j + 1
    return r


def spearman(xs, ys):
    if len(xs) < 3:
        return None
    rx, ry = ranks(xs), ranks(ys)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else None


def read_pf(path):
    out = {}
    if not path or not pathlib.Path(path).is_file():
        return out
    with open(path, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            try:
                out[str(r["row_id"]).split(".")[0]] = (float(r["baseline_log2FC"]), float(r["baseline_q"]))
            except (KeyError, ValueError):
                continue
    return out


class Table:
    def __init__(self):
        self.rows = []

    def add(self, mode, group, kind, ok, gold, run, note=""):
        self.rows.append((mode, group, kind, ok, gold, run, note))

    def exact(self, mode, group, gold, run, note=""):
        self.add(mode, group, "exact", gold == run and gold is not None, gold, run, note)

    def tol(self, mode, group, ok, gold, run, note=""):
        self.add(mode, group, "tolerance", bool(ok), gold, run, note)

    def judged(self, mode, group, gold, run, note=""):
        self.add(mode, group, "judged", None, gold, run, note)

    def show(self, modes):
        failed = 0
        print(f"{'':4} {'mode':9} {'kind':9} group")
        for mode, group, kind, ok, gold, run, note in self.rows:
            if mode not in modes and mode != "both":
                continue
            mark = "  ? " if ok is None else ("PASS" if ok else "FAIL")
            if ok is False:
                failed += 1
            print(f"{mark} {mode:9} {kind:9} {group}")
            if ok is not True:
                print(f"       gold: {str(gold)[:300]}")
                print(f"       run : {str(run)[:300]}")
            if note:
                print(f"       {note}")
        print()
        print(f"{failed} failing; judged rows (?) are read by a person against REHEARSAL.md")
        return failed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--per-feature")
    ap.add_argument("--mode", default="both", choices=["analyze", "interpret", "both"])
    ap.add_argument("--gold", default=str(HERE / "gold-facts.json"))
    ap.add_argument("--gold-per-feature", default=str(HERE / "gold-per-feature.csv"))
    ap.add_argument("--variation", default=str(HERE / "variation.json"))
    ap.add_argument("--science-only", action="store_true",
                    help="leave out the rows only a Symposium record can answer (for a run of the original skill)")
    a = ap.parse_args()

    G, R = load(a.gold), load(a.run)
    g, r = G["analyze"], R.get("analyze", {})
    t = Table()

    # ------------------------------------------------------------------ analyze: inputs
    gi = {i["file_name"]: i for i in (g["inputs"] or []) if i.get("sha256") and i.get("used")
          and not i["file_name"].startswith("input_prompt") and not i["file_name"].endswith(".html")
          # the network can be built from the pairs list and the feature table, so the GraphML
          # files are not required; an input that holds no data is not required either
          and not i["file_name"].endswith(".graphml") and (i.get("size_bytes") or 0) >= 100}
    ri = {i.get("sha256"): i for i in (r.get("inputs") or [])}
    missing = [n for n, i in gi.items() if i["sha256"] not in ri]
    # a task's status page is rendered afresh on each request, so its digest is not asserted
    t.add("analyze", "Inputs: every input the gold run used is imported with the same digest", "exact",
          not missing, sorted(gi), f"missing: {missing}" if missing else "all present")
    unused = {i["sha256"] for i in (g["inputs"] or []) if i.get("sha256") and not i.get("used")}
    extra = [i.get("file_name") for i in (r.get("inputs") or []) if i.get("sha256") in unused and i.get("used", True)]
    t.judged("analyze", "Inputs: nothing fetched and unused is imported", "gap-fill report and task library hits unused",
             f"imported from that set: {extra or 'none'}",
             "the gold re-run used the gap-fill report, so its use is not by itself a regression")

    # ------------------------------------------------------------------ analyze: counts
    gf, rf = g["filter_counts"] or {}, r.get("filter_counts") or {}
    t.exact("analyze", "Counts: features in", gf.get("features_in"), rf.get("features_in"))
    gfinal = (g.get("per_feature") or {}).get("features")
    rfinal = (r.get("per_feature") or {}).get("features")
    t.tol("analyze", "Counts: features retained, within 1%", within(gfinal, rfinal, 0.01), gfinal, rfinal)
    t.judged("analyze", "Add-back: the user's rule applied to the flagged features (the count is not compared)",
             f"{gf.get('added_back')} added back from the gold review's flagged list", f"{rf.get('added_back')} added back")
    t.exact("analyze", "Counts: merge candidates", g.get("feature_merge_candidates"), r.get("feature_merge_candidates"))
    t.exact("analyze", "Counts: merges applied", g.get("feature_merge_map_rows"), r.get("feature_merge_map_rows"))

    # ------------------------------------------------------------------ analyze: batch, normalization
    gb = (g.get("batch_correction_check") or {}).get("status")
    rb = (r.get("batch_correction_check") or {}).get("status")
    if rb is None:
        t.judged("analyze", "Batch correction: the check reports correction not possible", gb, "no check summary found in the run's facts")
    else:
        t.add("analyze", "Batch correction: the check reports correction not possible", "exact",
              "not possible" in str(rb).lower(), gb, rb)
    t.judged("analyze", "Normalization applied is sum (TIC)", "sum (TIC), scaled to the median; rCLR as sensitivity",
             r.get("normalization") or "read it from the normalization Analysis's procedure")

    # ------------------------------------------------------------------ analyze: statistics
    gp, rp = g.get("per_feature") or {}, r.get("per_feature") or {}
    t.tol("analyze", "Statistics: baseline hits at q < 0.05, within 5%", within(gp.get("q_lt_0.05"), rp.get("q_lt_0.05"), 0.05),
          gp.get("q_lt_0.05"), rp.get("q_lt_0.05"))
    for k, label in (("lower_in_surgery_at_q05", "lower with surgery"), ("higher_in_surgery_at_q05", "higher with surgery")):
        t.tol("analyze", f"Statistics: hits {label}, within 5%", within(gp.get(k), rp.get(k), 0.05), gp.get(k), rp.get(k))
    A, B = read_pf(a.gold_per_feature), read_pf(a.per_feature)
    common = sorted(set(A) & set(B))
    if common:
        rho_fc = spearman([A[k][0] for k in common], [B[k][0] for k in common])
        rho_q = spearman([A[k][1] for k in common], [B[k][1] for k in common])
        sa, sb = {k for k in A if A[k][1] < 0.05}, {k for k in B if B[k][1] < 0.05}
        jac = len(sa & sb) / len(sa | sb) if sa | sb else None
        both = sa & sb
        sign = sum((A[k][0] > 0) == (B[k][0] > 0) for k in both) / len(both) if both else None
        t.tol("analyze", "Statistics: per-feature effect size rank-correlates at 0.99 or more", rho_fc is not None and rho_fc >= 0.99,
              ">= 0.99", None if rho_fc is None else round(rho_fc, 4), f"{len(common)} features in common")
        t.tol("analyze", "Statistics: per-feature q rank-correlates at 0.99 or more", rho_q is not None and rho_q >= 0.99,
              ">= 0.99", None if rho_q is None else round(rho_q, 4))
        t.tol("analyze", "Statistics: baseline hits overlap gold at Jaccard 0.90 or more", jac is not None and jac >= 0.90,
              ">= 0.90", None if jac is None else round(jac, 3))
        t.tol("analyze", "Statistics: direction agrees for 99% or more of shared hits", sign is not None and sign >= 0.99,
              ">= 0.99", None if sign is None else round(sign, 4))
    else:
        t.tol("analyze", "Statistics: per-feature table compared with gold", False, f"{len(A)} features", "no per-feature table given or no feature in common")
    t.judged("analyze", "Statistics: 16 features with a surgery x time interaction at q < 0.05", 16,
             r.get("interaction_q05") or "read it from the report")

    # ------------------------------------------------------------------ analyze: detection, network
    gd = sorted(v["features"] for v in (g["detection_rate_bins"] or {}).values())
    rd = sorted(first_numbers({k: v}, 1)[0] if isinstance(v, dict) and first_numbers({k: v}, 1) else v
                for k, v in (r.get("detection_rate_bins") or {}).items()
                if isinstance(v, (int, float)) or (isinstance(v, dict) and "features" in v))
    rd = sorted(v["features"] if isinstance(v, dict) else v for v in (r.get("detection_rate_bins") or {}).values()
                if isinstance(v, (int, float)) or (isinstance(v, dict) and "features" in v))
    t.exact("analyze", "Detection rate: feature count in every bin", gd, rd)
    gn = g["network_summary"] or {}
    want = sorted(gn[k] for k in ("nodes", "edges", "families", "singletons", "ms2_features", "largest_family"))
    have = numbers(r.get("network_summary"))
    t.add("analyze", "Network: nodes, edges, families, singletons, MS/MS features, largest family", "exact",
          all(w in have for w in want), want, sorted(set(have) & set(want)))
    t.exact("analyze", "Network: family-size bins", sorted(numbers(g["network_family_sizes"])), sorted(numbers(r.get("network_family_sizes"))))
    gdm = sorted(v["edges"] for v in (g["network_delta_masses"] or {}).values() if isinstance(v, dict) and isinstance(v.get("edges"), (int, float)))
    rdm = sorted(v["edges"] if isinstance(v, dict) else v for v in (r.get("network_delta_masses") or {}).values()
                 if isinstance(v, (int, float)) or (isinstance(v, dict) and isinstance(v.get("edges"), (int, float))))
    shared = len(set(gdm) & set(rdm))
    t.add("analyze", "Network: delta-mass edge counts (at least 20 of gold's shared)", "exact", shared >= min(20, len(set(gdm))),
          f"{len(gdm)} labels", f"{len(rdm)} labels, {shared} edge counts shared")
    gc, rc = set(g["compound_class_composition"] or {}), set(r.get("compound_class_composition") or {})
    t.add("analyze", "Compound classes: the same class scheme (counts are not asserted)", "exact",
          bool(rc) and len(gc & rc) >= 0.9 * len(gc), f"{len(gc)} classes", f"{len(rc)} classes, {len(gc & rc)} shared names")

    # ------------------------------------------------------------------ analyze: judged
    t.judged("analyze", "Decisions: every decision in answers.md is stated in an Analysis procedure, with its parameters",
             f"{len(g['decisions'] or [])} decision rows in the gold logs", f"{len(r.get('procedures') or [])} Analysis procedures in the run")
    t.judged("analyze", "Activation: the first prompt starts analyze only, says so, and closes offering interpretation",
             "see REHEARSAL.md", "read the session's first and last messages")

    # ------------------------------------------------------------------ interpret
    gi_, ri_ = G["interpret"], R.get("interpret", {})
    themes = ["bile acids split by microbial processing (primary/conjugated higher, secondary lower)", "urobilinoids lower",
              "acylcarnitines higher", "N-acyl lipids differ", "fewer features detected per sample",
              "over time inconclusive: time and plate confounded"]
    t.judged("interpret", "Themes: each of the six gold themes is a finding with the same direction", themes,
             [f.get("claim") or f.get("title") for f in (ri_.get("findings") or [])])
    t.judged("interpret", "Findings: each gold hypothesis has a finding making the same claim at the same confidence",
             [h.get("title") for h in (gi_.get("hypotheses") or [])], [f.get("title") for f in (ri_.get("findings") or [])])
    gref = {x["url"].rstrip("/") for x in (gi_.get("key_references") or [])}
    core = {u for u in gref if "38172624" in u or "03r944h7" in u}
    rref = {str(u).rstrip("/") for u in (ri_.get("library_sources") or [])}
    cited = {str(u).rstrip("/") for u in (ri_.get("cited_sources") or [])}
    t.add("interpret", "Literature: every source a finding cites is in the library", "exact",
          bool(cited) and cited <= rref, "cited is a subset of the library's sources", f"{len(cited - rref)} cited and not in the library" if cited else "no cited sources found")
    t.add("interpret", "Literature: the two sources both gold runs cited are in the library", "exact",
          all(any(c.split("/")[-1] in u for u in rref) for c in core), sorted(core), sorted(rref)[:12])
    t.add("interpret", "Placement: no Argument is in the library", "exact", ri_.get("arguments_in_library") == 0, 0, ri_.get("arguments_in_library"))
    t.add("interpret", "Placement: every Ground cites a pointer equal to its library source", "exact",
          ri_.get("pointer_mismatches") == 0, 0, ri_.get("pointer_mismatches"))
    t.judged("interpret", "Activation: against a library with no accepted analysis, interpret says so and offers analyze; against the frozen library it names the analysis and confirms the question",
             "see REHEARSAL.md", "read the session's first messages")
    t.judged("interpret", "Overlap: a second interpretation shows an overlap table and publishes no finding restating one",
             "see REHEARSAL.md", "run only when checking this row")

    # ------------------------------------------------------------------ both
    for mode in (() if a.science_only else ("analyze", "interpret")):
        c = R.get(mode, {}).get("conclusion") or {}
        t.add(mode, "Conclusion: report accepted; closing message is the report; last line `Report file:`; the PDF exists", "exact",
              bool(c.get("report_accepted") and c.get("report_pdf_exists") and c.get("closing_last_line_ok")),
              "accepted, PDF present, last line names it", c or "not found")
        p = R.get(mode, {}).get("publish_timing") or {}
        t.add(mode, "Publish timing: nothing in the record before the draft was approved", "exact",
              p.get("published_before_approval") == 0, 0, p.get("published_before_approval"))
        t.judged(mode, "Report: every number in gold's at-a-glance and findings tables appears, within its band",
                 "rehearsal/gold/ reports' summary tables", "read the report artifact")
        t.judged(mode, "Completeness: every gold persisted item maps to an artifact or cited file",
                 "gold-manifest.json, column `becomes`", f"{R.get(mode, {}).get('artifacts')} artifacts, {R.get(mode, {}).get('stored_files')} stored files")

    modes = ("analyze", "interpret") if a.mode == "both" else (a.mode,)
    sys.exit(1 if t.show(modes) else 0)


if __name__ == "__main__":
    main()
