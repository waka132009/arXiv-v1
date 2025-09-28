# scripts/common.py — shared plotting style & helpers
from __future__ import annotations
import matplotlib as mpl
import matplotlib.pyplot as plt
from pathlib import Path

# Use mathtext (no external TeX requirement). 
# If you prefer full LaTeX, set text.usetex=True and add a preamble.
mpl.rcParams.update({
    "text.usetex": False,
    "mathtext.fontset": "stix",
    "mathtext.rm": "STIXGeneral",
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "legend.fontsize": 9,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "savefig.bbox": "tight",
})

def newfig(figsize=(4.7, 3.1)):
    fig, ax = plt.subplots(figsize=figsize)
    return fig, ax

def savefig(fig, outpath: str | Path, dpi_png=300):
    out = Path(outpath); out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out.with_suffix(".pdf"))
    fig.savefig(out.with_suffix(".png"), dpi=dpi_png)
