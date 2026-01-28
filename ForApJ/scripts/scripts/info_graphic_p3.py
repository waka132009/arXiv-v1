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

#GLOBAL_VARS
HOOK3_band=15.0

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
    ax.text(49, 5, "20–120 keV", fontsize=7, ha="center", va="bottom")

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
    """
    Hook 2 (Lag Hardening) — schematic only.
    - 連続 log10(E/keV) に対して lag が単調増加（d lag / d log E > 0）
    - 観測点なし：中央線 + 薄い許容帯 + （任意）低エネ参照帯
    - スタイルは common.py に依存（ここでは rcParams を触らない）
    """
    # ---- パラメータ（必要なら数字だけ調整）----
    x_min_keV, x_max_keV = 1.0, 100.0
    slope_per_dec   = 0.9      # [arb./dec] d(lag)/d log10(E)
    intercept_1keV  = 2.0      # [arb.]     lag at 1 keV
    band_frac       = 0.15     # 許容帯の相対幅（±15%）
    ref_band        = (1.0, 2.0)  # 低エネ参照帯（不要なら None）

    # ---- 軸データ（連続）----
    E_keV = np.logspace(np.log10(x_min_keV), np.log10(x_max_keV), 256)
    xlog  = np.log10(E_keV)
    lag_center = slope_per_dec * xlog + intercept_1keV
    lag_low    = lag_center * (1 - band_frac)
    lag_high   = lag_center * (1 + band_frac)

    # ---- 参照帯（任意）----
    if isinstance(ref_band, (tuple, list)) and len(ref_band) == 2:
        lo, hi = float(ref_band[0]), float(ref_band[1])
        if lo > hi:
            lo, hi = hi, lo

        # 主要目盛（log軸で使ってる値）にスナップ
        ticks = (1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0)
        def snap(v):
            for t in ticks:
                if abs(v - t) <= max(1e-6, 1e-6 * t):  # 浮動小数の誤差を吸収
                    return t
            return v

        lo, hi = snap(lo), snap(hi)
        if lo < hi:
            ax.axvspan(lo, hi, alpha=0.08, lw=0, label="Reference band", zorder=0)

    # ---- 概念図：許容帯 + 中央線（色は既存パレットに寄せる）----
    ax.fill_between(E_keV, lag_low, lag_high, alpha=0.12, linewidth=0,
                    color="#1f78b4", label="Expected range (schematic)")
    ax.plot(E_keV, lag_center, lw=2.0, color="#1f78b4",
            label="Model trend (schematic)")

    # ---- 体裁（カテゴリ軸→連続log軸へ置換）----
    ax.set_xscale("log")
    ax.set_xlim(x_min_keV*0.9, x_max_keV*1.1)
    ax.set_xlabel("Energy (keV)")
    #ax.set_ylabel("Lag (arb. units)")
    fig = ax.figure
    fig.subplots_adjust(left=0.235, right=0.965, top=0.88, bottom=0.285)
    ax.set_ylabel("Lag (arb. units)", labelpad=3)
    # 既存グリッド感に合わせて y のメジャーのみ点線
    ax.grid(True, which="major", alpha=0.28)
    ax.grid(True, which="minor", alpha=0.12)
    ax.minorticks_on()
    ax.set_xticks([1, 2, 5, 10, 20, 50, 100])
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
    # レイアウトに合わせた見栄えレンジ（必要なら自動にしてOK）
    ax.set_ylim(1.5, 6.5)

    # ---- 右上注記（符号主張のみ。数式は凡例に入れない）----
    #ax.text(0.98, 0.98,
    #        rf"$\frac{{d\,\mathrm{{lag}}}}{{d\log E}}>0$  (slope ≈ {slope_per_dec:.2f}/dec)",
    #        ha="right", va="top", transform=ax.transAxes)
    ax.text(0.7, 0.97,
            r"$\frac{d\,\mathrm{lag}}{d\log E}>0\ \ (\mathrm{slope}\approx0.90/\mathrm{dec})$",
            ha="right", va="top", transform=ax.transAxes,
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.55, pad=1.5),fontsize=9)

    # ---- 凡例（最小主義）----
    handles = [
        Line2D([0], [0], color="#1f78b4", linestyle="-", lw=1.8, label="Model trend (schematic)"),
        Line2D([0], [0], color="#1f78b4", linestyle="-", lw=8, alpha=0.12, label="Expected range (schematic)"),
    ]
    ax.legend(handles=handles, loc="upper right", bbox_to_anchor=(1.00, 1.19),
              fontsize=8, frameon=False)


def draw_hook3_polarization_plot(ax: plt.Axes,
                        *,
                        ref_band=(1.0, 2.0),
                        angle_band_deg=15.0,
                        deg_low_hi=(2.0, 8.0)):
    """
    Hook 3: X-ray Polarization (schematic)
    - Angle: should align with equatorial plane within ±angle_band_deg.
    - Degree: tends to rise with energy.
    - 観測点なし／メカニズム非依存の期待形のみを表示。
    """
    import numpy as np
    import matplotlib.pyplot as plt

    # --- x軸（1–100 keV）---
    x_min_keV, x_max_keV = 1.0, 100.0
    E = np.logspace(np.log10(x_min_keV), np.log10(x_max_keV), 256)
    xlog = np.log10(E)

    # --- Angle (deg) — 左y軸 ---
    # equator=0° を基準、±band を薄帯で示す
    y_center = np.zeros_like(E)
    HOOK3_band = float(angle_band_deg)
    y_low = -HOOK3_band * np.ones_like(E)
    y_high = +HOOK3_band * np.ones_like(E)

    # 参照帯（任意）
    if isinstance(ref_band, (tuple, list)) and len(ref_band) == 2:
        lo, hi = float(ref_band[0]), float(ref_band[1])
        # 目盛にスナップ（1,2,5,10,20,50,100）
        ticks = (1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0)
        def snap(v):
            for t in ticks:
                if abs(v - t) <= max(1e-6, 1e-6 * t):
                    return t
            return v
        lo, hi = snap(lo), snap(hi)
        if lo < hi:
            ax.axvspan(lo, hi, alpha=0.08, lw=0, label="Reference band", zorder=0)

    # 薄帯＋中心線（角度）
    ax.fill_between(E, -HOOK3_band, +HOOK3_band, alpha=0.12, linewidth=0, zorder=1,
                    label=r"Equatorial band ($\pm15^\circ$)")
    #ax.plot(E, np.zeros_like(E), lw=2.0, zorder=3, label="Polarization angle (schematic)")
    ax.plot(E, np.zeros_like(E), lw=2.6, color='#f8f9fa', zorder=3)
    ax.plot(E, np.zeros_like(E), lw=2.0, color="#0369a1", zorder=4, label="Polarization angle (schematic)")
    # --- Degree (%) — 右y軸（twin）---
    ax_r = ax.twinx()
    d0, d1 = float(deg_low_hi[0]), float(deg_low_hi[1])
    deg = d0 + (d1 - d0) * (xlog - xlog.min()) / (xlog.max() - xlog.min())
    ax_r.plot(E, deg, lw=1.6, ls="-.", zorder=2, label="Degree (schematic)")

    import matplotlib.ticker as mticker
    ax_r.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    ax.set_ylim(-18, 18); ax_r.set_ylim(0, 10)


    # --- 体裁 ---
    ax.set_xscale("log")
    ax.set_xlim(x_min_keV*0.9, x_max_keV*1.1)
    ax.set_xlabel("Energy (keV)")

    ax.set_ylabel("Polarization angle (deg)", labelpad=3)
    ax.tick_params(axis="y", pad=3)                        # ★ 追加：目盛りラベルの余白
    ax.set_ylim(-max(20.0, HOOK3_band*1.2), max(20.0, HOOK3_band*1.2))
    ax.minorticks_on()
    ax.set_xticks([1, 2, 5, 10, 20, 50, 100])
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
    ax.grid(True, which="major", alpha=0.28)
    ax.grid(True, which="minor", alpha=0.12)
   
    ax_r.set_ylabel("Polarization degree (%)", labelpad=3)
    ax_r.tick_params(axis="y", pad=3)
    #ax_r.set_ylim(0, max(10.0, d1*1.2))
    ax_r.set_ylim(0, 9)
    ax_r.grid(False)

    # 右上注記（角度の主張を短く）
    ax.text(0.80, 0.98, r"Angle $\approx$ equator ($\pm 15^\circ$)",
            ha="right", va="top", transform=ax.transAxes,
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.55, pad=1.5), fontsize=9)

    # --- twin の凡例を合体して外出し（内側の ax.legend を置き換え）---
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax_r.get_legend_handles_labels()
    short = {
        "Reference band": "Ref. band",
        r"Equatorial band ($\pm15^\circ$)": r"Equat. (±15°)",
        "Polarization angle (schematic)": "Angle (schem.)",
        "Degree (schematic)": "Degree (schem.)",
    }
    handles = h1 + h2
    labels  = [short.get(s, s) for s in (l1 + l2)] 
    
    ax.legend(
        handles, labels,
        loc="lower center",                 # ★ 中央基準
        bbox_to_anchor=(0.50, 1.02),        # ★ Axes上端の少し上
        bbox_transform=ax.transAxes,
        ncol=2, frameon=False,
        fontsize=9,                         # 少しだけ絞る
        handlelength=2.2, columnspacing=1.0, labelspacing=0.6,
        borderaxespad=0.0
    )
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
    ax_hook1_container.add_patch(Rectangle((-0.15, 0), 1.3, 1, 
                                     facecolor='#f8f9fa', edgecolor='#e2e8f0', 
                                     lw=1, transform=ax_hook1_container.transAxes, zorder=-1, clip_on=False))
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
            r"Shoulder expected in the 20–120 keV" "\n"
            r"$\Delta \mathrm{BIC}\!\geq\!6$ (shoulder vs.\ cutoff-PL)" "\n"
            r"over a standard continuum.",
    #        r"$\Delta \mathrm{BIC}\!\geq\!6$",
            ha="center", va="top", fontsize=10,
            linespacing=1.3, wrap=False,
            transform=ax_hook1_container.transAxes
    )
    # --- Hook 2 ---
    ax_hook2_container = fig.add_subplot(gs_hooks[0, 1])
    ax_hook2_container.axis("off")
    # FIX: Add background box
    ax_hook2_container.add_patch(Rectangle((-0.1, 0), 1.2, 1, 
                                     facecolor='#f8f9fa', edgecolor='#e2e8f0', 
                                     lw=1, transform=ax_hook2_container.transAxes, zorder=-1, clip_on=False))
    ax_hook2_container.text(0.5, 1.10, "Hook 2: Lag Hardening", 
                            ha='center', va='top', fontsize=14, weight='bold', 
                            color="#0369a1", transform=ax_hook2_container.transAxes)
    # FIX: Adjusted inset_axes
    ax_hook2_plot = ax_hook2_container.inset_axes([0.1, 0.45, 0.8, 0.45])
    draw_hook2_lag_plot(ax_hook2_plot)
    # FIX: Adjusted Y-position
    ax_hook2_container.text(0.5, 0.30,
         r"Lag increases with energy (``lag hardening'')." "\n"
         r"Schematic trend expected from the model;" "\n"
         r"$\frac{d\,\mathrm{lag}}{d\log E}>0$ across X-ray bands" "\n"
         r"evaluated against a baseline continuum.",
         ha='center', va='top', fontsize=10, linespacing=1.3, wrap=True, transform=ax_hook2_container.transAxes)

    # --- Hook 3 ---
    ax_hook3_container = fig.add_subplot(gs_hooks[0, 2])
    ax_hook3_container.axis("off")
    # FIX: Add background box
    ax_hook3_container.add_patch(Rectangle((-0.1, 0), 1.2, 1, 
                                     facecolor='#f8f9fa', edgecolor='#e2e8f0', 
                                     lw=1, transform=ax_hook3_container.transAxes, zorder=-1, clip_on=False))
    ax_hook3_container.text(0.5, 1.10, "Hook 3: X-Ray Polarization", 
                            ha='center', va='top', fontsize=14, weight='bold', 
                            color="#0369a1", transform=ax_hook3_container.transAxes)
    # FIX: Adjusted inset_axes
    ax_hook3_plot = ax_hook3_container.inset_axes([0.1, 0.45, 0.8, 0.45]) 
    draw_hook3_polarization_plot(ax_hook3_plot)
    # (Description is embedded in the plot function for Hook 3)
    ax_hook3_container.text(0.5, 0.30,
         r"X-ray polarization angle is" "\n"
         r"consistent with the equatorial plane." "\n"
         rf"Schematic expectation: angle within $\pm {int(HOOK3_band)}^\circ$;" "\n"
         r"polarization degree tends to rise with energy," "\n"
         r"relative to a mechanism-agnostic baseline.",
         ha='center', va='top', fontsize=10, linespacing=1.3, wrap=True, transform=ax_hook3_container.transAxes)


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

