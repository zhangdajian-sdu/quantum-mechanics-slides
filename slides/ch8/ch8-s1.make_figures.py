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

print("done:", sorted(p.name for p in OUT.glob("*.png")))
