#!/usr/bin/perl
@default_files = ('main.tex');

$pdflatex = 'pdflatex %O -shell-escape -halt-on-error -file-line-error -synctex=1 %S';
$lualatex = 'lualatex %O -shell-escape -halt-on-error -file-line-error -synctex=1 %S';
$xelatex = 'xelatex %O -shell-escape -halt-on-error -file-line-error -synctex=1 %S';
$bibtex = 'bibtex %O %S';
$biber = 'biber --bblencoding=utf8 -u -U --output_safechars --isbn-normalise --isbn13 %O %S';

$pdf_mode = 4;  # LuaLaTeX
# $pdf_mode = 5;  # XeLaTeX
