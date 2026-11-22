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
PANEL_TEAL = "#23586B"

MEDIA = Path(__file__).parent / "media"
MEDIA.mkdir(exist_ok=True)

# ---------- fig_cover: conserved (flat) vs non-conserved (oscillating) ----------
fig, ax = plt.subplots(figsize=(5.0, 6.2), facecolor=PANEL_TEAL)
ax.set_facecolor(PANEL_TEAL)
t = np.linspace(0, 10, 400)
ax.plot(t, 0.62 + 0.0 * t, color="#F0B27A", lw=2.6)
ax.text(5.0, 0.70, "守恒量：$\\overline{F}(t)=$ 常数", color="#F0B27A",
        ha="center", fontsize=11.5)
ax.plot(t, 0.30 + 0.13 * np.sin(2.2 * t) * np.exp(-0.12 * t), color="#FFFFFF", lw=2.2, ls="--")
ax.text(5.0, 0.10, "一般力学量：$\\overline{F}(t)$ 随时间变化", color="#FFFFFF",
        ha="center", fontsize=11.5)
ax.grid(False)
ax.set_xticks([]); ax.set_yticks([])
ax.set_xlim(0, 10); ax.set_ylim(0, 0.9)
ax.set_xlabel("时间 $t$", color="#FFFFFF", fontsize=11.5)
for s in ax.spines.values():
    s.set_color("#FFFFFF55")
fig.tight_layout()
fig.savefig(MEDIA / "fig_cover.png", dpi=200, bbox_inches="tight", facecolor=PANEL_TEAL)
plt.close(fig)

# ---------- fig_intro: parity conserved under time evolution ----------
fig, axes = plt.subplots(1, 2, figsize=(7.4, 4.4), facecolor=PAPER)
x = np.linspace(-3, 3, 600)
psi0 = np.exp(-x**2 / 0.5)
psi1 = 0.85 * np.exp(-((np.abs(x) - 0.9) ** 2) / 0.28)  # 仍是偶函数，形状已变
for ax, y, lab in [(axes[0], psi0, "$t=0$：偶函数"),
                   (axes[1], psi1, "$t=t_1$：形状变了，仍是偶函数")]:
    ax.set_facecolor(PAPER)
    ax.plot(x, y, color=TEAL, lw=2.2)
    ax.fill_between(x, y, color=TEAL, alpha=0.14)
    ax.axvline(0, color=GRAY, lw=1.0, ls=":")
    ax.grid(False)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_ylim(0, 1.15)
    ax.set_title(lab, fontsize=11.5, color=INK)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
fig.suptitle("宇称守恒：偶函数演化成偶函数", fontsize=13, color=INK)
fig.tight_layout(rect=[0, 0, 1, 0.90])
fig.savefig(MEDIA / "fig_intro.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

print("done:", sorted(p.name for p in MEDIA.glob("*.png")))
