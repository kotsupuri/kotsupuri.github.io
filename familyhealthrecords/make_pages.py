#!/usr/bin/env python3
# サポート・プライバシーポリシー・特商法の表記の Web ページを作る（H-503）。
#
#   使い方: python3 docs/release/site/make_pages.py
#
# 本文の正本はアプリ内の Packages/AppModules/Sources/FeatureSettings/LegalTexts.swift。
# そこから本文・氏名・メールアドレスを取り出して、同じフォルダに index.html・privacy.html・tokushoho.html を書く。
# LegalTexts.swift を直したら、これを流し直して公開先（kotsupuri.github.io の familyhealthrecords/）に置き直す。
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(ROOT, "Packages/AppModules/Sources/FeatureSettings/LegalTexts.swift")

src = open(SRC, encoding="utf-8").read()
name = re.search(r'static let name = "([^"]+)"', src).group(1)
email = re.search(r'static let email = "([^"]+)"', src).group(1)


def body(var):
    m = re.search(r"static var " + var + r': String \{\n\s*"""\n(.*?)\n\s*"""', src, re.S)
    text = re.sub(r"^ {8}", "", m.group(1), flags=re.M)
    return text.replace(r"\(SellerInfo.name)", name).replace(r"\(SellerInfo.email)", email)


CSS = """
:root{--bg:#ffffff;--text:#1d1d1f;--sub:#555;--accent:#C8343C;--line:#e5e5e5}
@media (prefers-color-scheme:dark){:root{--bg:#111;--text:#f2f2f2;--sub:#aaa;--accent:#E0555C;--line:#333}}
body{background:var(--bg);color:var(--text);font-family:-apple-system,"Hiragino Sans","Hiragino Kaku Gothic ProN",sans-serif;line-height:1.8;margin:0}
main{max-width:720px;margin:0 auto;padding:24px 16px 48px}
h1{font-size:1.5rem;color:var(--accent);margin:0 0 8px}
h2{font-size:1.1rem;margin:28px 0 4px;border-bottom:1px solid var(--line);padding-bottom:4px}
p{margin:4px 0 12px;white-space:pre-wrap}
nav a{color:var(--accent);margin-right:16px}
footer{color:var(--sub);font-size:.85rem;margin-top:40px}
"""


def page(title, inner):
    return f"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}｜みんなの病院手帳</title><style>{CSS}</style></head>
<body><main>
<nav><a href="index.html">サポート</a><a href="privacy.html">プライバシーポリシー</a><a href="tokushoho.html">特定商取引法に基づく表記</a></nav>
<h1>{html.escape(title)}</h1>
{inner}
<footer>© 2026 {html.escape(name)}</footer>
</main></body></html>
"""


def sections(text, is_heading):
    out = []
    for block in text.split("\n\n"):
        lines = block.split("\n")
        if is_heading(lines[0]):
            out.append(f"<h2>{html.escape(lines[0])}</h2>")
            if len(lines) > 1:
                out.append(f"<p>{html.escape(chr(10).join(lines[1:]))}</p>")
        else:
            out.append(f"<p>{html.escape(block)}</p>")
    return "\n".join(out)


SUPPORT = f"""<p>みんなの病院手帳は、家族の通院・お薬・体調の記録を、iPhone／iPadの中だけに保存するアプリです。</p>
<h2>お問い合わせ</h2>
<p>ご質問・不具合のご連絡は、次のメールアドレスにお送りください。件名に「みんなの病院手帳」とお書きください（同じ開発者のほかのアプリと共通の窓口です）。
{html.escape(email)}

お送りいただく内容に、ご家族の記録や医療の文書の画像は含めないでください。アプリのバージョン（設定 &gt; アプリについて）と、端末の機種・iOSのバージョン、起きたことと操作の手順をお書きください。</p>
<h2>よくある質問</h2>
<p>Q. 機種変更のとき、記録を移せますか？
A. 設定 &gt; バックアップ から、パスワード付きのバックアップファイルを書き出し、新しい端末で復元してください。データはiCloudやiPhoneのバックアップには含まれません。

Q. パスワードを忘れました。
A. バックアップのパスワードと、端末の中の暗号化の鍵は、開発者も復元できません。

Q. 購入したのに使えません。
A. 設定 &gt; 購入 の「購入を復元」をお試しください。ファミリー共有の家族が購入した場合も、ここで反映されます。

Q. 記録はどこかに送られますか？
A. 送りません。文書の読み取りも端末の中で行います。通信するのは、購入とその復元のときにApp Storeと通信するときだけです。</p>
<h2>ご注意</h2>
<p>本アプリは記録と閲覧のためのものです。診断は行いません。医療上の判断は医師にご相談ください。</p>
"""

pages = {
    "privacy.html": page("プライバシーポリシー", sections(body("privacyPolicy"), lambda l: re.match(r"^\d+\. ", l) is not None)),
    "tokushoho.html": page("特定商取引法に基づく表記", sections(body("commercialTransactions"), lambda l: True)),
    "index.html": page("サポート", SUPPORT),
}
for file_name, content in pages.items():
    with open(os.path.join(HERE, file_name), "w", encoding="utf-8") as f:
        f.write(content)
print("作りました:", ", ".join(pages))
