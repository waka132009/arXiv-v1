# Figures Starter Kit (PDF-first, math-consistent)

This kit helps you **rebuild all figures with LaTeX-style math labels** so PNG artefacts disappear.
Default output: **PDF (vector)** + matching **PNG (300 dpi)**.

## Quick start
1. Install Python 3.10+ and matplotlib.
   ```bash
   python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```
2. Put/replace your raw data in `data/` (CSV/TSV/NPY/etc.).
3. Edit or add scripts in `scripts/` (copy `fig1_example.py` as a template).
4. Run:
   - macOS/Linux: `bash make_figs.sh`
   - Windows: `./make_figs.ps1`
5. In LaTeX, prefer the **PDF** figures:
   ```tex
   \begin{figure}
     \centering
     \includegraphics[width=\linewidth]{figures/fig1.pdf}
     \caption{Peak $L_{\rm tot}/L_{\rm Edd}$ vs. $a_\ast$; $\mathrm{Fe\,K}\alpha$ lag, etc.}
   \end{figure}
   ```

## Notes
- All labels use mathtext (`$...$`) and Computer Modern-like fonts for consistency with AASTeX.
- If you _must_ ship PNGs, they are emitted alongside the PDFs at 300 dpi.
- Add new figures by creating `scripts/fig_<name>.py`. The runner discovers and executes `main()` in each script.
