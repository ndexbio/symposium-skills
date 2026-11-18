#!/usr/bin/env python3
"""qcrsc.py - QC-based batch/drift correction (QCRSC) with honest validation.

Part of the metabolomics interpretation skillset (Part 1, Section 3.10). Version 1.0 (4 Nov 2026).

METHOD
  QCRSC = quality-control-based robust spline signal correction. For every feature and every batch, a
  smoothing spline is fitted to the pooled-QC signal against injection order (natural-log scale; smoothing
  parameter chosen by 5-fold cross-validation); every injection in the batch is multiplied by
  (QC median / fitted trend). Batches are then aligned on their QC medians. Batches with 5-9 positive QCs use a
  robust (Huber) straight line instead; batches with fewer than 5 are left uncorrected and flagged.
  Zeros and missing values are never changed. Study samples and blanks never enter a fit.

  Implementation of the QC-RLSC / QCRSC approach of:
    Dunn WB et al. (2011) Nat Protoc 6:1060-1083. doi:10.1038/nprot.2011.335
    Broadhurst D et al. (2018) Metabolomics 14:72. doi:10.1007/s11306-018-1367-3
    Broadhurst DI. QC:MXP v3.2 (2025). doi:10.5281/zenodo.11101541  (reference implementation, Matlab)
  Validated against QC:MXP on one dataset (301 features, GNPS2 Everything Bagel task 9b80f45b...):
  median Spearman 0.996 between corrected sample values. This script is NOT QC:MXP.

HONEST VALIDATION
  A flexible spline always fits the QCs it was trained on, so in-sample QC RSD after correction is meaningless.
  `correct` therefore scores every QC with a model that never saw it (QCs alternate within each batch between
  two halves; each half is corrected by a model trained on the other half). Held-out numbers are the ones to report.

COMMANDS
  python qcrsc.py check   --quant Q.csv --injections I.csv --out DIR [--prefix batch_correction_v1]
      Diagnostics on the table as given (raw OR already corrected). Writes <prefix>_check_features.csv and
      <prefix>_check_summary.json with the recommendation (recommend / ask / skip). Changes no values.
  python qcrsc.py correct --quant Q.csv --injections I.csv --out DIR [--prefix batch_correction_v1]
      check + correction + held-out validation. Writes <prefix>_corrected.csv, <prefix>_features.csv,
      <prefix>_heldout_qc.csv, <prefix>_summary.json (and <prefix>_group_by_batch.csv if --group-col is given).
  python qcrsc.py selftest
      Synthetic data with a known batch shift and drift; also a no-effect null. Exit code 1 if it fails.

INPUTS
  Injection table CSV with columns SampleID, SampleType, Order, Batch (any case). SampleType: QC / Blank / Sample
  (pool, pooled, qcpool are read as QC; anything else is kept and corrected but never used for fitting).
  Order = injection order, numeric, increasing over the whole run. Batch = batch label (e.g. sequence file).
  Quant table CSV, either features in rows (first column = feature ID, one column per SampleID) or samples in
  rows (a SampleID column; numeric columns are features). A QC:MXP TidyMetqc data table works as both files.
  Requires numpy, pandas, scipy >= 1.10.
"""
import argparse, json, os, sys, warnings
import numpy as np
import pandas as pd
from scipy import stats
from scipy.interpolate import make_smoothing_spline

VERSION = "1.0"
LAMS = 10.0 ** np.arange(-7, 2)
MIN_SPLINE, MIN_LINEAR = 10, 5
# Decision thresholds (calibrated on one dataset; see Part 1, Section 3.10.4)
Q_CUT, R2_CUT = 0.05, 0.14
TRIGGER_RECOMMEND, TRIGGER_ASK = 0.10, 0.02
SHIFT_FOLD, DRIFT_RHO, DRIFT_P = 1.2, 0.3, 0.05
OK_HELDOUT_AFFECTED, OK_MEDIAN_RSD = 0.05, 20.0
MIN_QC_DETECT = 0.8
RESERVED = {"sampleid", "sampletype", "order", "batch", "qc", "blank", "reference", "sample", "ignore"}
QC_NAMES = {"qc", "pool", "pooled", "qcpool", "pooledqc", "poolqc", "pooled_qc", "qc_pool"}
BLANK_NAMES = {"blank", "blk", "solventblank", "procedural blank"}


# ----------------------------------------------------------------------------- core math
def _cv_lam(x, ly, k=5):
    best, bl, n = 1e99, LAMS[4], len(x)
    fold = np.arange(n) % k
    for lam in LAMS:
        err = 0.0
        for f in range(k):
            tr = fold != f
            try:
                s = make_smoothing_spline(x[tr], ly[tr], lam=lam)
                err += np.sum((s(x[~tr]) - ly[~tr]) ** 2)
            except Exception:
                err = 1e99
                break
        if err < best:
            best, bl = err, lam
    return bl


def _huber_line(xn, ly):
    w = np.ones_like(xn)
    for _ in range(20):
        c = np.polyfit(xn, ly, 1, w=w)
        r = ly - np.polyval(c, xn)
        s = 1.4826 * np.median(np.abs(r)) + 1e-9
        w = np.where(np.abs(r) <= 1.345 * s, 1, 1.345 * s / np.abs(r))
    return c


def fit_trend(xq, yq, xa):
    """Log-scale trend of the QC signal at injection orders xa. Returns (trend or None, method)."""
    ok = yq > 0
    x, y = xq[ok], yq[ok]
    if len(y) < MIN_LINEAR:
        return None, "too_few"
    srt = np.argsort(x, kind="stable")
    x, ly = x[srt], np.log(y[srt])
    lo, hi = x.min(), x.max()
    sc = (hi - lo) or 1.0
    xn, xan = (x - lo) / sc, np.clip((xa - lo) / sc, 0, 1)  # extrapolation is clamped to the end-QC value
    if len(y) >= MIN_SPLINE:
        if len(np.unique(xn)) < len(xn):  # tied injection orders: average them
            xu, inv = np.unique(xn, return_inverse=True)
            ly = np.bincount(inv, weights=ly) / np.bincount(inv)
            xn = xu
        if len(xn) >= MIN_SPLINE:
            return make_smoothing_spline(xn, ly, lam=_cv_lam(xn, ly))(xan), "spline"
    return np.polyval(_huber_line(xn, ly), xan), "linear"


def correct_row(v, order, bidx, nb, train):
    """Correct one feature. v: values over injections; train: boolean mask of QCs allowed in the fit.
    Returns (corrected values, list of per-batch methods)."""
    c = v.astype(float).copy()
    methods = []
    for b in range(nb):
        files = bidx == b
        q = files & train
        yq = v[q]
        f, m = fit_trend(order[q], yq, order[files])
        methods.append(m)
        if f is None:
            continue
        med = np.exp(np.median(np.log(yq[yq > 0])))
        vb = v[files]
        c[files] = np.where(vb > 0, vb * med / np.exp(f), vb)
    qm = np.full(nb, np.nan)  # between-batch alignment on training-QC medians
    for b in range(nb):
        x = c[(bidx == b) & train]
        x = x[x > 0]
        if len(x) >= 3:
            qm[b] = np.median(x)
    if np.isfinite(qm).any():
        g = np.nanmedian(qm)
        for b in range(nb):
            if np.isfinite(qm[b]) and qm[b] > 0:
                files = bidx == b
                vb = c[files]
                c[files] = np.where(vb > 0, vb * g / qm[b], vb)
    return c, methods


def rsd(a):
    a = np.asarray(a, float)
    a = a[np.isfinite(a) & (a > 0)]
    return np.nan if len(a) < 3 else 100 * a.std(ddof=1) / a.mean()


def bh(p):
    p = pd.Series(p).dropna().sort_values()
    n = len(p)
    q = (p * n / np.arange(1, n + 1))[::-1].cummin()[::-1].clip(upper=1)
    return q


# ----------------------------------------------------------------------------- diagnostics
def batch_r2(y, g):
    """Effect size and p of a one-way ANOVA of log10 QC signal by batch (positive values only)."""
    m = y > 0
    y, g = np.log10(y[m]), g[m]
    if len(y) < 3 or len(np.unique(y)) < 3:
        return np.nan, np.nan
    grp = [y[g == k] for k in np.unique(g) if (g == k).sum() > 1]
    if len(grp) < 2:
        return np.nan, np.nan
    F, p = stats.f_oneway(*grp)
    ssb = sum(len(x) * (x.mean() - y.mean()) ** 2 for x in grp)
    sst = ((y - y.mean()) ** 2).sum()
    return (ssb / sst if sst > 0 else np.nan), p


def qc_diag(Y, order, g):
    """Y: features x QCs. Per feature: batch R2, p, fold range of batch QC medians, within-batch drift."""
    rows = []
    for y in Y:
        r2, p = batch_r2(y, g)
        meds = [np.median(y[(g == k) & (y > 0)]) for k in np.unique(g) if ((g == k) & (y > 0)).sum() >= 3]
        fold = max(meds) / min(meds) if len(meds) >= 2 else np.nan
        mrho, flag, rhos = np.nan, False, []
        for k in np.unique(g):
            m = (g == k) & (y > 0)
            if m.sum() >= 8:
                rho, pp = stats.spearmanr(order[m], y[m])
                if np.isfinite(rho):
                    rhos.append(abs(rho))
                    mrho = abs(rho) if not np.isfinite(mrho) else max(mrho, abs(rho))
                    flag = flag or (abs(rho) >= DRIFT_RHO and pp < DRIFT_P)
        rows.append((r2, p, fold, mrho, float(np.mean(rhos)) if rhos else np.nan, flag))
    d = pd.DataFrame(rows, columns=["batch_r2", "batch_p", "fold_range", "drift_max_abs_rho", "drift_mean_abs_rho", "drift_flag"])
    d["batch_q"] = bh(d.batch_p).reindex(d.index).values if d.batch_p.notna().any() else np.nan
    d["batch_affected"] = (d.batch_q < Q_CUT) & (d.batch_r2 >= R2_CUT)
    return d


def decision_from(d, n_batches):
    n = len(d)
    if n < 20:
        return "ask", f"only {n} eligible features; too few to judge the dataset"
    if n_batches >= 2:
        frac = float(d.batch_affected.mean())
        basis = "batch test (q<%.2f and R2>=%.2f)" % (Q_CUT, R2_CUT)
    else:
        frac = float(d.drift_flag.mean())
        basis = "within-batch drift only (single batch; exploratory)"
    if frac >= TRIGGER_RECOMMEND:
        return "recommend", f"{100*frac:.1f}% of eligible features affected by {basis}"
    if frac >= TRIGGER_ASK:
        return "ask", f"{100*frac:.1f}% of eligible features affected by {basis}"
    return "skip", f"{100*frac:.1f}% of eligible features affected by {basis}"


# ----------------------------------------------------------------------------- IO
def _col(df, name):
    for c in df.columns:
        if c.strip().lower() == name:
            return c
    return None


def read_inputs(a):
    inj = pd.read_csv(a.injections)
    ren = {}
    for n, std in (("sampleid", "SampleID"), ("sampletype", "SampleType"), ("order", "Order"), ("batch", "Batch")):
        c = _col(inj, n)
        if c is None:
            sys.exit(f"ERROR: injection table lacks a {std} column (found: {list(inj.columns)})")
        ren[c] = std
    inj = inj.rename(columns=ren)
    inj["SampleID"] = inj["SampleID"].astype(str)
    if inj.SampleID.duplicated().any():
        sys.exit("ERROR: duplicate SampleID in the injection table: " + ", ".join(inj.SampleID[inj.SampleID.duplicated()].head(5)))
    inj["Order"] = pd.to_numeric(inj["Order"], errors="coerce")
    if inj.Order.isna().any():
        sys.exit("ERROR: Order must be numeric for every injection")
    q = pd.read_csv(a.quant, low_memory=False)
    orient = a.orient
    ids = set(inj.SampleID)
    if orient == "auto":
        orient = "features" if len(ids & set(map(str, q.columns))) >= 0.5 * len(ids) else "samples"
    if orient == "features":
        idc = a.id_col or q.columns[0]
        q[idc] = q[idc].astype(str)
        cols = [c for c in q.columns if str(c) in ids]
        missing = ids - set(map(str, cols))
        if missing:
            sys.exit(f"ERROR: {len(missing)} injections in the injection table are not columns of the quant table, e.g. {sorted(missing)[:5]}")
        inj = inj.set_index("SampleID").loc[[str(c) for c in cols]].reset_index()
        X = q[cols].apply(pd.to_numeric, errors="coerce").to_numpy(float)
        extra = q.drop(columns=cols + [idc])
        meta = dict(orient="features", idc=idc, cols=cols, table=q, extra=extra)
        fid = q[idc].values
    else:
        sidc = _col(q, "sampleid")
        if sidc is None:
            sys.exit("ERROR: samples-in-rows quant table needs a SampleID column")
        q[sidc] = q[sidc].astype(str)
        q = q.set_index(sidc, drop=False).loc[inj.SampleID]
        skip = RESERVED | {m.lower() for m in (a.meta_cols or [])}
        fcols = [c for c in q.columns if c.strip().lower() not in skip and pd.api.types.is_numeric_dtype(q[c])]
        X = q[fcols].to_numpy(float).T
        meta = dict(orient="samples", table=q, fcols=fcols, sidc=sidc)
        fid = np.array(fcols)
    typ = inj.SampleType.astype(str).str.strip().str.lower()
    kind = np.where(typ.isin(QC_NAMES), "QC", np.where(typ.isin(BLANK_NAMES), "Blank", np.where(typ == "sample", "Sample", "Other")))
    if (kind == "QC").sum() == 0:
        sys.exit("ERROR: no pooled QC injections (SampleType QC). QCRSC cannot run without them.")
    batches = pd.Series(inj.Batch.astype(str))
    ub = sorted(batches.unique(), key=lambda s: (float(s) if s.replace(".", "", 1).isdigit() else 1e18, s))
    bidx = batches.map({b: i for i, b in enumerate(ub)}).to_numpy()
    return dict(X=X, inj=inj, kind=kind, order=inj.Order.to_numpy(float), bidx=bidx, ub=ub, fid=fid, meta=meta)


# ----------------------------------------------------------------------------- run
def eligibility(X, isqc, bidx, nb, min_detect):
    pos = X[:, isqc] > 0
    det = pos.mean(axis=1)
    npos = pos.sum(axis=1)
    per_b = np.stack([(X[:, isqc & (bidx == b)] > 0).sum(axis=1) for b in range(nb)], axis=1)
    ok = (det >= min_detect) & (npos >= MIN_SPLINE)
    reason = np.where(ok, "", np.where(npos < MIN_SPLINE, "fewer_than_10_positive_QCs", "qc_detection_below_%.0f%%" % (100 * min_detect)))
    return ok, det, per_b, reason


def _work(args):
    row, order, bidx, nb, isqc, A, B = args
    full, meth = correct_row(row, order, bidx, nb, isqc)
    hA, _ = correct_row(row, order, bidx, nb, A)
    hB, _ = correct_row(row, order, bidx, nb, B)
    held = np.where(B, hA, hB)[isqc]  # each QC corrected by a model that never saw it
    return full, held, meth


def run(a, do_correct):
    D = read_inputs(a)
    X, inj, kind, order, bidx, ub = D["X"], D["inj"], D["kind"], D["order"], D["bidx"], D["ub"]
    nb, isqc = len(ub), D["kind"] == "QC"
    ok, det, per_b, reason = eligibility(X, isqc, bidx, nb, a.min_qc_detect)
    print(f"{X.shape[0]} features, {X.shape[1]} injections ({isqc.sum()} QC, {(kind=='Blank').sum()} blank, "
          f"{(kind=='Sample').sum()} sample), {nb} batches; {ok.sum()} eligible (QC detection >= {a.min_qc_detect:.0%} and >= {MIN_SPLINE} positive QCs)")
    if nb > 1 and (per_b[ok] >= MIN_LINEAR).all(axis=0).sum() < nb:
        print(f"WARNING: some batches have fewer than {MIN_LINEAR} positive QCs for many features; those batches are left uncorrected.")
    ei = np.where(ok)[0]
    raw = qc_diag(X[ei][:, isqc], order[isqc], bidx[isqc])
    raw.index = ei
    dec, why = decision_from(raw, nb)
    feat = pd.DataFrame({"feature_id": D["fid"], "qc_detection": det, "eligible": ok, "ineligible_reason": reason})
    for b in range(nb):
        feat[f"n_pos_qc_batch_{ub[b]}"] = per_b[:, b]
    for c in raw.columns:
        feat.loc[ei, c + "_raw"] = raw[c].values
    feat["shift_ge_%.1f" % SHIFT_FOLD] = feat["fold_range_raw"] >= SHIFT_FOLD
    os.makedirs(a.out, exist_ok=True)
    pre = os.path.join(a.out, a.prefix)
    summ = dict(script="qcrsc.py", version=VERSION, scipy=__import__("scipy").__version__, quant=os.path.basename(a.quant),
                injections=os.path.basename(a.injections), n_features=int(X.shape[0]), n_injections=int(X.shape[1]),
                n_qc=int(isqc.sum()), n_batches=nb, batches=ub, n_eligible=int(ok.sum()), min_qc_detect=a.min_qc_detect,
                thresholds=dict(batch_q=Q_CUT, batch_r2=R2_CUT, trigger_recommend=TRIGGER_RECOMMEND, trigger_ask=TRIGGER_ASK,
                                shift_fold=SHIFT_FOLD, drift_rho=DRIFT_RHO, drift_p=DRIFT_P),
                raw=dict(frac_batch_affected=float(raw.batch_affected.mean()) if len(raw) else None,
                         median_batch_r2=float(raw.batch_r2.median()) if len(raw) else None,
                         frac_shift_ge_threshold=float((raw.fold_range >= SHIFT_FOLD).mean()) if len(raw) else None,
                         frac_drift_flag=float(raw.drift_flag.mean()) if len(raw) else None,
                         median_qc_rsd=float(np.nanmedian([rsd(X[i, isqc]) for i in ei])) if len(ei) else None),
                recommendation=dec, recommendation_basis=why)
    if a.group_col:
        gc = _col(inj, a.group_col.lower())
        if gc is None:
            print(f"WARNING: --group-col {a.group_col} is not a column of the injection table; no group-by-batch table written")
        else:
            sm = kind == "Sample"
            pd.crosstab(inj[gc][sm].rename(a.group_col), pd.Series(np.array(ub)[bidx][sm], name="Batch")).to_csv(pre + "_group_by_batch.csv")
    print(f"RECOMMENDATION: {dec.upper()} - {why}")
    if not do_correct:
        feat.to_csv(pre + "_check_features.csv", index=False)
        json.dump(summ, open(pre + "_check_summary.json", "w"), indent=1)
        print("wrote", pre + "_check_features.csv,", pre + "_check_summary.json")
        return summ
    # ---- correction with held-out validation
    from multiprocessing import Pool
    qi = np.where(isqc)[0]
    qs = pd.DataFrame({"i": qi, "b": bidx[qi], "o": order[qi]}).sort_values(["b", "o"], kind="stable")
    qs["rank"] = qs.groupby("b").cumcount()
    A = np.zeros(len(order), bool)
    B = np.zeros(len(order), bool)
    A[qs.i[qs["rank"] % 2 == 0].values] = True
    B[qs.i[qs["rank"] % 2 == 1].values] = True
    jobs = [(X[i], order, bidx, nb, isqc, A, B) for i in ei]
    if a.workers > 1 and len(jobs) > 8:
        with Pool(a.workers) as p:
            res = p.map(_work, jobs, chunksize=max(1, len(jobs) // (a.workers * 8)))
    else:
        res = [_work(j) for j in jobs]
    C = X.astype(float).copy()
    H = np.full((X.shape[0], isqc.sum()), np.nan)
    corr_state = np.full(X.shape[0], "no", dtype=object)
    reason2 = reason.astype(object).copy()
    for i, (full, held, meth) in zip(ei, res):
        C[i], H[i] = full, held
        n_fit = sum(m in ("spline", "linear") for m in meth)
        corr_state[i] = "yes" if n_fit == nb else ("partial" if n_fit > 0 else "no")
        if n_fit < nb:
            reason2[i] = "batches_left_uncorrected(<5_positive_QCs):" + ",".join(str(ub[b]) for b, m in enumerate(meth) if m == "too_few")
    feat["batch_corrected"] = corr_state
    feat["batch_corrected_reason"] = reason2
    Hq = H[ei]
    after = qc_diag(Hq, order[isqc], bidx[isqc])
    after.index = ei
    for c in after.columns:
        feat.loc[ei, c + "_heldout"] = after[c].values
    rng = np.random.default_rng(a.seed)
    Bn = 1000
    qraw = X[:, isqc]
    delta_all, brow = [], []
    for i in ei:
        x, y = qraw[i], H[i]
        m = (x > 0) & (y > 0)
        x, y = x[m], y[m]
        feat.loc[i, "qc_rsd_raw"] = rsd(x)
        feat.loc[i, "qc_rsd_heldout"] = rsd(y)
        if len(x) < 20:
            continue
        idx = rng.integers(0, len(x), size=(Bn, len(x)))
        r = lambda v: 100 * v[idx].std(axis=1, ddof=1) / v[idx].mean(axis=1)
        d = r(x) - r(y)
        pv = min(1.0, max(2 * min((d <= 0).mean(), (d >= 0).mean()), 1 / Bn))
        feat.loc[i, ["delta_rsd", "delta_ci_lo", "delta_ci_hi", "delta_boot_p"]] = [rsd(x) - rsd(y), *np.percentile(d, [2.5, 97.5]), pv]
        delta_all.append(d)
    feat["significantly_worse"] = (feat.delta_boot_p < 0.05) & (feat.delta_rsd < 0)
    feat["significantly_better"] = (feat.delta_boot_p < 0.05) & (feat.delta_rsd > 0)
    pooled = np.mean(delta_all, axis=0) if delta_all else np.array([np.nan])
    ha = float(after.batch_affected.mean()) if len(after) else None
    medr = float(np.nanmedian(feat.loc[ei, "qc_rsd_heldout"])) if len(ei) else None
    summ.update(held_out=dict(frac_batch_affected=ha, median_qc_rsd_before=float(np.nanmedian(feat.loc[ei, "qc_rsd_raw"])),
                              median_qc_rsd_after=medr, n_improved_sig=int(feat.significantly_better.sum()),
                              n_worse_sig=int(feat.significantly_worse.sum()),
                              pooled_delta_mean=float(np.mean(pooled)), pooled_delta_ci95=[float(v) for v in np.percentile(pooled, [2.5, 97.5])],
                              bootstrap_resamples=Bn, seed=a.seed,
                              frac_drift_flag=float(after.drift_flag.mean()) if len(after) else None,
                              correction_worked=bool(ha is not None and ha < OK_HELDOUT_AFFECTED and medr is not None and medr <= OK_MEDIAN_RSD)),
                n_corrected_yes=int((corr_state == "yes").sum()), n_corrected_partial=int((corr_state == "partial").sum()),
                n_not_corrected=int((corr_state == "no").sum()))
    # corrected table in the input layout
    meta = D["meta"]
    if meta["orient"] == "features":
        out = meta["extra"].copy()
        out.insert(0, meta["idc"], meta["table"][meta["idc"]].values)
        out["batch_corrected"], out["batch_corrected_reason"] = corr_state, reason2
        for j, c in enumerate(meta["cols"]):
            out[c] = C[:, j]
    else:
        out = meta["table"].copy()
        for j, c in enumerate(meta["fcols"]):
            out[c] = C[j]
    out.to_csv(pre + "_corrected.csv", index=False)
    pd.DataFrame(H, index=D["fid"], columns=inj.SampleID[isqc].values).to_csv(pre + "_heldout_qc.csv")
    feat.to_csv(pre + "_features.csv", index=False)
    json.dump(summ, open(pre + "_summary.json", "w"), indent=1, default=str)
    ho = summ["held_out"]
    print(f"HELD-OUT: features with batch effect {100*summ['raw']['frac_batch_affected']:.1f}% -> {100*ha:.1f}%; median QC RSD "
          f"{summ['raw']['median_qc_rsd']:.1f}% -> {medr:.1f}%; significantly improved {ho['n_improved_sig']}, worse {ho['n_worse_sig']}; "
          f"correction_worked={ho['correction_worked']}")
    print("wrote", pre + "_corrected.csv, _features.csv, _heldout_qc.csv, _summary.json")
    return summ


# ----------------------------------------------------------------------------- selftest
def _synthetic(n_feat, n_batch, n_qc, shift, drift, seed):
    rng = np.random.default_rng(seed)
    rows, order = [], 0
    for b in range(n_batch):
        for k in range(n_qc + 3 * n_qc):  # 1 QC then 3 samples
            order += 1
            rows.append((f"S{order}", "QC" if k % 4 == 0 else "Sample", order, f"B{b+1}"))
    inj = pd.DataFrame(rows, columns=["SampleID", "SampleType", "Order", "Batch"])
    bi = inj.Batch.str[1:].astype(int).to_numpy() - 1
    pos = inj.groupby("Batch").cumcount().to_numpy() / (4 * n_qc)
    base = rng.uniform(1e5, 1e7, n_feat)[:, None]
    fb = np.exp(rng.normal(0, np.log(1.4), (n_feat, n_batch))) if shift else np.ones((n_feat, n_batch))
    fd = np.exp(rng.normal(0, 0.35, n_feat))[:, None] * np.ones((1, len(inj))) if drift else np.ones((n_feat, len(inj)))
    slope = rng.normal(0, 0.3, n_feat)[:, None] * (pos[None] - 0.5) if drift else 0
    bio = np.exp(rng.normal(0, 0.5, (n_feat, len(inj))))
    qc = (inj.SampleType == "QC").to_numpy()
    bio[:, qc] = 1.0
    X = base * fb[:, bi] * np.exp(slope) * bio * np.exp(rng.normal(0, 0.08, (n_feat, len(inj))))
    X[rng.random(X.shape) < 0.05] = 0.0
    return inj, X


def selftest():
    import tempfile
    warnings.filterwarnings("ignore")
    d = tempfile.mkdtemp()
    bad = []
    for name, shift, drift in (("effect", True, True), ("null", False, False)):
        inj, X = _synthetic(60, 4, 12, shift, drift, 7 if shift else 8)
        q = pd.DataFrame(X, columns=inj.SampleID)
        q.insert(0, "feature", [f"f{i}" for i in range(len(q))])
        if shift:
            q.iloc[0, 1:] = 0.0  # one never-detected feature: must be flagged, not corrected
            q.iloc[1, 1:] = np.where(inj.SampleType.eq("QC").to_numpy(), 0.0, q.iloc[1, 1:].astype(float))
        q.to_csv(f"{d}/q_{name}.csv", index=False)
        inj.to_csv(f"{d}/i_{name}.csv", index=False)
        a = argparse.Namespace(quant=f"{d}/q_{name}.csv", injections=f"{d}/i_{name}.csv", out=d, prefix=name, id_col=None,
                               orient="auto", meta_cols=None, group_col=None, min_qc_detect=0.8, workers=1, seed=1)
        s = run(a, True)
        if shift:
            r, ho = s["raw"], s["held_out"]
            for ok_, msg in ((s["recommendation"] == "recommend", "effect data: recommendation should be 'recommend'"),
                             (r["frac_batch_affected"] > 0.5, "effect data: most features should show a batch effect before correction"),
                             (ho["frac_batch_affected"] < 0.05, "effect data: held-out batch effect should be gone"),
                             (ho["median_qc_rsd_after"] < 0.6 * r["median_qc_rsd"], "effect data: held-out QC RSD should fall by at least 40%"),
                             (s["n_not_corrected"] >= 2, "effect data: the two undetected features must be flagged as not corrected")):
                if not ok_:
                    bad.append(msg)
            c = pd.read_csv(f"{d}/{name}_corrected.csv")
            if not (c.iloc[0, 3:] == 0).all():
                bad.append("zeros must stay zero")
            xin = pd.read_csv(f"{d}/q_{name}.csv")
            m = xin.iloc[:, 1:].to_numpy() == 0
            if not (c[xin.columns[1:]].to_numpy()[m] == 0).all():
                bad.append("input zeros must stay zero")
        else:
            if s["recommendation"] != "skip":
                bad.append(f"null data: should recommend 'skip', got {s['recommendation']} ({s['recommendation_basis']})")
    print("SELFTEST", "FAILED:\n  " + "\n  ".join(bad) if bad else "PASSED")
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description="QCRSC batch/drift correction with held-out validation (see module docstring).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for n in ("check", "correct"):
        p = sub.add_parser(n)
        p.add_argument("--quant", required=True)
        p.add_argument("--injections", required=True)
        p.add_argument("--out", required=True)
        p.add_argument("--prefix", default="batch_correction")
        p.add_argument("--id-col", default=None)
        p.add_argument("--orient", choices=["auto", "features", "samples"], default="auto")
        p.add_argument("--meta-cols", nargs="*", default=None, help="numeric metadata columns to exclude (samples-in-rows tables)")
        p.add_argument("--group-col", default=None, help="injection-table column for the group-by-batch table (e.g. Site)")
        p.add_argument("--min-qc-detect", type=float, default=MIN_QC_DETECT)
        p.add_argument("--workers", type=int, default=min(4, os.cpu_count() or 1))
        p.add_argument("--seed", type=int, default=20261104)
    sub.add_parser("selftest")
    a = ap.parse_args()
    warnings.filterwarnings("ignore")
    if a.cmd == "selftest":
        sys.exit(selftest())
    run(a, a.cmd == "correct")


if __name__ == "__main__":
    main()
