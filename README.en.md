# Quantum Mechanics · Lecture Slides

[中文](README.md) | **English**

Instructor: **Da-Jian Zhang** (Shandong University, China)
Textbook: *A Basic Course in Quantum Mechanics* by Esheng Chen (陈鄂生《量子力学基础教程》)

A complete set of undergraduate quantum mechanics lecture slides: **10 chapters, 58 lectures**, each an independent 16:9 PPT deck. Every lecture follows the same structure: *phenomenon-driven introduction → textbook derivation → case revisit → summary and exercises*.

**Course site (browse online & download)**: https://zhangdajian-sdu.github.io/quantum-mechanics-slides/

- Every lecture can be **flipped through online** — no download needed, with keyboard navigation and touch swipe on mobile
- The corresponding `.pptx` files can also be downloaded directly

## Repository layout

```
slides/
  ch1/   Historical background of quantum mechanics (5 lectures)
  ch2/   Wave function and the Schrödinger equation (5 lectures)
  ch3/   One-dimensional stationary problems (5 lectures)
  ch4/   Observables and operators (9 lectures)
  ch5/   Representations (4 lectures)
  ch6/   Three-dimensional stationary problems (6 lectures)
  ch7/   Approximation methods (8 lectures)
  ch8/   Spin (6 lectures)
  ch9/   Systems of identical particles (4 lectures)
  ch10/  Scattering (6 lectures)
docs/    Source of the GitHub Pages course site and the online slide viewer
```

Each lecture folder contains:

- `chN-sM.pptx` — the slide deck
- `chN-sM.make_figures.py` — script that regenerates every figure in the deck (Python + matplotlib, fully reproducible)

## Usage & license

- The slides can be used for teaching or further editing as-is; all figures can be regenerated or modified with the accompanying scripts.
- All content in this repository is released under **CC BY-SA 4.0**: you may freely share and adapt it, provided that you credit "Da-Jian Zhang (Shandong University)", indicate whether changes were made, and distribute adaptations under the same license. See [LICENSE](LICENSE) for the full text.
- Issues and pull requests are welcome if you spot any mistakes.
