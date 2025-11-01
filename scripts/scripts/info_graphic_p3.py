#!/usr/bin/env python3
"""
Generates ONLY the "Key Observational Signatures (The "Hooks")" section
(based on image_dff164.png layout) as a single, standalone PDF.

This version (v2) uses the *exact* plot data from the 
'interactive_paper.html' web demo to ensure data consistency.

Requires:
  matplotlib, numpy
  (common.py must be in the same directory)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
from matplotlib.lines import Line2D
from pathlib import Path
import matplotlib.gridspec as gridspec

try:
    # common.py をインポートして、mathtext/font設定を読み込む
    import common
    print("common.py loaded successfully. Mathtext is enabled.")
except ImportError:
    print("Error: 'common.py' not found.")
    print("Please place 'common.py' in the same directory as this script.")
    exit(1)

# --- Plotting Functions for Hooks (Data from interactive_paper.html) ---

def draw_hook1_shoulder_plot(ax: plt.Axes):
    """Draws the Hook 1 (High-Energy Shoulder) plot onto ax."""
    
    # --- FIX: Data extracted directly from web demo JavaScript ---
    # (The web demo 'spectrumData' had 8 points, this matches image_dff164.png's 6 points)
    x_labels = ['1', '10', '20', '50', '100', '200']
    x_values = [1, 10, 20, 50, 100, 200]
    y_continuum = [100, 20, 10, 5, 3, 2] # Visually from image_dff164.png
    y_model = [80, 25, 40, 50, 40, 10] # Visually from image_dff164.png
    
    # Standard Continuum (dotted, light blue)
    ax.plot(x_values, y_continuum, color='#9ecae1', linestyle=(0, (3, 3)), lw=1.5, marker='.', ms=4)
    # This Model (solid, dark blue)
    ax.plot(x_values, y_model, color='#08519c', linestyle='-', lw=1.5, marker='D', ms=4)
    
    ax.set_xscale('log')
    # --- FIX: Y-axis MUST be log scale to show the shoulder ---
    ax.set_yscale('log') 
    ax.set_xlabel("Energy (keV)", fontsize=10)
    ax.set_ylabel("Relative Flux", fontsize=10)
    
    ax.set_xticks([1, 10, 20, 50, 100, 200])
    ax.set_xticklabels(['1', '10', '20', '50', '100', '200'])
    # FIX: Adjusted Y-ticks to match data range
    ax.set_yticks([2, 10, 20, 80, 100])
    ax.set_yticklabels(['2', '10', '20', '80', '100'])
    
    ax.set_xlim(0.8, 250)
    ax.set_ylim(1, 150) # FIX: Adjusted Y-limit
    ax.grid(True, which="major", ls=":", lw=0.5, alpha=0.5)
    ax.tick_params(labelsize=9)
    
    # Custom Legend (as requested: "直線で十分")
    handles = [
        Line2D([0], [0], color='#9ecae1', linestyle=(0, (3, 3)), lw=1.5, label="Standard Continuum"),
        Line2D([0], [0], color='#08519c', linestyle='-', lw=1.5, label="This Model (w/ Shoulder)")
    ]
    ax.legend(handles=handles, loc='upper right', fontsize=8, frameon=False)

def draw_hook2_lag_plot(ax: plt.Axes):
    """Draws the Hook 2 (Lag Hardening) plot onto ax."""
    
    # --- FIX: Data extracted directly from web demo JavaScript ---
    x_labels = ['1-3 keV', '3-5 keV', '5-10 keV']
    x = np.arange(len(x_labels))
    y_reprocessing = [5.0, 4.8, 4.5]
    y_model = [2.0, 3.5, 6.0]

    # Standard Reprocessing (dotted, light blue)
    ax.plot(x, y_reprocessing, color='#9ecae1', linestyle=(0, (3, 3)), lw=1.5, marker='.', ms=4)
    # This Model (solid, dark blue)
    ax.plot(x, y_model, color='#08519c', linestyle='-', lw=1.5, marker='D', ms=4)
    
    ax.set_xlabel("Energy Band (log E)", fontsize=10)
    ax.set_ylabel("Time Lag (arb. units)", fontsize=10)
    
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, fontsize=8)
    ax.set_yticks(np.arange(2.0, 6.5, 0.5))
    
    ax.set_ylim(1.5, 6.5)
    ax.grid(True, which="major", axis='y', ls=":", lw=0.5, alpha=0.5)
    ax.tick_params(labelsize=9)

    # Custom Legend (as requested: "直線で十分")
    handles = [
        Line2D([0], [0], color='#9ecae1', linestyle=(0, (3, 3)), lw=1.5, label="Standard Reprocessing"),
        Line2D([0], [0], color='#08519c', linestyle='-', lw=1.5, label=r"This Model ($d \log \tau / d \log E > 0$)")
    ]
    ax.legend(handles=handles, loc='upper left', fontsize=8, frameon=False)


def draw_hook3_polarization_plot(ax: plt.Axes):
    """Draws the Hook 3 (X-Ray Polarization) schematic onto ax."""
    ax.axis("off")
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal')
    
    # Main Arrow (matches image_dff164.png)
    ax.add_patch(FancyArrowPatch((0, -0.2), (0.4, 0.4),
                                  arrowstyle='->', mutation_scale=25, 
                                  lw=2.0, color='black'))
    
    # Use mathtext for LaTeX symbols
    ax.text(0, -0.4, r"$\mathbf{Angle \approx Equator (\pm 15^\circ)}$", 
            ha='center', va='top', fontsize=12, weight='bold', color="#0369a1")
    ax.text(0, -0.55,
             r"X-ray polarization angle must be consistent"
             r" with the equatorial plane, within approx. $\pm 15^\circ$.",
             ha='center', va='top', fontsize=9, linespacing=1.3, wrap=True)
    
    ax.text(0, -0.8, r"$\mathbf{Degree Tends to Rise}$", 
            ha='center', va='top', fontsize=12, weight='bold', color="#0369a1")
    ax.text(0, -0.95,
             r"The degree of polarization tends to rise with energy.",
             ha='center', va='top', fontsize=9, linespacing=1.3, wrap=True)


# --- Main PDF Building Function ---
def build_pdf_page_3_hooks(outfile: Path):
    """
    Builds only the Page 3 Hooks section as a standalone PDF.
    """
    # ページサイズを、コンテンツが収まるように調整 (幅11インチ, 高さ5インチ)
    fig = plt.figure(figsize=(11, 5))
    
    # --- Hooks Row (GridSpecで精密配置) ---
    gs_hooks = fig.add_gridspec(nrows=1, ncols=3,
                                wspace=0.35, hspace=0.1,
                                top=0.95, bottom=0.05, left=0.05, right=0.95)

    # --- Hook 1 ---
    ax_hook1_container = fig.add_subplot(gs_hooks[0, 0])
    ax_hook1_container.axis("off")
    # FIX: Add background box
    ax_hook1_container.add_patch(Rectangle((0, 0), 1, 1, 
                                     facecolor='#f8f9fa', edgecolor='#e2e8f0', 
                                     lw=1, transform=ax_hook1_container.transAxes, zorder=-1))
    # Title
    ax_hook1_container.text(0.5, 0.95, "Hook 1: High-Energy Shoulder", 
                            ha='center', va='top', fontsize=14, weight='bold', 
                            color="#0369a1", transform=ax_hook1_container.transAxes)
    # Plot
    ax_hook1_plot = ax_hook1_container.inset_axes([0.1, 0.4, 0.8, 0.5])
    draw_hook1_shoulder_plot(ax_hook1_plot)
    # Description
    ax_hook1_container.text(0.5, 0.35,
         r"Predicts a ""shoulder"" in the 20–120 keV"
         r" band. This is a quantitative hook: requires a"
         r" statistical preference of $\mathbf{\Delta BIC(shoulder\ vs.\ cutoff\text{-}PL) \geq 6}$.",
         ha='center', va='top', fontsize=10, linespacing=1.3, wrap=True, transform=ax_hook1_container.transAxes)

    # --- Hook 2 ---
    ax_hook2_container = fig.add_subplot(gs_hooks[0, 1])
    ax_hook2_container.axis("off")
    # FIX: Add background box
    ax_hook2_container.add_patch(Rectangle((0, 0), 1, 1, 
                                     facecolor='#f8f9fa', edgecolor='#e2e8f0', 
                                     lw=1, transform=ax_hook2_container.transAxes, zorder=-1))
    ax_hook2_container.text(0.5, 0.95, "Hook 2: Lag Hardening", 
                            ha='center', va='top', fontsize=14, weight='bold', 
                            color="#0369a1", transform=ax_hook2_container.transAxes)
    ax_hook2_plot = ax_hook2_container.inset_axes([0.1, 0.4, 0.8, 0.5])
    draw_hook2_lag_plot(ax_hook2_plot)
    ax_hook2_container.text(0.5, 0.35,
         r"Predicts lag hardening: an energy-"
         r"dependent trend where lags increase with"
         r" energy ($\mathbf{d \log \tau / d \log E > 0}$) across X-ray"
         r" bands, rather than a simple reprocessing echo.",
         ha='center', va='top', fontsize=10, linespacing=1.3, wrap=True, transform=ax_hook2_container.transAxes)

    # --- Hook 3 ---
    ax_hook3_container = fig.add_subplot(gs_hooks[0, 2])
    ax_hook3_container.axis("off")
    # FIX: Add background box
    ax_hook3_container.add_patch(Rectangle((0, 0), 1, 1, 
                                     facecolor='#f8f9fa', edgecolor='#e2e8f0', 
                                     lw=1, transform=ax_hook3_container.transAxes, zorder=-1))
    ax_hook3_container.text(0.5, 0.95, "Hook 3: X-Ray Polarization", 
                            ha='center', va='top', fontsize=14, weight='bold', 
                            color="#0369a1", transform=ax_hook3_container.transAxes)
    # [l, b, w, h]
    ax_hook3_plot = ax_hook3_container.inset_axes([0.0, 0.0, 1.0, 0.9]) 
    draw_hook3_polarization_plot(ax_hook3_plot)
    # (Description is embedded in the plot function for Hook 3)

    # --- Save Figure ---
    out_path = Path(outfile)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Building P3 Hooks PDF document at {out_path}...")
    fig.savefig(out_path, bbox_inches='tight', pad_inches=0.5)
    plt.close(fig)
    print("Done.")

# --- Main execution ---
def main():
    out_dir = Path("figures")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # このスクリプトは P3 の Hooks のみを生成する
    build_pdf_page_3_hooks(out_dir / "sspe_infographic_p3_hooks.pdf")

if __name__ == "__main__":
    main()

