import asyncio, sys
from playwright.async_api import async_playwright
ROOT='/home/claude/site'
VARIANTS={
 'a':("Vos prochains clients sont de l'autre côté de la frontière.",),
 'b':("Votre antenne<br>entre la France et la Suisse.",),
}
def page(head, preview=False):
    photo = '<div class="pp"><img src="file://%s/static/img/luc-rohmer.jpg"></div>'%ROOT if preview else ''
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Arimo;src:url(file://{ROOT}/static/fonts/arimo-latin-wght-normal.woff2) format("woff2");font-weight:400 700}}
html,body{{margin:0}}
.b{{position:relative;width:1584px;height:396px;overflow:hidden;background:#1D1D1F;font-family:Arimo,Arial,sans-serif;color:#fff}}
.bg{{position:absolute;left:-60px;top:-70px;width:1700px;height:auto}}
.fade{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(29,29,31,0) 0%,rgba(29,29,31,0) 42%,rgba(29,29,31,.88) 62%,#1D1D1F 75%)}}
.bar{{position:absolute;left:0;top:0;width:100%;height:8px;background:#E8192C}}
.t{{position:absolute;right:84px;top:62px;width:690px}}
.k{{font-size:19px;font-weight:700;color:#FF4A58;letter-spacing:.04em;margin:0 0 18px}}
h1{{font-size:46px;line-height:1.14;font-weight:620;margin:0 0 18px;letter-spacing:-.01em;text-wrap:balance}}
.s{{font-size:21px;line-height:1.4;color:#C9C9CE;margin:0 0 26px;text-wrap:balance}}
.f{{display:flex;align-items:center;gap:22px}}
.f img{{height:30px}}
.f span{{font-size:20px;font-weight:600;color:#fff;border-left:1px solid rgba(255,255,255,.35);padding-left:22px}}
.pp{{position:absolute;left:47px;top:236px;width:300px;height:300px;border-radius:50%;border:8px solid #fff;overflow:hidden;box-sizing:border-box}}
.pp img{{width:100%;height:100%;object-fit:cover}}
</style></head><body><div class="b">
<img class="bg" src="file://{ROOT}/static/img/antenne.jpg"><div class="fade"></div><div class="bar"></div>
<div class="t"><p class="k">FRANCE · SUISSE ROMANDE · SUISSE ALÉMANIQUE</p>
<h1>{head}</h1>
<p class="s">Prospection, implantation, relocalisation et mises en relation pour PME, PMI et ETI</p>
<div class="f"><img src="file://{ROOT}/dist/logo-blanc.png"><span>www.leadr.ch</span></div></div>
{photo}</div></body></html>'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for k,(h,) in VARIANTS.items():
            for prev in (False,True):
                pg=await b.new_page(viewport={'width':1584,'height':396},device_scale_factor=1 if prev else 2)
                open('t.html','w').write(page(h,prev))
                await pg.goto('file:///home/claude/site/parts/banniere/t.html'); await pg.wait_for_timeout(400)
                await pg.screenshot(path=f'{"apercu" if prev else "banniere"}-{k}.png',clip={'x':0,'y':0,'width':1584,'height':396})
                await pg.close()
        await b.close()
asyncio.run(main())
