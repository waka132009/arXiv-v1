# ApJL SSPE Letter — Submission Package

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

cp *.pdf ../tex/figs
mv *.pdf ../figures
```

## Build

```bash
cd ../tex
latexmk -pdf -interaction=nonstopmode apjL.tex
```

## Metadata

- Journal: ApJL (submission version)
- OSF registration: DOI 10.17605/OSF.IO/Q7DTH
- ORCID (author): 0009-0008-1891-4579
- Tag (Git): apjl-sspe-v1.0-submission # ← 実際のタグ名に合わせて