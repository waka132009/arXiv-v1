# -*- coding: utf-8 -*-
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib.patheffects as pe

# -----------------------------
# constants (cgs)
# -----------------------------
c = 2.99792458e10
G = 6.67430e-8
sigma_T = 6.6524587321e-25
m_e = 9.10938356e-28
M_sun = 1.98847e33
Ledd_per_Msun = 1.26e38  # erg/s

# -----------------------------
# model parameters
# -----------------------------
ELL_CRIT = 30.0
LEVELS = np.linspace(1, 10, 10)

MBH = 1.0e9 * M_sun
ETA_ACC = 0.1
TAU_YR = 1.0e7                 # extraction e-folding timescale
LACC_OVER_LEDD = 1.0           # illustrative concurrent accretion level

LABEL_STYLE = "outline"
LABEL_POS = 0.55
GUIDE_LW = 1.6

# -----------------------------
# helper functions
# -----------------------------
def rg_cm(M: float) -> float:
    return G * M / c**2

def ledd(M: float) -> float:
    return Ledd_per_Msun * (M / M_sun)

def erot_fraction(a: float) -> float:
    # Eq. (1): E_rot / (M c^2)
    return 1.0 - np.sqrt(0.5 * (1.0 + np.sqrt(1.0 - a**2)))

def mean_extraction_power(M: float, a: float, tau_yr: float) -> float:
    tau_s = tau_yr * 365.25 * 24.0 * 3600.0
    Erot = erot_fraction(a) * M * c**2
    return Erot / tau_s

def active_extraction_power(M: float, a: float, tau_yr: float, d: np.ndarray) -> np.ndarray:
    return mean_extraction_power(M, a, tau_yr) / np.maximum(d, 1e-6)

def lself(eps: np.ndarray, Pext_act: np.ndarray) -> np.ndarray:
    # Eq. (4): L_self = eps_coup * P_ext
    return eps * Pext_act

def compactness(Lself: np.ndarray, Reff_rg: float, M: float) -> np.ndarray:
    Reff_cm = Reff_rg * rg_cm(M)
    return Lself * sigma_T / (4.0 * np.pi * Reff_cm * m_e * c**3)

def ltot_over_ledd(Lself: np.ndarray, M: float, lacc_over_ledd: float = 1.0) -> np.ndarray:
    Lacc = lacc_over_ledd * ledd(M)
    return (Lacc + Lself) / ledd(M)

def _place_contour_label(ax, cs):
    # cs: contour set for ell=30
    if not cs.allsegs[0]:
        return
    seg = max(cs.allsegs[0], key=lambda arr: arr.shape[0])
    i = int(np.clip(LABEL_POS, 0.0, 1.0) * (len(seg) - 1))
    x, y = seg[i]
    txt = ax.text(x, y, r"$\ell = 30$", ha="left", va="bottom")
    if LABEL_STYLE == "outline":
        txt.set_path_effects([pe.withStroke(linewidth=3, foreground="white")])

def make_panel(Reff_rg: float, outstem: Path, a_star: float = 0.99) -> None:
    eps = np.linspace(0.01, 0.30, 241)
    d = np.linspace(0.01, 0.30, 241)
    E, D = np.meshgrid(eps, d)

    Pext_act = active_extraction_power(MBH, a_star, TAU_YR, D)
    Lself = lself(E, Pext_act)
    ell = compactness(Lself, Reff_rg, MBH)
    Z = np.clip(ltot_over_ledd(Lself, MBH, LACC_OVER_LEDD), LEVELS.min(), LEVELS.max())

    fig = plt.figure(figsize=(5.4, 4.6), constrained_layout=True)
    ax = fig.add_subplot(111)

    cf = ax.contourf(E, D, Z, levels=LEVELS)
    cbar = fig.colorbar(cf, ax=ax, ticks=LEVELS[::2])
    cbar.set_label(r"Peak Eddington ratio $L_{\rm tot}/L_{\rm Edd}$")

    # ell=30 contour from the model
    cs = ax.contour(E, D, ell, levels=[ELL_CRIT], colors="black", linewidths=GUIDE_LW)
    _place_contour_label(ax, cs)

    ax.set_xlabel(r"Coupling efficiency $\epsilon_{\rm coup}$")
    ax.set_ylabel(r"Duty cycle $d$")
    ax.set_xlim(0.01, 0.30)
    ax.set_ylim(0.01, 0.30)
    ax.grid(True, alpha=0.30, linestyle="--")

    # visually indicate regions
    # ell < ell_crit : observational transparency window
    ax.contourf(
        E, D, ell,
        levels=[0.0, ELL_CRIT],
        colors=["white"],
        alpha=0.08,
    )

    # 透明窓側にハッチを追加
    ax.contourf(
        E, D, ell,
        levels=[0.0, ELL_CRIT],
        colors="none",
        hatches=["/"],
        alpha=0.0,
    )

    # ell > ell_crit : pair-thick / screened out
    ax.contourf(
        E, D, ell,
        levels=[ELL_CRIT, np.nanmax(ell) + 1.0],
        colors=["black"],
        alpha=0.06,
    )
    # region labels (place by hand; may need tuning)
    txt1 = ax.text(
        0.025, 0.285,
        r"$\ell < \ell_{\rm crit}$" "\n" r"(restricted low-$\ell$ window)",
        ha="left", va="top", fontsize=9, color="black",
    )
    txt1.set_path_effects([pe.withStroke(linewidth=3, foreground="white")])
    txt2 = ax.text(
        0.29, 0.02,
        r"pair-thick / excluded from Tier-1",
        ha="right", va="bottom", fontsize=9, color="0.35",
    )
    txt2.set_path_effects([pe.withStroke(linewidth=2.5, foreground="white")])
    outstem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outstem.with_suffix(".pdf"))
    plt.close(fig)

def main() -> None:
    root = Path(__file__).resolve().parent
    out = root / "figures"
    make_panel(100, out / "fig10a_Reff100")
    make_panel(1000, out / "fig10b_Reff1000")

if __name__ == "__main__":
    plt.rcParams.update(
        {
            "text.usetex": False,
            "mathtext.fontset": "stix",
            "mathtext.rm": "STIXGeneral",
            "font.size": 11,
            "axes.titlesize": 12,
            "axes.labelsize": 11,
            "legend.fontsize": 9,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "axes.linewidth": 0.8,
            "grid.alpha": 0.25,
            "grid.linestyle": "--",
            "savefig.bbox": "tight",
        }
    )
    main()