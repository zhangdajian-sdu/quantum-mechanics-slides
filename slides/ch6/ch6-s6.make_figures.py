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


# ---------- 封面：回旋轨道 ↔ 朗道能级（teal 底） ----------
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)
th = np.linspace(0, 2 * np.pi, 400)
cols = ["#FAF8F4", "#E8B48C", "#8FB6C2", "#FFFFFF66"]
# 上半：嵌套回旋轨道，半径 ~ sqrt(n)
for n, (c, lw) in enumerate([(cols[0], 2.6), (cols[1], 2.2), (cols[2], 2.2), (cols[3], 1.6)]):
    r = np.sqrt(n + 0.8) * 0.34
    ax.plot(r * np.cos(th), 1.05 + r * np.sin(th), color=c, lw=lw)
ax.annotate("", xy=(0.62, 1.36), xytext=(0.7, 1.15),
            arrowprops=dict(arrowstyle="-|>", color=cols[1], lw=2.2))
# 下半：等间隔能级梯，颜色与轨道一一对应
for n, c in enumerate(cols):
    y = -0.25 - 0.42 * n
    ax.plot([-0.85, 0.15], [y, y], color=c, lw=3.2, solid_capstyle="round")
ax.plot([0.45, 0.45], [-0.25, -1.51], color="#FFFFFF55", lw=1.2)
ax.annotate("", xy=(0.45, -1.51), xytext=(0.45, -0.25),
            arrowprops=dict(arrowstyle="<->", color="#FFFFFF88", lw=1.2))
ax.set_xlim(-1.15, 1.15)
ax.set_ylim(-2.05, 2.1)
ax.set_aspect("equal")
ax.axis("off")
save(fig, "fig_cover.png")


# ---------- 引入：一条谱线 → 三条谱线 ----------
fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.4), facecolor=PAPER)
for ax in axes:
    ax.set_facecolor(PAPER)
ax = axes[0]
ax.vlines(0, 0.15, 0.88, color=INK, lw=8)
ax.annotate("3p → 3s", (0, 0.98), ha="center", fontsize=12, color=INK)
ax.set_xlim(-1, 1)
ax.set_ylim(0, 1.15)
ax.axis("off")
ax.set_title("无磁场：一条谱线", fontsize=12.5, color=INK)
ax = axes[1]
for x0, lab in [(-0.42, "$\\sigma^-$"), (0, "$\\pi$"), (0.42, "$\\sigma^+$")]:
    ax.vlines(x0, 0.15, 0.88, color=OCHRE, lw=8)
    ax.annotate(lab, (x0, 0.02), ha="center", fontsize=11.5, color=GRAY)
ax.annotate("", xy=(0.42, 0.62), xytext=(-0.42, 0.62),
            arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.2))
ax.annotate("等间距", (0, 0.68), ha="center", fontsize=10.5, color=GRAY)
ax.set_xlim(-1, 1)
ax.set_ylim(0, 1.15)
ax.axis("off")
ax.set_title("强磁场：裂成三条", fontsize=12.5, color=OCHRE)
fig.tight_layout()
save(fig, "fig_intro.png")


# ---------- 朗道能级：经典回旋 ↔ 量子阶梯 ----------
fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.6), facecolor=PAPER)
for ax in axes:
    ax.set_facecolor(PAPER)
ax = axes[0]
for gx in np.linspace(-1, 1, 5):
    for gy in np.linspace(-1, 1, 5):
        ax.plot(gx, gy, "x", ms=5, color=GRAY, alpha=0.5, mew=1.2)
ax.plot(0.75 * np.cos(th), 0.75 * np.sin(th), color=TEAL, lw=2.6)
ax.annotate("", xy=(0.53, 0.56), xytext=(0.68, 0.35),
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2.4))
ax.annotate("B 指向纸内", (0, -1.38), ha="center", fontsize=11, color=GRAY)
ax.annotate("回旋频率 $\\omega=|q|B/\\mu c$", (0, 1.28), ha="center",
            fontsize=11.5, color=INK)
ax.set_xlim(-1.4, 1.4)
ax.set_ylim(-1.55, 1.55)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("经典图像：匀速圆周", fontsize=12.5, color=INK)
ax = axes[1]
for n in range(5):
    y = n + 0.5
    c = OCHRE if n == 0 else TEAL
    ax.hlines(y, 0.18, 0.78, color=c, lw=3.2)
    ax.annotate(f"n={n}", (0.82, y), va="center", fontsize=11, color=INK)
ax.annotate("", xy=(0.08, 1.5), xytext=(0.08, 0.5),
            arrowprops=dict(arrowstyle="<->", color=OCHRE, lw=1.6))
ax.annotate("$\\hbar\\omega$", (0.11, 1.0), fontsize=12, color=OCHRE, va="center")
ax.annotate("等间隔", (0.48, 5.05), ha="center", fontsize=11, color=GRAY)
ax.annotate("沿 B 方向自由：$+\\,p_z^2/2\\mu$", (0.48, 5.5), ha="center",
            fontsize=11, color=GRAY)
ax.set_xlim(0, 1.12)
ax.set_ylim(0.1, 5.8)
ax.axis("off")
ax.set_title("量子图像：朗道能级", fontsize=12.5, color=INK)
fig.tight_layout()
save(fig, "fig_landau.png")


# ---------- 正常塞曼效应：3p → 3s 能级分裂与三条谱线 ----------
fig, ax = plt.subplots(figsize=(8.8, 4.8), facecolor=PAPER)
ax.set_facecolor(PAPER)
# 左组：B = 0
ax.hlines(2.0, 0.5, 1.6, color=INK, lw=2.6)
ax.annotate("3p", (0.18, 2.0), va="center", fontsize=11.5, color=INK)
ax.hlines(0.4, 0.5, 1.6, color=INK, lw=2.6)
ax.annotate("3s", (0.18, 0.4), va="center", fontsize=11.5, color=INK)
ax.annotate("", xy=(1.05, 0.52), xytext=(1.05, 1.9),
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.8))
ax.annotate("一条线", (1.05, 0.02), ha="center", fontsize=10.5, color=GRAY)
ax.annotate("$B=0$", (1.05, 2.72), ha="center", fontsize=12.5, color=INK)
# 中组：B ≠ 0 能级分裂
for y, lab in [(2.3, "$m=+1$"), (2.0, "$m=0$"), (1.7, "$m=-1$")]:
    ax.hlines(y, 3.0, 4.2, color=TEAL, lw=2.6)
    ax.annotate(lab, (4.28, y), va="center", fontsize=10.5, color=TEAL)
ax.hlines(0.4, 3.0, 4.2, color=TEAL, lw=2.6)
ax.annotate("$m=0$", (4.28, 0.4), va="center", fontsize=10.5, color=TEAL)
ax.annotate("3p", (2.72, 2.0), va="center", fontsize=11.5, color=INK)
ax.annotate("3s", (2.72, 0.4), va="center", fontsize=11.5, color=INK)
for x0, y0 in [(3.3, 2.3), (3.6, 2.0), (3.9, 1.7)]:
    ax.annotate("", xy=(x0, 0.52), xytext=(x0, y0 - 0.1),
                arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=1.8))
ax.annotate("$B\\neq0$", (3.6, 2.72), ha="center", fontsize=12.5, color=INK)
# 右组：谱线
for x0, lab in [(5.7, "$\\sigma^-$"), (6.15, "$\\pi$"), (6.6, "$\\sigma^+$")]:
    ax.vlines(x0, 0.5, 1.9, color=OCHRE, lw=6)
    ax.annotate(lab, (x0, 0.18), ha="center", fontsize=11, color=GRAY)
ax.annotate("$\\Delta m=0,\\pm1$", (6.15, 2.3), ha="center", fontsize=11, color=GRAY)
ax.annotate("观察到的谱线", (6.15, 2.72), ha="center", fontsize=12.5, color=INK)
ax.set_xlim(0, 7.1)
ax.set_ylim(-0.2, 3.1)
ax.axis("off")
save(fig, "fig_zeeman.png")

print("done: fig_cover.png fig_intro.png fig_landau.png fig_zeeman.png")
