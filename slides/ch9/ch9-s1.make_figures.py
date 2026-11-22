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


def gauss(x, x0, s, a=1.0):
    return a * np.exp(-((x - x0) ** 2) / (2 * s ** 2))


# ---------- 封面：两个重叠波包 + 交换箭头（teal 底） ----------
x = np.linspace(-6, 6, 1200)
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)
p1 = gauss(x, -1.6, 1.1)
p2 = gauss(x, 1.6, 1.1)
ax.plot(x, p1, color="#FAF8F4", lw=2.6)
ax.plot(x, p2, color="#E8B48C", lw=2.6)
ax.fill_between(x, np.minimum(p1, p2), color="#8FB6C2", alpha=0.35)
ax.annotate("", xy=(1.9, 1.22), xytext=(-1.9, 1.22),
            arrowprops=dict(arrowstyle="<->", color="#FAF8F4", lw=1.6))
ax.text(0, 1.34, r"$\hat{P}_{ij}$", color="#FAF8F4", fontsize=17, ha="center")
ax.text(-1.6, -0.16, "粒子 $i$", color="#FAF8F4", fontsize=12, ha="center")
ax.text(1.6, -0.16, "粒子 $j$", color="#FAF8F4", fontsize=12, ha="center")
ax.text(0, 0.42, "重叠区无法区分", color="#DCE8EC", fontsize=12, ha="center")
ax.set_xlim(-5.4, 5.4); ax.set_ylim(-0.32, 1.62)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- 引入：经典可区分 vs 量子不可区分 ----------
fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.7), facecolor=PAPER)
for ax in axes:
    ax.set_facecolor(PAPER)
# 经典：两条可分辨的轨道
ax = axes[0]
t = np.linspace(0, 10, 400)
ax.plot(t, 1.5 * np.sin(0.55 * t) + 1.7, color=TEAL, lw=2.2)
ax.plot(t, 1.5 * np.sin(0.55 * t + np.pi) + 1.7, color=OCHRE, lw=2.2)
ax.plot(0.15, 1.5 * np.sin(0.55 * 0.15) + 1.7, "o", ms=8, color=TEAL)
ax.plot(0.15, 1.5 * np.sin(0.55 * 0.15 + np.pi) + 1.7, "o", ms=8, color=OCHRE)
ax.text(0.55, 3.35, "1 号", fontsize=11.5, color=TEAL)
ax.text(0.55, 0.28, "2 号", fontsize=11.5, color=OCHRE)
ax.text(6.9, 3.35, "全程跟得住", fontsize=11.5, color=INK)
ax.set_title("经典粒子：有轨道，可区分", fontsize=12, color=INK)
ax.set_xlim(0, 10); ax.set_ylim(0, 3.8)
# 量子：两个重叠波包
ax = axes[1]
xx = np.linspace(0, 10, 800)
w1 = gauss(xx, 3.6, 1.3)
w2 = gauss(xx, 6.4, 1.3)
ax.plot(xx, w1 * 3.0, color=TEAL, lw=2.2)
ax.plot(xx, w2 * 3.0, color=OCHRE, lw=2.2)
ax.fill_between(xx, 0, np.minimum(w1, w2) * 3.0, color=GRAY, alpha=0.30)
ax.text(5.0, 1.05, "？", fontsize=20, color=INK, ha="center", weight="bold")
ax.text(2.2, 3.35, "$|\\psi_1|^2$", fontsize=11.5, color=TEAL)
ax.text(7.3, 3.35, "$|\\psi_2|^2$", fontsize=11.5, color=OCHRE)
ax.text(5.0, -0.42, "重叠区里谁是谁？", fontsize=11.5, color=INK, ha="center")
ax.set_title("全同粒子：无轨道，只有几率分布", fontsize=12, color=INK)
ax.set_xlim(0, 10); ax.set_ylim(-0.6, 3.8)
for ax in axes:
    ax.set_xticks([]); ax.set_yticks([])
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
fig.tight_layout()
save(fig, "fig_intro.png")


# ---------- N=3 计数：费米子 1 种 vs 玻色子 10 种 ----------
def draw_slots(ax, occ, base_x, base_y, w=0.62, h=0.30, gap=0.06):
    """画 3 层能级槽（下低上高），occ=(n1,n2,n3) 放圆点。返回顶部 y。"""
    for k, n in enumerate(occ):  # k=0 最低
        y0 = base_y + k * (h + gap)
        ax.add_patch(plt.Rectangle((base_x, y0), w, h, fill=False,
                                   edgecolor=INK, lw=1.1))
        for d in range(n):
            ax.plot(base_x + w * (0.5 + (d - (n - 1) / 2) * 0.42),
                    y0 + h / 2, "o", ms=5.2, color=OCHRE, mec=OCHRE)
    return base_y + 3 * (h + gap)


fig = plt.figure(figsize=(8.6, 4.6), facecolor=PAPER)
# 左：费米子
axf = fig.add_axes([0.03, 0.10, 0.26, 0.78]); axf.set_facecolor(PAPER)
top = draw_slots(axf, (1, 1, 1), 0.9, 0.10)
axf.text(1.21, top + 0.12, "唯一一种", fontsize=11.5, color=INK, ha="center")
axf.text(1.21, top + 0.40, "每个态至多 1 个", fontsize=10.5, color=GRAY, ha="center")
axf.set_xlim(0, 2.4); axf.set_ylim(0, 2.0)
axf.axis("off")
axf.set_title("3 个费米子：1 种占法", fontsize=12.5, color=INK, pad=10)
# 右：玻色子 10 种，3+6+1
axb = fig.add_axes([0.33, 0.10, 0.65, 0.78]); axb.set_facecolor(PAPER)
cfgs_row1 = [(3, 0, 0), (0, 3, 0), (0, 0, 3)]
cfgs_row2 = [(2, 1, 0), (2, 0, 1), (1, 2, 0), (0, 2, 1), (1, 0, 2), (0, 1, 2)]
cfg_row3 = (1, 1, 1)
y1 = 2.72
for i, occ in enumerate(cfgs_row1):
    draw_slots(axb, occ, 0.55 + i * 1.55, y1)
axb.text(2.05, y1 - 0.26, "3 个同处一态：3 种", fontsize=10.5, color=GRAY, ha="center")
y2 = 1.38
for i, occ in enumerate(cfgs_row2):
    draw_slots(axb, occ, 0.02 + i * 0.90, y2)
axb.text(2.45, y2 - 0.26, "2+1 分配：6 种", fontsize=10.5, color=GRAY, ha="center")
draw_slots(axb, cfg_row3, 2.05, 0.04)
axb.text(2.36, 0.04 - 0.26, "各居一态：1 种", fontsize=10.5, color=GRAY, ha="center")
axb.set_xlim(-0.05, 5.6); axb.set_ylim(-0.42, 4.05)
axb.axis("off")
axb.set_title("3 个玻色子：10 种占法", fontsize=12.5, color=INK, pad=10)
save(fig, "fig_counting.png")


# ---------- 泡利原理：同一组量子数不许重复 ----------
fig, ax = plt.subplots(figsize=(7.6, 3.4), facecolor=PAPER)
ax.set_facecolor(PAPER)
# 允许：同一轨道一上一下
bx = 0.6
ax.add_patch(plt.Rectangle((bx, 0.35), 1.5, 0.62, fill=False, edgecolor=INK, lw=1.3))
ax.annotate("", xy=(bx + 0.62, 0.86), xytext=(bx + 0.62, 0.44),
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2))
ax.annotate("", xy=(bx + 0.88, 0.44), xytext=(bx + 0.88, 0.86),
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=2))
ax.text(bx + 0.75, 1.22, "允许：$m_s=+\\frac{1}{2}$ 与 $-\\frac{1}{2}$ 各一个",
        fontsize=11.5, color=INK, ha="center")
ax.text(bx + 0.75, 0.10, "四个量子数 $n,l,m,m_s$ 不完全相同", fontsize=10.5,
        color=GRAY, ha="center")
# 禁止：两个同向
bx2 = 3.9
ax.add_patch(plt.Rectangle((bx2, 0.35), 1.5, 0.62, fill=False, edgecolor=GRAY, lw=1.3))
ax.annotate("", xy=(bx2 + 0.62, 0.86), xytext=(bx2 + 0.62, 0.44),
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=2))
ax.annotate("", xy=(bx2 + 0.88, 0.86), xytext=(bx2 + 0.88, 0.44),
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=2))
ax.plot([bx2 - 0.15, bx2 + 1.65], [0.20, 1.12], color=OCHRE, lw=2.6)
ax.plot([bx2 - 0.15, bx2 + 1.65], [1.12, 0.20], color=OCHRE, lw=2.6)
ax.text(bx2 + 0.75, 1.22, "禁止：四个量子数全同", fontsize=11.5, color=OCHRE,
        ha="center")
ax.text(bx2 + 0.75, 0.10, "行列式两行相同 ⇒ $\\psi_A=0$", fontsize=10.5,
        color=GRAY, ha="center")
ax.set_xlim(0, 6.2); ax.set_ylim(0, 1.5)
ax.axis("off")
save(fig, "fig_pauli.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
