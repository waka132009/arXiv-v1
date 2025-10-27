Build:
  latexmk -pdf
  bibtex main
  latexmk -pdf
  latexmk -pdf

Conventions:
  - “In brief:” one-liners + thin rule
  - Ranges: 20--120~keV, $0.3$--$1$~MeV
  - \textemdash (no Unicode dashes)
  - Compactness macros: \ellcrit=30, \ellhard, \ellsoft
