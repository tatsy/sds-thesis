卒業論文用LaTeXフォーマット
===

# 使い方

## TeX環境の用意

TeXの環境はWindows，MacともにTexLiveをインストールするのがおすすめ (Macの場合はMacTexがTexLiveを利用している)．このテンプレートはLaTeX3を標準として，LuaLaTeX・XeLaTeXのいずれかを使って文書をビルドする．LaTeX3の利用にあたってTeXLiveは2021年以降のバージョンをインストールし，TexLive Managerを使って全てのパッケージを最新にアップデートしておくこと．

## VS Codeの用意

良く分からない人はVisual Studio CodeのLaTeX Workshopを使うことを推奨．このテンプレートはlatexmkというイマドキ (2020年現在) なビルドツールを使うので，latexmkで自動ビルドする設定をしておく．

```json
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

## ショートカット

```json
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

## トラブルシューティング

1. 引用が途中で表示されなくなってしまった
    * 変なキャッシュが残っているせいだと考えられるので、ターミナルを開いて `latexmk -C` と `biber --cache` を実行する

