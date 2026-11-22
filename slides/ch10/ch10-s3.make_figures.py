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


# ---------- 封面：高速粒子被轻微偏转 + 波矢三角形（teal 底，竖版） ----------
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)

# 势场区
circ = plt.Circle((0, 0), 1.5, color="#FAF8F4", alpha=0.10)
ax.add_patch(circ)
ax.plot(0, 0, "o", ms=12, color="#E8B48C", mec="#FAF8F4", mew=1.4)
ax.text(0.0, -1.95, "V(r)", color="#E8B48C", fontsize=13, ha="center")

# 入射（快，几乎不偏）与出射
ax.annotate("", xy=(-1.9, 0.42), xytext=(-4.3, 0.42),
            arrowprops=dict(arrowstyle="-|>", color="#FAF8F4", lw=2.0))
th = np.deg2rad(16)
ax.annotate("", xy=(1.5 + 2.6 * np.cos(th), 0.42 + 2.6 * np.sin(th)),
            xytext=(1.4, 0.42),
            arrowprops=dict(arrowstyle="-|>", color="#FAF8F4", lw=2.0))
ax.plot([1.4, 4.0], [0.42, 0.42], color="#FAF8F4", lw=0.9, ls=(0, (3, 3)), alpha=0.6)
ax.text(3.6, 0.62, r"$\theta$", color="#E8B48C", fontsize=14)

# 波矢三角形（下方）
ox, oy = -1.6, -3.6
L = 2.6
ax.annotate("", xy=(ox + L, oy), xytext=(ox, oy),
            arrowprops=dict(arrowstyle="-|>", color="#FAF8F4", lw=1.8))
thq = np.deg2rad(38)
ax.annotate("", xy=(ox + L * np.cos(thq) * 1.0 + L * (1 - np.cos(thq)), oy + L * np.sin(thq)),
            xytext=(ox, oy),
            arrowprops=dict(arrowstyle="-|>", color="#FAF8F4", lw=1.8))
kx, ky = ox + L * np.cos(thq), oy + L * np.sin(thq)
ax.annotate("", xy=(kx, ky), xytext=(ox + L, oy),
            arrowprops=dict(arrowstyle="-|>", color="#E8B48C", lw=1.8))
ax.text(ox + L * 0.45, oy - 0.3, r"$k_0$", color="#FAF8F4", fontsize=14)
ax.text(ox + L * 0.28, oy + 1.05, r"$k$", color="#FAF8F4", fontsize=14)
ax.text(ox + L * 0.98, oy + 0.85, r"$q$", color="#E8B48C", fontsize=15)

ax.text(0, 3.5, r"$q=2k\sin\dfrac{\theta}{2}$", color="#E8B48C", fontsize=16, ha="center")

ax.set_xlim(-4.6, 4.6)
ax.set_ylim(-4.9, 4.2)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- 波矢三角形：q = k − k0（仿教材图 10.3） ----------
fig, ax = plt.subplots(figsize=(6.8, 3.6), facecolor=PAPER)
ax.set_facecolor(PAPER)

ox, oy = 0.0, 0.0
L = 4.0
th = np.deg2rad(52)
# k0
ax.annotate("", xy=(ox + L, oy), xytext=(ox, oy),
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2.0))
ax.text(ox + L * 0.5, oy - 0.34, r"$k_0$", fontsize=14, color=TEAL, ha="center")
# k
kx, ky = L * np.cos(th), L * np.sin(th)
ax.annotate("", xy=(kx, ky), xytext=(ox, oy),
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2.0))
ax.text(kx * 0.42 - 0.28, ky * 0.55, r"$k$", fontsize=14, color=TEAL)
# q = k - k0
ax.annotate("", xy=(kx, ky), xytext=(ox + L, oy),
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=2.0))
ax.text((kx + L) / 2 + 0.22, ky / 2, r"$q=k-k_0$", fontsize=14, color=OCHRE)
# 等腰标记 |k|=|k0|
ax.text(ox + L * 0.5, oy + 0.16, "", fontsize=10)
arc = np.linspace(0, th, 80)
ax.plot(ox + 1.15 * np.cos(arc), oy + 1.15 * np.sin(arc), color=INK, lw=1.2)
ax.text(ox + 1.38, oy + 0.42, r"$\theta$", fontsize=14, color=INK)
# 中垂虚线说明 q=2k sin(θ/2)
mx, my = (ox + L + kx) / 2, ky / 2
ax.plot([ox + 0, (ox + L + kx) / 2], [oy, ky / 2], color=GRAY, lw=0.9, ls=(0, (4, 3)))
ax.text(-0.45, 3.32, r"$|k|=|k_0|$（弹性）$\Rightarrow q=2k\sin\dfrac{\theta}{2}$",
        fontsize=13, color=INK)

ax.set_xlim(-0.6, 5.6)
ax.set_ylim(-0.8, 3.6)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_q.png")


# ---------- 卢瑟福角分布：σ ∝ csc^4(θ/2) ----------
fig, ax = plt.subplots(figsize=(7.2, 3.3), facecolor=PAPER)
ax.set_facecolor(PAPER)

th = np.linspace(np.deg2rad(6), np.pi, 400)
sig = 1.0 / np.sin(th / 2) ** 4
ax.semilogy(np.rad2deg(th), sig, color=TEAL, lw=2.2)
ax.axvline(180, color=GRAY, lw=0.8, ls=":")
ax.set_xlabel(r"$\theta$（度）", fontsize=11, color=INK)
ax.set_ylabel(r"$\sigma(\theta)$（对数坐标）", fontsize=11, color=INK)
ax.text(38, 300, "前向峰：小角度截面巨大", fontsize=11.5, color=OCHRE)
ax.text(120, 0.5, r"$\sigma\propto\csc^{4}\dfrac{\theta}{2}$", fontsize=13, color=TEAL)
ax.set_xlim(0, 180)
ax.set_ylim(0.06, 3000)
ax.tick_params(labelsize=10, colors=INK)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
fig.tight_layout()
save(fig, "fig_ruth.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
