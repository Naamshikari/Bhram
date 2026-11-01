# Ep1 thumbnail — Blender pipeline

1. `python3 tex.py` — makes the scrap textures (colour, torn alpha, edge glow mask).
2. `python scene.py s=160 pct=100 rim=110 pool=20 key=1700 lens=60 ember=1.4 out=render_raw.png`
   — run with a Python that has `pip install bpy` (Blender 5.2 as a module). Renders in Cycles, ~2 min on 4 CPUs.
3. `python3 comp.py render_raw.png "UNKNOWN MAN" ../ep1_thumb4_UNKNOWN_MAN.png` — title, grade, grain.
   Change the second argument to try other titles without re-rendering.

Scripts use /tmp/claude-0/... paths for fonts and textures; edit the paths at the top to run elsewhere.
Fonts: Alfa Slab One (title), Liberation Serif Bold (scrap) — both open licence.
