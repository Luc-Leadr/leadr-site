# Images de partage (LinkedIn, Google) propres à chaque guide, 1200 x 627. Lancer depuis _source : python3 og/gen_og_guides.py
import json, asyncio, base64
from playwright.async_api import async_playwright
LOGO_W = 'data:image/png;base64,' + base64.b64encode(open('static/logo-blanc.png', 'rb').read()).decode()
GUIDES = {
    'og-guide-implantation.png': ('Guide 2026', 'Implantation en Suisse pour PME françaises', 'France → Suisse · leadr.ch'),
    'og-guide-tva-douane.png': ('Guide 2026', 'Vendre en Suisse depuis la France : TVA et douane', 'France → Suisse · leadr.ch'),
    'og-guide-prospection.png': ('Guide 2026', 'Prospection externalisée en Suisse', 'France → Suisse · leadr.ch'),
    'og-guide-marketing.png': ('Guide 2026', 'Marketing externalisé pour le marché suisse', 'France → Suisse · leadr.ch'),
    'og-guide-france.png': ('Guide 2026', 'S\'implanter en France : guide pour les entreprises suisses', 'Suisse → France · leadr.ch'),
    'og-guide-markteintritt.png': ('Leitfaden 2026', 'Markteintritt Frankreich für Schweizer KMU', 'Schweiz → Frankreich · leadr.ch'),
}
def page(k, h, sub):
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;width:1200px;height:627px;background:#1D1D1F;font-family:Arial,Helvetica,sans-serif;color:#FAF7F2;position:relative;overflow:hidden}}
.bar{{position:absolute;top:0;left:0;right:0;height:10px;background:#E8192C}}
.lg{{position:absolute;top:62px;left:72px;height:46px}}
.k{{position:absolute;left:72px;top:170px;font-size:26px;letter-spacing:3px;text-transform:uppercase;color:#FF6B78;font-weight:bold}}
h1{{position:absolute;left:72px;top:220px;margin:0;font-size:64px;line-height:1.06;letter-spacing:-2px;width:1000px}}
p{{position:absolute;left:72px;bottom:60px;margin:0;font-size:26px;color:#C9C4BA}}
</style></head><body><div class="bar"></div><img class="lg" src="{LOGO_W}" alt="">
<div class="k">{k}</div><h1>{h}</h1><p>{sub}</p></body></html>'''
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1200, 'height': 627})
        for f, (k, h, s) in GUIDES.items():
            await pg.set_content(page(k, h, s)); await pg.wait_for_timeout(150)
            await pg.screenshot(path=f'static/img/{f}')
        await b.close()
asyncio.run(main())
