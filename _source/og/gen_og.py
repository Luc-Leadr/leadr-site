import json, asyncio, base64
LOGO_W = 'data:image/png;base64,' + base64.b64encode(open('/home/claude/site/static/logo-blanc.png','rb').read()).decode()
from playwright.async_api import async_playwright
m = json.load(open('/home/claude/geo/map.json'))
x0,y0,x1,y1 = m['bbox']
vb = f"{x0-10:.0f} {y0-10:.0f} {x1-x0+20:.0f} {y1-y0+20:.0f}"
TXT = {'fr': ("Vos prochains clients sont de l'autre côté de la frontière.", "France · Suisse romande · Suisse alémanique · leadr.ch"),
       'de': ("Ihre nächsten Kunden sind auf der anderen Seite der Grenze.", "Frankreich · Romandie · Deutschschweiz · leadr.ch"),
       'en': ("Your next clients are on the other side of the border.", "France · French and German speaking Switzerland · leadr.ch")}
def page(h, sub):
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;width:1200px;height:627px;background:#1D1D1F;font-family:Arial,Helvetica,sans-serif;color:#FAF7F2;position:relative;overflow:hidden}}
.bar{{position:absolute;top:0;left:0;right:0;height:10px;background:#E8192C}}
.lg{{position:absolute;top:62px;left:72px;height:46px}}
.sq{{width:48px;height:48px;background:#E8192C;position:relative}}
.sq:before,.sq:after{{content:"";position:absolute;background:#fff}}
.sq:before{{left:19px;top:9px;width:10px;height:30px}}.sq:after{{left:9px;top:19px;width:30px;height:10px}}
.logo b{{color:#E8192C}}
h1{{position:absolute;left:72px;top:160px;margin:0;font-size:66px;line-height:1.02;letter-spacing:-2.5px;width:640px}}
p{{position:absolute;left:72px;bottom:60px;margin:0;font-size:26px;color:#C9C4BA}}
svg{{position:absolute;right:40px;top:110px;width:440px}}
.fr,.ch-w{{fill:#2B2B2E;stroke:#FAF7F2;stroke-width:1.2}} .ch-e{{fill:#FAF7F2;stroke:#FAF7F2;stroke-width:1.2}} .ch-i{{fill:#3A3A3D;stroke:#FAF7F2;stroke-width:1.2}}
.g{{fill:none;stroke:#E8192C;stroke-width:3;stroke-dasharray:4 3}} .a{{fill:none;stroke:#E8192C;stroke-width:4}}
</style></head><body><div class="bar"></div><img class="lg" src="{LOGO_W}" alt="">
<h1>{h}</h1><p>{sub}</p>
<svg viewBox="{vb}"><defs><marker id="ah" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#E8192C"/></marker></defs>
<path class="fr" d="{m['fr']}"/><path class="ch-w" d="{m['rom']}"/><path class="ch-e" d="{m['ale']}"/><path class="ch-i" d="{m['ita']}"/><path class="g" d="{m['rg']}"/>
<path class="a" marker-end="url(#ah)" d="M236 100 C 270 26, 356 30, 372 128"/><path class="a" marker-end="url(#ah)" d="M404 236 C 392 306, 312 306, 282 238"/><path class="a" marker-start="url(#ah)" marker-end="url(#ah)" d="M384 104 C 408 48, 478 44, 502 92"/>
</svg></body></html>'''
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width':1200,'height':627})
        for lg,(h,s) in TXT.items():
            await pg.set_content(page(h,s)); await pg.wait_for_timeout(200)
            await pg.screenshot(path=f'/home/claude/site/static/og-image{"" if lg=="fr" else "-"+lg}.png')
        await b.close()
asyncio.run(main())
