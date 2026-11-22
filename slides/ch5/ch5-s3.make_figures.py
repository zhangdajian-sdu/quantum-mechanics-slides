"""第五章 §5.3 插图：封面题图 + 引入页示意图（同一态矢，两组基）"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot

setup_plot()

import numpy as np
import matplotlib.pyplot as plt

INK = "#20242B"
TEAL = "#1F4E5F"
OCHRE = "#C4622D"
GRAY = "#8A8F98"
PAPER = "#FAF8F4"
LIGHT = "#DCE6EA"
PANEL_TEAL = "#23586B"

OUT = Path(__file__).parent / "media"
OUT.mkdir(exist_ok=True)


def draw_basis(ax, angle_deg, color, labels, length=1.35, lw=1.8, fontsize=13):
    th = np.deg2rad(angle_deg)
    for k, lab in enumerate(labels):
        a = th + k * np.pi / 2
        ax.annotate(
            "", xy=(length * np.cos(a), length * np.sin(a)), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=color, lw=lw),
        )
        ax.text(
            1.16 * length * np.cos(a), 1.16 * length * np.sin(a), lab,
            color=color, fontsize=fontsize, ha="center", va="center",
        )


ANG_VEC = np.deg2rad(65)
VEC = 1.25 * np.array([np.cos(ANG_VEC), np.sin(ANG_VEC)])

# ---------- 封面题图：同一态矢，两组基（固定画布，不用 tight 裁剪） ----------
fig, axes = plt.subplots(
    2, 1, figsize=(5.2, 6.2),
    gridspec_kw=dict(left=0.02, right=0.98, top=0.97, bottom=0.03, hspace=0.55),
)
fig.patch.set_facecolor(PANEL_TEAL)

panels = [
    (axes[0], 0, LIGHT, (r"$U_1$", r"$U_2$"),
     r"A 表象：$\Psi=(C_1,\,C_2)^{\mathsf{T}}$"),
    (axes[1], 40, OCHRE, (r"$V_1$", r"$V_2$"),
     r"B 表象：$\Psi'=(C'_1,\,C'_2)^{\mathsf{T}}$"),
]
for ax, ang, col, labs, cap in panels:
    ax.set_facecolor(PANEL_TEAL)
    draw_basis(ax, ang, col, labs)
    ax.annotate("", xy=VEC, xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="#FFFFFF", lw=2.8))
    ax.text(VEC[0] + 0.07, VEC[1] + 0.14, r"$\psi$", color="#FFFFFF", fontsize=17)
    ax.text(-1.65, -1.62, cap, color="#FFFFFFCC", fontsize=13, ha="left")
    ax.set_xlim(-1.75, 1.75)
    ax.set_ylim(-1.75, 1.75)
    ax.set_aspect("equal")
    ax.axis("off")

fig.text(0.5, 0.505, r"$\Psi'=S^{\dagger}\Psi$", color="#FFFFFF",
         fontsize=19, ha="center", va="center")
fig.savefig(OUT / "fig_cover.png", dpi=220, facecolor=PANEL_TEAL)
plt.close(fig)

# ---------- 引入页：两组基叠加在同一图上 ----------
fig, ax = plt.subplots(figsize=(7.0, 4.6))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

draw_basis(ax, 0, TEAL, (r"$U_1$", r"$U_2$"))
draw_basis(ax, 40, OCHRE, (r"$V_1$", r"$V_2$"))
ax.annotate("", xy=VEC, xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.6))
ax.text(VEC[0] + 0.06, VEC[1] + 0.12, r"$\psi$", color=INK, fontsize=16)

# 到 U_1 与 V_1 轴的投影虚线
th = np.deg2rad(40)
for axis, col in [(np.array([1.0, 0.0]), TEAL),
                  (np.array([np.cos(th), np.sin(th)]), OCHRE)]:
    p = np.dot(VEC, axis) * axis
    ax.plot([VEC[0], p[0]], [VEC[1], p[1]], ls="--", lw=1.2, color=col)
    ax.plot([p[0]], [p[1]], marker="o", ms=4, color=col)

ax.text(-1.68, -0.95, "同一个态 $\\psi$：", fontsize=12.5, color=INK)
ax.text(-1.68, -1.25, "在 A 表象读出一列分量 $\\{C_n\\}$", fontsize=12.5, color=TEAL)
ax.text(-1.68, -1.55, "在 B 表象读出另一列 $\\{C'_n\\}$", fontsize=12.5, color=OCHRE)

ax.set_xlim(-1.75, 1.75)
ax.set_ylim(-1.75, 1.75)
ax.set_aspect("equal")
ax.axis("off")
fig.tight_layout()
fig.savefig(OUT / "fig_intro.png", dpi=200, facecolor=PAPER)
plt.close(fig)

# ---------- 新引入页：同一自旋态，换方向测量 ----------
fig = plt.figure(figsize=(7.4, 4.9))
fig.patch.set_facecolor(PAPER)

# 左：态矢示意（自旋向上态 |+z>）
axL = fig.add_axes([0.03, 0.16, 0.40, 0.72])
axL.set_facecolor(PAPER)
axL.annotate("", xy=(0, 1.15), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=3.0))
axL.text(0.08, 1.18, r"自旋态 $S_z=+\hbar/2$", color=TEAL, fontsize=14)
axL.text(-0.06, -0.28, r"态只有这一个，", color=INK, fontsize=12.5)
axL.text(-0.06, -0.52, r"换的是测量方向", color=INK, fontsize=12.5)
axL.set_xlim(-1.0, 1.0)
axL.set_ylim(-0.7, 1.5)
axL.set_aspect("equal")
axL.axis("off")

# 右上：沿 z 测
axA = fig.add_axes([0.52, 0.56, 0.42, 0.28])
axA.set_facecolor(PAPER)
axA.bar([0, 1], [1.0, 0.0], width=0.5, color=[TEAL, "#C9D6DB"])
axA.set_xticks([0, 1])
axA.set_xticklabels([r"$+z$", r"$-z$"], fontsize=12)
axA.set_yticks([0, 0.5, 1.0])
axA.set_ylim(0, 1.12)
axA.set_title(r"沿 $z$ 方向测：几率 1 与 0", fontsize=12, color=INK, pad=6)
for s in ("top", "right"):
    axA.spines[s].set_visible(False)

# 右下：沿 x 测
axB = fig.add_axes([0.52, 0.10, 0.42, 0.28])
axB.set_facecolor(PAPER)
axB.bar([0, 1], [0.5, 0.5], width=0.5, color=[OCHRE, "#E4C9B8"])
axB.set_xticks([0, 1])
axB.set_xticklabels([r"$+x$", r"$-x$"], fontsize=12)
axB.set_yticks([0, 0.5, 1.0])
axB.set_ylim(0, 1.12)
axB.set_title(r"沿 $x$ 方向测：几率各 $1/2$", fontsize=12, color=INK, pad=6)
for s in ("top", "right"):
    axB.spines[s].set_visible(False)

fig.text(0.5, 0.955,
         r"同一个 $S_z=+\hbar/2$ 的态，换方向测，几率不同",
         fontsize=13.5, color=INK, ha="center")
fig.savefig(OUT / "fig_spin.png", dpi=200, facecolor=PAPER)
plt.close(fig)

print("done:", [p.name for p in OUT.glob("*.png")])
