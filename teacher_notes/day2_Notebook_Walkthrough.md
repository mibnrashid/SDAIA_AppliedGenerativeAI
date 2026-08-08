# Day 2 Lab — `day2_retrieval.ipynb`
### Line-by-line instructor walkthrough · Applied Generative AI · SDAIA Academy

> **How to read this file:** **bold = what is in the notebook, unpacked** · plain text = extra depth, gotchas, and answers to questions you'll get asked. Cells numbered 1–26 as Colab counts them.
>
> **Read "Fix list" at the bottom before Block 3.** There are six issues; two of them will stop the room dead — the placeholder repository URL in cell 2, and a BM25 tokenisation problem in cell 15 that can make the notebook's centrepiece demo fail.

---

## The shape of the notebook

- **26 cells. Part A is cells 1–12 (build the pipeline), Part B is 13–20 (make it good), Part C is 21–24 (measure it).** Only Part B has a markdown header; see fix list item 6.
- **Four TODOs: cell 6 (chunker loop body), cell 12 (three questions), cell 16 (the alpha line), cell 22 (golden set).** The rest is pre-written and meant to be read.
- **Deck mapping:** cell 3 ↔ slide 12 · cells 4–5 ↔ slides 13–14 · cells 6–7 ↔ slides 15–17 · cell 8 ↔ slides 18–19 · cell 10 ↔ slide 20 · cells 13–14 ↔ slide 22 · cells 15–17 ↔ slides 23–24 · cells 18–19 ↔ slide 25 · cell 20 ↔ slide 26 · cells 21–24 ↔ slides 28–29.
- **Note the ordering choice throughout Part B: failure first, then fix.** Cell 14 fails, cell 15 shows why, cells 16–17 fix it. Same in Part C: score the naive retriever alone before the comparison. Point this out once — it's a teaching pattern they can copy.

---

## Cell 1 — Setup

**`!pip install -q google-genai chromadb rank-bm25 numpy`**
- **Four packages instead of Sunday's one.** `chromadb` is the slow one — expect 30–60 seconds, and warn them so nobody re-runs it thinking it hung.
- `rank-bm25` is a tiny pure-Python package. `numpy` is already in Colab; listing it is harmless documentation of the dependency.

**Imports, key retrieval from Colab Secrets, `SystemExit` with six-step recovery**
- **Identical to Sunday's cell 1.** Say so — recognition is reassuring on the hardest day of the week, and it means anyone who solved the key problem on Sunday already knows the fix.

**`MODEL = "gemini-2.5-flash-lite"` / `EMBED_MODEL = "gemini-embedding-001"`**
- **`EMBED_MODEL` was defined and unused on Sunday; today it earns its place.** Nice callback if you made that promise then.
- Two different models doing two different jobs is worth naming: one turns text into meaning-coordinates, one turns a prompt into text. They are not interchangeable and neither can do the other's job.

---

## Cell 2 — The document set

**`RAW_BASE = "https://raw.githubusercontent.com/YOUR-ACCOUNT/YOUR-REPO/main/notebooks/data"`**
- ⚠️ **Placeholder. This must be replaced with your real repository URL or nothing downloads.** Fix list item 1 — this is the single highest-priority thing in the file.

**`FILES = [...]` — 15 documents: 11 English, 4 Arabic (`09`–`12`), covering leave, training, data governance, security, procurement, remote work, AI ethics, records, conduct, IT support, meeting rooms.**
- **The corpus is designed, not arbitrary.** Multiple documents mention training and multiple mention leave, so vector search has genuine near-misses to make. The Arabic files are what make cross-language retrieval demonstrable. Say that when someone asks why fifteen.

**`os.makedirs("data", exist_ok=True)` / `for name in FILES + ["scan_p03.png"]:`**
- **The scanned page rides along with the text files** and is filtered out later by the `.txt` check in cell 3.

**`if not os.path.exists("data/" + name): !wget -q -O data/{name} {RAW_BASE}/{name}`**
- **The existence check makes re-running cheap** — nothing re-downloads.
- **`{name}` and `{RAW_BASE}` in a `!` line is Colab's variable interpolation into the shell.** Worth one sentence for the non-coders: the `!` runs a shell command, and the braces let Python values into it.
- ⚠️ **`-q -O` is a silent-failure combination.** On a 404, wget writes the error page (or an empty file) to the destination and says nothing. The next cell then loads empty documents and everything downstream "works" with a corpus of nothing. See fix list item 2.

**`print("Downloaded:", len(os.listdir("data")), "files")`**
- **Counts files, not bytes** — so it prints 16 whether the download worked or not. Don't let this reassure you.

---

## Cell 3 — Load and clean

**`def load_documents(folder="data"):` … `for name in sorted(os.listdir(folder)):`**
- **`sorted()` makes the corpus order deterministic**, which matters more than it looks: chunk IDs, the BM25 index, the vector matrix, and the Chroma collection all depend on the same ordering. Any of them built from a different order and scores get attached to the wrong chunks with no error.

**`if not name.endswith(".txt"): continue`**
- **Skips `scan_p03.png`.** The scanned page joins the corpus in cell 5 instead, by a different route.

**`open(..., encoding="utf-8")`**
- **Explicit UTF-8, not the platform default.** With four Arabic files this is not optional — a default-encoding read on the wrong platform gives you mojibake that looks like data and searches like noise. This is slide 12's "fix the encoding first", in one keyword argument.

**`lines = [ln.rstrip() for ln in raw.split("\n")]` / `cleaned = "\n".join(lines)`**
- **Strips trailing whitespace from every line.** Trailing spaces are invisible and they break the blank-line detection the chunker depends on — a line of `"   "` is not `""`, so `\n\n` never matches and paragraph splitting silently fails.

**`while "\n\n\n" in cleaned: cleaned = cleaned.replace("\n\n\n", "\n\n")`**
- **Collapses runs of blank lines down to exactly one.** The `while` handles arbitrarily long runs; a single `.replace()` would leave `\n\n\n\n\n` as `\n\n\n`.
- **This is the line the chunker depends on.** Cell 6 splits on `"\n\n"` — without normalisation, a five-blank-line gap produces empty paragraphs, and the `if p.strip()` filter is what catches them. Two independent guards for one problem; point that out as defensive habit.

**`docs.append({"text": ..., "source": name, "page": 1})`**
- **The dictionary shape that everything downstream assumes: `text`, `source`, `page`.** Every subsequent stage preserves those three keys. **`page: 1` is a placeholder because these are plain text files** — for a real PDF corpus, page is the number that makes a citation actually checkable.
- **This is slide 12's argument, made concrete.** Metadata is attached at the very first step because retrofitting it means re-processing everything, including re-running the vision model over every scan.

**`print(docs[0]["text"][:300])`**
- **Prints the first document so they can see the corpus is real.** If this prints nothing or prints HTML, the download failed — that's your fast diagnostic for the cell 2 problem.

---

## Cell 4 — Multimodal ingestion markdown

**"A photograph of a page. It has no text layer. Open it with any text tool and you get an empty string."**
- **Same framing as slide 13.** The line to repeat verbatim: half the Arabic PDFs in a government archive look like this.
- **"Nothing downstream will know the difference — and that is what makes it a pipeline stage rather than a demo."** That distinction is the whole point of the next cell.

---

## Cell 5 — Vision extraction

**`page_bytes = pathlib.Path("data/scan_p03.png").read_bytes()`**
- **Raw bytes.** The SDK wants bytes plus a MIME type, not a PIL image or a file path.

**`VISION_PROMPT` — four instructions: transcribe exactly, keep Arabic in Arabic, keep table rows on separate lines, do not summarise / explain / add commentary.**
- **"Do not summarise, do not explain, do not add commentary" is three negations doing three different jobs.** Summarising loses detail; explaining adds the model's interpretation as if it were on the page; commentary adds "Here is the transcription:" which then gets chunked and embedded as if it were policy text. All three are real, all three are the model being helpful.
- **"Keep any Arabic text in Arabic"** guards a failure you'd never catch: asked in English, a vision model will sometimes translate as it transcribes. The chunk then embeds fine, reads fine, and can never be found by an Arabic query.
- This is slide 21 of Day 1 applied — the Format component of a prompt, on a task where format means "exactly what was on the paper".

**`contents=[types.Part.from_bytes(data=page_bytes, mime_type="image/png"), VISION_PROMPT]`**
- **Multimodal input is a list with mixed element types.** Image first, instruction second. That's the entire API surface, and it's less exotic than they expect.
- Instruction last means it sits nearest the generation — the same recency argument from Day 1's prompt anatomy.

**`print(vresp.text)`**
- **Watch the room here.** This is the moment on the slide notes worth waiting for: Arabic comes back as Arabic, off a photograph, in about two seconds.
- Say the caveat while they're impressed, not after: **a vision model can mis-transcribe a digit and does so fluently.** No confidence score, no flagged region — just wrong text that reads correctly. For anything financial or legal, a human checks the page. Classical OCR gives you per-character confidence; this doesn't. That's a genuine trade, not a disclaimer.

**`docs.append({"text": vresp.text, "source": "circular_2024_scan.pdf", "page": 3})`**
- **The payoff line, and the comment says it: same shape as every other document.** One `append` and a photograph is a first-class member of the corpus. Everything after this — chunking, embedding, retrieval, citation — treats it identically.
- **Note `page: 3` rather than `1`** — it's page three of a real circular, so the citation will actually point somewhere. Small detail, right instinct.

**`print("Corpus is now", len(docs), "documents.")`**
- Should read 16. If it reads 1, cell 2 failed and only the vision page loaded.

---

## Cell 6 — TODO: the chunker

**`def chunk(text, size=500, overlap=50):`** — size and overlap both in tokens, converted to characters with `* 4`.

**`paras = [p.strip() for p in text.split("\n\n") if p.strip()]`**
- **Paragraphs first. Structure before size** — slide 15's third column, in one line. The `if p.strip()` drops empties.

**`chunks, current = [], ""`** — accumulator and the chunk being built.

**`if len(current) + len(para) < size * 4:` → `current += para + "\n\n"`**
- **"Room left? Keep filling."** The `* 4` is Day 1's four-characters-per-token heuristic, used to avoid a tokenizer call per paragraph.
- Worth saying in this room: **that ratio is calibrated on English. Arabic is closer to 2 characters per token, so the same code produces roughly half-size chunks on the four Arabic files.** Cell 7 measures exactly this — see below.

**`else:` → the TODO, two lines:**
1. **append the finished chunk, stripped, to `chunks`**
2. **restart `current` from the last `overlap * 4` characters of the finished chunk, then add this paragraph**

The expected answer:
```python
chunks.append(current.strip())
current = current[-overlap * 4:] + para + "\n\n"
```
- **Take the slice from `current` *before* reassigning it** — that's the ordering people get wrong. Assign first and you carry the tail of the new chunk, which is the paragraph you just added.
- ⚠️ **The `pass` placeholder is a silent-failure trap.** If a student runs the cell before filling it in, the full chunk is never appended and the paragraph is never added — the paragraph is simply *dropped*, `current` keeps growing, and the cell prints a plausible chunk count. Nothing errors. Tell the room before you release them: if your chunk count looks suspiciously low, you haven't filled in the TODO. See fix list item 3.
- ⚠️ **Two edge cases their correct answer still won't handle**, and it's worth deciding whether to raise them: a paragraph longer than `size * 4` is never split (it becomes one oversized chunk), and if the *first* paragraph is oversized, `current` is `""` so an empty string gets appended as chunk zero. Both fire on real policy PDFs. Fix list item 4 has the patch and the argument for leaving it in as an exercise.

**`if current.strip(): chunks.append(current.strip())`**
- **Flushes the final partial chunk.** Easy to forget, and forgetting it silently loses the tail of every document — which in a policy corpus is often the appendix everyone asks about.

**`records = [{"text": ch, "source": d["source"], "page": d["page"]} for d in docs for ch in chunk(d["text"])]`**
- **The comprehension where metadata survives into every chunk.** Read the two `for` clauses left to right: for each document, for each chunk of it. That order confuses people who expect nesting to read like nested loops written vertically — it does, it's just flattened.
- **This list is the spine of the rest of the notebook.** `records` order defines the vector matrix order, the BM25 index order, and the Chroma IDs. Say that now, because cells 8, 9, 15 and 16 all silently depend on it.

---

## Cell 7 — Inspect three chunks

**`for r in records[:3]:` printing source, page, character count, and the first 400 characters**
- **"A chunk is retrieved ALONE"** is the sentence that justifies the whole cell. They're not checking the text is present; they're checking each chunk *means something by itself*.
- **Make them actually do this.** The habit — print three chunks immediately after writing a chunker — generalises to every pipeline they build, and it's the fastest way to catch a broken split.
- What to look for, in order: cut mid-word (overlap slice landed inside a word — cosmetic), a chunk with no heading (slide 16's failure — serious), and a chunk that is one line long or three pages long (the edge cases above).

**`print("Arabic prints right-to-left in the output; that is the terminal doing its job, not your data being broken.")`**
- **This comment prevents a panic.** Somebody will see reversed-looking output and conclude the encoding broke. Bidi rendering in a browser output cell is display-only; the bytes are in logical order.
- **"Check `len()` rather than trusting your eye"** is the right instruction, and it generalises: for RTL text, verify programmatically, never visually.

**`arabic_chunks = [r for r in records if r["source"].endswith("_ar.txt")]` and the average character count**
- **This is the cell that proves the tokenisation point empirically.** Compare the Arabic average against the English chunks and you should see Arabic chunks running noticeably shorter in characters — because the `* 4` heuristic assumes English density.
- **Worth two minutes if you have them:** ask the room why. The answer chains all the way back to Day 1 slide 13. This is the throughline moment of the morning.

---

## Cell 8 — Embed every chunk

**`def embed(texts, task="RETRIEVAL_DOCUMENT", batch=32, pause=1.0):`**
- **One function for both documents and queries; the task type is the switch, and it's a default argument so the common case is clean.**
- **The docstring carries the whole lesson: `RETRIEVAL_DOCUMENT` for chunks, `RETRIEVAL_QUERY` for questions, and using the wrong one quietly costs accuracy.** Emphasise *quietly* — nothing errors, results just get worse in a way you can't see.
- The mechanism, if asked: a question and a passage are projected slightly differently, because a good question isn't supposed to *look like* its answer, it's supposed to *find* it. Mixing the task types collapses that asymmetry.

**`for i in range(0, len(texts), batch):` / `contents=texts[i:i + batch]`**
- **Batching, because the free tier rate-limits.** ⚠️ Verify 32 works on a free-tier key this morning — fix list item 5.

**`out += [e.values for e in r.embeddings]`**
- **One embedding object per input; `.values` is the float list.** **Order is preserved, and the entire notebook depends on that.** `vectors[i]` must correspond to `records[i]` or every score lands on the wrong chunk.

**`print(f"  embedded {min(i + batch, len(texts))}/{len(texts)}")`**
- **A progress line, because this cell takes a while and silence looks like a hang.** The `min()` stops the last batch reporting more than the total.
- Note this also fires for single-query embeds in cell 10, printing "embedded 1/1" on every search. Cosmetic noise; mention it so nobody thinks something is looping.

**`time.sleep(pause)` — "do not remove this line"**
- **The comment is there because someone will remove it.** It looks like waste; it is the difference between finishing and getting 429s for ten minutes.
- Connect it to Day 1: `ask()` had exponential backoff, which is *reactive*. This is *preventive*. Production wants both — throttle on the way out, back off on the way back.
- **`pause` is a parameter, which is why cell 10 can pass `pause=0`** for single-query embeds where throttling is pointless.

**`vectors = embed([r["text"] for r in records])` / `print(len(vectors), "vectors of", len(vectors[0]), "dimensions")`**
- **Should print 3072 dimensions.** Worth one line: that's 3072 floats per chunk, which is why storage is a real cost at scale, and why the model supports truncating to 1536 or 768 with modest quality loss.

---

## Cell 9 — Store in Chroma

**`db = chromadb.Client()`**
- **In-memory. Zero setup, dies with the kernel.** That's the right choice for teaching and the reason a runtime restart costs them the whole morning's indexing — worth saying out loud before anyone restarts.

**`try: db.delete_collection("policies") … except Exception: pass`**
- **The guard, and the comment names it as the second most common failure of the day.** Delete-then-create is idempotent; `get_or_create` plus `add` would silently double the collection instead.
- **"Run the whole cell, not just part of it"** from the troubleshooting table is the operative instruction — someone will select just the `col.add(...)` block and re-run it.

**`col = db.create_collection("policies")`**
- **`create`, not `get_or_create`** — deliberate, because it makes a duplicate attempt fail loudly rather than quietly append.

**`col.add(ids=[f"c{i}" ...], documents=..., embeddings=vectors, metadatas=[{"source": ..., "page": ...}])`**
- **Four parallel lists, all indexed identically to `records`.** This is where the ordering invariant finally gets locked in.
- **`embeddings=vectors` means Chroma does not embed anything itself** — we pass pre-computed vectors. Worth saying, because Chroma *can* embed for you with a default model, and if anyone copies this pattern elsewhere they need to know which side owns embedding.
- **`metadatas` is slide 12's payoff.** The `source` and `page` carried from ingestion land in the database, and cell 11 pulls them straight back out into a citation.

**`print("Stored", col.count(), "chunks.")`**
- Should match `len(records)`. A mismatch means duplicate IDs were silently merged.

---

## Cell 10 — `search(query, k)`

**`qv = embed([query], task="RETRIEVAL_QUERY", pause=0)[0]`**
- **The query task type, paired with the document one from cell 8.** Point at the pair explicitly — this is the only place in the notebook where both appear within two cells of each other.
- **`pause=0`** because there's no batch to throttle.

**`res = col.query(query_embeddings=[qv], n_results=k)`**
- **`n_results` is the k from slide 20.** Default here is 4 — inside the 3–5 working range.
- Chroma returns a nested structure — `res["documents"]` is a *list of result lists*, one per query embedding. Hence `[0]` everywhere. That indexing confuses people; name it once.

**`for text, meta in zip(res["documents"][0], res["metadatas"][0]):`**
- **`zip` walks the two parallel lists together** and rebuilds the `{text, source, page}` dict shape. **Same shape as `records`**, which is what lets `search`, `hybrid_search` and `reranked_search` be passed interchangeably to `evaluate()` in cell 23. That interface consistency is a deliberate design choice worth pointing at.

**The demo query, "How many leave days does grade 11 get?"**
- **This is the question from slide 16.** It should retrieve the leave policy chunk with the heading attached. If it retrieves an orphaned table fragment, the chunker TODO was implemented without the heading surviving — a live illustration of the exact failure from the deck.

---

## Cell 11 — `answer(query)` with citations

**`GROUNDED` prompt template — four instructions in the system portion:**
- **"Answer using ONLY the reference material between the tags"** — scope restriction. This is what makes the answer groundable.
- **"Cite the source file and page for every fact"** — with a format example. The example is the important part; describing a citation format never works as well as showing one.
- **"If the material does not contain the answer, say you do not know."** **This is the most important line in the cell** and the one everybody omits. Without it the model falls back on training data and you get a fluent, uncited, unverifiable answer.
- **`<reference>` tags** — Day 1 slide 21's delimiters, and also the first line of Thursday's injection defence. Worth flagging the double duty.
- ⚠️ Minor: the example citation is `(leave_policy.txt p.1)` but actual filenames are `01_leave_policy_en.txt`. Fix list item 6 — the model will follow the example over the data and produce citations that don't match a real file.

**`context = "\n\n".join(f"[{h['source']} p.{h['page']}]\n{h['text']}" for h in hits)`**
- **Each chunk is prefixed with its own source label.** This is what makes per-fact citation possible — without the label inline, the model has no way to attribute one sentence to one chunk.
- **This line is slide 8's "step three is string concatenation".** Show it and say it: the entire "augment" stage of retrieval-augmented generation is this `join`. There is no magic.

**`config=types.GenerateContentConfig(temperature=0.1)`**
- **Low, because this is extraction-with-phrasing, not drafting.** Not 0.0 — a little room for natural sentence construction. Reasonable, and worth naming as a judgement call rather than a rule.

**The two demo calls**
- **First: a real question that should answer with citations.**
- **Second: "What is the capital of Brazil?" — should decline.** ⚠️ **Rehearse this one.** The model knows the answer perfectly well from training, and whether it refuses depends entirely on the strength of that one prompt line. If it answers "Brasília" in front of the room, don't hide it — that's a *better* lesson: grounding is a prompt instruction, not a hard constraint, and it's exactly the kind of thing Thursday attacks. Have the recovery line ready either way.

---

## Cell 12 — TODO: three questions of your own

**`my_questions = ["TODO: your first question", ...]`**
- **They use the provided corpus for now and point it at their own documents on Wednesday.** Say that — otherwise someone tries to load their own PDFs at 11:45 and loses the block.
- **"Write questions a real colleague would actually type"** is the same discipline as the golden set, rehearsed early. Good design.

**The closing comment: "was the retrieved chunk the right chunk? If not, was it a chunking problem or a retrieval problem?"**
- **That distinction is the diagnostic skill of the whole day, and it's the bridge into Part B.** Spell out how to tell them apart: if the right text isn't in *any* chunk in a usable form, it's chunking. If the right chunk exists but didn't come back, it's retrieval. Chunking is fixed by re-indexing; retrieval is fixed by hybrid, re-ranking, or rewriting.
- **This is the cell to circulate on.** Their three questions tell you who understood the corpus and who is typing filler.

---

## Cell 13 — Part B markdown

**"Embeddings encode meaning. So what happens when the query has no meaning to encode?"**
- **The rhetorical setup for slide 22.** `SDAIA-F-CRS-201-01-V1` is not a concept, it's a string of characters, and its embedding lands somewhere close to arbitrary.
- **"This is what a professional user types."** That's the line that makes the room go quiet — it reframes an edge case as the expert case.

---

## Cell 14 — Watch vector search fail

**`QUERY_ID = "SDAIA-F-CRS-201-01-V1"`** — one constant, reused in cells 15, 17 and 22. Good hygiene; also means a typo here breaks four cells.

**`contains = QUERY_ID in hit["text"]`**
- **A boolean per hit, printed alongside the source.** Turning the failure into `False, False, False, False` is far more convincing than reading four irrelevant chunks and asserting they're wrong.
- **This is the notebook's best piece of instructional design.** The failure is *measured*, not described. Point that out to them as a technique.

**`print("The document that IS this form is:", "02_training_policy_en.txt")`**
- **Hardcoded, so it depends on the corpus content.** Verify it's true of your actual data files before Monday — if the ID lives in a different file, this line teaches the wrong thing with total confidence.

---

## Cell 15 — BM25

**`tokenised = [r["text"].lower().split() for r in records]`**
- **Lowercase, then whitespace-split. Same chunks, same order as the vector index** — that invariant again.
- ⚠️ **This is the cell most likely to break the demo.** `.split()` keeps punctuation attached to tokens. If the corpus writes the identifier as `SDAIA-F-CRS-201-01-V1.` at the end of a sentence, or `(SDAIA-F-CRS-201-01-V1)`, the token is `"sdaia-f-crs-201-01-v1."` and the query token is `"sdaia-f-crs-201-01-v1"` — **no match, and hybrid search fails exactly where it's supposed to triumph.** Fix list item 2 has the one-line fix. Test it this morning.
- Beyond the demo: `.split()` also means no stemming ("policies" won't match "policy"), and **for the four Arabic files it means attached prefixes and clitics make الموظف and للموظف different tokens.** Worth one honest sentence — this is the teaching version; real Arabic BM25 wants a light stemmer.

**`bm25 = BM25Okapi(tokenised)`**
- **Built once, over the whole corpus.** BM25 needs global statistics — how rare each term is across all documents — which is why it's constructed from everything rather than scored pairwise.
- The intuition worth thirty seconds: BM25 weights *rare* terms heavily and common terms near zero, and normalises for chunk length. That's precisely why it nails identifiers — a form number is maximally rare, so a chunk containing it gets an overwhelming score.

**`scores = bm25.get_scores(QUERY_ID.lower().split())` / `top = np.argsort(scores)[::-1][:3]`**
- **`argsort` ascending, reverse, take three.** This three-slice idiom recurs in cell 16; slow down for the non-coders the first time.

**The printed table with `contains id: True`**
- **The mirror image of cell 14.** Two cells, the same query, opposite outcomes. That contrast *is* the argument for hybrid — you don't have to make it in prose.

---

## Cell 16 — TODO: `hybrid_search()`

**`def norm(x): spread = np.ptp(x); return (x - x.min()) / (spread + 1e-9)`**
- **Min-max squash to 0..1 so two different score scales can be added.** BM25 is unbounded and can be 40; cosine sits in roughly 0 to 1. Add them raw and BM25 drowns the vector entirely.
- **`+ 1e-9`** guards division by zero when every score is identical — which happens when a query matches nothing at all in BM25.
- ⚠️ Conceptual gotcha worth raising with a sharp room: **min-max is *relative*.** The best result always scores exactly 1.0 whether it's a perfect match or garbage, and the worst always scores 0.0. The combined score tells you which chunk is best *among these*; it never tells you whether any of them are good. That's why "I don't know" needs a separate mechanism, not a score threshold on this number.

**`DOC_MATRIX = np.array(vectors, dtype=float)`**
- **Cached once so hybrid search isn't slow.** Shape is (n_chunks, 3072). Building it per query would be the difference between milliseconds and seconds.

**`def vector_scores(query):` → `dots = DOC_MATRIX @ qv` → `dots / (norms * norm(qv) + 1e-9)`**
- **`@` is matrix multiplication — every chunk's dot product with the query, in one operation.** For the non-coders: this computes 400-odd similarities in a single line, which is why numpy exists.
- **Dividing by the norms turns dot product into cosine similarity** — the angle between the vectors, ignoring their lengths. That's the "near each other" from slide 18, spelled out arithmetically.
- ⚠️ Subtle and worth knowing: **Chroma's default distance metric is L2, not cosine.** So `search()` (cell 10, via Chroma) and `hybrid_search(alpha=1.0)` (here, cosine) are not guaranteed to rank identically. If the embeddings are unit-normalised the two orderings coincide and nobody notices; if they aren't, the comparison table in cell 24 is comparing slightly different things. Check `np.linalg.norm(DOC_MATRIX, axis=1)` this morning — if it's all ~1.0, you're fine and can ignore this.

**`kw = norm(bm25.get_scores(query.lower().split()))` / `vec = norm(vector_scores(query))`**
- **Both normalised, both in the same order as `records`.**

**The TODO — one line:**
```python
score = alpha * vec + (1 - alpha) * kw
```
- **`alpha=1.0` is pure vector; `alpha=0.0` is pure keyword.** Have them sanity-check both extremes before trusting the middle — it's a thirty-second test that catches an inverted weighting.
- **`score = None` is the placeholder, and `np.argsort(None)` raises.** Good design: this TODO fails loudly, unlike cell 6's.
- Read the line as what it is — a weighted average — and say that the entire "hybrid retrieval" concept is this one arithmetic expression. Demystifying it is worth more than the code.

**`top = np.argsort(score)[::-1][:k]` / `return [records[i] for i in top]`**
- **Returns `records` entries, so the shape matches `search()`** and both can be handed to `evaluate()`.

---

## Cell 17 — Watch it succeed

**Re-run `QUERY_ID` through `hybrid_search`, print `contains the id` per hit.**
- **Wait for this.** The slide notes say don't move on until the room sees it, and they're right — `False False False False` becoming `True` at rank one is the emotional payoff of the entire afternoon.
- **"Same query, same chunks, same embeddings. One weighted average."** Read that closing line aloud. It's the correct proportion: a large win from a small, comprehensible change.
- If it *doesn't* succeed, the cause is almost certainly the tokenisation issue from cell 15. Have the fix pasteable.

---

## Cell 18 — Re-ranking markdown

**Three steps: hybrid returns 20 → something expensive scores each 0–10 → keep the best 4.**
- **"Recall comes from the cheap wide net; precision comes from the expensive judge; the prompt stays small so generation stays cheap."** Three clauses, three benefits, one pattern.
- **"Yes — this is the k = 20 I warned you about."** The notebook pre-empts the contradiction, same as slide 25. Say it anyway, out loud.
- The mechanism worth one sentence if you have time: retrieval uses a *bi-encoder* (question and chunk embedded separately, so chunks can be indexed in advance); re-ranking uses a *cross-encoder* (reads both together, far more accurate, can't be precomputed). That's the whole speed/quality trade and why two stages exist.

---

## Cell 19 — LLM-as-reranker

**`RERANK_SCHEMA = {"type": "object", "properties": {"scores": {"type": "array", "items": {"type": "integer"}}}, "required": ["scores"]}`**
- **Day 1's schema, doing real work on Day 2.** Call that out explicitly — this is the first time a schema appears as *infrastructure* rather than a lesson. Without it you'd be regex-parsing "Passage 3: 7/10" out of prose.
- **`"items": {"type": "integer"}`** — an array of ints, nothing else possible.

**`listing = "\n\n".join(f"[{i}] {c['text'][:400]}" for i, c in enumerate(candidates))`**
- **Numbered passages, truncated to 400 characters each.** The truncation keeps the judging prompt affordable — 20 × 400 chars instead of 20 × 2000.
- ⚠️ The cost: **the judge only sees the first 400 characters.** A chunk whose answer sits in its second half gets scored on its opening. That's a real quality ceiling, and a fair question if someone asks why re-ranking didn't help as much as expected.

**`contents=(f"Question: {query}\n\nScore each passage 0-10 ... in order.\n\n{listing}")`**
- **"in order" is doing critical work** — the schema guarantees an array of integers, not that the array aligns with the passages. Alignment is a prompt instruction, not a constraint.

**`temperature=0.0`** — **judging is extraction, so the ranking is stable between runs.** Without it, running `evaluate()` twice gives you two different tables, which would undermine the entire measurement exercise.

**`scores = json.loads(r.text)["scores"]`**
- **One call, one parse, twenty scores.** Contrast with the naive design — twenty separate calls — and it's twenty times cheaper and twenty times faster.

**`ranked = sorted(zip(scores, candidates), key=lambda p: p[0], reverse=True)`**
- ⚠️ **`zip` truncates to the shorter list.** If the model returns 18 scores for 20 passages, two candidates are silently dropped and no error appears. Worth a defensive `assert len(scores) == len(candidates)` if you want to be safe; worth mentioning either way, because it's the kind of silent failure this whole course is about.
- Also note `sorted` is stable, so ties keep hybrid-search order — which means when the judge can't distinguish, you fall back on the retriever's opinion. Sensible default, worth naming.

**`def reranked_search(query, k=4): wide = hybrid_search(query, k=20); return rerank(query, wide, keep=k)`**
- **Two lines, and the comments say it: cheap and wide, then expensive and narrow.** Same signature as `search` and `hybrid_search`, which is what makes cell 24's comparison possible.
- **Cost note for Wednesday:** this adds one generation call per question, on top of the answer call. Doubling your per-question LLM calls to improve retrieval is usually the best trade in the pipeline — but it *is* a doubling, and they should know it.

---

## Cell 20 — Query rewriting

**`def rewrite(question, history=""):`** — history plus latest message in, standalone search query out.

**"Keep any identifiers or numbers exactly"**
- **The most important instruction in the prompt.** Without it, a rewriter will happily "clean up" `SDAIA-F-CRS-201-01-V1` into "the training request form" — and undo everything cells 15–17 just achieved.

**"Return only the query"** — no preamble, no explanation. Otherwise "Here is the rewritten query:" ends up as your search string.

**`temperature=0.0`** — rewriting, not drafting.

**The demo: "and what about carrying it over?" → "annual leave carry over grade 11" (or similar)**
- **This is the second question in every conversation** — the one where chat-over-documents systems quietly fall apart, because **the retriever has no memory.** The model sees history; the retriever sees only the string you hand it. That asymmetry surprises people who assume the pipeline *is* the chat.
- ⚠️ **Note `rewrite()` is demonstrated but never wired into `answer()` or into the evaluation.** That's a reasonable scope decision for the time available — say so explicitly, or a sharp participant will ask why the hit rate didn't change. The natural extension, if anyone finishes early: `answer(rewrite(q, history))`.

---

## Cell 21 — Golden set markdown

**Ten questions you already know the answers to, written *before* you tune.**
- **The four rules: real user questions not questions your system passes; include the awkward ones (identifier, acronym, Arabic); include one whose answer is not in the corpus; write them before you tune.**
- **"Or you are marking your own homework."** Let that land.
- The third rule is the one people skip and the one that catches a system which confidently answers everything. A retriever that always returns its four nearest chunks scores perfectly on a set with no negatives — and is dangerous.

---

## Cell 22 — TODO: fill in the golden set

**Three examples given: the grade-11 leave question, the identifier question, and a breach-reporting question.**
- **Note the shape of `must_contain`:** a phrase that must appear in the *retrieved text*, not the answer. `"30 working days"`, `"SDAIA-F-CRS-201-01-V1"`, `"twenty-four hours"`.
- ⚠️ **`must_contain` must be copied verbatim from the actual document.** If the file says "24 hours" and the golden entry says "twenty-four hours", the question fails forever regardless of how good retrieval is — and a participant will spend twenty minutes debugging a retriever that's working fine. **Say this before you release them:** open the document, find the sentence, copy the phrase.
- **The brief asks for five more, including one identifier question, one Arabic question, and one with no answer in the corpus.**
- ⚠️ The no-answer question doesn't fit this scoring function. `must_contain` measures whether text *was* retrieved; there's no phrase that proves an absence. Have an answer ready: either they write it and accept it always fails (which is honest and makes the point), or they check `answer(q)` manually for a refusal. Don't let it become a confusing dead end.
- Arabic `must_contain` needs care: `.lower()` in cell 23 does nothing for Arabic, so the match must be exact including any diacritics. Tell them to copy-paste rather than type.

---

## Cell 23 — `evaluate(search_fn)`

**`def evaluate(search_fn, k=4, verbose=False):`**
- **The retriever is an argument.** That's the design decision that makes the three-way comparison possible: three retrievers, one scorer, identical questions. Point at it as a pattern.

**`got = " ".join(r["text"] for r in search_fn(item["q"], k))`**
- **Concatenate everything retrieved into one string.** Which means position doesn't matter — a hit at rank 4 scores the same as rank 1.

**`ok = item["must_contain"].lower() in got.lower()` / `hits += ok`**
- **Substring containment, case-folded. `hits += ok` relies on `True` being `1`** — Pythonic, and worth explaining once for the non-coders.
- **Name the metric: this is recall@k.** Did the right text appear anywhere in the top k. It says nothing about ranking and nothing about answer quality.
- **The crudeness is deliberate, and you should defend it rather than apologise for it.** Retrieval is the part they can fix today, and a crude metric they will actually compute beats a sophisticated one they won't. MRR and nDCG are the next steps; mention, don't teach.

**`if verbose: print(("  PASS  " if ok else "  MISS  ") + item["q"][:60])`**
- **Per-question output, which is what makes the reflection cell answerable.** A single number tells you where you are; the PASS/MISS list tells you what to fix.

**`evaluate(search, verbose=True)`**
- **Naive vector search, scored alone, before the comparison.** Right order — establish the baseline, feel the misses, then show the improvement.

---

## Cell 24 — The comparison table

**`for name, fn in [("naive vector", search), ("hybrid", hybrid_search), ("hybrid + rerank", reranked_search)]:`**
- **Three retrievers, one loop.** All three share a signature, which is why this is three lines instead of thirty.
- **This cell is slow** — `reranked_search` fires a 20-candidate rerank call per golden question, so with 8–10 questions expect a noticeable wait. Warn them, or someone interrupts the kernel.

**`print(f"{name:<20} {rate * len(GOLDEN):>5.0f}/{len(GOLDEN)}  {rate:>5.0%}")`**
- **Reconstructs the hit count from the rate.** Format specifiers: `<20` left-pad, `>5.0f` right-align no decimals, `>5.0%` as a percentage.
- **"This table is what goes in your Thursday presentation."** Make them screenshot it. That instruction is the difference between a team that says "it seemed to work" and a team with a number.
- Manage expectations: with a hand-written golden set of 8–10 questions, the improvement may be one or two questions, not the 6→8→9 on the slide. **A small or even flat improvement is a legitimate result** and a better teaching moment than a clean win — it means their questions didn't stress the thing hybrid fixes. Have that framing ready.

---

## Cell 25 — Reflection

**Four questions: which retriever won and by how much; which golden questions still fail and what they have in common; is the remaining failure chunking, retrieval, or unanswerable; what would you change first.**
- **The third question is the one that matters** — it's the diagnostic skill from cell 12, now applied to measured failures instead of impressions.
- **The second is the analytical one**: failures usually cluster. All the Arabic questions, or all the ones needing two documents, or all the ones about the scanned page. Spotting the cluster is the skill.
- **Read these while circulating.** They tell you who has a mental model and who ran cells.

---

## Cell 26 — Troubleshooting

**Three rows: 429s while embedding (raise `pause` to 2.0), collection already exists (run the whole storage cell), Arabic looks scrambled (bidi rendering, check `len()`).**
- **All three are pre-empted elsewhere in the notebook**, which is good design — the table is a backstop, not the first line of defence.
- **Add a fourth row for today: empty or missing documents from cell 2.** Given the placeholder URL, that's more likely than any of these three. Symptom: `0 documents loaded`, or `docs[0]["text"]` printing HTML.

---

# Fix list — before Block 3

**1 · `RAW_BASE` in cell 2 is a placeholder.** `YOUR-ACCOUNT/YOUR-REPO` must be replaced with the real raw GitHub URL, and the fifteen text files plus `scan_p03.png` must actually be at that path. Nothing in the notebook works without it. Test from a fresh runtime, not your own — a cached `data/` folder will hide the problem.

**2 · BM25 tokenisation in cell 15 may break the centrepiece demo.** `.split()` leaves punctuation attached, so `SDAIA-F-CRS-201-01-V1.` at the end of a sentence never matches the query token. Check how the identifier is written in `02_training_policy_en.txt`, and if it's ever followed by punctuation, switch both the index and the query to:
```python
import re
def toks(s): return re.findall(r"[\w\-]+", s.lower())
tokenised = [toks(r["text"]) for r in records]
scores = bm25.get_scores(toks(QUERY_ID))
```
…and make the same change inside `hybrid_search`. Run cells 15 and 17 this morning and confirm you get `True`.

**3 · Cell 6's `pass` fails silently.** A student who runs it unedited loses every paragraph that would have started a new chunk, and gets a plausible-looking chunk count with no error. Either seed the TODO with a `raise NotImplementedError("fill in the TODO")` instead of `pass`, or announce it verbally: "if your chunk count looks low, you haven't written the TODO yet."

**4 · The chunker has two edge cases even when correctly implemented.** A paragraph longer than `size * 4` is never split, and an oversized *first* paragraph appends an empty chunk. Either patch it:
```python
else:
    if current.strip():
        chunks.append(current.strip())
        current = current[-overlap * 4:] + para + "\n\n"
    else:
        current = para + "\n\n"
```
…or leave it and turn cell 7 into the discovery: "print your chunk lengths, find the outlier, tell me why." The second is better teaching — but only if you know it's there.

**5 · Verify the embedding batch size.** Cell 8 sends 32 texts per `embed_content` call. Documentation for `gemini-embedding-001` on the Vertex path specifies a single input per request, and behaviour differs between the Vertex and Developer APIs. Run cell 8 against a free-tier key before the room does; the fallback is `batch=1` with the sleep, which is slower but works.

**6 · Two small ones.** The citation example in cell 11's prompt (`leave_policy.txt p.1`) doesn't match the real filenames (`01_leave_policy_en.txt`) — the model follows the example, so citations won't match a real file; change the example to a real filename. And Part A and Part C have no markdown headers, unlike Part B at cell 13 — worth adding two cells so the three-part structure from slide 31 is visible in the notebook itself.

**Also worth rehearsing:** the "What is the capital of Brazil?" refusal in cell 11 depends entirely on one prompt instruction, and the model does know the answer. Run it a few times. If it answers, that's a better lesson than a clean refusal — grounding is an instruction, not a constraint — but you want to choose that framing in advance rather than improvise it.
