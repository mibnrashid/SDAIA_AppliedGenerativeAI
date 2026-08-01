# `prompts.md` — Claude Code build sequence

**Applied Generative AI · SDAIA Academy course site**

Run these **one at a time, in order**, in an empty folder that already
contains your `assets/` with `sdaia.svg` and `sdaia-academy.svg`.

After each prompt: open the affected page in a browser, check it, then move
on. Do not batch them — each one assumes the previous one landed.

---

## Ground rules (paste this once at the start of your Claude Code session)

> You are building a static course site for SDAIA Academy that I will deploy
> to GitHub Pages. Hard constraints, applying to everything you write:
>
> - **No build step.** Plain HTML, CSS, and vanilla JS only. No npm, no
> bundler, no framework, no TypeScript.
> - **No CDN dependencies.** The venue wifi is unreliable and I need every
> page to work fully offline. If you need a library, vendor the file into
> `assets/vendor/`. Prefer writing it yourself.
> - **Relative paths only.** This deploys to a GitHub Pages *project* site
> served from `/repo-name/`, so a leading-slash path like
> `/assets/theme.css` will 404. Always use `../assets/theme.css` or
> `./assets/theme.css`.
> - **No localStorage key collisions.** Every stored key is prefixed
> `agai:`.
> - **Arabic-safe.** Some content contains Arabic terms inline in English
> sentences. Wrap them in `<span lang="ar" dir="rtl">` and make sure the
> surrounding paragraph stays LTR.
> - **Accessible.** Real heading order, keyboard-reachable controls, visible
> focus rings, `alt` on the logos.
> - After each task, tell me exactly which files you created or changed and
> what I should click to verify it.

---



## Prompt 1 — Scaffold and theme

> Create the folder structure below, plus `assets/theme.css` and
> `assets/site.css`. Do not write page content yet — this task is only the
> skeleton and the design tokens.
>
> ```
> index.html
> assets/{theme.css,site.css,deck.css,deck.js,store.js,activity.css}
> slides/{day1..day5}.html
> activities/{index.html,tokenizer-race.html,chunk-lab.html,be-the-agent.html,cost-auction.html,red-team.html}
> assessment/{pretest.html,posttest.html}
> project/index.html
> notebooks/README.md
> README.md
> .nojekyll
> ```
>
> Create every file, but the HTML files can be empty stubs with just a title
> for now. `.nojekyll` must be an empty file — it stops GitHub Pages
> mangling anything.
>
> `assets/theme.css` holds CSS custom properties only. Read
> `assets/sdaia.svg` and `assets/sdaia-academy.svg` and pull the real brand
> colours out of them rather than guessing. The palette I want, adjusted to
> whatever those SVGs actually contain:
>
> - `--ink` very dark navy, the hero background
> - `--ink-2` a slightly lighter navy for cards on dark
> - `--teal` the primary accent (buttons, links, active states)
> - `--teal-bright` a lighter teal for highlights on dark backgrounds
> - `--coral`, `--amber` two secondary accents for activity cards
> - `--paper` off-white page background, `--card` white card surface
> - `--text`, `--text-muted`, `--border`
>
> Typography: a serif display face for large headlines and a clean sans for
> everything else. **Use system font stacks — no Google Fonts, no network
> requests.** Something like
> `Georgia, 'Times New Roman', serif` for display and the standard system
> sans stack for body. Define `--font-display` and `--font-sans`.
>
> Also define spacing (`--s1` … `--s6`), `--radius`, and `--maxw` (1120px).
>
> `assets/site.css` holds the shared page chrome: a header bar with
> `sdaia-academy.svg` top-left and `sdaia.svg` top-right, a page container,
> a footer with both logos and the text
> `Built for the SDAIA Academy course · Instructor: Musa Ibn Rashid`,
> plus base type styles, link styles, and a `.btn` class.
>
> Both logos must render correctly on a dark background *and* a light one —
> check the SVGs and if they're single-colour, use a CSS filter or a
> `currentColor` fill so they invert cleanly.

---



## Prompt 2 — The home page

> Build `index.html` — the page I send students on Sunday morning.
>
> Match the visual language of my previous SDAIA workshop hub: a full-width
> dark navy hero, an eyebrow line in teal small-caps reading
> `SDAIA ACADEMY · APPLIED GENERATIVE AI`, then a large serif headline, then
> a short paragraph, then a row of pill-shaped chips.
>
> - Headline: **From a prompt to a system.**
> - Paragraph: "Five days building generative AI that actually ships —
> retrieval you can measure, tools that do real work, and the numbers to
> prove it runs. Slides, labs, and activities all live here."
> - Chips: `Foundations` `Retrieval` `Agents` `Production` `Security`
>
> Below the hero, on the light background:
>
> 1. A **call-to-action band** for the pre-test, styled like a wide teal
>   card: "New here? Take the pre-test first — 20 questions across the
>    whole course. It measures the course, not you." with a
>    `Start pre-test →` button linking to `assessment/pretest.html`.
> 2. A **five-card grid**, one per day. Each card: a big number `01`–`05` in
>   the coloured header, a `DAY 1` badge, the day title, a one-line
>    description, and three links in the card footer —
>    `Slides →`, `Lab →`, `Activity →`. Use alternating header colours from
>    the theme (teal, ink, teal-bright, coral, amber) exactly like my
>    workshop hub cards.
>   - 01 · Day 1 — **From token to typed output.** How the model works, and
>   how to make it return data your code can trust.
>   - 02 · Day 2 — **Retrieval you can measure.** Build RAG, then prove it
>   works with hybrid search and a golden set.
>   - 03 · Day 3 — **Tools and agents.** Let the model act, then keep it on
>   a short leash.
>   - 04 · Day 4 — **Production and the numbers.** Latency, caching, and
>   what this actually costs per user.
>   - 05 · Day 5 — **Break it, then defend it.** Prompt injection, red
>   teaming, and governance.
> 3. A **two-card row** below: one linking to `project/index.html` (title
>   "The project", text "What you're building, and exactly how it's
>    scored — 100 points, due Thursday.") and one linking to
>    `activities/index.html` ("All activities", "Six scored activities you
>    can replay any time.").
> 4. A **progress strip** at the bottom in a bordered card: "Your progress —
>   N of 6 activities attempted · pre-test: done/not done · session total
>    X / Y", with a `Reset my progress` button. Read this from
>    `localStorage` via `assets/store.js` — write that file now with this
>    API and nothing more:
>
> Every link must work even though most target pages are still stubs.

---



## Prompt 3 — The deck engine

> Build `assets/deck.css` and `assets/deck.js` — a reusable HTML slide
> engine. Then convert `slides/day1.html` into a three-slide demo that
> exercises every feature, so I can check the engine before we write real
> content.
>
> Authoring format — a deck is plain HTML:
>
> ```html
> <div class="deck" data-title="Day 1 — From token to typed output">
>   <section class="slide slide--title"> … </section>
>   <section class="slide"> … </section>
> </div>
> ```
>
> `deck.js` must provide:
>
> - **Navigation:** `→` `←` `Space` `PageUp/PageDown`, click on the right or
> left third of the screen, and swipe on touch. `Home`/`End` jump to
> first/last.
> - **A progress dot strip** at the bottom, clickable to jump.
> - **Slide counter** bottom-right, `4 / 27`.
> - **Deep linking:** the URL hash is the slide number, so `#12` opens on
> slide 12 and refresh keeps position.
> - `P` **toggles presenter notes** — any `<aside class="notes">` inside a
> slide is hidden by default and shown as a fixed panel at the bottom when
> toggled. This is what I read from while teaching.
> - `F` **toggles fullscreen.**
> - **A print-to-PDF button** in the top bar. It sets a `printing` class on
> `<body>` and calls `window.print()`.
> - `?` **shows a keyboard help overlay.**
>
> `deck.css` must include an `@media print` block that is genuinely good, not
> an afterthought:
>
> - every slide becomes exactly one landscape A4 page, `page-break-after: always`
> - all slides visible (they're hidden in screen mode)
> - dot strip, counter, buttons and the help overlay hidden
> - notes printed underneath their slide in small type
> - both logos on every printed page
> - backgrounds preserved with `print-color-adjust: exact`
>
> Slide layout classes to support: `.slide--title`, `.slide--section`
> (full-bleed dark divider), `.slide--split` (two columns),
> `.slide--code` (a code block with a caption column beside it), and
> `.slide--full` (one big statement).
>
> Slides must scale to the viewport rather than scroll. Use a fixed
> 1280×720 slide canvas with a CSS `transform: scale()` fitted on resize.
>
> Build the Day 1 demo deck with: a title slide, one split slide, and one
> code slide with notes, so I can test all of it.

---



## Prompt 4 — Day 1 deck

> Fill `slides/day1.html` with the real Day 1 deck, using the engine from
> the previous task. Target **22–26 slides**. Add
> `<aside class="notes">` to every content slide — 2–4 complete, speakable
> sentences I can read aloud verbatim without having to interpret anything
> on the spot. Never write notes that just restate the slide title.
>
> Structure:
>
> 1. Title slide
> 2. **Day 1 objectives** — 5 numbered items
> 3. The week map, five days, one line each, Day 1 highlighted
> 4. Section divider: *How the thing actually works*
> 5. Discriminative vs generative — one slide, then move on
> 6. Tokens — what they are, with a worked example
> 7. **Tokens in Arabic vs English** — the same sentence, two counts, and
>   the cost consequence. Embed a small live widget: a textarea and an
>    approximate token count that updates as I type (approximate is fine —
>    use a simple heuristic and label it "approximate").
> 8. Context window — what it is, and one line: "this is why chunking exists
>   tomorrow"
> 9. Next-token prediction — why it's fluent and wrong at once
> 10. Temperature — a visual: same prompt, three outputs at 0.0 / 0.7 / 1.2
> 11. Hallucination — a property to design around, not a bug to patch
> 12. **The four ways to make a model useful** — a comparison table:
>   prompting / RAG / tools / fine-tuning, each with "what it is", "cost",
>     "when". Add the line "most people reach for fine-tuning and should
>     have reached for RAG."
> 13. Section divider: *Make it reliable*
> 14. System vs user role — and note the separation is a security boundary
>   we'll attack on Day 5
> 15. Anatomy of a prompt that holds: role, context, task, format, examples
> 16. Few-shot examples — before/after
> 17. Section divider: *Make it typed*
> 18. Why free text is unusable inside software — a concrete failure
> 19. **Code slide:** JSON mode with a response schema. Walk it argument by
>   argument in the notes.
> 20. **Code slide:** `json.loads()` and branching on the result — the
>   moment generative AI becomes a component
> 21. **Code slide:** the `ask()` wrapper with retries
> 22. Model ≠ solution — the six layers (application, orchestration, model,
>   tools, data, governance)
> 23. The solution lifecycle — six steps
> 24. Today's lab — what they'll build, with a Colab button
> 25. **Day 1 summary** — 4 bullets
> 26. Homework: GitHub account, pick a document set
>
> Code slides must show real, runnable `google-genai` Python using
> `gemini-2.5-flash-lite`. Check the current SDK syntax rather than writing
> it from memory — if you're not certain of a method signature, say so in a
> comment rather than inventing one.

---



## Prompt 5 — Day 2 deck

> Build `slides/day2.html`, same engine and conventions, **26–30 slides**.
> This is the most important deck of the week — Day 2 has the highest
> ceiling.
>
> 1. Title · 2. Day 2 objectives · 3. Recall from Day 1 (3 questions to ask
>
> the room, not answers)
> 4. Divider: *Choosing an architecture*
> 5. Why the model doesn't know your documents
> 6. RAG in four steps — an animated-on-click diagram if you can do it
>    cleanly with CSS, static if not
> 7. Agents as a loop
> 8. RAG vs Agents comparison table
> 9. The decision rule + "start with the simplest thing that works"
> 10. Divider: *The pipeline*
> 11. The five stages overview
> 12. Ingestion — cleaning, and keeping source + page metadata for citations
> 13. **Multimodal ingestion** — a scanned Arabic PDF has no text layer;
>     send the page image to a vision model. Frame this as a pipeline stage,
>     not a demo.
> 14. **Code slide:** vision extraction
> 15. Chunking — size, overlap, structure-aware
> 16. Chunking gone wrong — show a bad split mid-table
> 17. **Code slide:** the chunker
> 18. Embeddings — meaning as coordinates, "annual leave" vs "vacation days"
> 19. Vector databases — Chroma, Pinecone, Weaviate
> 20. **Code slide:** embed and store
> 21. Retrieval and top-k — coverage vs noise
> 22. Divider: *Making it actually good*
> 23. **Where vector search fails** — IDs, acronyms, exact names. Use
>     `SDAIA-F-CRS-201-01-V1` as the worked example.
> 24. Hybrid retrieval — BM25 + vector, scores combined
> 25. **Code slide:** hybrid search
> 26. Re-ranking — retrieve 20 cheap, keep the best 4
> 27. Query rewriting
> 28. Divider: *Proving it works*
> 29. **The golden question set** — what it is and how to write one
> 30. **Code slide:** the evaluation loop and a results table
> 31. Common RAG mistakes — chunks too big, top-k too high, no metadata, no
>     evaluation
> 32. Today's lab + Colab button
> 33. Day 2 summary
>
> Trim to fit 30 if needed, but do not cut anything from slide 22 onward —
> that's the part of the day that earns the course title.

---



## Prompt 6 — Days 3, 4 and 5 decks

> Build `slides/day3.html`, `slides/day4.html` and `slides/day5.html`. Same
> engine, same conventions, 22–26 slides each, notes on every content slide.
> Do all three in this task, but show me each file as you finish it.
>
> **Day 3 — Tools and agents.** Objectives · why the model needs tools (no
> live data, no actions, unreliable arithmetic) · **the model does not run
> your code** (give this its own full-bleed statement slide) · the 5-step
> loop · code: tool schema walked argument by argument · why `description`
> is the most important field · code: the manual round trip · the agent loop
> · code: `run_agent` with `max_steps` · what happens without a step cap ·
> the six patterns (ReAct, Plan-and-Execute, Reflection, Routing,
> Hierarchical, Human-in-the-loop) one line each plus "use it when" ·
> guardrails · error recovery — what a tool returns when it fails ·
> **agentic RAG**: yesterday's retriever becomes today's tool · code ·
> lab + Colab · summary.
>
> **Day 4 — Production and the numbers.** Objectives · prototype vs
> production comparison table · scalability: concurrency, async, caching,
> rate limiting · connect rate limiting back to the 429 errors they hit on
> Monday · **the cost slide** — embed a live calculator: inputs for
> users/day, queries/user, avg input tokens, avg output tokens, and a price
> field; outputs cost per query, per day, per month. Make it real and
> usable. · Arabic costs more — callback to Day 1 · latency: streaming,
> model right-sizing, caching, batching · reliability: retries, backoff,
> fallback chains, timeouts · observability: logging, tracing, metrics,
> continuous eval · deployment architecture diagram · UX for AI products ·
> lab + Colab · summary.
>
> **Day 5 — Break it, then defend it.** Objectives · the new attack surface:
> the input *is* the attack · direct injection · **indirect injection** —
> hidden instructions inside a retrieved document, and the line "nobody
> attacked the system; the attack was in the data" as a full-bleed slide ·
> consequences · layered defences, one slide per layer · **honest slide: this
> is not solved** · grounding and structured output as reliability controls ·
> PII and privacy — callback to the Day 1 free-tier warning · governance:
> policies, audit, accountability, compliance · responsible AI: bias,
> fairness, transparency · the pre-launch checklist as a printable table ·
> red team activity brief · presentation format · course summary · where to
> go next.

---



## Prompt 7 — The pre-test and post-test

> Build `assessment/pretest.html` and `assessment/posttest.html`. They share
> the same 20 questions and the same engine — put the questions in
> `assessment/questions.js` as a single exported array so both pages read
> from one source and can never drift apart.
>
> Write all 20 questions yourself, following this coverage: 4 on LLM
> mechanics (tokens, context window, temperature, hallucination), 4 on
> retrieval, 3 on architecture choice, 3 on tools and agents, 3 on
> production and cost, 3 on security and governance.
>
> Rules for the questions:
>
> - Multiple choice, exactly 4 options, one correct.
> - Every question must be answerable from the material in `slides/`.
> - At least 6 must be answerable by a smart person with no AI background,
> so the pre-test doesn't demoralise anyone.
> - At least 3 must be hard enough that most people will still miss them on
> Thursday.
> - Distractors must be plausible. No joke options.
> - Each question carries a short `explanation` string, shown **only on the
> post-test** after submission.
>
> Behaviour:
>
> - One question per screen with a progress bar, or all on one page —
> whichever you judge better for a 15-minute in-class test on laptops.
> Justify your choice to me in one line.
> - No timer. No back-button trapping.
> - On submit: score out of 20, saved to `localStorage` as `agai:pretest`
> or `agai:posttest`.
> - **A big "Copy my result" button** that copies e.g.
> `Pre-test: 11/20` to the clipboard — students read this out for the
> SDAIA attendance sheet, so it has to be one tap.
> - The post-test page additionally shows the delta against the stored
> pre-test score: "You went from 11 to 17. +6."

---



## Prompt 8 — Activities hub and the first two activities

> Build `activities/index.html` plus `activities/tokenizer-race.html` and
> `activities/chunk-lab.html`. Also write `assets/activity.css` for the
> shared activity chrome: a header with the activity name and its day badge,
> a scoring strip, and a "back to all activities" link.
>
> `activities/index.html` is a card grid of all six activities, matching my
> workshop hub layout: numbered `01`–`06`, day badge, title, one-line
> description, and a footer showing either `Not started` or
> `✓ Best 12 / 14` from `Store`, with a `Start →` / `Play again →` link.
> Bottom card shows session total and a reset button.
>
> **Activity 1 · Tokenizer Race** (Day 1, 8 minutes)
> A sentence appears. The student guesses how many tokens it is and submits.
> The real count is revealed with the sentence split into visible coloured
> token chunks. Score by closeness: exact = 3 points, within 2 = 2, within 5
> = 1. Eight rounds, alternating English and Arabic sentences, ending on a
> pair of sentences with the *same meaning* in both languages so the cost
> difference lands. Max 24 points.
>
> For tokenisation, implement a documented heuristic in JS — roughly 4
> characters per token for English, roughly 2 for Arabic, with whitespace
> and punctuation handling. **Label it "approximate" on screen.** Do not
> pull in a real tokeniser library; offline matters more than precision
> here, and the teaching point is the ratio, not the exact number.
>
> **Activity 2 · Chunk Lab** (Day 2, 20 minutes)
> A real two-page policy document is displayed as flowing text. The student
> clicks between paragraphs to place chunk boundaries. Live readout: number
> of chunks, average size in approximate tokens, largest and smallest.
>
> Then a **Test my chunking** button runs 6 pre-written questions against
> their chunking. Each question has an associated span of the document that
> must fall inside a single chunk to be answerable. Show pass/fail per
> question with the reason ("this answer was split across two chunks").
> Score out of 6, plus 2 bonus points for having no chunk over 800
> approximate tokens.
>
> Then a **Show me a naive split** button that overlays what a blind
> 500-character split does to the same document, so they can see it cut
> mid-sentence and orphan a heading from its table. This comparison is the
> whole point of the activity — make it visually obvious.
>
> Save best scores through `Store.saveScore()`.

---



## Prompt 9 — The remaining three activities

> Build `activities/be-the-agent.html`, `activities/cost-auction.html` and
> `activities/red-team.html`. Same chrome, same scoring pattern.
>
> **Activity 3 · Be the Agent** (Day 3, 15 minutes)
> The student plays the *model* in a tool loop. A goal appears — "find the
> cheapest flight to Jeddah on Tuesday and tell me the total for 3
> passengers." Each turn they choose from: call a tool (pick which, and fill
> its arguments), or give a final answer. The tools are simulated with a
> fixed dataset and respond realistically, including one deliberate error
> response they have to recover from.
>
> Score: reaching the correct answer = 6 points, minus 1 per wasted step
> beyond the minimum, plus 2 for recovering from the tool error correctly.
> Show a running trace panel on the right that looks like real agent output.
> After finishing, a summary explains what a real agent would have done at
> each turn.
>
> **Activity 4 · Cost Auction** (Day 4, 12 minutes)
> Five scenarios, each describing a deployment in plain language ("an
> internal HR assistant for 500 employees, 4 questions each per working
> day, answers around 300 words"). The student enters their estimate of the
> monthly cost. Reveal shows the worked calculation line by line. Score by
> order of magnitude: right order of magnitude = 3, one off = 1, else 0.
> Max 15. Final screen shows a full cost model they can reuse.
>
> **Activity 5 · Red Team** (Day 5, 25 minutes)
> A simulated document assistant with a visible (but locked) system prompt
> and a small retrievable corpus. Five attack objectives, each worth points:
> instruction override (3), system prompt extraction (3), scope escape (2),
> indirect injection via adding a poisoned document to the corpus (5),
> resource exhaustion (2). Max 15.
>
> Attacks are matched against pattern rules you define in JS — no live model
> call, this must work offline. Be generous with the matching; the point is
> to reward creative attempts, not to be a strict grader.
>
> Then a **Turn on defences** toggle that visibly enables input sanitising,
> instruction/data separation and output validation — and lets them re-run
> their successful attacks to see which now fail and which still get
> through. **Make sure at least one still gets through**, and say so on
> screen. That honesty is the lesson.

---

Prompt 10a — Notebook generator + Notebook 0 and 1

Before the notebook pages, we need the notebooks themselves. Create
notebooks/ containing real .ipynb files.

How to build them: write a Python script notebooks/build.py that
constructs each notebook as a dict and writes valid nbformat 4 JSON. Do
not hand-write .ipynb JSON — one missing comma and Colab refuses to
open it. The script must be re-runnable so I can regenerate after edits.
Run it and confirm every file parses with json.load().

Conventions for all notebooks:

Cell 1 is always: pip install -q the needed packages, imports, then
the key load:
python
from google.colab import userdata
API_KEY = userdata.get('GEMINI_API_KEY')
wrapped in try/except printing a clear instruction to open the 🔑 panel
in the Colab sidebar and add a secret named GEMINI_API_KEY.
Model everywhere: gemini-2.5-flash-lite. Embeddings:
gemini-embedding-001.
Nobody writes a cell from empty. # TODO cells have the full
structure written with one or two lines blanked and a comment saying
exactly what goes there.
Every notebook ends with a markdown reflection cell with blank
prompts to fill in, and an "If this breaks" markdown cell listing
the three most likely failures and their fixes.
Markdown cells carry the teaching: explain why before each code cell,
not just what.
Every notebook opens with a markdown title cell naming the day and
stating what they'll have working by the end.

Check the current google-genai SDK syntax rather than writing from
memory. If unsure of a method signature, leave a comment saying so rather
than inventing one — these run live in front of a camera.

Build two notebooks in this task:

day1_first_calls.ipynb — 20 cells, exactly as follows: setup ·
what-you'll-build · first call (pre-written, 4 lines) · what just happened
· print usage_metadata · TODO their own prompt · Arabic vs English token
count on the same sentence · why Arabic costs more · temperature 0.0 run
3× · temperature 1.2 run 3× · TODO reflection on the difference · system
instruction with two personas · TODO write a system instruction forcing
bullet points under 50 words · context window overflow, catch the error ·
markdown: why free text is unusable in software · JSON mode with a
response schema extracting {name, email, intent, urgency} from a support
message · json.loads() then branch on it with an if · TODO their
own schema · the ask() wrapper with system prompt, temperature, retries
and optional schema, given complete · reflection + if-this-breaks.

project_scaffold.ipynb — the file students build their project on.
Twelve clearly-headed sections, structure written, TODO markers
throughout: config · load_my_documents() pointing at their own files ·
chunk · index · hybrid retrieve (given complete) · tools, one example plus
an empty slot · agent loop (given complete) · guardrails, one example plus
a slot · instrumentation from Day 4 · demo() — the function they run on
Thursday · a golden set of 5 questions · a README template in a markdown
cell they copy into their repo.

Prompt 10b — Notebook 2

Build notebooks/day2_retrieval.ipynb via build.py. This is the longest
and most important notebook of the week, taught across two blocks. 25
cells.

Part A — a working naive RAG (cells 1–12):
setup with chromadb, google-genai, rank-bm25 · download the provided
document set · load and clean into {text, source, page} dicts
(pre-written) · markdown on multimodal ingestion · send a scanned page
image to the vision model, get text back, add it to the corpus
(pre-written, high impact) · chunk(text, size, overlap) as a TODO
with the loop body blanked · inspect 3 chunks, check nothing is cut
mid-word · embed all chunks batched with gemini-embedding-001 · store in
Chroma with metadata · search(query, k) printing chunks with sources ·
answer(query) retrieving and generating with citations · TODO: three
questions about their own domain.

Part B — the ceiling (cells 13–25):
markdown on where vector search fails · demonstrate it — search
"SDAIA-F-CRS-201" and watch it miss · BM25 index over the same chunks ·
hybrid_search() with the weighting line as a TODO · re-run the
failing query, watch it succeed · markdown on re-ranking · LLM-as-reranker
scoring 20 chunks 0–10, keep top 4 · query rewriting · markdown on golden
sets · GOLDEN = [{"q":..., "must_contain":...}] as a TODO they fill ·
evaluate(search_fn) returning hit rate, pre-written · score naive vs
hybrid vs re-ranked and print a comparison table · reflection.

Also create the corpus. Write notebooks/data/build_corpus.py that
generates ~15 short documents — a mix of English and Arabic, policy-style,
with realistic IDs like SDAIA-F-CRS-201-01-V1 embedded in the text so
the vector-search-failure demo actually works. Plus one PNG of a rendered
page with no text layer for the vision-extraction cell. Commit the
generated files so students download them from the repo raw URLs, not from
a live service.

Known breakages to handle in the code itself: embedding rate limits
(batch with a sleep, pre-written), Chroma collection already existing on
re-run (add a delete_collection guard), and Arabic text direction
scrambling printed output.

Prompt 10c — Notebooks 3, 4, 5

Build the remaining three notebooks via build.py. Show me each as you
finish it.

day3_agents.ipynb — 18 cells: setup · calculate(expression) as a
real function · get_weather(city) mocked deliberately · markdown on why
a mock is fine, the loop is the lesson · tool schemas walked argument by
argument · the manual round trip split across four separate cells —
send, inspect the request, execute, send the result back — so the
round-trip is impossible to miss · markdown restating that the model never
ran your function · run_agent(goal, tools, max_steps) given complete ·
run a two-step task with verbose=True printing every decision · TODO
their own third tool · remove the step cap and run a task it can't
finish — watch it spiral, interrupt manually · markdown on what that
would have cost on a paid key · cap restored plus an output validator ·
markdown: the ceiling is agentic RAG · wrap Notebook 2's search() as a
tool named search_documents · give the agent both retriever and
calculator, ask a question needing both · print the trace · reflection.

day4_production.ipynb — 15 cells, applied to their own project:
setup importing their Day 2/3 functions · @retry decorator with
exponential backoff, given complete · force a failure to prove it fires ·
streaming vs non-streaming side by side, timed · markdown: streaming
doesn't make it faster, it makes it feel faster · dict cache keyed on
prompt · 20 queries with 8 repeats, measure hit rate and time saved ·
log_request() appending {timestamp, prompt_tokens, output_tokens, latency, cost} · TODO: the cost formula from the pricing table · 15
mixed queries into a pandas DataFrame, .describe() · plot latency
distribution and cumulative cost · TODO markdown: from your table,
compute cost per query and per user per month at 4 queries/day ·
fallback chain primary → cheaper → canned · break the primary, watch the
fallback engage · reflection.

day5_redteam.ipynb — 15 cells: setup loading a deliberately
vulnerable assistant (given) · attack 1 instruction override, watch it
work · attack 2 system prompt extraction · attack 3 scope escape, make a
policy bot answer about football · markdown on indirect injection ·
add a poisoned document containing hidden instructions to the corpus ·
ask a normal question, watch the retrieved document hijack the answer ·
markdown: nobody attacked the system, the attack was in the data ·
defence 1 delimiters and instruction/data separation · defence 2 input
validation and a retrieved-content sanitiser · defence 3 output validation
against allowed topics · re-run all four attacks, print a before/after
table · TODO their own fifth attack · honest markdown: some of these
still get through, that's the state of the art · reflection plus the
pre-launch checklist as a markdown table.

Prompt 10d — Verify every notebook actually runs

Before we link to these, verify they work. Do not skip this — these run
live in front of a camera.

json.load() every .ipynb and confirm valid nbformat 4. Report any
that fail.
Extract every code cell and check it parses as valid Python with
ast.parse(). Report syntax errors with file and cell number.
Check every import appears in that notebook's cell-1 pip install.
Flag any missing.
Check every function called is either defined earlier in the same
notebook, imported, or a builtin. Flag undefined references — this
catches cells that silently depend on something I deleted.
Confirm no notebook contains a hardcoded API key, and that every one
uses the userdata.get('GEMINI_API_KEY') pattern.
Confirm gemini-2.5-flash-lite and gemini-embedding-001 are the only
model strings used.
Confirm every notebook has both a reflection cell and an
"If this breaks" cell.
Confirm every # TODO cell has surrounding structure — flag any that
would leave a student staring at an empty cell.

Report findings as a list first, then fix them.

---



## Prompt 10 — Project page and notebooks page

> Build `project/index.html` and `notebooks/index.html`.
>
> `project/index.html`:
>
> - Hero: **The project** — "Build a generative AI assistant over documents
> you care about. Ship it to GitHub. Defend the architecture you chose."
> - The five required components as a checklist
> - **The rubric as a table**: 6 criteria, points, and what full marks looks
> like. Total 100, pass 60. Make this the most prominent thing on the
> page.
> - The SDAIA GitHub requirements as a copyable checklist, including the
> link to [https://github.com/SDAIAAcademy](https://github.com/SDAIAAcademy)
> - A timeline strip: Monday pitch → Tuesday build → Wednesday harden +
> README → Thursday present
> - A README template in a `<pre>` block with a **copy to clipboard** button
> - A note that the scaffold notebook is the starting point, with a Colab
> button
>
> `notebooks/index.html`:
>
> - A table of all six notebooks: number, name, which day, one-line
> description, and an **Open in Colab** button styled like the real Colab
> badge.
> - Read the URLs from `notebooks/notebooks.json` so I can paste in my Colab
> links after uploading, without touching HTML. Create that JSON with
> empty `colab_url` fields and a comment in the page telling me where to
> fill them in.
> - Each row also links to the raw `.ipynb` in the repo as a fallback.
> - Notebooks: `project_scaffold`, `day1_first_calls`, `day2_retrieval`,
> `day3_agents`, `day4_production`, `day5_redteam`.

---



## Prompt 11 — QA pass

> Full review pass. Do not add features — find and fix defects.
>
> 1. **Path check.** Every `href` and `src` in every file. Flag any leading
>   slash. This site is served from `/repo-name/` and absolute paths will
>    404 on GitHub Pages.
> 2. **Offline check.** Search every file for `http://` and `https://` in
>   `src` and `href`. The only external links allowed are ones the student
>    deliberately clicks (GitHub, Colab, AI Studio). No stylesheets, fonts,
>    or scripts may load from the network. List anything you find.
> 3. **Print check.** Open each deck's print stylesheet and verify: one
>   slide per page, no clipped content, notes included, dot strip and
>    buttons hidden, logos on each page. Fix what's broken.
> 4. **Store check.** Every activity actually calls `Store.saveScore()` with
>   a unique id, and the home page and activities hub both read the same
>    ids. Verify the totals add up.
> 5. **Keyboard check.** Every deck control and every activity control is
>   reachable by keyboard with a visible focus ring.
> 6. **Arabic check.** Every Arabic string is inside
>   `<span lang="ar" dir="rtl">` and doesn't break the surrounding LTR
>    line.
> 7. **Dead link check.** Every internal link resolves to a file that
>   exists.
> 8. **Contrast check.** Flag any text under 4.5:1 against its background,
>   especially teal on navy.
>
> Report what you found as a list before you fix anything, then fix it.

---



## Prompt 12 — README and deploy

> Write the top-level `README.md`:
>
> - What this is, who it's for, the dates
> - How to run it locally (`python3 -m http.server` and open localhost)
> - How to deploy: push to GitHub, Settings → Pages → deploy from `main`,
> root. Note that `.nojekyll` must stay.
> - The file structure with a one-line description per folder
> - A short section for me: how to add a slide, how to add an activity, how
> to fill in the Colab URLs in `notebooks/notebooks.json`
> - Credit line: SDAIA Academy, instructor Musa Ibn Rashid, August 2026
>
> Then create a `CHECKLIST.md` for me covering the morning of each day and   
> what will the content or flow of the day be.

---



## After the build

Things only you can do, in this order:

1. Upload the six notebooks to Colab, get share links, paste them into
  `notebooks/notebooks.json`.
2. Push to GitHub, enable Pages, confirm every page loads from the
  `/repo-name/` URL — this is where absolute paths break if any survived.
3. Open each deck on the actual projector at the actual resolution. Slide
  scaling is the thing that goes wrong on unfamiliar hardware.
4. Print Day 1 to PDF and read it on your iPad — that's your teaching
  fallback if the venue wifi dies.

