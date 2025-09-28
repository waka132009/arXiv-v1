# Transfer Kit — Penrose Handoff (2025-09-21)

**90秒要約**  
- このZIPを **OSF にアップ** → Private → Public → DOI 取得。  
- 論文の *Data availability* に **OSFスナップショット + CHECKSUMS** を1行追記。  
- 専門家へは **このREADMEの要約**と **WHAT_TO_TEST.md** を送付。  
- 図は **PDFベース**（本文と記号統一）。`scripts/` を実行すれば再生成できます。

## 再現手順
### Windows
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
for %F in (scriptsig*.py) do python %F
latexmk -pdf main.tex
```
### Unix
```
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
for f in scripts/fig*.py; do python "$f"; done
latexmk -pdf main.tex
```

## ディレクトリ
- figures/ : PDF図
- scripts/ : 図生成コード
- data/    : サンプルCSV
- WHAT_TO_TEST.md / CHECKSUMS.txt / latexmkrc / CITATION.cff / LICENSE.txt

