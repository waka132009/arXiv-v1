#!/usr/bin/env python3
"""
Generate a schematic: fig_equatorial_trigger_schematic.(pdf|png|svg)

- Minimal, monochrome-friendly (default)
- Vector-safe when using PDF/SVG
- No deps beyond matplotlib & numpy

Usage examples:
  python fig_equatorial_trigger_schematic.py --out figures --fmt pdf
  python fig_equatorial_trigger_schematic.py --fmt svg --plasmoids 9 --angle 10
"""

import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Arc
from matplotlib.lines import Line2D
import matplotlib as mpl
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype']  = 42

COL = {
    "sheet": "#1f77b4",     # 青: equatorial return current sheet
    "erg":   "#ff7f0e",     # 橙: ergosurface
    "plas":  "#2ca02c",     # 緑: plasmoid
    "neg":   "#d62728",     # 赤: negative-energy branch
    "gain":  "#9467bd",     # 紫: gain branch (quasi-beam)
    "isco":  "#7f7f7f",     # 灰: ISCO
    "guide": "#bdbdbd"      # 薄灰: equatorial guide
}

def build_figure(n_plasmoids=7, opening_deg=12, with_legend=False, label_bg=False):
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, FancyArrowPatch, Arc
    from matplotlib.lines import Line2D

    FS = 8.5   # 基本フォントサイズ（小さめ）
    C  = "black"

    fig, ax = plt.subplots(figsize=(7.4, 4.4))  # わずかに小型化
    ax.set_aspect("equal")
    ax.set_xlim(-6.3, 6.3)
    ax.set_ylim(-3.5, 3.1)
    ax.axis("off")

    bbox = dict(facecolor="white", alpha=0.65, edgecolor="none", pad=1) if label_bg else None

    # Horizon（薄め）
    horizon = Circle((0, 0), radius=1.3, color=C, fill=True, alpha=0.05, linewidth=1.0)
    ax.add_patch(horizon)
    ax.text(0, 0.35, "BH (horizon)", ha="center", va="top", fontsize=FS, color=C, bbox=bbox)

    # Ergosurface（破線の楕円）
    erg_arc = Arc((0,0), 9.8, 4.8, lw=1.1, linestyle=(0,(6,4)), color=COL["erg"])
    ax.add_patch(erg_arc)
    ax.text(5.0, 2.25, "Ergosurface", ha="right", va="bottom", fontsize=FS, color=C, bbox=bbox)

    # ISCO（浅い弧）
    isco = Arc((0,0), 7.4, 7.4/6, lw=1.1, color=COL["isco"])
    ax.add_patch(isco)
    ax.text(3.9, -0.70, "ISCO (equatorial)", ha="center", va="top", fontsize=FS-0.2, color=C, bbox=bbox)

    # equatorial guide
    ax.plot([-6.1, 6.1], [0, 0], lw=0.7, linestyle=(0,(1,3)), color=COL["guide"], alpha=0.35)

    # return current sheet
    ax.plot([-4.0, 4.0], [0, 0], lw=2.0, solid_capstyle="round", color=COL["sheet"])

    # Resistive ticks
    for x in np.linspace(-3.1, 3.1, 9):
        ax.plot([x, x], [0.052, -0.052], lw=0.9, color=C)

    # Plasmoid chain（数は既定7。混むなら5に）
    xs = np.linspace(-3.0, 3.0, n_plasmoids)
    r0 = 0.16
    for i, px in enumerate(xs):
        circ = circ = Circle((px, 0.0), r0*(1.0 + 0.15*np.cos(i)), fill=False, lw=1.2, edgecolor=COL["plas"])
        ax.add_patch(circ)
    ax.text(xs[0]-0.2, 0.55, "plasmoid chain", ha="left", va="bottom", fontsize=FS-0.2, color=C, bbox=bbox)

    # Gain branch → 右（実線）
    for x0 in [0.55, 1.35, 2.15, 2.95]:
        ax.add_patch(FancyArrowPatch((x0,0.0),(x0+1.02,0.0),
                                     arrowstyle="->", mutation_scale=9, lw=1.2, color=COL["gain"]))
    # Negative-energy branch → 左（破線）
    for x0 in [-0.55, -1.35, -2.15, -2.95]:
        ax.add_patch(FancyArrowPatch((x0,0.0),(x0-1.02,0.0),
                                     arrowstyle="->", mutation_scale=9, lw=1.0, linestyle="--", color=COL["neg"]))
    # ノズルの開き角（短めにして衝突回避）
    L1, L2 = 3.55, 4.70
    slope = np.tan(np.deg2rad(opening_deg/2))
    ax.plot([L1, L2], [ 0.18 + slope*(L2-L1),  0.18], lw=0.9, color=C)
    ax.plot([L1, L2], [-0.18 - slope*(L2-L1), -0.18], lw=0.9, color=C)
    ax.text(5.15, -0.35, "equatorial nozzle", ha="left", va="center", fontsize=FS-0.2, color=C, bbox=bbox)

    # ラベル（高めのyにずらす）
    ax.text(-2.8, 1.12, r"Penrose branch: $E-\Omega_H L<0$ (into BH)",
            ha="left", va="bottom", fontsize=FS, color=C, bbox=bbox)
    ax.text(2.20, 1.32, "Gain branch → quasi-beam", ha="left", va="bottom",
            fontsize=FS, color=C, bbox=bbox)

    # Back-flow（さらに上へ）
    ax.add_patch(FancyArrowPatch((4.35, 0.26), (3.00, 0.86),
                                 connectionstyle="arc3,rad=0.25",
                                 arrowstyle="->", mutation_scale=9, lw=1.0, color=C))
    ax.text(2.95, 0.95, "back-flow / heating (inner disk)", ha="left", va="bottom",
            fontsize=FS-0.2, color=C, bbox=bbox)

    # アクティブゾーン注釈（raw文字列でエスケープ警告回避）
    ax.annotate(r"active zone widens as $a_*\!\to\!1$",
                xy=(0, 0), xytext=(0, -2.0),
                arrowprops=dict(arrowstyle="-|>", lw=0.9, color=C),
                ha="center", va="top", fontsize=FS, color=C, bbox=bbox)

    from matplotlib.lines import Line2D
    # 凡例の線幅を図中の線と揃える
    lw_sheet, lw_erg, lw_isco = 2.2, 1.3, 1.3

    handles = [
        Line2D([], [], lw=lw_sheet, color=COL["sheet"],
               label="equatorial return current sheet"),
        Line2D([], [], lw=lw_erg, linestyle=(0, (6, 4)), color=COL["erg"],
               label="ergosurface (schematic)"),
        Line2D([], [], lw=1.2, color=COL["plas"], marker='o', markersize=5,
               markerfacecolor='none', linestyle='None',
               label="plasmoid (magnetic island)"),
        Line2D([], [], lw=1.0, color=COL["neg"], linestyle='--',
               label="negative-energy branch (into BH)"),
        Line2D([], [], lw=1.2, color=COL["gain"],
               label="gain branch (outward) \u2192 quasi-beam"),  # →（Unicode）
        Line2D([], [], lw=lw_isco, color=COL["isco"],
               label="ISCO (equatorial)"),
    ]
    leg = ax.legend(handles=handles, loc="lower left",
                    bbox_to_anchor=(1.02, 0.05),
                    frameon=False, handlelength=2.6, handletextpad=0.8,
                    borderaxespad=0.0)
    return fig

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="figures", help="output directory")
    p.add_argument("--fmt", default="pdf", choices=["pdf","png","svg"], help="output format")
    p.add_argument("--plasmoids", type=int, default=7, help="number of plasmoids (magnetic islands)")
    p.add_argument("--angle", type=float, default=14.0, help="equatorial nozzle opening (deg, visual)")
    args = p.parse_args()

    out_dir = Path(args.out); out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"fig_equatorial_trigger_schematic.{args.fmt}"

    fig = build_figure(n_plasmoids=args.plasmoids, opening_deg=args.angle)
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    print(out_path.as_posix())

if __name__ == "__main__":
    main()
