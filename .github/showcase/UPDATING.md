# Updating the README

The repository's root is the live website chefolapp.com (GitHub Pages, Jekyll, from the
root of `main`), and its README presents ChefOl as a whole: the app and its AI proxy,
whose source is private, and this website. Every file at the root becomes a URL on the
site, so everything that serves only the README lives under `.github/`, which Jekyll
skips: the website screenshot in `.github/readme/`, and here in `.github/showcase/` the
other pictures, the scripts that build them and this file. Paths below are relative to
`.github/showcase/`. Every image has one source and one script.

Until 11-22 this lived in a separate repository, `chefol-showcase`; Özcan folded it in
here because Chefol already has a public face, this repository.

| What | Where it comes from | Rebuild |
| --- | --- | --- |
| Page text, English and the Turkish section | `README.md` at the repository root, written by hand | nothing |
| Website screenshot (`.github/readme/desktop.png`) | the live site on a desktop, English, dark theme | shoot it again when the site changes |
| Phone loop at the top (`media/phone.webp`) | the screens in `media/phone.json`, inside a phone frame drawn by the script | `python tools/phone.py` |
| Screens strip (`media/gallery-en.webp`, `media/gallery-tr.webp`) | four screens each, listed in `tools/gallery.py` | `python tools/gallery.py` |
| Health engine and proxy diagrams (`media/diagrams/`) | text and layout in `tools/diagrams.py`, English and Turkish, light and dark | `python tools/diagrams.py` |
| Section numbers (`media/headings/`) | accent colours and count in `media/headings/headings.json` | `python tools/headers.py` |
| Store badges (`media/badges/`) | Apple's and Google's official badges, the same files as on the profile page | nothing |
| Fonts (`media/fonts/`) | IBM Plex, SIL Open Font License (`media/fonts/OFL.txt`) | nothing |

`tools/phone.py` and `tools/headers.py` are the profile repository's scripts
(`OzcanOrhanDemirci/OzcanOrhanDemirci`), pointed at this folder, so the phone and the
headings look the same on both pages.

## The screens

`media/screens/` holds the app's screens at 1080x2400: a profile build of ChefOl 1.0.8
on an Android emulator, guest user, dark theme; files ending in `_TR` are the app in
Turkish (11-22: one recipe generated through the staging proxy, nothing written to the
live project), the others English.
They were re-saved without metadata. To change a screen, put the new one here and
rebuild the phone and the strip. New screens are taken from the app itself, never
mocked up.

Each language section shows the app in its language: the English strip English screens,
the Turkish strip Turkish ones.

## Before pushing

Preview the page through GitHub's renderer, phone and desktop, light and dark:

```sh
python C:/dev/OzcanOrhanDemirci/tools/preview.py C:/Temp/vitrin/showcase/chefol --repo C:/dev/chefol OzcanOrhanDemirci/chefol
```

The phone is where most visitors read it. The page is long: at the phone's 3x scale a
full-page shot passes Chrome's 16384 px limit and the lower part repeats the top, so
shoot the phone at 2x when checking the bottom of the page.

## What never goes in

Every push redeploys the live site: after one, check that chefolapp.com looks as before
and that nothing under `.github/` is served. No URLs of the proxy or any backend, no project or
database IDs, no token or key names or values, no rate-limit or cost numbers, no
known gaps or open bugs, no user or download numbers, no account details, and nothing
from the project's `.claude/`.
Before each push run gitleaks over the history and the tree, and check that images
carry no EXIF or GPS data.

The app's claims stay within the approved wording: "allergy-sensitive", never "safe for
allergies", and no medical claim.
