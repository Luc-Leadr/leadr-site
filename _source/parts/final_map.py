import json
m=json.load(open('map.json'))
x0,y0,x1,y1=m['bbox']
vb=f"{x0-16:.0f} {y0-14:.0f} {x1-x0+32:.0f} {y1-y0+28:.0f}"
c=m['cities']
lab={'Paris':('start',6,4),'Lyon':('start',6,4),'Genève':('middle',0,15),'Lausanne':('end',-6,-3),'Bâle':('end',-6,-4),'Zurich':('start',6,4)}
cities=''.join(f'<g class="city"><circle cx="{v[0]:.1f}" cy="{v[1]:.1f}" r="2.8"/><text x="{v[0]+lab[k][1]:.1f}" y="{v[1]+lab[k][2]:.1f}" text-anchor="{lab[k][0]}">{k}</text></g>' for k,v in c.items())
arrows='''<path class="arrow a1" marker-end="url(#ah)" d="M236 100 C 270 26, 356 30, 372 128"/>
  <path class="arrow a2" marker-end="url(#ah)" d="M404 236 C 392 306, 312 306, 282 238"/>
  <path class="arrow a3" marker-start="url(#ah)" marker-end="url(#ah)" d="M384 104 C 408 48, 478 44, 502 92"/>'''
svg=f'''<figure class="map" aria-label="Carte : la France, la Suisse romande et la Suisse alémanique, reliées par trois directions">
<svg viewBox="{vb}" role="img">
  <defs><marker id="ah" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#E8192C"/></marker></defs>
  <path class="land fr" d="{m['fr']}"/>
  <path class="land ch-w" d="{m['rom']}"/><path class="land ch-e" d="{m['ale']}"/><path class="land ch-i" d="{m['ita']}"/>
  <path class="lake" d="{m['lakes']}"/>
  <path class="graben" d="{m['rg']}"/>
  {arrows}
  {cities}
</svg>
<figcaption><span class="sw sw-w"></span>Suisse romande <span class="sw sw-e"></span>Suisse alémanique <span class="sw sw-g"></span>Röstigraben</figcaption>
</figure>'''
open('/home/claude/site/parts/map.svg','w').write(svg)
# version de test
open('test2.html','w').write('<html><head><link rel="stylesheet" href="/home/claude/site/static/css/style.css"></head><body style="background:#FAF7F2;width:700px;padding:20px">'+svg+'</body></html>')
print(vb, len(svg))
