# Applied Generative AI — 5-Day Delivery Plan (v2)
**SDAIA Academy, Riyadh · Sunday 2 – Thursday 6 August 2026 · Musa Ibn Rashid**

---

## 0. What changed from v1, and why

You pushed on three things. All three were right.

1. **The theory had a floor but no ceiling.** v1 built foundations and stayed
   there. The modality "tour" was passive — watching demos is not applied
   anything. **Fix:** every day now has an explicit **Floor → Climb →
   Ceiling** ladder, and the ceilings are real: structured output
   enforcement, hybrid retrieval with re-ranking, retrieval evaluation,
   agentic RAG, instrumented cost/latency measurement, scored adversarial
   testing. That is the material that earns the word "Applied."
2. **The labs were bullet points.** You can't generate a notebook from
   "build a mini RAG." **Fix:** §7 is a cell-by-cell spec for all six
   notebooks — every cell, what's pre-written, what's a `TODO`, what the
   output should look like, and what will break.
3. **The icebreaker was nerdy.** **Fix:** Two Truths and a Lie, run for
   speed and for camera. Nothing to do with AI.

Also new: the whole thing ships as a **static site on GitHub Pages** — HTML
decks with print-to-PDF, browser activities with local score caching, the
pre/post test in-browser, and Colab links. §9 covers the build.

---

## 1. The daily grid (identical every day)

| Block | Time | Length |
|---|---|---|
| Block 1 | 9:00 – 10:00 | 60 min |
| *Break* | 10:00 – 10:20 | 20 |
| Block 2 | 10:20 – 11:00 | 40 min |
| *Break* | 11:00 – 11:20 | 20 |
| Block 3 | 11:20 – 12:00 | 40 min |
| *Lunch* | 12:00 – 1:00 | 60 |
| Block 4 | 1:00 – 1:50 | 50 min |
| *Break* | 1:50 – 2:00 | 10 |
| Block 5 | 2:00 – 2:30 | 30 min |

**Announce 9:00. Start 9:15.** The 15 minutes are your API-key and
laptop-problem buffer. Never announce the real start.

Each day ends with a **[STRETCH]** block — deploy it if a supervisor or the
camera crew is in the room, drop it silently otherwise.

---

## 2. The ladder (this is the answer to "are we actually going up?")

Read this table top to bottom and you can see the week rise. If any day's
ceiling feels reachable at 9:15 that morning, that day is too flat.

| Day | Floor (9:15) | Ceiling (2:30) |
|---|---|---|
| **1** | "A token is a piece of text." | A reusable `ask()` wrapper with system prompt, temperature, retries, **and enforced JSON schema output that they parse in code** |
| **2** | "Cut the document into pieces." | **Hybrid retrieval (keyword + vector) with a re-ranking pass, scored against a golden question set they wrote themselves** |
| **3** | "The model asks, your code executes." | A multi-tool agent with **retrieval as one of its tools** (agentic RAG), step cap, error recovery, and a printed decision trace |
| **4** | "It works on my laptop." | Their own app **instrumented**: per-request latency, token count, and cost logged to a table, with a measured cache hit rate |
| **5** | "Someone can type 'ignore your instructions.'" | A **scored adversarial test** run against a peer system across five attack classes, defences implemented, and a re-test showing the delta |

**The rule that keeps it honest:** every day, the last 90 minutes must be
work the *strongest* person in the room finds non-trivial. The first 90
minutes must be work the *weakest* person can follow. The middle is the
climb. If you find yourself explaining something easy after 12:00, the day
has gone flat — skip to the ceiling material.

---

## 3. How the "Applied" name gets earned (revised)

v1 tried to earn it with breadth-as-tourism: look at image models, look at
audio. That's passive and it's the thing you objected to. Cut it.

**The name is earned by making generative AI do useful work end to end, and
by teaching the decisions nobody teaches.** Concretely, the four additions
that no other version of this course has:

| Addition | Where | Why it earns the name |
|---|---|---|
| **Structured output as a contract** | Day 1 ceiling | The difference between a chatbot and a *component in a system*. If the model returns validated JSON, you can build software on it. This is the single most under-taught idea in GenAI courses. |
| **Retrieval evaluation** | Day 2 ceiling | Everyone builds RAG. Almost nobody measures it. Students leave able to say "my retrieval is 7/10 on my golden set" instead of "it looked right." |
| **Multimodal as a pipeline stage** | Day 2 climb | Not a demo. A vision model reading a **scanned** document so it can enter the RAG pipeline. Applied, and immediately useful in a Saudi government context where scanned Arabic PDFs are everywhere. |
| **Instrumentation and cost** | Day 4 ceiling | They produce a real numbers table from their own app. Engineers who can answer "what does this cost per user per month" get hired. |

Keep all seven محاور. Nothing is removed. The SDAIA email explicitly invites
additions: *"يمكنك الاضافة على المحتوى او تعديله في حال تواجد اي نقص"*.

### Old (provided) vs New (built) — your slide 3 and your email to SDAIA

| | Provided deck | This delivery |
|---|---|---|
| Format | 45 PowerPoint slides | Interactive HTML decks on a public site + print-to-PDF |
| LLM mechanics | listed as a prerequisite | taught, with a lab |
| Structured output / JSON schema | absent | **Day 1 ceiling** |
| Retrieval evaluation | absent | **Day 2 ceiling** |
| Hybrid retrieval + re-ranking | one bullet | **taught and built** |
| Multimodal document ingestion | absent | **Day 2, applied** |
| Agentic RAG | absent | **Day 3 ceiling** |
| Cost & latency instrumentation | conceptual only | **measured, in their own app** |
| Code on slides | zero | ~12 slides, walked line by line |
| Labs | 5 described in one line each | **6 Colab notebooks, cell-by-cell** |
| Activities / games | none | **6, browser-based, scored** |
| Capstone + rubric | none | defined, /100, GitHub-submitted |
| Pre/post test | none | 20 questions, in-browser, both ends |
| Student-facing resource | a PDF | **a live site they keep** |

---

## 4. Model access — resolved

**Gemini API has a real free tier. No credit card.** Your assumption that it
isn't free was wrong, and it's what unblocks the week.

- Keys at **aistudio.google.com** → "Get API key". Google account only.
- **`gemini-embedding-001` is free** — this is what makes Day 2 possible at
  zero spend.
- Free generation limits sit around 10–30 req/min and 250–1,500 req/day
  depending on model.

**Every student creates their own key. Never share one.** Limits are per
project — one shared key means one student's loop throttles the room.

**Lab model:** `gemini-2.5-flash-lite` (highest ceiling, fastest). Mention
`gemini-2.5-flash` as the step up for harder reasoning.

**Warn explicitly:** free-tier inputs may be used to improve Google's
models. No real SDAIA data, no personal data, no client data. Then call back
to this on Day 5 when you teach privacy — it lands much harder as a
callback than as a new point.

**Before Sunday:** create a key, run Notebook 1 end to end from a *fresh*
Colab in an incognito window, and screenshot every step of key creation.
Key setup failing live on camera on Day 1 is the highest-probability
disaster of the week.

**Backup:** OpenRouter free-tier slots, one signup. Keep 2–3 spare keys of
your own in your pocket for students who can't create an account.

---

## 5. The icebreaker (replaced)

### Two Truths and a Lie — group heats, then a final

**Total 20 minutes. Nothing to do with AI.**

1. **(3 min)** Everyone gets a card. Write three statements about yourself:
   two true, one false. Tell them the goal is not to be clever — it's to
   make the lie *boring enough to believe*. That instruction is what makes
   this game work; without it people write obvious jokes.
2. **(10 min)** Split into groups of 5. Each person reads their three
   statements; the group votes on which is the lie; reveal. Each group picks
   the person whose lie fooled the most people.
3. **(6 min)** **The final.** The 4–5 group winners come to the front and
   present to the whole room. Everyone votes by raised hand. Reveal one at a
   time. Winner takes a small prize.
4. **(1 min)** **You go last, out of competition.** Two truths and a lie
   about yourself. This is how they get to know you, and it lands better
   after they've all done it than as an opener.

**Why this shape:** everyone speaks inside the first fifteen minutes, which
is the single strongest predictor of who participates for the rest of the
week. The heats keep it fast for 20+ people. The final is the camera moment.

**Bonus:** those groups of 5 become your project team pool on Monday. Say so
at the end — "remember your group."

Then a fast round-the-room: name + **one sentence on what they want AI to do
for them by Thursday**. Capture these on a flipchart — that flipchart is the
project idea pool.

---

## 6. Day-by-day

Format below: **Floor → Climb → Ceiling** per day, then blocks.

---

### DAY 1 — Sunday · From token to typed output
**Theme: "The model is a function. Make it a reliable one."**
**Official: المحور 1 · Introduction to GenAI solutions engineering**

> **Floor:** what a token is.
> **Climb:** temperature, system prompts, context window, hallucination.
> **Ceiling:** a reusable `ask()` function with retries that returns
> **schema-validated JSON** they parse in code.

That ceiling is deliberately chosen. The moment a student sees the model
return parseable JSON that their `if` statement branches on, generative AI
stops being a chat toy and becomes a component. Everything the rest of the
week builds sits on that realisation.

**Block 1 · 9:15–10:05** — Icebreaker (§5, 20 min) · Pre-test (15 min, in
browser) · Course map, site tour, old-vs-new slide, project reveal + rubric

**Block 2 · 10:15–11:05** — *How the thing actually works*
- Discriminative vs generative in one slide, then move on
- **Tokens.** Live tokenizer demo: paste English, paste Arabic, compare.
  Arabic costs roughly 2–3× the tokens per word. Local, concrete, memorable,
  and it explains a cost line item they will hit.
- **Context window** — and immediately: *this is why chunking exists on
  Monday*
- **Next-token prediction** — why it is fluent and wrong simultaneously
- **Temperature, top-p** — what you actually turn and when
- **Hallucination** — a property to design around, not a bug to patch
- **The four ways to make a model useful** — prompting / RAG / tools /
  fine-tuning, with cost and "when." Say plainly: *most people reach for
  fine-tuning and should have reached for RAG.* This slide is the spine of
  the week; every later day points back to it.
- **Activity 1 · Tokenizer Race** (browser, 8 min, scored)

**Block 3 · 11:15–12:00** — *Get your key, make your first call*
- Walk AI Studio key creation on screen with screenshot backup
- **Notebook 1, cells 1–8.** Start before lunch so lunch absorbs stragglers.
  Circulate. Do not sit down.

**Block 4 · 1:00–1:50** — *The climb: prompts that hold*
- System vs user role, and why the separation is a security boundary (seeds
  Day 5)
- Few-shot examples, delimiters, explicit output format
- **Notebook 1, cells 9–14** — temperature comparison, system prompt
  rewriting

**Block 5 · 2:00–2:30** — *The ceiling: typed output*
- **Structured output.** Ask for JSON, define a schema, validate it in code,
  branch on the result. Show a failing parse and a retry.
- **Notebook 1, cells 15–18** — the `ask()` wrapper with retries + JSON mode
- Day 1 summary · homework: GitHub account, pick a document set

**[STRETCH]** Live prompt clinic — take a volunteer's real messy prompt,
improve it on screen, before/after. Infinitely expandable.

---

### DAY 2 — Monday · Retrieval that you can actually measure
**Theme: "Everyone builds RAG. Almost nobody measures it."**
**Official: المحور 2 (RAG vs Agents) · المحور 3 (retrieval pipeline)**

> **Floor:** why the model doesn't know your documents.
> **Climb:** ingestion, chunking, embeddings, vector search, top-k.
> **Ceiling:** hybrid retrieval + re-ranking, **scored against a golden
> question set the students write themselves.**

**Block 1 · 9:15–10:05** — *Architecture choice*
- Day 1 recall — questions to the room, not a slide
- RAG in four steps · Agents as a loop · the comparison table (yours is
  good, keep it) · the decision rule · **start with the simplest thing that
  works**
- Where this fits the four-ways slide from Day 1

**Block 2 · 10:15–11:05** — *The pipeline, stage by stage*
1. **Ingestion** — clean text, strip furniture, **keep source + page as
   metadata so you can cite later**
2. **Multimodal ingestion** *(the applied addition)* — a scanned Arabic PDF
   has no text layer. Send the page image to a vision model, get text back,
   feed it into the same pipeline. Demo live. This is not a modality tour;
   it is a pipeline stage that solves a problem they will actually meet.
3. **Chunking** — size, overlap, structure-aware splitting
4. **Embedding + vector DB** — meaning as coordinates; "annual leave"
   matches "vacation days" with no shared word
5. **Retrieval** — embed query, nearest top-k

**Fix before you print:** your deck says ~200–500 **words**, the other deck
says 500–1000 **tokens**. Pick one. Recommend: *"start at ~500 tokens with
~10% overlap, then tune"* — and say out loud that it's a starting point.

**Block 3 · 11:15–12:00** — *Activity 2 · Chunk Lab* (browser, 20 min,
scored) then **Notebook 2, cells 1–12** — load, chunk, embed, store, query

Chunk Lab is the best activity of the week for non-coders: a real document
on screen, they drag the split points, and the tool shows which questions
their chunking answers badly. Ten minutes here beats any slide.

**Block 4 · 1:00–1:50** — *The ceiling, part 1: making retrieval better*
- **Why pure vector search fails**: exact terms, IDs, names, acronyms.
  "SDAIA-F-CRS-201" is a string, not a meaning.
- **Hybrid retrieval** — BM25 keyword + vector, scores combined
- **Re-ranking** — retrieve 20 cheap, re-rank to the best 4
- **Query rewriting** — the user's question is rarely the best search string
- **Notebook 2, cells 13–20**

**Block 5 · 2:00–2:30** — *The ceiling, part 2: proving it works*
- **Golden question set** — write 10 questions you know the answers to,
  record which chunk *should* be retrieved, measure hit rate
- **Notebook 2, cells 21–24** — score naive vs hybrid vs re-ranked, print a
  comparison table
- Day 2 summary · **project team formation and idea pitching** using the
  Day 1 flipchart and the icebreaker groups

**[STRETCH]** Chunking strategies deep-dive — semantic chunking,
parent-document retrieval, contextual chunk headers.

---

### DAY 3 — Tuesday · Tools, agents, and agentic RAG (+ project)
**Theme: "Let it act — but keep the leash short."**
**Official: المحور 4 (function calling) · المحور 5 (agent patterns)**

> **Floor:** the model requests, your code executes.
> **Climb:** tool schemas, the loop, agent patterns, guardrails.
> **Ceiling:** a multi-tool agent that uses **their own Day 2 retriever as
> one of its tools**, with a step cap, error recovery, and a printed trace.

That ceiling is the payoff of the whole week — Day 2's work becomes a tool
inside Day 3's agent. Say that out loud when you introduce it.

**Block 1 · 9:15–10:05** — *Function calling*
- Why: no live data, no actions, unreliable arithmetic
- **State three times: the model does not run your code.** It *requests*;
  your app executes; you hand the result back.
- The loop in 5 steps
- Tool schema walked argument by argument — and emphasise that
  `description` is what the model reads to decide. A vague description is a
  broken tool.
- **Activity 3 · Be the Agent** (browser + room, 15 min) — students drive a
  simulated loop by choosing the model's next move; the tool responses are
  real. Everyone sees who executes what.

**Block 2 · 10:15–11:05** — *Patterns and control*
- How uncontrolled agents fail: loops, cost, unpredictability
- **ReAct** · **Plan-and-Execute** · **Reflection** · **Routing** ·
  **Hierarchical** · **Human-in-the-loop** — one line each plus "use it when"
- Guardrails: max steps, tool allow-list, output validation, stop conditions
- Error recovery: what a tool should return when it fails, so the model can
  recover instead of hallucinating

**Block 3 · 11:15–12:00** — **Notebook 3** — two tools, the loop, step cap,
decision trace, then **retrieval-as-a-tool** (agentic RAG)

**Blocks 4 + 5 · 1:00–2:30 — PROJECT TIME (80 min)**
You circulate. Do not present. Checkpoint every pair twice.
**Gate by 2:30:** documents loaded, chunked, embedded, one query returning
something. Not polished — running. Anyone stuck at 2:00 gets you sitting
next to them.
Close with a 5-minute stand-up: one sentence per pair. Public
accountability, and it tells you who to rescue tomorrow.

---

### DAY 4 — Wednesday · Production and the numbers (+ project)
**Theme: "What does this cost per user per month?"**
**Official: المحور 6 (production-ready applications)**

> **Floor:** prototype vs production.
> **Climb:** scalability, caching, streaming, fallbacks, observability.
> **Ceiling:** their own app instrumented — latency, tokens and cost logged
> per request, with a **measured** cache hit rate and a real numbers table.

**Block 1 · 9:15–10:05** — *The gap and the arithmetic*
- One user vs thousands · errors tolerated vs handled · cost ignored vs
  managed
- Rate limiting — **and connect it to the 429s they actually hit on Monday.**
  Lived experience beats a definition.
- **Cost, concretely.** Tokens in + tokens out × price, computed on screen
  for a realistic internal assistant. Then Arabic tokenisation from Day 1
  comes back: the same assistant costs more in Arabic. Nobody teaches this.
- **Activity 4 · Cost Auction** (browser, 12 min, scored) — estimate the
  monthly bill for a given scenario, closest wins, then reveal the maths

**Block 2 · 10:15–11:05** — *Reliability and observability*
- Retries with exponential backoff · fallback chains · timeouts
- **Observability**: logging, **tracing** (one request across every tool),
  metrics, continuous evaluation. Name LangSmith / Langfuse.
- Deployment architecture: UI → API → orchestration → model + tools + vector
  DB → cache → monitoring → security
- **UX for AI**: streaming so it feels fast, citations so it feels
  trustworthy, honest failure states

**Block 3 · 11:15–12:00** — **Notebook 4**, applied to *their own project*:
retry wrapper, streaming, cache with hit-rate measurement, per-request
logging to a DataFrame, fallback. Ends with them printing their own metrics
table.

**Blocks 4 + 5 · 1:00–2:30 — PROJECT TIME (80 min)**
- 1:00–2:00 build, you circulate
- **2:00–2:20 README clinic** — SDAIA repo requirements on screen, every
  pair writes their README *now*, with you checking. READMEs written the
  night before are always bad.
- 2:20–2:30 Thursday briefing: 4-minute format, what to demo, and that an
  honestly-explained broken demo scores better than a fake working one

---

### DAY 5 — Thursday · Adversarial testing and demo day
**Theme: "Would you actually let this loose?"**
**Official: المحور 7 (security, reliability, governance)**

> **Floor:** someone can type "ignore your instructions."
> **Climb:** direct vs indirect injection, layered defences, privacy,
> governance.
> **Ceiling:** a **scored** red-team against a peer system across five
> attack classes, defences implemented, re-test showing the delta.

**Block 1 · 9:15–10:05**
- 9:15–9:30 **Post-test** (same 20 questions, in browser) → enter both
  scores in the SDAIA sheet
- 9:30–9:35 **Course evaluation link** — distribute at the *start* of the
  day; attendance decays
- 9:35–10:05 **Prompt injection**
  - **Direct** — the user types it
  - **Indirect** — hidden text inside a retrieved document. Far worse: the
    attacker never speaks to your system. *Their own Day 2 RAG is the
    attack surface.* Demo this against a planted document.
  - Consequences: data leakage, unauthorised tool execution, bypassed rules
  - Layered defences: instruction/data separation, input validation, tool
    least privilege, sandboxing, human approval on irreversible actions
  - **Say honestly: this is not solved.** No patch exists. You reduce risk
    in layers. They should leave knowing that.

**Block 2 · 10:15–11:05** — *Reliability, privacy, governance + red team*
- Grounding, schema validation, citations, adversarial testing
- **PII and privacy** — callback to Day 1's free-tier warning
- Governance: policies, audit logs, accountability, compliance
- Responsible AI: bias, fairness, transparency about limits
- **Pre-launch checklist** — one-page handout they take to work
- **Activity 5 · Red Team** (browser + live, 25 min, scored). Pairs swap
  projects. Five attack classes, points per success:
  instruction override · data exfiltration · scope escape · indirect
  injection via a planted document · resource exhaustion.
  Two winners: best attacker, and most resilient system. Then 10 minutes of
  fixes applied before presentations.

**Block 3 · 11:15–12:00 and Block 4 · 1:00–1:50 — Presentations**
4 min + 2 min questions. Each pair: the problem · the architecture and
**why** · live demo · one thing that broke and what they did.
Score against the rubric live, on paper, as they go.
*If more than 14 pairs:* gallery walk — laptops open, 40 min circulation
with scoring sheets, then 5 teams present.

**Block 5 · 2:00–2:30** — Close
- Journey summary, one line per day
- **Where next**, concretely: LangChain/LlamaIndex docs, evaluation tooling,
  the SDAIA Academy GitHub, one book, one course
- Confirm every repo is pushed, public, and links
  https://github.com/SDAIAAcademy
- Group photo

**[STRETCH]** "What's coming" — multimodal agents, computer-use models,
where the field is going, open Q&A.

---

## 7. Notebook specifications

Six notebooks. Convention throughout:

- **Cell 1 is always** install + imports + `userdata.get('GEMINI_API_KEY')`
  with a clear error message if the key is missing.
- **Pre-written cells** are complete and runnable. **`# TODO` cells** have
  the structure written and one or two lines blanked. Given "can edit a
  script" as the floor, **nobody writes a cell from empty.**
- Every notebook ends with a **markdown reflection cell** they fill in — it
  is what you check when circulating.
- Every notebook has a **"If this breaks"** markdown cell listing the three
  most likely failures and their fixes. This is what saves you from
  answering the same question twenty times.
- There should be concise and short but clear comments for all lines of code 
  so that they can understand line by line what is happening.

---

### Notebook 1 — `day1_first_calls.ipynb`
*From a first request to a typed, validated response.*

| # | Type | Content |
|---|---|---|
| 1 | code | `pip install google-genai`, imports, key load, friendly error |
| 2 | md | What you'll build today — ends with the JSON output as the goal |
| 3 | code | First call. 4 lines. **Pre-written.** They just run it. |
| 4 | md | What just happened: request → tokens → sampling → response |
| 5 | code | Print `usage_metadata` — prompt tokens, output tokens, total |
| 6 | code | **TODO** — send their own prompt, note the token count |
| 7 | code | Arabic vs English token count on the same sentence. Pre-written. |
| 8 | md | Why Arabic costs more, and why that's a budget line |
| 9 | code | Same prompt at `temperature=0.0` run 3× — identical output |
| 10 | code | Same prompt at `temperature=1.2` run 3× — different output |
| 11 | md | **TODO reflection** — describe the difference in one sentence |
| 12 | code | System instruction demo: same user prompt, two different personas |
| 13 | code | **TODO** — write a system instruction making it answer only in bullet points, under 50 words |
| 14 | code | Context window: send a very long input, catch the error |
| 15 | md | **The ceiling starts here.** Why free text is unusable in software |
| 16 | code | JSON mode: `response_mime_type="application/json"` + a schema. Extract `{name, email, intent, urgency}` from a support message. Pre-written. |
| 17 | code | `json.loads()` the result and **branch on it** — `if data["urgency"] == "high": ...`. This is the moment. |
| 18 | code | **TODO** — define their own schema for a different extraction task |
| 19 | code | The `ask()` wrapper: system prompt, temperature, retries with backoff, optional schema. **Given complete** — they read it, don't write it. |
| 20 | md | Reflection + "If this breaks" |

**Breaks:** key not in Colab secrets (most common — show the 🔑 panel
explicitly); wrong model name; JSON parse failure when schema is omitted.

---

### Notebook 2 — `day2_retrieval.ipynb`
*The longest and most important notebook of the week. Two sittings.*

**Part A (Block 3) — a working naive RAG**

| # | Type | Content |
|---|---|---|
| 1 | code | Install `chromadb`, `google-genai`, `rank-bm25`; imports; key |
| 2 | code | Download a provided document set (~15 short Arabic + English policy docs) |
| 3 | code | Load and clean → list of `{text, source, page}` dicts. Pre-written. |
| 4 | md | **Multimodal ingestion** — one of these files is a scanned image |
| 5 | code | Send the scanned page to the vision model, get text back, add it to the corpus. Pre-written, high-impact. |
| 6 | code | `chunk(text, size, overlap)` — **TODO**, the loop body is blanked |
| 7 | code | Inspect chunks: print 3, check nothing is cut mid-word |
| 8 | code | Embed all chunks with `gemini-embedding-001`, batched |
| 9 | code | Store in Chroma with metadata |
| 10 | code | `search(query, k)` → print retrieved chunks with sources |
| 11 | code | `answer(query)` — retrieve, build a prompt, generate **with citations** |
| 12 | code | **TODO** — ask three questions about their own domain, note quality |

**Part B (Blocks 4–5) — the ceiling**

| # | Type | Content |
|---|---|---|
| 13 | md | Where vector search fails: IDs, acronyms, exact names |
| 14 | code | Demonstrate the failure — search for `"SDAIA-F-CRS-201"`, watch it miss |
| 15 | code | BM25 keyword index over the same chunks |
| 16 | code | `hybrid_search()` — combine scores. **TODO:** the weighting line |
| 17 | code | Re-run the failing query — watch it succeed |
| 18 | md | Re-ranking: retrieve 20 cheap, keep the best 4 |
| 19 | code | LLM-as-reranker — score each of 20 chunks 0–10 for relevance, keep top 4 |
| 20 | code | Query rewriting — turn a conversational question into a search string |
| 21 | md | **Golden set.** Write 10 questions you know the answers to |
| 22 | code | `GOLDEN = [{"q": ..., "must_contain": ...}, ...]` — **TODO**, they fill it |
| 23 | code | `evaluate(search_fn)` → hit rate. Pre-written. |
| 24 | code | Score naive vs hybrid vs re-ranked, print a comparison table |
| 25 | md | Reflection: which won, by how much, and where it still fails |

**Breaks:** embedding rate limits (batch and sleep — pre-written); Chroma
collection already exists on re-run (add `delete_collection` guard); Arabic
text direction confusing them in printed output.

---

### Notebook 3 — `day3_agents.ipynb`

| # | Type | Content |
|---|---|---|
| 1 | code | Setup + imports + key |
| 2 | code | Tool 1: `calculate(expression)` — a real Python function |
| 3 | code | Tool 2: `get_weather(city)` — mock data, deliberately |
| 4 | md | Why a mock is fine: the *loop* is the lesson, not the API |
| 5 | code | Tool schemas — declarations walked argument by argument |
| 6 | code | Single tool call, **manually**: send → inspect the request → execute → send result back. Four separate cells so the round-trip is impossible to miss. |
| 7 | md | Say it again: the model never ran your function |
| 8 | code | `run_agent(goal, tools, max_steps)` — the loop, **given complete** |
| 9 | code | Run a two-step task with `verbose=True` — prints every decision |
| 10 | code | **TODO** — write their own third tool and register it |
| 11 | code | **Remove the step cap and run a task it can't finish.** Watch it spiral. Interrupt manually. |
| 12 | md | What that cost, if it had been a paid key |
| 13 | code | Put the cap back. Add an output validator. |
| 14 | md | **The ceiling: agentic RAG** |
| 15 | code | Wrap Notebook 2's `search()` as a tool named `search_documents` |
| 16 | code | Give the agent both the retriever and the calculator; ask a question needing both |
| 17 | code | Print the trace — watch it choose retrieval, then arithmetic |
| 18 | md | Reflection + "If this breaks" |

**Breaks:** tool schema type mismatches; infinite loop when the model can't
satisfy the goal (that's cell 11, deliberate); forgetting to append the tool
result to history.

---

### Notebook 4 — `day4_production.ipynb`
*Applied to their own project, not a toy.*

| # | Type | Content |
|---|---|---|
| 1 | code | Setup; import their Day 2/3 functions |
| 2 | code | `@retry` decorator with exponential backoff. Given complete. |
| 3 | code | Force a failure to prove the retry fires |
| 4 | code | Streaming — same prompt, side by side, timed |
| 5 | md | Streaming doesn't make it faster. It makes it *feel* faster. |
| 6 | code | Simple dict cache keyed on the prompt |
| 7 | code | Run 20 queries with 8 repeats — measure hit rate and time saved |
| 8 | code | `log_request()` → appends `{timestamp, prompt_tokens, output_tokens, latency, cost}` to a list |
| 9 | code | **TODO** — fill in the cost formula from the pricing table |
| 10 | code | Run 15 mixed queries, build a pandas DataFrame, `.describe()` |
| 11 | code | Plot latency distribution and cumulative cost |
| 12 | md | **TODO** — from your table: cost per query, per user per month at 4 queries/day |
| 13 | code | Fallback chain: primary model → cheaper model → canned response |
| 14 | code | Break the primary on purpose, watch the fallback engage |
| 15 | md | Reflection + "If this breaks" |

---

### Notebook 5 — `day5_redteam.ipynb`

| # | Type | Content |
|---|---|---|
| 1 | code | Setup; load a deliberately vulnerable assistant (given) |
| 2 | code | **Attack 1 — instruction override.** Direct. Watch it work. |
| 3 | code | **Attack 2 — system prompt extraction.** |
| 4 | code | **Attack 3 — scope escape.** Make a policy bot answer about football. |
| 5 | md | **Indirect injection — the dangerous one** |
| 6 | code | Add a poisoned document containing hidden instructions to the corpus |
| 7 | code | Ask a normal question. Watch the retrieved document hijack the answer. |
| 8 | md | Nobody attacked the system. The attack was *in the data.* |
| 9 | code | **Defence 1** — clear delimiters and instruction/data separation |
| 10 | code | **Defence 2** — input validation and a retrieved-content sanitiser |
| 11 | code | **Defence 3** — output validation against an allowed-topics check |
| 12 | code | **Re-run all four attacks.** Print a before/after table. |
| 13 | code | **TODO** — write a fifth attack of their own and try to defend it |
| 14 | md | Honest note: some of these still get through. That's the state of the art. |
| 15 | md | Reflection + the pre-launch checklist as a markdown table |

---

### Notebook 0 — `project_scaffold.ipynb`
*Handed out Monday afternoon. This is what they build on.*

Sections, all with structure written and `TODO` markers:
1. Config — key, model, constants
2. Ingest — `load_my_documents()` ← they point it at their own files
3. Chunk — calls their Day 2 chunker
4. Index — embed + store
5. Retrieve — hybrid search, given
6. Tools — one example tool + a slot for theirs
7. Agent loop — given
8. Guardrails — one example + a slot
9. Instrumentation — logging from Day 4
10. `demo()` — the function they run on Thursday
11. Golden set — 5 questions to prove it works
12. README template as a markdown cell they copy into the repo

---

## 8. Assessment

### Pre/post test — 20 questions, identical both times
In-browser, auto-scored, results in `localStorage`, with a
"copy my score" button so students can read it out for the SDAIA sheet.

Coverage: 4 LLM mechanics · 4 retrieval · 3 architecture choice · 3
tools/agents · 3 production & cost · 3 security & governance.

**Design rules:** every question maps to something you actually teach; at
least 6 answerable by a smart non-technical person so the pre-test isn't
demoralising; 3 should be hard enough that few get them even on Thursday.

**Framing on Day 1, out loud:** "This measures me, not you. Zero is a fine
score right now."

*(Ask me and I'll write all 20 with the answer key and distractor rationale.)*

### Project rubric — 100 points

| Criterion | Pts | Full marks |
|---|---|---|
| Architecture choice & justification | 25 | Picked RAG / agent / hybrid and can say *why* in one sentence tied to their use case. Wrong-but-justified beats right-but-unexplained. |
| Working retrieval | 25 | Their own docs, sensible chunking, relevant retrieval, visibly grounded answers with citations |
| Tool integration | 15 | ≥1 function-calling tool that executes and whose result reaches the answer |
| Safety & reliability | 10 | ≥1 guardrail demonstrated; handles a failure without crashing |
| Repo quality | 15 | All six SDAIA requirements; README a stranger could follow |
| Presentation | 10 | 4 minutes; demo works, or the failure is explained honestly |

**Pass = 60. Publish Day 1, not Thursday.**

**Scope guards:** ship the scaffold notebook; pairs preferred (pair a coder
with a non-coder and say that's deliberate); "working" means it runs in
Colab — no deployment, no frontend, no Docker.

### SDAIA GitHub requirements (verbatim, put on a slide)
- Clear, comprehensive project description
- Professional `README.md`: idea, how to run, how to use
- Appropriate technical documentation
- Git version-control best practice — real commits, not one dump
- Name the training programme
- Link https://github.com/SDAIAAcademy

---

## 9. What ships as the website

Static site, GitHub Pages, no build step. Structure:

```
applied-genai/
├── index.html                 hero, 5-day map, links to everything
├── assets/
│   ├── sdaia.svg              top-right on every page
│   ├── sdaia-academy.svg      top-left on every page
│   ├── theme.css              tokens: colours, type, spacing
│   ├── site.css               shared page chrome
│   ├── deck.css               slide-deck styling + @media print
│   ├── deck.js                slide engine: keys, dots, print-to-PDF
│   ├── store.js               localStorage scores + progress
│   └── activity.css           shared activity chrome
├── slides/day1.html … day5.html
├── activities/
│   ├── index.html
│   ├── tokenizer-race.html
│   ├── chunk-lab.html
│   ├── be-the-agent.html
│   ├── cost-auction.html
│   └── red-team.html
├── assessment/
│   ├── pretest.html
│   └── posttest.html
├── project/index.html         brief, rubric, GitHub requirements
├── notebooks/                 .ipynb files + notebooks.json (Colab links)
└── README.md
```

**Design language:** reuse the Workshop Hub exactly — dark navy hero, serif
display headline, teal accent, numbered cards with day badges, session-total
footer, both logos. It's already proven with SDAIA and students will
recognise it.

**Decks as HTML, not PPTX:** keyboard navigation, a print-to-PDF button that
lays one slide per page, live embedded demos (a real tokenizer on the token
slide, a real cost calculator on the cost slide) — things PowerPoint cannot
do. That's a differentiator worth naming in your old-vs-new table.

**Build it with the prompts in `prompts.md`**, one at a time, in order.

---

