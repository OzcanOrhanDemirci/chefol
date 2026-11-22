"""ChefOl phone loop: media/phone.webp, built from media/phone.json.

    python tools/phone.py

The app's screens take turns inside a phone frame drawn here: a rounded graphite body
with a faint rim, a thin bezel, a punch-hole camera and two side keys, on a transparent
background. Each screen holds, then dissolves (or slides) into the next; the last one
goes back into the first, so the loop has no seam. Holds are single long frames, so the
file stays small.

phone.json:
  "screens":    paths relative to media/, portrait PNGs of the same size
  "hold":       seconds each screen stands still
  "transition": {"kind": "fade" | "slide", "seconds": 0.45, "fps": 20}
  "width":      output width in px (the page shows it at half that)
  "frame":      body / rim colours, bezel and corner radius in px, camera diameter, buttons
  "quality":    WebP quality
"""
import json
import pathlib

from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIR = ROOT / "media"
SS = 4  # supersampling for the frame's curves


def rounded_mask(size, radius):
    w, h = size
    m = Image.new("L", (w * SS, h * SS), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w * SS - 1, h * SS - 1), radius * SS, fill=255)
    return m.resize(size, Image.LANCZOS)


class Phone:
    def __init__(self, width, screen_aspect, f):
        self.margin = 4 if f.get("buttons", True) else 1  # room for the side keys
        bezel, radius = f["bezel"], f["radius"]
        self.body = (width - 2 * self.margin, 0)
        sw = self.body[0] - 2 * bezel
        sh = round(sw * screen_aspect)
        self.body = (self.body[0], sh + 2 * bezel)
        self.size = (width, self.body[1] + 2 * self.margin)
        self.screen_size = (sw, sh)
        self.screen_at = (self.margin + bezel, self.margin + bezel)
        self.screen_mask = rounded_mask((sw, sh), radius - bezel)

        W, H = self.size[0] * SS, self.size[1] * SS
        m = self.margin * SS
        base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(base)
        if f.get("buttons", True):
            bw = 5 * SS
            x0 = W - m - 2 * SS
            for top, length in ((0.17, 0.085), (0.27, 0.06)):  # volume, then power
                y = round(H * top)
                d.rounded_rectangle((x0, y, x0 + bw, y + round(H * length)), 2 * SS, fill=f["rim"])
        bx0, by0, bx1, by1 = m, m, W - m - 1, H - m - 1
        d.rounded_rectangle((bx0, by0, bx1, by1), radius * SS, fill=f["rim"])
        rim = round(1.6 * SS)
        d.rounded_rectangle((bx0 + rim, by0 + rim, bx1 - rim, by1 - rim), radius * SS - rim, fill=f["body"])
        self.base = base.resize(self.size, Image.LANCZOS)

        cam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(cam)
        r = f["camera"] * SS / 2
        cx = W / 2
        cy = (self.margin + bezel) * SS + 21 * SS
        d.ellipse((cx - r - SS, cy - r - SS, cx + r + SS, cy + r + SS), fill=(40, 44, 50, 255))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(6, 7, 9, 255))
        g = r * 0.32  # a faint lens glint
        d.ellipse((cx - g * 0.4, cy - g * 1.4, cx + g * 0.6, cy - g * 0.4), fill=(70, 80, 110, 160))
        self.camera = cam.resize(self.size, Image.LANCZOS)

    def frame(self, screen):
        out = self.base.copy()
        out.paste(screen, self.screen_at, self.screen_mask)
        return Image.alpha_composite(out, self.camera)


def main():
    r = json.loads((DIR / "phone.json").read_text(encoding="utf-8"))
    shots = [Image.open(DIR / s).convert("RGB") for s in r["screens"]]
    w, h = shots[0].size
    phone = Phone(r["width"], h / w, r["frame"])
    shots = [s.resize(phone.screen_size, Image.LANCZOS) for s in shots]

    t = r["transition"]
    n = max(1, round(t["seconds"] * t["fps"]))
    step = round(1000 / t["fps"])
    frames, durations = [], []
    for i, a in enumerate(shots):
        b = shots[(i + 1) % len(shots)]
        frames.append(phone.frame(a))
        durations.append(round(r["hold"] * 1000))
        for k in range(1, n + 1):
            x = k / (n + 1)
            x = x * x * (3 - 2 * x)  # ease in and out
            if t["kind"] == "slide":
                sw = phone.screen_size[0]
                dx = round(sw * x)
                mix = Image.new("RGB", phone.screen_size)
                mix.paste(a, (-dx, 0))
                mix.paste(b, (sw - dx, 0))
            else:
                mix = Image.blend(a, b, x)
            frames.append(phone.frame(mix))
            durations.append(step)

    out = DIR / r.get("out", "phone.webp")
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=durations, loop=0,
                   quality=r.get("quality", 82), method=6)
    total = sum(durations) / 1000
    print(f"{out.relative_to(ROOT)}  {phone.size[0]}x{phone.size[1]}  {len(frames)} frames  "
          f"{total:.1f} s  {out.stat().st_size / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
