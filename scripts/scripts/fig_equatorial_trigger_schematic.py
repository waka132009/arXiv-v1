#!/usr/bin/env python3
"""
Generate a schematic: fig_equatorial_trigger_schematic.(pdf|png|svg)

- Minimal, monochrome-friendly
- Vector-safe when using PDF/SVG
- No deps beyond matplotlib & numpy

Usage:
  python fig_equatorial_trigger_schematic.py --out figures --fmt pdf --label-bg
  python fig_equatorial_trigger_schematic.py --fmt svg --plasmoids 9 --angle 10
"""

import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Arc
from matplotlib.lines import Line2D
import matplotlib as mpl

# Embed TrueType fonts (safer for publishers)
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"]  = 42
# Math text / fonts (LaTeX不要で数式OK)
mpl.rcParams.update({
    "mathtext.fontset": "stix",
    "font.family": "STIXGeneral",
    "axes.unicode_minus": False,
})

COL = {
    "sheet": "#1f77b4",     # 青: equatorial return current sheet
    "erg":   "#ff7f0e",     # 橙: ergosurface (schematic)
    "plas":  "#2ca02c",     # 緑: plasmoid
    "neg":   "#2f6db3",     # 青系: negative-energy branch (into BH)
    "pos":   "#d23b3b",     # 赤系: positive-energy branch (outward)
    "isco":  "#7f7f7f",     # 灰: ISCO
    "guide": "#bdbdbd",     # 薄灰: equatorial guide
    "back":  "#000000",     # 黒: back-flow arrow
}

def build_figure(n_plasmoids: int = 7,
                 opening_deg: float = 12,
                 with_legend: bool = True,
                 label_bg: bool = False,
                 sheet_width: float = 6.0,      # 帯の太さ（線幅相当）
                 branch_offset: float = 0.12    # 枝の上下オフセット（y軸）
                 ):
    FS = 9.0
    C  = "black"

    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    ax.set_aspect("equal")
    ax.set_xlim(-6.3, 6.3)
    ax.set_ylim(-3.5, 3.1)
    ax.axis("off")

    bbox = dict(facecolor="white", alpha=0.65, edgecolor="none", pad=1) if label_bg else None

    # --- Horizon（薄め） ---
    horizon = Circle((0, 0), radius=1.3, color=C, fill=True, alpha=0.05, linewidth=1.0)
    ax.add_patch(horizon)
    ax.text(0, 0.35, r"event horizon $r_{\rm H}$",
            ha="center", va="top", fontsize=FS, color=C, bbox=bbox)

    # --- Ergosurface（破線の楕円） ---
    erg_arc = Arc((0, 0), 9.8, 4.8, lw=1.1, linestyle=(0, (6, 4)), color=COL["erg"])
    ax.add_patch(erg_arc)
    ax.text(5.0, 2.25, "ergosurface",
        ha="right", va="bottom", fontsize=FS, color=C, bbox=bbox)

    # --- ISCO（浅い弧） ---
    isco = Arc((0, 0), 7.4, 7.4/6, lw=1.1, color=COL["isco"])
    ax.add_patch(isco)
    ax.text(3.9, -0.70, r"$r_{\rm ISCO}$ (equatorial)",
            ha="center", va="top", fontsize=FS-0.2, color=C, bbox=bbox)

    # --- equatorial guide（薄い点線の基準）---
    ax.plot([-6.1, 6.1], [0, 0], lw=0.7, linestyle=(0, (1, 3)),
            color=COL["guide"], alpha=0.35)

    # --- return current sheet を“帯”として描画（下地。zorderを低く） ---
    ax.plot([-4.0, 4.0], [0, 0],
            lw=sheet_width, solid_capstyle="round",
            color=COL["sheet"], alpha=0.18, zorder=0)  # 半透明の帯
    # 外縁を細線で縁取り（視認性アップ）
    ax.plot([-4.0, 4.0], [0, 0], lw=2.0, color=COL["sheet"], zorder=1)

    # --- Resistive ticks ---
    for x in np.linspace(-3.1, 3.1, 9):
        ax.plot([x, x], [0.052, -0.052], lw=0.9, color=C, zorder=2)

    # --- Plasmoid chain ---
    xs = np.linspace(-3.0, 3.0, n_plasmoids)
    r0 = 0.16
    for i, px in enumerate(xs):
        circ = Circle((px, 0.0), r0 * (1.0 + 0.15 * np.cos(i)),
                      fill=False, lw=1.2, edgecolor=COL["plas"], zorder=2)
        ax.add_patch(circ)
    ax.text(xs[0] - 0.2, 0.55, "plasmoids / intermittent ejections",
            ha="left", va="bottom", fontsize=FS-0.2, color=C, bbox=bbox)

    # --- Positive/negative branches：帯の上下へ±オフセットして並走 ---
    y_pos = +branch_offset
    y_neg = -branch_offset

    # positive-energy branch → 右（実線・赤）
    pos_starts = [0.55, 1.35, 2.15, 2.95]
    for x0 in pos_starts:
        ax.add_patch(FancyArrowPatch((x0, y_pos), (x0 + 1.02, y_pos),
                                     arrowstyle="->", mutation_scale=9,
                                     lw=1.6, color=COL["pos"], zorder=4))
    # negative-energy branch → 左（破線・青）
    for x0 in [-0.55, -1.35, -2.15, -2.95]:
        ax.add_patch(FancyArrowPatch((x0, y_neg), (x0 - 1.02, y_neg),
                                     arrowstyle="->", mutation_scale=9,
                                     lw=1.8, linestyle=(0, (6, 3)),
                                     color=COL["neg"], zorder=4))

    # --- ノズルの開き角 ---
    L1, L2 = 3.55, 4.70
    slope = np.tan(np.deg2rad(opening_deg / 2.0))
    ax.plot([L1, L2], [0.18 + slope * (L2 - L1), 0.18], lw=0.9, color=C, zorder=3)
    ax.plot([L1, L2], [-0.18 - slope * (L2 - L1), -0.18], lw=0.9, color=C, zorder=3)
    ax.text(5.15, -0.35, "equatorial venting spread (schematic)",
            ha="left", va="center", fontsize=FS-0.2, color=C, bbox=bbox)

    # --- ラベル（“点指し”で結ぶ／重なり回避） ---
    ax.annotate(r"negative-energy branch: $E-\Omega_H L<0$ (to BH)",
                xy=(-1.35 - 0.9, y_neg), xycoords='data',
                xytext=(-3.25, 1.05), textcoords='data',
                arrowprops=dict(arrowstyle='->', lw=0.9, color=COL["neg"],
                                connectionstyle="arc3,rad=-0.15"),
                fontsize=FS, color=COL["neg"], bbox=bbox)

    ax.annotate(r'positive-energy branch $\rightarrow$ equatorially concentrated outflow (candidate quasi-beam)',
                xy=(2.95 + 0.9, y_pos), xycoords='data',
                xytext=(3.55, 1.30), textcoords='data',
                arrowprops=dict(arrowstyle='->', lw=0.9, color=COL["pos"],
                                connectionstyle="arc3,rad=0.18"),
                fontsize=FS, color=COL["pos"], bbox=bbox)

    # --- back-flow/heating（曲線矢印：凡例には入れない）---
    ax.annotate('back-flow / heating (inner disk)',
                xy=(4.35, 0.26), xytext=(3.05, 0.72),
                arrowprops=dict(arrowstyle='->',
                                connectionstyle="arc3,rad=0.25",
                                lw=1.0, color=COL["back"]),
                fontsize=FS-0.2, color=COL["back"], bbox=bbox)

    # --- Legend（プロキシで必要項目だけ） ---
    if with_legend:
        handles = [
            Line2D([0], [0], lw=sheet_width, color=COL["sheet"], alpha=0.18,
                   label="equatorial current layer (schematic)"),  # 帯の見た目に合わせる
#            Line2D([0], [0], lw=2.0, color=COL["sheet"], label="_nolegend_"),  # 枠線は凡例に出さない
            Line2D([0], [0], lw=1.2, color=COL["erg"], ls=(0, (6, 4)),
                   label="ergosurface (schematic)"),
            Line2D([0], [0], lw=1.2, color=COL["isco"],
                   label="ISCO (equatorial)"),
            Line2D([0], [0], marker='o', mfc='none', mec=COL["plas"], lw=0,
                   label="plasmoid (magnetic island)"),
            Line2D([0], [0], lw=1.6, color=COL["pos"], ls='-',
                   label="positive-energy branch (outward)"),
            Line2D([0], [0], lw=1.8, color=COL["neg"], ls=(0, (6, 3)),
                   label="negative-energy branch (into BH)"),
        ]
        ax.legend(handles=handles,
                  loc="lower left", bbox_to_anchor=(1.02, 0.05),
                  frameon=False, handlelength=2.6, handletextpad=0.8,
                  borderaxespad=0.0, fontsize=FS)

    return fig

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="figures", help="output directory")
    p.add_argument("--fmt", default="pdf", choices=["pdf", "png", "svg"], help="output format")
    p.add_argument("--plasmoids", type=int, default=7, help="number of plasmoids (magnetic islands)")
    p.add_argument("--angle", type=float, default=14.0, help="equatorial nozzle opening (deg, visual)")
    p.add_argument("--no-legend", action="store_true", help="hide legend")
    p.add_argument("--label-bg", action="store_true", help="enable white background under labels")
    p.add_argument("--sheet-width", type=float, default=6.0, help="thickness of return current sheet (lw)")
    p.add_argument("--branch-offset", type=float, default=0.12, help="vertical offset of branches")
    args = p.parse_args()

    out_dir = Path(args.out); out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"fig_equatorial_trigger_schematic.{args.fmt}"

    fig = build_figure(n_plasmoids=args.plasmoids,
                       opening_deg=args.angle,
                       with_legend=not args.no_legend,
                       label_bg=args.label_bg,
                       sheet_width=args.sheet_width,
                       branch_offset=args.branch_offset)
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    print(out_path.as_posix())

if __name__ == "__main__":
    main()
