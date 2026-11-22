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


# ---------- 封面：球贝塞尔函数族（teal 底） ----------
from scipy.special import jv

def jl(l, x):
    return np.sqrt(np.pi / (2 * x)) * jv(l + 0.5, x)

x = np.linspace(0.02, 16, 1200)
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)
for l, c, lw in [(0, "#FAF8F4", 2.6), (1, "#E8B48C", 2.2), (2, "#8FB6C2", 2.2)]:
    ax.plot(x, jl(l, x), color=c, lw=lw)
ax.axhline(0, color="#FFFFFF55", lw=0.8)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- 导言：两种球方势阱剖面 ----------
fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.6), facecolor=PAPER)
for ax in axes:
    ax.set_facecolor(PAPER)
ax = axes[0]
ax.plot([0, 1, 1, 2], [0, 0, 3, 3], color=INK, lw=2)
ax.fill_between([0, 1], 0, 3, color=TEAL, alpha=0.10)
ax.annotate("V = 0", (0.5, 0.25), ha="center", fontsize=11, color=INK)
ax.annotate("V → ∞", (1.55, 2.55), ha="center", fontsize=11, color=INK)
ax.set_title("无限深球方势阱", fontsize=12, color=INK)
ax.set_xticks([1]); ax.set_xticklabels(["a"], fontsize=11)
ax.set_yticks([]); ax.set_xlim(0, 2); ax.set_ylim(0, 3)
ax.set_xlabel("r", fontsize=11)
ax = axes[1]
ax.plot([0, 1, 1, 2], [0, 0, 1.5, 1.5], color=INK, lw=2)
ax.fill_between([0, 1], 0, 1.5, color=OCHRE, alpha=0.12)
ax.annotate("V = 0", (0.5, 0.25), ha="center", fontsize=11, color=INK)
ax.annotate("V = $V_0$", (1.55, 1.7), ha="center", fontsize=11, color=INK)
ax.set_title("有限深球方势阱", fontsize=12, color=INK)
ax.set_xticks([1]); ax.set_xticklabels(["a"], fontsize=11)
ax.set_yticks([]); ax.set_xlim(0, 2); ax.set_ylim(0, 3)
ax.set_xlabel("r", fontsize=11)
for ax in axes:
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
fig.tight_layout()
save(fig, "fig_intro.png")


# ---------- 球贝塞尔函数与零点 ----------
fig, ax = plt.subplots(figsize=(7.8, 4.2), facecolor=PAPER)
ax.set_facecolor(PAPER)
for l, c, lab in [(0, INK, "$j_0$"), (1, TEAL, "$j_1$"), (2, OCHRE, "$j_2$")]:
    ax.plot(x, jl(l, x), color=c, lw=2, label=lab)
# j0 的零点 n*pi
for n in [1, 2, 3, 4]:
    ax.plot(n * np.pi, 0, "v", ms=8, color=INK)
ax.annotate("$x_{n0}=n\\pi$", (np.pi, 0.055), fontsize=11.5, color=INK, ha="center")
ax.axhline(0, color=GRAY, lw=0.8)
ax.legend(fontsize=11, frameon=False, loc="upper right")
ax.set_xlabel("$kr$", fontsize=11.5)
ax.set_xticks([np.pi, 2 * np.pi, 3 * np.pi, 4 * np.pi])
ax.set_xticklabels(["$\\pi$", "$2\\pi$", "$3\\pi$", "$4\\pi$"], fontsize=10.5)
ax.set_yticks([])
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
save(fig, "fig_bessel.png")


# ---------- 有限深 l=0 图解：η=-ζcotζ 与圆 ----------
fig, ax = plt.subplots(figsize=(7.2, 5.0), facecolor=PAPER)
ax.set_facecolor(PAPER)
z1 = np.linspace(np.pi / 2 + 0.02, np.pi - 0.02, 400)
ax.plot(z1, -z1 / np.tan(z1), color=TEAL, lw=2.2,
        label="$\\eta=-\\zeta\\cot\\zeta$")
# 两个半径的圆
for R, c, ls, lab in [(2.4, OCHRE, "-", "深阱：有交点"),
                      (1.2, GRAY, "--", "浅阱：无交点")]:
    th = np.linspace(0, np.pi / 2, 200)
    ax.plot(R * np.cos(th), R * np.sin(th), ls, color=c, lw=1.8, label=lab)
ax.axvline(np.pi / 2, color=GRAY, lw=1, ls=":")
ax.annotate("$\\zeta=\\pi/2$", (np.pi / 2, 4.6), fontsize=11, color=GRAY,
            ha="center")
ax.annotate("交点 → 束缚态", (2.0, 2.6), fontsize=11, color=OCHRE)
ax.set_xlim(0, 3.6); ax.set_ylim(0, 5)
ax.set_xlabel("$\\zeta=ka$", fontsize=11.5)
ax.set_ylabel("$\\eta=\\alpha a$", fontsize=11.5)
ax.legend(fontsize=10.5, frameon=False, loc="upper left")
ax.set_xticks([np.pi / 2, np.pi])
ax.set_xticklabels(["$\\pi/2$", "$\\pi$"], fontsize=10.5)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
save(fig, "fig_graph.png")


# ---------- 课外：有限深阱中 s 态 u(r)——波函数漏出阱外 ----------
r_in = np.linspace(0.001, 1, 300)
r_out = np.linspace(1, 3, 300)
# 基态：阱内约 3/4 个半波后接指数尾巴
k, alpha = 2.2, 1.1
A = 1.0
u_in = A * np.sin(k * r_in)
B = A * np.sin(k) * np.exp(alpha)
u_out = B * np.exp(-alpha * r_out)
fig, ax = plt.subplots(figsize=(7.4, 4.4), facecolor=PAPER)
ax.set_facecolor(PAPER)
ax.plot(r_in, u_in, color=TEAL, lw=2.4, label="阱内：$A\\sin kr$")
ax.plot(r_out, u_out, color=OCHRE, lw=2.4, label="阱外：$B\\,e^{-\\alpha r}$")
ax.axvline(1, color=GRAY, lw=1, ls=":")
ax.annotate("$r=a$", (1.0, -0.34), fontsize=11, color=GRAY, ha="center")
ax.fill_between(r_out, 0, u_out, color=OCHRE, alpha=0.12)
ax.annotate("漏出阱外的几率", (1.85, 0.16), fontsize=11, color=OCHRE)
ax.axhline(0, color=INK, lw=0.8)
ax.set_xlabel("r", fontsize=11.5)
ax.set_ylabel("$u(r)$", fontsize=11.5)
ax.set_xticks([]); ax.set_yticks([])
ax.legend(fontsize=10.5, frameon=False, loc="upper right")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
save(fig, "fig_extra.png")
