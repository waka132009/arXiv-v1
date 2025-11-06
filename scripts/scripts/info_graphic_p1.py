# -*- coding: utf-8 -*-
"""
sspe_p1_conundrum.py  (FULL REPLACEMENT)
Generates Page 1: "The Quasar Conundrum"
- Layout matches P2/P3: top = figure, bottom = text
- TeX-like math via MathText (a_*, L/L_Edd)
- Vector-friendly (pdf.fonttype=42)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import FancyBboxPatch

# ---- Unified style (aligned with P2/P3) ----
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"]  = 42
plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 18,
    "axes.labelsize": 12,
    "legend.fontsize": 10,
    "axes.linewidth": 1.0,
})

BLUE       = "#0369a1"
PANEL_BG   = "#f6f7f9"
PANEL_EDGE = "#d9dee7"
GRID_MJ    = 0.28
GRID_MN    = 0.12

# ---- Panel helper: returns (ax_plot, ax_text) in a rounded plate ----
def _panel(ax_page, box):
    x0, y0, w, h = box
    ax_page.add_patch(FancyBboxPatch(
        (x0, y0), w, h, transform=ax_page.transAxes,
        boxstyle="round,pad=0.012,rounding_size=8",
        facecolor=PANEL_BG, edgecolor=PANEL_EDGE, linewidth=1.0
    ))
    # top figure, bottom text
    ax_plot = ax_page.inset_axes([x0+0.04, y0+0.27, w-0.08, h-0.35])
    ax_text = ax_page.inset_axes([x0+0.04, y0+0.02, w-0.08, h-0.44])
    ax_text.axis("off")
    return ax_plot, ax_text

def make_p1_conundrum(figpath="figures/sspe_infographic_p1_conundrum.pdf"):
    # ---- Page canvas ----
    fig = plt.figure(figsize=(9.0, 5.8))
    ax_page = fig.add_axes([0.03, 0.03, 0.94, 0.94])
    ax_page.axis("off")

    # Headline
    ax_page.text(0.05, 0.95, "The Quasar Conundrum",
                 color=BLUE, fontsize=24, fontweight=800,
                 ha="left", va="top", transform=ax_page.transAxes)

    # Layout boxes
    left_box  = [0.05, 0.14, 0.43, 0.68]
    right_box = [0.52, 0.14, 0.43, 0.68]

    # ---- LEFT: Luminosity problem (figure) ----
    axL_plot, axL_txt = _panel(ax_page, left_box)
    axL_plot.text(0.0, 1.10, "Luminosity problem",
                  color=BLUE, fontsize=16, fontweight=700,
                  ha="left", va="bottom", transform=axL_plot.transAxes)
    axL_plot.text(-0.06, 1.10, "①", color=BLUE, fontsize=14, fontweight=700,
                  ha="right", va="bottom", transform=axL_plot.transAxes)

    axL_plot.set_facecolor("white")
    for sp in axL_plot.spines.values(): sp.set_visible(True)
    axL_plot.set_xscale("log")
    axL_plot.set_xlim(0.9, 20)
    axL_plot.set_ylim(0.3, 3.5)
    axL_plot.grid(True, which="major", alpha=GRID_MJ)
    axL_plot.grid(True, which="minor", alpha=GRID_MN)

    # Curve with explicit super-Eddington peak (>2)
    x = np.logspace(np.log10(0.9), np.log10(20), 200)
    peak = 1.3 * np.exp(-((np.log10(x) - 0.2) / 0.35) ** 2)             # +1.3 at peak
    tail = -0.15 * np.exp(-((np.log10(x) - 1.2) / 0.5) ** 2)            # slight dip later
    y = 1.0 + peak + tail                                               # crosses > 2 clearly

    # Highlight region L/LEdd > 1
    axL_plot.axhspan(1.0, axL_plot.get_ylim()[1], color=BLUE, alpha=0.06, lw=0)
    axL_plot.plot(x, y, lw=2.0, color=BLUE, label=r"$L/L_{\rm Edd}$")
    axL_plot.axhline(1.0, color="black", lw=1.0, ls="--")
    axL_plot.text(0.02, 0.21, r"$L/L_{\rm Edd}=1$", fontsize=9,
                  ha="left", va="bottom", transform=axL_plot.transAxes)
    axL_plot.set_xlabel("Time (arb.)", fontsize=9)
    axL_plot.set_ylabel(r"$L/L_{\rm Edd}$", fontsize=9)
    axL_plot.tick_params(labelsize=8)

    # ---- LEFT text ----
    left_lines = [
        r"$\mathbf{Luminosity:}$ quasars exist with $L/L_{\rm Edd}>1$.",
        r"Super-Eddington phases likely required",
        r"for hyper-luminosity.",
        r"Population tail shows $L/L_{\rm Edd}\gtrsim 2$ (illustrative).",
    ]
    ytxt = 0.70
    for s in left_lines:
        axL_txt.text(0.0, ytxt, s, ha="left", va="top",
                     transform=axL_txt.transAxes, fontsize=11, linespacing=1.12)
        ytxt -= 0.14

    # ---- RIGHT: Spin ceiling problem (figure) ----
    axR_plot, axR_txt = _panel(ax_page, right_box)
    axR_plot.text(0.0, 1.10, "Spin ceiling problem",
                  color=BLUE, fontsize=16, fontweight=700,
                  ha="left", va="bottom", transform=axR_plot.transAxes)
    axR_plot.text(-0.06, 1.10, "②", color=BLUE, fontsize=14, fontweight=700,
                  ha="right", va="bottom", transform=axR_plot.transAxes)

    axR_plot.set_facecolor("white")
    for sp in axR_plot.spines.values(): sp.set_visible(True)
    axR_plot.grid(True, which="major", alpha=GRID_MJ)
    axR_plot.grid(True, which="minor", alpha=GRID_MN)

    t = np.linspace(0, 1, 60)
    a = 0.92 + 0.06 * (1 - np.exp(-6 * t))  # monotonic rise toward ~0.98
    axR_plot.plot(t, a, lw=2.0, color=BLUE, label=r"$a_\ast$")
    axR_plot.axhline(0.9985, color="black", lw=1.0, ls="--")
    axR_plot.text(0.02, 0.85, r"Thorne limit $a_\ast\simeq0.9985$",
                  ha="left", va="bottom", fontsize=9, transform=axR_plot.transAxes,
                  bbox=dict(facecolor="white", edgecolor="none", alpha=0.6, pad=1.0))
    axR_plot.set_xlabel("Time (arb.)", fontsize=9)
    axR_plot.set_ylabel(r"$a_\ast$", fontsize=9)
    axR_plot.set_ylim(0.9, 1.005)
    axR_plot.tick_params(labelsize=8)

    # ---- RIGHT text ----
    right_lines = [
        r"$\mathbf{Spin\ ceiling:}$ sustained accretion",
        r"should push $a_\ast\!\to\!1$, yet observations",
        r"cluster below the Thorne limit $a_\ast\simeq0.9985$.",
        r"Counter-torque or dissipation",
        r"is implied (unspecified here).",
    ]
    ytxt = 0.70
    for s in right_lines:
        axR_txt.text(0.0, ytxt, s, ha="left", va="top",
                     transform=axR_txt.transAxes, fontsize=11, linespacing=1.12)
        ytxt -= 0.14

    # Footer navigation cue
    ax_page.text(0.95, 0.04, "See p.2 for the proposed mechanism →",
                 color="#444", ha="right", va="center", fontsize=10, style="italic",
                 transform=ax_page.transAxes)

    fig.savefig(figpath, bbox_inches="tight", pad_inches=0.35)
    plt.close(fig)

if __name__ == "__main__":
    make_p1_conundrum()
