# Day 1 — From token to typed output
### Instructor side-notes · Applied Generative AI · SDAIA Academy

> **How to read this file:** **bold = what is on the slide, unpacked** · plain text = extra depth, context, or answers to questions the slide will provoke. Bullets run foundation → detail → payoff, so you can stop anywhere and still have said something complete.

---

## Slide 1 · Title — From token to typed output

- **The promise of the day is one sentence: by 2:30 they will have a function that returns JSON their own code can branch on.** Say the destination out loud before any theory — adults tolerate abstraction only when they can see what it buys them.
- **"The model is a function"** is the frame for the whole week. Input → output, with a cost, a latency, and a failure mode. Not a mind, not an oracle.
- Set the contract for the room now: interrupt immediately, don't save questions. In a 5-day build course, a silent stuck person on Sunday is a lost person by Tuesday.
- Read the room in the first 3 minutes — ask for hands: who writes Python weekly, who has called any LLM API, who has only used the chat window. Your pacing for Part One depends entirely on that ratio.
- If you want a hook: the gap between "I used ChatGPT" and "I shipped something with a model in it" is almost entirely today's last half hour.

---

## Slide 5 · Where today sits

- **The week is a dependency chain, not five independent topics:** typed output (Sun) → grounded retrieval (Mon) → the retriever becomes a tool (Tue) → instrument and cost it (Wed) → attack and defend it (Thu).
- **Because it's a chain, falling behind compounds.** This is the justification for "tell me the moment you're stuck" — say it as a systems argument, not as pastoral care, and it lands harder with a technical room.
- **Thursday's 4-minute paired demo** is worth mentioning now so they start building with an audience in mind. People make better scope decisions when they know they must show it.
- Extra framing, if useful: the week walks *up* the stack of trust. Sunday you trust the shape of the output; Monday you trust the source; Tuesday you trust it to act; Wednesday you trust it under load; Thursday you assume an adversary and check the trust holds.
- Expect the question "why not start with agents, that's the exciting part?" — answer: an agent is a loop around today's typed call. An agent built on unparseable output is a loop around a coin flip.

---

## Slide 9 · What you will be able to do by 2:30

- **Five outcomes, phrased as verbs they perform, not topics you cover.** Promise to re-show this slide at 2:30 — and actually do it. The retrospective check is what makes the promise real.
- **Outcome 1 (tokens, Arabic cost) is the vocabulary.** Outcome 2 (call it, read usage) is the muscle. Outcome 3 (temperature, system) is control. Outcome 4 (schema) is the leap. Outcome 5 (`ask()`) is the reusable artefact.
- **Number 4 is the one you're claiming nobody teaches** — defend that claim, because someone will test it. Most courses stop at "write better prompts", which leaves the output as prose, which leaves the developer writing regex.
- Deliberate pairing of coders with non-coders is a teaching decision worth naming: the non-coder forces the coder to explain, and explanation is where understanding gets checked.
- Outcome-based objectives also give you a fair post-test: every item on this list is directly observable in their notebook.

---

## Slide 10 · Part One — How the thing actually works

- **Forty minutes of mechanics, and you are explicitly asking the experienced people to sit through it.** Justify it: the vocabulary set here (token, context window, temperature, grounding) is used for four more days without re-explanation.
- Signpost the three parts of the day so they can locate themselves: mechanics → prompting → typed output. Say the day gets more practical as it goes.
- Time discipline note for you: Part One is the segment most likely to overrun, because it's the part where the interesting tangents live. Park deep questions on a visible list and answer at the break.

---

## Slide 11 · Two kinds of model

- **Discriminative: learns a boundary between classes. Fixed, finite answer set. `P(label | input)`.** You can enumerate every possible output, so accuracy, precision and recall are all directly measurable.
- **Generative: models the distribution of the data itself, and samples from it. `P(next token | everything so far)`.** The output space is effectively infinite, so "correct" stops being a lookup and becomes a judgement.
- **That difference is a promise problem, not an architecture problem** — the line to hit. A classifier lets you tell your users "it is 94% accurate". A generative model does not hand you that sentence for free; you have to build the evaluation that earns it (Monday's golden set).
- Extra: this is why the entire week is about *narrowing the output space* — schemas, enums, retrieved context, tool signatures, guardrails. Every one of those shrinks the set of things the model is allowed to say.
- Useful aside for a sceptic: modern LLMs do classification perfectly well — you just constrain a generative model down to a label set (which is literally slide 25's `enum`). Generative is the more general machine; discriminative is what you make it behave like.
- Don't linger. You said "one slide on theory" — honour it, it buys you credibility for the rest of the day.

---

## Slide 12 · A token is not a word

- **The model never sees characters or words. Text is segmented into subword chunks, each mapped to an integer ID, and only those integers enter the network.**
- **"unbelievably" → `un | bel | iev | ably`: rare words fragment, common words survive whole.** The vocabulary was learned from a corpus; frequency decides what got its own slot.
- The algorithm behind it is usually **BPE (byte-pair encoding)** or a variant: start from bytes, repeatedly merge the most frequent adjacent pair, stop at a fixed vocabulary size (typically 32k–256k entries). Nothing linguistic about it — it's compression statistics.
- Because it starts from *bytes*, there is no such thing as an unknown character. Emoji, Chinese, mathematical symbols all encode — just expensively, at several tokens each.
- **Rule of thumb for English: ~4 characters per token, so 100 words ≈ 130 tokens.** Good enough for budgeting; not exact enough for a hard limit — for that, count with the real tokenizer.
- **"You are billed per token, in and out" — tokens are the unit of cost, of rate limits, and of latency.** Latency especially: output tokens are generated one at a time, so a long answer is slow in a way a long prompt is not.
- Nice classroom moment: this is why models are bad at counting letters in a word or reversing strings. They never see letters. "How many r's in strawberry" is not a reasoning failure, it's a representation failure.

---

## Slide 13 · The same sentence costs more in Arabic (LIVE)

- **Same meaning, 11 tokens in English vs ~26 in Arabic — 2–3× on identical content.** State plainly: that is a direct multiplier on your bill, your latency, and how much you can fit in a context window.
- **The live box uses a heuristic (~4 chars/token Latin, ~2 for Arabic), not the real tokenizer** — say that out loud, because someone will compare it to a real count and find a difference.
- Why it happens, in order of importance: (1) Arabic is under-represented in the corpus the vocabulary was learned from, so fewer Arabic words earned a whole-token slot; (2) Arabic script is multi-byte in UTF-8, so byte-level fallback is expensive; (3) rich templatic morphology — prefixes, clitics, attached pronouns — means one orthographic word carries what English spreads over several, and gets split anyway.
- Diacritics (tashkīl) make it dramatically worse. Un-vowelled text tokenizes far more cheaply, which is a real preprocessing decision for an Arabic product.
- The gap has been narrowing across tokenizer generations (larger, more multilingual vocabularies), but it has not closed and probably won't. Treat it as a permanent tax to design around.
- **Consequences to name now, and cash in on Wednesday:** an Arabic assistant costs meaningfully more per user than the identical English one; the effective context window is smaller in Arabic; per-request token caps set from English testing will truncate Arabic answers.
- Good exercise instruction: have them paste a real paragraph from their own work, then its translation. The number being *theirs* is what makes it stick.

---

## Slide 14 · The context window

- **Everything the model can see on one call: system instruction + full conversation history + pasted documents + the answer being generated. All of it counted in tokens, all of it paid for.**
- **The window is not memory.** This is the sentence to say slowly. Between calls the model retains nothing — the client re-sends the entire conversation every single turn, which is why a long chat gets progressively more expensive per message.
- **Overflow behaviour splits two ways: a hard API error, or silent truncation where the earliest content quietly drops out.** The second is worse, because it looks like the model "forgot" or "ignored your instructions" when actually your instructions left the building.
- Why windows aren't just made infinite: attention cost grows roughly with the square of sequence length, and the KV cache grows linearly in memory. Big windows are an engineering expense someone is paying for.
- Quality degrades before capacity does — the "lost in the middle" effect: material at the start and end of a long context is recalled far more reliably than material buried in the middle. A 1M-token window is not 1M tokens of *attention*.
- **"This is why chunking exists tomorrow"** — deliver it as the setup it is. Retrieval isn't a workaround for small windows; it's how you put the *right* 2,000 tokens in front of the model instead of the *wrong* 400,000.
- If asked about prompt caching: yes, providers let you cache a stable prefix so re-sending it is cheaper. It reduces the bill, not the window.

---

## Slide 15 · It is predicting the next token

- **The full algorithm: given the sequence so far, produce a probability over every token in the vocabulary; pick one; append it; repeat.** Autoregressive generation. Hundreds of iterations for one paragraph.
- **"Riyadh — 94%, the — 2%, located — 1%…"** — note that the alternatives are mostly *grammatical continuations*, not rival facts. The model is completing a sentence, not answering a question.
- Under the hood: the network emits a raw score (logit) per token, softmax turns those into a distribution, and a sampler picks. Temperature and top-p act on that distribution — which is exactly the next slide.
- **Nothing in this loop checks truth. It checks likelihood.** There is no database lookup, no retrieval, no verification step. Facts are only in there as statistical residue of training text.
- **"Fluent and wrong are not opposites here."** Fluency is literally the training objective; truth was never optimised for directly. Confidence in the prose tells you nothing about correctness of the claim.
- Extra that pays off later: because it appends its own output back into the input, an early wrong token *conditions everything after it*. The model will happily build three consistent paragraphs on top of a fabricated policy number. Error compounds forward — that's the mechanical argument for why agent loops need verification at every step (Tuesday).
- Anticipate the objection: "but it clearly reasons." Fair — next-token prediction at scale produces behaviour that looks like reasoning, and chain-of-thought genuinely improves results. But the mechanism is unchanged, and it explains the failures better than any other story.

---

## Slide 16 · Temperature

- **One prompt, three temperatures, three characters of output: 0.0 deterministic and flat, 0.7 varied wording with the same substance, 1.2 creative and starting to invent.**
- **Mechanically: temperature rescales the logits before sampling.** Below 1 it sharpens the distribution (the likely token gets likelier); above 1 it flattens it (unlikely tokens get a real chance). At 0 it collapses to always taking the top token — greedy decoding.
- **The practical rule: 0.0–0.2 for anything you parse — extraction, classification, routing, structured output. 0.7+ for drafting, naming, ideation, brainstorming.**
- **The failure you see constantly: extraction run at the default temperature, then complaints about inconsistency.** Most SDKs default around 0.7–1.0. Nobody changes it. Name this as the single cheapest bug fix in the room.
- Related dial they'll meet in the docs: **top_p / nucleus sampling** — instead of reshaping probabilities, it truncates the candidate list to the smallest set summing to p. Change one or the other, not both; they interact confusingly.
- Important honesty: temperature 0 is *near*-deterministic, not guaranteed reproducible. Floating-point non-determinism, batching, and mixture-of-experts routing mean identical calls can still differ. Don't promise byte-identical output to a room that will test it.
- Higher temperature does not mean "more creative" in a useful sense past a point — it means more likely to leave the distribution's sensible region. 1.2 is the edge; 2.0 is usually noise.
- **Lab connection: three runs at 0.0, three at 1.2.** Tell them to look at *sentence structure*, not just wording — at 0.0 it repeats exactly, which is the observation that makes the mechanism obvious.

---

## Slide 17 · Hallucination is a property, not a bug

- **Direct consequence of slide 15: the model always produces likely text. With no grounding, likely text still arrives — confident, well-formatted, and wrong.**
- **It fabricates precisely the things that look most authoritative:** policy numbers, article references, dates, citations, statute names, URLs. The format is learned; the content is invented to fit.
- Be honest about the mechanism: the model has no signal for "I don't know" unless the training process deliberately built one. Saying "I'm not sure" is itself just a likely continuation — one that has to be made likely.
- **Four mitigations, and each is a day of this course:**
  - **Ground it** — put the actual document in the context (Monday, RAG).
  - **Cite it** — force it to show which chunk supported each claim, so unsupported answers are visible.
  - **Type it** — a schema removes the room to waffle (this afternoon).
  - **Check it** — validate in code before you act on it. Cheapest and most skipped.
- **"There is no patch coming."** Newer models hallucinate less, not never. Anyone who architects on the assumption that the next release fixes it is building on a schedule they don't control.
- Add a fifth if you like, as a design principle: **make wrong answers cheap.** Don't auto-execute; show the source; let the human confirm the irreversible step. Most real-world safety comes from what the output is allowed to *trigger*, not from the output being perfect.
- Note the honest limitation of "type it": a schema guarantees the *shape* is right, not that the *content* is true. `{"policy_number": "HR-4471"}` is perfectly valid JSON and may be entirely fictional. Say this explicitly — it prevents a false sense of safety this afternoon.

---

## Slide 18 · Four ways to make a model useful

- **The spine table. Prompting → RAG → Tools → Fine-tuning, ordered by cost, and you should try them in exactly that order.**
- **Prompting: minutes, free. Always first.** Roughly 80% of the improvement people chase with fine-tuning is available here for the price of an afternoon.
- **RAG: days, low cost. Use when the model needs knowledge it doesn't have** — your policies, your handbook, anything internal or newer than the training cutoff.
- **Tools: days, low cost. Use when it needs live data or needs to *act*** — today's stock price, this customer's balance, sending the email. Retrieval is reading; tools are reading *and* writing.
- **Fine-tuning: weeks, high cost. Use when you need a style, format, or domain register that prompting cannot hold** — and when you have hundreds to thousands of clean labelled examples, which most teams do not.
- **The killer clarification: fine-tuning teaches a model *how to say things*, not *what is true*.** Fine-tuning on your policy documents does not reliably install those policies as facts — it teaches the model to sound like your policy documents, which is arguably worse, because now it hallucinates in your house style.
- **"Most people reach for fine-tuning and should have reached for RAG"** — because fine-tuning sounds like the serious engineering answer, and retrieval sounds like a workaround. It's the other way round.
- They're combinable and often should be: RAG for the facts, a few-shot prompt for the format, fine-tuning only if the format still won't hold. Also worth naming: fine-tuning creates a maintenance burden — every base-model upgrade means retraining.

---

## Slide 19 · Part Two — Make it reliable

- **The pivot: everything before this was how the model works; everything after is what you do about it.**
- **Start with prompting because it's free and it's where most of the improvement actually lives.** Frame it as engineering, not wordsmithing — you're specifying an interface in natural language.
- Good energy-management moment: this is roughly where attention dips. Change register — more examples, more "what would you do", fewer mechanisms.

---

## Slide 20 · System instruction vs user message

- **System = who the model is, what it may do, how it answers. Set by you, the developer. Re-sent on every call.**
- **User = the question. Comes from outside. Possibly from someone who does not wish you well.**
- **The mental model that matters: this is the same boundary as trusted server code vs untrusted form input.** Every instinct they have about validating web form input applies here.
- Practically, providers train models to weight system content more heavily, and it works most of the time. Put durable policy in system — role, refusal rules, output format, tone, scope limits. Keep per-request content in user.
- **The uncomfortable truth to plant for Thursday: both end up as text in the same context window.** The separation is a strong convention enforced by training, not a hardware boundary or a permission system. There is no privilege bit.
- That's why prompt injection is a genuinely unsolved class of problem, not a bug with a patch: an instruction hidden inside a retrieved document arrives in the same channel as your policy. Say "we will break this on Thursday" and leave it there — don't teach the attack yet.
- Practical hygiene worth stating now: never concatenate user text directly into your system instruction. It's the LLM equivalent of string-concatenating SQL.

---

## Slide 21 · Anatomy of a prompt that holds

- **Five components: Role, Context, Task, Format, Examples.** Treat it as a checklist, not a template — when a prompt misbehaves, walk the five and find the missing one.
- **Role** — who is answering and what they're accountable for. Sets vocabulary and register, and gives the refusal rules something to attach to ("as an HR assistant, you do not give legal advice").
- **Context** — documents, data, conversation, *clearly delimited*. Delimiters (`<document>…</document>`) do two jobs: they mark where instructions end and content begins, and they give you something to reference unambiguously ("summarise the text inside `<document>` tags").
- **Task** — one instruction, imperative. Three questions in a paragraph reliably gets you one and a half answers. If you truly need three things, ask three times or ask for three named fields.
- **Format** — exactly what shape comes back. **Nine failures out of ten are here.** "Be concise" is not a format; "under 50 words, three bullets, no preamble" is.
- **Examples** — one or two done correctly, worth more than another paragraph of instruction.
- Order matters more than people expect: put the instruction *after* long context, since material near the end of the window gets attended to most reliably. For very long documents, sandwich it — instruction, document, instruction restated.
- Negative instructions are weak ("do not mention pricing" often surfaces pricing). Prefer positive specification of what you *do* want.
- A prompt is a source artefact. It belongs in version control, with the model name and temperature next to it, because changing any of the three changes behaviour.

---

## Slide 22 · Show it, don't tell it

- **Zero-shot gives you a different shape every run — unparseable. Two examples give you the same shape every time.**
- **Examples do three things at once that instructions can't: they demonstrate the output shape, the level of detail, and the vocabulary.** Much faster than describing all three in prose.
- The formal name is **in-context learning / few-shot prompting** — the model isn't learning in any persistent sense, it's pattern-matching within this one call. Nothing is retained after the response.
- **Two or three examples is normally enough. If you're at ten and still fighting, that's a genuine signal for fine-tuning** — one of the few honest triggers for it.
- Practical rules for choosing examples: cover the *edge* cases, not the obvious ones; keep them consistent in format down to punctuation, because the model copies inconsistency too; include a hard or ambiguous case with the answer you actually want.
- Watch for label bias — if all your examples end in `high`, expect more `high`. Balance the classes.
- Examples cost tokens on every single call, forever. That's the honest trade against fine-tuning at high volume, and it comes back on Wednesday when you price this.
- **"Notice what the right-hand column bought us — output we can parse."** That is your bridge into Part Three. Then immediately undercut it: splitting on a pipe still assumes the model always emits a pipe. Which it won't. Which is why we need something stronger than a good example.

---

## Slide 23 · Part Three — Make it typed

- **The claim: this is the half hour that earns the word "applied", and it's what most generative AI courses leave out.**
- **The distinction to hold: everything so far made the model *behave* better. This makes its output something *software can depend on*.** Behaviour is a hope; a type is a contract.
- Energy note: this is the peak of the day. Slow down, don't rush slides 24–26, and make sure everyone is actually looking at the screen for slide 26.

---

## Slide 24 · Free text is unusable inside software

- **Same request, three runs, three shapes: a sentence, a key-value block, a chatty preamble. Now write the `if` that routes the urgent ones.**
- Let the room sit in that for a beat. Ideally ask someone to say out loud what their regex would be, then break it with the third example. Discovered pain beats described pain.
- **The instinct is a smarter parser. That's the wrong move — you're patching a symptom of an unconstrained interface.** Every regex you add is a new failure mode that fires in production and never in testing.
- Why the shapes vary at all: sampling (slide 15) plus no format specification. Even at temperature 0, a slightly different input produces a differently-shaped output, because shape was never constrained — only content was requested.
- The chatty-preamble case is worth calling out separately: "Sure! Here's what I found…" is an artefact of chat-assistant training. The model is being helpful *to a human reader*, and your parser is not a human reader.
- **"The fix is not a better parser — it is a contract."** Something the model must satisfy *before the response reaches your code*.

---

## Slide 25 · Ask for JSON, and define the shape

- **`response_mime_type="application/json"` — no prose, no markdown fence, no preamble. That's the first highlighted line.**
- **`response_schema=schema` — and *which* JSON. That's the contract itself, and it's the second highlighted line.** Two lines are what change the behaviour; everything else is ordinary setup.
- **The schema is plain JSON Schema — the same thing you'd write for an API.** That's the point, and it's the sentence that makes the developers in the room relax. Nothing new to learn.
- **`enum` on `urgency` is the highest-value line on the slide.** It's the difference between branching on three known values and parsing English adjectives forever. The model *cannot* return "quite urgent". Not "is discouraged from" — cannot.
- **`required` guarantees the keys exist**, so `data["urgency"]` won't raise a KeyError. Note what it doesn't guarantee: a required string can still be `""`.
- **`temperature=0` because this is extraction. There is no creativity wanted in a field value.** Tie it back to slide 16 explicitly — this is the rule being applied, not a new idea.
- The mechanism worth mentioning, because it separates this from "asking nicely": constrained decoding. The schema is compiled into a state machine over the token vocabulary, and at each step tokens that would break the schema are masked out before sampling. It's structurally impossible to emit invalid JSON. That's a stronger guarantee than any instruction in a prompt.
- **The SDK also accepts a Pydantic model in place of the dict** — and that's what you'd use in a real project: one definition that is simultaneously the API contract, the validator, and the type hint your IDE understands.
- Design advice they'll thank you for later: keep field names descriptive (`urgency` not `u`), because names are semantic signal to the model, not just labels. And add an explicit `"unknown"` or `"other"` enum member — without an escape hatch, an ambiguous input gets forced into a wrong bucket with false confidence.
- Honest caveat, repeated from slide 17: valid does not mean true. The schema constrains the shape. Monday constrains the substance.

---

## Slide 26 · This is the moment

- **`json.loads(resp.text)` returns a real dict. Then `if data["urgency"] == "high": page_duty_officer(data)` — ordinary Python, branching on a typed value.**
- **Stop here. This is the slide the whole day was built towards.** Say that, and then actually pause.
- **The key observation: that `if` statement doesn't know or care that a language model produced the dictionary.** The LLM has become an implementation detail of one function. Everything downstream — tests, monitoring, type checking, code review — works normally again.
- **No regex, no string matching, no "if the answer contains the word urgent".**
- What this unlocks, concretely: you can unit-test it with fixtures; you can swap the model without touching the caller; you can log structured fields instead of blobs; you can put it behind an interface and mock it.
- **`resp.usage_metadata` → `prompt_token_count`, `candidates_token_count`. That is your bill, on every single call.** Tell them to log it from day one. On Wednesday, the people who logged tokens can price their product; the people who didn't will be guessing.
- Still wrap the `json.loads` in a try/except in real code — constrained decoding is very strong, but truncation at `max_output_tokens` produces valid-schema-so-far JSON that is nonetheless unparseable. A schema doesn't protect you from a length cap.
- **"Everything on Tuesday — tools, agents — is this idea again, in a loop."** A tool call *is* a typed output: the model emits a function name and typed arguments, your code executes it, and the result goes back in. If they understand slide 26, they already understand the core of agents.

---

## Slide 27 · Wrap it once, use it all week

- **One `ask()` function: prompt, system, temperature, optional schema, retries. Given complete in the notebook — read it, don't retype it.**
- **What it buys: one place to change the model name; retries with backoff; and schema-optional behaviour — prose when you want prose, typed data when you don't.**
- **The `if schema:` branch is the design point.** The two JSON config lines only appear when a schema was passed, and the return value switches between a parsed dict and raw text accordingly. One function, two honest modes.
- **`time.sleep(2 ** n)` → 1s, 2s, 4s. That's exponential backoff**, and the reason for it is that hammering a rate-limited endpoint at a fixed interval makes the situation worse, for you and for everyone sharing the quota.
- Add jitter in production (`2**n + random()`): without it, every client that failed at the same moment retries at the same moment, and you've built a synchronised stampede.
- **Catching bare `Exception` is deliberately blunt for teaching** — say so, and say what replaces it on Wednesday: retry only what is retryable. 429 (rate limit) and 5xx (transient) yes; 400 (malformed request) and 401 (bad key) no, because retrying a bad request three times just gets you three failures and a longer wait.
- The pattern generalises: this is a thin **anti-corruption layer** between your code and a vendor SDK. When the provider changes their API — and they will — you edit one function instead of forty call sites.
- Things they'll want to add by Wednesday: a timeout, structured logging of the token counts, a cache keyed on (prompt, model, temperature), and a `max_output_tokens`.

---

## Slide 28 · The model is not the solution

- **Six layers: Application, Orchestration, Model, Tools, Data, Governance. The model sits in the middle and is the easiest one to replace.**
- **Application** — what the user touches: streaming, citations, and honest failure states. That last one matters most; "I couldn't find that in your documents" is a *feature*, and it's the hardest thing to get a model to say.
- **Orchestration** — prompts, chains, the agent loop, retries. Where your actual logic lives. Today's `ask()` is the seed of this layer.
- **Model** — swappable, and should be. If swapping it is hard, that's a design smell, and it's a commercial risk too: capability and price move every few months.
- **Tools** (Tuesday), **Data** (Monday), **Governance** (Thursday) — guardrails, logging, audit, privacy, evaluation.
- **"You spend maybe 10% of your time on the model layer. The other five are the job."** This is the slide to quote back at anyone who says "we're building an AI solution" — ask which of the six they've designed. Usually the answer is the middle one only.
- The expensive layers are Data and Governance, and both are mostly organisational rather than technical: who owns the documents, who approves the answers, what gets logged, what happens when it's wrong. Worth naming for the managers in the room.
- Note also that the six layers map onto ownership: in a real org, different teams own different rows, which is exactly why the interfaces between them need to be typed.

---

## Slide 29 · The solution lifecycle

- **Six steps: Frame → Choose → Prototype → Evaluate → Harden → Operate.** The project this week walks 1–5, and Thursday morning is a compressed 6.
- **Frame** — the use case, the user, and what "good" means, *written down before any code*. If you can't define good, you cannot tell whether you succeeded, and you will ship on vibes.
- **Choose** — prompting, RAG, tools, or fine-tuning. The simplest thing that could work (slide 18's table).
- **Prototype** — one notebook, one happy path, real data. Days, not months. Real data from the start, because demo data hides every problem you actually have.
- **Evaluate** — a golden set and a number. **"It looked right" is not a result.**
- **Harden** — retries, caching, guardrails, and cost and latency you have *measured*.
- **Operate** — log, trace, watch, re-evaluate. **It drifts, and so do your documents** — the policy gets updated and your retrieval quietly returns the old one.
- **"Most teams skip step 4 and then cannot tell whether step 5 helped."** This is the sentence that explains the pilot-to-production graveyard. Without a number, every change is an opinion, and the team argues instead of measuring.
- The golden set doesn't need to be big to be useful — 30 to 50 real questions with agreed answers already beats intuition decisively. Tell them that now, because "we don't have an eval set" is usually "we imagined it had to be enormous".
- **Tomorrow afternoon they build that golden set on their own documents** — which is why tonight's homework matters.

---

## Slide 30 · Lab · Notebook 1

- **Six tasks: first call and token counts → Arabic vs English → temperature 0.0 vs 1.2 (three runs each) → two personas, one prompt → JSON mode with a schema and branching → the `ask()` wrapper, given complete.**
- **Each task maps to a slide** — say which, so the lab reads as confirmation rather than new material.
- **Everyone creates their own key.** A shared key means a shared rate limit, and the first person to write a loop throttles the entire room. This is a practical certainty, not a policy preference.
- **Put it in Colab Secrets as `GEMINI_API_KEY`, not in a cell.** The most common failure in the next ten minutes is the key not being in Secrets, or the notebook's access toggle not being enabled for that secret — put the key panel on screen before they start.
- Second most common failure: pasting the key with a trailing space or newline. Third: an old `google-generativeai` install shadowing the new `google-genai` SDK — different package, different import.
- **Take the privacy line seriously: free tier, so no real SDAIA data, no personal data. It may be used to train the model.** This is exactly the paid-vs-free distinction that matters in an enterprise setting, and it returns on Thursday.
- While circulating: the people to check on first are the non-coders in each pair — the failure mode is a coder quietly doing all the typing. Ask the non-coder to explain what the schema is doing.
- Have a fallback ready for anyone whose key won't provision: pair them up, and let them drive while the partner types.

---

## Slide 31 · What today was

- **Four things: (1) tokens are the unit of everything, and Arabic costs 2–3× more; (2) it predicts likely text, not true text; (3) prompting is the cheapest improvement available; (4) a schema turns output into a contract.**
- **If they remember one thing, make it number four** — the schema is what made the output safe to build on, and it's what turns a demo into a component.
- Re-show slide 9 here and do the promised check: hands up per outcome. Any outcome with weak hands is a five-minute recap tomorrow at 9:15, not a hope.
- **"Tomorrow the model still doesn't know *your* documents. We fix that, and then we measure it."** The second clause is the one to stress — anyone can bolt on retrieval; almost nobody measures whether it helped.
- Good closing question to leave hanging: today you constrained the *shape* of the answer. What still constrains the *substance*? Answer: nothing yet. That's tomorrow.

---

## Slide 32 · Two things tonight

- **1 · A GitHub account** — the project gets pushed on Thursday. Get it done tonight, not Thursday morning.
- **2 · Pick your documents — 10 to 30 pages you genuinely care about.** A policy, a manual, a handbook. Theirs, not a demo set.
- **Everything for the rest of the week runs on that document set**, so this is the highest-leverage 20 minutes they'll spend all week. The people who bring documents they care about are the people still working on this in three weeks.
- **Nothing confidential — it goes through a free tier.** A public policy, a published manual, a standards document, or their own university notes are all ideal.
- Practical guidance to save Monday's morning: text-based PDFs or plain text, not scans (no OCR on Monday); 10–30 pages, because a two-page document makes retrieval look pointless and a 500-page one makes chunking a debugging exercise; and it should be a document set they can genuinely imagine asking questions of.
- Have 2–3 spare public document sets ready on a shared drive for whoever arrives empty-handed — someone always will, and you don't want them idle for the most important day of the week.
- **"See you at nine. We start at nine fifteen."**
