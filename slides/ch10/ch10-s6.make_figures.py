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


# ---------- 封面：同一方向 θ 的两种不可区分事件（teal 底，竖版） ----------
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)

W = "#FAF8F4"
OR = "#E8B48C"
th = np.deg2rad(38)

# 入射束
ax.annotate("", xy=(2.0, 0), xytext=(-3.6, 0),
            arrowprops=dict(arrowstyle="-|>", color=W, lw=2.2))
ax.text(-2.6, -0.42, "入射（沿 z 轴）", color=W, fontsize=12, ha="center")
ax.plot(0, 0, "o", ms=10, color=OR)

# 事件 A：散射粒子到 θ
d1 = np.array([np.cos(th), np.sin(th)]) * 3.1
ax.annotate("", xy=d1, xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=W, lw=2.2))
ax.plot(*d1, "o", ms=13, color=W)
ax.text(d1[0] + 0.25, d1[1] + 0.28, r"$f(\theta,\varphi)$", color=W, fontsize=14)

# 事件 B：散射粒子到 π-θ，反冲靶到 θ
d2 = np.array([-np.cos(th), np.sin(th)]) * 3.1
ax.annotate("", xy=d2, xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=OR, lw=2.2, linestyle="--"))
ax.plot(*d2, "o", ms=13, color=OR)
ax.text(d2[0] - 0.4, d2[1] + 0.28, r"$f(\pi-\theta,\ \varphi+\pi)$", color=OR,
        fontsize=14, ha="right")

# θ 方向探测器（两种事件都落到这里）
ax.add_patch(plt.Rectangle((d1[0] - 0.55, d1[1] + 0.75), 1.1, 0.62,
                           fill=False, edgecolor=W, lw=1.6))
ax.text(d1[0], d1[1] + 1.72, "探测器", color=W, fontsize=12, ha="center")
ax.text(0, -1.5, "θ 方向的计数 = 散射的入射粒子 + 反冲的靶粒子",
        color=W, fontsize=12.5, ha="center")
ax.text(0, -2.15, "全同粒子无法区分这两种事件", color=OR, fontsize=13, ha="center")
ax.text(0, -3.3, r"$\sigma(\theta,\varphi)=|f(\theta,\varphi)+f(\pi-\theta,\varphi+\pi)|^{2}$",
        color=W, fontsize=15, ha="center")

ax.set_xlim(-5.2, 5.2)
ax.set_ylim(-4.9, 4.6)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- 干涉：σ(θ) 关于 π/2 对称，90° 处 4|f|² vs 2|f|² vs 0（示意） ----------
fig, ax = plt.subplots(figsize=(7.2, 4.9), facecolor=PAPER)
ax.set_facecolor(PAPER)

thg = np.linspace(0.03, np.pi - 0.03, 400)
A = np.sqrt(1 + 0.25 * np.cos(thg))
f = A * np.exp(0.5j * thg)
A2 = np.sqrt(1 + 0.25 * np.cos(np.pi - thg))
f2 = A2 * np.exp(0.5j * (np.pi - thg))

s_cl = np.abs(f) ** 2 + np.abs(f2) ** 2
s_b = np.abs(f + f2) ** 2
s_f = np.abs(f - f2) ** 2

ax.plot(thg, s_b, color=TEAL, lw=2.4,
        label=r"玻色子 / 单态：$|f(\theta)+f(\pi-\theta)|^{2}$")
ax.plot(thg, s_cl, color=GRAY, lw=1.8, ls="--",
        label=r"经典计数：$|f(\theta)|^{2}+|f(\pi-\theta)|^{2}$")
ax.plot(thg, s_f, color=OCHRE, lw=2.4,
        label=r"费米子三重态：$|f(\theta)-f(\pi-\theta)|^{2}$")

ax.axvline(np.pi / 2, color=GRAY, lw=0.8, alpha=0.5)
ax.plot(np.pi / 2, 4, "o", ms=6, color=TEAL)
ax.plot(np.pi / 2, 2, "o", ms=6, color=GRAY)
ax.plot(np.pi / 2, 0, "o", ms=6, color=OCHRE)
ax.annotate(r"$4|f(\pi/2)|^{2}$", xy=(np.pi / 2, 4), xytext=(np.pi / 2 + 0.15, 3.86),
            fontsize=12, color=TEAL)
ax.annotate(r"$2|f(\pi/2)|^{2}$", xy=(np.pi / 2, 2), xytext=(2.25, 2.12),
            fontsize=12, color=GRAY)
ax.annotate("0", xy=(np.pi / 2, 0), xytext=(np.pi / 2 + 0.15, 0.08),
            fontsize=12, color=OCHRE)

ax.set_xticks([0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi])
ax.set_xticklabels(["0", r"$\pi/4$", r"$\pi/2$", r"$3\pi/4$", r"$\pi$"], fontsize=11)
ax.set_yticks([])
ax.set_xlabel(r"质心系散射角 $\theta$", fontsize=12)
ax.set_ylabel(r"$\sigma(\theta)$（示意）", fontsize=12)
ax.set_xlim(0, np.pi)
ax.set_ylim(-0.15, 4.45)
ax.legend(fontsize=10, loc="lower center", bbox_to_anchor=(0.5, 1.01),
          frameon=False, handlelength=1.8)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
save(fig, "fig_interf.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
