# Regression checks

Run from the repository root with the same TeX packages and fonts as the template,
plus Python 3 and Poppler (`pdftotext`):

```sh
python3 tests/check.py prepare
latexmk -lualatex main_ja.tex main_en.tex regression_ja.tex regression_en.tex
python3 tests/check.py check
```

The repository `latexmkrc` already selects LuaLaTeX, so `-lualatex` can be omitted
when running from the repository root; it is written out here to avoid falling back
to pdfLaTeX, which `sdsthesis.sty` rejects.

The generated main documents exercise both language modes with logos. The
regression documents use `nologo`, omit English metadata in Japanese mode, and
exercise bilingual theorem environments, forward/backward appendix references,
appendix equation/figure/table numbers, and a multi-page abstract. The checker
inspects the build logs, auxiliary labels and PDF text.

To check XeLaTeX, clean the generated outputs and repeat the build with XeLaTeX.
`latexmkrc` only lists `main.tex` as a default file, so pass the generated wrapper
filenames explicitly:

```sh
latexmk -C main_ja.tex main_en.tex regression_ja.tex regression_en.tex
latexmk -xelatex main_ja.tex main_en.tex regression_ja.tex regression_en.tex
python3 tests/check.py check
```

For the unsupported-engine diagnostic, `pdflatex -halt-on-error regression_ja.tex`
should fail with `Only XeTeX and LuaTeX are supported`.
