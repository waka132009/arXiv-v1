#!/usr/bin/env python3
"""
Generates ONLY the "Key Observational Signatures (The "Hooks")" section
(based on image_dff164.png layout) as a single, standalone PDF.

This version (v4) fixes:
1.  Data for Hook 1 & 2 is sourced *exactly* from the web demo.
2.  Hook 1 Y-axis and X-axis are 'log' scale to correctly show the "shoulder".
3.  A background box (Rectangle) is added to each hook section.
4.  Text overlaps are fixed by precisely adjusting inset_axes and text positions.
5.  Hook 3 layout is corrected.

Requires:
  matplotlib, numpy
  (common.py must be in the same directory)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
from matplotlib.lines import Line2D
from pathlib import Path
import matplotlib.patheffects as pe
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
    """
    Hook 1（High-Energy Shoulder）— 可読化版
    ・正規化：10 keV ピボット（実点を使う）
    ・対数軸／肩帯（20–120 keV）／色弱対応の線種
    ・標準反射ハンプの参照（点線）
    ・代表誤差（少数点）
    ・yレンジ固定で潰れ防止
    """
    # 元の簡易データ
    E = np.array([1, 10, 20, 50, 100, 200], dtype=float)
    y_cont  = np.array([100, 20, 10, 5, 3, 2], dtype=float)    # cutoff-PL（肩なし）
    y_model = np.array([80,  25, 40, 50, 40,10], dtype=float)  # 肩あり

    # ---- 正規化：10 keV ピボット ----
    # 実データ点があるので外挿せずに済む
    pivot_E = 10.0
    idx10 = np.where(E == pivot_E)[0][0]
    y_cont  = y_cont  / y_cont[idx10]
    y_model = y_model / y_model[idx10]

    # ---- 肩帯（obs 20–120 keV）----
    ax.axvspan(20, 120, color='#4c78a8', alpha=0.13,
               label ="shoulder band (obs 20–120 keV)")
    ax.text(45, 5, "20–120 keV", fontsize=7, ha="center", va="bottom")

    # ---- 反射ハンプの参照（薄グレー点線：混同防止）----
    #Eh = np.logspace(np.log10(8), np.log10(40), 120)
    #hump = 0.8 * (Eh/20.0)**(-0.3) * np.exp(-((np.log10(Eh)-np.log10(20))/0.35)**2)
    # 10 keV に合わせて規格化
    # 10 keV がレンジ外の場合は最も近い点にスナップ
    #def nearest_idx(arr, val): return int(np.argmin(np.abs(arr - val)))
    #hump /= hump[nearest_idx(Eh, 10.0)]
    #ax.plot(Eh, hump, linestyle=":", linewidth=1.1, alpha=0.55, color="#777777",
    #        label="standard reflection (schematic)")

    # ---- 主曲線（色弱対応：実線＋● vs 長破線）----
    ax.errorbar(E, y_model, yerr=[0,0,0.12,0.10,0,0.15], fmt='o-', lw=2.1, ms=4.6,
                color='#0b4f9c', capsize=2, label="This model (with shoulder)")
    ax.plot(E, y_cont, linestyle=(0,(8,4)), lw=2.0, color='#93c2e6',
            label="Cutoff power-law")

    # --- roll-off 注記（log–log補間で y を取る）---
    def _loglog_interp(xp, yp, xq):
        xp = np.asarray(xp); yp = np.asarray(yp)
        return np.exp(np.interp(np.log(xq), np.log(xp), np.log(yp)))

    roll_x = 160.0                                   # 矢印の先（keV）← ここを動かすだけ
    roll_y = _loglog_interp(E, y_model, roll_x)      # y を log–log で補間
    text_x = 130.0                                    # テキスト位置 x（keV）
    text_y = roll_y * 4.0                            # テキスト位置 y（相対で上へ）

    ann=ax.annotate("shoulder roll-off",
                xy=(roll_x, roll_y), xycoords='data',
                xytext=(text_x, text_y), textcoords='data',
                ha='left', va='bottom',
                arrowprops=dict(arrowstyle='->', lw=1.0), fontsize=8, zorder=6, annotation_clip=False)
    ann.set_path_effects([pe.withStroke(linewidth=2.6, foreground='white')])
    ## ---- roll-off 注記（~200 keV）----
    #ax.annotate("shoulder roll-off", xy=(200, y_model[-1]), xycoords='data',
    #            xytext=(110, 0.45), textcoords='data',
    #            arrowprops=dict(arrowstyle='->', lw=1.0), fontsize=8)

    # ---- 軸・レンジ・書式 ----
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlim(0.9, 230)
    ax.set_ylim(0.08, 8.0)  # ← 潰れ防止の固定レンジ
    ax.set_xticks([1,2,5,10,20,50,100,200])
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
    ax.set_xlabel("Energy (keV)")
    ax.set_ylabel("Relative Flux (normalized to 10 keV)")
    ax.grid(True, which='both', axis='both', alpha=0.15)

    
    # Custom Legend (as requested: "直線で十分")
    handles = [
        Line2D([0], [0], color='#9ecae1', linestyle=(0, (3, 3)), lw=1.5, label="Standard Continuum"),
        Line2D([0], [0], color='#08519c', linestyle='-', lw=1.5, label="This Model (with shoulder)")
    ]
   # 微調整（少し上にずらす）するコード
    ax.legend(
        handles=handles,
        loc='upper right', # 凡例自身の「右上隅」を...
        bbox_to_anchor=(0.86, 1.19), # グラフ領域の「(x=1.0, y=1.05)」の位置に配置する
        fontsize=8,
        frameon=False
    )

def draw_hook2_lag_plot(ax: plt.Axes):
    """Draws the Hook 2 (Lag Hardening) plot onto ax."""
    
    # --- Data extracted directly from web demo JavaScript ---
    x_labels = ['1-3 keV', '3-5 keV', '5-10 keV']
    x = np.arange(len(x_labels))
    y_reprocessing = [5.0, 4.8, 4.5]
    y_model = [2.0, 3.5, 6.0]

    # Standard Reprocessing (dotted, light blue)
    ax.plot(x, y_reprocessing, color='#a6cee3', linestyle=(0, (3, 3)), lw=1.5, marker='.', ms=4)
    # This Model (solid, dark blue)
    ax.plot(x, y_model, color='#1f78b4', linestyle='-', lw=1.5, marker='D', ms=4)
    
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
        Line2D([0], [0], color='#a6cee3', linestyle=(0, (3, 3)), lw=1.5, label="Standard Reprocessing"),
        Line2D([0], [0], color='#1f78b4', linestyle='-', lw=1.5, label=r"This Model ($d \log \tau / d \log E > 0$)")
    ]
    ax.legend(
        handles=handles,
        loc='upper right', 
        bbox_to_anchor=(0.90, 1.19),
        fontsize=8,
        frameon=False
    )


def draw_hook3_polarization_plot(ax: plt.Axes):
    """Draws the Hook 3 (X-Ray Polarization) schematic onto ax."""
    ax.axis("off")
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal')
    
    # --- FIX: Re-centered layout ---
    
    # Main Arrow (matches image_dff164.png)
    ax.add_patch(FancyArrowPatch((0, -0.1), (0.4, 0.5), # Adjusted coordinates
                                  arrowstyle='->', mutation_scale=25, 
                                  lw=2.0, color='black'))
    
    # Use mathtext for LaTeX symbols
    ax.text(0.5, 0.2, r"$\mathbf{Angle \approx Equator (\pm 15^\circ)}$", 
            ha='center', va='top', fontsize=12, weight='bold', color="#0369a1", transform=ax.transAxes)
    ax.text(0.5, 0.05,
             r"X-ray polarization angle must be consistent"
             r" with the equatorial plane, within approx. $\pm 15^\circ$.",
             ha='center', va='top', fontsize=9, linespacing=1.3, wrap=True, transform=ax.transAxes)
    
    ax.text(0.5, -0.2, r"$\mathbf{Degree Tends to Rise}$", 
            ha='center', va='top', fontsize=12, weight='bold', color="#0369a1", transform=ax.transAxes)
    ax.text(0.5, -0.35,
             r"The degree of polarization tends to rise with energy.",
             ha='center', va='top', fontsize=9, linespacing=1.3, wrap=True, transform=ax.transAxes)


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
    ax_hook1_container.text(0.5, 1.10, "Hook 1: High-Energy Shoulder", 
                            ha='center', va='top', fontsize=14, weight='bold', 
                            color="#0369a1", transform=ax_hook1_container.transAxes)
    # Plot
    # FIX: Adjusted inset_axes [l, b, w, h] to make space for text
    ax_hook1_plot = ax_hook1_container.inset_axes([0.1, 0.45, 0.8, 0.45])
    draw_hook1_shoulder_plot(ax_hook1_plot)
    # Description
    # FIX: Adjusted Y-position (0.35 -> 0.38)
    ax_hook1_container.text(
            0.5, 0.28,
            r"Shoulder expected in the 20–120 keV"
            "\n"
            r"band. Quantitative hook:"
            "\n"
            r"$\Delta \mathrm{BIC}\!\geq\!6$ (shoulder vs.\ cutoff-PL)"
            "\n"
            r"over a standard continuum.",
            ha="center", va="top", fontsize=10,
            linespacing=1.3, wrap=False,
            transform=ax_hook1_container.transAxes
    )
    # --- Hook 2 ---
    ax_hook2_container = fig.add_subplot(gs_hooks[0, 1])
    ax_hook2_container.axis("off")
    # FIX: Add background box
    ax_hook2_container.add_patch(Rectangle((0, 0), 1, 1, 
                                     facecolor='#f8f9fa', edgecolor='#e2e8f0', 
                                     lw=1, transform=ax_hook2_container.transAxes, zorder=-1))
    ax_hook2_container.text(0.5, 1.10, "Hook 2: Lag Hardening", 
                            ha='center', va='top', fontsize=14, weight='bold', 
                            color="#0369a1", transform=ax_hook2_container.transAxes)
    # FIX: Adjusted inset_axes
    ax_hook2_plot = ax_hook2_container.inset_axes([0.1, 0.45, 0.8, 0.45])
    draw_hook2_lag_plot(ax_hook2_plot)
    # FIX: Adjusted Y-position
    ax_hook2_container.text(0.5, 0.38,
         r"Predicts lag hardening: an energy-" "\n"
         r"dependent trend where lags increase with" "\n"
         r"energy ($\mathbf{d \log \tau / d \log E > 0}$) across X-ray" "\n"
         r"bands, rather than a simple reprocessing echo.",
         ha='center', va='top', fontsize=10, linespacing=1.3, wrap=True, transform=ax_hook2_container.transAxes)

    # --- Hook 3 ---
    ax_hook3_container = fig.add_subplot(gs_hooks[0, 2])
    ax_hook3_container.axis("off")
    # FIX: Add background box
    ax_hook3_container.add_patch(Rectangle((0, 0), 1, 1, 
                                     facecolor='#f8f9fa', edgecolor='#e2e8f0', 
                                     lw=1, transform=ax_hook3_container.transAxes, zorder=-1))
    ax_hook3_container.text(0.5, 1.10, "Hook 3: X-Ray Polarization", 
                            ha='center', va='top', fontsize=14, weight='bold', 
                            color="#0369a1", transform=ax_hook3_container.transAxes)
    # FIX: Adjusted inset_axes
    ax_hook3_plot = ax_hook3_container.inset_axes([0.1, 0.1, 0.8, 0.8]) 
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

