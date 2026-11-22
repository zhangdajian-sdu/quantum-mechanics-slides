import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
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


# ---------- 封面：三个矩阵，穷尽二维（teal 底） ----------
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)

mats = [
    ("$\\sigma_x$", [["0", "1"], ["1", "0"]]),
    ("$\\sigma_y$", [["0", "$-\\mathrm{i}$"], ["$\\mathrm{i}$", "0"]]),
    ("$\\sigma_z$", [["1", "0"], ["0", "$-1$"]]),
]
cw, ch = 0.66, 0.58  # cell 宽高
for k, (name, m) in enumerate(mats):
    x0 = -1.95 + k * 1.95
    y0 = 0.0
    ax.text(x0 + cw, y0 + 2 * ch + 0.42, name, color="#FAF8F4", fontsize=17,
            ha="center", weight="bold")
    for i in range(2):
        for j in range(2):
            x = x0 + j * cw
            y = y0 + (1 - i) * ch
            ax.add_patch(plt.Rectangle((x, y), cw, ch, fill=False,
                                       edgecolor="#FFFFFF55", lw=1.0))
            entry = m[i][j]
            dim = entry in ("0",)
            ax.text(x + cw / 2, y + ch / 2, entry, fontsize=15,
                    color="#FFFFFF66" if dim else "#E8B48C",
                    ha="center", va="center")

ax.text(0.0, 2.62, "三个矩阵，", color="#FAF8F4", fontsize=17, ha="center", weight="bold")
ax.text(0.0, 2.40, "穷尽自旋的二维世界", color="#FAF8F4", fontsize=17, ha="center", weight="bold")
ax.text(0.0, 2.10, "$\\hat{\\boldsymbol{S}}=\\dfrac{\\hbar}{2}\\hat{\\boldsymbol{\\sigma}}$",
        color="#E8B48C", fontsize=16, ha="center")
ax.text(0.0, -0.75, "泡利矩阵：自旋世界的字母表", color="#FFFFFF99", fontsize=11, ha="center")
ax.set_xlim(-3.3, 3.3)
ax.set_ylim(-1.0, 2.9)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- 任意方向 n(θ,φ) 示意 ----------
fig, ax = plt.subplots(figsize=(6.4, 5.0), facecolor=PAPER)
ax.set_facecolor(PAPER)

o = np.array([0.0, 0.0])
zdir = np.array([0.0, 2.9])
xdir = np.array([2.3, -0.95])
ydir = np.array([-1.9, -0.85])
ndir = np.array([1.55, 1.95])

for d, lb, c in [(zdir, "$z$", INK), (xdir, "$x$", INK), (ydir, "$y$", INK)]:
    ax.annotate("", xy=o + d, xytext=o,
                arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.5))
    ax.text(*(o + d * 1.12), lb, fontsize=13, color=INK, ha="center")

# n 的投影与 φ
proj = np.array([1.30, -0.54])
ax.plot([ndir[0], proj[0]], [ndir[1], proj[1]], color=GRAY, lw=1.1, ls="--")
ax.plot([o[0], proj[0]], [o[1], proj[1]], color=GRAY, lw=1.1, ls="--")
ax.add_patch(Arc(o, 1.5, 0.62, angle=0, theta1=-24, theta2=0, color=TEAL, lw=1.4))
ax.text(0.98, -0.42, "$\\varphi$", fontsize=13, color=TEAL)

# n 矢量与 θ
ax.annotate("", xy=ndir, xytext=o,
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=2.4))
ax.text(ndir[0] + 0.14, ndir[1] + 0.06, "$\\boldsymbol{n}(\\theta,\\varphi)$",
        fontsize=14, color=OCHRE)
ax.add_patch(Arc(o, 2.2, 2.2, angle=0, theta1=51, theta2=90, color=TEAL, lw=1.4))
ax.text(0.42, 1.55, "$\\theta$", fontsize=13, color=TEAL)

ax.text(-1.75, 2.45, "$\\hat{S}_{n}=\\hat{\\boldsymbol{S}}\\cdot\\boldsymbol{n}$",
        fontsize=15, color=INK)
ax.set_xlim(-2.6, 3.1); ax.set_ylim(-1.5, 3.2)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_bloch.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
