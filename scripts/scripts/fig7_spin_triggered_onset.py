#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spin-triggered onset figure (PDF)
- x: spin parameter a_*
- y: peak Eddington ratio L_tot / L_Edd
- vertical dashed line: a_th

Usage:
  python scripts/fig_onset.py --ath 0.97 --polished
  # 立ち上がりを鋭く: --n 6
"""
import argparse, os
import numpy as np
import matplotlib.pyplot as plt

def onset_curve(a, a_th=0.97, floor=1.0, amp=12.0, n=4.0, a_right=1.0):
    """
    '静穏→立ち上がり' を x 右端まで滑らかに到達させる版。
    正規化 s = clip((a - a_th)/(a_right - a_th), 0, 1)
    y = floor + amp * s^n
    """
    a = np.asarray(a, dtype=float)
    denom = max(a_right - a_th, 1e-9)
    s = np.clip((a - a_th) / denom, 0.0, 1.0)
    return floor + amp * (s ** n)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ath",   type=float, default=0.97,  help="threshold spin a_th")
    ap.add_argument("--floor", type=float, default=1.0,   help="baseline floor level")
    ap.add_argument("--amp",   type=float, default=12.0,  help="rise amplitude above floor")
    ap.add_argument("--n",     type=float, default=4.0,   help="steepness exponent (3–6 recommended)")
    ap.add_argument("--xmin",  type=float, default=0.90,  help="x-axis min (spin)")
    ap.add_argument("--xmax",  type=float, default=1.00,  help="x-axis max (spin)")
    ap.add_argument("--out",   default="figures/Fig_Onset.pdf", help="output PDF path")
    ap.add_argument("--polished", action="store_true", help="save into figures/polished/")
    ap.add_argument("--title", default="", help="optional title text")
    args = ap.parse_args()

    # grid（右端を含む）
    a = np.linspace(args.xmin, args.xmax, 600, endpoint=True)
    y = onset_curve(a, a_th=args.ath, floor=args.floor, amp=args.amp, n=args.n, a_right=args.xmax)

    # figure
    fig = plt.figure(figsize=(6, 4.0), dpi=300)
    ax = plt.gca()
    ax.plot(a, y, linewidth=2.2)
    ax.axvline(args.ath, linestyle="--", linewidth=1.8, color="C3",
               label=fr"$a_{{\rm th}}={args.ath:.2f}$")
    ax.legend(frameon=False, loc="upper left")

    if args.title:
        ax.set_title(args.title)
    ax.set_xlabel(r"Spin parameter $a_\ast$")
    ax.set_ylabel(r"Peak Eddington ratio $L_{\rm tot}/L_{\rm Edd}$")
    ax.grid(True, which="both", alpha=0.25)
    ax.set_xlim(args.xmin, args.xmax)
    ax.margins(x=0)  # 余計な左右マージンを消す

    # y範囲：床の少し下〜最大値の少し上
    y_min = min(y.min(), args.floor) - 0.05 * max(1.0, args.amp)
    y_max = y.max() + 0.05 * max(1.0, args.amp)
    ax.set_ylim(y_min, y_max)

    # save
    base, name = os.path.split(args.out)
    if args.polished:
        base = os.path.join(base, "polished")
    os.makedirs(base, exist_ok=True)
    out_path = os.path.join(base, name)
    fig.tight_layout()
    fig.savefig(out_path)
    print("[Onset] saved ->", out_path)

if __name__ == "__main__":
    main()
