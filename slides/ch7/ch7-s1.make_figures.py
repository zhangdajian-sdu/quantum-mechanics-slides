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


# ---------- 封面：能级在微扰下移动（teal 底） ----------
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)

levels = [0.5, 1.5, 2.5, 3.5]
shift = [-0.12, -0.16, -0.20, -0.24]
for i, (e, d) in enumerate(zip(levels, shift)):
    y0 = e
    y1 = e + d
    ax.plot([0.08, 0.40], [y0, y0], color="#FAF8F4", lw=2.6, solid_capstyle="round")
    ax.plot([0.60, 0.92], [y1, y1], color="#E8B48C", lw=2.2, ls=(0, (6, 4)),
            solid_capstyle="round")
    ax.annotate("", xy=(0.58, y1), xytext=(0.42, y0),
                arrowprops=dict(arrowstyle="-|>", color="#FFFFFF88", lw=1.4,
                                connectionstyle="arc3,rad=-0.25"))
ax.text(0.24, 4.05, r"$E_n^{(0)}$", color="#FAF8F4", fontsize=17, ha="center")
ax.text(0.76, 4.05, r"$E_n$", color="#E8B48C", fontsize=17, ha="center")
ax.text(0.24, 0.18, "会解的", color="#FFFFFF99", fontsize=13, ha="center")
ax.text(0.76, 0.18, "真实的", color="#FFFFFF99", fontsize=13, ha="center")
ax.set_xlim(0, 1); ax.set_ylim(0, 4.4)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- 引入：弱电场中的带电谐振子 ----------
fig, ax = plt.subplots(figsize=(8.4, 6.0), facecolor=PAPER)
ax.set_facecolor(PAPER)

x = np.linspace(-3.1, 3.1, 600)
V0 = 0.5 * x**2
eps = 0.55                      # eε，弱场
V1 = 0.5 * x**2 - eps * x
dE = eps**2 / 2                 # e²ε² / 2μω²（μ=ω=1）
x0 = eps                        # 新平衡点

ax.plot(x, V0, color=INK, lw=2.4, label=r"$V_0=\frac{1}{2}\mu\omega^2x^2$")
ax.plot(x, V1, color=OCHRE, lw=2.2, ls="--", label=r"$V_0-e\varepsilon x$")

for n in (0, 1):
    E = n + 0.5
    half = np.sqrt(2 * E)
    ax.plot([-half, half], [E, E], color=TEAL, lw=1.8)
    Es = E - dE
    # 交点条件：½(x−x0)² − dE = Es → 半宽 = sqrt(2(Es+dE))，与原能级线相同
    hs = np.sqrt(2 * (Es + dE))
    ax.plot([x0 - hs, x0 + hs], [Es, Es], color=OCHRE, lw=1.8, ls=(0, (5, 3)))

# 标出平衡点位移 x0 与新最低点
ax.axvline(x0, color=GRAY, lw=1.2, ls=(0, (2, 3)), ymin=0, ymax=0.62)
ax.plot([x0], [-dE], marker="o", ms=5, color=OCHRE)
ax.annotate("平衡点位移 $x_0$", xy=(x0, -dE), xytext=(x0 + 0.55, -dE + 0.55),
            fontsize=11.5, color=GRAY,
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.1))

ax.set_xlabel("x", fontsize=12)
ax.set_ylabel("V", fontsize=12)
ax.set_xlim(-3.1, 3.1); ax.set_ylim(-0.6, 4.2)
ax.set_xticks([]); ax.set_yticks([])
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color(HAIR)
ax.legend(loc="upper center", fontsize=12, frameon=False)
save(fig, "fig_intro.png")


# ---------- 适用条件：各级近似 vs 严格解（习题 4 模型） ----------
fig, ax = plt.subplots(figsize=(8.0, 4.5), facecolor=PAPER)
ax.set_facecolor(PAPER)

lam = np.linspace(0, 1.6, 400)
exact = np.sqrt(1 + lam)
o0 = np.ones_like(lam)
o1 = 1 + lam / 2
o2 = o1 - lam**2 / 8
o3 = o2 + lam**3 / 16

ax.plot(lam, exact, color=INK, lw=2.6, label="严格解 √(1+λ)")
ax.plot(lam, o0, color=GRAY, lw=1.6, ls=":", label="零级")
ax.plot(lam, o1, color=OCHRE, lw=1.8, ls="--", label="到一级")
ax.plot(lam, o2, color=TEAL, lw=1.8, ls="-.", label="到二级")
ax.plot(lam, o3, color="#6B4E8E", lw=1.8, ls=(0, (1, 1.6)), label="到三级")
ax.axvline(1.0, color=HAIR, lw=1.4)
ax.text(1.02, 0.62, "λ = 1", fontsize=11, color=GRAY)
ax.set_xlabel("λ（微扰强度）", fontsize=12)
ax.set_ylabel(r"$E_0\,/\,\frac{1}{2}\hbar\omega$", fontsize=13)
ax.set_xlim(0, 1.6); ax.set_ylim(0.5, 2.1)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color(HAIR)
ax.tick_params(colors=GRAY, labelsize=10)
ax.legend(loc="upper left", fontsize=10.5, frameon=False)
save(fig, "fig_converge.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
