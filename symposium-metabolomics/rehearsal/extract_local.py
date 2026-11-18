#!/usr/bin/env python3
"""Extract the facts the rehearsal's assertions read from a run of the ORIGINAL skill.

    extract_local.py <run folder> <out.json> [--per-feature <out.csv>] [--transcript <md>]

The original skill writes versioned files into a folder. This walks the folder, takes the
highest version of each table it knows by stem, and reduces each to the values an assertion
compares. A stem that is absent is recorded as absent rather than guessed.
"""

import argparse
import csv
import gzip
import hashlib
import io
import json
import pathlib
import re
import sys

csv.field_size_limit(sys.maxsize)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def version_of(name):
    m = re.search(r"_v(\d+)(?=[._])", name)
    return int(m.group(1)) if m else 0


def find(root, stem, exts=(".csv", ".json", ".yaml", ".md", ".csv.gz", ".tsv")):
    """The highest-versioned file whose name starts with `stem`, anywhere under root, skipping
    folders that hold superseded versions."""
    hits = []
    for p in root.rglob("*"):
        if not p.is_file() or "previous_versions" in p.parts or "user_supplied_input_files" in p.parts:
            continue
        if p.name.startswith(stem) and p.name.endswith(exts):
            hits.append(p)
    hits.sort(key=lambda p: (version_of(p.name), p.stat().st_mtime))
    return hits[-1] if hits else None


def rows(path):
    if path is None:
        return None
    opener = gzip.open if path.name.endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8-sig", newline="") as f:
        dialect = "excel-tab" if path.suffix == ".tsv" else "excel"
        return list(csv.DictReader(f, dialect=dialect))


def num(x):
    try:
        v = float(x)
        return int(v) if v == int(v) and abs(v) < 1e15 else v
    except (TypeError, ValueError):
        return x


def col(row, *names):
    """First column present whose lowercased name contains every word of one of `names`."""
    low = {k.lower(): k for k in row}
    for n in names:
        words = n.lower().split()
        for lk, k in low.items():
            if all(w in lk for w in words):
                return k
    return None


def inputs(root):
    out = []
    man = None
    for p in root.rglob("input_files_manifest.csv"):
        man = p
    if man is None:
        return None
    folder = man.parent
    for r in rows(man):
        name = r.get("file_name", "")
        f = folder / name
        note = " ".join(str(r.get(k, "")) for k in ("source", "note")).lower()
        out.append(
            {
                "file_name": name,
                "origin": r.get("origin"),
                "source": r.get("source"),
                "task_id": r.get("task_id") or None,
                "size_bytes": f.stat().st_size if f.is_file() else num(r.get("size_bytes")),
                "sha256": sha256(f) if f.is_file() else None,
                "used": not ("not used" in note),
            }
        )
    return sorted(out, key=lambda r: r["file_name"])


def decisions(root):
    """Every decision-log row, across all versions, latest status of each block last."""
    out = []
    logs = [p for p in root.rglob("decision_log*.md")]
    logs.sort(key=lambda p: version_of(p.name))
    for p in logs:
        for line in p.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\|\s*([a-z_0-9]+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$", line)
            if m and m.group(1) not in ("block",):
                out.append({"log": p.name, "block": m.group(1), "status": m.group(2), "detail": m.group(3)})
    return out or None


def keyed(table, key_col, value_cols=None):
    if table is None:
        return None
    out = {}
    for r in table:
        k = r.get(key_col)
        if k is None:
            k = next(iter(r.values()))
        vals = {c: num(v) for c, v in r.items() if c != key_col and (value_cols is None or c in value_cols)}
        out[str(k)] = vals if len(vals) != 1 else next(iter(vals.values()))
    return out


def per_feature(root, out_csv):
    p = find(root, "per_feature_results")
    table = rows(p)
    if not table:
        return None
    r0 = table[0]
    c_id = col(r0, "row id") or next(iter(r0))
    c_fc = col(r0, "baseline log2fc surg", "baseline log2fc", "log2fc")
    c_p = col(r0, "baseline p_raw", "baseline p raw", "p_raw", "p raw")
    c_q = col(r0, "b_q_filtered", "baseline q filtered", "q_filtered", "q")
    keep = []
    for r in table:
        keep.append((r[c_id], r.get(c_fc, ""), r.get(c_p, ""), r.get(c_q, "")))
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

    return {
        "file": p.name,
        "columns_used": {"id": c_id, "effect": c_fc, "p": c_p, "q": c_q},
        "features": len(keep),
        "q_lt_0.05": sum(lt(k[3], 0.05) for k in keep),
        "p_lt_0.05": sum(lt(k[2], 0.05) for k in keep),
        "higher_in_surgery_at_q05": sum(lt(k[3], 0.05) and float(k[1]) > 0 for k in keep),
        "lower_in_surgery_at_q05": sum(lt(k[3], 0.05) and float(k[1]) < 0 for k in keep),
    }


def filter_counts(root):
    table = rows(find(root, "filter_table"))
    if not table:
        return None
    r0 = table[0]
    out = {"features_in": len(table)}
    for label, names in {
        "pass_blank": ("pass_blank",),
        "pass_prevalence": ("pass_prev",),
        "retained_first_pass": ("retained_v1", "retained"),
        "added_back": ("rescued",),
    }.items():
        c = col(r0, *names)
        if c:
            out[label] = sum(str(r[c]).strip().lower() in ("true", "1", "yes", "y") for r in table)
    c = col(r0, "origin")
    if c:
        kinds = {}
        for r in table:
            kinds[r[c]] = kinds.get(r[c], 0) + 1
        out["by_origin"] = kinds
    return out


def patterns(root):
    table = rows(find(root, "pattern_summary_final") or find(root, "pattern_summary"))
    if not table:
        return None
    out = []
    for r in table:
        out.append(
            {
                "id": r.get("pid"),
                "theme": r.get("theme"),
                "title": r.get("title"),
                "members": num(r.get("n_members")),
                "lower": num(r.get("n_lower")),
                "higher": num(r.get("n_higher")),
                "mean_log2FC": num(r.get("mean_log2FC")),
                "tier": r.get("tier_short") or r.get("tier"),
                "tag": r.get("tag"),
                "verdict": r.get("verdict"),
                "meaning": r.get("meaning"),
            }
        )
    return out


def hypotheses(root):
    p = find(root, "hypothesis_record", exts=(".yaml", ".yml"))
    if p is None:
        return None
    out, cur = [], None
    for line in p.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*-\s+id:\s*(.+)", line)
        if m:
            cur = {"id": m.group(1).strip()}
            out.append(cur)
            continue
        m = re.match(r"\s+([a-z_]+):\s*(.+)", line)
        if m and cur is not None:
            cur[m.group(1)] = m.group(2).strip()
    return out


def references(transcript):
    if not transcript:
        return None
    t = pathlib.Path(transcript).read_text(encoding="utf-8")
    seen = {}
    for title, url, acc in re.findall(
        r"^- \[([^\]]+)\]\((https?://[^)\s]+)\)(?: \((summary only|abstract only|full text)\))?", t, re.M
    ):
        seen.setdefault(url, {"title": title, "url": url, "access": acc or "summary only"})
    return list(seen.values())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("out")
    ap.add_argument("--per-feature")
    ap.add_argument("--transcript")
    a = ap.parse_args()
    root = pathlib.Path(a.root)

    def js(stem):
        p = find(root, stem, exts=(".json",))
        return json.loads(p.read_text(encoding="utf-8")) if p else None

    facts = {
        "source": str(root),
        "analyze": {
            "inputs": inputs(root),
            "decisions": decisions(root),
            "filter_counts": filter_counts(root),
            "unfiltered_filtered_validation": js("unfiltered_filtered_validation"),
            "batch_correction_check": js("batch_correction") ,
            "feature_merge_map_rows": len(rows(find(root, "feature_merge_map")) or []),
            "feature_merge_candidates": len(rows(find(root, "feature_merge_candidates")) or []),
            "timepoint_summary": keyed(rows(find(root, "timepoint_summary")), "time_point"),
            "per_feature": per_feature(root, a.per_feature),
            "detection_rate_bins": keyed(rows(find(root, "detection_rate_bins")), "bin"),
            "detection_rate_cumulative": keyed(rows(find(root, "detection_rate_cumulative")), "bin"),
            "network_summary": keyed(rows(find(root, "network_summary")), "item"),
            "network_family_sizes": keyed(rows(find(root, "network_family_sizes")), "bin"),
            "network_delta_masses": keyed(rows(find(root, "network_delta_masses")), "label", ("mass", "edges")),
            "compound_class_composition": {
                f"{r.get('class_group')} / {r.get('fine_class')}": {
                    k: num(r.get(k)) for k in ("annotated", "networked", "tested", "significant")
                }
                for r in (rows(find(root, "compound_class_composition")) or [])
            }
            or None,
            "internal_standards": [
                {k: num(r.get(k)) for k in ("standard", "group", "n", "detected", "status")}
                for r in (rows(find(root, "internal_standard_check")) or [])
            ]
            or None,
        },
        "interpret": {
            "patterns": patterns(root),
            "hypotheses": hypotheses(root),
            "key_references": references(a.transcript),
        },
    }
    pathlib.Path(a.out).write_text(json.dumps(facts, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    absent = [f"{m}.{k}" for m in ("analyze", "interpret") for k, v in facts[m].items() if v is None]
    print(f"wrote {a.out}; absent: {absent or 'none'}")


if __name__ == "__main__":
    main()
