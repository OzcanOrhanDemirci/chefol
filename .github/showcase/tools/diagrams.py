"""The two diagrams: media/diagrams/<name>-<lang>-<theme>.png

    python tools/diagrams.py

Drawn for a phone first: one column of few boxes, large labels, shown at width 400 so a
720 px drawing lands near 18 px titles and 14 px notes on a 390 px wide phone. Text is
in the tables below, English and Turkish; colours follow the page's accent
(media/headings/headings.json) and GitHub's light and dark surfaces. Transparent
background, so each sits on the page's own colour.
"""
import json
import pathlib

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "media" / "diagrams"
FONTS = ROOT / "media" / "fonts"
W = 720
PAD = 6

ACCENT = json.loads((ROOT / "media" / "headings" / "headings.json").read_text(encoding="utf-8"))["accent"]
THEMES = {
    "light": dict(box="#f6f8fa", line="#d1d9e0", text="#1f2328", muted="#59636e", accent=ACCENT["light"]),
    "dark": dict(box="#151b23", line="#3d444d", text="#e6edf3", muted="#9198a1", accent=ACCENT["dark"]),
}

HEALTH = {
    "en": [
        ("code", "1  Pre-filter", "Ingredients that conflict with the profile are removed before the model sees the request"),
        ("code", "2  Prompt rules", "The profile is written into the model's instructions"),
        ("model", "Language model", "Probabilistic: proposes recipes"),
        ("code", "3  Recipe check", "Every ingredient of the answer is matched against the profile, Turkish suffixes included"),
        ("code", "4  On screen", "Pantry greys out with the reason; warnings on the recipe"),
    ],
    "tr": [
        ("code", "1  Ön filtre", "Profille çakışan malzemeler, istek modele gitmeden çıkarılır"),
        ("code", "2  İstem kuralları", "Profil, modelin talimatlarına yazılır"),
        ("model", "Dil modeli", "Olasılıksal: tarif önerir"),
        ("code", "3  Tarif denetimi", "Yanıttaki her malzeme, Türkçe çekim ekleriyle birlikte profille eşleştirilir"),
        ("code", "4  Ekranda", "Kiler sebebiyle griye döner; tarifte uyarılar"),
    ],
}

PROXY = {
    "en": dict(
        app="ChefOl app", frame="Proxy on Cloudflare Workers",
        boxes=[
            ("Gate", "Firebase sign-in, request shape, per-user rate limit"),
            ("One model per attempt", "A short chain, each model with its own time budget"),
            ("Acceptance check", "The same structural check the app runs"),
        ],
        loop=["not usable:", "next model"], ok="usable", back="Recipe in the app"),
    "tr": dict(
        app="ChefOl uygulaması", frame="Cloudflare Workers üzerinde proxy",
        boxes=[
            ("Kapı", "Firebase oturumu, istek biçimi, kullanıcı başına istek sınırı"),
            ("Her denemede bir model", "Kısa bir zincir, her modelin kendi süresi"),
            ("Kabul denetimi", "Uygulamanın yaptığı yapısal denetimin aynısı"),
        ],
        loop=["kullanılamaz:", "sonraki model"], ok="kullanılabilir", back="Tarif uygulamada"),
}


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


TITLE = font("IBMPlexSans-SemiBold.ttf", 38)
NOTE = font("IBMPlexSans-Regular.ttf", 30)
SMALL = font("IBMPlexSans-Medium.ttf", 27)


def wrap(d, text, f, width):
    lines, cur = [], ""
    for word in text.split():
        t = f"{cur} {word}".strip()
        if d.textlength(t, font=f) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = word
    return lines + [cur]


def box_height(d, title, note, width):
    h = 26 + 48 * len(wrap(d, title, TITLE, width - 56)) - 4
    if note:
        h += 40 * len(wrap(d, note, NOTE, width - 56))
    return h + 22


def draw_box(d, x, y, width, title, note, c, kind="code"):
    h = box_height(d, title, note, width)
    if kind == "model":
        dashed_rect(d, (x, y, x + width, y + h), c["muted"])
    else:
        d.rounded_rectangle((x, y, x + width, y + h), 16, fill=c["box"], outline=c["line"], width=2)
        if kind == "code":
            d.rounded_rectangle((x, y, x + 8, y + h), 4, fill=c["accent"])
    ty = y + 26
    for line in wrap(d, title, TITLE, width - 56):
        d.text((x + 28, ty), line, font=TITLE, fill=c["text"], anchor="la")
        ty += 48
    ty += 2
    for line in wrap(d, note, NOTE, width - 56) if note else []:
        d.text((x + 28, ty), line, font=NOTE, fill=c["muted"], anchor="la")
        ty += 40
    return y + h


def dashed_rect(d, rect, color, dash=14, gap=10, width=2):
    x0, y0, x1, y1 = rect
    for a, b, horiz, fixed in ((x0, x1, True, y0), (x0, x1, True, y1), (y0, y1, False, x0), (y0, y1, False, x1)):
        p = a
        while p < b:
            q = min(p + dash, b)
            d.line(((p, fixed), (q, fixed)) if horiz else ((fixed, p), (fixed, q)), fill=color, width=width)
            p = q + gap


def arrow_down(d, x, y0, y1, color, label=None, c=None):
    d.line(((x, y0), (x, y1 - 12)), fill=color, width=4)
    d.polygon(((x - 11, y1 - 16), (x + 11, y1 - 16), (x, y1)), fill=color)
    if label:
        d.text((x + 20, (y0 + y1) / 2), label, font=SMALL, fill=c["muted"], anchor="lm")


def save(im, name):
    OUT.mkdir(parents=True, exist_ok=True)
    bbox = im.getbbox()
    im = im.crop((0, 0, W, bbox[3] + PAD))
    out = OUT / f"{name}.png"
    im.save(out, optimize=True)
    print(out.relative_to(ROOT), im.size)


def health(lang, theme):
    c = THEMES[theme]
    im = Image.new("RGBA", (W, 2000), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y, x, width = PAD, PAD, W - 2 * PAD
    for i, (kind, title, note) in enumerate(HEALTH[lang]):
        if i:
            arrow_down(d, W // 2, y, y + 46, c["accent"] if kind == "code" or HEALTH[lang][i - 1][0] == "code" else c["muted"])
            y += 46
        y = draw_box(d, x, y, width, title, note, c, kind)
    save(im, f"health-{lang}-{theme}")


def proxy(lang, theme):
    c, t = THEMES[theme], PROXY[lang]
    im = Image.new("RGBA", (W, 2000), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x, y = PAD, PAD
    y = draw_box(d, x, y, W - 2 * PAD, t["app"], None, c, kind="plain")
    arrow_down(d, 200, y, y + 54, c["accent"])
    y += 54

    # The proxy's frame, its name on top, the three steps inside; the loop runs up the right.
    top = y
    loop_w = 236
    inner_x, inner_w = x + 24, W - 2 * PAD - 48 - loop_w
    y += 22
    d.text((inner_x, y), t["frame"], font=SMALL, fill=c["accent"], anchor="la")
    y += 50
    mids = []
    for i, (title, note) in enumerate(t["boxes"]):
        if i:
            arrow_down(d, 200, y, y + 46, c["accent"])
            y += 46
        y0 = y
        y = draw_box(d, inner_x, y, inner_w, title, note, c)
        mids.append((y0 + y) // 2)
    bottom = y + 24
    d.rounded_rectangle((x, top, W - PAD, bottom), 20, outline=c["accent"], width=3)

    # Loop: from the acceptance check's right edge, up to the model box.
    rx = inner_x + inner_w
    lx = rx + 36
    col = c["accent"]
    d.line(((rx, mids[2]), (lx, mids[2])), fill=col, width=4)
    d.line(((lx, mids[2]), (lx, mids[1])), fill=col, width=4)
    d.line(((lx, mids[1]), (rx + 14, mids[1])), fill=col, width=4)
    d.polygon(((rx + 16, mids[1] - 11), (rx + 16, mids[1] + 11), (rx, mids[1])), fill=col)
    ly = (mids[1] + mids[2]) / 2 - 20
    for i, line in enumerate(t["loop"]):
        d.text((lx + 12, ly + i * 36), line, font=SMALL, fill=c["text"], anchor="lm")

    arrow_down(d, 200, bottom, bottom + 64, c["accent"], t["ok"], c)
    y = bottom + 64
    draw_box(d, x, y, W - 2 * PAD, t["back"], None, c, kind="plain")
    save(im, f"proxy-{lang}-{theme}")


def main():
    for lang in ("en", "tr"):
        for theme in THEMES:
            health(lang, theme)
            proxy(lang, theme)


if __name__ == "__main__":
    main()
