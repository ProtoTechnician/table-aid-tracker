#!/usr/bin/env python3
"""Regenerate table_aid_blank.html from abyss_tracker.html.
Empties every content constant, rebrands, and adds the welcome panel.
Run this after ANY change to abyss_tracker.html so the two stay in sync."""
import os
from pathlib import Path
# Repo-relative paths. Override the tracker source with TABLE_AID_SOURCE.
ROOT = Path(__file__).resolve().parent.parent
SOURCE_TRACKER = Path(os.environ.get(
    'TABLE_AID_SOURCE', ROOT.parent / 'abyss_tracker.html'))

import io, re, sys

SRC=str(SOURCE_TRACKER)
DST=str(ROOT/'tracker'/'table_aid_blank.html')
s=io.open(SRC,encoding='utf-8').read()
misses=[]

def empty_const(name, open_ch, close_ch):
    """Blank out  const NAME=[ ... ];  keeping the surrounding comment."""
    global s
    start = s.find('const %s=%s' % (name, open_ch))
    if start < 0:
        misses.append('const '+name); return
    i = s.index(open_ch, start)
    depth=0
    j=i
    while j < len(s):
        c=s[j]
        if c==open_ch: depth+=1
        elif c==close_ch:
            depth-=1
            if depth==0: break
        j+=1
    s = s[:i+1] + '\n' + s[j:]

for n in ['MONSTERS','ENCOUNTERS','SCENES','CHAPTERS','DEFAULT_TOOLS','DEFAULT_CARDS']:
    empty_const(n,'[',']')
for n in ['KITS','TRIG','MAPS']:
    empty_const(n,'{','}')

def rep(old,new,label,count=1):
    global s
    if old not in s: misses.append(label); return
    s=s.replace(old,new,count)

# The public blank never carries a per-copy build id, whatever the source had.
import re as _re
s=_re.sub(r"BUILD=\{v:'([^']*)',b:'[0-9a-f]*'\}", lambda m:"BUILD={v:'%s',b:'0000000'}"%m.group(1), s)

rep('<title>Abyss Table — Combat &amp; Session Tracker</title>',
    '<title>Table Aid — your session, in one tab</title>','title')
rep('<span class="bname" id="bname">ABYSS TABLE</span>',
    '<span class="bname" id="bname">TABLE AID</span>','bname')
rep('<span class="bsub" id="bsub">THE NINTH STEP</span>',
    '<span class="bsub" id="bsub">UNTITLED CAMPAIGN</span>','bsub')
rep("    title:'Abyss Table', sub:'The Ninth Step',",
    "    title:'Table Aid', sub:'Untitled campaign',",'seed title')
rep("    party:{size:4,level:10,items:{rare:4},itemPct:{}},",
    "    party:{size:4,level:10,items:{},itemPct:{}},",'seed party')
rep("a.download='abyss-session.json'; a.click(); markSaved();",
    "a.download='table-aid-session.json'; a.click(); markSaved();",'save name')
rep("toast('Saved <b>abyss-session.json</b> to your downloads.');",
    "toast('Saved <b>table-aid-session.json</b> to your downloads.');",'save toast')
rep("""  E.style.display=S.combatants.length?'none':'block';
  const cur=S.combatants[S.turn];""",
"""  E.style.display=S.combatants.length?'none':'block';
  const wel=document.getElementById('welcome');
  if(wel)wel.style.display=(!S.combatants.length&&!MON().length)?'block':'none';
  const cur=S.combatants[S.turn];""",'welcome toggle')

WELCOME = """    <div class="card" id="welcome" style="max-width:820px;margin:10px auto 0;border-left:3px solid var(--teal)">
      <h2 class="sec">Empty tracker &mdash; two ways in</h2>
      <div class="note" style="line-height:1.8;margin-bottom:14px">
        <b style="color:var(--teal)">The fast way.</b> Write your adventure as plain text &mdash; however you already write it &mdash;
        and hand it to Claude with the authoring guide. It fills every tab in and marks anything it invented in red
        so you can check its work, then hands you a block of JSON. Paste that into
        <b>&#8942; top right &rarr; Paste a build from Claude</b>. <a href="build.html" style="color:var(--teal)">How that works &rarr;</a>
        &nbsp;&middot;&nbsp; <a href="demo.html" style="color:var(--teal)">See a filled-in example &rarr;</a>
      </div>
      <div class="note" style="line-height:1.8;margin-bottom:14px">
        <b style="color:var(--amber)">The hands-on way.</b> Build it here yourself:
      </div>
      <ol class="note" style="line-height:1.95;padding-left:20px;margin:0">
        <li><b>&#8942; top right</b> &mdash; name your campaign, set party size and level, pick a theme. The moon/sun/gear switches dark, light or system.</li>
        <li><b>Party</b> &mdash; add your players. Click an HP bar to roll hit points per level.</li>
        <li><b>Bestiary</b> &mdash; <b>+ New creature</b> opens 118 templates that rescale to any CR. Every field has a <b>&#8942; library</b> button.</li>
        <li><b>Encounters</b> &mdash; build a fight and it rates the difficulty against your party.</li>
        <li><b>Story</b> &mdash; chapters hold segments. One segment per beat, with times so the pacing clock works, and key beats you can read at a glance.</li>
        <li><b>Tools</b> &mdash; a dice roller, your campaign's homebrew rules, and the handouts and puzzles you throw onto the players' screen.</li>
        <li><b>Players</b> in the header opens a second window for the other screen &mdash; order of battle, battle map, or whichever handout you pick.</li>
        <li><b>Save</b> often. One file holds everything. Nothing leaves this browser.</li>
      </ol>
    </div>
"""
# drop the welcome card in at the end of the Initiative page
marker = '''  </div></section>

  <!-- ============ PARTY ============ -->'''
if marker in s:
    s = s.replace(marker, WELCOME + marker, 1)
else:
    misses.append('welcome insert')

io.open(DST,'w',encoding='utf-8').write(s)
print('wrote', DST, len(s), 'bytes; misses:', misses)
