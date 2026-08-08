# Day 1 Lab — `day1_first_calls.ipynb`
### Line-by-line instructor walkthrough · Applied Generative AI · SDAIA Academy

> **How to read this file:** same convention as the slide notes — **bold = what is in the notebook, unpacked** · plain text = extra depth, gotchas, and answers to questions you'll get asked. Cells are numbered 1–21 as Colab counts them (1-indexed), which matches the troubleshooting table in the last cell.
>
> **Read the "Problems to fix before Sunday" section at the bottom first.** There are four things in here that will bite you in the room, one of them badly.

---

## The shape of the notebook

- **21 cells, four movements:** make a call (2–7) → control the output (8–14) → constrain it with a schema (15–18) → wrap it (19). Then reflection and troubleshooting.
- **Three TODO cells** — 5, 12, 17. Everything else is run-and-read. That ratio is deliberate for a mixed room: the non-coders can keep up, and the coders get the schema exercise in cell 17 which is genuinely open-ended.
- **Deck mapping:** cell 3 ↔ slide 15 (next-token), cells 6–7 ↔ slide 13 (Arabic), cells 8–10 ↔ slide 16 (temperature), cell 11 ↔ slide 20 (system vs user), cell 13 ↔ slide 14 (context window), cell 14 ↔ slide 24, cells 15–16 ↔ slides 25–26, cell 18 ↔ slide 27.

---

## Cell 1 — Setup

**`!pip install -q google-genai`**
- **The `!` sends the line to the shell rather than Python; `-q` keeps the projector readable.**
- The package is `google-genai` (the current unified SDK). The *old* one was `google-generativeai`. If someone has both installed, imports get confusing fast — this is the third most likely failure in the room. Fix is `!pip uninstall -y google-generativeai`.
- Colab will print a restart-runtime warning sometimes. It is safe to ignore for this package.

**`import os, json, time`**
- **Standard library only.** `json` is used in cells 16, 17 and 18; `time` only inside `ask()` for the backoff sleep. `os` is imported but never actually used — harmless.

**`from google import genai` / `from google.genai import types`**
- **`genai` gives you the `Client`. `types` gives you `GenerateContentConfig`** — every knob you turn today (temperature, system instruction, mime type, schema) goes inside that one config object.
- Worth saying out loud: the split exists because config objects are typed classes, not loose dicts. Your IDE can autocomplete them, and a typo raises immediately instead of being silently ignored.

**`try: from google.colab import userdata` … `API_KEY = userdata.get('GEMINI_API_KEY')`**
- **The key is read from Colab Secrets at runtime, never typed into a cell.** Say why: a notebook gets shared, screenshotted, and pushed to GitHub. A key pasted in a cell leaks all three ways.
- `userdata.get` raises if notebook access is toggled off for that secret — a separate failure from the secret not existing at all, and the one people miss because the secret *is* visibly there in the sidebar.

**`if not API_KEY: raise ValueError("empty")`**
- **Guards the case where the secret exists but is blank.** The `ValueError` is caught two lines later by the same `except`, so it just funnels into the friendly message. That's the intent — it isn't a bug.

**`except Exception: raise SystemExit(...)`**
- **Catches every failure path — not on Colab, secret missing, access off, blank value — and prints one six-step recovery message.**
- `SystemExit` in Colab stops the cell without killing the kernel or dumping a traceback. That's the reason for choosing it over a plain `raise`: what the student sees is the instructions, not a stack trace.
- The cost is that it swallows the real exception. If someone has a genuinely weird failure you'll want `except Exception as e:` and to print `e` while you debug at their desk.

**`client = genai.Client(api_key=API_KEY)`**
- **One client object, reused by every cell for the rest of the notebook.** It holds the credential and the HTTP session.
- This is why a kernel restart breaks everything downstream — `client` disappears. When someone says "it worked five minutes ago", the answer is almost always "run cell 1 again".

**`MODEL = "gemini-2.5-flash-lite"` / `EMBED_MODEL = "gemini-embedding-001"`**
- **Model name in one constant at the top** — the same discipline the `ask()` wrapper formalises in cell 19. One place to change it.
- **`EMBED_MODEL` is defined but never used today.** It's pre-seeded for Monday. Tell them that, or someone will hunt for where it's used and think they missed a cell.
- Flash-lite is chosen for speed and free-tier headroom with thirty people hitting it at once, not because it's the best model. Worth saying — otherwise they'll assume it's the recommended production choice.

---

## Cell 2 — The title markdown

**Frames the destination: `ask()` returning schema-validated JSON, in four steps.**
- Note this sits *after* the setup cell, so the notebook opens on code rather than a title. See the fix list at the bottom — worth swapping.

---

## Cell 3 — Your first call

**`resp = client.models.generate_content(model=MODEL, contents="Explain what a token is…")`**
- **Three arguments, one of which is the prompt. That is the entire API.** Land this: everything else all week is configuration around these three lines.
- `contents` accepts a plain string here, but it's really a list-of-messages parameter — the SDK is quietly wrapping your string into a single user turn. That matters on Tuesday when you start building multi-turn histories by hand.
- **No config object at all**, so the model's default temperature applies. Nobody notices, which is exactly the failure mode you called out on slide 16.

**`print(resp.text)`**
- **`.text` is a convenience accessor** that concatenates the text parts of the first candidate. If a response comes back with no text (blocked by a safety filter, or truncated at zero tokens) `.text` can be `None` and `print` shows `None` rather than raising. Rare here; worth knowing.

---

## Cell 4 — "What just happened" markdown

**Four steps: tokenise → predict next token → append and repeat → decode.**
- **The closing line — likely, not true — is the same sentence as slide 15.** Say it identically both times; the repetition is what makes it stick.
- Good moment to ask the room: "so where in those four steps does it check a fact?" The silence answers itself.

---

## Cell 5 — Reading the token counts

**`u = resp.usage_metadata`**
- **Every response carries its own bill.** Not an estimate, not a heuristic — the provider's own count of what you're charged for.

**`u.prompt_token_count` / `u.candidates_token_count` / `u.total_token_count`**
- **Input, output, and total.** "Candidates" is the API's word for generated responses — the model can return more than one candidate, though we ask for one.
- Input and output are priced at *different rates*, output being several times more expensive. That's why the split matters and why Wednesday's costing needs both numbers, not just the total.
- **Expect `total` not to equal `prompt + output` exactly.** The 2.5 family has an internal thinking budget, and thinking tokens show up in the total (and on the bill) while sitting in a separate field. If a student spots the arithmetic not adding up, that's the reason — `dir(resp.usage_metadata)`, as the comment suggests, will show the extra field.

**The `dir(resp.usage_metadata)` comment**
- **A deliberate teaching move: attribute names drift between SDK versions.** Rather than promising the names are stable, the notebook shows them how to look. Worth naming explicitly as a habit.

---

## Cell 6 — TODO: your own prompt

**`my_prompt = "TODO: write your own prompt here"`**
- **One line to change.** The instruction to use something from their real work is the important part — it makes the token number theirs, and it starts them thinking about their document set for tonight's homework.
- **`resp2` and not `resp`** — deliberately a new variable, so the earlier response stays intact. Point this out, because cell 15 later *does* overwrite `resp`, which is a real trap (see fix list).

**`print("in:", …prompt_token_count, "| out:", …candidates_token_count)`**
- Have two or three people call their numbers out. The spread across the room is the lesson — a one-line prompt and a paste-a-paragraph prompt differ by an order of magnitude, and both cost real money at volume.

---

## Cell 7 — Arabic vs English, measured

**`english = …` / `arabic = …` — the same sentence, both languages, pre-written.**
- Using a data-protection sentence rather than "hello world" is deliberate; it's the register their actual documents are written in.

**`client.models.count_tokens(model=MODEL, contents=…)`**
- **This is the real tokenizer, not the heuristic from the slide.** Say that explicitly — the live box on slide 13 approximates, this call is authoritative.
- **`count_tokens` doesn't generate anything, so it's free and instant.** That makes it the right tool for pre-flight checks: before you send a 50-page document, count it and compare against the window.

**`en.total_tokens` / `ar.total_tokens` and `len(english)` / `len(arabic)`**
- **Printing characters alongside tokens is the point of the cell.** Arabic uses *fewer characters* and *more tokens* — that pairing is what kills the "Arabic is just a longer language" explanation before it starts.

**`"%.1fx" % (ar.total_tokens / en.total_tokens)`**
- **The ratio is computed live rather than hard-coded**, so it stays honest if the tokenizer changes under you. Expect roughly 2×; don't promise a number in advance.

---

## Cell 8 — "Why Arabic costs more" markdown

**Tokenizers are trained mostly on English, so Arabic fragments; 2–3× on input and output, on every call, for the product's lifetime.**
- **The $18 → $45 figure is a forward reference to Wednesday.** Flag it as illustrative rather than quoted, unless you've priced it against current rates.
- If someone wants the deeper reason, it's the three-part answer from the slide notes: corpus under-representation, multi-byte UTF-8, and templatic morphology. Don't volunteer all three unless asked — one line here, depth on request.

---

## Cells 9 and 10 — Temperature 0.0, then 1.2

**`prompt = "Describe a data governance policy in one short sentence."` — defined in cell 9 and reused in cell 10.**
- **Cross-cell dependency.** Anyone who runs cell 10 alone gets a `NameError`. Cheap to mention once now and save three interruptions later.

**`for i in range(3):` … `config=types.GenerateContentConfig(temperature=0.0)`**
- **Three identical calls, the only variable being the sampler.** This is the first cell where a config object appears — point at it and say "everything you control lives in here".
- **At 0.0 the sampler always takes the top token, so the three lines should match.** *Should*, not *will*: batching and floating-point non-determinism mean you can occasionally get a variation even at zero. If that happens live, say so — it's a more honest lesson than pretending it's guaranteed.

**Cell 10, `temperature=1.2`**
- **Same loop, flatter distribution, visibly different sentences.**
- Risk to manage: on a short, factual, one-sentence prompt, flash-lite may produce three fairly similar outputs even at 1.2, and the demo lands weakly. Have a backup prompt ready — something with room to roam, e.g. "Write one sentence describing a data governance policy to a child." Run it live if the first result is flat.
- Anyone who asks about `top_p`: it's the other truncation dial, it clips the candidate list instead of reshaping probabilities, and you change one or the other, not both.

---

## Cell 11 — Reflection TODO

**Two questions: describe the difference, then pick a temperature for extracting a name and email.**
- **The second question is the assessable one** — the answer is 0.0, and the reasoning is "extraction has one right answer, so variation is pure loss".
- These are markdown cells, so nothing enforces an answer. If you want them filled in, say you'll read them while circulating — otherwise most rooms skip straight past.

---

## Cell 12 — System instruction, two personas

**`question = "An employee asks whether they can carry over 15 days of leave."` — held constant.**

**`for persona in [ "formal HR policy officer…", "friendly colleague over coffee…" ]:`**
- **The user message never changes; only the system instruction does.** That's the whole experiment, and the inline comment `← the only thing changing` is doing the teaching.

**`config=types.GenerateContentConfig(system_instruction=persona, temperature=0.3)`**
- **`system_instruction` is a config field, not part of `contents`** — and that separation *is* the security boundary from slide 20. Make the connection explicit: what you just typed as a keyword argument is the thing Thursday's attacks try to override.
- **`temperature=0.3` is low deliberately**, so the difference they see comes from the persona and not from sampling noise. Worth naming, or the experiment isn't controlled.
- Both personas specify a *length* as well as a tone ("one precise sentence", "two casual sentences"). That's the Format component from slide 21 sneaking in — point at it.

**`print("-" * 60)`**
- Separator between runs. Trivial, but it's the kind of small thing that makes output readable on a projector, and worth copying.

---

## Cell 13 — TODO: your own system instruction

**`my_system = "TODO: your system instruction here"` — one line.**
- **The brief is bullet points, under 50 words.** The instruction to be explicit is the lesson: "be brief" produces something around 80 words; "reply as 3 bullet points, maximum 50 words total, no introduction" produces 45.

**`print("Word count:", len(r.text.split()), "(target: under 50)")`**
- **A self-check built into the cell**, which is a nice pattern to point at: the notebook grades the prompt instead of the instructor doing it.
- `.split()` counts whitespace-separated chunks, so bullet markers and stray dashes inflate it slightly. Don't let anyone argue about 51.
- If someone lands well over target, that's the teaching moment: the model complied with the *tone* and ignored the *number*, because the number was buried. Move it to the last line of the instruction and re-run — recency helps.

---

## Cell 14 — Deliberately overflowing the context window

**`huge = "The quick brown fox…" * 400_000`**
- **Intent is right: let them see the failure once, in a safe place, so they recognise it in production.**
- **This cell as written is the biggest risk in the notebook — see the fix list at the bottom before you run it.** It builds an 18 MB string and tries to upload it, thirty times over, on conference wi-fi.

**`try: … except Exception as e: print(type(e).__name__, ":", str(e)[:300])`**
- **Catching and printing the exception *type* rather than letting it traceback** is the point — they should leave able to recognise the error class by name.
- **`str(e)[:300]` truncates** because API errors can dump a large payload echo. Small detail, saves the projector.

**`# This is why chunking exists tomorrow.`**
- **Same closing line as slide 14.** Land it the same way.

---

## Cell 15 — "The ceiling starts here" markdown

**Three shapes for the same request, then: you cannot write the `if`.**
- **Identical to slide 24**, deliberately. The notebook restates it because the labs get done out of order and some people will read this cold after lunch.
- **"The fix is a contract" is the hinge sentence of the whole day.** Everything before is preparation; everything after is the payoff.

---

## Cell 16 — JSON mode with a schema

**`message = """From: sara.alotaibi@example.gov.sa … form SDAIA-F-CRS-201-01-V1"""`**
- **A realistic message, with a real-looking form code and a deadline.** The realism is doing work: it contains the fields in *prose*, in a different order than the schema lists them, which is what makes the extraction non-trivial.

**`schema = { "type": "object", "properties": { … } }`**
- **Plain JSON Schema. Nothing Gemini-specific.** The same document you'd write for an OpenAPI spec. Say it — it's what makes the developers relax.

**`"name": {"type": "string"}` / `"email": {"type": "string"}`**
- **Free-form strings: you're constraining the *key* and the *type*, not the value.** The model can return anything as long as it's a string.
- Note what's absent: no `"format": "email"` validation. The schema will happily accept a malformed address. If they want that guarantee, it belongs in their code after parsing — which is the "check it" bullet from slide 17.

**`"intent": {"type": "string", "enum": ["question", "complaint", "request", "outage"]}`**
- **The highest-value line in the cell.** Four allowed strings, and the model *cannot* emit a fifth. The inline comment says it: not "quite urgent".
- Note this enum has four members where the slide had three — `outage` was added because the example message is an outage. Good design instinct to point at: the enum has to actually cover your domain, or the model gets forced into a wrong bucket. That's the argument for including an `"other"` member in real schemas.

**`"urgency": {"type": "string", "enum": ["low", "medium", "high"]}`**
- **Three values you can branch on, which is exactly what cell 17 does.** Contrast with the alternative: parsing "quite urgent", "fairly pressing", "ASAP" forever.

**`"required": ["name", "email", "intent", "urgency"]`**
- **Guarantees the keys exist, so `data["urgency"]` won't `KeyError`.** It does *not* guarantee the values are non-empty or correct — a required string can come back as `""`.

**`config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=schema, temperature=0.0)`**
- **`response_mime_type`** — no prose, no "Sure! Here's…", no ```json fence. **`response_schema`** — which JSON. **`temperature=0.0`** — extraction, so no creativity wanted.
- The mechanism, if you want the deeper answer: the schema is compiled into a state machine over the token vocabulary, and tokens that would break the schema are masked out *before* sampling. Invalid JSON is structurally impossible, not merely discouraged. That's what separates this from asking politely in a prompt.
- **`resp` is reassigned here**, overwriting the response from cell 3. Harmless if you run in order; confusing if someone jumps back to cell 5 afterwards and sees different token counts.

---

## Cell 17 — This is the moment

**`data = json.loads(resp.text)`**
- **One line, and the model's output becomes a Python dict.** Pause here. This is the slide-26 moment.

**`if data["urgency"] == "high": … elif data["intent"] == "complaint": … else: …`**
- **Ordinary Python, branching on values you defined.** No regex, no substring search, no "if the answer contains the word urgent".
- **The `if` doesn't know an LLM was involved** — that's the sentence to say. Everything downstream (tests, logging, type checking, code review) works normally again.
- Point at the order of the branches: urgency is checked before intent, so a high-urgency complaint pages the duty officer rather than opening a ticket. That's a *business rule*, expressed in code where it belongs, not buried in a prompt.

**The closing comment block**
- **"The rest of your system does not need to know an LLM was involved."** Same line as the slide. Repeat it verbatim.

---

## Cell 18 — TODO: your own schema

**`my_text = """Ticket 4471: … Reported by Ahmed Al-Qahtani. Not urgent, but it has happened three times this month."""`**
- **A different domain from cell 16, so they can't copy the schema across.** The text contains a ticket number, a system, a department, a reporter, an urgency signal, and a frequency — at least six extractable fields, which is a generous target for "at least three".

**`my_schema = { "type": "object", "properties": { # ← TODO (2 lines) }, "required": [] }`**
- **The brief: at least three fields, at least one using `enum`.** The enum requirement is the real exercise — anyone can name a string field; choosing the allowed value set forces them to think about what their downstream code will branch on.
- **`"required": []` must be filled in too.** The comment says so but it's easy to miss, and leaving it empty means the model may omit fields — which is a *good* accidental lesson if it happens.
- **Warning: an empty `properties: {}` will error, not return `{}`.** A student who runs the cell before editing gets an API error rather than an empty result, and may think they've broken their key. Pre-empt it in one sentence before you release them.
- The interesting failures to look for while circulating: an enum whose values don't appear in the text at all (model picks the least-wrong one — a great illustration of why you need an `"other"` member), and a field like `"date"` where the text says "yesterday" (model may resolve it, may hallucinate a date — perfect illustration of "valid ≠ true").

---

## Cell 19 — The `ask()` wrapper

**`def ask(prompt, system=None, temperature=0.2, schema=None, tries=3):`**
- **Five parameters, four with defaults, so `ask("hello")` works.** Good API design worth naming: the common case is one argument.
- **`temperature=0.2` as the default** is a deliberate choice — biased toward reliable rather than creative, because most calls in a system are doing work rather than writing copy.

**`opts = {"temperature": temperature}` then `if system:` / `if schema:`**
- **Config built as a dict and only populated when the argument was given.** Compare with the slide version, which passed `system_instruction: system` unconditionally — the notebook's guarded version is the better one, and it's fine to say the deck simplified it for the projector.
- **The `if schema:` branch adds two keys together**, because they only make sense as a pair. Setting the mime type without a schema gives you JSON of unpredictable shape.

**`cfg = types.GenerateContentConfig(**opts)`**
- **`**opts` unpacks the dict into keyword arguments.** For the non-coders: the dict is a bag of settings, and the star-star tips it into the function. Because the class is typed, a misspelled key fails here, immediately, rather than being silently ignored — which is the argument for building it this way rather than passing a raw dict to the API.

**`for attempt in range(tries):` / `try:` / `return json.loads(r.text) if schema else r.text`**
- **One return statement handling both modes: parsed dict when a schema was given, raw text otherwise.** That conditional expression is the whole reason `ask()` is usable for both Monday's prose summaries and today's extraction.

**`except Exception as e:` / `if attempt == tries - 1: raise`**
- **On the last attempt, re-raise rather than returning something fake.** Say this out loud — the failure mode you're avoiding is a wrapper that swallows errors and returns `None`, which then propagates as a mystery three functions away.
- **Catching bare `Exception` is deliberately blunt**, same caveat as the slide: it retries a malformed request three times for no reason. Wednesday replaces it with retry-only-what's-retryable — 429 and 5xx yes, 400 and 401 no.

**`wait = 2 ** attempt` / `time.sleep(wait)`**
- **1s, 2s, 4s — exponential backoff**, and the reason is that a fixed-interval retry against a rate limit makes the limit worse for you and everyone sharing the quota.
- Production would add jitter (`2**attempt + random.random()`), otherwise every client that failed at the same instant retries at the same instant.

**`print(f"  attempt {attempt+1} failed ({type(e).__name__}), retrying in {wait}s")`**
- **Visible retries.** In a teaching notebook this is right — they see the mechanism work. In production it becomes a structured log line, not a print.

**`print(ask("Name three benefits of retrieval-augmented generation.", temperature=0.4))`**
- **Prose mode: no schema, returns a string.**

**`print(ask("Extract the fields.\n" + message, schema=schema))`**
- **Typed mode: returns a dict, and the whole day collapses into one line.**
- **This line depends on `message` and `schema` from cell 16.** Anyone who restarted the runtime, or who worked cell 18 heavily and lost track, gets a `NameError` here. Worth one sentence of warning.

---

## Cell 20 — Reflection

**Three questions: what surprised you, what a schema gives you that a prompt doesn't, and one thing at work that could use `ask()` with a schema.**
- **The third one is the valuable one** — it's the bridge to tonight's homework and to their project. Read these while circulating; the answers tell you who has a real use case and who is still browsing.
- The expected answer to question two: a prompt *requests* a shape, a schema *enforces* one at decode time. If someone writes "it makes the model more accurate", correct it gently — shape, not truth.

---

## Cell 21 — Troubleshooting table

**Three failures: `SystemExit` on cell 1 (key/secrets), `404` (model name), `JSONDecodeError` (parsed a response with no schema).**
- **The cell references are 1-indexed and consistent** — "cell 1" is the setup cell, "cell 16" is the schema cell. Don't renumber them.
- **The third row is the most instructive**: `json.loads` on prose fails immediately and loudly, which is the good version of the failure. The bad version is prose that *happens* to parse.
- Add a fourth row if you like, for the failure I'd bet on after the key: `NameError` from running cells out of order. The fix is Runtime → Run all, or just re-run from cell 1.

---

# Problems to fix before Sunday

**1 · Cell 14 will hurt you. Fix this one.**
`"The quick brown fox jumps over the lazy dog. " * 400_000` builds an **18 MB string** and tries to POST it. Thirty people doing that simultaneously is over half a gigabyte of uploads on room wi-fi, and what they'll get is a slow hang or a network-layer error rather than the clean context-window error you're teaching. Drop the multiplier to `20_000` (~900 KB, still far past the window) — or better, replace the whole thing with a `count_tokens` call on the big string, which makes the point *without* the upload:
```python
huge = "The quick brown fox jumps over the lazy dog. " * 20_000
print(client.models.count_tokens(model=MODEL, contents=huge).total_tokens, "tokens")
```
Then attempt the generate call on that smaller-but-still-oversized string to show the error.

**2 · The setup cell is above the title cell.**
The notebook opens on `!pip install` rather than on "Day 1 — From your first call to typed output". Move the markdown title to the top. Cosmetic, but it's the first thing thirty people see, and the cell-number references in the troubleshooting table shift by one if you do — so update "cell 1" → "cell 2" and "cell 16" → "cell 17" at the same time.

**3 · `resp` is reused across cells 3 and 16.**
Cell 16 overwrites the response object from cell 3, so re-running cell 5 afterwards shows the *schema* call's token counts. Rename the cell 16 response to `resp_json` and update cell 17's `json.loads(resp_json.text)`. One-word change, removes a genuinely confusing moment.

**4 · Cell 18 errors rather than returning empty if left unedited.**
An empty `properties: {}` isn't a valid response schema, so a student who hits Run-All before editing gets an API error and may think their key is broken. Either pre-empt it verbally, or seed one field in the properties dict as a worked example so the cell runs green out of the box and the TODO is "add two more".

**Minor, take or leave:** `os` is imported and never used; `EMBED_MODEL` is defined and never used today (say it's for Monday); and neither `ask()` nor any call sets `max_output_tokens`, which is the one config field a cost-conscious room will ask about — worth a sentence when you're on cell 19.
