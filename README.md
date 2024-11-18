卒業論文用LaTeXフォーマット
===========================

事前準備
---------

TeXの環境はWindows、MacともにTexLiveをインストールするのがおすすめ (Macの場合はMacTexがTexLiveを利用している)。このテンプレートはLaTeX3を標準として、LuaLaTeX・XeLaTeXのいずれかを使って文書をビルドする。
LaTeX3の利用にあたってTeXLiveは2021年以降のバージョンをインストールし、TexLive Managerを使って全てのパッケージを最新にアップデートしておくこと。

### フォントのインストール

フォントに関してはGoogle NotoフォントとSTIX Twoフォントを使用しています。事前に各自の環境にインストールしてください。なお、日本語の部分には斜体は使えないので注意してください。

-Noto Sans JP: <https://fonts.google.com/noto/specimen/Noto+Sans+JP>
-Noto Serif JP: <https://fonts.google.com/noto/specimen/Noto+Serif+JP>
-STIX Two Text: <https://fonts.google.com/specimen/STIX+Two+Text>

### Overleafの使用

Overleafを使用する場合は、本リポジトリをZIPファイルでダウンロードし、直接Overleafにアップロードする。コンパイラをLuaLaTeXあるいはXeLaTeXに設定すれば文書がビルド出来る。

### LuaLaTeXとXeLaTeXの違い

- LuaLaTeXの方が日本語は正しく表示される (例えば、行の先頭に小文字がこない)が、コンパイルに時間がかかる。
- XeLaTeXの方がコンパイルは早いが、日本語の表示があまり正しくない。

VS Codeの用意
-------------

良く分からない人はVisual Studio CodeのLaTeX Workshopを使うことを推奨。
このテンプレートはlatexmkというイマドキ (2020年現在) なビルドツールを使うのでlatexmkで自動ビルドする設定をしておく。

### VSCode自体の設定 (settings.json)

```jsonc
{
    // LaTeX
    "latex-workshop.view.pdf.viewer": "tab",
    "latex-workshop.view.pdf.zoom": "page-width",
    "latex-workshop.message.badbox.show": false,
    "latex-workshop.latex.autoBuild.run": "onFileChange",
    "latex-workshop.latex.recipes": [
        {
            "name": "latexmk",
            "tools": [
                "latexmk"
            ]
        }
    ],
    "latex-workshop.latex.tools": [
        {
            "name": "latexmk",
            "command": "latexmk",
            "args": [
                "-f",
                "-synctex=1",
                "-interaction=nonstopmode",
                "-file-line-error",
                "%DOC%"
            ]
        }
    ],
    "window.zoomLevel": 0
}
```

### ショートカットの設定 (keybindings.json)

```jsonc
[
    // LaTeX
    {
        "key": "cmd+alt+c",
        "command": "latex-workshop.clean",
        "when": "resourceLangId == latex"
    },
    {
        "key": "cmd+alt+k",
        "command": "latex-workshop.kill",
        "when": "resourceLangId == latex"
    },
    {
        "key": "cmd+alt+s",
        "command": "latex-workshop.synctex",
        "when": "resourceLangId == latex"
    }
]
```

トラブルシューティング
----------------------

1. 引用が途中で表示されなくなってしまった
    - 変なキャッシュが残っているせいだと考えられるので、ターミナルを開いて `latexmk -C` と `biber --cache` を実行する

免責事項
--------

本テンプレートを用いた事により発生する如何なる問題についても作者は責任を負いません。各自の責任で使用の上、最終版を提出する前には、必要事項が正しく記載されているかを確認してください。

Copyright
---------

No License 2024 (c) Tatsuya Yatagawa
