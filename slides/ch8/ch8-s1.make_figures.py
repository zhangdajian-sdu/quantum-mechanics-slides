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


# ---------- 封面：每个方向，只有两个取值（teal 底） ----------
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)

t = np.linspace(0, 1, 200)
ax.plot(-3.0 + 2.2 * t, 0 * t, color="#FAF8F4", lw=1.8, alpha=0.9)          # 入射束
ax.plot(-0.8 + 2.6 * t, 0.0 + 1.05 * t ** 1.6, color="#FAF8F4", lw=1.8)     # 上束
ax.plot(-0.8 + 2.6 * t, 0.0 - 1.05 * t ** 1.6, color="#FAF8F4", lw=1.8)     # 下束
ax.plot([1.8], [1.05], "o", color="#E8B48C", ms=11)
ax.plot([1.8], [-1.05], "o", color="#E8B48C", ms=11)
ax.text(2.05, 1.05, "$+\\hbar/2$", color="#E8B48C", fontsize=15, va="center")
ax.text(2.05, -1.05, "$-\\hbar/2$", color="#E8B48C", fontsize=15, va="center")
ax.annotate("", xy=(-0.2, 0.86), xytext=(-0.2, 0.18),
            arrowprops=dict(arrowstyle="-|>", color="#E8B48C", lw=1.6))
ax.text(-0.45, 0.55, "非均匀磁场", color="#FFFFFF99", fontsize=10.5, ha="right")

ax.text(0.0, 2.35, "任一方向，", color="#FAF8F4", fontsize=17, ha="center", weight="bold")
ax.text(0.0, 2.13, "自旋投影只有两个取值", color="#FAF8F4", fontsize=17, ha="center", weight="bold")
ax.text(0.0, 1.88, "$S_x=S_y=S_z=\\pm\\hbar/2$", color="#E8B48C", fontsize=15, ha="center")
ax.text(0.0, -1.85, "斯特恩–盖拉赫实验：银原子束分裂成两束", color="#FFFFFF99", fontsize=11, ha="center")
ax.set_xlim(-3.3, 3.3)
ax.set_ylim(-2.05, 2.6)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- 斯特恩–盖拉赫实验示意 ----------
fig, ax = plt.subplots(figsize=(8.4, 5.0), facecolor=PAPER)
ax.set_facecolor(PAPER)

# 炉子与准直缝
oven = plt.Rectangle((0.2, 1.9), 0.9, 1.2, facecolor="#E7E2D6", edgecolor=GRAY, lw=1.2)
ax.add_patch(oven)
ax.text(0.65, 2.5, "银原子炉", fontsize=11.5, color=INK, ha="center", va="center")
slit = plt.Rectangle((1.55, 2.28), 0.16, 0.44, facecolor=INK)
ax.add_patch(slit)
ax.text(1.63, 3.0, "准直缝", fontsize=10.5, color=GRAY, ha="center")

# 入射束
ax.annotate("", xy=(3.6, 2.5), xytext=(1.75, 2.5),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.8))
ax.text(2.6, 2.72, "原子束", fontsize=11.5, color=INK, ha="center")

# 磁铁（N 尖、S 平）
n_pole = plt.Polygon([(3.8, 3.4), (5.4, 3.4), (4.9, 2.86), (4.3, 2.86)],
                     closed=True, facecolor=TEAL, alpha=0.92)
s_pole = plt.Rectangle((3.8, 1.55), 1.6, 0.5, facecolor="#5B7B8A", alpha=0.9)
ax.add_patch(n_pole); ax.add_patch(s_pole)
ax.text(4.6, 3.16, "N", fontsize=13, color="white", ha="center", weight="bold")
ax.text(4.6, 1.8, "S", fontsize=13, color="white", ha="center", weight="bold")
ax.text(4.6, 1.18, "非均匀磁场", fontsize=11, color=GRAY, ha="center")

# 分裂束
t = np.linspace(0, 1, 100)
ax.plot(5.4 + 2.2 * t, 2.5 + 0.95 * t ** 1.5, color=OCHRE, lw=2.2)
ax.plot(5.4 + 2.2 * t, 2.5 - 0.95 * t ** 1.5, color=TEAL, lw=2.2)

# 屏与两个斑点
ax.plot([7.75, 7.75], [0.6, 4.4], color=GRAY, lw=2.4)
ax.plot([7.68], [3.42], "o", color=OCHRE, ms=13)
ax.plot([7.68], [1.58], "o", color=TEAL, ms=13)
ax.text(7.95, 3.42, "自旋向上 $s_z=+\\hbar/2$", fontsize=11.5, color=OCHRE, va="center")
ax.text(7.95, 1.58, "自旋向下 $s_z=-\\hbar/2$", fontsize=11.5, color=TEAL, va="center")
ax.plot([7.68], [2.5], "s", color=PAPER, mec=GRAY, ms=8)  # 经典预期位置：没有斑
ax.text(7.95, 2.5, "经典预期：连续一片（没有！）", fontsize=10.5, color=GRAY, va="center")

ax.set_xlim(0, 10.4); ax.set_ylim(0.4, 4.7)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title("斯特恩–盖拉赫实验（1922）：束流只裂成两束，屏上只有两个斑点", fontsize=13, color=INK, pad=8)
save(fig, "fig_sg.png")

# ---------- 钠原子 D 双线：3P 精细结构示意 ----------
fig, ax = plt.subplots(figsize=(7.2, 6.0), facecolor=PAPER)
ax.set_facecolor(PAPER)

y_s, y_p1, y_p3 = 0.0, 2.0, 2.34   # 3P 分裂间隔夸大画出
x0, x1 = 1.2, 5.2

# 能级
ax.plot([x0, x1], [y_s, y_s], color=INK, lw=2.6)
ax.plot([x0, x1], [y_p1, y_p1], color=INK, lw=2.6)
ax.plot([x0, x1], [y_p3, y_p3], color=INK, lw=2.6)
ax.text(x0 - 0.18, y_s, r"$3S_{1/2}$", fontsize=16, color=INK, ha="right", va="center")
ax.text(x0 - 0.18, y_p1, r"$3P_{1/2}$", fontsize=16, color=INK, ha="right", va="center")
ax.text(x0 - 0.18, y_p3, r"$3P_{3/2}$", fontsize=16, color=INK, ha="right", va="center")

# 3P 间隔标注
ax.annotate("", xy=(x1 + 0.45, y_p3), xytext=(x1 + 0.45, y_p1),
            arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.4))
ax.text(x1 + 0.62, (y_p1 + y_p3) / 2, "精细分裂\n（间隔已夸大）", fontsize=10.5, color=GRAY, va="center")

# 两条跃迁
x_a, x_b = 2.6, 3.8
ax.annotate("", xy=(x_a, y_s + 0.06), xytext=(x_a, y_p3 - 0.06),
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=2.2))
ax.annotate("", xy=(x_b, y_s + 0.06), xytext=(x_b, y_p1 - 0.06),
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2.2))
ax.text(x_a, y_p3 + 0.24, r"$D_2$ 线", fontsize=13, color=OCHRE, ha="center")
ax.text(x_a, y_s - 0.32, "589.0 nm", fontsize=12, color=OCHRE, ha="center")
ax.text(x_b, y_p3 + 0.24, r"$D_1$ 线", fontsize=13, color=TEAL, ha="center")
ax.text(x_b, y_s - 0.32, "589.6 nm", fontsize=12, color=TEAL, ha="center")

# 双竖线（光谱线）
ax.plot([7.05, 7.05], [0.2, 2.1], color=OCHRE, lw=3.2)
ax.plot([7.3, 7.3], [0.2, 2.1], color=TEAL, lw=2.2)
ax.text(7.17, -0.5, "两线间隔 " + r"$\Delta\lambda\approx 0.6$ nm", fontsize=11, color=GRAY, ha="center")
ax.text(7.17, 2.45, "光谱仪里看到的两条线", fontsize=11, color=GRAY, ha="center")

ax.set_xlim(-0.2, 8.2); ax.set_ylim(-1.0, 3.1)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_na_doublet.png")


# ---------- 布洛赫球：任意自旋态的几何图像 ----------
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

fig = plt.figure(figsize=(6.8, 6.2), facecolor=PAPER)
ax = fig.add_subplot(111, projection="3d", facecolor=PAPER)

# 球面网格
u = np.linspace(0, 2 * np.pi, 40)
v = np.linspace(0, np.pi, 24)
xs = np.outer(np.cos(u), np.sin(v))
ys = np.outer(np.sin(u), np.sin(v))
zs = np.outer(np.ones_like(u), np.cos(v))
ax.plot_wireframe(xs, ys, zs, color=GRAY, alpha=0.22, lw=0.7)
# 赤道
th = np.linspace(0, 2 * np.pi, 100)
ax.plot(np.cos(th), np.sin(th), 0, color=GRAY, lw=1.0, alpha=0.5)

# 坐标轴
for vec, lab in [((1.45, 0, 0), "$S_x$"), ((0, 1.45, 0), "$S_y$"), ((0, 0, 1.5), "$S_z$")]:
    ax.quiver(0, 0, 0, *vec, color=INK, lw=1.4, arrow_length_ratio=0.06)
ax.text(1.6, 0, 0, "$S_x$", fontsize=13, color=INK)
ax.text(0, 1.62, 0, "$S_y$", fontsize=13, color=INK)
ax.text(0, 0, 1.62, "$S_z$", fontsize=13, color=INK)

# 一般态矢
theta, phi = np.deg2rad(52), np.deg2rad(38)
vdir = np.array([np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)])
ax.quiver(0, 0, 0, *vdir, color=OCHRE, lw=3.0, arrow_length_ratio=0.10)
ax.text(*(vdir * 1.22), r"$\chi=a\alpha+b\beta$", fontsize=13.5, color=OCHRE)

# 两极：alpha / beta
ax.scatter([0], [0], [1], color=TEAL, s=64)
ax.scatter([0], [0], [-1], color=TEAL, s=64)
ax.text(0.08, 0.08, 1.13, r"$\alpha=\binom{1}{0}$ 自旋向上", fontsize=12.5, color=TEAL)
ax.text(0.08, 0.08, -1.3, r"$\beta=\binom{0}{1}$ 自旋向下", fontsize=12.5, color=TEAL)

ax.set_box_aspect((1, 1, 1))
ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3); ax.set_zlim(-1.35, 1.55)
ax.set_axis_off()
ax.view_init(elev=16, azim=-58)
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
fig.savefig(OUT / "fig_bloch.png", dpi=200, bbox_inches="tight", facecolor=PAPER, pad_inches=0.05)
plt.close(fig)
print("saved fig_bloch.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
