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

# ---------- fig_cover: oscillator expectation values on dark teal ----------
# xbar ~ cos(wt), pbar ~ -sin(wt); top: curves vs t, bottom: ellipse in phase plane
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5.0, 6.4), facecolor=PANEL_TEAL,
                               gridspec_kw={"height_ratios": [1.15, 1.0]})
for ax in (ax1, ax2):
    ax.set_facecolor(PANEL_TEAL)
    ax.grid(False)

t = np.linspace(0, 2 * np.pi, 400)
ax1.plot(t, np.cos(t), color="#F0B27A", lw=2.6, label="$\\overline{x}(t)$")
ax1.plot(t, -np.sin(t), color="#FFFFFF", lw=2.2, ls="--", label="$\\overline{p}(t)$")
ax1.set_xticks([]); ax1.set_yticks([])
ax1.legend(loc="upper center", bbox_to_anchor=(0.40, 1.02), frameon=False,
           fontsize=11, labelcolor="#FFFFFF", ncol=2)
for s in ax1.spines.values():
    s.set_color("#FFFFFF55")

th = np.linspace(0, 2 * np.pi, 300)
ax2.plot(np.cos(th), -np.sin(th), color="#F0B27A", lw=2.4)
ax2.plot([1], [0], marker="o", ms=7, color="#FFFFFF")
ax2.annotate("", xy=(0.05, -1.0), xytext=(0.72, -0.72),
             arrowprops=dict(arrowstyle="->", color="#FFFFFF", lw=1.6))
ax2.text(1.06, 0.02, "$t=0$", color="#FFFFFF", fontsize=10.5, va="center")
ax2.set_xlabel("$\\overline{x}$", color="#FFFFFF", fontsize=11.5)
ax2.set_ylabel("$\\overline{p}$", color="#FFFFFF", fontsize=11.5)
ax2.set_xticks([]); ax2.set_yticks([])
ax2.set_xlim(-1.45, 1.45); ax2.set_ylim(-1.35, 1.35)
ax2.set_aspect("equal")
for s in ax2.spines.values():
    s.set_color("#FFFFFF55")
fig.tight_layout(pad=1.6)
fig.savefig(MEDIA / "fig_cover.png", dpi=200, facecolor=PANEL_TEAL)
plt.close(fig)

# ---------- fig_intro: state rotates vs operator rotates ----------
fig, axes = plt.subplots(1, 2, figsize=(7.4, 4.2), facecolor=PAPER)

def draw_circle(ax, state_angle, op_angle, state_fixed, op_fixed):
    ax.set_facecolor(PAPER)
    circ = plt.Circle((0, 0), 1.0, fill=False, color=GRAY, lw=1.2, ls=":")
    ax.add_patch(circ)
    # operator axis (teal)
    ox, oy = np.cos(op_angle), np.sin(op_angle)
    ax.annotate("", xy=(0.92 * ox, 0.92 * oy), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color=TEAL, lw=2.4))
    ax.text(1.12 * ox, 1.12 * oy, "$\\hat{F}$", color=TEAL, fontsize=13,
            ha="center", va="center")
    # state vector (ochre)
    sx, sy = np.cos(state_angle), np.sin(state_angle)
    ax.annotate("", xy=(0.92 * sx, 0.92 * sy), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color=OCHRE, lw=2.4))
    ax.text(1.12 * sx, 1.12 * sy, "$\\psi$", color=OCHRE, fontsize=13,
            ha="center", va="center")
    # ghost of the moving one
    if state_fixed:  # operator moves: show ghosts of operator (trailing behind)
        for a in (op_angle - 0.7, op_angle - 1.4):
            ax.annotate("", xy=(0.85 * np.cos(a), 0.85 * np.sin(a)), xytext=(0, 0),
                        arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2, alpha=0.35))
        ax.text(0, -1.42, "态不动，算符在动", color=INK, fontsize=11.5,
                ha="center")
    else:  # state moves: ghosts of state
        for a in (state_angle + 0.7, state_angle + 1.4):
            ax.annotate("", xy=(0.85 * np.cos(a), 0.85 * np.sin(a)), xytext=(0, 0),
                        arrowprops=dict(arrowstyle="->", color=OCHRE, lw=1.2, alpha=0.35))
        ax.text(0, -1.42, "算符不动，态在动", color=INK, fontsize=11.5,
                ha="center")
    ax.grid(False)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.65, 1.45)
    ax.set_aspect("equal")
    for s in ax.spines.values():
        s.set_visible(False)

draw_circle(axes[0], state_angle=1.15, op_angle=0.42, state_fixed=False, op_fixed=True)
axes[0].set_title("薛定谔绘景", fontsize=13, color=INK)
draw_circle(axes[1], state_angle=1.15, op_angle=0.42, state_fixed=True, op_fixed=False)
axes[1].set_title("海森伯绘景", fontsize=13, color=INK)
fig.tight_layout()
fig.savefig(MEDIA / "fig_intro.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

# ---------- fig_example: xbar(t), pbar(t) with quarter-period markers ----------
fig, ax = plt.subplots(figsize=(7.4, 4.0), facecolor=PAPER)
ax.set_facecolor(PAPER)
t = np.linspace(0, 2 * np.pi, 400)
ax.plot(t, np.cos(t), color=TEAL, lw=2.4, label="$\\overline{x}(t)=\\frac{1}{\\sqrt{2}\\,\\alpha}\\cos\\omega t$")
ax.plot(t, -np.sin(t), color=OCHRE, lw=2.2, ls="--", label="$\\overline{p}(t)=-\\frac{\\alpha\\hbar}{\\sqrt{2}}\\sin\\omega t$")
for tt, name in [(0, "$t=0$"), (np.pi / 2, "$T/4$"), (np.pi, "$T/2$")]:
    ax.plot([tt], [np.cos(tt)], marker="o", ms=6, color=TEAL)
    ax.plot([tt], [-np.sin(tt)], marker="s", ms=6, color=OCHRE)
ax.axhline(0, color=GRAY, lw=0.8)
ax.grid(False)
ax.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi])
ax.set_xticklabels(["0", "$T/4$", "$T/2$", "$3T/4$", "$T$"], fontsize=10.5)
ax.set_yticks([])
ax.set_xlabel("时间", fontsize=11.5, color=INK)
ax.legend(loc="lower right", frameon=False, fontsize=10.5)
ax.set_title("例题(2)：$\\psi(x,0)=[\\psi_0(x)+\\psi_1(x)]/\\sqrt{2}$ 的平均值振荡",
             fontsize=12, color=INK)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(MEDIA / "fig_example.png", dpi=200, bbox_inches="tight", facecolor=PAPER)
plt.close(fig)

print("done:", sorted(p.name for p in MEDIA.glob("*.png")))
