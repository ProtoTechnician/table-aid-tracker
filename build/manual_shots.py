#!/usr/bin/env python3
"""Capture the figures used in the manual, straight out of demo.html."""
import os
from pathlib import Path
# Repo-relative paths. Override the tracker source with TABLE_AID_SOURCE.
ROOT = Path(__file__).resolve().parent.parent
SOURCE_TRACKER = Path(os.environ.get(
    'TABLE_AID_SOURCE', ROOT.parent / 'abyss_tracker.html'))

import asyncio, http.server, socketserver, threading, functools, os
from playwright.async_api import async_playwright

PORT = 8931
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT/'tracker'))
httpd = socketserver.TCPServer(("", PORT), H)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
OUT = str(ROOT/'docs'/'figs')
os.makedirs(OUT, exist_ok=True)

async def main():
    errs = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': 1600, 'height': 1000}, device_scale_factor=2)
        pg = await ctx.new_page()
        pg.on('pageerror', lambda e: errs.append(str(e)))
        url = f'http://localhost:{PORT}/demo.html'
        await pg.goto(url); await pg.wait_for_timeout(900)

        async def shot(name, sel=None, clip=None, h=None):
            if sel:
                await pg.locator(sel).first.screenshot(path=f'{OUT}/{name}.png')
            else:
                await pg.screenshot(path=f'{OUT}/{name}.png', clip=clip)
            print('  ', name)

        # 1 — Story, first segment open
        await pg.click('#tabs >> text=Story'); await pg.wait_for_timeout(400)
        await shot('story', clip={'x': 90, 'y': 100, 'width': 1420, 'height': 700})

        # 2 — Encounters with the budget bar and map
        await pg.click('#tabs >> text=Encounters'); await pg.wait_for_timeout(400)
        await shot('budget', clip={'x': 90, 'y': 100, 'width': 1420, 'height': 330})
        await pg.locator('.enc button:has-text("▶ Map")').nth(2).click(); await pg.wait_for_timeout(500)
        await pg.locator('.enc').nth(2).scroll_into_view_if_needed(); await pg.wait_for_timeout(400)
        await shot('map', sel='.enc:nth-of-type(3) .mapwrap')

        # 3 — Bestiary with a tray-bearing card
        await pg.click('#tabs >> text=Bestiary'); await pg.wait_for_timeout(400)
        await pg.fill('#monSearch', 'grist'); await pg.wait_for_timeout(400)
        await shot('bestiary', sel='.mon')
        await pg.fill('#monSearch', ''); await pg.wait_for_timeout(300)

        # 4 — Tools: dice + handouts
        await pg.click('#tabs >> text=Tools'); await pg.wait_for_timeout(400)
        await pg.fill('#dt_expr', '4d6kh3')
        await pg.click('.dicebay button:has-text("Roll")'); await pg.wait_for_timeout(300)
        await pg.fill('#dt_expr', '2d8+1d6+4')
        await pg.click('.dicebay button:has-text("Roll")'); await pg.wait_for_timeout(300)
        await shot('dice', clip={'x': 90, 'y': 100, 'width': 1420, 'height': 400})
        await pg.locator('#nowBar').scroll_into_view_if_needed(); await pg.wait_for_timeout(400)
        await shot('handouts', clip={'x': 90, 'y': 430, 'width': 1420, 'height': 540})

        # 5 — the fight: load an encounter, add a timer, mark a reaction
        await pg.click('#tabs >> text=Encounters'); await pg.wait_for_timeout(300)
        await pg.locator("button:has-text('Load into initiative')").nth(2).click(); await pg.wait_for_timeout(700)
        await shot('trigger', sel='#tsheet')
        await pg.evaluate("()=>closeTrig()"); await pg.wait_for_timeout(300)
        await pg.evaluate("()=>{addPartyToInit&&addPartyToInit()}"); await pg.wait_for_timeout(400)
        await pg.fill('#fxName', 'Bless'); await pg.fill('#fxR', '10')
        await pg.click("button:has-text('+ Timer')"); await pg.wait_for_timeout(300)
        await pg.fill('#fxName', 'Sluice open — floor flooded'); await pg.fill('#fxR', '3')
        await pg.click("button:has-text('+ Timer')"); await pg.wait_for_timeout(300)
        await pg.locator('.rx').first.click(); await pg.wait_for_timeout(300)
        await pg.evaluate("()=>{const c=S.combatants.find(x=>x.type==='foe');if(c){c.hp=Math.round(c.maxhp*0.4);c.conds=['Prone'];c.conc=true}renderInit()}")
        await pg.wait_for_timeout(300)
        await shot('initiative', clip={'x': 90, 'y': 100, 'width': 1420, 'height': 560})

        # 6 — area damage
        await pg.click("button:has-text('Area damage')"); await pg.wait_for_timeout(500)
        await pg.fill('#aoeAmt', '22'); await pg.wait_for_timeout(200)
        await pg.click("#edbody >> button:has-text('All foes')"); await pg.wait_for_timeout(300)
        await pg.locator('.aoerow .seg3 button:has-text("saved")').nth(1).click(); await pg.wait_for_timeout(400)
        await shot('aoe', sel='#edbody .f')
        await pg.evaluate("()=>closeEd()"); await pg.wait_for_timeout(300)

        # 7 — party + HP roller
        await pg.click('#tabs >> text=Party'); await pg.wait_for_timeout(400)
        await shot('party', clip={'x': 90, 'y': 100, 'width': 1420, 'height': 470})
        await pg.locator('#partyGrid .hpbar').first.click(); await pg.wait_for_timeout(600)
        await shot('hproll', sel='#modal > div')

        await pg.reload(); await pg.wait_for_timeout(900)

        # 8 — provenance
        await pg.click('#tabs >> text=Bestiary'); await pg.wait_for_timeout(400)
        await pg.fill('#monSearch', 'hound'); await pg.wait_for_timeout(400)
        await shot('provenance', sel='.mon')

        # 9 + 10 — the player window
        async with ctx.expect_page() as npg:
            await pg.click('#playerBtn')
        pw = await npg.value
        await pw.set_viewport_size({'width': 1280, 'height': 800})
        await pg.wait_for_timeout(600)
        await pg.click('#tabs >> text=Tools'); await pg.wait_for_timeout(400)
        await pg.locator(".ho button:has-text('Show to players')").first.click(); await pg.wait_for_timeout(700)
        await pw.screenshot(path=f'{OUT}/player_handout.png'); print('   player_handout')
        await pg.click('#tabs >> text=Encounters'); await pg.wait_for_timeout(300)
        await pg.locator("button:has-text('Load into initiative')").first.click(); await pg.wait_for_timeout(700)
        await pg.evaluate("()=>closeTrig()")
        await pg.evaluate("()=>{addPartyToInit&&addPartyToInit();S.data.playerOrder=true;renderInit();pushPlayer()}")
        await pg.wait_for_timeout(600)
        await pw.screenshot(path=f'{OUT}/player_map.png'); print('   player_map')
        await pg.click('#tabs >> text=Story'); await pg.wait_for_timeout(400)
        await pg.locator('.scene .scimg').first.click(); await pg.wait_for_timeout(700)
        await pw.screenshot(path=f'{OUT}/player_image.png'); print('   player_image')

        await b.close()
    print('errors:', errs or 'none')

asyncio.run(main())
