#!/usr/bin/env python3
"""Render the Table Aid manual into a print-ready PDF with figures."""
import os
from pathlib import Path
# Repo-relative paths. Override the tracker source with TABLE_AID_SOURCE.
ROOT = Path(__file__).resolve().parent.parent
SOURCE_TRACKER = Path(os.environ.get(
    'TABLE_AID_SOURCE', ROOT.parent / 'abyss_tracker.html'))

import asyncio, re, base64, io, os
from pathlib import Path
import markdown

SRC = ROOT/'docs'/'Table_Aid_Manual.md'
HTML_OUT = ROOT/'build'/'manual.html'
PDF_OUT = ROOT/'docs'/'Table_Aid_Manual.pdf'
FIGS = ROOT/'docs'/'figs'

body_md = SRC.read_text(encoding='utf-8')
html_body = markdown.markdown(body_md, extensions=['tables','sane_lists','attr_list','fenced_code'])

# figures: <p><img src=figs/x.png alt=caption></p>  ->  <figure>
def fig(m):
    src, alt = m.group(1), m.group(2)
    p = FIGS / Path(src).name
    if not p.exists():
        return ''
    b64 = base64.b64encode(p.read_bytes()).decode()
    return (f'<figure><img src="data:image/png;base64,{b64}" alt="">'
            f'<figcaption>{alt}</figcaption></figure>')
html_body = re.sub(r'<p><img alt="([^"]*)" src="([^"]+)"\s*/?></p>',
                   lambda m: fig(type('M',(),{'group':lambda s,i:(m.group(2) if i==1 else m.group(1))})()),
                   html_body)

CSS = """
@page { size: A4; margin: 17mm 16mm 18mm 16mm; }
:root{
  --ink:#1b2027; --muted:#4a5665; --dim:#6f7d8c; --line:#d5dde5;
  --teal:#1d6478; --teal-l:#eaf4f7; --amber:#8a5a12; --amber-l:#fbf3e4;
  --red:#9a2f38; --red-l:#fbeceE; --panel:#f5f8fa;
  --mono:"SF Mono",Menlo,Consolas,monospace;
}
*{box-sizing:border-box}
body{font:9.9pt/1.62 Georgia,"Times New Roman",serif;color:var(--ink);margin:0}
h1,h2,h3,h4{font-family:-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;line-height:1.2}
h2{font-size:15.5pt;margin:20pt 0 11pt;padding-bottom:6pt;border-bottom:2px solid var(--teal);
   color:var(--teal);letter-spacing:.01em;page-break-after:avoid;break-after:avoid}
h2:first-of-type{margin-top:0}
h3{font-size:11.6pt;margin:16pt 0 5pt;color:var(--ink);page-break-after:avoid}
p{margin:0 0 8pt}
strong{color:#0f141a}
em{color:var(--muted)}
ul,ol{margin:0 0 9pt;padding-left:16pt}
li{margin-bottom:3.5pt}
code{font-family:var(--mono);font-size:8.4pt;background:var(--panel);border:1px solid var(--line);
  border-radius:3px;padding:0 3px;color:var(--amber)}
hr{border:0;border-top:1px solid var(--line);margin:14pt 0}
pre{background:#f5f8fa;border:1px solid var(--line);border-left:3px solid var(--teal);
  border-radius:5px;padding:9pt 12pt;margin:9pt 0;overflow:hidden;page-break-inside:avoid}
pre code{font-family:var(--mono);font-size:8.3pt;line-height:1.55;color:#23303c;background:none;
  border:none;padding:0;white-space:pre-wrap}
a{color:var(--teal);text-decoration:none}

blockquote{margin:11pt 0;padding:9pt 13pt;background:var(--teal-l);
  border:1px solid #cfe3e9;border-left:3px solid var(--teal);border-radius:5px;
  page-break-inside:avoid}
blockquote p{margin:0 0 6pt}
blockquote p:last-child{margin:0}

table{width:100%;border-collapse:collapse;margin:10pt 0 12pt;font-size:8.9pt;
  font-family:-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;page-break-inside:avoid}
th{text-align:left;background:var(--panel);color:var(--muted);font-size:7.4pt;letter-spacing:.09em;
  text-transform:uppercase;padding:5pt 7pt;border-bottom:1.5px solid var(--line);font-weight:700}
td{padding:5pt 7pt;border-bottom:1px solid #e7edf2;vertical-align:top;color:var(--ink)}
td:first-child{white-space:nowrap;font-weight:600}
table td code{font-size:8.2pt}

figure{margin:12pt 0 14pt;page-break-inside:avoid;text-align:center}
figure img{width:100%;border:1px solid var(--line);border-radius:5px;display:block}
figcaption{font-size:8.2pt;color:var(--dim);margin-top:5pt;font-style:italic;
  font-family:-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;text-align:left}

/* cover */
.cover{height:243mm;display:flex;flex-direction:column;justify-content:center;
  page-break-after:always;text-align:left}
.cover .kick{font-family:-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;font-size:8.5pt;
  letter-spacing:.28em;text-transform:uppercase;color:var(--amber);margin-bottom:14pt}
.cover h1{font-size:40pt;line-height:1.02;margin:0 0 6pt;letter-spacing:-.02em;color:var(--teal)}
.cover .sub{font-size:15pt;color:var(--muted);margin:0 0 22pt;font-style:italic}
.cover .rule{height:3px;background:var(--teal);width:76mm;margin:0 0 22pt}
.cover .meta{font-family:-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;font-size:9.4pt;
  color:var(--muted);line-height:1.9}
.cover .meta b{color:var(--ink)}
.cover .foot{margin-top:auto;font-size:8.4pt;color:var(--dim);
  font-family:-apple-system,"Segoe UI",Helvetica,Arial,sans-serif}
.toc{font-family:-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;font-size:9.4pt;
  columns:2;column-gap:14mm;margin-top:6pt}
.toc div{margin-bottom:4.5pt;break-inside:avoid;color:var(--muted)}
.toc b{color:var(--ink)}
"""

COVER = """
<div class="cover">
  <div class="kick">A Dungeon Master's screen in one browser tab</div>
  <h1>Table Aid</h1>
  <div class="sub">What it does, how to use it, and how to build one from your own notes</div>
  <div class="rule"></div>
  <div class="meta">
    <b>One HTML file.</b> No install, no account, no internet.<br>
    <b>D&amp;D 2024 rules.</b> You roll the dice; it does the arithmetic.<br>
    <b>Your campaign stays on your machine.</b> Save writes a file. That is the whole system.
  </div>
  <div class="toc" style="margin-top:26pt">
    <div><b>1</b> &nbsp;What this is</div>
    <div><b>2</b> &nbsp;Five minutes to your first fight</div>
    <div><b>3</b> &nbsp;The header</div>
    <div><b>4</b> &nbsp;Initiative</div>
    <div><b>5</b> &nbsp;Party</div>
    <div><b>6</b> &nbsp;Bestiary</div>
    <div><b>7</b> &nbsp;Encounters</div>
    <div><b>8</b> &nbsp;Story</div>
    <div><b>9</b> &nbsp;Tools</div>
    <div><b>10</b> &nbsp;The players' screen</div>
    <div><b>11</b> &nbsp;Setting Claude up &mdash; once</div>
    <div><b>12</b> &nbsp;From your notes to the tracker</div>
    <div><b>13</b> &nbsp;Checking Claude's work</div>
    <div><b>14</b> &nbsp;Asking for changes</div>
    <div><b>15</b> &nbsp;Saving, undo and backups</div>
    <div><b>16</b> &nbsp;Keyboard</div>
    <div><b>17</b> &nbsp;Things that will bite you</div>
    <div><b>A</b> &nbsp;Map tiles</div>
    <div><b>B</b> &nbsp;Editor syntax</div>
  </div>
  <div class="foot">Unofficial fan tool. Not affiliated with Wizards of the Coast.<br>
    Every screenshot is taken from the demonstration file, <i>The Miller's Debt</i>.</div>
</div>
"""

HTML = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>Table Aid — manual</title><style>{CSS}</style></head>
<body>{COVER}{html_body}</body></html>"""

HTML_OUT.write_text(HTML, encoding='utf-8')

async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        await pg.goto('file://' + str(HTML_OUT))
        await pg.wait_for_timeout(1200)
        await pg.pdf(path=str(PDF_OUT), format='A4', print_background=True,
                     margin={'top':'17mm','bottom':'18mm','left':'16mm','right':'16mm'},
                     display_header_footer=True,
                     header_template='<div></div>',
                     footer_template='<div style="width:100%;font-size:7.5pt;color:#8a97a5;'
                                     'font-family:-apple-system,Segoe UI,Helvetica,sans-serif;'
                                     'padding:0 16mm;display:flex;justify-content:space-between">'
                                     '<span>Table Aid — manual</span>'
                                     '<span class="pageNumber"></span></div>')
        await b.close()
    print('wrote', PDF_OUT, PDF_OUT.stat().st_size // 1024, 'KB')

asyncio.run(main())
