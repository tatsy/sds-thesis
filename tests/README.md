# Regression checks

Run from the repository root with the same TeX packages and fonts as the template,
plus Python 3 and Poppler (`pdftotext`):

```sh
python3 tests/check.py prepare
latexmk main_ja.tex main_en.tex regression_ja.tex regression_en.tex
python3 tests/check.py check
```

The generated main documents exercise both language modes with logos. The
regression documents use `nologo`, omit English metadata in Japanese mode, and
exercise bilingual theorem environments, forward/backward appendix references,
appendix equation/figure/table numbers, and a multi-page abstract. The checker
inspects the build logs, auxiliary labels and PDF text.

To check XeLaTeX, clean the generated outputs with `latexmk -C` and repeat the
build with `latexmk -xelatex`.

For the unsupported-engine diagnostic, `pdflatex -halt-on-error regression_ja.tex`
should fail with `Only XeTeX and LuaTeX are supported`.
