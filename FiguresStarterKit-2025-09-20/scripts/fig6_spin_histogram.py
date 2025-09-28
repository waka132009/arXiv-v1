#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig6: Candidate gallery table (readable, grayscale-friendly)
Reads: data/fig6_gallery.csv
Writes: figures/Fig6.pdf (or figures/polished/Fig6.pdf with --polished)

CSV expected columns (order flexible; missing columns are skipped):
 name, z, MBH_Msun, a_eq, L_over_LEdd, FeKa_lag, MeV_excess, Polarization, Notes

- Booleans: FeKa_lag / MeV_excess / Polarization accept 1/0, true/false, yes/no
- Numbers are auto-formatted (MBH in scientific notation by default)
"""

import argparse, os, csv, math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.table import Table

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
        headers = [h.strip() for h in rdr.fieldnames or []]
        for r in rdr:
            rows.append({k.strip(): (v.strip() if isinstance(v,str) else v) for k,v in r.items()})
    return rows

def as_float(x):
    try:
        return float(x)
    except Exception:
        return math.nan

def fmt_mbh(x):
    """Format MBH in scientific notation (Msun)."""
    v = as_float(x)
    if math.isnan(v) or v <= 0: return ""
    # show in 10^x Msun (e.g., 6.6e10)
    m, e = f"{v:.2e}".split("e")
    e = int(e)
    m = m.rstrip("0").rstrip(".")
    return f"{m}e{e}"

def fmt_num(x, digits=2):
    v = as_float(x)
    if math.isnan(v): return ""
    return f"{v:.{digits}f}".rstrip("0").rstrip(".")

def as_check(x):
    s = (str(x or "")).strip().lower()
    if s in ("1","true","t","yes","y","✓","check","ok"): return "✓"
    if s in ("0","false","f","no","n","×","x"): return ""
    return s  # leave as-is (e.g., uncertain/limits)

def wrap(text, width):
    s = str(text or "")
    if len(s) <= width: return s
    # simple wrap by spaces
    parts, line, out = s.split(), "", []
    for w in parts:
        if len(line)+len(w)+1 <= width:
            line = (line+" "+w).strip()
        else:
            out.append(line); line = w
    if line: out.append(line)
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="data/fig6_gallery.csv")
    ap.add_argument("--out", default="figures/Fig6.pdf")
    ap.add_argument("--polished", action="store_true")
    args = ap.parse_args()

    rows = load_rows(args.csv)

    # Column order & labels
    preferred = [
        ("name", "Name"),
        ("z", "z"),
        ("MBH_Msun", r"$M_{\rm BH}\ (M_\odot)$"),
        ("a_eq", r"$a_{\rm eq}$"),
        ("L_over_LEdd", r"$L/L_{\rm Edd}$"),
        ("FeKa_lag", r"Fe K$\alpha$ lag"),
        ("MeV_excess", "MeV/hard-X excess"),
        ("Polarization", "Polarization"),
        ("Notes", "Notes"),
    ]
    # Keep only present columns, in preferred order
    present_keys = [k for k,_ in preferred if any(k in r for r in rows)] if rows else [k for k,_ in preferred]
    cols = [(k, lab) for k,lab in preferred if k in present_keys]

    # Build table data
    data = []
    for r in rows:
        row = []
        for k,lab in cols:
            val = r.get(k, "")
            if k == "MBH_Msun":
                row.append(fmt_mbh(val))
            elif k in ("a_eq", "L_over_LEdd"):
                row.append(fmt_num(val, 3))
            elif k in ("FeKa_lag","MeV_excess","Polarization"):
                row.append(as_check(val))
            elif k == "name":
                row.append(wrap(val, 20))
            elif k == "Notes":
                row.append(wrap(val, 28))
            else:
                row.append(str(val))
        data.append(row)

    # Figure size: scale with number of rows
    nrows = max(1, len(data))
    ncols = len(cols)
    row_h = 0.36  # inches per row
    col_w = 1.3   # inches per column (avg)
    # widen Notes column
    notes_idx = next((i for i,(k,_) in enumerate(cols) if k=="Notes"), None)
    fig_w = max(6.0, ncols*col_w + (0.3 if notes_idx is None else 1.1))
    fig_h = min(10.0, 0.8 + nrows*row_h)

    fig = plt.figure(figsize=(fig_w, fig_h), dpi=300)
    ax = plt.gca()
    ax.set_axis_off()

    # Create the table
    table = Table(ax, bbox=[0, 0, 1, 1])

    # Column widths: make Notes wider
    widths = [1.1]*ncols
    if notes_idx is not None:
        widths[notes_idx] = 1.8
    total_w = sum(widths)
    norm_w = [w/total_w for w in widths]

    # Header
    header_height = 0.07
    y = 1.0
    x = 0.0
    for j,(k,label) in enumerate(cols):
        w = norm_w[j]
        cell = table.add_cell(-1, j, w, header_height, text=label, loc="center")
        cell.PAD = 0.02
        cell.set_edgecolor("0.2")
        cell.set_linewidth(0.8)
        cell.set_text_props(fontsize=9, fontweight="bold")
        x += w

    # Body
    cell_h = (1.0 - header_height) / max(nrows,1)
    for i in range(nrows):
        for j in range(ncols):
            txt = data[i][j] if i < len(data) else ""
            w = norm_w[j]
            cell = table.add_cell(i, j, w, cell_h, text=txt, loc="center")
            cell.PAD = 0.02
            cell.set_edgecolor("0.85")
            cell.set_linewidth(0.6)
            cell.set_text_props(fontsize=8)
            # Left-align certain columns
            if cols[j][0] in ("name","Notes"):
                cell._text.set_ha("left")

    ax.add_table(table)

    out = ensure_out(args.out, args.polished)
    fig.tight_layout(pad=0.4)
    fig.savefig(out)
    print("[Fig6] saved ->", out)

if __name__ == "__main__":
    main()
