import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import gaussian_filter, uniform_filter1d

def load(p): return np.asarray(Image.open(p).convert('RGB')).astype(float)

def sky_mask(a, blue_min=25, tol=14, fix=None):
    from scipy.ndimage import median_filter
    sa = gaussian_filter(a, (1, 1, 0))
    H, W, _ = a.shape
    ridge = np.zeros(W, int)
    for x in range(W):
        ref = sa[0, x].copy(); y = 1
        while y < H - 2:
            d = np.abs(sa[y, x] - ref).max()
            d2 = np.abs(sa[y + 1, x] - ref).max()
            if d > tol and d2 > tol: break
            ref = 0.8 * ref + 0.2 * sa[y, x]
            y += 1
        ridge[x] = y
    ridge = median_filter(ridge, 9)
    if fix:
        for x0, x1 in fix:
            ridge[x0:x1] = np.round(np.interp(np.arange(x0, x1), [x0 - 1, x1], [ridge[x0 - 1], ridge[x1]])).astype(int)
    m = np.zeros((H, W))
    for x in range(W): m[:ridge[x], x] = 1
    return gaussian_filter(m, 0.8), ridge

def lum(a):
    return (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]) / 255

def tone(L, gamma=1.25, lo=0.08, hi=0.98):
    L = np.clip((L - lo) / (hi - lo), 0, 1)
    return L ** gamma

def compose(src, crop, canvas, place_x, height_frac, bg, colorize, out, fade_bottom=0.25, side_fade=0.18, blur=0.6, sky_min=25, fix=None, dump=False):
    a = load(src)[crop[1]:crop[3], crop[0]:crop[2]]
    sm, ridge = sky_mask(a, sky_min, fix=fix)
    if dump: print(list(enumerate(ridge))[380:480])
    L = tone(lum(a))
    CW, CH = canvas
    h = int(CH * height_frac); w = int(a.shape[1] * h / a.shape[0])
    Li = np.asarray(Image.fromarray((L * 255).astype(np.uint8)).resize((w, h), Image.LANCZOS)).astype(float) / 255
    Mi = np.asarray(Image.fromarray((sm * 255).astype(np.uint8)).resize((w, h), Image.LANCZOS)).astype(float) / 255
    alpha = 1 - Mi
    # fades: left/right edges of the photo, bottom
    xs = np.linspace(0, 1, w)[None, :]
    ef = np.clip(xs / side_fade, 0, 1) * np.clip((1 - xs) / side_fade, 0, 1)
    ys = np.linspace(0, 1, h)[:, None]
    bf = np.clip((1 - ys) / fade_bottom, 0, 1) if fade_bottom else 1
    alpha = alpha * ef * bf
    canvasL = np.zeros((CH, CW)); canvasA = np.zeros((CH, CW))
    x0 = int(place_x * CW - w / 2); y0 = CH - h
    xa, xb = max(0, x0), min(CW, x0 + w)
    canvasL[y0:, xa:xb] = Li[:, xa - x0:xb - x0]
    canvasA[y0:, xa:xb] = alpha[:, xa - x0:xb - x0]
    rgb = colorize(canvasL, canvasA, np.array(bg, float))
    im = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
    im.save(out, quality=82, optimize=True, progressive=True)
    return ridge

def dark(lo_val, hi_val):
    def f(L, A, bg):
        g = lo_val + (hi_val - lo_val) * L
        tint = np.stack([g, g, g * 1.04], -1)
        return bg * (1 - A[..., None]) + tint * A[..., None]
    return f

def red(strength):
    def f(L, A, bg):
        k = 1 + strength * (L - 0.45)            # snow lighter, rock darker
        k = k[..., None]
        light = bg + (255 - bg) * np.clip(k - 1, 0, 1)
        darkc = bg * np.clip(k, 0, 1)
        c = np.where(k > 1, light, darkc)
        return bg * (1 - A[..., None]) + c * A[..., None]
    return f
