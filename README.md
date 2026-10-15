# Dmytro Tarasenko — portfolio

Static, bilingual portfolio for GitHub Pages: [wolfs0ng.github.io](https://wolfs0ng.github.io).

The site includes a personal overview, selected game projects, a Carnage Club project page, and a public game guide in Ukrainian and English. The generated pages work without a framework or a backend. Guide text and navigation are readable without JavaScript; JavaScript adds search, language preferences, and image previews.

## Edit and preview

- `scripts/build.py` contains the portfolio layouts and bilingual copy.
- `content/guide.json` contains the editorially curated public guide.
- `content/media.json` records external publisher screenshots, store links, and video sources.
- `styles.css` and `assets/js/` contain the shared appearance and interactions.

Rebuild generated pages with Python **3.12+** (standard library only):

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8765 --bind 127.0.0.1
```

Open `http://127.0.0.1:8765/`. The checked-in HTML is the deployable site; GitHub Pages needs no build installation. `.nojekyll` keeps delivery static.

## Public guide scope

The game repository is private. This site contains a standalone public adaptation of the current README and Wiki, not a mirror of the internal documentation. The public guide explains the game, combat, development of a character, equipment, adaptive opponents, exploration, and atmosphere.

Excluded: serialized configuration, balance tables, code and private-source links, testing material, agent notes, walkthroughs, full dialogue scripts, quest solutions, endings, narrative drafts, and unreleased design promises. Updating the guide is an editorial step; do not automatically copy the private Wiki into this repository.

The original Unity project and its documentation are not modified by this website.

## Media

Carnage Club screenshots were supplied by the author. WebP derivatives retain the original composition; smaller versions load in galleries, while full versions open on selection.

Commercial game images load directly from the public App Store media CDN. Video links lead to the official Smart Project, Murka, and Jutiful channels. These materials belong to their respective owners and may show versions released after the developer's involvement.

- [Kitty Sort — App Store](https://apps.apple.com/us/app/kitty-sort-twisted-tails/id6504183751) · [Google Play video source](https://play.google.com/store/apps/details?id=org.smapps.sort)
- [Scatter Slots — App Store](https://apps.apple.com/us/app/scatter-slots-slot-machines/id944158857) · [Official trailer](https://www.youtube.com/watch?v=_0tD6613Cs8)
- [AZZL — App Store](https://apps.apple.com/us/app/azzl/id640484311) · [Official launch trailer](https://www.youtube.com/watch?v=zwV3EBCQ7aU)

## Publishing

Push the reviewed files through the repository's existing GitHub Pages publishing flow. Previewing or rebuilding locally does not publish the changes.

## Brand assets

The approved personal identity is the circular Wolfsong emblem. `assets/images/branding/wolfsong-master.png` preserves the selected original; optimized derivatives supply the header, favicon, and touch icon. The supplied Mad Hydra Production logo appears inside the Carnage Club studio section.

Readability uses 18px body copy, 16px navigation and links, and a 14px minimum for supporting labels. Large heading sizes remain unchanged.
