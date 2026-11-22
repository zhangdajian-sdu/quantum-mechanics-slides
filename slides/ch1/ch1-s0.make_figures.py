"""ch1-s0 课程导论 全部插图"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
setup_plot()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

OUT = Path(__file__).parent / "media"
OUT.mkdir(exist_ok=True)

INK = "#20242B"
TEAL = "#1F4E5F"
OCHRE = "#C4622D"
GRAY = "#8A8F98"
PAPER = "#FAF8F4"

# ---------------------------------------------------------------- cover
# 竖向题图：箱中驻波(n=1..4) + 黑体辐射曲线，墨绿-橙褐配色
fig, ax = plt.subplots(figsize=(3.4, 5.4))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

x = np.linspace(0, 1, 400)
levels = [(1, 0.16), (2, 0.36), (3, 0.56), (4, 0.76)]
for n, y0 in levels:
    psi = np.sin(n * np.pi * x) * 0.075
    ax.axhline(y0, color=GRAY, lw=0.7, alpha=0.55, zorder=1)
    ax.plot(x, y0 + psi, color=TEAL, lw=1.6, zorder=3)
    ax.fill_between(x, y0, y0 + psi, color=TEAL, alpha=0.16, zorder=2)
    ax.text(1.045, y0, f"n={n}", va="center", ha="left",
            fontsize=10, color=INK)

# 底部黑体辐射型曲线
t = np.linspace(0.02, 1, 300)
bb = t**3 / (np.exp(4.6 * t) - 1)
bb = bb / bb.max() * 0.10
ax.plot(t, 0.045 + bb, color=OCHRE, lw=1.8, zorder=3)
ax.fill_between(t, 0.045, 0.045 + bb, color=OCHRE, alpha=0.15, zorder=2)
ax.axhline(0.045, color=GRAY, lw=0.7, alpha=0.55)
ax.text(1.045, 0.045, "热辐射", va="center", ha="left", fontsize=9, color=OCHRE)

ax.set_xlim(0, 1.22)
ax.set_ylim(0, 0.94)
ax.axis("off")
fig.savefig(OUT / "fig_cover.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

# ---------------------------------------------------------------- quantum corral
# 量子围栏示意：48 个 Fe 原子围成圆圈 + 内部电子驻波波纹
fig, ax = plt.subplots(figsize=(6.4, 4.8))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

# 内部驻波（贝塞尔型径向波纹）
R = 1.0
yy, xx = np.mgrid[-1.05:1.05:400j, -1.05:1.05:400j]
rr = np.sqrt(xx**2 + yy**2)
from scipy.special import j0, jn_zeros
z = jn_zeros(0, 3)[-1]
field = j0(z * rr / R) * (rr <= R)
ax.imshow(field, extent=(-1.05, 1.05, -1.05, 1.05), cmap="cividis",
          alpha=0.85, zorder=1, interpolation="bilinear")

# 48 个铁原子
theta = np.linspace(0, 2 * np.pi, 49)[:-1]
ax.scatter(R * np.cos(theta), R * np.sin(theta), s=52, color=OCHRE,
           edgecolors=INK, linewidths=0.5, zorder=3)
ax.text(0, -1.32, "48 个 Fe 原子在 Cu(111) 表面围成的「量子围栏」（示意）",
        ha="center", fontsize=10.5, color=GRAY)

ax.set_xlim(-1.25, 1.25)
ax.set_ylim(-1.45, 1.25)
ax.set_aspect("equal")
ax.axis("off")
fig.savefig(OUT / "fig_corral.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

# ---------------------------------------------------------------- timeline
# 量子力学发展史时间线 1900–1930
fig, ax = plt.subplots(figsize=(12.4, 3.6))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

events_up = [
    (1900, "普朗克", "振子能量量子化", 0.0),
    (1913, "玻尔", "原子能量量子化", 0.0),
    (1925, "海森伯", "矩阵力学", -2.0),
    (1927, "海森伯", "不确定关系", 1.6),
]
events_dn = [
    (1905, "爱因斯坦", "光量子假设", 0.0),
    (1924, "德布罗意", "物质波假设", -1.6),
    (1926, "薛定谔", "波动方程", 1.8),
]
x0, x1 = 1897, 1931
ax.axhline(0, color=INK, lw=1.6, zorder=2)
ax.annotate("", xy=(x1 + 0.8, 0), xytext=(x1, 0),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6))

for yr, who, what, dx in events_up:
    ax.plot([yr], [0], "o", ms=7, color=TEAL, zorder=4)
    ax.plot([yr, yr], [0, 0.55], color=TEAL, lw=1.0, alpha=0.6, zorder=3)
    ax.text(yr + dx, 0.62, f"{yr}", ha="center", fontsize=11, color=TEAL, weight="bold")
    ax.text(yr + dx, 0.92, f"{who}", ha="center", fontsize=10.5, color=INK, weight="bold")
    ax.text(yr + dx, 1.16, what, ha="center", fontsize=9.5, color=GRAY)

for yr, who, what, dx in events_dn:
    ax.plot([yr], [0], "o", ms=7, color=OCHRE, zorder=4)
    ax.plot([yr, yr], [0, -0.55], color=OCHRE, lw=1.0, alpha=0.6, zorder=3)
    ax.text(yr + dx, -0.70, f"{yr}", ha="center", fontsize=11, color=OCHRE, weight="bold")
    ax.text(yr + dx, -1.02, f"{who}", ha="center", fontsize=10.5, color=INK, weight="bold")
    ax.text(yr + dx, -1.28, what, ha="center", fontsize=9.5, color=GRAY)

ax.set_xlim(x0 - 0.5, x1 + 1.2)
ax.set_ylim(-1.5, 1.42)
ax.axis("off")
fig.savefig(OUT / "fig_timeline.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

print("done:", [p.name for p in OUT.glob("*.png")])
