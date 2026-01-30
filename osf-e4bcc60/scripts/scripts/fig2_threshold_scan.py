# scripts/fig2a_spin_evolution.py
from __future__ import annotations
import numpy as np, matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from pathlib import Path

# 見た目（前のPNGに寄せる）
plt.rcParams.update({
    "text.usetex": False,            # TeX不要（本文と記号統一なら r"$a_\ast$" 表記でOK）
    "mathtext.fontset": "stix",
    "mathtext.rm": "STIXGeneral",
    "font.size": 11,
    "axes.titlesize": 18,            # 大きめタイトル
    "axes.labelsize": 14,
    "axes.linewidth": 1.2,
    "grid.alpha": 0.35,
    "grid.linestyle": "--",
    "savefig.bbox": "tight",
})

def spin_model(t):
    # 形状は前画像に近いゆるやかな減衰（必要なら tau / 下限を微調整）
    a0  = 0.998
    floor = 0.987
    tau = 28.0  # Myr
    return floor + (a0 - floor) * np.exp(-t / tau)

def main():
    t = np.linspace(0, 50, 400)   # [Myr]
    a = spin_model(t)

    fig, ax = plt.subplots(figsize=(8.0, 5.2))  # 横長
    ax.plot(t, a, color="#d99a00", lw=6, solid_capstyle="round")  # マスタード色・一定幅

    # 軸レンジと目盛り（前の絵の刻みに合わせる）
    ax.set_xlim(0, 50)
    ax.set_ylim(0.987, 0.9982)
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_major_formatter(FormatStrFormatter("%.3f"))
    ax.yaxis.set_minor_locator(MultipleLocator(0.001))

    # ラベル／タイトル
    ax.set_xlabel("Time [Myr]", labelpad=8)
    ax.set_ylabel(r"Spin parameter $a_\ast$", labelpad=12)
    # ax.set_title("Figure 2a: Spin Evolution vs Time", pad=14)

    # グリッド
    ax.grid(True, which="major")
    ax.grid(True, which="minor", alpha=0.15)

    out = Path(__file__).resolve().parents[1] / "figures" / "fig2a_spin_evolution"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out.with_suffix(".pdf"))   # PDFのみ
    plt.close(fig)

if __name__ == "__main__":
    main()
