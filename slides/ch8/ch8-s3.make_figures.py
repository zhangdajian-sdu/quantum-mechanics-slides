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


# ---------- 封面：两个角动量合成一个（teal 底） ----------
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)

o = np.array([-1.6, -1.1])
j1 = np.array([2.5, 0.9])    # J1
j2 = np.array([1.1, 1.7])    # J2
jt = j1 + j2                 # J

# 平行四边形虚线
ax.plot([o[0] + j1[0], o[0] + jt[0]], [o[1] + j1[1], o[1] + jt[1]],
        color="#FFFFFF44", lw=1.2, ls="--")
ax.plot([o[0] + j2[0], o[0] + jt[0]], [o[1] + j2[1], o[1] + jt[1]],
        color="#FFFFFF44", lw=1.2, ls="--")

for v, lb, c, fs in [(j1, "$\\hat{\\boldsymbol{J}}_1$", "#FAF8F4", 16),
                     (j2, "$\\hat{\\boldsymbol{J}}_2$", "#FAF8F4", 16),
                     (jt, "$\\hat{\\boldsymbol{J}}=\\hat{\\boldsymbol{J}}_1+\\hat{\\boldsymbol{J}}_2$",
                      "#E8B48C", 15)]:
    ax.annotate("", xy=o + v, xytext=o,
                arrowprops=dict(arrowstyle="-|>", color=c, lw=2.6))
    ax.text(*(o + v * 1.13), lb, color=c, fontsize=fs, ha="center", weight="bold")

ax.text(0.0, 2.62, "两个角动量，", color="#FAF8F4", fontsize=17, ha="center", weight="bold")
ax.text(0.0, 2.40, "合成一个总角动量", color="#FAF8F4", fontsize=17, ha="center", weight="bold")
ax.text(0.0, -1.95, "$j=j_1+j_2,\\ j_1+j_2-1,\\ \\cdots,\\ |j_1-j_2|$",
        color="#E8B48C", fontsize=15, ha="center")
ax.text(0.0, -2.32, "同一堆态，两种数法", color="#FFFFFF99", fontsize=11, ha="center")
ax.set_xlim(-3.4, 3.4)
ax.set_ylim(-2.6, 2.9)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- m 值计数图：j1=3, j2=1（m1 × m2 网格，按 m 着色） ----------
fig, ax = plt.subplots(figsize=(7.2, 4.6), facecolor=PAPER)
ax.set_facecolor(PAPER)

m1s = [3, 2, 1, 0, -1, -2, -3]
m2s = [1, 0, -1]
# m 值 -> 颜色（同一 m 同一色，teal→ochre 交替区分相邻对角线）
cmap = {4: "#1F4E5F", 3: "#C4622D", 2: "#1F4E5F", 1: "#C4622D",
        0: "#1F4E5F", -1: "#C4622D", -2: "#1F4E5F", -3: "#C4622D", -4: "#1F4E5F"}

for i, m1 in enumerate(m1s):
    for j, m2 in enumerate(m2s):
        m = m1 + m2
        ax.scatter(i, j, s=430, color=cmap[m], zorder=3, edgecolor="white", lw=1.5)
        ax.text(i, j, (f"{m:+d}" if m != 0 else "0"), color="white", fontsize=10.5, ha="center",
                va="center", zorder=4, weight="bold")

ax.set_xticks(range(len(m1s)))
ax.set_xticklabels([(f"{m:+d}" if m != 0 else "0") for m in m1s], fontsize=11, color=INK)
ax.set_yticks(range(len(m2s)))
ax.set_yticklabels([(f"{m:+d}" if m != 0 else "0") for m in m2s], fontsize=11, color=INK)
ax.set_xlabel("$m_1$", fontsize=12, color=INK)
ax.set_ylabel("$m_2$", fontsize=12, color=INK)
ax.set_xlim(-0.6, 6.6)
ax.set_ylim(-0.6, 2.6)
for s in ax.spines.values():
    s.set_visible(False)
ax.tick_params(length=0)

# 对角线注释：点数 1,2,3,3,3,3,3,2,1
counts = {4: 1, 3: 2, 2: 3, 1: 3, 0: 3, -1: 3, -2: 3, -3: 2, -4: 1}
ax.text(3.0, 3.05, "格点里的数是 $m=m_1+m_2$；同一斜行点数 = 该 $m$ 出现次数：1, 2, 3, 3, 3, 3, 3, 2, 1",
        fontsize=10.5, color=GRAY, ha="center")
save(fig, "fig_count.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
