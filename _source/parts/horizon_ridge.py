import math, random
random.seed(7)
W, H = 1600, 520
def interp(pts, x):
    for (x0,y0),(x1,y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            t = (x-x0)/(x1-x0) if x1>x0 else 0
            return y0 + (y1-y0)*t
    return pts[-1][1] if x > pts[-1][0] else pts[0][1]
# Matterhorn profile (normalized), as seen from Zermatt
MH = [(0.00,0.03),(0.10,0.10),(0.20,0.22),(0.30,0.40),(0.38,0.57),(0.44,0.71),(0.49,0.83),(0.52,0.905),(0.545,0.955),(0.566,0.99),(0.578,1.0),(0.588,0.997),(0.600,0.985),(0.614,0.955),(0.638,0.905),(0.66,0.85),(0.69,0.795),(0.715,0.755),(0.735,0.737),(0.755,0.73),(0.772,0.712),(0.80,0.655),(0.85,0.54),(0.90,0.38),(0.95,0.22),(1.0,0.07)]
def matterhorn(x, cx, w, h):
    u = (x-(cx-w/2))/w
    if u < 0 or u > 1: return 0
    return interp(MH, u)*h
def noise_ridge(x, seed, amp, scale):
    r = random.Random(seed)
    ph = [r.uniform(0, 6.28) for _ in range(5)]
    return amp*sum(math.sin(x/scale*(k+1)*0.9+ph[k])/(k+1)**1.3 for k in range(5))
def peaks(x, specs):
    v = 0
    for cx, w, h, sharp in specs:
        d = abs(x-cx)/(w/2)
        if d < 1: v = max(v, h*(1-d)**sharp)
    return v
layers = []
# back layer: Matterhorn + neighbours (Dent d'Herens left, Breithorn mass right)
def L0(x):
    return max(matterhorn(x, 430, 400, 360),
               peaks(x, [(110, 300, 140, 1.4), (240, 240, 105, 1.6), (760, 360, 150, 1.3), (930, 260, 120, 1.5), (1180, 420, 135, 1.3), (1420, 320, 115, 1.4), (1560, 240, 95, 1.4)]) + noise_ridge(x, 1, 7, 40),
               34 + noise_ridge(x, 2, 10, 70))
def L1(x):
    return max(peaks(x, [(180, 460, 150, 1.1), (520, 420, 120, 1.2), (880, 380, 95, 1.3), (1250, 480, 130, 1.1), (1560, 300, 110, 1.2)]) + noise_ridge(x, 3, 8, 30), 30 + noise_ridge(x, 4, 8, 45))
def L2(x):
    return max(peaks(x, [(330, 700, 80, 1.0), (1000, 800, 70, 1.0), (1500, 500, 75, 1.0)]) + noise_ridge(x, 5, 6, 50), 18 + noise_ridge(x, 6, 6, 60))
def path(f, base, step=3):
    pts = [(x, base - f(x)) for x in range(0, W+step, step)]
    return 'M' + ' L'.join(f'{x:.0f} {y:.1f}' for x, y in pts)
BG = "#1D1D1F"
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMax slice" fill="none" stroke="#fff" stroke-linejoin="round" stroke-linecap="round">']
base0 = 420
for i in range(1, 15):
    k = 1 - i/15
    f = (lambda k: (lambda x: L0(x)*k))(k)
    op = 0.6*(1-i/17)
    out.append(f'<path d="{path(f, base0 + i*6, 6)}" stroke-width="1" opacity="{op:.2f}"/>')
out.append(f'<path d="{path(L0, base0)}" stroke-width="1.7"/>')
def closed(f, base):
    return path(f, base) + f' L{W} {H} L0 {H}Z'
out.append(f'<path d="{closed(L1, 478)}" fill="{BG}" stroke-width="1.3" opacity="1"/>')
for i in range(1, 6):
    k = 1 - i/6
    f = (lambda k: (lambda x: L1(x)*k))(k)
    out.append(f'<path d="{path(f, 478 + i*6, 6)}" stroke-width="1" opacity="{0.45*(1-i/7):.2f}"/>')
out.append(f'<path d="{closed(L2, 518)}" fill="{BG}" stroke-width="1.1" opacity=".9"/>')
out.append('</svg>')
open('alpes.svg','w').write('\n'.join(out))
print(len(''.join(out)))

# horizon: single ridge line for the CTA band
h = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 400" preserveAspectRatio="xMidYMax slice" fill="none" stroke="#fff" stroke-linejoin="round" stroke-linecap="round">']
h.append(f'<path d="{path(L0, 400)}" stroke-width="1.6"/>')
h.append(f'<path d="{path(lambda x: L0(x)*0.55, 404, 6)}" stroke-width="1" opacity=".5"/>')
h.append('</svg>')
open('horizon.svg','w').write('\n'.join(h))
