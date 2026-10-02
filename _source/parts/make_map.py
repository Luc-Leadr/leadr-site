# Génère la carte stylisée France / Suisse (régions linguistiques) en SVG
import json, math, shapefile
from shapely.geometry import shape, Polygon, MultiPolygon, mapping
from shapely.ops import unary_union, transform

SM = 'node_modules/swiss-maps/2024/'

def lv95_to_wgs(E, N):
    y = (E - 2600000) / 1e6; x = (N - 1200000) / 1e6
    lam = 2.6779094 + 4.728982*y + 0.791484*y*x + 0.1306*y*x*x - 0.0436*y**3
    phi = 16.9023892 + 3.238272*x - 0.270978*y*y - 0.002528*x*x - 0.0447*y*y*x - 0.0140*x**3
    return lam*100/36, phi*100/36

def ch_geom(s):
    g = shape(s.__geo_interface__)
    return transform(lambda X, Y, Z=None: tuple(zip(*[lv95_to_wgs(a, b) for a, b in zip(X, Y)])) if hasattr(X, '__len__') else lv95_to_wgs(X, Y), g)

def to_wgs(g):
    def f(xs, ys, zs=None):
        out = [lv95_to_wgs(a, b) for a, b in zip(xs, ys)]
        return [o[0] for o in out], [o[1] for o in out]
    return transform(f, g)

FR_DIST = {241, 1001, 1002, 1003, 1004, 1007, 2302, 2303, 2305, 2307, 2308, 2310, 2311, 2312}
FR_CANT = {22, 24, 25, 26}
IT_CANT = {21}; IT_DIST = {1842, 1847}

r = shapefile.Reader(SM + 'districts')
rom, ale, ita = [], [], []
for sr in r.iterShapeRecords():
    did, name, kt = sr.record[0], sr.record[1], sr.record[2]
    g = to_wgs(shape(sr.shape.__geo_interface__)).buffer(0)
    if kt in FR_CANT or did in FR_DIST: rom.append(g)
    elif kt in IT_CANT or did in IT_DIST: ita.append(g)
    else: ale.append(g)
rom = unary_union(rom); ale = unary_union(ale); ita = unary_union(ita)

lk = shapefile.Reader(SM + 'lakes')
lakes = []
for sr in lk.iterShapeRecords():
    if sr.record[1] not in ('Bodensee', 'Lago Maggiore', 'Lago di Lugano'):
        lakes.append(to_wgs(shape(sr.shape.__geo_interface__)).buffer(0))
lakes = unary_union(lakes)

fr = shape(json.load(open('france.json'))['geometry'])
fr = MultiPolygon([p for p in fr.geoms if -6 < p.centroid.x < 10 and 41 < p.centroid.y < 52])

# Projection : équirectangulaire centrée, Suisse légèrement détachée et agrandie
LAT0 = 46.6; K = 36.0; C = math.cos(math.radians(LAT0))
def proj(lon, lat): return ((lon + 5.4) * C * K, (51.4 - lat) * K)
CH_DX, CH_S = 112, 2.1
ch_c = proj(8.2, 46.8)
def proj_ch(lon, lat):
    x, y = proj(lon, lat)
    return (ch_c[0] + (x - ch_c[0]) * CH_S + CH_DX, ch_c[1] + (y - ch_c[1]) * CH_S)

def P(g, fn, tol, exterior_only=True):
    g = transform(lambda xs, ys, zs=None: tuple(map(list, zip(*[fn(a, b) for a, b in zip(xs, ys)]))), g)
    g = g.simplify(tol, preserve_topology=True)
    polys = [g] if isinstance(g, Polygon) else list(g.geoms)
    d = ''
    for p in polys:
        if p.area < 2: continue
        for ring in ([p.exterior] if exterior_only else [p.exterior] + list(p.interiors)):
            pts = list(ring.coords)
            d += 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts[:-1]) + 'Z'
    return d

d_fr = P(fr, proj, 0.6)
d_rom = P(rom, proj_ch, 0.35); d_ale = P(ale, proj_ch, 0.35); d_ita = P(ita, proj_ch, 0.35)
d_lak = P(lakes, proj_ch, 0.25)
# Röstigraben : frontière commune romande / alémanique
border = rom.boundary.intersection(ale.buffer(0.004))
d_rg = ''
bl = transform(lambda xs, ys, zs=None: tuple(map(list, zip(*[proj_ch(a, b) for a, b in zip(xs, ys)]))), border).simplify(0.4)
for line in (getattr(bl, 'geoms', [bl])):
    if line.geom_type == 'LineString' and line.length > 3:
        d_rg += 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in line.coords)

allx = []
for d in (d_fr, d_ale, d_rom, d_ita):
    for tok in d.replace('M', ' ').replace('L', ' ').replace('Z', ' ').split():
        allx.append(float(tok))
xs = allx[0::2]; ys = allx[1::2]
print('bbox', min(xs), min(ys), max(xs), max(ys))

cities = {'Paris': proj(2.35, 48.86), 'Lyon': proj(4.84, 45.76), 'Genève': proj_ch(6.14, 46.20), 'Lausanne': proj_ch(6.63, 46.52),
          'Bâle': proj_ch(7.59, 47.56), 'Zurich': proj_ch(8.54, 47.37)}
rom_c = proj_ch(6.9, 46.65); ale_c = proj_ch(8.3, 47.15); fr_c = proj(2.6, 46.8)
json.dump({'fr': d_fr, 'rom': d_rom, 'ale': d_ale, 'ita': d_ita, 'lakes': d_lak, 'rg': d_rg, 'cities': cities,
           'rom_c': rom_c, 'ale_c': ale_c, 'fr_c': fr_c, 'bbox': [min(xs), min(ys), max(xs), max(ys)]}, open('map.json', 'w'))
print({k: (round(v[0]), round(v[1])) for k, v in cities.items()}, rom_c, ale_c, fr_c, len(d_fr), len(d_rom), len(d_ale))
