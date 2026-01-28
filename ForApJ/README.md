Build:
  latexmk -pdf v2.1.tex
  bibtex v2.1.bib
  latexmk -pdf v2.1.tex
  latexmk -pdf v2.1.tex

Conventions:
  - “In brief:” one-liners + thin rule
  - Ranges: 20--120~keV, $0.3$--$1$~MeV
  - \textemdash (no Unicode dashes)
  - Compactness macros: \ellcrit=30, \ellhard, \ellsoft
