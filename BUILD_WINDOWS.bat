@echo off
setlocal
python -m venv .venv
call .\.venv\Scripts\activate
python -m pip install -U pip
for %%F in (scripts\fig*.py) do python %%F
latexmk -pdf main.tex
echo Done.
