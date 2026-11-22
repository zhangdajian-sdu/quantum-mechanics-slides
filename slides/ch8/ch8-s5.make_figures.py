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


# ---------- 封面：能级一分为二（teal 底） ----------
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)

ax.text(0.0, 2.66, "一条谱线，", color="#FAF8F4", fontsize=18,
        ha="center", weight="bold")
ax.text(0.0, 2.40, "裂成两条", color="#FAF8F4", fontsize=18,
        ha="center", weight="bold")

# 左：未分裂能级
ax.plot([-2.9, -1.5], [1.1, 1.1], color="#FFFFFFAA", lw=2.2)
ax.text(-2.2, 1.28, "$E_{nl}$", color="#FAF8F4", fontsize=13, ha="center")
ax.text(-2.2, 0.84, "不计自旋", color="#FFFFFF88", fontsize=10, ha="center")

# 箭头
ax.annotate("", xy=(-0.55, 1.1), xytext=(-1.35, 1.1),
            arrowprops=dict(arrowstyle="-|>", color="#E8B48C", lw=1.6))

# 右：分裂后的两个能级（间距夸大）
ax.plot([0.0, 1.4], [1.34, 1.34], color="#FAF8F4", lw=2.2)
ax.plot([0.0, 1.4], [0.86, 0.86], color="#E8B48C", lw=2.2)
ax.text(0.7, 1.52, "$j=l+\\frac{1}{2}$", color="#FAF8F4", fontsize=12, ha="center")
ax.text(0.7, 0.58, "$j=l-\\frac{1}{2}$", color="#E8B48C", fontsize=12, ha="center")
ax.plot([1.52, 1.52], [0.86, 1.34], color="#FFFFFF66", lw=1.0)
ax.text(1.68, 1.1, "$\\Delta E$ 很小", color="#FFFFFF99", fontsize=10, ha="left")

# 底部：谱线 一 -> 二
ax.plot([-2.9, -1.5], [-0.6, -0.6], color="#FFFFFF55", lw=1.0)
ax.plot([-2.2], [-0.25], marker="|", ms=46, color="#FFFFFFAA", mew=2.4)
ax.text(-2.2, -1.02, "一条谱线", color="#FFFFFF88", fontsize=10.5, ha="center")

ax.annotate("", xy=(-0.55, -0.45), xytext=(-1.35, -0.45),
            arrowprops=dict(arrowstyle="-|>", color="#E8B48C", lw=1.6))

ax.plot([0.0, 1.4], [-0.6, -0.6], color="#FFFFFF55", lw=1.0)
for x in (0.62, 0.78):
    ax.plot([x], [-0.25], marker="|", ms=46, color="#FAF8F4", mew=2.4)
ax.text(0.7, -1.02, "双线：精细结构", color="#FAF8F4", fontsize=10.5, ha="center")

ax.text(0.0, -1.7, "起源：自旋–轨道耦合 $\\xi(r)\\,\\hat{\\boldsymbol{S}}\\cdot\\hat{\\boldsymbol{L}}$",
        color="#FAF8F4", fontsize=12.5, ha="center")
ax.text(0.0, -2.08, "强度 $\\propto 1/c^2$，很弱，所以双线靠得很近",
        color="#FFFFFF99", fontsize=10.5, ha="center")

ax.set_xlim(-3.4, 3.4)
ax.set_ylim(-2.4, 2.95)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- 能级分裂：E_nl -> E_nlj（paper 底） ----------
fig, ax = plt.subplots(figsize=(6.6, 4.6), facecolor=PAPER)
ax.set_facecolor(PAPER)

# 左：零级能级
ax.plot([0.3, 1.9], [1.6, 1.6], color=GRAY, lw=2.4)
ax.text(1.1, 1.78, "$E_{nl}$（$2(2l+1)$ 度简并）", color=INK, fontsize=11.5,
        ha="center")
ax.text(1.1, 1.36, "屏蔽后 $Z\\to Z(n,l)$", color=GRAY, fontsize=9.5, ha="center")

ax.annotate("", xy=(2.85, 1.6), xytext=(2.15, 1.6),
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=1.6))
ax.text(2.5, 1.74, "$\\hat{H}^{\\prime}$", color=OCHRE, fontsize=11, ha="center")

# 右：两个能级
ax.plot([3.3, 4.9], [1.95, 1.95], color=TEAL, lw=2.4)
ax.plot([3.3, 4.9], [1.25, 1.25], color=OCHRE, lw=2.4)
ax.text(5.05, 1.95, "$E_{nlj=l+1/2}=E_{nl}+E^{(1)}_{+}$", color=TEAL,
        fontsize=11, ha="left", va="center")
ax.text(5.05, 1.25, "$E_{nlj=l-1/2}=E_{nl}-|E^{(1)}_{-}|$", color=OCHRE,
        fontsize=11, ha="left", va="center")

# 间距标注
ax.plot([3.14, 3.14], [1.25, 1.95], color=GRAY, lw=1.0)
ax.text(2.98, 1.28, "$\\propto\\frac{Z^{4}}{n^{3}}$", color=GRAY, fontsize=10,
        ha="right", va="center")

ax.text(2.6, 0.62, "简并未完全解除：每个能级仍 $2j+1$ 度简并（对 $m_j$）",
        color=INK, fontsize=10.5, ha="center")
ax.text(2.6, 0.26, "$j=l+\\frac{1}{2}$ 的能级一定在上方",
        color=GRAY, fontsize=10, ha="center")

ax.set_xlim(0, 7.6)
ax.set_ylim(0, 2.3)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_split.png")


# ---------- 钠 D 双线示意（paper 底） ----------
fig, ax = plt.subplots(figsize=(6.8, 4.6), facecolor=PAPER)
ax.set_facecolor(PAPER)

# 上能级 3P 双态
ax.plot([0.4, 2.2], [2.55, 2.55], color=TEAL, lw=2.4)
ax.plot([1.05, 2.2], [2.30, 2.30], color=OCHRE, lw=2.4)
ax.text(1.3, 2.72, "$3P_{3/2}$", color=TEAL, fontsize=11.5, ha="center")
ax.text(1.62, 2.06, "$3P_{1/2}$", color=OCHRE, fontsize=11.5, ha="center")

# 下能级 3S
ax.plot([0.4, 2.2], [0.55, 0.55], color=INK, lw=2.4)
ax.text(1.3, 0.28, "$3S_{1/2}$", color=INK, fontsize=11.5, ha="center")

# 跃迁箭头
ax.annotate("", xy=(0.72, 0.62), xytext=(0.72, 2.48),
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.8))
ax.annotate("", xy=(1.7, 0.62), xytext=(1.7, 2.23),
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=1.8))

# 右侧谱线
ax.plot([3.4, 6.2], [0.55, 0.55], color=HAIR, lw=1.2)
ax.plot([4.45], [1.0], marker="|", ms=46, color=TEAL, mew=2.6)
ax.plot([4.85], [1.0], marker="|", ms=46, color=OCHRE, mew=2.6)
ax.text(4.45, 0.68, "$D_{2}$", color=TEAL, fontsize=11, ha="center")
ax.text(4.85, 0.68, "$D_{1}$", color=OCHRE, fontsize=11, ha="center")
ax.text(4.8, 1.58, "钠黄光双线\n$\\approx 589.0,\\,589.6\\,\\mathrm{nm}$",
        color=INK, fontsize=10.5, ha="center")
ax.text(4.8, 0.12, "间距仅 $\\approx 0.6\\,\\mathrm{nm}$",
        color=GRAY, fontsize=10, ha="center")

ax.set_xlim(0, 6.6)
ax.set_ylim(0, 3.0)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_sodium.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
