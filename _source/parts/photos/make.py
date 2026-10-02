from proc import *
INK = (0x1D, 0x1D, 0x1F); RED = (0xE8, 0x19, 0x2C)
# 1. dark block: Matterhorn, summit at 27% of the canvas
compose('cervin.jpg', (0, 30, 890, 330), (2400, 760), 0.27, 0.80, INK, dark(34, 150), 'antenne.jpg', fade_bottom=0.35, side_fade=0.22, fix=[(409, 466)])
# 2. red block: Bachalpsee range, mountains on the right
compose('bachalpsee2.jpg', (0, 60, 700, 250), (2400, 700), 0.72, 0.62, RED, red(0.55), 'rouge.jpg', fade_bottom=0.30, side_fade=0.2)
# 3. CTA: Schreckhorn range, wide
compose('bachalpsee1.jpg', (0, 170, 890, 420), (2400, 600), 0.5, 0.75, INK, dark(30, 120), 'cta.jpg', fade_bottom=0.35, side_fade=0.15)
for n in ['antenne', 'rouge', 'cta']:
    Image.open(n + '.jpg').resize((1200, int(1200 * Image.open(n + '.jpg').size[1] / 2400))).save(n + '-prev.png')
