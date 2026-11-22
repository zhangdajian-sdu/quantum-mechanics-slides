import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
import numpy as np
import matplotlib.pyplot as plt
from daimon_runtime import setup_plot

setup_plot()

INK = "#20242B"
TEAL = "#1F4E5F"
OCHRE = "#C4622D"
GRAY = "#8A8F98"
PAPER = "#FAF8F4"
HAIR = "#E2DFD8"

OUT = Path(__file__).parent / "media"
OUT.mkdir(exist_ok=True)


def save(fig, name):
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print("saved", name)


# ---------- 封面：核 + 两电子云 + e^2/r12（teal 底，竖版） ----------
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)

# 电子云：以核为中心的 1s 型径向密度（用等高线晕染）
xg = np.linspace(-4, 4, 400)
X, Y = np.meshgrid(xg, xg)
R = np.sqrt(X ** 2 + Y ** 2)
cloud = np.exp(-R / 1.1)
ax.contourf(X, Y, cloud, levels=14, cmap=plt.cm.Blues, alpha=0.55)

# 核
ax.plot(0, 0, "o", ms=13, color="#E8B48C", mec="#FAF8F4", mew=1.4)
ax.text(0, 0, "+2e", color=TEAL, fontsize=11, ha="center", va="center", weight="bold")

# 两个电子
th1, th2 = np.deg2rad(38), np.deg2rad(218)
r_e = 1.55
e1 = (r_e * np.cos(th1), r_e * np.sin(th1))
e2 = (r_e * np.cos(th2), r_e * np.sin(th2))
ax.plot(*e1, "o", ms=10, color="#FAF8F4")
ax.plot(*e2, "o", ms=10, color="#FAF8F4")
ax.text(e1[0] + 0.42, e1[1] + 0.30, "电子 1", color="#FAF8F4", fontsize=12)
ax.text(e2[0] + 0.42, e2[1] - 0.42, "电子 2", color="#FAF8F4", fontsize=12)

# r12 虚线
ax.plot([e1[0], e2[0]], [e1[1], e2[1]], ls="--", lw=1.6, color="#E8B48C")
ax.text(-1.62, 0.62, r"$r_{12}$", color="#E8B48C", fontsize=15)
ax.text(0, -3.55, r"$\hat{H}^{\prime}=\dfrac{e^{2}}{r_{12}}$", color="#FAF8F4",
        fontsize=17, ha="center")

ax.set_xlim(-4.1, 4.1); ax.set_ylim(-4.1, 4.1)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- 基态能量：零级 → 一级近似 → 实验值 ----------
fig, ax = plt.subplots(figsize=(7.8, 3.3), facecolor=PAPER)
ax.set_facecolor(PAPER)

levels = [
    (0.4, 2.6, -108.8, r"$E^{(0)}=-\dfrac{4e^{2}}{a}=-108.8$ eV", INK, "-"),
    (3.6, 5.8, -74.8, r"$E^{(0)}+E^{(1)}=-\dfrac{11e^{2}}{4a}=-74.8$ eV", TEAL, "-"),
    (6.8, 9.0, -79.0, r"实验值 $-79.0$ eV", GRAY, "--"),
]
for x0, x1, E, lab, c, ls in levels:
    ax.plot([x0, x1], [E, E], ls, color=c, lw=2.4)
    ax.text((x0 + x1) / 2, E + 2.2, lab, ha="center", fontsize=11.5, color=c)

ax.annotate("", xy=(3.3, -74.8), xytext=(3.3, -108.8),
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=1.8))
ax.text(3.42, -95, r"$+\,\dfrac{5e^{2}}{4a}$", color=OCHRE, fontsize=12)

ax.annotate("", xy=(7.9, -79.0), xytext=(7.9, -74.8),
            arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.2))
ax.text(8.02, -76.4, "差 5%", color=GRAY, fontsize=10)

ax.set_xlim(0, 9.8); ax.set_ylim(-118, -62)
ax.set_yticks([]); ax.set_xticks([])
ax.set_ylabel("E", fontsize=12, color=INK)
for s in ["top", "right", "bottom"]:
    ax.spines[s].set_visible(False)
fig.tight_layout()
save(fig, "fig_ground.png")


# ---------- K 与 J：库仑积分 vs 交换积分 ----------
fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.3), facecolor=PAPER)
x = np.linspace(0, 10, 800)


def gauss(x, x0, s, a=1.0):
    return a * np.exp(-((x - x0) ** 2) / (2 * s ** 2))


# K：两团电荷的静电排斥
ax = axes[0]; ax.set_facecolor(PAPER)
d1 = gauss(x, 3.2, 0.9)
d2 = gauss(x, 6.8, 0.9)
ax.fill_between(x, d1 * 3.0, color=TEAL, alpha=0.30)
ax.fill_between(x, d2 * 3.0, color=TEAL, alpha=0.30)
ax.plot(x, d1 * 3.0, color=TEAL, lw=2.2)
ax.plot(x, d2 * 3.0, color=TEAL, lw=2.2)
ax.text(3.2, 3.25, r"$|\varphi_a(\boldsymbol{r}_1)|^2$", fontsize=11, color=TEAL, ha="center")
ax.text(6.8, 3.25, r"$|\varphi_b(\boldsymbol{r}_2)|^2$", fontsize=11, color=TEAL, ha="center")
ax.annotate("", xy=(6.2, 1.55), xytext=(3.8, 1.55),
            arrowprops=dict(arrowstyle="<->", color=OCHRE, lw=1.6))
ax.text(5.0, 1.72, r"$\dfrac{e^{2}}{r_{12}}$", fontsize=12, color=OCHRE, ha="center")
ax.set_title("库仑积分 K：两团电荷的静电能", fontsize=12, color=INK)
ax.set_xlim(0, 10); ax.set_ylim(0, 3.9)

# J：交换积分靠重叠区
ax = axes[1]; ax.set_facecolor(PAPER)
w1 = gauss(x, 4.2, 1.15)
w2 = gauss(x, 5.8, 1.15)
ax.plot(x, w1 * 3.0, color=TEAL, lw=2.2)
ax.plot(x, w2 * 3.0, color=OCHRE, lw=2.2)
ax.fill_between(x, np.minimum(w1, w2) * 3.0, color=GRAY, alpha=0.35)
ax.text(3.0, 3.25, r"$\varphi_a$", fontsize=11, color=TEAL, ha="center")
ax.text(7.0, 3.25, r"$\varphi_b$", fontsize=11, color=OCHRE, ha="center")
ax.text(5.0, 0.55, "重叠越大，J 越大", fontsize=11, color=INK, ha="center")
ax.set_title("交换积分 J：只存在于重叠区", fontsize=12, color=INK)
ax.set_xlim(0, 10); ax.set_ylim(0, 3.9)

for ax in axes:
    ax.set_xticks([]); ax.set_yticks([])
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
fig.tight_layout()
save(fig, "fig_exchange.png")


# ---------- 激发态裂分：E0 → +K → ±J ----------
fig, ax = plt.subplots(figsize=(8.2, 3.6), facecolor=PAPER)
ax.set_facecolor(PAPER)

ax.plot([0.3, 2.3], [0, 0], color=INK, lw=2.4)
ax.text(1.3, 0.16, r"$E^{(0)}$（交换简并）", ha="center", fontsize=11.5, color=INK)

ax.plot([3.5, 5.5], [1.0, 1.0], color=INK, lw=2.4)
ax.text(4.5, 1.16, r"$E^{(0)}+K$", ha="center", fontsize=11.5, color=INK)

ax.plot([6.7, 8.7], [1.55, 1.55], color=TEAL, lw=2.4)
ax.text(7.7, 1.71, r"仲氦 $E^{(0)}+K+J$（单态）", ha="center", fontsize=11.5, color=TEAL)
ax.plot([6.7, 8.7], [0.45, 0.45], color=OCHRE, lw=2.4)
ax.text(7.7, 0.61, r"正氦 $E^{(0)}+K-J$（三重态）", ha="center", fontsize=11.5, color=OCHRE)

ax.annotate("", xy=(3.05, 1.0), xytext=(3.05, 0),
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.5))
ax.text(3.17, 0.42, r"$+\,K$", color=GRAY, fontsize=12)
ax.annotate("", xy=(6.25, 1.55), xytext=(6.25, 1.0),
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.5))
ax.text(6.37, 1.30, r"$+\,J$", color=TEAL, fontsize=12)
ax.annotate("", xy=(6.25, 0.45), xytext=(6.25, 1.0),
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=1.5))
ax.text(6.37, 0.62, r"$-\,J$", color=OCHRE, fontsize=12)

ax.annotate("", xy=(9.05, 1.55), xytext=(9.05, 0.45),
            arrowprops=dict(arrowstyle="<->", color=INK, lw=1.3))
ax.text(9.17, 1.0, r"$2J$", color=INK, fontsize=12.5)

ax.set_xlim(0, 10.2); ax.set_ylim(-0.35, 2.2)
ax.set_xticks([]); ax.set_yticks([])
for s in ["top", "right", "bottom"]:
    ax.spines[s].set_visible(False)
fig.tight_layout()
save(fig, "fig_split.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
