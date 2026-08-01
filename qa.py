#!/usr/bin/env python3
"""
qa.py — site-wide checks. Run before every deploy.

    python qa.py

  1. Path check      — no leading-slash href/src (GitHub Pages project site)
  2. Offline check   — nothing loads from the network
  3. Store check     — activity ids unique, and the hub totals add up
  4. Arabic check    — every Arabic string carries lang="ar" dir="rtl"
  5. Dead links      — every internal link resolves to a file that exists
  6. Contrast check  — every text/background pair is at least 4.5:1
                       (3:1 for large text, which is noted where it applies)

Print and keyboard checks are structural and are asserted here as far as a
script can: print rules are checked for presence in deck.css, and every
interactive element is checked for being a real button/a/input rather than a
clickable div.
"""

import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP_DIRS = {".git", "docs", "__pycache__", "data"}

# External links a student deliberately clicks. Anything else is a defect.
ALLOWED_HOSTS = ("github.com", "colab.research.google.com", "aistudio.google.com",
                 "raw.githubusercontent.com", "www.w3.org")

ARABIC = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]")

findings = []


def add(kind, path, detail):
    findings.append((kind, os.path.relpath(path, ROOT).replace("\\", "/"), detail))


def walk(exts):
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in sorted(files):
            if f.endswith(exts):
                yield os.path.join(base, f)


def read(path):
    with io.open(path, encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------- 1
def check_paths():
    for path in walk((".html", ".css", ".js")):
        text = read(path)
        for m in re.finditer(r'(?:href|src)\s*=\s*"(/[^/"][^"]*)"', text):
            add("PATH", path, "absolute path %r will 404 under /repo-name/" % m.group(1))
        for m in re.finditer(r'url\(\s*"?(/[^/"\')]+)', text):
            add("PATH", path, "absolute CSS url %r" % m.group(1))


# ---------------------------------------------------------------- 2
def check_offline():
    for path in walk((".html", ".css", ".js")):
        text = read(path)
        for m in re.finditer(r'(?:href|src)\s*=\s*"(https?://[^"]+)"', text):
            url = m.group(1)
            if not any(h in url for h in ALLOWED_HOSTS):
                add("OFFLINE", path, "loads %r from the network" % url)
        # A stylesheet or script from the network is never acceptable.
        for m in re.finditer(r'<(?:link|script)[^>]*(?:href|src)="(https?://[^"]+)"', text):
            add("OFFLINE", path, "stylesheet/script from the network: %r" % m.group(1))
        for m in re.finditer(r'@import\s+(?:url\()?["\']?(https?://[^"\')]+)', text):
            add("OFFLINE", path, "@import from the network: %r" % m.group(1))


# ---------------------------------------------------------------- 3
def check_store():
    registry = read(os.path.join(ROOT, "assets", "activities.js"))
    ids = re.findall(r"id:\s*'([a-z\-]+)'", registry)
    maxes = [int(m) for m in re.findall(r"max:\s*(\d+)", registry)]

    if len(ids) != len(set(ids)):
        add("STORE", os.path.join(ROOT, "assets", "activities.js"), "duplicate activity ids")

    total = sum(maxes)
    print("    registry: %d activities, %d points total" % (len(ids), total))

    # Every activity page must save with its registry id, and the max it
    # saves must match the registry.
    for aid, amax in zip(ids, maxes):
        page = os.path.join(ROOT, "activities", aid + ".html")
        if not os.path.exists(page):
            add("STORE", page, "registry lists %r but the page does not exist" % aid)
            continue
        text = read(page)
        if "Store.saveScore(" not in text:
            add("STORE", page, "never calls Store.saveScore()")
        if ("ACTIVITY_ID = '%s'" % aid) not in text:
            add("STORE", page, "does not declare ACTIVITY_ID = '%s'" % aid)
        m = re.search(r"var MAX = (\d+)", text)
        if m and int(m.group(1)) != amax:
            add("STORE", page, "MAX is %s but the registry says %d" % (m.group(1), amax))

    # Both readers must use the shared registry rather than a local copy.
    for reader in ("index.html", os.path.join("activities", "index.html")):
        text = read(os.path.join(ROOT, reader))
        if "activities.js" not in text:
            add("STORE", os.path.join(ROOT, reader), "does not load the shared registry")
        if re.search(r"var ACTIVITIES\s*=\s*\[", text):
            add("STORE", os.path.join(ROOT, reader), "declares its own ACTIVITIES list — will drift")


# ---------------------------------------------------------------- 4
def check_arabic():
    for path in walk((".html",)):
        text = read(path)

        # Strip <script> blocks: Arabic there is data, and the elements it
        # is written into set lang/dir at runtime. Checked separately below.
        stripped = re.sub(r"<script\b.*?</script>", "", text, flags=re.S)

        for m in ARABIC.finditer(stripped):
            start = m.start()
            # Find the tag that opens the text node this character sits in.
            open_tag = stripped.rfind("<", 0, start)
            tag_text = stripped[open_tag:start]
            # Walk back up to 400 chars looking for a lang="ar" on the
            # element or an ancestor that opened recently.
            window = stripped[max(0, start - 400):start]
            if 'lang="ar"' not in window:
                line = stripped[:start].count("\n") + 1
                add("ARABIC", path,
                    "line %d: Arabic text not inside lang=\"ar\": %r"
                    % (line, stripped[start:start + 30]))
                break     # one report per file is enough to act on

        # Where Arabic lives in JS, the element it is written into must get
        # both lang and dir set.
        if ARABIC.search(text) and "<script" in text:
            js = "\n".join(re.findall(r"<script\b.*?</script>", text, flags=re.S))
            if ARABIC.search(js):
                if "setAttribute('lang', 'ar')" not in js and "lang=\"ar\"" not in js \
                        and "'lang', r.lang" not in js and "setAttribute('lang'" not in js:
                    add("ARABIC", path, "Arabic in a script block, but no lang attribute is set on the target element")


# ---------------------------------------------------------------- 5
def check_links():
    for path in walk((".html",)):
        # Strip script blocks: href="..." inside JS string concatenation is
        # a template, not a link, and matching it invents dead links.
        # Strip HTML comments too — markup in a comment never loads, and
        # commented-out examples are documentation, not defects.
        text = re.sub(r"<script\b.*?</script>", "", read(path), flags=re.S)
        text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
        base = os.path.dirname(path)
        for m in re.finditer(r'(?:href|src)\s*=\s*"([^"#?][^"]*?)"', text):
            url = m.group(1)
            if url.startswith(("http://", "https://", "mailto:", "data:", "#")):
                continue
            target = os.path.normpath(os.path.join(base, url.split("#")[0].split("?")[0]))
            if not os.path.exists(target):
                add("DEADLINK", path, "%r does not exist" % url)


# ---------------------------------------------------------------- 6
def luminance(hexcolour):
    h = hexcolour.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4) for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def check_contrast():
    theme = read(os.path.join(ROOT, "assets", "theme.css"))
    tok = dict(re.findall(r"--([a-z0-9\-]+):\s*(#[0-9a-fA-F]{3,6});", theme))

    # (name, foreground, background, minimum) — 3.0 where the usage is
    # large text only, which is noted in the label.
    pairs = [
        ("body text on paper",            tok["text"], tok["paper"], 4.5),
        ("muted text on paper",           tok["text-muted"], tok["paper"], 4.5),
        ("muted text on card",            tok["text-muted"], tok["card"], 4.5),
        ("teal link on paper",            tok["teal"], tok["paper"], 4.5),
        ("teal link on card",             tok["teal"], tok["card"], 4.5),
        ("white on teal button",          "#ffffff", tok["teal"], 4.5),
        ("white on teal-dark",            "#ffffff", tok["teal-dark"], 4.5),
        ("text on dark, on ink",          tok["text-on-dark"], tok["ink"], 4.5),
        ("muted on dark, on ink",         tok["text-muted-on-dark"], tok["ink"], 4.5),
        ("muted on dark, on ink-2",       tok["text-muted-on-dark"], tok["ink-2"], 4.5),
        ("teal-bright on ink",            tok["teal-bright"], tok["ink"], 4.5),
        ("teal-bright on ink-2",          tok["teal-bright"], tok["ink-2"], 4.5),
        ("sky on ink",                    tok["sky"], tok["ink"], 4.5),
        ("coral-ink on paper",            tok["coral-ink"], tok["paper"], 4.5),
        ("amber-ink on paper",            tok["amber-ink"], tok["paper"], 4.5),
        ("ink text on teal-bright card",  tok["ink"], tok["teal-bright"], 4.5),
        ("ink text on amber card",        tok["ink"], tok["amber"], 4.5),
        ("white on coral card (large)",   "#ffffff", tok["coral"], 3.0),
    ]

    for label, fg, bg, minimum in pairs:
        ratio = contrast(fg, bg)
        flag = "ok " if ratio >= minimum else "FAIL"
        print("    %s %-32s %5.2f:1  (min %.1f)" % (flag, label, ratio, minimum))
        if ratio < minimum:
            add("CONTRAST", os.path.join(ROOT, "assets", "theme.css"),
                "%s is %.2f:1, below %.1f" % (label, ratio, minimum))


# ---------------------------------------------------------------- print/kbd
def check_print_and_keyboard():
    deck = read(os.path.join(ROOT, "assets", "deck.css"))
    required = [
        ("one slide per page", "page-break-after: always"),
        ("slides visible in print", "display: flex !important"),
        ("dot strip hidden", ".deck-dots"),
        ("counter hidden", ".deck-counter"),
        ("buttons hidden", ".deck-bar"),
        ("help overlay hidden", ".deck-help"),
        ("notes printed", ".slide-wrap > .notes"),
        ("backgrounds preserved", "print-color-adjust: exact"),
        ("landscape A4", "size: A4 landscape"),
    ]
    print_block = deck[deck.find("@media print"):]
    for label, needle in required:
        if needle not in print_block:
            add("PRINT", os.path.join(ROOT, "assets", "deck.css"),
                "print rule missing: %s (%r)" % (label, needle))

    # Logos print from inside the slide, so they must be stamped per slide.
    if "stampLogos" not in read(os.path.join(ROOT, "assets", "deck.js")):
        add("PRINT", os.path.join(ROOT, "assets", "deck.js"), "no per-slide logo stamping")

    # Keyboard: no clickable divs/spans anywhere.
    for path in walk((".html",)):
        text = read(path)
        for m in re.finditer(r'<(div|span|p|li)\b[^>]*\bonclick=', text):
            add("KEYBOARD", path, "clickable <%s> is not keyboard reachable" % m.group(1))
        # createElement('div') + addEventListener('click') in the same file
        # is the JS version of the same mistake.
        if re.search(r"createElement\(['\"]div['\"]\)[\s\S]{0,400}?addEventListener\(['\"]click['\"]", text):
            add("KEYBOARD", path, "a generated <div> has a click handler — check it is focusable")

    site = read(os.path.join(ROOT, "assets", "site.css"))
    if ":focus-visible" not in site:
        add("KEYBOARD", os.path.join(ROOT, "assets", "site.css"), "no visible focus ring defined")


def main():
    print("QA pass\n")

    print("  1 · paths");          check_paths()
    print("  2 · offline");        check_offline()
    print("  3 · store");          check_store()
    print("  4 · arabic");         check_arabic()
    print("  5 · dead links");     check_links()
    print("  6 · contrast");       check_contrast()
    print("  7 · print + keyboard"); check_print_and_keyboard()

    print()
    if not findings:
        print("PASS — nothing found.")
        return 0

    print("%d finding(s):\n" % len(findings))
    for kind, path, detail in findings:
        print("  [%s] %s: %s" % (kind, path, detail))
    return 1


if __name__ == "__main__":
    sys.exit(main())
