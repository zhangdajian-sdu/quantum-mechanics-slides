# -*- coding: utf-8 -*-
"""Figures for ch2-s3: Schrödinger equation (§2.3)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
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


# ---------------------------------------------------------------- fig_method
# Hypothesis -> deduction -> experiment loop (methodology of "guessing" the equation)
fig, ax = plt.subplots(figsize=(8.8, 2.6))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)
ax.set_xlim(0, 10)
ax.set_ylim(0, 3)
ax.axis("off")

nodes = [
    (1.7, "提出假设", "（猜出方程）"),
    (5.0, "演绎推论", "（解方程、算预言）"),
    (8.3, "实验检验", "（对照测量结果）"),
]
for x, main, sub in nodes:
    ax.text(x, 2.35, main, ha="center", va="center", fontsize=15, color=INK, weight="bold")
    ax.text(x, 1.78, sub, ha="center", va="center", fontsize=10.5, color=GRAY)

for x0, x1 in [(2.75, 3.95), (6.05, 7.25)]:
    ax.add_patch(FancyArrowPatch((x0, 2.35), (x1, 2.35),
                                 arrowstyle="-|>", mutation_scale=18,
                                 lw=1.6, color=TEAL))

# return loop: experiment back to hypothesis
ax.add_patch(FancyArrowPatch((8.3, 1.45), (1.7, 1.45),
                             connectionstyle="arc3,rad=-0.32",
                             arrowstyle="-|>", mutation_scale=16,
                             lw=1.3, color=OCHRE, linestyle=(0, (5, 3))))
ax.text(5.0, 0.12, "预言不符 → 修正假设，重新来过；全部相符 → 方程被接受（仍只是“没被推翻”）",
        ha="center", va="center", fontsize=10.5, color=OCHRE)

save(fig, "fig_method.png")


# ------------------------------------------------------------------ fig_step
# EXACT scattering solution (E < V0) across a finite potential step:
# psi = cos(k1 x + delta) for x<0, cos(delta) exp(-kappa x) for x>=0,
# delta = arctan(kappa/k1)  =>  psi and psi' continuous, psi'' jumps with V
x = np.linspace(-6, 6, 2000)
V0 = 1.0
V = np.where(x >= 0, V0, 0.0)

k1, kappa = 1.6, 0.85
delta = np.arctan(kappa / k1)
psi_s = np.where(x < 0,
                 np.cos(k1 * x + delta),
                 np.cos(delta) * np.exp(-kappa * x))
dpsi = np.where(x < 0,
                -k1 * np.sin(k1 * x + delta),
                -kappa * np.cos(delta) * np.exp(-kappa * x))

fig, axes = plt.subplots(2, 1, figsize=(7.6, 4.6), sharex=True,
                         gridspec_kw={"height_ratios": [1, 1.6], "hspace": 0.16})
fig.patch.set_facecolor(PAPER)

axV, axP = axes
for ax in axes:
    ax.set_facecolor(PAPER)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRAY)
    ax.tick_params(colors=GRAY, labelsize=9)
    ax.axvline(0, color=HAIRLINE, lw=1.2, zorder=0)

axV.plot(x, V, color=OCHRE, lw=2.0)
axV.set_ylabel(r"$V(x)$", fontsize=11, color=INK)
axV.set_yticks([0, V0])
axV.set_yticklabels(["0", r"$V_0$"], fontsize=10)
axV.set_ylim(-0.25, 1.5)
axV.annotate("势能在 $x=0$ 处有限阶跃", xy=(0.12, 0.6), xytext=(2.1, 1.22),
             fontsize=10.5, color=OCHRE,
             arrowprops=dict(arrowstyle="-", color=OCHRE, lw=0.9))

axP.plot(x, psi_s, color=TEAL, lw=2.0, label=r"$\psi(x)$")
axP.plot(x, dpsi, color=GRAY, lw=1.4, linestyle=(0, (4, 2)), label=r"$\psi\,'(x)$")
axP.axhline(0, color=HAIRLINE, lw=0.8, zorder=0)
axP.set_ylabel(r"$\psi,\ \psi\,'$", fontsize=11, color=INK)
axP.set_xlabel(r"$x$", fontsize=11, color=INK)
axP.set_yticks([])
axP.legend(loc="upper right", fontsize=10, frameon=False)
axP.annotate("$E<V_0$ 的严格解：$\psi$ 与 $\psi\,'$ 连续穿过界面" + "\n" + "（折角只出现在 $\psi\,''$ 上，与 $V$ 的阶跃同步）",
             xy=(0.05, psi_s[1005]), xytext=(-5.7, 1.32),
             fontsize=10.5, color=INK,
             arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.9))
axP.set_ylim(-1.5, 1.75)

save(fig, "fig_step.png")


# ------------------------------------------------- fig_wave_vs_diffusion
# Free Gaussian packet |psi|^2: diffusion-type (no i, area decays) vs
# unitary Schroedinger evolution (packet spreads, area strictly conserved)
x = np.linspace(-6, 6, 1200)

rho0 = np.exp(-x**2)                       # area = sqrt(pi)
rho_diff = 0.42 * np.exp(-x**2 / 1.55**2)  # area ~ 0.65 sqrt(pi)  -> leaks
rho_unit = 0.50 * np.exp(-x**2 / 2.0**2)   # area = 1.00 sqrt(pi)  -> conserved

fig, axes = plt.subplots(1, 2, figsize=(8.8, 2.7))
fig.patch.set_facecolor(PAPER)

for ax in axes:
    ax.set_facecolor(PAPER)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRAY)
    ax.tick_params(colors=GRAY, labelsize=8)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.plot(x, rho0, color=TEAL, lw=2.0, label=r"$t=0$")
    ax.set_ylim(-0.08, 1.2)

axL, axR = axes

axL.plot(x, rho_diff, color=OCHRE, lw=1.8, linestyle=(0, (5, 3)), label=r"$t>0$")
axL.fill_between(x, 0, rho_diff, color=OCHRE, alpha=0.14, lw=0)
axL.set_title("只去掉 i：扩散型", fontsize=12, color=INK, pad=8)
axL.annotate("阴影面积 = 总几率\n随时间漏掉", xy=(1.6, 0.20), xytext=(1.9, 0.72),
             fontsize=10, color=OCHRE,
             arrowprops=dict(arrowstyle="-", color=OCHRE, lw=0.9))
axL.legend(loc="upper left", fontsize=9, frameon=False)

axR.plot(x, rho_unit, color=OCHRE, lw=1.8, linestyle=(0, (5, 3)), label=r"$t>0$")
axR.fill_between(x, 0, rho_unit, color=TEAL, alpha=0.14, lw=0)
axR.set_title("带上 i：幺正演化", fontsize=12, color=INK, pad=8)
axR.annotate("波包展宽、变矮\n阴影面积严格不变", xy=(2.1, 0.25), xytext=(2.15, 0.78),
             fontsize=10, color=TEAL,
             arrowprops=dict(arrowstyle="-", color=TEAL, lw=0.9))
axR.legend(loc="upper left", fontsize=9, frameon=False)

fig.tight_layout()
save(fig, "fig_wave_vs_diffusion.png")


# ------------------------------------------------- fig_atom
# Z-electron atom: nucleus at origin, electron distances r_i and r_ij
fig, ax = plt.subplots(figsize=(5.0, 3.5))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)
ax.set_xlim(-3.4, 3.4)
ax.set_ylim(-2.45, 2.45)
ax.set_aspect("equal")
ax.axis("off")

# orbit guide
orbit = plt.Circle((0, 0), 2.0, fill=False, color=HAIRLINE, lw=1.2, linestyle=(0, (4, 3)))
ax.add_patch(orbit)

# nucleus
ax.add_patch(plt.Circle((0, 0), 0.30, color=OCHRE, zorder=5))
ax.text(0, -0.72, "核（$+Ze$，置于原点）", ha="center", va="top", fontsize=10.5, color=OCHRE)

# electrons
angles = np.deg2rad([28, 118, 208, 298])
pts = [np.array([2.0 * np.cos(a), 2.0 * np.sin(a)]) for a in angles]
for p in pts:
    ax.add_patch(plt.Circle(p, 0.13, color=TEAL, zorder=6))
ax.text(pts[3][0] + 0.28, pts[3][1] - 0.34, "电子（$-e$）", fontsize=10.5, color=TEAL)

# r_i : origin -> electron 0
p0 = pts[0]
ax.plot([0, p0[0]], [0, p0[1]], color=INK, lw=1.3, zorder=4)
ax.text(p0[0] * 0.52 + 0.1, p0[1] * 0.52 + 0.18, r"$r_i$", fontsize=13, color=INK)

# r_ij : electron 0 -> electron 1
p1 = pts[1]
ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=GRAY, lw=1.2, linestyle=(0, (4, 2)), zorder=4)
mid = (p0 + p1) / 2
ax.text(mid[0] + 0.14, mid[1] + 0.16, r"$r_{ij}$", fontsize=13, color=GRAY)

save(fig, "fig_atom.png")


# ------------------------------------------------- fig_cover
# Cover artwork: two-source interference ripples on the teal cover background
from matplotlib.colors import LinearSegmentedColormap

yy, xx = np.mgrid[-5:5:640j, -4.2:4.2:560j]
a = 1.15
r1 = np.hypot(xx, yy - a)
r2 = np.hypot(xx, yy + a)
inten = np.cos(6.5 * (r1 - r2) / 2) ** 2
fade = np.exp(-(np.hypot(xx, yy) / 7.5) ** 2)
img = inten * (0.18 + 0.82 * fade) * 0.9

cmap = LinearSegmentedColormap.from_list(
    "wave", ["#1F4E5F", "#2F6375", "#5E93A3", "#A9C9D2", "#E4ECE9"])

fig = plt.figure(figsize=(4.2, 5.0))
fig.patch.set_facecolor(TEAL)
ax = fig.add_axes([0, 0, 1, 1])
ax.imshow(img, cmap=cmap, origin="lower", extent=[-4.2, 4.2, -5, 5],
          interpolation="bilinear")
ax.plot([0, 0], [a, -a], "o", color=OCHRE, ms=7)
ax.set_xlim(-4.2, 4.2)
ax.set_ylim(-5, 5)
ax.axis("off")

fig.savefig(OUT / "fig_cover.png", dpi=170, facecolor=TEAL)
plt.close(fig)
print("saved fig_cover.png")

print("done")
