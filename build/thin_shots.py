#!/usr/bin/env python3
"""What the same adventure looks like when the brief was two sentences.
Used for the thin-vs-thorough comparison in the manual."""
import os
from pathlib import Path
# Repo-relative paths. Override the tracker source with TABLE_AID_SOURCE.
ROOT = Path(__file__).resolve().parent.parent
SOURCE_TRACKER = Path(os.environ.get(
    'TABLE_AID_SOURCE', ROOT.parent / 'abyss_tracker.html'))

import asyncio, http.server, socketserver, threading, functools, json, io

PORT = 8953
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT/'tracker'))
httpd = socketserver.TCPServer(("", PORT), H)
threading.Thread(target=httpd.serve_forever, daemon=True).start()

def ai(note):
    return {"ai": True, "aiOk": False, "aiNote": note}

SC = lambda a,b,t,keys,note,mark: dict(ch="c1", a=a, b=b, t=t, keys=keys, note=note, imgs=[],
                                       **(ai(mark) if mark else {}))

THIN = {"tableAidBuild":1,"data":{
 "title":"The Haunted Mill","sub":"Built from a two-sentence brief",
 "theme":{"name":"slate","mode":"dark"},
 "party":{"size":4,"level":3,"items":{},"itemPct":{}},
 "playerOrder":False,
 "chapters":[{"id":"c1","name":"Chapter One","sub":"","open":True}],
 "scenes":[
  SC("0:00","0:20","Arrival at the village",
     ["The party arrives and the villagers are reluctant to talk about the mill",
      "A local can be persuaded to explain that the miller vanished"],
     "Opening scene. Establish the mill and the missing miller.",
     "Invented — your brief gives no scenes at all, so the whole running order, its titles, its timings and its beats are mine."),
  SC("0:20","0:45","Investigating the mill house",
     ["Search the house for clues about what happened",
      "A DC 13 Investigation check finds something useful"],
     "Exploration scene.",
     "Invented — no scene list was given; this is a guess at the shape of a two-hour session."),
  SC("0:45","1:10","First encounter",
     ["Something attacks as the party approaches the water"],
     "A fight to open the second act.",
     "Invented — and I do not know what should attack here, because the brief only names a hag."),
  SC("1:10","1:35","Deeper into the mill",
     ["The party finds the way down to the wheel"],
     "Transition scene.",
     "Invented — filler between the two fights, because a two-hour session needs a beat here and your brief has none."),
  SC("1:35","1:55","The hag","The hag confronts the party",
     "Boss fight.",
     "Invented — you named a hag and nothing else, so the confrontation, its stakes and how it can be won are all mine."),
  SC("1:55","2:00","Conclusion",
     ["Wrap up and reward the party"],
     "Ending.",
     "Invented — your brief has no ending, so this is a placeholder. This is the one I would most like you to replace."),
 ],
 "mon":[
  dict(n="Mill Haunt", t="Medium Undead, Neutral Evil", cr="1", xp=200, ac=12, hp=26, hd="4d8+8",
       dex=1, conSv=3, sp="30 ft.", ab=[14,12,14,8,10,8], grp="The Mill", side="foe",
       lines=["<span class='k'>Saves</span> Con +3 · <span class='k'>PP</span> 10",
              "<span class='k'>Chilling Touch.</span> +4, reach 5 ft, 1d8+2 cold."],
       **ai("Invented — your brief names no creatures except a hag, so this exists only because the fights needed something in them.")),
  dict(n="Bog Beast", t="Large Beast, Unaligned", cr="2", xp=450, ac=13, hp=45, hd="6d10+12",
       dex=1, conSv=4, sp="30 ft., swim 30 ft.", ab=[16,12,15,3,11,6], grp="The Fen", side="foe",
       lines=["<span class='k'>Saves</span> Con +4 · <span class='k'>PP</span> 11",
              "<span class='k'>Bite.</span> +5, reach 5 ft, 2d6+3 piercing."],
       **ai("Invented from nothing — I needed a second foe to make the first fight worth running.")),
  dict(n="The Hag", t="Medium Fey, Neutral Evil", cr="5", xp=1800, ac=16, hp=82, hd="11d8+33",
       dex=2, conSv=6, sp="30 ft.", ab=[16,14,16,13,14,14], grp="The Mill", side="foe",
       legRes=2, legAct=3,
       lines=["<span class='k'>Saves</span> Con +6, Wis +5 · <span class='k'>PP</span> 15",
              "<span class='k'>Legendary Resistance (2/Day).</span>",
              "<span class='k'>Multiattack.</span> Two Claws.",
              "<span class='k'>Claw.</span> +7, reach 5 ft, 2d6+4 slashing."],
       **ai("Statted at CR 5 — you wrote the word 'hag' and nothing else, so her name, her numbers, her tricks and her motive are all mine.")),
 ],
 "enc":[
  dict(n="Fight 1", loc="Outside the mill", note="An opening fight.",
       m=[["Mill Haunt",3],["Bog Beast",1]],
       **ai("Invented — no fights were described, so the composition is a guess at what fits a level-3 party.")),
  dict(n="Fight 2 — the hag", loc="Inside the mill", note="The boss fight.",
       m=[["The Hag",1],["Mill Haunt",2]],
       **ai("Invented — I do not know what the hag wants or how she can be beaten, so this is a straight fight with no way out but damage.")),
 ],
 "tools":[], "cards":[],
}}

async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': 1600, 'height': 1000}, device_scale_factor=2)
        pg = await ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(f'http://localhost:{PORT}/table_aid_blank.html'); await pg.wait_for_timeout(800)
        await pg.evaluate("()=>document.querySelector('#optBtn').click()"); await pg.wait_for_timeout(300)
        await pg.evaluate("(t)=>{document.getElementById('o_paste').value=t}", json.dumps(THIN))
        await pg.click("text=Replace everything"); await pg.wait_for_timeout(800)
        pill = await pg.locator('#aiPill').inner_text()
        await pg.click('#tabs >> text=Story'); await pg.wait_for_timeout(500)
        await pg.evaluate("()=>{allScenes(true)}"); await pg.wait_for_timeout(500)
        await pg.screenshot(path=str(ROOT/'docs'/'figs'/'thin_story.png'),
                            clip={'x': 90, 'y': 62, 'width': 1420, 'height': 620})
        marked = await pg.evaluate("()=>aiList().length")
        total = await pg.evaluate("()=>MON().length+ENC().length+SC().length+TOOLS().length+CARDS().length")
        print('thin build: pill =', pill, '| marked', marked, 'of', total, 'items')
        await b.close()
        print('errors:', errs or 'none')

asyncio.run(main())
