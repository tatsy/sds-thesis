#!/usr/bin/env python3
"""Prepare CI sources, or check PDFs after latexmk builds them (Python + Poppler)."""
import argparse
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def prepare():
    source = (ROOT / 'main.tex').read_text()
    for language, options in [('ja', ''), ('en', '[english]')]:
        text, count = re.subn(
            r'^\\usepackage(?:\[[^\]\n]*\])?\{sdsthesis\}[^\n]*$',
            lambda _: rf'\usepackage{options}{{sdsthesis}}',
            source, flags=re.MULTILINE,
        )
        assert count == 1, 'Expected one active sdsthesis package declaration'
        (ROOT / f'main_{language}.tex').write_text(text)
        prefix = r'\def\SdsTestEnglish{1}' if language == 'en' else ''
        (ROOT / f'regression_{language}.tex').write_text(
            prefix + '\n' + r'\input{tests/regression.tex}' + '\n'
        )


def pdf_text(name):
    return subprocess.check_output(
        ['pdftotext', '-layout', str(ROOT / f'{name}.pdf'), '-'], text=True
    )


def compact(text):
    return re.sub(r'\s+', '', text)


def check():
    for language in ['ja', 'en']:
        for prefix in ['main', 'regression']:
            name = f'{prefix}_{language}'
            log = (ROOT / f'{name}.log').read_text(errors='replace')
            for error in ['Undefined control sequence', 'undefined references',
                          'undefined citations', 'multiply defined',
                          'Reference format for label type', 'Overfull \\vbox']:
                assert error not in log, f'{name}: {error}'
            text = pdf_text(name)
            cover = compact(text.split('\f')[0])
            if prefix == 'regression':
                assert '2026年3月提出' in cover, f'{name}: Japanese date missing'
                assert ('March,2026' in cover) == (language == 'en'), name
        name = f'regression_{language}'
        pages = pdf_text(name).split('\f')
        first = next(i for i, page in enumerate(pages) if 'ABSTRACT-START' in page)
        last = next(i for i, page in enumerate(pages) if 'ABSTRACT-END' in page)
        assert last > first, f'{name}: abstract did not span pages'
        aux = (ROOT / f'{name}.aux').read_text()
        for label, number in [('sec:body', '1.1'), ('eq:body', '1.1'),
                              ('sec:appendix', 'A.1'), ('subsec:appendix', 'A.1.1'),
                              ('eq:appendix', 'A.1'), ('fig:appendix', 'A.1'),
                              ('tab:appendix', 'A.1'), ('eq:appendix-b', 'B.1')]:
            assert rf'\newlabel{{{label}}}{{{{{number}}}' in aux, (name, label)
        text = compact('\n'.join(pages))
        if language == 'ja':
            expected = ['Forward:付録A;付録A.1;付録A.1.1;式A.1;図A.1;表A.1',
                        'Backward:第1章;第1.1節;式1.1',
                        '定理1', '補題1', '定義1', '命題1', '証明',
                        'Range:式A.1から式A.3', 'ならびに']
        else:
            expected = ['Forward:AppendixA;AppendixA.1;AppendixA.1.1;Equation(A.1);FigureA.1;TableA.1',
                        'Backward:Chapter1;Section1.1;Equation(1.1)',
                        'Theorem1', 'Lemma1', 'Definition1', 'Proposition1', 'Proof']
        for item in expected:
            assert item in text, (name, item)
    print('PASS: dates, bilingual theorems, appendix numbers/references and long abstracts')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'check'])
    args = parser.parse_args()
    prepare() if args.action == 'prepare' else check()
