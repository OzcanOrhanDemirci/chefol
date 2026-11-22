"""Section numbers for the headings: media/headings/n<NN>-<light|dark>.png

    python tools/headers.py

The headings themselves are GitHub's own text (they stay sharp and readable on a phone);
in front of each sits its number in IBM Plex Mono in the accent colour, an image so it
can carry the colour. The accent for each theme is in media/headings/headings.json.
Drawn at 2x, shown at height 22.
"""
import json
import pathlib

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIR = ROOT / "media" / "headings"
FONT = ROOT / "media" / "fonts" / "IBMPlexMono-Medium.ttf"


def hex_rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def main() -> None:
    cfg = json.loads((DIR / "headings.json").read_text(encoding="utf-8"))
    font = ImageFont.truetype(str(FONT), 44)
    for n in range(1, cfg["count"] + 1):
        s = f"{n:02d}"
        w = int(ImageDraw.Draw(Image.new("RGBA", (1, 1))).textlength(s, font=font)) + 2
        for theme in ("light", "dark"):
            im = Image.new("RGBA", (w, 48), (0, 0, 0, 0))
            ImageDraw.Draw(im).text((0, 40), s, font=font, fill=hex_rgb(cfg["accent"][theme]), anchor="ls")
            out = DIR / f"n{s}-{theme}.png"
            im.save(out, optimize=True)
            print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
