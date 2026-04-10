# scripts/fig2a_spin_evolution.py
from __future__ import annotations
import numpy as np, matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from pathlib import Path

# ここは共通スタイルに合わせて必要なら import common でも可
mpl = plt.matplotlib
mpl.rcParams.update({
    "text.usetex": False,           # TeX不要でSTIX数式
    "mathtext.fontset": "stix",
    "mathtext.rm": "STIXGeneral",
    "font.size": 11,
    "axes.titlesize": 18,           # タイトル大きめ
    "axes.labelsize": 14,
    "axes.linewidth": 1.2,
    "grid.alpha": 0.35,
    "grid.linestyle": "--",
    "savefig.bbox": "tight",
})

def spin_model(t):
    # 例: 初期 a*=0.998 から緩やかに減衰（形は調整してOK）
    a0 = 0.998
    tau = 28.0  # Myr（形を合わせたいならここを触る）
    return 0.987 + (a0 - 0.987) * np.exp(-t / tau)

def main():
    t = np.linspace(0, 50, 400)            # [Myr]
    a = spin_model(t)

    fig, ax = plt.subplots(figsize=(8.0, 5.2))  # 横長比率
    ax.plot(t, a, color="#d99a00", lw=6, solid_capstyle="round")  # マスタード太線

    # 軸レンジと目盛り
    ax.set_xlim(0, 50)
    ax.set_ylim(0.987, 0.9982)
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_major_formatter(FormatStrFormatter("%.3f"))
    ax.yaxis.set_minor_locator(MultipleLocator(0.001))

    # ラベル（本文に合わせるなら '$a_\\ast$' 推奨）
    ax.set_xlabel(r"Cumulative active time $t_{\rm act}$ [Myr]", fontsize=18, labelpad=8)
    ax.set_ylabel(r"Spin parameter $a_\ast$", labelpad=12)

    # タイトルを上大きめで
    # ax.set_title("Figure 2a: Spin Evolution vs Time", pad=14)

    # グリッド
    ax.grid(True, which="major")
    ax.grid(True, which="minor", alpha=0.15)

    out = Path(__file__).resolve().parents[1] / "figures" / "fig2a_spin_evolution"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out.with_suffix(".pdf"))
    plt.close(fig)

if __name__ == "__main__":
    main()
