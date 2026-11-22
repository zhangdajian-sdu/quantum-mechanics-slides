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


# ---------- 封面：费米球截面（teal 底，竖版） ----------
fig, ax = plt.subplots(figsize=(6.4, 7.6), facecolor=TEAL)
ax.set_facecolor(TEAL)

R = 3.0
circle = plt.Circle((0, 0), R, fill=False, ec="#FAF8F4", lw=2.2)
ax.add_patch(circle)

# 球内格点（被占据的态）
rng = np.random.default_rng(7)
pts = []
g = 0.42
for ix in np.arange(-R, R + g, g):
    for iy in np.arange(-R, R + g, g):
        if ix ** 2 + iy ** 2 < (R - 0.25) ** 2:
            pts.append((ix + rng.uniform(-0.05, 0.05), iy + rng.uniform(-0.05, 0.05)))
pts = np.array(pts)
ax.plot(pts[:, 0], pts[:, 1], "o", ms=2.6, color="#8FB6C2", alpha=0.85)

# 半径箭头 k_F
ax.annotate("", xy=(R * np.cos(0.42), R * np.sin(0.42)), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color="#E8B48C", lw=2.0))
ax.text(1.28, 1.02, r"$k_F$", color="#E8B48C", fontsize=17)

ax.text(0, -3.85, "球内每个态一个粒子，球外全空", color="#DCE8EC",
        fontsize=12.5, ha="center")
ax.text(0, 3.55, r"$k$ 空间", color="#FAF8F4", fontsize=13, ha="center")

ax.set_xlim(-4.1, 4.1); ax.set_ylim(-4.3, 4.1)
ax.set_xticks([]); ax.set_yticks([])
ax.set_aspect("equal")
for s in ax.spines.values():
    s.set_visible(False)
save(fig, "fig_cover.png")


# ---------- n 空间格点：第一卦限 1/8 球 ----------
fig, ax = plt.subplots(figsize=(4.6, 4.3), facecolor=PAPER)
ax.set_facecolor(PAPER)

N = 7
for i in range(1, N + 1):
    for j in range(1, N + 1):
        inside = i ** 2 + j ** 2 <= 6.2 ** 2
        ax.plot(i, j, "o", ms=5.5, color=TEAL if inside else GRAY,
                alpha=0.95 if inside else 0.45)

th = np.linspace(0, np.pi / 2, 200)
ax.plot(6.2 * np.cos(th), 6.2 * np.sin(th), color=OCHRE, lw=2.2)
ax.text(4.62, 4.35, "能量 ≤ E 的态\n落在 1/8 球内", fontsize=11.5, color=OCHRE,
        ha="center")
ax.text(2.9, 1.6, "每个格点\n× 2 个自旋态", fontsize=11, color=TEAL, ha="center")

ax.set_xlim(0, 8.6); ax.set_ylim(0, 8.0)
ax.set_xlabel(r"$n_x$", fontsize=12, color=INK)
ax.set_ylabel(r"$n_y$", fontsize=12, color=INK)
ax.set_xticks([]); ax.set_yticks([])
ax.set_aspect("equal")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
fig.tight_layout()
save(fig, "fig_lattice.png")


# ---------- 态密度 D(E) 与费米能 ----------
fig, ax = plt.subplots(figsize=(7.8, 3.5), facecolor=PAPER)
ax.set_facecolor(PAPER)

EF = 1.0
E = np.linspace(0, 1.45 * EF, 400)
D = np.sqrt(E / EF)
ax.plot(E / EF, D, color=TEAL, lw=2.6)
ax.fill_between(E / EF, D, where=E <= EF, color=TEAL, alpha=0.22)
ax.axvline(1.0, color=OCHRE, lw=1.6, ls="--")
ax.text(1.015, 1.32, r"$E_F$", color=OCHRE, fontsize=14)
ax.text(0.5, 0.42, r"$N=\int_0^{E_F}D(E)\,\mathrm{d}E$" + "\n阴影面积 = 粒子数",
        fontsize=11.5, color=INK, ha="center")
ax.text(1.22, 0.30, "空着", fontsize=11.5, color=GRAY, ha="center")
ax.text(0.62, 1.06, r"$D(E)\propto\sqrt{E}$", fontsize=12.5, color=TEAL, ha="center")

ax.set_xlim(0, 1.5); ax.set_ylim(0, 1.5)
ax.set_xlabel("E", fontsize=12, color=INK)
ax.set_ylabel("D(E)", fontsize=12, color=INK)
ax.set_xticks([]); ax.set_yticks([])
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
fig.tight_layout()
save(fig, "fig_dos.png")


# ---------- 室温激发：只有 E_F 附近 kT 窗口 ----------
fig, ax = plt.subplots(figsize=(7.8, 3.5), facecolor=PAPER)
ax.set_facecolor(PAPER)

E = np.linspace(0, 1.45 * EF, 400)
D = np.sqrt(E / EF)
ax.plot(E / EF, D, color=TEAL, lw=2.6)
ax.fill_between(E / EF, D, where=E <= EF, color=TEAL, alpha=0.20)

# kT 窗口（夸大宽度以便看清）
w = 0.14
ax.axvspan(1 - w, 1 + w, color=OCHRE, alpha=0.30)
ax.axvline(1.0, color=OCHRE, lw=1.6, ls="--")
ax.text(1.0, 1.36, r"$E_F$", color=OCHRE, fontsize=14, ha="center")
ax.annotate("", xy=(1 + w, 1.22), xytext=(1 - w, 1.22),
            arrowprops=dict(arrowstyle="<->", color=OCHRE, lw=1.4))
ax.text(1.0, 1.26, r"$\sim kT$", color=OCHRE, fontsize=11.5, ha="center")

ax.text(0.42, 0.40, "深处的电子：\n上面全被占着，无处可去", fontsize=11.5,
        color=INK, ha="center")
ax.text(1.28, 0.42, "只有窗口内的电子\n能被热激发", fontsize=11.5, color=OCHRE,
        ha="center")

ax.set_xlim(0, 1.5); ax.set_ylim(0, 1.5)
ax.set_xlabel("E", fontsize=12, color=INK)
ax.set_ylabel("D(E)", fontsize=12, color=INK)
ax.set_xticks([]); ax.set_yticks([])
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
fig.tight_layout()
save(fig, "fig_heat.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
