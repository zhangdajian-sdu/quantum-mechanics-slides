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


# ---------- 封面：四个总自旋态（teal 底） ----------
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)

ax.text(0.0, 2.62, "两个自旋 1/2 粒子，", color="#FAF8F4", fontsize=17,
        ha="center", weight="bold")
ax.text(0.0, 2.40, "拼出三重态与单态", color="#FAF8F4", fontsize=17,
        ha="center", weight="bold")

cells = [
    (-2.7, "$\\uparrow\\uparrow$", 13, False),
    (-0.9, "$(\\uparrow\\downarrow+\\downarrow\\uparrow)/\\sqrt{2}$", 10.5, False),
    (0.9, "$\\downarrow\\downarrow$", 13, False),
    (2.7, "$(\\uparrow\\downarrow-\\downarrow\\uparrow)/\\sqrt{2}$", 10.5, True),
]
for x0, txt, fs, singlet in cells:
    w = 1.66
    ax.add_patch(plt.Rectangle((x0 - w / 2, 0.0), w, 1.0, fill=False,
                               edgecolor="#E8B48C" if singlet else "#FFFFFF55",
                               lw=1.6 if singlet else 1.0))
    ax.text(x0, 0.5, txt, color="#E8B48C" if singlet else "#FAF8F4",
            fontsize=fs, ha="center", va="center")

# 分组标签
ax.plot([-3.53, 1.73], [-0.28, -0.28], color="#FFFFFF88", lw=1.2)
ax.text(-0.9, -0.62, "三重态 $s=1$（对称）", color="#FAF8F4", fontsize=13,
        ha="center", weight="bold")
ax.text(2.7, -0.62, "单态 $s=0$", color="#E8B48C", fontsize=13,
        ha="center", weight="bold")
ax.text(2.7, -0.92, "（反对称）", color="#E8B48C", fontsize=11, ha="center")

ax.text(0.0, -1.62, "三重态 $E=\\dfrac{A\\hbar^2}{4}$，单态 $E=-\\dfrac{3A\\hbar^2}{4}$",
        color="#FAF8F4", fontsize=14, ha="center")
ax.text(0.0, -2.05, "同一相互作用 $A\\hat{\\boldsymbol{S}}_1\\cdot\\hat{\\boldsymbol{S}}_2$，两伙态能量不同",
        color="#FFFFFF99", fontsize=10.5, ha="center")

ax.set_xlim(-3.7, 3.7)
ax.set_ylim(-2.4, 2.9)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- 自旋交换振荡：P(t) ----------
fig, ax = plt.subplots(figsize=(7.0, 4.4), facecolor=PAPER)
ax.set_facecolor(PAPER)

t = np.linspace(0, 2 * np.pi, 400)
p_ab = np.cos(t / 2) ** 2
p_ba = np.sin(t / 2) ** 2

ax.plot(t, p_ab, color=TEAL, lw=2.4, label="$|\\langle\\alpha\\beta|\\psi(t)\\rangle|^2=\\cos^2\\dfrac{A\\hbar t}{2}$")
ax.plot(t, p_ba, color=OCHRE, lw=2.4, ls="--", label="$|\\langle\\beta\\alpha|\\psi(t)\\rangle|^2=\\sin^2\\dfrac{A\\hbar t}{2}$")

ax.set_xlabel("$A\\hbar\\,t$", fontsize=12, color=INK)
ax.set_ylabel("几率", fontsize=12, color=INK)
ax.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi])
ax.set_xticklabels(["0", "$\\pi/2$", "$\\pi$", "$3\\pi/2$", "$2\\pi$"], fontsize=11)
ax.set_ylim(-0.05, 1.08)
ax.set_xlim(0, 2 * np.pi)
ax.tick_params(colors=GRAY, length=0)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color(HAIR)
ax.legend(fontsize=11.5, loc="upper center", frameon=False, ncol=1,
          bbox_to_anchor=(0.5, 1.22))
ax.text(np.pi, 0.44, "自旋交换振荡\n周期 $A\\hbar\\,t=2\\pi$", fontsize=10.5,
        color=GRAY, ha="center", va="center")
save(fig, "fig_osc.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
