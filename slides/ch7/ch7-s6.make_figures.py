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


def wavy(ax, x0, x1, y, color, lw=1.8, n=6, amp=0.035, vertical=False):
    t = np.linspace(0, 1, 300)
    if vertical:
        xs = x0 + amp * np.sin(t * n * 2 * np.pi)
        ys = y[0] + t * (y[1] - y[0])
        ax.plot(xs, ys, color=color, lw=lw)
    else:
        xs = x0 + t * (x1 - x0)
        ys = y + amp * np.sin(t * n * 2 * np.pi)
        ax.plot(xs, ys, color=color, lw=lw)


# ---------- 封面：调到共振，只有 ω = ω_mk 的跃迁留下来（teal 底） ----------
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)

x = np.linspace(-1, 1, 400)
for g, a in [(2.0, 0.35), (5.0, 0.6), (14.0, 1.0)]:
    y = np.sin(x * g * 3) ** 2 / (np.pi * (x * 3) ** 2 * g + 1e-12)
    y = y / y.max()
    ax.plot(x, y * 0.9 + 1.15, color="#FAF8F4", lw=1.4, alpha=a)
ax.annotate("", xy=(0.0, 2.5), xytext=(0.35, 1.6),
            arrowprops=dict(arrowstyle="-|>", color="#E8B48C", lw=1.8))
ax.text(0.08, 2.3, "峰只立在 ω = ω_mk 处", color="#E8B48C", fontsize=12)
ax.text(0.0, 0.78, "共振：光的频率对上能级间隔", color="#FFFFFF99", fontsize=11.5, ha="center")

# 底部：吸收（向上）与发射（向下）
ax.plot([0.06, 0.44], [0.42, 0.42], color="#FAF8F4", lw=2.4, solid_capstyle="round")
ax.plot([0.06, 0.44], [0.12, 0.12], color="#FAF8F4", lw=2.4, solid_capstyle="round")
ax.annotate("", xy=(0.25, 0.40), xytext=(0.25, 0.14),
            arrowprops=dict(arrowstyle="-|>", color="#E8B48C", lw=2.0))
ax.text(0.30, 0.27, "吸收 $\\hbar\\omega$", color="#E8B48C", fontsize=10.5, va="center")

ax.plot([0.56, 0.94], [0.42, 0.42], color="#FAF8F4", lw=2.4, solid_capstyle="round")
ax.plot([0.56, 0.94], [0.12, 0.12], color="#FAF8F4", lw=2.4, solid_capstyle="round")
ax.annotate("", xy=(0.75, 0.14), xytext=(0.75, 0.40),
            arrowprops=dict(arrowstyle="-|>", color="#E8B48C", lw=2.0))
ax.text(0.80, 0.27, "发射 $\\hbar\\omega$", color="#E8B48C", fontsize=10.5, va="center")
ax.set_ylim(-0.05, 2.75)

ax.text(0.5, 2.59, "周期微扰 + 足够长时间", color="#FAF8F4", fontsize=16.5, ha="center", weight="bold")
ax.text(0.5, 2.93, "只有「共振」的跃迁留下来", color="#FAF8F4", fontsize=12.5, ha="center")
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- 跃迁几率随光频率的分布：共振峰 ----------
fig, ax = plt.subplots(figsize=(8.4, 5.2), facecolor=PAPER)
ax.set_facecolor(PAPER)

x = np.linspace(0, 3, 1500)
for tt, c, lb in [(6 * np.pi, "#5B7B8A", "t 较大"), (20 * np.pi, TEAL, "t 很大")]:
    d = x - 1.0
    y = np.sin(d * tt / 2) ** 2 / (np.pi * d ** 2 * tt / 2 + 1e-300)
    ax.plot(x, y, color=c, lw=2.0 if tt > 10 * np.pi else 1.6, label=lb)
ax.set_xlabel(r"光的角频率 $\omega$（单位：$\omega_{mk}$）", fontsize=12.5, color=INK)
ax.set_ylabel(r"跃迁几率 $W_{k\to m}$", fontsize=12.5, color=INK)
ax.set_xlim(0, 3); ax.set_ylim(0, 11)
ax.set_xticks([1.0]); ax.set_xticklabels([r"$\omega_{mk}$"], fontsize=12)
ax.set_yticks([])
ax.tick_params(colors=GRAY, labelsize=10)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(HAIR)
ax.annotate("共振条件：$\\omega=\\omega_{mk}$\n即 $E_m=E_k+\\hbar\\omega$", xy=(1.0, 9.8), xytext=(1.6, 9.6),
            fontsize=12.5, color=OCHRE,
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=1.4))
ax.annotate("峰宽 ∝ 1/t：\n时间越长，对频率越挑剔",
            xy=(0.86, 4.6), xytext=(0.18, 6.4), fontsize=11.5, color=INK,
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.2))
ax.legend(frameon=False, fontsize=11.5, loc="upper right")
ax.set_title("跃迁几率集中在 $\\omega\\approx\\omega_{mk}$ 附近——这就是「共振」", fontsize=13.5, color=INK, pad=8)
save(fig, "fig_detune.png")


# ---------- 共振吸收与共振发射 ----------
fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.6), facecolor=PAPER)
fig.subplots_adjust(wspace=0.35)

for ax, title, up in [(axes[0], "共振吸收：$E_m=E_k+\\hbar\\omega$", True),
                      (axes[1], "共振发射：$E_m=E_k-\\hbar\\omega$", False)]:
    ax.set_facecolor(PAPER)
    ylo, yhi = 0.16, 0.74
    ax.plot([0.18, 0.82], [ylo, ylo], color=TEAL, lw=3.0, solid_capstyle="round")
    ax.plot([0.18, 0.82], [yhi, yhi], color=TEAL, lw=3.0, solid_capstyle="round")
    if up:
        ax.annotate("", xy=(0.42, yhi - 0.02), xytext=(0.42, ylo + 0.02),
                    arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=2.4))
        wavy(ax, 0.02, 0.36, 0.45, GRAY, lw=1.6)
        ax.text(0.02, 0.53, "光子 $\\hbar\\omega$ 进来", fontsize=10.5, color=GRAY)
        ax.text(0.86, ylo - 0.015, "$E_k$", fontsize=12.5, color=INK, va="center")
        ax.text(0.86, yhi - 0.015, "$E_m$", fontsize=12.5, color=INK, va="center")
        ax.text(0.5, 0.02, "低能态 → 高能态，吸收一个光子", fontsize=11, color=INK, ha="center")
    else:
        ax.annotate("", xy=(0.58, ylo + 0.02), xytext=(0.58, yhi - 0.02),
                    arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=2.4))
        wavy(ax, 0.64, 0.98, 0.45, GRAY, lw=1.6)
        ax.text(0.60, 0.53, "光子 $\\hbar\\omega$ 出去", fontsize=10.5, color=GRAY)
        ax.text(0.86, ylo - 0.015, "$E_m$", fontsize=12.5, color=INK, va="center")
        ax.text(0.86, yhi - 0.015, "$E_k$", fontsize=12.5, color=INK, va="center")
        ax.text(0.5, 0.02, "高能态 → 低能态，发射一个光子", fontsize=11, color=INK, ha="center")
    ax.set_xlim(0, 1.25); ax.set_ylim(-0.08, 1.0)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(title, fontsize=13, color=INK, pad=8)

fig.suptitle("式 (16)：$|F_{mk}|^2=|F_{km}|^2$ ——同一对能态之间，吸收与发射的速率相等",
             fontsize=12.5, color=OCHRE, y=0.02)
save(fig, "fig_levels.png")


# ---------- λ ≫ a：电偶极近似 ----------
fig, ax = plt.subplots(figsize=(8.4, 4.6), facecolor=PAPER)
ax.set_facecolor(PAPER)

z = np.linspace(0, 10, 800)
ax.plot(z, np.sin(2 * np.pi * z / 4.0), color=TEAL, lw=2.0)
ax.axhline(0, color=HAIR, lw=1.0)
# λ 标注
ax.annotate("", xy=(4.0, 1.35), xytext=(0.0, 1.35),
            arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=1.4))
ax.text(2.0, 1.48, "波长 $\\lambda\\approx10^{-4}\\,$cm（可见光）", fontsize=12, color=INK, ha="center")
# 原子：原点处的小圆
atom = plt.Circle((1.0, 0.0), 0.12, facecolor="#C4622D33", edgecolor=OCHRE, lw=1.6)
ax.add_patch(atom)
ax.annotate("原子半径 $a\\approx10^{-8}\\,$cm\n$\\lambda/a\\sim10^{4}$", xy=(1.0, -0.12), xytext=(3.2, -1.15),
            fontsize=12, color=OCHRE,
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=1.3))
ax.text(6.6, 0.75, "在原子范围内，电场几乎不随位置变：\n$\\varepsilon_x(z,t)\\approx\\varepsilon_0\\cos\\omega t$\n——电偶极近似",
        fontsize=12, color=INK,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#F3F1EA", edgecolor=HAIR))
ax.set_xlim(-0.3, 10.3); ax.set_ylim(-1.7, 1.9)
ax.set_aspect("equal", adjustable="box")
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title("为什么可以只取展开式的第一项（式 20–21）", fontsize=13.5, color=INK, pad=8)
save(fig, "fig_dipole.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
