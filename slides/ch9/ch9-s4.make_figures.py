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


# ---------- 封面：谐振子能级阶梯 + a† 逐级上升（teal 底） ----------
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)
levels = [0, 1, 2, 3, 4]
for n in levels:
    y = 0.35 + n * 0.62
    ax.plot([0.9, 3.1], [y, y], color="#FAF8F4", lw=2.2)
    ax.text(3.25, y, f"$|{n}\\rangle$", color="#FAF8F4", fontsize=15, va="center")
    ax.text(0.62, y, f"$n={n}$", color="#8FB6C2", fontsize=11, va="center", ha="right")
for n in range(4):
    y0 = 0.35 + n * 0.62
    ax.annotate("", xy=(1.55, y0 + 0.62), xytext=(1.55, y0 + 0.10),
                arrowprops=dict(arrowstyle="-|>", color="#E8B48C", lw=2.0))
ax.text(1.85, 1.62, r"$a^{\dagger}$", color="#E8B48C", fontsize=17)
ax.text(2.0, 3.42, "每升一级，多一个量子", color="#DCE8EC", fontsize=12, ha="center")
ax.set_xlim(0, 4.4); ax.set_ylim(0, 3.9)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- 引入：编号描述 vs 占有数描述 ----------
fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.9), facecolor=PAPER)
for ax in axes:
    ax.set_facecolor(PAPER)
# 左：编号描述
ax = axes[0]
bx, bw, bh, gap = 0.7, 1.35, 0.5, 0.14
labels = [r"$\varphi_1$", r"$\varphi_2$", r"$\varphi_3$"]
who = ["1 号, 2 号", "3 号", "—"]
for k in range(3):
    y0 = 0.25 + k * (bh + gap)
    ax.add_patch(plt.Rectangle((bx, y0), bw, bh, fill=False, edgecolor=INK, lw=1.2))
    ax.text(bx - 0.18, y0 + bh / 2, labels[k], fontsize=13, color=INK,
            ha="right", va="center")
    ax.text(bx + bw / 2, y0 + bh / 2, who[k], fontsize=11, color=TEAL,
            ha="center", va="center")
ax.annotate("", xy=(bx + bw + 0.85, 0.25 + bh / 2),
            xytext=(bx + bw + 0.85, 0.25 + bh + gap + bh / 2),
            arrowprops=dict(arrowstyle="<->", color=OCHRE, lw=1.8))
ax.text(bx + bw + 1.05, 0.25 + bh + gap / 2, r"$\hat{P}_{ij}$", fontsize=12,
        color=OCHRE, va="center")
ax.text(bx + 1.1, 2.72, r"$\psi(q_1,q_2,q_3)$：每个号码各占哪个态",
        fontsize=11, color=GRAY, ha="center")
ax.set_title("编号描述：交换前后是「同一个态」", fontsize=12, color=INK)
ax.set_xlim(0, 3.9); ax.set_ylim(0, 3.0)
# 右：占有数描述
ax = axes[1]
occ = [2, 1, 0, 0, 0]
for k, n in enumerate(occ):
    y0 = 0.25 + k * (0.38 + 0.075)
    ax.add_patch(plt.Rectangle((0.7, y0), 1.35, 0.38, fill=False, edgecolor=INK, lw=1.2))
    ax.text(0.52, y0 + 0.19, rf"$\varphi_{k+1}$", fontsize=12, color=INK,
            ha="right", va="center")
    for d in range(n):
        ax.plot(0.7 + 1.35 * (0.5 + (d - (n - 1) / 2) * 0.4), y0 + 0.19, "o",
                ms=6, color=OCHRE, mec=OCHRE)
ax.text(2.35, 1.15, "只数人数：$n_1=2,\\ n_2=1$\n不问号码", fontsize=11, color=TEAL,
        va="center")
ax.text(1.4, 2.72, r"$\sum_i n_i = N$，交换信息自动消失", fontsize=11, color=GRAY,
        ha="center")
ax.set_title("占有数描述：每个态上有几个粒子", fontsize=12, color=INK)
ax.set_xlim(0, 3.9); ax.set_ylim(0, 3.0)
for ax in axes:
    ax.set_xticks([]); ax.set_yticks([])
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
fig.tight_layout()
save(fig, "fig_intro.png")


# ---------- 升降算符：阶梯上的系数 ----------
fig, ax = plt.subplots(figsize=(7.8, 4.2), facecolor=PAPER)
ax.set_facecolor(PAPER)
ns = [0, 1, 2, 3]
for n in ns:
    y = 0.3 + n * 0.78
    ax.plot([1.0, 3.4], [y, y], color=INK, lw=2.0)
    ax.text(0.8, y, f"$|{n}\\rangle$", fontsize=13, color=INK, ha="right", va="center")
    ax.text(2.2, y + 0.10, f"$E_n=(n+\\frac{{1}}{{2}})\\hbar\\omega$",
            fontsize=10.5, color=GRAY, ha="center")
# a† 上升（右侧）
for n in range(3):
    y0 = 0.3 + n * 0.78
    ax.annotate("", xy=(3.05, y0 + 0.78), xytext=(3.05, y0 + 0.12),
                arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2.0))
    ax.text(3.28, y0 + 0.42, rf"$\sqrt{{{n+1}}}$", fontsize=12, color=TEAL)
# a 下降（左侧）
for n in range(1, 4):
    y0 = 0.3 + n * 0.78
    ax.annotate("", xy=(1.35, y0 - 0.78), xytext=(1.35, y0 - 0.12),
                arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=2.0))
    ax.text(1.06, y0 - 0.36, rf"$\sqrt{{{n}}}$", fontsize=12, color=OCHRE,
            ha="right")
ax.text(3.05, 3.25, r"$a^{\dagger}$ 产生", fontsize=12.5, color=TEAL, ha="center")
ax.text(1.35, 3.25, r"$a$ 消灭", fontsize=12.5, color=OCHRE, ha="center")
ax.text(2.2, -0.12, r"$a|0\rangle=0$：阶梯到此为止，$n$ 只能是 $0,1,2,\cdots$",
        fontsize=11, color=GRAY, ha="center")
ax.set_xlim(0, 4.3); ax.set_ylim(-0.35, 3.55)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_ladder.png")


# ---------- 占有数表象基矢：n=(2,0,3,1) 四槽 ----------
fig, ax = plt.subplots(figsize=(8.2, 3.4), facecolor=PAPER)
ax.set_facecolor(PAPER)
occ = [2, 0, 3, 1]
for k, n in enumerate(occ):
    y0 = 0.3 + k * 0.62
    ax.add_patch(plt.Rectangle((0.9, y0), 1.7, 0.5, fill=False, edgecolor=INK, lw=1.3))
    ax.text(0.68, y0 + 0.25, rf"$\varphi_{k+1}$", fontsize=13, color=INK,
            ha="right", va="center")
    for d in range(n):
        ax.plot(0.9 + 1.7 * (0.5 + (d - (n - 1) / 2) * 0.30), y0 + 0.25, "o",
                ms=7, color=OCHRE, mec=OCHRE)
    ax.text(2.85, y0 + 0.25, rf"$n_{k+1}={n}$", fontsize=12, color=TEAL, va="center")
ax.text(4.15, 1.35,
        "态矢写成\n$|2,0,3,1\\rangle$\n\n粒子总数 $N=6$\n每个 $n_i$ 都是好量子数",
        fontsize=12, color=INK, va="center", linespacing=1.7)
ax.text(1.75, 3.05, "基矢由整组占有数 $(n_1,n_2,n_3,\\cdots)$ 唯一标记",
        fontsize=11.5, color=GRAY, ha="center")
ax.set_xlim(0, 5.9); ax.set_ylim(0, 3.2)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_occ.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
