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


# ---------- 封面：一条简并能级裂成一簇（teal 底） ----------
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)

ax.plot([0.10, 0.42], [2.0, 2.0], color="#FAF8F4", lw=2.8, solid_capstyle="round")
fans = [1.30, 1.75, 2.25, 2.70]
for y1 in fans:
    ax.plot([0.62, 0.92], [y1, y1], color="#E8B48C", lw=2.2, ls=(0, (6, 4)),
            solid_capstyle="round")
    ax.annotate("", xy=(0.60, y1), xytext=(0.44, 2.0),
                arrowprops=dict(arrowstyle="-|>", color="#FFFFFF88", lw=1.3,
                                connectionstyle="arc3,rad=0.12"))
ax.text(0.26, 2.16, r"$E_n^{(0)}$（$k$ 度简并）", color="#FAF8F4", fontsize=14, ha="center")
ax.text(0.77, 2.86, r"$E_{n\alpha}$", color="#E8B48C", fontsize=15, ha="center")
ax.text(0.26, 1.62, "一个能级", color="#FFFFFF99", fontsize=12.5, ha="center")
ax.text(0.77, 1.02, "裂成 k 条", color="#FFFFFF99", fontsize=12.5, ha="center")
ax.set_xlim(0, 1); ax.set_ylim(0.8, 3.1)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- 引入：2p→1s 谱线在电场中一条变三条 ----------
fig, ax = plt.subplots(figsize=(8.4, 5.6), facecolor=PAPER)
ax.set_facecolor(PAPER)

# 上：无电场，一条线
ax.plot([0.5, 0.5], [1.55, 2.30], color=INK, lw=3.0, solid_capstyle="round")
ax.text(0.5, 2.42, "无电场：一条", ha="center", fontsize=12.5, color=INK)
# 下：加电场，三条线
for x in (0.32, 0.50, 0.68):
    ax.plot([x, x], [0.35, 1.10], color=OCHRE, lw=3.0, solid_capstyle="round")
ax.text(0.5, 1.22, "加电场：裂成三条", ha="center", fontsize=12.5, color=OCHRE)
ax.annotate("", xy=(0.5, 1.45), xytext=(0.5, 1.52), arrowprops=dict(arrowstyle="-", color="none"))
ax.set_xlim(0, 1); ax.set_ylim(0.1, 2.65)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title(r"氢光谱 $2p\to1s$（斯塔克，1913）", fontsize=13.5, color=INK, pad=8)
save(fig, "fig_intro.png")


# ---------- 例题 1：n=2 能级分裂与零级波函数 ----------
fig, axes = plt.subplots(1, 2, figsize=(9.6, 5.4), facecolor=PAPER)

E2 = 2.6
E1 = 0.6
d = 0.55  # 3eεa 的图示大小

for ax, title in zip(axes, ["无电场", "均匀电场 ε"]):
    ax.set_facecolor(PAPER)
    ax.set_xlim(0, 1); ax.set_ylim(0, 3.4)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(title, fontsize=13, color=INK)

# 左：E2 一条（4 度简并）→ E1 一条
ax = axes[0]
ax.plot([0.15, 0.85], [E2, E2], color=TEAL, lw=2.6)
ax.plot([0.15, 0.85], [E1, E1], color=INK, lw=2.6)
ax.text(0.5, E2 + 0.12, r"$E_2^{(0)}$（4 度简并）", ha="center", fontsize=12, color=TEAL)
ax.text(0.5, E1 - 0.30, r"$E_1^{(0)}$", ha="center", fontsize=12, color=INK)
ax.annotate("", xy=(0.5, E1 + 0.06), xytext=(0.5, E2 - 0.06),
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.6))
ax.text(0.56, (E1 + E2) / 2, "一条谱线", fontsize=11.5, color=GRAY)

# 右：三条
ax = axes[1]
ys = [E2 + d, E2, E2 - d]
labels = [r"$+3e\varepsilon a$", r"$0$（仍 2 度）", r"$-3e\varepsilon a$"]
cols = [OCHRE, GRAY, OCHRE]
for y, lb, c in zip(ys, labels, cols):
    ax.plot([0.12, 0.62], [y, y], color=c, lw=2.4)
    ax.text(0.66, y, lb, fontsize=11, color=c, va="center")
ax.plot([0.12, 0.62], [E1, E1], color=INK, lw=2.6)
ax.text(0.66, E1, r"$E_1^{(0)}$", fontsize=11, color=INK, va="center")
for y in ys:
    ax.annotate("", xy=(0.37, E1 + 0.06), xytext=(0.37, y - 0.06),
                arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.2, alpha=0.75))
ax.text(0.5, 0.12, "三条谱线", ha="center", fontsize=11.5, color=GRAY)

fig.suptitle(r"氢原子 $n=2$ 能级在电场中的分裂（线性斯塔克效应）", fontsize=13.5, color=INK)
fig.tight_layout(rect=[0, 0, 1, 0.94])
save(fig, "fig_split.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
