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


# ---------- 封面：微扰一来，定态不再「定」（teal 底） ----------
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)

# 两条能级
ax.plot([0.10, 0.90], [1.15, 1.15], color="#FAF8F4", lw=2.8, solid_capstyle="round")
ax.plot([0.10, 0.90], [2.30, 2.30], color="#FAF8F4", lw=2.8, solid_capstyle="round")
ax.text(0.92, 1.15, r"$E_k$", color="#FAF8F4", fontsize=14, va="center")
ax.text(0.92, 2.30, r"$E_m$", color="#FAF8F4", fontsize=14, va="center")
ax.text(0.10, 0.96, "粒子原来在这里（定态）", color="#FFFFFF99", fontsize=11.5, va="top")
ax.plot([0.30], [1.15], "o", ms=11, color="#E8B48C", zorder=5)

# 跃迁波浪箭头
t = np.linspace(0, 1, 200)
xw = 0.42 + 0.20 * t
yw = 1.15 + (2.30 - 1.15) * t + 0.045 * np.sin(t * 8 * np.pi)
ax.plot(xw, yw, color="#E8B48C", lw=2.2)
ax.annotate("", xy=(0.63, 2.30), xytext=(xw[-2], yw[-2]),
            arrowprops=dict(arrowstyle="-|>", color="#E8B48C", lw=2.2))
ax.text(0.66, 1.72, r"$|a_m(t)|^2=?$", color="#E8B48C", fontsize=13.5)

# 底部衰减脉冲
xp = np.linspace(0, 1, 200)
yp = 0.28 + 0.34 * np.exp(-3.2 * xp) * (xp >= 0.12)
yp[xp < 0.12] = 0.28
ax.plot([0.12, 0.12], [0.28, 0.62], color="#FFFFFF55", lw=1.6, ls=(0, (4, 3)))
ax.plot(xp, yp, color="#FFFFFF88", lw=2.0)
ax.text(0.50, 0.12, r"外加的含时微扰 $H^{\prime}(t)$", color="#FFFFFF88",
        fontsize=11.5, ha="center")

ax.text(0.5, 2.86, "微扰随时间变化", color="#FAF8F4", fontsize=16.5, ha="center", weight="bold")
ax.text(0.5, 2.62, "定态之间开始「跳槽」", color="#FAF8F4", fontsize=13, ha="center")
ax.set_xlim(0, 1.12); ax.set_ylim(0, 3.05)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- 引入：粒子以一定几率出现在其他定态 ----------
fig, ax = plt.subplots(figsize=(8.4, 5.4), facecolor=PAPER)
ax.set_facecolor(PAPER)

levels = [0.7, 1.5, 2.2, 2.8]
names = [r"$\varphi_1$", r"$\varphi_2$", r"$\varphi_3$", r"$\varphi_4$"]
for y, n in zip(levels, names):
    ax.plot([0.10, 0.55], [y, y], color=INK, lw=2.4, solid_capstyle="round")
    ax.text(0.08, y, n, ha="right", va="center", fontsize=13, color=INK)

# 初态粒子
ax.plot([0.20], [0.7], "o", ms=11, color=TEAL, zorder=5)
ax.text(0.20, 0.44, r"$t<0$：确定地处于 $\varphi_k$", ha="center", fontsize=12, color=TEAL)

# 到各末态的箭头与几率
targets = [(1.5, r"$|a_2(t)|^2$"), (2.2, r"$|a_3(t)|^2$"), (2.8, r"$|a_4(t)|^2$")]
cols = [OCHRE, GRAY, GRAY]
for (y, lb), c in zip(targets, cols):
    ax.annotate("", xy=(0.86, y), xytext=(0.30, 0.78),
                arrowprops=dict(arrowstyle="-|>", color=c, lw=1.8,
                                connectionstyle="arc3,rad=-0.18"))
    ax.plot([0.86], [y], "o", ms=8, color=c, zorder=5)
    ax.text(0.90, y, lb, fontsize=13, color=c, va="center")

ax.text(0.86, 3.06, r"$t\geq0$：加上 $H^{\prime}(t)$", ha="center", fontsize=12.5, color=INK)
ax.set_xlim(0, 1.18); ax.set_ylim(0.2, 3.3)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title("含时微扰不修改能级，而是让粒子在定态之间转移", fontsize=13.5, color=INK, pad=8)
save(fig, "fig_intro.png")


# ---------- 例题：电场脉冲 ε(t) ----------
fig, ax = plt.subplots(figsize=(8.4, 4.6), facecolor=PAPER)
ax.set_facecolor(PAPER)

tau = 2.0
t1 = np.linspace(-2, 0, 50)
t2 = np.linspace(0, 9, 200)
ax.plot(t1, np.zeros_like(t1), color=TEAL, lw=2.6)
ax.plot(t2, np.exp(-t2 / tau), color=TEAL, lw=2.6)
ax.plot([0, 0], [0, 1], color=TEAL, lw=2.6)
ax.plot([0], [1], "o", ms=8, color=OCHRE, zorder=5)
ax.annotate(r"$t=0$ 突然充电到 $\varepsilon_0$（时间常数为 0）",
            xy=(0, 1.0), xytext=(-1.9, 1.13), fontsize=12, color=INK,
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.2))
ax.annotate(r"逐渐放电：$\varepsilon(t)=\varepsilon_0\,e^{-t/\tau}$",
            xy=(3.2, np.exp(-1.6)), xytext=(3.6, 0.62), fontsize=12, color=OCHRE,
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=1.4))
ax.axvline(0, color=HAIR, lw=1.0, zorder=0)
ax.set_xlabel(r"$t$", fontsize=12.5, color=INK)
ax.set_ylabel(r"$\varepsilon(t)$", fontsize=12.5, color=INK)
ax.set_xlim(-2, 9); ax.set_ylim(0, 1.32)
ax.set_yticks([1.0]); ax.set_yticklabels([r"$\varepsilon_0$"])
ax.set_xticks([0]); ax.set_xticklabels(["0"])
ax.tick_params(colors=GRAY, labelsize=11)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(HAIR)
ax.set_title("平板电容器中的电场：先接通、再指数衰减", fontsize=13.5, color=INK, pad=8)
save(fig, "fig_pulse.png")


# ---------- 例题：跃迁几率随放电时间常数 τ 的变化 ----------
fig, ax = plt.subplots(figsize=(8.4, 5.0), facecolor=PAPER)
ax.set_facecolor(PAPER)

x = np.linspace(0, 4.5, 300)
y = x ** 2 / (1 + x ** 2)
ax.plot(x, y, color=TEAL, lw=2.6)
ax.plot([0, 4.5], [1, 1], color=GRAY, lw=1.8, ls=(0, (6, 4)))
ax.text(4.5, 1.03, "饱和值", ha="right", fontsize=11.5, color=GRAY)
ax.annotate(r"$\omega\tau\ll1$：$W\propto\tau^{2}$，" "\n"
            "脉冲太短，来不及跃迁",
            xy=(0.55, 0.55 ** 2 / (1 + 0.55 ** 2)), xytext=(0.7, 0.62),
            fontsize=11.5, color=INK,
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.2))
ax.annotate(r"$\omega\tau\gtrsim1$：趋于饱和",
            xy=(2.6, 2.6 ** 2 / (1 + 2.6 ** 2)), xytext=(2.15, 0.52),
            fontsize=11.5, color=OCHRE,
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=1.4))
ax.set_xlabel(r"$\omega_{mk}\tau=\dfrac{3e^{2}\tau}{8a\hbar}$（无量纲的放电时间）",
              fontsize=12.5, color=INK)
ax.set_ylabel(r"$W_{1s\to2p}$（相对单位）", fontsize=12.5, color=INK)
ax.set_xlim(0, 4.5); ax.set_ylim(0, 1.15)
ax.tick_params(colors=GRAY, labelsize=10)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(HAIR)
ax.set_title("跃迁几率由「放电快慢」与「能级节拍」的比拼决定", fontsize=13.5, color=INK, pad=8)
save(fig, "fig_tau.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
