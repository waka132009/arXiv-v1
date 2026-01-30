# -*- coding: utf-8 -*-
# scripts/fig10_parameter_space.py
# Parameter-space panels for SSPE: (eps_coup, duty cycle) vs peak L_tot/L_Edd,
# with an in-axes ℓ = 30 guide line and screened / excluded regions.

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib.patheffects as pe

# ======= 可変パラメータ（好みに応じてここだけ触ればOK） =========================

LABEL_STYLE = "outline"  # "outline"（白ふち） or "box"（薄い白ボックス）
LABEL_POS = 0.40         # 0.0=内区間の左端, 1.0=右端（0.30〜0.60あたりが見やすい）
GUIDE_LW = 1.4           # ℓ=30 線の太さ（両図で統一）

LEVELS = np.linspace(1, 10, 10)  # 等高線の値（色段の数）
ELL_CRIT = 30.0                  # compactness threshold ℓ_crit

# ==============================================================================


def z_func(eps: np.ndarray, d: np.ndarray) -> np.ndarray:
    """
    スカラー場（説明用の簡易モデル）。
    「ピーク L_tot / L_Edd」が (eps_coup, d) にどう依存するかのダミー関数。

    - eps: coupling efficiency ε_coup
    - d  : duty cycle d

    ここを本気で物理に合わせたい場合は、V2 本文の式に応じて定義し直す。
    """
    # シンプルな形： 1 + const * eps / d で上に伸びて行くようにしておく
    z = 1.0 + 35.0 * eps / (d + 1e-3)
    return np.clip(z, 1.0, LEVELS.max())


def _place_l30_label(ax, x, y, k):
    """
    ℓ=30 ラベルを必ず枠内に配置。
    y の内側区間から LABEL_POS に基づいて選点する。
    """
    # y の「内側区間」（少しマージンを取る）
    ymin, ymax = ax.get_ylim()
    ymin_in, ymax_in = ymin + 0.02, ymax - 0.02

    inside = (y > ymin_in) & (y < ymax_in)
    idxs = np.where(inside)[0]

    if len(idxs) == 0:
        i = len(x) // 2
    else:
        i = idxs[int(np.clip(LABEL_POS, 0.0, 1.0) * max(len(idxs) - 1, 0))]

    txt = ax.text(
        x[i],
        y[i],
        r"$\ell = 30$",
        rotation=np.degrees(np.arctan(k)),
        ha="left",
        va="bottom",
        clip_on=True,
    )

    if LABEL_STYLE == "outline":
        # 白ふちアウトライン（箱なしで見やすい）
        txt.set_path_effects([pe.withStroke(linewidth=3, foreground="white")])
    elif LABEL_STYLE == "box":
        # 薄い白ボックス（安全寄り）
        txt.set_bbox(
            dict(
                boxstyle="round,pad=0.15",
                fc="white",
                ec="none",
                alpha=0.38,
            )
        )

    return txt


def make_panel(Reff: float, outstem: Path) -> None:
    """
    一枚のパネルを作る。

    Parameters
    ----------
    Reff : float
        有効半径 R_eff / r_g （ℓ=30 ガイドラインの傾きを変えるためのパラメータ）。
    outstem : Path
        出力ファイル（拡張子なし）のパス。
    """
    # グリッド
    eps = np.linspace(0.01, 0.30, 241)
    d = np.linspace(0.01, 0.30, 241)
    E, D = np.meshgrid(eps, d)
    Z = z_func(E, D)

    # 図キャンバス
    fig = plt.figure(figsize=(5.4, 4.6), constrained_layout=True)
    ax = fig.add_subplot(111)

    # 等高塗り＋カラーバー
    cf = ax.contourf(E, D, Z, levels=LEVELS)
    cbar = fig.colorbar(cf, ax=ax, ticks=LEVELS[::2])
    cbar.set_label(r"Peak Eddington ratio $L_{\rm tot}/L_{\rm Edd}$")

    # 軸ラベル・範囲
    ax.set_xlabel(r"Coupling efficiency $\epsilon_{\rm coup}$")
    ax.set_ylabel(r"Duty cycle $d$")
    ax.set_xlim(0.01, 0.30)
    ax.set_ylim(0.01, 0.30)

    ax.grid(True, alpha=0.30, linestyle="--")

    # ℓ=30 ガイドライン（傾きは Reff に反比例）
    k = 300.0 / Reff  # Reff=100 → 急, 1000 → 緩やか
    x = np.linspace(0.02, 0.30, 400)
    y = k * x

    # 描画は表示範囲にクリップ
    yclip = np.clip(y, *ax.get_ylim())
    line, = ax.plot(x, yclip, color="black", lw=GUIDE_LW)

    # 上下を薄く塗り分けて「screened / excluded」を可視化
    ymin, ymax = ax.get_ylim()

    # ℓ > ℓcrit 側（線より上）：pair-thick / excluded
    ax.fill_between(
        x,
        yclip,
        ymax,
        where=yclip < ymax,
        alpha=0.06,
        color="black",
        interpolate=True,
    )

    # ℓ < ℓcrit 側（線より下）：screened sample
    ax.fill_between(
        x,
        ymin,
        yclip,
        where=yclip > ymin,
        alpha=0.04,
        color="white",
        interpolate=True,
    )

    # ラベル（ℓ=30）
    _place_l30_label(ax, x, y, k)

    # リージョンの簡単なテキスト
    ax.text(
        0.025,
        ymax - 0.03,
        r"$\ell > \ell_{\rm crit}$" "\n" r"(pair-thick / excluded)",
        ha="left",
        va="top",
        fontsize=9,
    )
    ax.text(
        0.27,
        ymin + 0.03,
        r"$\ell < \ell_{\rm crit}$" "\n" r"(screened sample)",
        ha="right",
        va="bottom",
        fontsize=9,
    )

    # 保存（PDFのみ）
    outstem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outstem.with_suffix(".pdf"))
    plt.close(fig)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    out = root / "figures"

    # Reff = 100, 1000 の2パネル（ApJ V2 では片方だけ使うならここを削ってOK）
    make_panel(100, out / "fig10a_Reff100")
    make_panel(1000, out / "fig10b_Reff1000")


if __name__ == "__main__":
    # 既定のスタイル（TeX不要の mathtext; 既存の共通設定を壊さない）
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
