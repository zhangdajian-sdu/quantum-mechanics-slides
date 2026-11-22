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

OUT = Path(__file__).parent / "media"
OUT.mkdir(exist_ok=True)


def save(fig, name):
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print("saved", name)


# ---------- 封面：平面波 + 出射球面波（teal 底，竖版） ----------
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)

# 入射平面波（左侧平行波纹，沿 +z 传播）
xs = np.linspace(-4.3, -0.95, 300)
for y0 in np.linspace(-3.6, 3.6, 8):
    ax.plot(xs, y0 + 0.16 * np.sin(2.6 * xs), color="#FAF8F4", lw=1.05, alpha=0.8)

# 散射中心
ax.plot(0, 0, "o", ms=13, color="#E8B48C", mec="#FAF8F4", mew=1.4)
ax.text(0.0, -0.66, "V(r)", color="#E8B48C", fontsize=13, ha="center")

# 出射球面波（右半圆弧）
for i, r in enumerate(np.linspace(0.75, 3.9, 7)):
    th = np.linspace(-np.pi / 2 + 0.12, np.pi / 2 - 0.12, 240)
    ripple = 1 + 0.05 * np.sin(5 * th)
    ax.plot(r * np.cos(th) * ripple, r * np.sin(th), color="#FAF8F4",
            lw=1.05, alpha=max(0.25, 0.95 - i * 0.11))

ax.annotate("", xy=(-0.8, 2.2), xytext=(-2.7, 2.2),
            arrowprops=dict(arrowstyle="-|>", color="#E8B48C", lw=1.5))
ax.text(-3.75, 2.55, r"入射 $\mathrm{e}^{ikz}$", color="#FAF8F4", fontsize=14)

ax.annotate("", xy=(2.95 * np.cos(np.deg2rad(35)), 2.95 * np.sin(np.deg2rad(35))),
            xytext=(1.25 * np.cos(np.deg2rad(35)), 1.25 * np.sin(np.deg2rad(35))),
            arrowprops=dict(arrowstyle="-|>", color="#E8B48C", lw=1.5))
ax.text(1.7, 3.35, r"出射 $f(\theta,\varphi)\,\dfrac{\mathrm{e}^{ikr}}{r}$",
        color="#FAF8F4", fontsize=14, ha="center")

ax.text(0, -4.4, r"$\sigma(\theta,\varphi)=|f(\theta,\varphi)|^{2}$",
        color="#E8B48C", fontsize=17, ha="center")

ax.set_xlim(-4.6, 4.6)
ax.set_ylim(-4.9, 4.3)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- 经典散射图像：瞄准距离与散射角（仿教材图 10.1） ----------
fig, ax = plt.subplots(figsize=(7.8, 4.2), facecolor=PAPER)
ax.set_facecolor(PAPER)

ax.axhline(0, color=GRAY, lw=1.0, ls=(0, (4, 3)))
ax.plot(0, 0, "o", ms=11, color=OCHRE, mec=INK, mew=0.8)
ax.text(0.2, -0.46, "靶粒子", fontsize=11, color=OCHRE)


def traj(b, theta_deg, x_hit=-0.15):
    ax.annotate("", xy=(x_hit - 0.6, b), xytext=(-5.6, b),
                arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.6))
    ax.plot([x_hit - 0.6, x_hit], [b, b], color=TEAL, lw=1.6)
    th = np.deg2rad(theta_deg)
    L = 4.4
    ax.plot([x_hit, x_hit + L * np.cos(th)], [b, b + L * np.sin(th)],
            color=TEAL, lw=1.6)
    ax.plot([x_hit, x_hit + 1.5], [b, b], color=GRAY, lw=0.9, ls=(0, (3, 3)))


for b, th in [(2.55, 12), (1.85, 30), (1.15, 62), (0.45, 118)]:
    traj(b, th)

# 瞄准距离标注（对 b=1.15 那条）
ax.annotate("", xy=(-3.6, 1.15), xytext=(-3.6, 0),
            arrowprops=dict(arrowstyle="<->", color=INK, lw=1.2))
ax.text(-3.48, 0.5, "b", fontsize=13, color=INK, style="italic")

# 散射角标注（对 b=0.45 那条）
x0, y0 = -0.15, 0.45
arc = np.linspace(0, np.deg2rad(118), 100)
ax.plot(x0 + 1.1 * np.cos(arc), y0 + 1.1 * np.sin(arc), color=OCHRE, lw=1.2)
ax.text(x0 + 1.36, y0 + 0.6, r"$\theta$", fontsize=14, color=OCHRE)

ax.text(-5.55, 2.9, "入射粒子流", fontsize=11, color=TEAL)
ax.text(1.35, -0.68, "瞄准距离 b 愈小，散射角 θ 愈大", fontsize=12, color=INK)

ax.set_xlim(-6, 5.0)
ax.set_ylim(-1.0, 4.2)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_geometry.png")


# ---------- 截面 = 靶的有效横截面积 ----------
fig, ax = plt.subplots(figsize=(7.8, 2.9), facecolor=PAPER)
ax.set_facecolor(PAPER)

R = 0.42
cx, cy = 3.2, 1.05
for y in np.linspace(0.15, 1.95, 8):
    hit = abs(y - cy) < R
    c = OCHRE if hit else GRAY
    ax.annotate("", xy=(cx - R - 0.12, y), xytext=(0.3, y),
                arrowprops=dict(arrowstyle="-|>", color=c, lw=1.3,
                                alpha=0.95 if hit else 0.5))
    if hit:
        ax.plot([cx + R + 0.06, 4.9], [y, y + (y - cy) * 2.6], color=OCHRE, lw=1.3)
    else:
        ax.plot([cx + R + 0.06, 5.3], [y, y], color=GRAY, lw=1.3, alpha=0.5)

disk = plt.Circle((cx, cy), R, color=OCHRE, alpha=0.22, zorder=3)
ax.add_patch(disk)
ax.plot(cx, cy, "o", ms=8, color=OCHRE, zorder=4)
ax.text(cx, cy + R + 0.24, r"有效面积 $\sigma$", ha="center", fontsize=12, color=OCHRE)

ax.text(0.3, 2.32, "均匀入射束流", fontsize=11, color=INK)
ax.text(3.95, 2.86, "只有「撞上」圆盘的粒子被散射", fontsize=11, color=INK)

ax.set_xlim(0, 5.8)
ax.set_ylim(-0.55, 3.25)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_area.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
