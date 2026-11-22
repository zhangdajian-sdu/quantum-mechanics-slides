# -*- coding: utf-8 -*-
"""Figures for ch2-s4: probability conservation and current density (§2.4)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
from daimon_runtime import setup_plot

setup_plot()

PAPER = "#FAF8F4"
INK = "#20242B"
TEAL = "#1F4E5F"
OCHRE = "#C4622D"
GRAY = "#8A8F98"
HAIRLINE = "#E2DFD8"

OUT = Path(__file__).parent / "media"
OUT.mkdir(exist_ok=True)


def save(fig, name):
    fig.savefig(OUT / name, dpi=160, facecolor=PAPER, bbox_inches="tight")
    plt.close(fig)
    print("saved", name)


# ------------------------------------------------------------------ fig_flux
# Closed surface S enclosing volume V, probability current flowing through
fig, ax = plt.subplots(figsize=(7.2, 4.4))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.2)
ax.axis("off")
ax.set_aspect("equal")

cx, cy, R = 5.0, 3.0, 1.85
ax.add_patch(Circle((cx, cy), R, fill=True, facecolor="#F3F1EA",
                    edgecolor=TEAL, lw=1.6, linestyle=(0, (5, 3)), zorder=1))
ax.text(cx, cy + 0.1, "V", fontsize=17, color=TEAL, ha="center", va="center", zorder=3)
ax.text(cx + 1.28, cy + 1.62, "S", fontsize=15, color=TEAL, ha="center", va="center")

# streamlines crossing the surface
ys = [4.35, 3.0, 1.65]
for y in ys:
    ax.add_patch(FancyArrowPatch((0.6, y + 0.35), (9.4, y - 0.35),
                                 connectionstyle="arc3,rad=-0.06",
                                 arrowstyle="-", lw=1.7, color=GRAY, zorder=2))
    ax.add_patch(FancyArrowPatch((4.7, y + 0.10), (6.1, y - 0.06),
                                 connectionstyle="arc3,rad=-0.06",
                                 arrowstyle="-|>", mutation_scale=17,
                                 lw=1.7, color=GRAY, zorder=4))

ax.annotate("", xy=(1.15, 5.05), xytext=(1.15, 4.35))
ax.text(0.62, 4.62, r"$\mathbf{j}$", fontsize=15, color=INK, ha="center")

# surface element with outward normal
ang = np.deg2rad(38)
px, py = cx + R * np.cos(ang), cy + R * np.sin(ang)
nx, ny = np.cos(ang), np.sin(ang)
ax.add_patch(FancyArrowPatch((px, py), (px + 1.0 * nx, py + 1.0 * ny),
                             arrowstyle="-|>", mutation_scale=15,
                             lw=1.5, color=OCHRE, zorder=5))
ax.text(px + 1.25 * nx, py + 1.25 * ny, r"$\mathrm{d}\mathbf{s}$", fontsize=13,
        color=OCHRE, ha="left", va="center")

ax.text(5.0, 0.35, "单位时间内 V 中几率的增加 = 由 S 外流入 S 内的几率",
        fontsize=11.5, color=INK, ha="center")

save(fig, "fig_flux.png")


# ----------------------------------------------------------------- fig_waves
# Standing wave (real psi, j=0) vs travelling wave (j = rho v)
x = np.linspace(0, 4 * np.pi, 1200)
k = 1.6

fig, axes = plt.subplots(1, 2, figsize=(8.8, 3.1))
fig.patch.set_facecolor(PAPER)

for ax, mode in zip(axes, ("standing", "travelling")):
    ax.set_facecolor(PAPER)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRAY)
    ax.tick_params(colors=GRAY, labelsize=8)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axhline(0, color=HAIRLINE, lw=0.9, zorder=0)
    ax.set_xlim(0, 4 * np.pi)
    ax.set_ylim(-1.7, 1.9)

axS, axT = axes
axS.plot(x, np.cos(k * x), color=TEAL, lw=1.9)
axS.set_title(r"$\psi = \cos kx$（实函数，驻波）", fontsize=11.5, color=INK, pad=8)
axS.text(np.pi * 2, -1.5, r"$\mathbf{j}=0$：向 $+x$ 与 $-x$ 运动的几率相等",
         fontsize=10.5, color=OCHRE, ha="center")

axT.plot(x, np.cos(k * x), color=TEAL, lw=1.9)
axT.plot(x, np.ones_like(x), color=OCHRE, lw=1.5, linestyle=(0, (4, 2)))
axT.set_title(r"$\psi = \mathrm{e}^{\mathrm{i}kx}$（行波）", fontsize=11.5, color=INK, pad=8)
axT.text(12.05, 1.13, r"$|\psi|^{2}=1$", fontsize=10, color=OCHRE, ha="right")
axT.text(12.05, -0.95, r"$\mathrm{Re}\,\psi$", fontsize=10, color=TEAL, ha="right")
for xa in (1.1, 3.4, 5.7, 8.0, 10.3):
    axT.add_patch(FancyArrowPatch((xa, 1.55), (xa + 1.1, 1.55),
                                  arrowstyle="-|>", mutation_scale=13,
                                  lw=1.4, color=GRAY))
axT.text(np.pi * 2, -1.5, r"$\mathbf{j}=\dfrac{p}{\mu}\,|\psi|^{2}$：沿 $+x$ 方向的几率流",
         fontsize=10.5, color=OCHRE, ha="center")

fig.subplots_adjust(wspace=0.18)
save(fig, "fig_waves.png")

# ------------------------------------------------- fig_cover
# Cover artwork: divergence-free probability current flowing across the frame,
# with an ochre dashed closed surface — "what flows in must flow out"
from matplotlib.colors import LinearSegmentedColormap

yy, xx = np.mgrid[-5:5:640j, -4.2:4.2:560j]

# streamfunction => divergence-free field (no sources or sinks)
x0, y0, s2, A = -1.2, 0.8, 4.0, 1.6
r2 = (xx - x0) ** 2 + (yy - y0) ** 2
bump = A * np.exp(-r2 / s2)
u = 1.0 - 2 * (yy - y0) / s2 * bump
v = 2 * (xx - x0) / s2 * bump
speed = np.hypot(u, v)

fig = plt.figure(figsize=(4.2, 5.0))
fig.patch.set_facecolor(TEAL)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor(TEAL)

# soft teal glow backdrop
glow = np.exp(-(np.hypot(xx - 0.6, yy + 0.4) / 4.5) ** 2)
cmap_bg = LinearSegmentedColormap.from_list(
    "bg", ["#1A4353", "#1F4E5F", "#28596B", "#36707F"])
ax.imshow(glow, cmap=cmap_bg, origin="lower", extent=[-4.2, 4.2, -5, 5],
          interpolation="bilinear", vmin=0, vmax=1)

# luminous streamlines, thicker where the current is faster
lw = 0.7 + 2.1 * (speed / speed.max())
ax.streamplot(xx, yy, u, v, density=1.05, color="#DCE9E666", linewidth=lw,
              arrowstyle="-", broken_streamlines=False)

# the closed surface S (dashed ochre circle)
ax.add_patch(Circle((0.9, -0.6), 1.35, fill=False, edgecolor=OCHRE,
                    lw=2.2, linestyle=(0, (5, 4)), zorder=5))

ax.set_xlim(-4.2, 4.2)
ax.set_ylim(-5, 5)
ax.axis("off")

fig.savefig(OUT / "fig_cover.png", dpi=170, facecolor=TEAL)
plt.close(fig)
print("saved fig_cover.png")

print("done")
