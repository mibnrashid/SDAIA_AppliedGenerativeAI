# Applied Generative AI — SDAIA Academy

The course site for **Applied Generative AI**, delivered at SDAIA Academy,
Riyadh, **Sunday 2 – Thursday 6 August 2026**. Instructor: **Musa Ibn Rashid**.

It is for the people in the room: five HTML slide decks, six Colab notebooks,
five scored browser activities, a pre/post test, and the project brief with its
rubric. Students keep the link afterwards.

Everything here is plain HTML, CSS and vanilla JavaScript. **No build step, no
npm, no framework, and nothing loads from the network** — every page works with
the venue wifi off. That is a deliberate constraint, not an accident.

---

## Run it locally

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000/>.

Use a server rather than opening the files directly: `notebooks/index.html`
reads `notebooks.json` with `fetch()`, which every browser blocks on `file://`.
Everything else works either way.

---

## Deploy to GitHub Pages

1. Push this folder to a GitHub repository.
2. **Settings → Pages → Build and deployment → Deploy from a branch**.
3. Branch `main`, folder `/ (root)`. Save.
4. Wait a minute, then open `https://<account>.github.io/<repo-name>/`.

**Keep `.nojekyll`.** Without it GitHub Pages runs Jekyll over the site, which
can mangle files and silently drop anything beginning with an underscore.

Every path in this repository is relative (`../assets/theme.css`, never
`/assets/theme.css`), because a project site is served from `/<repo-name>/` and
an absolute path 404s there. `python qa.py` checks this.

---

## Structure

```
index.html          course home: hero, five day cards, progress strip
assets/             theme tokens, shared CSS, the deck engine, logos
  theme.css           design tokens only — colours, type, spacing
  site.css            shared page chrome: header, footer, buttons, links
  deck.css/.js        the slide engine: keys, dots, notes, print-to-PDF
  activity.css        shared chrome for the activities
  store.js            the only file that touches localStorage (agai: prefix)
  activities.js       the activity registry — ids and maximum scores
  tokenize.js         the approximate tokenizer used by two activities
slides/             one deck per day, day1.html … day5.html
activities/         the five scored browser activities plus their hub
assessment/         pre-test and post-test, sharing questions.js
project/            the brief, the rubric, the README template
notebooks/          six .ipynb files, build.py that generates them, verify.py
  data/               the document set for Notebook 2, plus build_corpus.py
qa.py               site-wide checks — run before every deploy
CHECKLIST.md        what to do each morning, and how each day runs
```

---

## For me, later

### Add a slide

Open the day's file in `slides/` and add a `<section class="slide">` in the
right place. The engine picks it up automatically — the dot strip, the counter
and the deep links all recount on load.

Layout classes: `.slide--title`, `.slide--section` (dark divider),
`.slide--split` (two columns, wrap them in `.slide__cols`), `.slide--code`
(code plus a caption column), `.slide--full` (one big statement, add
`.slide--dark` for a dark one).

Put an `<aside class="notes">` inside every content slide. Write two to four
complete sentences you can read aloud verbatim at nine in the morning without
having to interpret anything. Notes that only restate the slide title are worse
than no notes.

The canvas is a fixed 1280×720 box, so you can size things in pixels against
it. If a slide overflows, it will be clipped rather than scrolled — check it
before you teach it.

### Add an activity

1. Add an entry to `assets/activities.js`: `id`, `num`, `day`, `minutes`,
   `max`, `file`, `title`, `desc`. **This registry is the single source of
   truth** — the home page progress strip and the activities hub both read it,
   so they cannot drift apart.
2. Copy an existing activity page as a starting point. Keep the header, the
   `.scorestrip`, and the "back to all activities" link.
3. Call `Store.saveScore('<your-id>', score, max)` when it finishes, using
   exactly the id from the registry.
4. Run `python qa.py` — it checks the id matches, that `MAX` agrees with the
   registry, and that the totals add up.

### Fill in the Colab URLs

Upload each notebook to Colab, then **File → Share → anyone with the link →
Viewer**, and paste the URL into the matching `colab_url` field in
`notebooks/notebooks.json`. Nothing in the HTML needs editing —
`notebooks/index.html` reads that file at load time. Rows with an empty
`colab_url` show a greyed-out badge and still offer the `.ipynb` download.

### Regenerate the notebooks

The `.ipynb` files are generated, not hand-edited:

```bash
python notebooks/build.py      # rebuild all six from build.py
python notebooks/verify.py     # eight checks: JSON, syntax, imports, keys, TODOs
python notebooks/data/build_corpus.py   # regenerate the Notebook 2 document set
```

Edit `notebooks/build.py`, never the `.ipynb` directly — one missing comma in
hand-written notebook JSON and Colab refuses to open the file, in front of a
room.

### Before every deploy

```bash
python qa.py
```

Paths, offline-safety, the store ids, Arabic wrapping, dead links, colour
contrast, the print stylesheet, and keyboard reachability. It exits non-zero if
anything is wrong.

---

Built for the **SDAIA Academy** course *Applied Generative AI*.
Instructor: **Musa Ibn Rashid** · August 2026.
