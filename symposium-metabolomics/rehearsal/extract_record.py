#!/usr/bin/env python3
"""Extract the facts the rehearsal's assertions read from a run of THIS skill.

    extract_record.py --library <record dir> [--interpretation <record dir>]
                      [--files <dir>] [--run-json <run.json> ...] [--closing <reply.md> ...]
                      [--short-name <name>] --out facts.json [--per-feature out.csv]

`<record dir>` is a member's synced copy of a community's record: one JSON file per artifact.
`--files` holds the files the record cites, fetched beforehand, each saved as
`<artifact name>.<content name>` with any extension. `--run-json` is a mode's working file and
`--closing` the session's last message for that mode, given in the order analyze, interpret.

A record names and shapes its tables as the member who published them chose, so tables are
found by what their title and description say, and reduced to the values an assertion compares.
What cannot be found is recorded as absent, never guessed. After a change to how the skill
describes its tables, check the `absent` line this prints before reading the comparison.

Needs only the standard library.
"""

import argparse
import csv
import gzip
import io
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import extract_local as L  # noqa: E402  (the reducers are shared with the gold extractor)

csv.field_size_limit(sys.maxsize)
HEX64 = re.compile(r"\b[0-9a-f]{64}\b")


def load_record(d, short):
    out = []
    if not d:
        return out
    for p in sorted(pathlib.Path(d).glob("*.json")):
        try:
            o = json.loads(p.read_text(encoding="utf-8"))
        except ValueError:
            continue
        a = o.get("artifact") if isinstance(o, dict) else None
        if not a or not a.get("name"):
            continue  # not an artifact: the record folder holds other files too
        if short and short not in a["name"]:
            continue
        out.append(o)
    return out


def words(o):
    a = o["artifact"]
    return " ".join(str(a.get(k, "")) for k in ("name", "title", "description")).lower().replace("_", " ").replace("-", " ")


def contents(o):
    return [x for x in o.get("objects", []) if x.get("type") == "Content"]


def embedded_tables(o, prop=None):
    """Every CSV held in a string property of the artifact, as lists of row dicts; with `prop`,
    only the properties whose name holds it."""
    out = []
    for k, v in (o.get("artifact") or {}).items():
        if prop and prop not in k.lower():
            continue
        if isinstance(v, str) and "\n" in v and v.count(",") >= 2 and k not in ("description", "procedure", "text", "import_method", "rationale"):
            try:
                rows = list(csv.DictReader(io.StringIO(v)))
            except csv.Error:
                continue
            if rows and len(rows[0]) >= 2:
                out.append(rows)
    return out


def file_tables(o, files, content=None):
    out = []
    if not files:
        return out
    name = o["artifact"]["name"]
    for c in contents(o):
        if content is not None and c.get("name") != content:
            continue
        for p in pathlib.Path(files).glob(f"{name}.{c.get('name')}*"):
            if p.suffix.lower() in (".png", ".pdf", ".py", ".svg"):
                continue
            # a stored file carries no reliable name: recognise gzip by its magic bytes, and read
            # only what looks like a table (code and text are stored beside the tables too)
            with open(p, "rb") as raw:
                magic = raw.read(2)
            opener = gzip.open if magic == b"\x1f\x8b" else open
            try:
                with opener(p, "rt", encoding="utf-8-sig", newline="") as f:
                    head = f.read(4096)
                    first = head.split("\n", 1)[0]
                    if first.startswith(("#", '"""', "import ", "from ", "%PDF", "def ", "<")) or (
                        first.count(",") < 1 and first.count("\t") < 1
                    ):
                        continue
                    f.seek(0)
                    dialect = "excel-tab" if first.count("\t") > first.count(",") else "excel"
                    out.append(list(csv.DictReader(f, dialect=dialect)))
            except (OSError, csv.Error, UnicodeDecodeError, EOFError):
                continue
    return out


def find_table(arts, files, must, must_not=(), prefer_file=False, prop=None, content=None):
    """A table of the latest artifact whose name, title and description hold every word in
    `must` and none in `must_not`. One artifact often holds several tables, so `prop` narrows
    to an embedded property whose name holds it, and `content` to the file of one Content. Where
    neither is given, the largest table is taken."""
    hits = [o for o in arts if o["artifact"].get("type") == "Data" and all(w in words(o) for w in must)
            and not any(w in words(o) for w in must_not)]
    hits.sort(key=lambda o: str(o["artifact"].get("created") or ""))
    for o in reversed(hits):
        if prop is not None or content is not None:
            tabs = (embedded_tables(o, prop) if prop is not None else []) + (file_tables(o, files, content) if content is not None else [])
        elif prefer_file:
            tabs = file_tables(o, files) + embedded_tables(o)
        else:
            tabs = embedded_tables(o) + file_tables(o, files)
        if tabs:
            return max(tabs, key=len)
    return None


def keyed_first(table, value_cols=None):
    if not table:
        return None
    key = next(iter(table[0]))
    return L.keyed(table, key, value_cols)


def per_feature(table, out_csv):
    if not table:
        return None
    # a table that also carries removed features marks the retained ones; keep those
    rc = next((k for k in table[0] if k.strip().lower() in ("retained", "in_primary_family", "primary_family")), None)
    if rc and len(table) > 1:
        kept = [r for r in table if str(r[rc]).strip().lower() in ("true", "1", "yes", "y")]
        table = kept or table
    r0 = table[0]

    def exact(*patterns):
        """The first column whose whole name matches one of the patterns, in their order: a
        table may carry the same statistic for several contrasts, and the primary one is the
        one named plainly."""
        for pat in patterns:
            for k in r0:
                if re.fullmatch(pat, k.strip().lower()):
                    return k
        return None

    c_id = exact(r"row[ _]?id", r"feature[ _]?id", r"id") or L.col(r0, "row id", "feature") or next(iter(r0))
    c_fc = exact(r"primary_log2fc", r"(baseline|base|b)_log2_?fc(_surg(ery)?_vs_none)?", r"log2_?fc") or L.col(r0, "baseline log2fc")
    c_q = exact(r"primary_q", r"(baseline|base|b)_q(_filtered)?(_family)?", r"q(_value)?") or L.col(r0, "baseline q")
    c_p = exact(r"primary_p", r"(baseline|base|b)_(raw_)?p(_raw)?", r"p(_raw|_value)?") or L.col(r0, "baseline p")
    keep = [(r[c_id], r.get(c_fc, ""), r.get(c_p, "") if c_p else "", r.get(c_q, "")) for r in table]
    if out_csv:
        with open(out_csv, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["row_id", "baseline_log2FC", "baseline_p_raw", "baseline_q"])
            w.writerows(keep)

    def lt(x, t):
        try:
            return float(x) < t
        except ValueError:
            return False

    def val(x):
        try:
            return float(x)
        except ValueError:
            return 0.0

    return {
        "columns_used": {"id": c_id, "effect": c_fc, "p": c_p, "q": c_q},
        "features": len(keep),
        "q_lt_0.05": sum(lt(k[3], 0.05) for k in keep),
        "higher_in_surgery_at_q05": sum(lt(k[3], 0.05) and val(k[1]) > 0 for k in keep),
        "lower_in_surgery_at_q05": sum(lt(k[3], 0.05) and val(k[1]) < 0 for k in keep),
    }


def inputs(arts):
    out = []
    for o in arts:
        a = o["artifact"]
        if not a.get("import_method"):
            continue
        for c in contents(o):
            loc = str(c.get("location") or "")
            if not loc:
                continue
            digests = [c.get("sha256")] if c.get("sha256") else HEX64.findall(a["import_method"])
            out.append({
                "artifact": a["name"],
                "file_name": loc.rstrip("/").split("/")[-1].split("=")[-1],
                "location": loc,
                "held": "community" if loc.startswith("symposium-data:") else "outside",
                "sha256": digests[0] if digests else None,
            })
    return out or None


def conclusion(arts, run_json, closing):
    rep = [o for o in arts if "report" in o["artifact"].get("name", "") and o["artifact"].get("created")]
    pdf, approved = None, None
    if run_json and pathlib.Path(run_json).is_file():
        rj = json.loads(pathlib.Path(run_json).read_text(encoding="utf-8"))
        pdf = rj.get("report_pdf")
        approved = rj.get("draft_approved_at")
    last = ""
    if closing and pathlib.Path(closing).is_file():
        lines = [x.strip() for x in pathlib.Path(closing).read_text(encoding="utf-8").splitlines()
                 if x.strip() and not x.startswith("[turns:")]
        last = lines[-1] if lines else ""
    created = sorted(str(o["artifact"].get("created")) for o in arts if o["artifact"].get("created"))
    return (
        {
            "report_accepted": bool(rep),
            "report_pdf": pdf,
            "report_pdf_exists": bool(pdf and pathlib.Path(pdf).is_file()),
            "closing_last_line": last[:200],
            "closing_last_line_ok": bool(pdf) and last.replace("`", "") == f"Report file: {pdf}",
        },
        {
            "draft_approved_at": approved,
            "first_accepted": created[0] if created else None,
            "published_before_approval": None if not approved else sum(c < str(approved) for c in created),
        },
    )


# ---------------------------------------------------------------- the record profile
#
# reference/RECORD.md fixes each artifact's topic and the tables inside it. Read by those names
# first; the searches above are the fallback for a record made before the profile.

STAGES = {
    "qc_standards": (["internal_standards", "qc_summary"], ["sample_table"]),
    "merges": (["counts", "candidates", "merge_map"], []),
    "batch": (["check_summary"], []),
    "processing": (["normalization_comparison"], ["filter_table", "processed_filtered", "processed_unfiltered"]),
    "statistics": (["counts"], ["results", "results_unfiltered"]),
    "sensitivity": (["summary"], []),
    "multivariate": (["summary"], []),
    "detection_rate": (["bins", "cumulative"], ["per_feature"]),
    "network_classes": (["summary", "family_sizes", "families", "delta_masses", "composition", "color_key", "unclassified"],
                        ["nodes", "edges", "class_assignments"]),
    "removed_review": (["flagged", "added_back"], []),
}
COLUMNS = {
    ("statistics", "results"): ["row_id", "mz", "rt_min", "retained", "added_back", "removed_by", "primary_log2fc", "primary_p", "primary_q"],
    ("processing", "filter_table"): ["row_id", "retained", "added_back", "removed_by"],
    ("detection_rate", "bins"): ["bin", "features", "features_with_msms", "features_with_library_match"],
    ("network_classes", "summary"): ["item", "value"],
    ("network_classes", "family_sizes"): ["bin", "families"],
    ("network_classes", "delta_masses"): ["label", "mass", "edges"],
    ("network_classes", "composition"): ["class_group", "fine_class", "annotated", "networked", "tested", "significant"],
    ("merges", "candidates"): ["row_id_a", "row_id_b", "class", "decision"],
    ("batch", "check_summary"): ["item", "value"],
}


def by_topic(arts, topic):
    pat = re.compile(r".*_" + re.escape(topic) + r"_v(\d+)$")
    hits = [(int(pat.match(o["artifact"]["name"]).group(1)), o) for o in arts if pat.match(o["artifact"]["name"])]
    return max(hits, key=lambda h: h[0])[1] if hits else None


def prop_table(o, prop):
    v = (o or {}).get("artifact", {}).get(prop) if o else None
    if not isinstance(v, str) or "\n" not in v:
        return None
    try:
        rows = list(csv.DictReader(io.StringIO(v)))
    except csv.Error:
        return None
    return rows or None


def file_table(o, files, name):
    if not o:
        return None
    tabs = file_tables(o, files, f"{name}_download")
    return max(tabs, key=len) if tabs else None


def record_shape(arts, files):
    """What the profile requires and the record lacks, as a list of short descriptions."""
    missing = []
    goal = by_topic(arts, "goal")
    if not goal or goal["artifact"].get("type") != "ResearchGoal":
        missing.append("goal")
    else:
        for k in ("skill", "mode", "short_name", "task"):
            if not goal["artifact"].get(k):
                missing.append(f"goal.{k}")
    if not by_topic(arts, "input_feature_table"):
        missing.append("input_feature_table")
    for stage, (props, fls) in STAGES.items():
        if not by_topic(arts, f"analysis_{stage}"):
            missing.append(f"analysis_{stage}")
        d = by_topic(arts, f"data_{stage}")
        if not d:
            missing.append(f"data_{stage}")
            continue
        names = {c.get("name") for c in contents(d)}
        for pr in props:
            if pr not in d["artifact"]:
                missing.append(f"data_{stage}.{pr}")
            elif f"{pr}_csv" not in names:
                missing.append(f"data_{stage}.{pr}_csv")
        for fl in fls:
            if f"{fl}_download" not in names:
                missing.append(f"data_{stage}.{fl}_download")
        for (st, tab), cols in COLUMNS.items():
            if st != stage:
                continue
            t = prop_table(d, tab) if tab in props else file_table(d, files, tab)
            if t is None:
                if files or tab in props:
                    missing.append(f"data_{stage}.{tab} (unreadable)")
                continue
            have = {k.strip() for k in t[0]}
            for c in cols:
                if c not in have:
                    missing.append(f"data_{stage}.{tab}.{c}")
    for t in ("handoff", "technical_report"):
        if not by_topic(arts, t):
            missing.append(t)
    return missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--library", required=True)
    ap.add_argument("--interpretation")
    ap.add_argument("--files")
    ap.add_argument("--run-json", action="append", default=[])
    ap.add_argument("--closing", action="append", default=[])
    ap.add_argument("--short-name", default="")
    ap.add_argument("--out", required=True)
    ap.add_argument("--per-feature")
    a = ap.parse_args()
    lib = load_record(a.library, a.short_name)
    itp = load_record(a.interpretation, "")
    F = a.files

    def T(must, must_not=(), prefer_file=False, prop=None, content=None):
        return find_table(lib, F, must, must_not, prefer_file, prop, content)

    P = lambda topic: by_topic(lib, topic)
    filt = file_table(P("data_processing"), F, "filter_table")
    for o in ([] if filt else lib):
        if o["artifact"].get("type") != "Data":
            continue
        for c in contents(o):
            if "filter" in c.get("name", "") and "table" in c.get("name", ""):
                tabs = file_tables(o, F, c["name"])
                if tabs:
                    filt = max(tabs, key=len)
    filt = filt or T(["filter"], ["candidate", "merge"], content="download") or T(["filter"], ["candidate", "merge"], prefer_file=True)
    fc = None
    if filt:
        fc = {"features_in": len(filt)}
        c = L.col(filt[0], "rescued", "added back", "added_back")
        if c:
            fc["added_back"] = sum(str(r[c]).strip().lower() in ("true", "1", "yes", "y") for r in filt)
    status = None
    cs = prop_table(by_topic(lib, "data_batch"), "check_summary")
    if cs:
        st = {str(r.get("item")).strip(): str(r.get("value")).strip() for r in cs}.get("status")
        status = st or None
    for o in ([] if status else lib):
        if o["artifact"].get("type") in ("Data", "Analysis"):
            text = json.dumps(o["artifact"]).lower()
            if "batch" not in text:
                continue
            if re.search(r"batch[^.]{0,200}not possible|not possible[^.]{0,200}batch|pooled_qc_available\W+(no|false)", text):
                status = "not possible"
            elif status is None and "batch" in words(o):
                status = "check run"
    norm = [o["artifact"].get("procedure", "") for o in lib if o["artifact"].get("type") == "Analysis" and "normaliz" in words(o)]
    mmap = prop_table(by_topic(lib, "data_merges"), "merge_map") or T(["merge"], prop="map")
    has_map = mmap is not None or any("merge" in words(o) and "map" in words(o) for o in lib)
    # the primary per-feature results are the table, among those the record holds, that carries a
    # plainly named baseline q column; of several, the one for the primary family (not the
    # unfiltered table) and, after that, the largest
    pf, best = file_table(P("data_statistics"), F, "results"), None
    for o in ([] if pf else lib):
        if o["artifact"].get("type") != "Data":
            continue
        for tab in file_tables(o, F) + embedded_tables(o):
            if not tab:
                continue
            cols = [k.strip().lower() for k in tab[0]]
            if not any(re.fullmatch(r"(baseline|base|b)_q(_filtered)?(_family)?", c) for c in cols):
                continue
            # the abundance results carry an effect size; a detection table carries only p and q
            has_fc = any(re.fullmatch(r"(baseline|base|b)_log2_?fc(_surg(ery)?_vs_none)?", c) for c in cols)
            key = (has_fc, "unfiltered" not in words(o), len(tab))
            if best is None or key > best:
                pf, best = tab, key
    c1, t1 = conclusion(lib, a.run_json[0] if a.run_json else None, a.closing[0] if a.closing else None)
    analyze = {
        "inputs": inputs(lib),
        "procedures": [o["artifact"]["name"] for o in lib if o["artifact"].get("type") == "Analysis"] or None,
        "filter_counts": fc,
        "batch_correction_check": {"status": status} if status else None,
        "normalization": (norm[-1][:400] if norm else None),
        "feature_merge_candidates": len(prop_table(P("data_merges"), "candidates") or T(["merge"], prop="candidate") or T(["merge", "candidate"]) or []) or None,
        "feature_merge_map_rows": len(mmap or []) if has_map else None,
        "per_feature": per_feature(pf, a.per_feature),
        "detection_rate_bins": keyed_first(prop_table(P("data_detection_rate"), "bins") or T(["detection"], prop="bins")),
        "detection_rate_cumulative": keyed_first(prop_table(P("data_detection_rate"), "cumulative") or T(["detection"], prop="cumulative")),
        "network_summary": keyed_first(prop_table(P("data_network_classes"), "summary") or T(["network"], prop="summary")),
        "network_family_sizes": keyed_first(prop_table(P("data_network_classes"), "family_sizes") or T(["network"], prop="family_size")),
        "network_delta_masses": keyed_first(prop_table(P("data_network_classes"), "delta_masses") or T(["network"], prop="delta"), ("mass", "edges")),
        "compound_class_composition": {
            f"{r.get('class_group')} / {r.get('fine_class')}": {k: L.num(r.get(k)) for k in ("annotated", "networked", "tested", "significant")}
            for r in (prop_table(P("data_network_classes"), "composition") or T(["class"], prop="composition") or T(["class", "composition"]) or [])
        } or None,
        "record_shape_missing": record_shape(lib, F),
        "artifacts": len(lib),
        "stored_files": sum(1 for o in lib for c in contents(o) if str(c.get("location", "")).startswith("symposium-data:")),
        "conclusion": c1,
        "publish_timing": t1,
    }
    facts = {"source": {"library": a.library, "interpretation": a.interpretation}, "analyze": analyze}

    if a.interpretation:
        def pubs(arts):
            out = []
            for o in arts:
                if o["artifact"].get("type") != "ScientificPublication":
                    continue
                out += [str(c["location"]) for c in contents(o) if c.get("location") and not str(c["location"]).startswith("symposium-data:")]
                out += [str(o["artifact"][k]) for k in ("doi", "identifier", "pmid", "url") if o["artifact"].get(k)]
            return out

        libnames = {o["artifact"]["name"]: o for o in lib}
        mismatches = checked = 0
        for o in itp:
            named = re.findall(r"`([A-Za-z0-9_\-]+)`", str(o["artifact"].get("import_method", "")))
            src = [n for n in named if n in libnames]
            if not src:
                continue
            checked += 1
            s = libnames[src[0]]
            if file_tables(s, F):
                continue  # rows cut from a file: compared by the driver against the file itself
            held = " ".join(v for v in s["artifact"].values() if isinstance(v, str))
            for k, v in o["artifact"].items():
                if isinstance(v, str) and k not in ("description", "import_method", "title", "name", "type") and len(v) > 40:
                    if not all(x in held for x in v.splitlines() if x.strip()):
                        mismatches += 1
        args = [o for o in itp if o["artifact"].get("type") == "Argument"]
        c2, t2 = conclusion(itp, a.run_json[1] if len(a.run_json) > 1 else None, a.closing[1] if len(a.closing) > 1 else None)
        facts["interpret"] = {
            "findings": [{"name": o["artifact"]["name"], "title": o["artifact"].get("title"),
                          "claim": next((x.get("claim") for x in o.get("objects", []) if x.get("name") == o["artifact"].get("primary_assertion")), None),
                          "verdict": str(o["artifact"].get("verdict", ""))[:300]} for o in args],
            "conjectures": [o["artifact"].get("title") for o in itp
                            if o["artifact"].get("type") == "NonGroundable" and "report" not in o["artifact"]["name"]],
            "library_sources": sorted(set(pubs(lib))),
            "cited_sources": sorted(set(pubs(itp))),
            "arguments_in_library": sum(1 for o in lib if o["artifact"].get("type") == "Argument"),
            "pointers_checked": checked,
            "pointer_mismatches": mismatches if checked else None,
            "artifacts": len(itp),
            "stored_files": sum(1 for o in itp for c in contents(o) if str(c.get("location", "")).startswith("symposium-data:")),
            "conclusion": c2,
            "publish_timing": t2,
        }
    pathlib.Path(a.out).write_text(json.dumps(facts, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    absent = [f"{m}.{k}" for m in facts if m != "source" for k, v in facts[m].items() if v is None]
    print(f"wrote {a.out}; absent: {absent or 'none'}")


if __name__ == "__main__":
    main()
