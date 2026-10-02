import numpy as np, sys
from PIL import Image, ImageFilter
img=np.load('/tmp/claude-0/art2/raw.npy'); a=np.load('/tmp/claude-0/art2/alpha.npy')
H,W=img.shape
bg=np.array([0x1D,0x1D,0x1F],float)
yy=np.arange(H)[:,None]
# sky: bg with faint haze near the horizon
sky=np.ones((H,W,1))*bg + (np.exp(-((yy-0.50*H)/(0.16*H))**2)*9)[...,None]
gain=float(sys.argv[1]) if len(sys.argv)>1 else 1.0
lum=np.clip(img*255*gain,0,255)
terr=np.stack([lum,lum,lum*1.03],-1)
# never darker than bg
terr=np.maximum(terr, bg*0.95)
rgb=sky*(1-a[...,None])+terr*a[...,None]
rgb+=np.random.default_rng(1).normal(0,1.8,(H,W))[...,None]
out=Image.fromarray(np.clip(rgb,0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.5))
out.save(sys.argv[2] if len(sys.argv)>2 else '/tmp/claude-0/art2/alpes.jpg', quality=80, optimize=True, progressive=True)
out.resize((1200,400)).save('/tmp/claude-0/art2/prev2.png')
