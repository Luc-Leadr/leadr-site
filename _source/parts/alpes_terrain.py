import numpy as np
from scipy.ndimage import zoom, gaussian_filter, map_coordinates
from PIL import Image, ImageFilter
N = 1024
rng = np.random.default_rng(4)

def noise(octaves=8, base=4, pers=0.5, ridged=False, seed=0):
    r = np.random.default_rng(seed)
    out = np.zeros((N, N)); amp = 1.0; tot = 0
    for o in range(octaves):
        s = base * 2 ** o
        if s > N: break
        g = r.normal(0, 1, (s + 1, s + 1))
        up = zoom(g, N / (s + 1), order=3)[:N, :N]
        if ridged:
            up = 1 - np.abs(up)
            up = up ** 2
        out += amp * up; tot += amp; amp *= pers
    return out / tot

zz, xx = np.mgrid[0:N, 0:N] / N    # zz: depth (0 near camera, 1 far), xx: left-right
# base relief: ridged multifractal mountains, increasing with distance
ridge = noise(9, 3, 0.52, ridged=True, seed=1)
ridge = (ridge - ridge.min()) / (ridge.max() - ridge.min())
fine = noise(9, 16, 0.55, seed=2)
h = 0.40 * ridge ** 2.0 + 0.02 * fine
h *= np.clip((zz - 0.12) / 0.5, 0, 1) ** 1.2 * (1.0 + 1.3 * np.clip((zz - 0.55) / 0.4, 0, 1)) + 0.05     # valley in the foreground

# Matterhorn: four-faced pyramid rotated ~40deg, slightly hooked summit, at (x=0.28, z=0.62)
cx, cz, R, Hm = 0.30, 0.62, 0.08, 0.64
dx, dz = xx - cx, zz - cz
a = np.deg2rad(38)
rx = dx * np.cos(a) - dz * np.sin(a); rz = dx * np.sin(a) + dz * np.cos(a)
d = np.maximum(np.abs(rx) * 1.0, np.abs(rz) * 1.12) / R
rn = noise(8, 20, 0.6, ridged=True, seed=5)
n1 = noise(8, 10, 0.6, seed=8); n2 = noise(8, 40, 0.65, ridged=True, seed=9)
dd = d + 0.16 * n1 * d + 0.05 * (n2 - n2.mean())          # ragged ridges, more at the base
pyr = Hm * np.clip(1 - dd, 0, 1) ** 1.45
pyr *= 1 + 0.16 * (rn - rn.mean())
theta = np.arctan2(dz, dx); rr = np.sqrt(dx**2 + dz**2)
r1 = np.random.default_rng(21).normal(0, 1, 361); r2 = np.random.default_rng(22).normal(0, 1, 1441)
tt = (theta + np.pi) / (2 * np.pi)
rad = 0.6 * np.interp(tt, np.linspace(0, 1, 361), r1) + 0.4 * np.interp(tt, np.linspace(0, 1, 1441), r2)
rad = rad * (0.7 + 0.3 * noise(6, 8, 0.5, seed=23))
pyr -= 0.018 * np.clip(rad, -2, 2) * np.clip(rr / R, 0.15, 1) * (pyr > 0.02)
# hooked summit: tilt the top slightly toward the camera-right
tip = np.exp(-((rx - 0.012) ** 2 + (rz + 0.008) ** 2) / 0.0004) * 0.035
# shoulder on the Hornli ridge
sh = np.exp(-(((rx - 0.035) / 0.02) ** 2 + ((rz + 0.0) / 0.03) ** 2)) * 0.04
h = np.maximum(h, pyr + sh + tip)
h = gaussian_filter(h, 0.7)

# lighting
gz, gx = np.gradient(h * N * 0.9)
nx, nz, ny = -gx, -gz, np.ones_like(h)
nrm = np.sqrt(nx ** 2 + ny ** 2 + nz ** 2); nx, ny, nz = nx / nrm, ny / nrm, nz / nrm
L = np.array([-0.75, 0.55, -0.35]); L = L / np.linalg.norm(L)   # light from the left, slightly from camera side
diff = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1)
slope = 1 - ny
snow = np.clip((h - 0.22) / 0.10, 0, 1) * np.clip(1.15 - slope * 1.3, 0, 1)
shade = 0.16 + 0.84 * diff ** 1.15
alb = 0.45 + 0.55 * snow
col_map = shade * alb      # 0..1 luminance

# voxel-space render
W, H = 2400, 800
cam_x, cam_z, cam_h = 0.5, -0.02, 0.12
horizon = H * 0.56
scale = H * 1.9
fov = 1.05
cols = np.arange(W)
ang = (cols / W - 0.5) * fov
zs = np.concatenate([np.linspace(0.02, 0.3, 400), np.linspace(0.3, 1.05, 1400)])
SY = np.zeros((len(zs), W)); CV = np.zeros((len(zs), W)); FG = np.zeros(len(zs))
for k, z in enumerate(zs):
    wx = cam_x + np.tan(ang) * z
    wz = np.full(W, cam_z + z)
    inb = (wx >= 0) & (wx < 1) & (wz >= 0) & (wz < 1)
    xi = np.clip(wx * (N - 1), 0, N - 1); zi = np.clip(wz * (N - 1), 0, N - 1)
    hv = map_coordinates(h, [zi, xi], order=1)
    cv = map_coordinates(col_map, [zi, xi], order=1)
    hv = np.where(inb, hv, -1); 
    SY[k] = horizon + (cam_h - hv) / z * scale / 4.2
    CV[k] = cv
    FG[k] = np.clip((z - 0.30) / 0.85, 0, 1) ** 1.5
M = np.minimum.accumulate(SY, axis=0)
img = np.zeros((H, W)); alpha = np.zeros((H, W))
ys = np.arange(H) + 0.5
for c in range(W):
    idx = np.searchsorted(-M[:, c], -ys, side='left')
    ok = idx < len(zs)
    k = np.clip(idx, 0, len(zs) - 1)
    near = np.clip(zs[k] / 0.45, 0.25, 1) ** 1.2
    val = CV[k, c] * near * (1 - FG[k]) + 0.26 * FG[k]
    img[:, c] = np.where(ok, val, 0); alpha[:, c] = ok
np.save('raw.npy', img); np.save('alpha.npy', alpha)
print('ok', img.max(), alpha.mean())
