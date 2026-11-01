# Ep1 thumbnail v5 (fern UNABOMBER layout)

1. `python man.py s=128 pct=200 red=420 warm=130 fill=0.6 top=25 out=man_full.png`
   (Python with `pip install bpy`) renders the man: 1940s fedora and coat, backlit, face in shadow, transparent background.
2. `MANSCALE=1.1 MANDY=225 MANDX=50 python3 make.py "UNKNOWN MAN" out.png` composites:
   pencil code page (left), dark side with faint handwriting (right), glowing red rip, the man, title, grade and grain.
Paths inside point at /tmp/claude-0; edit them to run elsewhere.
