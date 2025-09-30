#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig5: Observational hooks vs equilibrium spin
  - Fig5a: Fe Kα reverberation lag normalized by r_g/c vs a_eq
  - Fig5b: Hard X-ray (or MeV) excess fraction OR polarization vs a_eq

CSV: data/fig5_candidates.csv  （列は下のテンプレ参照。存在する列だけ自動で使います）
Usage:
  python scripts/fig5.py --polished
"""

import argparse, os, csv, math
import numpy as np
import matplotlib.pyplot as plt

RG_OVER_C_S = 4.925490947e-6  # seconds-per-solar-mass (G M_sun / c^3)

def ensure_out(path, polished=False):
    base, name = os.path.split(path)
    if polished:
        base = os.path.join(base, "polished")
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, name)

def load_rows(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            rows.append({k.strip(): v.strip() for k, v in r.items()})
    return rows

def to_float(x):
    try:
        return float(x)
    except Exception:
        return np.nan

def pick_first(*vals):
    """Return first non-empty string; else ''."""
    for v in vals:
        if v is None: 
            continue
        s = str(v).strip()
        if s != "":
            return s
    return ""

def lag_to_tau_rg(r):
    """
    Convert various lag fields to tau in units of (r_g/c).
    Prefer 'lag_rg'. Else use seconds (lag_ms/lag_s/lag_ks) with MBH.
    """
    lag_rg = to_float(r.get("lag_rg"))
    if not math.isnan(lag_rg):
        return lag_rg

    # seconds from any provided time column
    t_s = np.nan
    for key, scale in [("lag_s", 1.0), ("lag_ms", 1e-3), ("lag_ks", 1e3)]:
        val = to_float(r.get(key))
        if not math.isnan(val):
            t_s = val * scale
            break
    MBH = to_float(r.get("MBH_Msun"))
    if not math.isnan(t_s) and not math.isnan(MBH) and MBH > 0:
        # tau_rg = t / (GM/c^3) = t / (RG_OVER_C_S * MBH)
        return t_s / (RG_OVER_C_S * MBH)
    return np.nan

def y2_value(r):
    """
    Pick Y for Fig5b in優先順位:
      1) hard_x_frac (0..1 or %)
      2) pol_pct (%)
    戻り値は(値, ラベル文字列)
    """
    hard = r.get("hard_x_frac", "")
    pol = r.get("pol_pct", "")
    v = np.nan
    label = ""
    if hard != "":
        vv = to_float(hard)
        if not math.isnan(vv):
            # 0..1 を想定。>1 なら%と解釈して 0..1 に直す。
            v = vv/100.0 if vv > 1.5 else vv
            label = "hard X/MeV excess (fraction)"
            return v, label
    if pol != "":
        vv = to_float(pol)
        if not math.isnan(vv):
            v = vv / 100.0  # %→fraction
            label = "polarization (fraction)"
            return v, label
    return np.nan, label

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="data/fig5_candidates.csv",
                    help="input CSV of candidates/measurements")
    ap.add_argument("--outa", default="figures/Fig5a.pdf")
    ap.add_argument("--outb", default="figures/Fig5b.pdf")
    ap.add_argument("--polished", action="store_true")
    args = ap.parse_args()

    rows = load_rows(args.csv)

    # ------------ Collect series ------------
    names, aeqs, tau_rg, y2, y2label = [], [], [], [], ""
    xerr, yerr = [], []
    for r in rows:
        name = pick_first(r.get("name"), r.get("id"), r.get("source"), r.get("object"))
        aeq = to_float(r.get("a_eq"))
        aeq_lo, aeq_hi = to_float(r.get("a_eq_lo")), to_float(r.get("a_eq_hi"))
        tau = lag_to_tau_rg(r)
        tau_lo, tau_hi = to_float(r.get("lag_rg_lo")), to_float(r.get("lag_rg_hi"))

        yy, lbl = y2_value(r)
        if lbl and not y2label:
            y2label = lbl

        if not math.isnan(aeq) and not math.isnan(tau):
            names.append(name or "")
            aeqs.append(aeq)
            tau_rg.append(tau)
            # 対称誤差に落とす
            if not math.isnan(aeq_lo) and not math.isnan(aeq_hi):
                xerr.append([[aeq - aeq_lo], [aeq_hi - aeq]])
            else:
                xerr.append(None)
            if not math.isnan(tau_lo) and not math.isnan(tau_hi):
                yerr.append([[tau - tau_lo], [tau_hi - tau]])
            else:
                yerr.append(None)

        # y2（Fig5b）
    names2, aeqs2, y2s = [], [], []
    for r in rows:
        aeq = to_float(r.get("a_eq"))
        yy, _ = y2_value(r)
        if not math.isnan(aeq) and not math.isnan(yy):
            names2.append(pick_first(r.get("name"), r.get("id"), r.get("source"), r.get("object")))
            aeqs2.append(aeq)
            y2s.append(yy)

    # ------------ Fig5a ------------
    fig = plt.figure(figsize=(6, 4.2), dpi=300); ax = plt.gca()
    if aeqs:
        # 誤差があればerrorbar、無ければscatter
        for i, (x, y) in enumerate(zip(aeqs, tau_rg)):
            xe = xerr[i]; ye = yerr[i]
            if xe is not None or ye is not None:
                ax.errorbar(x, y,
                            xerr=xe if xe is not None else None,
                            yerr=ye if ye is not None else None,
                            fmt="o", capsize=2, linewidth=1.0)
            else:
                ax.plot(x, y, marker="o", linestyle="")

        # 名前ラベル（重なり最小のオフセット）
        for x, y, n in zip(aeqs, tau_rg, names):
            ax.annotate(n, (x, y), textcoords="offset points", xytext=(6, 4), fontsize=7)
    else:
        # デモ点（CSVが空でも図が出るように）
        ax.plot([0.9, 0.95], [30, 10], marker="o", linestyle="")

    ax.set_xlabel(r"equilibrium spin $a_{\rm eq}$")
    ax.set_ylabel(r"Fe K$\alpha$ lag $\tau_{\rm FeK\alpha}$ ($r_g/c$)")
    ax.grid(True, which="both", alpha=0.25)
    ax.set_xlim(0.85, 1.0)

    out_a = ensure_out(args.outa, args.polished)
    fig.tight_layout(); fig.savefig(out_a)
    print("[Fig5a] saved ->", out_a)

    # ------------ Fig5b ------------
    fig = plt.figure(figsize=(6, 4.2), dpi=300); ax = plt.gca()
    if aeqs2:
        ax.plot(aeqs2, y2s, linestyle="--", linewidth=1.2)  # 傾向線（色は指定しない）
        ax.plot(aeqs2, y2s, marker="D", linestyle="")
        for x, y, n in zip(aeqs2, y2s, names2):
            ax.annotate(n, (x, y), textcoords="offset points", xytext=(6, 4), fontsize=7)
    else:
        ax.plot([0.9, 0.96], [0.15, 0.30], linestyle="--", linewidth=1.2)
        ax.plot([0.9, 0.96], [0.15, 0.30], marker="D", linestyle="")

    ax.set_xlabel(r"equilibrium spin $a_{\rm eq}$")
    ax.set_ylabel(y2label if y2label else "observable (fraction)")
    ax.grid(True, which="both", alpha=0.25)
    ax.set_xlim(0.85, 1.0)
    if "hard X" in (y2label or "").lower():
        ax.axhline(0.0, linewidth=0.8)

    out_b = ensure_out(args.outb, args.polished)
    fig.tight_layout(); fig.savefig(out_b)
    print("[Fig5b] saved ->", out_b)

if __name__ == "__main__":
    main()
