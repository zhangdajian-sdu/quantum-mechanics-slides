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


# ---------- 封面：时间够长，只留下「等能」的跃迁（teal 底） ----------
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)

x = np.linspace(-1, 1, 400)
for g, a in [(2.0, 0.35), (5.0, 0.6), (14.0, 1.0)]:
    y = np.sin(x * g * 3) ** 2 / (np.pi * (x * 3) ** 2 * g + 1e-12)
    y = y / y.max()
    ax.plot(x, y * 0.9 + 1.0, color="#FAF8F4", lw=1.4, alpha=a)
ax.annotate("", xy=(0.0, 2.35), xytext=(0.35, 1.45),
            arrowprops=dict(arrowstyle="-|>", color="#E8B48C", lw=1.8))
ax.text(0.08, 2.15, "t 增大：峰变高变窄", color="#E8B48C", fontsize=12)
ax.text(0.0, 0.62, "极限是一根「针」——δ 函数", color="#FFFFFF99", fontsize=11.5, ha="center")

# 底部：两个能级，只有等能的箭头留下
ax.plot([0.12, 0.88], [0.30, 0.30], color="#FAF8F4", lw=2.4, solid_capstyle="round")
ax.plot([0.12, 0.88], [0.10, 0.10], color="#FAF8F4", lw=2.4, solid_capstyle="round")
ax.annotate("", xy=(0.62, 0.10), xytext=(0.38, 0.30),
            arrowprops=dict(arrowstyle="-|>", color="#E8B48C", lw=2.0))
ax.text(0.66, 0.20, "只留下这样的", color="#E8B48C", fontsize=11, va="center")
ax.set_ylim(-0.05, 2.6)

ax.text(0.5, 2.44, "常微扰 + 足够长时间", color="#FAF8F4", fontsize=16.5, ha="center", weight="bold")
ax.text(0.5, 2.78, "只有「等能」的跃迁留下来", color="#FAF8F4", fontsize=12.5, ha="center")
ax.text(-1.0, -0.05, "", fontsize=1)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- sin² 峰随时间变窄变高，趋向 δ 函数 ----------
fig, ax = plt.subplots(figsize=(8.4, 5.2), facecolor=PAPER)
ax.set_facecolor(PAPER)

x = np.linspace(-3, 3, 1200)
for tt, c, lb in [(2 * np.pi, GRAY, "t 较小"), (6 * np.pi, "#5B7B8A", "t 较大"), (20 * np.pi, TEAL, "t 很大")]:
    y = np.sin(x * tt / 2) ** 2 / (np.pi * x ** 2 * tt / 2 + 1e-300)
    ax.plot(x, y, color=c, lw=2.0 if tt > 3 * np.pi else 1.6, label=lb)
ax.set_xlabel(r"$\omega_{mk}=(E_m-E_k)/\hbar$", fontsize=12.5, color=INK)
ax.set_ylabel(r"$\sin^{2}(\omega_{mk}t/2)\,/\,(\pi\omega_{mk}^{2}t/2)$", fontsize=12.5, color=INK)
ax.set_xlim(-3, 3); ax.set_ylim(0, 11)
ax.set_yticks([])
ax.tick_params(colors=GRAY, labelsize=10)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(HAIR)
ax.annotate("峰高 ∝ t，峰宽 ∝ 1/t，面积恒为 1", xy=(0.28, 9.6), xytext=(0.75, 10.2),
            fontsize=12, color=OCHRE,
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=1.4))
ax.annotate("t→∞ 时变成 $\\delta(\\omega_{mk})$：\n只有 $\\omega_{mk}=0$（等能）的跃迁",
            xy=(0.05, 10.0), xytext=(1.15, 5.2), fontsize=11.5, color=INK,
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.2))
ax.legend(frameon=False, fontsize=11.5, loc="upper left")
ax.set_title("时间越长，sin² 峰越高越窄——δ 函数的极限", fontsize=13.5, color=INK, pad=8)
save(fig, "fig_sinc.png")


# ---------- 动量空间晶格与薄球壳 ----------
fig, ax = plt.subplots(figsize=(8.4, 5.4), facecolor=PAPER)
ax.set_facecolor(PAPER)

n = np.arange(-3, 4)
gx, gy = np.meshgrid(n, n)
ax.plot(gx, gy, ".", ms=7, color=TEAL)
# 一个格子
ax.add_patch(plt.Rectangle((0, 0), 1, 1, fill=True, facecolor="#C4622D22",
                           edgecolor=OCHRE, lw=1.5))
ax.text(0.5, -0.32, r"每格占 $(2\pi\hbar/L)^{3}$", ha="center", fontsize=11.5, color=OCHRE)
# 薄球壳
th = np.linspace(0, 2 * np.pi, 200)
ax.plot(2.6 * np.cos(th), 2.6 * np.sin(th), color=GRAY, lw=1.6)
ax.plot(2.95 * np.cos(th), 2.95 * np.sin(th), color=GRAY, lw=1.6, ls=(0, (5, 4)))
ax.annotate(r"$p\sim p+\mathrm{d}p$ 的薄球壳，" "\n" r"方向取 $\mathrm{d}\Omega$",
            xy=(2.05, 1.85), xytext=(3.4, 3.0), fontsize=11.5, color=INK,
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.2))
ax.text(-3.4, 3.2, r"动量空间：每点 $(p_x,p_y,p_z)$ 是一个态", fontsize=12, color=INK)
ax.text(-3.4, -3.6, r"格点间距 $2\pi\hbar/L$——$L$ 很大时态非常密，可按连续处理",
        fontsize=11.5, color=GRAY)
ax.set_xlim(-4.2, 5.6); ax.set_ylim(-4.0, 3.8)
ax.set_aspect("equal")
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title("箱中自由粒子：动量取分立值，态均匀分布在晶格格点上", fontsize=13.5, color=INK, pad=8)
save(fig, "fig_lattice.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
