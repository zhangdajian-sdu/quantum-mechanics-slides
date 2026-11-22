import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot

setup_plot()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse

MEDIA = Path(__file__).parent / "media"
MEDIA.mkdir(exist_ok=True)

TEAL = "#1F4E5F"
OCHRE = "#C4622D"
INK = "#20242B"
PAPER = "#FAF8F4"
GRAY = "#8A8F98"

# ---------- fig_cover.png : 双体环绕示意图（深 teal 底，融入封面） ----------
fig, ax = plt.subplots(figsize=(6.4, 7.64), dpi=100)
fig.patch.set_facecolor(TEAL)
ax.set_facecolor(TEAL)

t = np.linspace(0, 2 * np.pi, 400)
# 两条环绕质心的椭圆轨道（半长轴按质量反比 2:1）
for a, b, col, lw, alpha in [(2.4, 1.5, "#FFFFFF", 1.4, 0.55), (1.2, 0.75, OCHRE, 1.4, 0.9)]:
    ax.plot(a * np.cos(t), b * np.sin(t), color=col, lw=lw, alpha=alpha)

# 某一时刻：两粒子在过质心的一条直线上（经典两体的瞬时位形）
th = np.deg2rad(38)
p1 = np.array([2.4 * np.cos(th), 1.5 * np.sin(th)])      # 小粒子（远）
p2 = np.array([-1.2 * np.cos(th), -0.75 * np.sin(th)])   # 大粒子（近）

ax.plot([p1[0], p2[0]], [p1[1], p2[1]], ls="--", color="#FFFFFF", lw=1.2, alpha=0.7)
ax.scatter(*p1, s=150, color="#FFFFFF", zorder=5, edgecolors="#FFFFFF")
ax.scatter(*p2, s=420, color=OCHRE, zorder=5, edgecolors="#FFD9C2", linewidths=1.2)
ax.scatter(0, 0, s=70, marker="*", color="#F2C14E", zorder=6)

ax.annotate("m$_1$", p1 + [0.16, 0.22], color="#FFFFFF", fontsize=15)
ax.annotate("m$_2$", p2 + [-0.75, -0.1], color="#FFD9C2", fontsize=15)
ax.annotate("质心", (0.14, 0.30), color="#F2C14E", fontsize=13)

# 相对位矢箭头：从 m2 指向 m1
ax.annotate("", xy=p1 - 0.06 * (p1 - p2), xytext=p2 + 0.06 * (p1 - p2),
            arrowprops=dict(arrowstyle="-|>", color="#9FD4D9", lw=1.6))
mid = (p1 + p2) / 2 + np.array([0.42, -0.28])
ax.annotate(r"$\boldsymbol{r}=\boldsymbol{r}_1-\boldsymbol{r}_2$", mid,
            color="#9FD4D9", fontsize=13.5)

ax.set_xlim(-3.1, 3.1)
ax.set_ylim(-3.65, 3.65)
ax.set_aspect("equal")
ax.axis("off")
fig.savefig(MEDIA / "fig_cover.png", bbox_inches="tight", facecolor=TEAL)
plt.close(fig)

# ---------- fig_coords.png : 质心坐标与相对坐标的矢量图（paper 底） ----------
fig, ax = plt.subplots(figsize=(8.0, 5.0), dpi=100)
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

O = np.array([0.0, 0.0])
r2 = np.array([1.7, 2.7])      # 大质量粒子 m2
r1 = np.array([5.7, 1.2])      # 小质量粒子 m1
# 质量比 m2:m1 = 2:1 -> 质心在连线上 1/3 处（靠 m2）
m1, m2 = 1.0, 2.0
R = (m1 * r1 + m2 * r2) / (m1 + m2)

def arrow(p, q, col, lw=2.0, label=None, off=(0, 0), fs=15):
    ax.annotate("", xy=q, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=col, lw=lw,
                                shrinkA=0, shrinkB=0))
    if label:
        ax.annotate(label, (p + q) / 2 + np.array(off), color=col, fontsize=fs)

arrow(O, r1, TEAL, label=r"$\boldsymbol{r}_1$", off=(0.10, -0.42))
arrow(O, r2, TEAL, label=r"$\boldsymbol{r}_2$", off=(-0.42, -0.02))
arrow(O, R, OCHRE, lw=2.4, label=r"$\boldsymbol{R}$", off=(-0.15, 0.22))
arrow(r2, r1, GRAY, lw=1.6, label=r"$\boldsymbol{r}=\boldsymbol{r}_1-\boldsymbol{r}_2$", off=(0.6, -0.62), fs=13.5)

ax.plot([r1[0], r2[0]], [r1[1], r2[1]], ls=":", color=GRAY, lw=1.0)
ax.scatter(*r1, s=170, color=TEAL, zorder=5)
ax.scatter(*r2, s=380, color=TEAL, zorder=5)
ax.scatter(*R, s=110, marker="*", color=OCHRE, zorder=6)
ax.annotate("$m_1$", r1 + [0.18, 0.10], fontsize=15, color=INK)
ax.annotate("$m_2$", r2 + [-0.10, 0.22], fontsize=15, color=INK)
ax.annotate("质心", R + [0.14, 0.14], fontsize=13.5, color=OCHRE)
ax.annotate("O", O + [-0.26, -0.05], fontsize=14, color=INK)

ax.set_xlim(-0.5, 7.3)
ax.set_ylim(-0.6, 4.6)
ax.set_aspect("equal")
ax.axis("off")
fig.savefig(MEDIA / "fig_coords.png", bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

print("figures done:", [p.name for p in MEDIA.glob("*.png")])
