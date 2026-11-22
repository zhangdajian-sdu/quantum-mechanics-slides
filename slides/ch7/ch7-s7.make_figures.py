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


def wavy(ax, x0, x1, y, color, lw=1.8, n=6, amp=0.035):
    t = np.linspace(0, 1, 300)
    xs = x0 + t * (x1 - x0)
    ys = y + amp * np.sin(t * n * 2 * np.pi)
    ax.plot(xs, ys, color=color, lw=lw)


# ---------- 封面：三种跃迁过程（teal 底） ----------
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)

W = "#FAF8F4"
L = "#E8B48C"

def mini(xc, title, mode):
    ylo, yhi = 0.10, 0.42
    ax.plot([xc - 0.16, xc + 0.16], [ylo, ylo], color=W, lw=2.4, solid_capstyle="round")
    ax.plot([xc - 0.16, xc + 0.16], [yhi, yhi], color=W, lw=2.4, solid_capstyle="round")
    if mode == "abs":
        wavy(ax, xc - 0.30, xc - 0.04, 0.26, L, lw=1.6, n=4, amp=0.02)
        ax.annotate("", xy=(xc + 0.04, yhi - 0.01), xytext=(xc + 0.04, ylo + 0.01),
                    arrowprops=dict(arrowstyle="-|>", color=L, lw=1.8))
    elif mode == "stim":
        wavy(ax, xc - 0.30, xc - 0.06, 0.26, L, lw=1.6, n=4, amp=0.02)
        ax.annotate("", xy=(xc + 0.02, ylo + 0.01), xytext=(xc + 0.02, yhi - 0.01),
                    arrowprops=dict(arrowstyle="-|>", color=L, lw=1.8))
        wavy(ax, xc + 0.08, xc + 0.30, 0.26, L, lw=1.6, n=4, amp=0.02)
    else:
        ax.annotate("", xy=(xc - 0.02, ylo + 0.01), xytext=(xc - 0.02, yhi - 0.01),
                    arrowprops=dict(arrowstyle="-|>", color=L, lw=1.8))
        wavy(ax, xc + 0.06, xc + 0.30, 0.26, L, lw=1.6, n=4, amp=0.02)
    ax.text(xc, -0.06, title, color=W, fontsize=12, ha="center")

mini(0.17, "共振吸收", "abs")
mini(0.50, "共振发射", "stim")
mini(0.83, "自发发射", "spon")

ax.text(0.5, 0.72, "没有光照，激发态原子", color=W, fontsize=17, ha="center", weight="bold")
ax.text(0.5, 0.64, "也会自己发光", color=W, fontsize=17, ha="center", weight="bold")
ax.text(0.5, 0.54, "爱因斯坦用热力学平衡「借」出了答案", color="#FFFFFF99", fontsize=11.5, ha="center")
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.16, 0.85)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- Planck 辐射公式 ----------
fig, ax = plt.subplots(figsize=(8.4, 5.0), facecolor=PAPER)
ax.set_facecolor(PAPER)

x = np.linspace(0.02, 7.0, 1200)
for T, c, lb in [(1.0, "#5B7B8A", "温度 T"), (1.6, TEAL, "更高温度 T′")]:
    y = x ** 3 / (np.exp(x / T) - 1)
    ax.plot(x, y / 5.4, color=c, lw=2.0, label=lb)

ax.set_xlabel(r"角频率 $\omega$", fontsize=12.5, color=INK)
ax.set_ylabel(r"辐射场强度 $I(\omega)$", fontsize=12.5, color=INK)
ax.set_xticks([]); ax.set_yticks([])
ax.set_xlim(0, 7.0); ax.set_ylim(0, 1.05)
ax.tick_params(colors=GRAY, labelsize=10)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(HAIR)
ax.plot([2.2], [0.246], "o", color=OCHRE, ms=7)
ax.annotate("原子只关心共振频率处的值\n$I(\\omega_{km})$",
            xy=(2.2, 0.246), xytext=(3.3, 0.42), fontsize=12, color=OCHRE,
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=1.4))
ax.legend(frameon=False, fontsize=11.5, loc="upper left")
ax.set_title("黑体空腔中的辐射场（式 2）：温度恒定，谱形恒定", fontsize=13.5, color=INK, pad=8)
save(fig, "fig_planck.png")


# ---------- 细致平衡：三种过程 ----------
fig, ax = plt.subplots(figsize=(8.4, 5.0), facecolor=PAPER)
ax.set_facecolor(PAPER)

ylo, yhi = 0.22, 0.78
ax.plot([0.28, 0.72], [ylo, ylo], color=TEAL, lw=3.2, solid_capstyle="round")
ax.plot([0.28, 0.72], [yhi, yhi], color=TEAL, lw=3.2, solid_capstyle="round")
ax.text(0.76, ylo, "$\\varphi_m$（低能态，$N_m$ 个原子）", fontsize=12.5, color=INK, va="center")
ax.text(0.76, yhi, "$\\varphi_k$（高能态，$N_k$ 个原子）", fontsize=12.5, color=INK, va="center")

# 吸收（向上，左侧）
ax.annotate("", xy=(0.38, yhi - 0.02), xytext=(0.38, ylo + 0.02),
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=2.4))
ax.text(0.325, 0.50, "吸收", fontsize=12.5, color=INK, ha="center", va="center")

# 受激发射（向下，中间）
ax.annotate("", xy=(0.53, ylo + 0.02), xytext=(0.53, yhi - 0.02),
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=2.4))
ax.text(0.475, 0.50, "共振\n发射", fontsize=12.5, color=INK, ha="center", va="center")

# 自发发射（向下，右侧，虚线）
ax.annotate("", xy=(0.68, ylo + 0.02), xytext=(0.68, yhi - 0.02),
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=2.0, linestyle="--"))
ax.text(0.755, 0.50, "自发\n发射", fontsize=12.5, color=INK, ha="center", va="center")

ax.text(0.55, 0.99, "细致平衡：向下的光子数 = 向上的光子数", fontsize=13.5, color=INK, ha="center")
ax.text(0.55, -0.07, "$N_k A_{k\\to m}+N_k B_{k\\to m} I(\\omega_{km})\\;=\\;N_m B_{m\\to k} I(\\omega_{km})$（式 9）",
        fontsize=12.5, color=INK, ha="center")
ax.text(0.55, -0.16, "自发发射（虚线）不需要光来「点燃」——它就是我们要算的量",
        fontsize=11, color=GRAY, ha="center")
ax.set_xlim(0.10, 1.60); ax.set_ylim(-0.22, 1.08)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_balance.png")


# ---------- 激发态指数衰减与寿命 ----------
fig, ax = plt.subplots(figsize=(8.4, 4.8), facecolor=PAPER)
ax.set_facecolor(PAPER)

t = np.linspace(0, 4, 400)
ax.plot(t, np.exp(-t), color=TEAL, lw=2.2)
ax.axvline(1.0, color=GRAY, lw=1.2, linestyle="--")
ax.plot([1.0], [np.exp(-1)], "o", color=OCHRE, ms=7)
ax.annotate("$t=\\tau=1/A_{k\\to m}$ 时\n$N_k$ 降到 $1/\\mathrm{e}$",
            xy=(1.0, np.exp(-1)), xytext=(1.55, 0.55), fontsize=12.5, color=OCHRE,
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=1.4))
ax.set_xlabel(r"时间 $t$（单位：$\tau$）", fontsize=12.5, color=INK)
ax.set_ylabel(r"激发态原子数 $N_k(t)$", fontsize=12.5, color=INK)
ax.set_xticks([]); ax.set_yticks([])
ax.set_xlim(0, 4); ax.set_ylim(0, 1.05)
ax.tick_params(colors=GRAY, labelsize=10)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(HAIR)
ax.set_title("$N_k(t)=N_k(0)\\,\\mathrm{e}^{-A_{k\\to m}t}$：$A$ 越大，激发态越短命", fontsize=13.5, color=INK, pad=8)
save(fig, "fig_decay.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
