#!/usr/bin/env python3
"""
Generates ONLY the "A Proposed Solution" flowchart section
(based on image_b768b9.png) as a single, standalone PDF.

This version (v10) incorporates the user's fontsize/position
modifications (v9) AND fixes the remaining box/arrow layout
overlaps by adjusting gridspec 'wspace' and arrow coordinates.

Requires:
  matplotlib, numpy
  (common.py must be in the same directory)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
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

def build_pdf_page_2_flowchart(outfile: Path):
    """
    Builds only the Page 2 flowchart section as a standalone PDF.
    """
    # ページサイズを、コンテンツが収まるように調整 (幅8.5インチ, 高さ5.5インチ)
    fig = plt.figure(figsize=(8.5, 5.5))
    
    # メインのAxes（キャンバス）
    ax_main = fig.add_axes([0.05, 0.05, 0.9, 0.9])
    ax_main.axis("off")
    
    # --- "How It Works" Box (CONTENT & STYLE & POSITION) ---
    
    ax_main.text(0.5, 0.95, "How It Works: A Spin-Regulated Feedback Loop", 
                 ha='center', va='top', fontsize=14, weight='bold', transform=ax_main.transAxes,
                 color="#0369a1") 

    # --- 数式用背景ボックス (User's v9 coordinates) ---
    box_y_top = 0.88
    box_height = 0.14
    ax_main.add_patch(Rectangle((0.25, box_y_top - box_height), 0.5, box_height, 
                                     facecolor='#f8f9fa', edgecolor='none', transform=ax_main.transAxes))
    
    # --- 数式 (User's v9 coordinates and fontsize) ---
    ax_main.text(0.5, box_y_top - 0.02, # Y=0.86
                 r"$P_{\rm ext} = P_{\rm eq} + P_{\rm BZ} + P_{\rm res}$",
                 ha='center', va='top', fontsize=14, transform=ax_main.transAxes) 
    ax_main.text(0.5, box_y_top - 0.07, # Y=0.81
                 r"Total extracted power is the sum of equatorial, BZ, and residual power.",
                 ha='center', va='top', fontsize=9, linespacing=1.4, transform=ax_main.transAxes)
    
    ax_main.text(0.5, box_y_top - 0.13, # Y=0.78
                 r"$f_{\rm eq} + f_{\rm BZ} + f_{\rm res} = 1$",
                 ha='center', va='top', fontsize=14, transform=ax_main.transAxes)
    ax_main.text(0.5, box_y_top - 0.18, # Y=0.75
                 r"The fractional contributions sum to unity.",
                 ha='center', va='top', fontsize=9, linespacing=1.4, transform=ax_main.transAxes)
    
    # --- 説明文 (User's v9 coordinates) ---
    ax_main.text(0.5, box_y_top - box_height - 0.09, # Y=0.70 (User had -0.09, this provides more space)
                 "This mechanism acts as a 'spin-extraction channel' that taps into the black hole's rotational energy to power the disk's luminosity,\n"
                 "creating a self-sustaining and self-limiting cycle.",
                 ha='center', va='top', fontsize=11, linespacing=1.4, transform=ax_main.transAxes)

    # --- Flowchart (GridSpecで精密配置) ---
    # FIX: wspace を 0.35 に増やしてボックス間の重なりを解消
    gs_flowchart = fig.add_gridspec(nrows=2, ncols=3,
                                    wspace=0.35, hspace=0.3, 
                                    top=0.60, bottom=0.10, left=0.05, right=0.95) 

    box_props_123 = dict(boxstyle='round,pad=0.5', facecolor='#cceeff', edgecolor='#bce1f7', lw=1)
    box_props_fb = dict(boxstyle='round,pad=0.5', facecolor='#a9bcca', edgecolor='#a9bcca', lw=1) 

    # --- Row 1: Boxes 1, 2, 3 ---
    ax_flow1 = fig.add_subplot(gs_flowchart[0, 0])
    ax_flow1.axis("off")
    ax_flow1.text(0.5, 0.5, "1. High Accretion\nGas flows in at super-\nEddington rates.",
                  ha='center', va='center', fontsize=9, linespacing=1.3, bbox=box_props_123, wrap=True, transform=ax_flow1.transAxes)

    ax_flow2 = fig.add_subplot(gs_flowchart[0, 1])
    ax_flow2.axis("off")
    ax_flow2.text(0.5, 0.5, "2. Penrose Excitation\nAt the ISCO-ergoregion boundary,\ndisk energy taps into BH spin energy.",
                  ha='center', va='center', fontsize=9, linespacing=1.3, bbox=box_props_123, wrap=True, transform=ax_flow2.transAxes)

    ax_flow3 = fig.add_subplot(gs_flowchart[0, 2])
    ax_flow3.axis("off")
    # FIX: wrap=True を削除し、手動改行(\n)を強制する
    ax_flow3.text(0.5, 0.5, r"3. Sustained $L/L_{\rm Edd} > 1$" "\n"
                  r"The extracted spin energy powers the disk," "\n"
                  r"sustaining super-Eddington luminosity.",
                  ha='center', va='center', fontsize=9, linespacing=1.3, bbox=box_props_123, transform=ax_flow3.transAxes)

    # --- Row 2: Box 4 (Feedback) ---
    ax_flow4 = fig.add_subplot(gs_flowchart[1, 1]) # 中心のセル
    ax_flow4.axis("off")
    ax_flow4.text(0.5, 0.5, "4. Spin Regulation (Feedback)\nThis energy extraction creates a counter-torque,\nslowing the black hole and enforcing a \"spin ceiling,\"\nwhich in turn regulates the excitation process.",
                  ha='center', va='center', fontsize=9, linespacing=1.3, bbox=box_props_fb, wrap=True, transform=ax_flow4.transAxes)
    
    # --- Arrows (座標をFigure基準で精密調整) ---
    # 座標系は Figure (0,0) -> (1,1)
    
    # 1 -> 2 (Straight)
    # FIX: 矢印の座標を wspace の変更に合わせて調整
    ax_main.add_patch(FancyArrowPatch((0.31, 0.48), (0.37, 0.48), # User (0.28->0.34)
                                      arrowstyle='->', mutation_scale=15, color='black', lw=0.8, transform=fig.transFigure))
    # 2 -> 3 (Straight)
    # FIX: 矢印の座標を wspace の変更に合わせて調整
    ax_main.add_patch(FancyArrowPatch((0.63, 0.48), (0.69, 0.48), # User (0.62->0.68)
                                      arrowstyle='->', mutation_scale=15, color='black', lw=0.8, transform=fig.transFigure))
    
    # 3 -> 4 (Down-left curve)
    ax_main.add_patch(FancyArrowPatch((0.75, 0.46), (0.60, 0.32), 
                                      arrowstyle='->', mutation_scale=15, color='black', lw=0.8, transform=fig.transFigure,
                                      connectionstyle="arc3,rad=-0.3"))
    
    # 4 -> 2 (U-turn curve)
    ax_main.add_patch(FancyArrowPatch((0.40, 0.32), (0.30, 0.32), 
                                      arrowstyle='->', mutation_scale=15, color='black', lw=0.8, transform=fig.transFigure,
                                      connectionstyle="arc3,rad=0.8"))

    # --- Save Figure ---
    out_path = Path(outfile)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Building P2 Flowchart PDF document at {out_path}...")
    fig.savefig(out_path, bbox_inches='tight', pad_inches=0.5)
    plt.close(fig)
    print("Done.")

# --- Main execution ---
def main():
    out_dir = Path("figures")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # このスクリプトは P2 のフローチャートのみを生成する
    build_pdf_page_2_flowchart(out_dir / "sspe_infographic_p2_flowchart.pdf")

if __name__ == "__main__":
    main()
