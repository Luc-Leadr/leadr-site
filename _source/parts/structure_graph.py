import math
W, H = 760, 360
base = 330
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMaxYMax meet" fill="none" stroke="#fff" stroke-linecap="round" stroke-linejoin="round">']
# baseline
o.append(f'<path d="M0 {base} H{W}" stroke-width="1.2" opacity=".7"/>')
# revenue bars (growing), x 20..440
n = 14
pts = []
for i in range(n):
    x = 24 + i*31
    t = i/(n-1)
    h = 22 + 230*(t**1.6)
    o.append(f'<rect x="{x}" y="{base-h:.1f}" width="16" height="{h:.1f}" stroke-width="1.2" opacity=".55"/>')
    pts.append((x+8, base-h-14))
# curve over bars
d = 'M' + ' '.join(f'{"L" if i else ""}{x:.1f} {y:.1f}' for i,(x,y) in enumerate(pts))
o.append(f'<path d="{d}" stroke-width="2"/>')
for x,y in pts[::3]+[pts[-1]]:
    o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="#fff" stroke="none"/>')
# arrow head at end of curve
x,y = pts[-1]; x0,y0 = pts[-2]
ang = math.atan2(y-y0, x-x0)
def rot(px,py): return (x+px*math.cos(ang)-py*math.sin(ang), y+px*math.sin(ang)+py*math.cos(ang))
a=rot(-14,-7); b=rot(-14,7)
o.append(f'<path d="M{a[0]:.1f} {a[1]:.1f} L{x:.1f} {y:.1f} L{b[0]:.1f} {b[1]:.1f}" stroke-width="2"/>')
# structure: dashed blueprint building, x 500..720
bx, bw, bh = 520, 190, 210
dash = 'stroke-dasharray="6 6"'
o.append(f'<path d="M{bx} {base} V{base-bh} H{bx+bw} V{base}" stroke-width="1.6" {dash}/>')
# roof line / floors
for k in range(1,5):
    yy = base - bh*k/5
    o.append(f'<path d="M{bx} {yy:.1f} H{bx+bw}" stroke-width="1" {dash} opacity=".7"/>')
for k in range(1,4):
    xx = bx + bw*k/4
    o.append(f'<path d="M{xx:.1f} {base-bh} V{base}" stroke-width="1" {dash} opacity=".5"/>')
# swiss-cross flag on top of the building
fx, fy = bx+bw-30, base-bh
o.append(f'<path d="M{fx} {fy} V{fy-46}" stroke-width="1.4" {dash}/>')
o.append(f'<rect x="{fx}" y="{fy-46}" width="26" height="26" stroke-width="1.4" {dash}/>')
o.append(f'<path d="M{fx+13} {fy-41} V{fy-25} M{fx+5} {fy-33} H{fx+21}" stroke-width="2"/>')
o.append('</svg>')
open('structure.svg','w').write('\n'.join(o))
