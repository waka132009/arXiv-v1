#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig4:
  - Fig4a: tau_eq (time to reach equilibrium spin) vs epsilon_coup
  - Fig4b: L/L_Edd vs a_eq (mapping from equilibrium spin to luminosity)

Usage:
  python scripts/fig4.py --polished
  python scripts/fig4.py --params data/fig3_params.csv --polished
    # params CSV: column 'epsilon_coup' (re-use of fig3 file)
"""

import argparse, os, csv, numpy as np
import matplotlib.pyplot as plt

# ================= Placeholder physics (差し替えポイント) =================
def torque_balance(a, eps):
    # Same toy model as Fig3; replace with actual da/dt(a, eps).
    return (1.0 - a)**1.5 * (1.0 - 0.1*eps) - eps * a**2

def L_over_LEdd_from_eps(eps):
    # Placeholder mapping used in Fig2 idea; replace with your relation.
    return 1.0 + 25.0*eps/(0.12 + eps)

# ---------- Helpers ----------
def load_eps_list(path):
    defaults = [0.005, 0.01, 0.02, 0.05, 0.10]
    try:
        vals = []
        with open(path, newline="", encoding="utf-8") as f:
            rdr = csv.DictReader(f)
            if not rdr.fieldnames or "epsilon_coup" not in rdr.fieldnames:
                return defaults
            for r in rdr:
                s = (r.get("epsilon_coup") or "").strip()
                if s:
                    vals.append(float(s))
        return sorted(vals) if vals else defaults
    except FileNotFoundError:
        return defaults

def ensure_out(path, polished=False):
    base, name = os.path.split(path)
    if polished:
        base = os.path.join(base, "polished")
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, name)

def find_a_eq(eps, grid=np.linspace(0.85, 0.9995, 4000)):
    y = torque_balance(grid, eps)
    s = np.sign(y); z = np.where(np.diff(s) != 0)[0]
    if len(z)==0:
        return float(grid[np.argmin(np.abs(y))])
    i = z[0]
    x1,x2,y1,y2 = grid[i],grid[i+1],y[i],y[i+1]
    return float(x1 - y1*(x2 - x1)/(y2 - y1))

def time_to_equilibrium(eps, a0=0.86, da_dt=torque_balance,
                        dt=0.5, max_steps=200000, tol=1e-4):
    """
    Euler integrate da/dt = f(a, eps) until |a - a_eq| < tol.
    Units are arbitrary (dt scales them) — OK for relative comparison.
    """
    a_eq = find_a_eq(eps)
    a = a0
    t = 0.0
    for _ in range(max_steps):
        a += da_dt(a, eps)*dt
        t += dt
        if abs(a - a_eq) < tol:
            return t, a_eq
        # reflect if overshoot beyond [0,1]
        if a < 0.0: a = 0.0
        if a > 0.9999: a = 0.9999
    return np.nan, a_eq

# ============================== Main ==============================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", default="data/fig3_params.csv",
                    help="CSV with 'epsilon_coup' (optional)")
    ap.add_argument("--outa", default="figures/Fig4a.pdf",
                    help="output path for Fig4a")
    ap.add_argument("--outb", default="figures/Fig4b.pdf",
                    help="output path for Fig4b")
    ap.add_argument("--polished", action="store_true",
                    help="save under figures/polished/")
    args = ap.parse_args()

    eps_list = load_eps_list(args.params)

    # ---------- Compute series ----------
    taus = []
    aeqs = []
    Ls   = []
    for eps in eps_list:
        tau, aeq = time_to_equilibrium(eps)
        taus.append(tau)
        aeqs.append(aeq)
        Ls.append(L_over_LEdd_from_eps(eps))
    eps_arr = np.array(eps_list)
    taus = np.array(taus); aeqs = np.array(aeqs); Ls = np.array(Ls)

    # ---------- Fig4a: tau_eq vs epsilon ----------
    fig = plt.figure(figsize=(6,4.2), dpi=300); ax = plt.gca()
    ax.semilogx(eps_arr, taus, marker="o", linewidth=2.0)
    ax.set_xlabel(r"$\epsilon_{\mathrm{coup}}$")
    ax.set_ylabel(r"time to equilibrium $\tau_{\rm eq}$ (arb.)")
    ax.grid(True, which="both", alpha=0.25)

    # plausible band (合わせてFig3bと整合)
    ax.axvspan(0.01, 0.10, alpha=0.12,
               label=r"$\epsilon_{\mathrm{coup}}\approx0.01\text{--}0.10$")
    ax.legend(frameon=False, loc="upper right", fontsize=9)

    # 追加・変更:
    ax.set_ylim(bottom=0)                       # y>=0 に固定
    ax.legend(frameon=False, loc="upper left",  # ← 左上へ
          fontsize=9)

    out_a = ensure_out(args.outa, args.polished)
    fig.tight_layout(); fig.savefig(out_a)
    print("[Fig4a] saved ->", out_a)

    # ---------- Fig4b: L/L_Edd vs a_eq ----------
    fig = plt.figure(figsize=(6,4.2), dpi=300); ax = plt.gca()
    ax.plot(aeqs, Ls, linewidth=0, marker="D")
    for x,y,eps in zip(aeqs, Ls, eps_list):
        ax.annotate(f"{eps:g}", (x,y), textcoords="offset points", xytext=(6,4), fontsize=8)
    # 追加:
    ax.axhspan(2.0, 3.0, alpha=0.12, label=r"$L/L_{\rm Edd}\approx2\text{--}3$")
    ax.plot(aeqs, Ls, linestyle="--", linewidth=1.2)  # 傾向線（色は指定しない）

    ax.legend(frameon=False, loc="lower right", fontsize=9)  # 帯の説明を凡例化
    ax.set_xlabel(r"equilibrium spin $a_{\rm eq}$")
    ax.set_ylabel(r"$L/L_{\rm Edd}$")
    ax.grid(True, which="both", alpha=0.25)
    ax.set_xlim(0.85, 1.0)

    out_b = ensure_out(args.outb, args.polished)
    fig.tight_layout(); fig.savefig(out_b)
    print("[Fig4b] saved ->", out_b)

if __name__ == "__main__":
    main()
