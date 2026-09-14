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
    for variant, prefix in [('ja', ''), ('en', r'\def\SdsTestEnglish{1}'),
                            ('kuten', r'\def\SdsTestKuten{1}')]:
        (ROOT / f'regression_{variant}.tex').write_text(
            prefix + '\n' + r'\input{tests/regression.tex}' + '\n'
        )


def pdf_text(name):
    return subprocess.check_output(
        ['pdftotext', '-layout', str(ROOT / f'{name}.pdf'), '-'], text=True
    )


def compact(text):
    return re.sub(r'\s+', '', text)


def pdf_info(name):
    return subprocess.check_output(['pdfinfo', str(ROOT / f'{name}.pdf')], text=True)


def check():
    documents = ['main_ja', 'main_en', 'regression_ja', 'regression_en', 'regression_kuten']
    for name in documents:
        log = (ROOT / f'{name}.log').read_text(errors='replace')
        for error in ['Undefined control sequence', 'undefined references',
                      'undefined citations', 'multiply defined',
                      'Reference format for label type', 'Overfull \\vbox',
                      'Token not allowed in a PDF string']:
            assert error not in log, f'{name}: {error}'
        text = pdf_text(name)
        cover = compact(text.split('\f')[0])
        english = name == 'main_en' or name == 'regression_en'
        if name.startswith('regression'):
            assert '2026年3月提出' in cover, f'{name}: Japanese date missing'
            assert ('March,2026' in cover) == english, name
        # PDF/A metadata only with the pdfa option (regression_en declares it)
        pdfa = b'pdfaid:part' in (ROOT / f'{name}.pdf').read_bytes()
        assert pdfa == (name == 'regression_en'), f'{name}: unexpected PDF/A state'
        # punctuation is unified in one direction according to the option
        body = compact(text)
        if name == 'regression_kuten':
            assert '、' in body and '。' in body, f'{name}: kuten punctuation missing'
            assert '，' not in body and '．' not in body, f'{name}: comma punctuation left'
        else:
            assert '，' in body and '．' in body, f'{name}: comma punctuation missing'
            assert '、' not in body and '。' not in body, f'{name}: kuten punctuation left'
    # document metadata comes from the cover information
    for name, title, author in [('main_ja', '卒業・修了論文の書き方', '山田 太郎'),
                                ('main_en', 'How to Write a Graduation Thesis', 'Taro Yamada'),
                                ('regression_ja', '表紙と参照の確認', '山田 太郎'),
                                ('regression_en', 'Regression test', 'Taro Yamada')]:
        info = pdf_info(name)
        assert re.search(rf'^Title:\s+{re.escape(title)}$', info, re.M), (name, 'title')
        if name == 'regression_en':
            # hyperxmp (pdfa) keeps authors only in the XMP packet, not in the Info dictionary
            pdf = (ROOT / f'{name}.pdf').read_bytes()
            assert f'<rdf:li>{author}</rdf:li>'.encode() in pdf, (name, 'author')
        else:
            assert re.search(rf'^Author:\s+{re.escape(author)}$', info, re.M), (name, 'author')
    for language in ['ja', 'en', 'kuten']:
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
        if language != 'en':
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
    print('PASS: dates, metadata, PDF/A option, punctuation, bilingual theorems, '
          'appendix numbers/references and long abstracts')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'check'])
    args = parser.parse_args()
    prepare() if args.action == 'prepare' else check()
