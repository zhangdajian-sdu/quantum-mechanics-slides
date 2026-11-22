import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot

setup_plot()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
from scipy.special import lpmv

INK = "#20242B"
TEAL = "#1F4E5F"
OCHRE = "#C4622D"
GRAY = "#8A8F98"
PAPER = "#FAF8F4"
LIGHT = "#DCE6EA"
PANEL_TEAL = "#23586B"

MEDIA = Path(__file__).parent / "media"
MEDIA.mkdir(exist_ok=True)


def newfig(w, h, facecolor=PAPER):
    fig = plt.figure(figsize=(w, h), dpi=200)
    fig.patch.set_facecolor(facecolor)
    return fig


# ---------------------------------------------------------------- fig_cover
# 空间量子化：l = 2 时 L 的 5 个允许取向
fig = newfig(4.8, 5.7, PANEL_TEAL)
ax = fig.add_axes([0.06, 0.04, 0.88, 0.90])
ax.set_facecolor(PANEL_TEAL)

l = 2
Lmag = np.sqrt(l * (l + 1))  # sqrt(6) ~ 2.449

# dashed reference circle
th = np.linspace(0, 2 * np.pi, 400)
ax.plot(Lmag * np.cos(th), Lmag * np.sin(th), ls=(0, (4, 4)),
        color="#FFFFFF55", lw=1.2)

# axes
ax.annotate("", xy=(0, 3.15), xytext=(0, -3.15),
            arrowprops=dict(arrowstyle="-|>", color="#FFFFFFAA", lw=1.4))
ax.annotate("", xy=(3.15, 0), xytext=(-3.15, 0),
            arrowprops=dict(arrowstyle="-|>", color="#FFFFFF66", lw=1.1))
ax.text(0.10, 3.18, r"$L_z$", color="white", fontsize=13)
ax.text(3.20, -0.32, r"$L_x$", color="#FFFFFFAA", fontsize=12)

# m levels and vectors
for m in range(-l, l + 1):
    cosang = m / Lmag
    # horizontal dashed guide at z = m
    xmax = np.sqrt(Lmag**2 - m**2)
    ax.plot([-xmax, xmax], [m, m], ls=(0, (2, 3)), color="#FFFFFF33", lw=0.9)
    # allowed direction in the x-z plane (take +x side)
    ax.annotate("", xy=(xmax, m), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="#F2B27E", lw=2.0))
    ax.text(-0.16, m + 0.14, rf"$m={m}$" if m >= 0 else rf"$m={m}$",
            color="white", fontsize=10.5, ha="right")

ax.text(0, -3.75, r"$|\mathbf{L}|=\sqrt{l(l+1)}\,\hbar=\sqrt{6}\,\hbar$",
        color="white", fontsize=12.5, ha="center")
ax.text(0, 3.62, r"$l=2$：只有 $2l+1=5$ 个允许取向",
        color="white", fontsize=12.5, ha="center")

ax.set_xlim(-3.4, 3.6)
ax.set_ylim(-4.05, 4.0)
ax.set_aspect("equal")
ax.axis("off")
fig.savefig(MEDIA / "fig_cover.png", facecolor=PANEL_TEAL)
plt.close(fig)

# ---------------------------------------------------------------- fig_intro
# 双原子分子转动：能级 l(l+1)ε 与等间距转动谱线
fig = newfig(8.3, 5.9)

# left: energy ladder
ax1 = fig.add_axes([0.075, 0.12, 0.40, 0.76])
ax1.set_facecolor(PAPER)
levels = list(range(0, 5))
for l in levels:
    E = l * (l + 1)
    ax1.plot([0.10, 0.62], [E, E], color=TEAL, lw=2.4)
    ax1.text(0.065, E, rf"$l={l}$", ha="right", va="center",
             fontsize=11.5, color=INK)
    ax1.text(0.64, E, rf"$E_l={E}\varepsilon$" if l > 0 else r"$E_0=0$",
             ha="left", va="center", fontsize=11.5, color=INK)
# transitions l -> l-1
for l in range(1, 5):
    E2, E1 = l * (l + 1), (l - 1) * l
    ax1.annotate("", xy=(0.36, E1), xytext=(0.36, E2),
                 arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=1.6))
    ax1.text(0.385, (E1 + E2) / 2, rf"${2*l}\varepsilon$", fontsize=10.5,
             color=OCHRE, va="center")
ax1.set_ylim(-1.2, 22.5)
ax1.set_xlim(-0.28, 1.35)
ax1.axis("off")
ax1.set_title("转动能级  $E_l=l(l+1)\\varepsilon$", fontsize=13, color=INK, pad=10)

# right: stick spectrum, equally spaced
ax2 = fig.add_axes([0.55, 0.12, 0.42, 0.76])
ax2.set_facecolor(PAPER)
xs = [2, 4, 6, 8]
hs = [0.62, 1.00, 0.80, 0.45]
for x, h in zip(xs, hs):
    ax2.plot([x, x], [0, h], color=TEAL, lw=3.2, solid_capstyle="round")
    ax2.text(x, h + 0.045, rf"${x}\varepsilon$", ha="center", fontsize=11, color=INK)
# spacing braces
for x0 in [2, 4, 6]:
    ax2.annotate("", xy=(x0 + 2, 1.24), xytext=(x0, 1.24),
                 arrowprops=dict(arrowstyle="<->", color=OCHRE, lw=1.3))
    ax2.text(x0 + 1, 1.30, r"$2\varepsilon$", ha="center", fontsize=10.5, color=OCHRE)
ax2.set_ylim(0, 1.5)
ax2.set_xlim(0.4, 9.6)
ax2.set_yticks([])
ax2.set_xticks(xs)
ax2.set_xticklabels([rf"${x}\varepsilon$" for x in xs], fontsize=10.5, color=GRAY)
for s in ["left", "right", "top"]:
    ax2.spines[s].set_visible(False)
ax2.spines["bottom"].set_color(GRAY)
ax2.set_title("转动光谱：谱线等间距", fontsize=13, color=INK, pad=10)

fig.savefig(MEDIA / "fig_intro.png", facecolor=PAPER, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- fig_cone
# 角动量锥面：L² 与 Lz 确定，Lx Ly 不确定
fig = newfig(7.2, 5.0)
ax = fig.add_axes([0.02, 0.04, 0.56, 0.90])
ax.set_facecolor(PAPER)

Lz = 1.55
Lmag = 2.45
r = np.sqrt(Lmag**2 - Lz**2)

# z axis
ax.annotate("", xy=(0, 3.15), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.4))
ax.text(0.10, 3.08, r"$L_z$", fontsize=13, color=INK)

# cone side lines
ax.plot([-r, 0, r], [Lz, 0, Lz], color="#8A8F9866", lw=1.0)
# precession circle (dashed) at z = Lz
ax.add_patch(Circle((0, Lz), r, fill=False, ls=(0, (4, 4)),
                    ec=OCHRE, lw=1.7))
# L2 sphere circle faint
ax.add_patch(Circle((0, 0), Lmag, fill=False, ls=(0, (2, 4)),
                    ec="#8A8F9855", lw=1.0))

# several possible L vectors on the cone
for ang_deg, alpha in [(205, 0.35), (300, 0.35), (40, 1.0)]:
    a = np.deg2rad(ang_deg)
    ax.annotate("", xy=(r * np.cos(a), Lz), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2.0,
                                alpha=alpha))
# z component guide
ax.plot([0, 0], [0, Lz], color=GRAY, lw=1.2)
ax.plot([0, r * np.cos(np.deg2rad(40))], [Lz, Lz], ls=(0, (2, 3)),
        color=GRAY, lw=1.0)

ax.set_xlim(-2.85, 2.85)
ax.set_ylim(-0.55, 3.45)
ax.set_aspect("equal")
ax.axis("off")

# right-side legend notes
fig.text(0.615, 0.74, r"$|\mathbf{L}|=\sqrt{l(l+1)}\,\hbar$", fontsize=13.5, color=TEAL)
fig.text(0.615, 0.665, "长度确定", fontsize=11.5, color=INK)
fig.text(0.615, 0.50, r"$L_z=m\hbar$", fontsize=13.5, color=INK)
fig.text(0.615, 0.425, "z 分量确定", fontsize=11.5, color=INK)
fig.text(0.615, 0.26, r"$L_x,\ L_y$", fontsize=13.5, color=OCHRE)
fig.text(0.615, 0.175, "不确定——矢量端点在\n锥面圆环上进动", fontsize=11.5, color=INK,
         va="bottom")

fig.savefig(MEDIA / "fig_cone.png", facecolor=PAPER, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- fig_ylm
# 球谐函数花瓣图：|P_l^m(cos θ)| 极坐标网格
pairs = [(0, 0), (1, 0), (1, 1), (2, 0), (2, 1), (2, 2),
         (3, 0), (3, 1), (3, 2), (3, 3)]
fig = newfig(8.6, 6.2, PANEL_TEAL)
th = np.linspace(0, 2 * np.pi, 720)

for i, (l, m) in enumerate(pairs):
    ax = fig.add_axes([0.04 + (i % 5) * 0.196, 0.54 - (i // 5) * 0.47, 0.16, 0.38],
                      projection="polar")
    ax.set_facecolor(PANEL_TEAL)
    r = np.abs(lpmv(m, l, np.cos(th)))
    if r.max() > 0:
        r = r / r.max()
    ax.plot(th, r, color="#F2B27E", lw=1.8)
    ax.fill(th, r, color="#F2B27E", alpha=0.30)
    ax.set_rticks([])
    ax.set_xticks([])
    ax.spines["polar"].set_color("#FFFFFF2E")
    ax.grid(color="#FFFFFF14", lw=0.5)
    ax.set_title(rf"$|Y_{{{l}{m}}}|\;(l={l},\,m={m})$".replace("{", "{").replace("}", "}"),
                 color="white", fontsize=10, pad=6)

fig.text(0.5, 0.955, "球谐函数的「花瓣」：$|Y_{lm}(\\theta,\\varphi)|$ 随 $\\theta$ 的分布",
         color="white", fontsize=13, ha="center")
fig.savefig(MEDIA / "fig_ylm.png", facecolor=PANEL_TEAL)
plt.close(fig)

print("done:", sorted(p.name for p in MEDIA.glob("*.png")))
