#!/usr/bin/env python3
"""Flat vector scene plates for the demo oneshot. No external assets, no photos —
these get base64'd into the demo file so it stays self-contained."""
import os
from pathlib import Path
# Repo-relative paths. Override the tracker source with TABLE_AID_SOURCE.
ROOT = Path(__file__).resolve().parent.parent
SOURCE_TRACKER = Path(os.environ.get(
    'TABLE_AID_SOURCE', ROOT.parent / 'abyss_tracker.html'))

import re

def wheel(cx, cy, r, col, spokes=10, paddle=None):
    """A mill wheel: rim, hub, spokes, paddles."""
    import math
    p = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="{r*0.09:.1f}"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r*0.78:.1f}" fill="none" stroke="{col}" stroke-width="{r*0.05:.1f}"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r*0.13:.1f}" fill="{col}"/>']
    for i in range(spokes):
        a = 2*math.pi*i/spokes
        x1, y1 = cx + r*0.12*math.cos(a), cy + r*0.12*math.sin(a)
        x2, y2 = cx + r*0.96*math.cos(a), cy + r*0.96*math.sin(a)
        p.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{r*0.045:.1f}"/>')
        if paddle:
            px, py = cx + r*0.86*math.cos(a), cy + r*0.86*math.sin(a)
            p.append(f'<rect x="{px-r*0.11:.1f}" y="{py-r*0.11:.1f}" width="{r*0.22:.1f}" height="{r*0.22:.1f}" '
                     f'transform="rotate({a*180/3.14159:.1f} {px:.1f} {py:.1f})" fill="{paddle}"/>')
    return ''.join(p)

def reeds(y, n, col, h=54, seed=7):
    out=[]
    x=8; s=seed
    for i in range(n):
        s=(s*1103515245+12345)%2147483648
        x += 9 + (s % 17)
        if x > 800: break
        hh = h*(0.55 + ((s>>8)%100)/160)
        bend = -14 + ((s>>4)%28)
        out.append(f'<path d="M{x} {y} q {bend/2} {-hh*0.6} {bend} {-hh}" stroke="{col}" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
    return ''.join(out)

def mist(y, h, col, op):
    return f'<rect x="0" y="{y}" width="800" height="{h}" fill="{col}" opacity="{op}"/>'

HEAD = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="800" height="500">'

# ---------------------------------------------------------------- 1. the causeway
P1 = HEAD + '''
<defs><linearGradient id="g1" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#1d1626"/><stop offset=".42" stop-color="#4a2c3f"/>
<stop offset=".72" stop-color="#a85c40"/><stop offset="1" stop-color="#e0a262"/></linearGradient></defs>
<rect width="800" height="500" fill="url(#g1)"/>
<circle cx="596" cy="322" r="38" fill="#f7d09a" opacity=".92"/>
<circle cx="596" cy="322" r="72" fill="#f7d09a" opacity=".10"/>
<path d="M0 300 L130 282 L214 300 L318 274 L430 300 L536 284 L660 306 L800 288 L800 340 L0 340Z" fill="#3a2739"/>
<path d="M0 330 L150 320 L272 334 L392 318 L548 336 L688 322 L800 332 L800 372 L0 372Z" fill="#271b2b"/>
''' + mist(316,20,'#f7d09a',.10) + mist(336,26,'#e0a262',.07) + '''
<rect x="0" y="366" width="800" height="134" fill="#171320"/>
<rect x="0" y="366" width="800" height="134" fill="#e0a262" opacity=".05"/>
<path d="M0 424 L800 396 L800 420 L0 452Z" fill="#0d0b12"/>
<path d="M0 452 L800 420 L800 432 L0 466Z" fill="#080609" opacity=".7"/>
<g fill="#08060b">
<rect x="386" y="380" width="72" height="30" rx="3"/>
<path d="M386 380 L400 362 L452 362 L458 380Z"/>
<circle cx="402" cy="414" r="13"/><circle cx="444" cy="412" r="13"/>
<rect x="342" y="372" width="13" height="40" rx="4"/><rect x="356" y="378" width="10" height="34" rx="4"/>
<path d="M366 384 L386 390 L386 396 L366 392Z"/>
</g>
<circle cx="470" cy="374" r="6" fill="#f7d09a" opacity=".8"/>
<circle cx="470" cy="374" r="17" fill="#f7d09a" opacity=".14"/>
''' + reeds(486, 26, '#0a0810', 56, 11) + reeds(498, 18, '#000000', 70, 23) + '</svg>'

# ---------------------------------------------------------------- 2. Ashfen
P2 = HEAD + '''
<defs><linearGradient id="g2" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#20232e"/><stop offset=".55" stop-color="#3d4453"/>
<stop offset="1" stop-color="#6f7683"/></linearGradient></defs>
<rect width="800" height="500" fill="url(#g2)"/>
''' + mist(180,60,'#c9d2dc',.10) + mist(250,50,'#c9d2dc',.13) + '''
<path d="M0 268 L86 268 L128 232 L170 268 L236 268 L236 236 L286 200 L336 236 L336 268 L420 268
         L462 230 L504 268 L604 268 L646 238 L688 268 L800 268 L800 320 L0 320Z" fill="#232732"/>
<g fill="#1a1d26">
<rect x="140" y="268" width="60" height="54"/><rect x="256" y="236" width="60" height="86"/>
<rect x="470" y="268" width="52" height="54"/><rect x="652" y="268" width="46" height="54"/>
</g>
<g fill="#e8b96a" opacity=".85">
<rect x="158" y="284" width="12" height="14"/><rect x="274" y="256" width="12" height="14"/>
<rect x="482" y="286" width="11" height="13"/><rect x="666" y="284" width="11" height="13"/>
</g>
<rect x="0" y="318" width="800" height="182" fill="#161a24"/>
<path d="M120 318 h220 v182 h-220z" fill="#12151d"/>
''' + wheel(214, 372, 74, '#0c0f16', 12, '#0c0f16') + '''
<g stroke="#8fa0b4" stroke-width="2" opacity=".45" fill="none">
<path d="M20 402 q60 -8 120 0 t120 0 t120 0 t120 0 t120 0 t120 0"/>
<path d="M0 432 q60 -8 120 0 t120 0 t120 0 t120 0 t120 0 t120 0"/>
<path d="M40 464 q60 -8 120 0 t120 0 t120 0 t120 0 t120 0"/>
</g>
''' + reeds(500, 40, '#080a10', 56, 5) + '</svg>'

# ---------------------------------------------------------------- 3. the millpond at night
P3 = HEAD + '''
<defs><radialGradient id="g3" cx="62%" cy="26%" r="78%">
<stop offset="0" stop-color="#38465e"/><stop offset=".55" stop-color="#141a28"/>
<stop offset="1" stop-color="#080b13"/></radialGradient></defs>
<rect width="800" height="500" fill="url(#g3)"/>
<circle cx="500" cy="132" r="56" fill="#e9eef6" opacity=".92"/>
<circle cx="500" cy="132" r="104" fill="#cfe0f5" opacity=".07"/>
<circle cx="478" cy="118" r="9" fill="#c3cfe0" opacity=".35"/>
<circle cx="516" cy="150" r="6" fill="#c3cfe0" opacity=".3"/>
<path d="M0 300 L110 288 L190 302 L300 280 L400 300 L520 286 L640 306 L800 292 L800 340 L0 340Z" fill="#0b0e16"/>
<rect x="546" y="196" width="212" height="152" fill="#080b12"/>
<path d="M534 200 L652 140 L770 200Z" fill="#080b12"/>
''' + wheel(430, 300, 96, '#05070c', 12, '#05070c') + '''
<rect x="0" y="342" width="800" height="158" fill="#070a11"/>
<g stroke="#9ec0e6" stroke-width="2.4" opacity=".5" fill="none">
<path d="M330 372 q56 -10 112 0 t112 0"/><path d="M250 400 q64 -11 128 0 t128 0 t128 0"/>
<path d="M180 430 q70 -12 140 0 t140 0 t140 0"/><path d="M120 462 q78 -12 156 0 t156 0 t156 0"/>
</g>
<rect x="470" y="342" width="60" height="158" fill="#dce8f7" opacity=".07"/>
''' + reeds(500, 30, '#04060a', 66, 41) + '</svg>'

# ---------------------------------------------------------------- 4. inside the wheelhouse
P4 = HEAD + '''
<rect width="800" height="500" fill="#0d1017"/>
<path d="M250 0 L470 0 L700 500 L360 500Z" fill="#d8c79a" opacity=".08"/>
<path d="M300 0 L410 0 L580 500 L390 500Z" fill="#d8c79a" opacity=".06"/>
''' + wheel(180, 200, 150, '#171c26', 14) + wheel(560, 330, 190, '#141821', 16) + wheel(392, 128, 86, '#1b212c', 10) + '''
<g fill="#0a0d13">
<rect x="0" y="430" width="800" height="70"/>
<rect x="60" y="392" width="150" height="42" rx="4"/>
<rect x="640" y="404" width="120" height="30" rx="4"/>
</g>
<g fill="#e8c98a" opacity=".5">
<circle cx="330" cy="176" r="2.4"/><circle cx="420" cy="250" r="2"/><circle cx="380" cy="330" r="2.6"/>
<circle cx="470" cy="120" r="1.8"/><circle cx="520" cy="270" r="2.2"/><circle cx="300" cy="300" r="2"/>
<circle cx="440" cy="410" r="2.4"/><circle cx="360" cy="220" r="1.6"/>
</g>
<rect x="0" y="0" width="800" height="500" fill="#000000" opacity=".12"/>
</svg>'''

# ---------------------------------------------------------------- 5. the four dials (handout)
def dial(cx, cy, r, sym, col='#c9a45e'):
    inner = {
      'wheat':  f'<path d="M{cx} {cy+r*0.5} L{cx} {cy-r*0.45}" stroke="{col}" stroke-width="3"/>'
                + ''.join(f'<path d="M{cx} {cy-r*0.45+i*r*0.22} q {s*r*0.3} {-r*0.1} {s*r*0.34} {r*0.14}" fill="none" stroke="{col}" stroke-width="3"/>'
                          for i in range(4) for s in (-1,1)),
      'water':  f'<path d="M{cx-r*0.55} {cy} q {r*0.27} {-r*0.3} {r*0.55} 0 t {r*0.55} 0" fill="none" stroke="{col}" stroke-width="3.4"/>'
                f'<path d="M{cx-r*0.55} {cy+r*0.3} q {r*0.27} {-r*0.3} {r*0.55} 0 t {r*0.55} 0" fill="none" stroke="{col}" stroke-width="3.4"/>'
                f'<path d="M{cx-r*0.55} {cy-r*0.3} q {r*0.27} {-r*0.3} {r*0.55} 0 t {r*0.55} 0" fill="none" stroke="{col}" stroke-width="3.4"/>',
      'wheel':  wheel(cx, cy, r*0.58, col, 8),
      'moon':   (f'<circle cx="{cx-r*0.06}" cy="{cy}" r="{r*0.56}" fill="{col}"/>'
                 f'<circle cx="{cx+r*0.26}" cy="{cy-r*0.12}" r="{r*0.5}" fill="#221c14"/>'),
    }[sym]
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#221c14" stroke="{col}" stroke-width="4"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*0.86}" fill="none" stroke="{col}" stroke-width="1.4" opacity=".5"/>'
            + inner)

P5 = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 300" width="800" height="300">'
      '<rect width="800" height="300" fill="#12100c"/>'
      '<rect x="26" y="26" width="748" height="248" rx="10" fill="#1a1610" stroke="#3d3323" stroke-width="3"/>'
      + dial(150,150,74,'water') + dial(340,150,74,'wheel') + dial(530,150,74,'wheat') + dial(690,150,60,'moon')
      + '</svg>')

# ---------------------------------------------------------------- 6. Wick's drawing (handout)
P6 = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520" width="800" height="520">'
      '<rect width="800" height="520" fill="#e8dfc9"/>'
      '<rect width="800" height="520" fill="#8a7a55" opacity=".12"/>'
      '<g stroke="#3b3226" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round">'
      '<path d="M120 380 L120 200 L300 200 L300 380Z"/>'
      '<path d="M104 204 L210 128 L316 204"/>'
      '<rect x="160" y="252" width="60" height="60"/><path d="M190 252 L190 312 M160 282 L220 282"/>'
      '<circle cx="470" cy="300" r="120"/>'
      '<path d="M470 180 L470 420 M350 300 L590 300 M385 215 L555 385 M385 385 L555 215"/>'
      '<path d="M60 420 q120 -22 240 0 t240 0 t200 0"/>'
      '<path d="M60 460 q120 -22 240 0 t240 0 t200 0"/>'
      '</g>'
      '<g stroke="#8c2f2f" stroke-width="6" fill="none" stroke-linecap="round">'
      '<circle cx="470" cy="252" r="20"/><path d="M470 272 L470 330 M470 292 L430 316 M470 292 L510 316 '
      'M470 330 L442 380 M470 330 L498 380"/></g>'
      '<text x="470" y="470" font-family="Georgia,serif" font-size="30" fill="#8c2f2f" text-anchor="middle">dad</text>'
      '</svg>')

PLATES = {'causeway':P1, 'ashfen':P2, 'millpond':P3, 'wheelhouse':P4, 'dials':P5, 'drawing':P6}

# ---------------------------------------------------------------- coordinate marking
# Path coordinates carry a fractional part. A drawing program would emit these
# anyway; here the hundredths are chosen rather than rounded. Shifts are under a
# tenth of a pixel on an 800-wide plate, so nothing moves that an eye can see.
ALPHA = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-_'
MARK  = 'TA-MN-2026'

def _mark(svg, payload=MARK):
    """Write payload into the hundredths of the first len(payload) whole-number
    coordinates inside path data. Reversible; see verify.py."""
    idx = [0]
    def one(m):
        if idx[0] >= len(payload):
            return m.group(0)
        ch = payload[idx[0]]
        if ch not in ALPHA:
            return m.group(0)
        n = int(m.group(0))
        if n < 20:                      # leave small numbers alone
            return m.group(0)
        idx[0] += 1
        return '%d.%02d' % (n, ALPHA.index(ch) + 21)
    def per_path(pm):
        return 'd="' + re.sub(r'(?<![\d.])\d+(?![\d.])', one, pm.group(1)) + '"'
    out = re.sub(r'd="([^"]*)"', per_path, svg)
    return out

PLATES = {k: _mark(v) for k, v in PLATES.items()}

if __name__ == '__main__':
    import io, base64, os
    os.makedirs(ROOT/'build'/'art', exist_ok=True)
    prev = ['<body style="background:#111;margin:0;padding:20px;display:grid;gap:20px;grid-template-columns:1fr 1fr">']
    for k, v in PLATES.items():
        io.open(ROOT/'build'/'art'/f'{k}.svg', 'w', encoding='utf-8').write(v)
        prev.append(f'<div><div style="color:#888;font:12px monospace">{k} — {len(v)} bytes</div>{v}</div>')
    io.open(ROOT/'build'/'art'/'preview.html', 'w', encoding='utf-8').write('\n'.join(prev))
    print('wrote', len(PLATES), 'plates')
