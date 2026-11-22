"""The screens strip: media/gallery-<lang>.webp

    python tools/gallery.py

Four of the app's screens side by side, each with rounded corners, on a transparent
background so one file sits on both themes (the screens are the app's dark theme).
The English page shows the English cooking step; the Turkish section shows the Turkish
one, which has a cooking timer.
"""
import pathlib

from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCREENS = ROOT / "media" / "screens"
STRIPS = {
    "en": ["02_pantry_pick_ingredients_dark", "06a_allergies_dark",
           "04a_recipe_generated_overview_dark", "05a_cooking_mode_step_dark"],
    "tr": ["02_pantry_pick_ingredients_dark_TR", "06a_allergies_dark_TR",
           "04a_recipe_generated_overview_dark_TR", "05b_cooking_mode_step_timer_dark_TR"],
}
SW, SH, GAP, RADIUS, SS = 360, 800, 24, 30, 4


def mask():
    m = Image.new("L", (SW * SS, SH * SS), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, SW * SS - 1, SH * SS - 1), RADIUS * SS, fill=255)
    return m.resize((SW, SH), Image.LANCZOS)


def main():
    m = mask()
    for lang, names in STRIPS.items():
        out = Image.new("RGBA", (len(names) * SW + (len(names) - 1) * GAP, SH), (0, 0, 0, 0))
        for i, n in enumerate(names):
            shot = Image.open(SCREENS / f"{n}.png").convert("RGB").resize((SW, SH), Image.LANCZOS)
            out.paste(shot, (i * (SW + GAP), 0), m)
        path = ROOT / "media" / f"gallery-{lang}.webp"
        out.save(path, quality=86, method=6)
        print(path.relative_to(ROOT), out.size, f"{path.stat().st_size / 1e3:.0f} kB")


if __name__ == "__main__":
    main()
