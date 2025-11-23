# ApJL SSPE Letter — Submission Package

## Directory Tree

``` bash
ApJL-SSPE-submission
├─ figures/          # final PDFs for submission
├─ scripts/          # Python scripts to regenerate figures
└─ tex/
    ├─ apjL.tex
    ├─ apjL.bib
    └─ figs/         # PDFs used by LaTeX (\includegraphics)
```

- Manuscript: `tex/apjL.tex`
- Bibliography: `tex/apjL.bib`
- Figures (PDF): `figures/*.pdf, tex/figs/*.pdf`
- Figure scripts (reproducible): `scripts/*.py`

## Regenerate figures

```bash
cd scripts
python info_graphic_p1.py
python info_graphic_p2.py
python info_graphic_p3.py
python fig7_spin_triggered_onset.py

# copy PDFs for LaTeX build, then move originals to the final figures/ directory
cp *.pdf ../tex/figs
mv *.pdf ../figures
```

## Dependencies (for scripts):

- Python 3.x
- matplotlib
- numpy


## Build

```bash
cd ../tex
latexmk -pdf -interaction=nonstopmode apjL.tex
```

## Metadata

- Journal: ApJL (submission version)
- OSF registration: DOI 10.17605/OSF.IO/Q7DTH
- ORCID (author): 0009-0008-1891-4579
- Tag (Git): apjl-sspe-v1.0-submission