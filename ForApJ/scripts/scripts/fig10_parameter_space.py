# -*- coding: utf-8 -*-
# scripts/fig10_parameter_space.py
# Figure 10 (a,b): Parameter space panels with robust in-axes ℓ=30 label

from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib.patheffects as pe

# ======= 可変パラメータ（好みに応じてここだけ触ればOK） =========================
LABEL_STYLE = "outline"   # "outline"（白ふち） or "box"（薄い白ボックス）
LABEL_POS   = 0.40        # 0.0=内区間の左端, 1.0=右端（0.30〜0.60あたりが見やすい）
GUIDE_LW    = 1.4         # ℓ=30 線の太さ（両図で統一）
LEVELS      = np.linspace(1, 10, 10)  # 等高線の値（色段の数）
# ==============================================================================

def z_func(eps, d):
    """スカラー場（説明用の簡易モデル）。必要なら式をここで定義し直す。"""
    z = 1.0 + 35.0 * eps / (d + 1e-3)
    return np.clip(z, 1.0, LEVELS.max())

def _place_label(ax, x, y, k):
    """ラベルを必ず枠内に配置。yの内側区間から LABEL_POS に基づいて選点。"""
    # 枠（少し内側にマージン）
    ymin, ymax = 0.01, 0.30
    margin = 0.02
    inside = (y > ymin + margin) & (y < ymax - margin)
    idxs = np.where(inside)[0]
    if len(idxs) == 0:
        i = len(x) // 2
    else:
        i = idxs[int(np.clip(LABEL_POS, 0.0, 1.0) * (len(idxs)-1))]

    txt = ax.text(x[i], y[i], r"$\ell = 30$",
                  rotation=np.degrees(np.arctan(k)),
                  ha="left", va="bottom", clip_on=True)

    if LABEL_STYLE == "outline":
        # 白ふちアウトライン（箱なしで見やすい）
        txt.set_path_effects([pe.withStroke(linewidth=3, foreground="white")])
    elif LABEL_STYLE == "box":
        # 薄い白ボックス（安全寄り）
        txt.set_bbox(dict(boxstyle="round,pad=0.15",
                          fc="white", ec="none", alpha=0.38))
    return txt

def make_panel(Reff: float, outstem: Path):
    # グリッド
    eps = np.linspace(0.01, 0.30, 241)
    d   = np.linspace(0.01, 0.30, 241)
    E, D = np.meshgrid(eps, d)
    Z = z_func(E, D)

    # 図キャンバス
    fig = plt.figure(figsize=(5.4, 4.6), constrained_layout=True)
    ax  = fig.add_subplot(111)

    # 等高塗り＋カラーバー
    cf = ax.contourf(E, D, Z, levels=LEVELS)
    cbar = fig.colorbar(cf, ax=ax, ticks=LEVELS[::2])
    cbar.set_label(r"Peak Eddington ratio $L_{\rm tot}/L_{\rm Edd}$")

    # ラベル・軸
    # ax.set_title(rf"Figure 1: Parameter Space ($R_{{\rm eff}} = {int(Reff)}\,r_g$)")
    ax.set_xlabel(r"Coupling efficiency $\varepsilon_{\rm coup}$")
    ax.set_ylabel(r"Duty cycle $d$")
    ax.set_xlim(0.01, 0.30)
    ax.set_ylim(0.01, 0.30)
    ax.grid(True, alpha=0.30, linestyle="--")

    # ℓ=30 ガイドライン（傾きは Reff に反比例）
    k = 300.0 / Reff                      # Reff=100 → 急、1000 → 緩やか
    x = np.linspace(0.02, 0.30, 400)
    y = k * x
    # 描画は表示範囲にクリップ（線が外へ飛び出しても見た目はOK）
    yclip = np.clip(y, ax.get_ylim()[0], ax.get_ylim()[1])
    ax.plot(x, yclip, color="black", lw=GUIDE_LW)

    # ラベル（必ず枠内へ）
    _place_label(ax, x, y, k)

    # 保存（PDFのみ）
    outstem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outstem.with_suffix(".pdf"))
    plt.close(fig)

def main():
    root = Path(__file__).resolve().parents[1]
    out  = root / "figures"
    make_panel(100,  out / "fig10a_Reff100")
    make_panel(1000, out / "fig10b_Reff1000")

if __name__ == "__main__":
    # 既定のスタイル（TeX不要のmathtext; 既存の共通設定を壊さない）
    plt.rcParams.update({
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
    })
    main()
