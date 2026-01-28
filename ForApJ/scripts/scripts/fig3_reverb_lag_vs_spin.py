#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig3:
  - Fig3a: da/dt vs a (phase portrait) for multiple epsilon_coup values
  - Fig3b: a_eq vs epsilon_coup with plausible band

Usage:
  python scripts/fig3.py --polished
  python scripts/fig3.py --params data/fig3_params.csv --polished
"""

import argparse
import os
import csv
import numpy as np
import matplotlib.pyplot as plt


# ===================== Physics placeholder (差し替えポイント) =====================
def torque_balance(a, eps):
    """
    Returns da/dt (arb. units). Positive -> spin-up, Negative -> spin-down.
    Replace with the actual model:
      da/dt = [accretion spin-up term(a)] - [extraction term(a, eps)]
    Toy behavior: spin-up weakens near a~1, extraction grows with eps and a.
    """
    return (1.0 - a) ** 1.5 * (1.0 - 0.1 * eps) - eps * a ** 2


def find_equilibrium_spin(eps, grid=None):
    if grid is None:
        grid = np.linspace(0.85, 0.9995, 2000)
    y = torque_balance(grid, eps)
    s = np.sign(y)
    z = np.where(np.diff(s) != 0)[0]
    if len(z) == 0:
        # fallback: choose min |da/dt|
        return float(grid[np.argmin(np.abs(y))])
    i = z[0]
    # linear interpolation for zero crossing
    x1, x2, y1, y2 = grid[i], grid[i + 1], y[i], y[i + 1]
    return float(x1 - y1 * (x2 - x1) / (y2 - y1))


# ============================== IO helpers ====================================
def load_eps_list(path):
    """
    Load epsilon_coup list from CSV with header 'epsilon_coup'.
    Falls back to defaults if file missing or empty.
    """
    defaults = [0.005, 0.01, 0.02, 0.05, 0.10]
    try:
        vals = []
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames or "epsilon_coup" not in reader.fieldnames:
                return defaults
            for r in reader:
                s = (r.get("epsilon_coup") or "").strip()
                if s:
                    vals.append(float(s))
        return sorted(vals) if vals else defaults
    except FileNotFoundError:
        return defaults


def ensure_out(path, polished=False):
    """
    Ensure output directory exists; if polished, save under figures/polished/.
    Returns the full output path.
    """
    base, name = os.path.split(path)
    if polished:
        base = os.path.join(base, "polished")
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, name)


# ================================== Main ======================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", default="data/fig3_params.csv",
                    help="CSV with column 'epsilon_coup' (optional)")
    ap.add_argument("--outa", default="figures/Fig3a.pdf",
                    help="output path for Fig3a")
    ap.add_argument("--outb", default="figures/Fig3b.pdf",
                    help="output path for Fig3b")
    ap.add_argument("--polished", action="store_true",
                    help="save into figures/polished/")
    args = ap.parse_args()

    # Data
    eps_list = load_eps_list(args.params)
    a_grid = np.linspace(0.85, 0.9995, 600)

    # ----------------------------- Fig3a: da/dt vs a ---------------------------
    fig = plt.figure(figsize=(6, 4.2), dpi=300)
    ax = plt.gca()

    # モノクロ印刷でも識別できるよう、線種/マーカーで差別化（色は指定しない）
    linestyles = ["-", "--", "-.", ":", (0, (3, 1, 1, 1))]  # 5種ローテーション
    markers = ["", "o", "s", "D", "^"]

    for i, eps in enumerate(eps_list):
        y = torque_balance(a_grid, eps)
        ls = linestyles[i % len(linestyles)]
        mk = markers[i % len(markers)]
        ax.plot(
            a_grid,
            y,
            linestyle=ls,
            marker=mk,
            markevery=50,
            linewidth=1.8,
            label=f"{eps:g}",
        )

    # --- Fig3a 曲線を描いた直後あたりに追加 ---
    ymin, ymax = ax.get_ylim()
    if ymax < 0.0:
        ax.set_ylim(ymin, 0.0)  # 上端を 0 に引き上げる（= y=0 を必ず見える範囲に）

    # y=0（トルク収支線）を前面に
    ax.axhline(0.0, linewidth=1.0, zorder=2)

    # “白抜きボックス”の注記（x軸上）も前面＆クリップ無効
    ax.text(
        0.06, 0.0, r"$\dot a=0$",
        transform=ax.get_yaxis_transform(),   # x: axes fraction, y: data(=0)
        ha="left", va="bottom", fontsize=8, zorder=3, clip_on=False,
        bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9),
    )

    # 軸ラベル（数式を図に焼き込み）
    ax.set_xlabel(r"spin parameter $a$")
    ax.set_ylabel(r"$\mathrm{d}a/\mathrm{d}t$  (arb. units)")

    ax.grid(True, which="both", alpha=0.25)

    # 凡例：左下＋少し上げる（重なり回避）— ご指定の (0.03, 0.09)
    leg = ax.legend(
        title=r"$\epsilon_{\mathrm{coup}}$",
        frameon=False,
        loc="lower left",
        bbox_to_anchor=(0.03, 0.09),  # ← ここはお好みで微調整可
        fontsize=10,
        title_fontsize=10,
        handlelength=2.8,
        handletextpad=0.8,
    )
    try:
        leg._legend_box.align = "left"  # 古いmatplotlibでは無視される
    except Exception:
        pass

    out_a = ensure_out(args.outa, args.polished)
    fig.tight_layout(pad=0.6)
    fig.savefig(out_a)
    print("[Fig3a] saved ->", out_a)

    # ---------------------- Fig3b: a_eq vs epsilon_coup ------------------------
    fig = plt.figure(figsize=(6, 4.2), dpi=300)
    ax = plt.gca()

    eps_dense = np.logspace(-3, -0.5, 120)
    a_eq = [find_equilibrium_spin(e) for e in eps_dense]

    # 縦帯（妥当範囲）を凡例に出すため label を付与
    ax.axvspan(
        0.01, 0.10, alpha=0.12,
        label=r"$\epsilon_{\mathrm{coup}}\approx0.01\text{--}0.10$"
    )
    ax.semilogx(eps_dense, a_eq, linewidth=2.0)

    ax.set_xlabel(r"$\epsilon_{\mathrm{coup}}$")
    ax.set_ylabel(r"equilibrium spin $a_{\mathrm{eq}}$")
    ax.set_ylim(0.85, 1.0)
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False, loc="lower left", fontsize=10)

    out_b = ensure_out(args.outb, args.polished)
    fig.tight_layout(pad=0.6)
    fig.savefig(out_b)
    print("[Fig3b] saved ->", out_b)


if __name__ == "__main__":
    main()
