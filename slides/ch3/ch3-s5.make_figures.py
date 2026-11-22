"""§3.5 δ函数势 — figures for the slide deck."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot

import numpy as np
import matplotlib.pyplot as plt

setup_plot()

OUT = Path(__file__).parent / "media"
OUT.mkdir(exist_ok=True)

PAPER = "#FFFFFF"
INK = "#20242B"
TEAL = "#1F4E5F"
OCHRE = "#C4622D"
GRAY = "#8A8F98"
HAIR = "#E2DFD8"
PANEL = "#F3F1EA"


def style_ax(ax):
    ax.set_facecolor(PAPER)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRAY)
    ax.tick_params(colors=GRAY, labelsize=8)
    ax.grid(False)


def save(fig, name):
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight", facecolor=PAPER)
    plt.close(fig)


# ---------------------------------------------------------------- fig_cover
# vertical cover art: three delta-spike + cusp-wave panels
fig, ax = plt.subplots(figsize=(4.2, 7.5))
ax.set_xlim(0, 1)
ax.set_ylim(0, 3)
ax.axis("off")
fig.patch.set_facecolor(PAPER)

x = np.linspace(-1, 1, 1200)
bands = [("#1F4E5F", 2.55, 1.0), ("#C4622D", 1.55, 0.75), ("#8A8F98", 0.55, 0.5)]
for color, y0, alpha in bands:
    psi = np.exp(-np.abs(x) / 0.28)
    ax.plot((x + 1) / 2, y0 + 0.22 * psi, color=color, lw=1.8, alpha=min(alpha + 0.2, 1.0))
    ax.axhline(y0, color=color, lw=0.6, ls=(0, (4, 4)), alpha=0.4)
    # delta spike at center
    ax.annotate("", xy=(0.5, y0 - 0.34), xytext=(0.5, y0 - 0.02),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2.2, alpha=min(alpha + 0.2, 1.0)))
save(fig, "fig_cover.png")

# ------------------------------------------------------------- fig_delta
# delta function as the limit of narrowing rectangles
fig, ax = plt.subplots(figsize=(6.2, 3.6))
style_ax(ax)
for w, h, color, lw in [(0.8, 1 / 0.8, "#8A8F98", 1.4), (0.3, 1 / 0.3, "#C4622D", 1.6), (0.1, 10.0, TEAL, 2.0)]:
    ax.add_patch(plt.Rectangle((-w / 2, 0), w, h, fill=False, ec=color, lw=lw))
ax.annotate("", xy=(0, 11.6), xytext=(0, 10.2),
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2.0))
ax.text(0.16, 11.0, r"$\delta(x)$", fontsize=13, color=TEAL)
ax.text(0.75, 8.6, r"宽度 $\to 0$" + "\n" + r"高度 $\to \infty$" + "\n面积恒为 1", fontsize=9.5, color=GRAY, ha="left")
ax.set_xlim(-1.3, 1.6)
ax.set_ylim(0, 12.6)
ax.set_xticks([-1, -0.5, 0, 0.5, 1])
ax.set_yticks([])
ax.set_xlabel("$x$", fontsize=9.5, color=INK)
save(fig, "fig_delta.png")

# ------------------------------------------------------- fig_well_wave
# delta well: downward spike + cusp bound state
fig, ax = plt.subplots(figsize=(6.6, 3.8))
style_ax(ax)
x = np.linspace(-3, 3, 1600)
alpha = 1.4
psi = np.sqrt(alpha) * np.exp(-alpha * np.abs(x))
ax.plot(x, psi, color=TEAL, lw=2.2, label=r"$\psi(x)=\sqrt{\alpha}\,\mathrm{e}^{-\alpha|x|}$")
ax.fill_between(x, 0, psi, color=TEAL, alpha=0.10)
# delta well spike (downward) at x=0
ax.annotate("", xy=(0, -1.05), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=OCHRE, lw=2.4))
ax.text(0.12, -0.98, r"$V(x)=-\gamma\,\delta(x)$", fontsize=10.5, color=OCHRE)
# annotate cusp
ax.annotate("尖点：$\\psi'$ 跳变", xy=(0, np.sqrt(alpha)), xytext=(1.15, 1.42),
            fontsize=9.5, color=GRAY,
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.9))
ax.text(-2.8, 1.62, r"束缚态 $\ E=-\dfrac{\mu\gamma^{2}}{2\hbar^{2}}$", fontsize=11, color=TEAL)
ax.axhline(0, color=GRAY, lw=0.8)
ax.set_xlim(-3, 3)
ax.set_ylim(-1.25, 1.85)
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel("$x$", fontsize=9.5, color=INK)
save(fig, "fig_well_wave.png")

# -------------------------------------------------------- fig_delta_T
# transmission through a delta barrier: T(E) = 1/(1+E0/E)
fig, ax = plt.subplots(figsize=(6.4, 3.6))
style_ax(ax)
E = np.linspace(0.02, 8, 800)
E0 = 1.0
T = 1.0 / (1.0 + E0 / E)
R = 1.0 - T
ax.plot(E, T, color=TEAL, lw=2.2, label=r"$T$")
ax.plot(E, R, color=OCHRE, lw=1.8, ls="--", label=r"$R$")
ax.axvline(E0, color=GRAY, lw=0.9, ls=":")
ax.text(E0 + 0.12, 0.08, r"$E=E_{0}\equiv\mu\gamma^{2}/2\hbar^{2}$", fontsize=9, color=GRAY)
ax.plot([E0], [0.5], "o", ms=6, mfc="none", mec=INK, mew=1.4)
ax.text(E0 + 0.12, 0.56, r"$T=R=\frac{1}{2}$", fontsize=9.5, color=INK)
ax.text(5.4, 0.62, "$E\\to 0$：全反射\n$E\\to\\infty$：全透射", fontsize=9.5, color=GRAY)
ax.set_xlim(0, 8)
ax.set_ylim(0, 1.05)
ax.set_xlabel("$E$（以 $E_{0}$ 为单位）", fontsize=9.5, color=INK)
ax.set_ylabel("$T,\\ R$", fontsize=10, color=INK)
ax.legend(fontsize=9, frameon=False, loc="lower right")
save(fig, "fig_delta_T.png")

# -------------------------------------------------------- fig_limit
# intro page: rectangular barrier squeezed to zero width, V0*a = gamma fixed
fig, ax = plt.subplots(figsize=(6.4, 3.8))
style_ax(ax)
gamma = 1.0
for a, color, lw in [(1.0, GRAY, 1.4), (0.4, OCHRE, 1.7), (0.14, TEAL, 2.0)]:
    v0 = gamma / a
    ax.add_patch(plt.Rectangle((-a / 2, 0), a, v0, fill=False, ec=color, lw=lw))
ax.annotate("", xy=(0, 8.4), xytext=(0, 7.3),
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2.2))
ax.text(0.16, 7.9, r"$V(x)=\gamma\,\delta(x)$", fontsize=12, color=TEAL)
ax.text(0.62, 5.1, r"$a\to 0,\ V_{0}\to\infty$" + "\n" + r"$V_{0}a=\gamma$ 固定", fontsize=10, color=GRAY, ha="left")
ax.text(0, 0.14, r"$a$", fontsize=10, color=GRAY, ha="center")
ax.text(-0.60, 0.42, r"$V_{0}$", fontsize=10, color=GRAY, ha="right")
ax.set_xlim(-1.3, 1.75)
ax.set_ylim(0, 9.2)
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel("$x$", fontsize=9.5, color=INK)
ax.set_ylabel("$V(x)$", fontsize=10, color=INK)
save(fig, "fig_limit.png")

print("done:", sorted(p.name for p in OUT.glob("*.png")))
# -------------------------------------------------------- fig_delta_pm
# page 3: negative vs positive delta potential side by side
fig, axes = plt.subplots(1, 2, figsize=(6.4, 3.3))
for ax, sign, color, title, sub in [
    (axes[0], -1, TEAL, r"$\delta$ 势阱（吸引）", "束缚态问题 $E<0$"),
    (axes[1], +1, OCHRE, r"$\delta$ 势垒（排斥）", "散射问题 $E>0$"),
]:
    style_ax(ax)
    y0, y1 = (-1.15, 0) if sign < 0 else (1.15, 0)
    ax.annotate("", xy=(0, y0), xytext=(0, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2.6))
    ax.text(0.14, y0 + (0.10 if sign < 0 else -0.28),
            r"$V(x)=-\gamma\,\delta(x)$" if sign < 0 else r"$V(x)=+\gamma\,\delta(x)$",
            fontsize=11, color=color)
    ax.axhline(0, color=GRAY, lw=0.9)
    ax.set_title(title, fontsize=12, color=INK, pad=8)
    ax.text(-1.3, 1.26, sub, fontsize=10.5, color=GRAY, ha="left")
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.5, 1.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("$x$", fontsize=9.5, color=INK)
fig.subplots_adjust(wspace=0.25)
save(fig, "fig_delta_pm.png")

# ------------------------------------------------------ fig_gamma_wave
# page 7: bound-state wavefunction for increasing gamma (alpha = mu*gamma/hbar^2)
fig, ax = plt.subplots(figsize=(6.2, 3.5))
style_ax(ax)
x = np.linspace(-3, 3, 1600)
for alpha, color, lw, lab in [(0.55, GRAY, 1.6, r"$\gamma$ 小"),
                              (1.2, OCHRE, 1.9, r"$\gamma$ 中"),
                              (2.4, TEAL, 2.2, r"$\gamma$ 大")]:
    psi = np.sqrt(alpha) * np.exp(-alpha * np.abs(x))
    ax.plot(x, psi, color=color, lw=lw, label=lab)
ax.axhline(0, color=GRAY, lw=0.8)
ax.text(-2.9, 2.35, r"$\psi=\sqrt{\alpha}\,\mathrm{e}^{-\alpha|x|}$，$\alpha=\mu\gamma/\hbar^{2}$",
        fontsize=10.5, color=INK)
ax.text(-2.9, 2.02, r"$|E|\propto\gamma^{2}$ 更深，宽度 $1/\alpha\propto1/\gamma$ 更窄",
        fontsize=9.5, color=GRAY)
ax.legend(fontsize=9.5, frameon=False, loc="upper right")
ax.set_xlim(-3, 3)
ax.set_ylim(0, 2.6)
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel("$x$", fontsize=9.5, color=INK)
save(fig, "fig_gamma_wave.png")

# ------------------------------------------------------------- fig_kp
# page 11 (extra): periodic delta array -> energy bands
# Kronig–Penney dispersion for a repulsive delta array:
#   cos(ka) = cos(u) + P·sin(u)/u,  u = αa = √(2μE)·a/ℏ,  P = μγa/ℏ²
P = 10.0
u = np.linspace(1e-3, 3 * np.pi, 9000)
rhs = np.cos(u) + P * np.sin(u) / u
allowed = np.abs(rhs) <= 1.0
segs = []                      # allowed-band index segments in u
i = 0
while i < len(u):
    if allowed[i]:
        j = i
        while j < len(u) and allowed[j]:
            j += 1
        segs.append((i, j - 1))
        i = j
    else:
        i += 1
eps = (u / np.pi) ** 2         # E in units of π²ℏ²/(2μa²)
ka = np.arccos(np.clip(rhs, -1.0, 1.0))

fig, axes = plt.subplots(1, 2, figsize=(6.4, 3.3), gridspec_kw={"width_ratios": [1.15, 1]})
ax = axes[0]
style_ax(ax)
for n in range(-2, 3):
    ax.annotate("", xy=(n, 1.05), xytext=(n, 0),
                arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.8))
ax.axhline(0, color=GRAY, lw=0.9)
ax.set_title(r"周期排列：$V(x)=\gamma\sum_{n}\delta(x-na)$", fontsize=10.5, color=INK, pad=8)
ax.text(0, -0.42, "Kronig–Penney 模型（1931）", fontsize=9.5, color=GRAY, ha="center")
ax.set_xlim(-2.7, 2.7)
ax.set_ylim(-0.6, 1.35)
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel("$x$", fontsize=9.5, color=INK)
ax = axes[1]
style_ax(ax)
for i0, i1 in segs:
    kb, eb = ka[i0:i1 + 1], eps[i0:i1 + 1]
    ax.plot(np.concatenate([-kb[::-1], kb]), np.concatenate([eb[::-1], eb]),
            color=TEAL, lw=2.0, solid_capstyle="round")
for (l0, l1), (r0, r1) in zip(segs[:-1], segs[1:]):
    ax.axhspan(eps[l1], eps[r0], color=OCHRE, alpha=0.16)
gap1_mid = (eps[segs[0][1]] + eps[segs[1][0]]) / 2
ax.text(0, gap1_mid, "禁带", fontsize=9.5, color=OCHRE, ha="center", va="center")
band1_mid = (eps[segs[0][0]] + eps[segs[0][1]]) / 2
ax.text(0, band1_mid, "允带", fontsize=9.5, color=TEAL, ha="center", va="center")
ax.set_title(r"$E(k)$：允带与禁带（数值计算，$P=\mu\gamma a/\hbar^{2}=10$）", fontsize=10, color=INK, pad=8)
ax.set_xlim(-np.pi, np.pi)
ax.set_ylim(0, 9.6)
ax.set_xticks([-np.pi, 0, np.pi])
ax.set_xticklabels([r"$-\pi/a$", "0", r"$\pi/a$"], fontsize=8.5)
ax.set_yticks([])
ax.set_xlabel("$k$", fontsize=9.5, color=INK)
ax.set_ylabel("$E$（以 $\\pi^{2}\\hbar^{2}/2\\mu a^{2}$ 为单位）", fontsize=9, color=INK)
fig.subplots_adjust(wspace=0.22)
save(fig, "fig_kp.png")

print("new figures done")
