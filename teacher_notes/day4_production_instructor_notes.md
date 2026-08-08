# Day 4 — Production and the numbers · Instructor notes
**Applied Generative AI · SDAIA Academy · Wednesday 5 August 2026**

---

## How to read this

- One section per slide, in deck order, numbered **1–22 to match the deck's own footer**.
- **Bold = what is actually on the slide, unpacked.** Read these and you have covered the slide.
- Plain text = depth to have ready that is *not* on screen: mechanism, anticipated questions, honest caveats.
- Bullets run foundation → detail → payoff. Stop anywhere and you have still said something complete.
- Every bullet is a full sentence you can say out loud without supplementing from memory.

**On the two code slides.** The PDF is 24 pages and the footer counts 22, because the code slides carry no chrome. Per your instruction they get no section of their own — their content sits inside the section for the slide they follow, under a **`▸ CODE SLIDE`** subheading. So the streaming-and-cache code is inside Slide 14, and the retry-and-fallback code is inside Slide 15. Bugs in that code are still in the fix list, because they will still be on the projector.

**One new slide.** You asked for a deployment-toolbox slide after Slide 19. The full spec and its notes are at the end of this file, under **"New slide · insert after Slide 19."** Adding it makes the deck 23 numbered slides and shifts the current 20, 21 and 22 to 21, 22 and 23.

---

## Shape of the deck

**Frame (1–5, ~10 min).** Title, week map, day map, objectives, three recall questions from Day 3. The recall questions are diagnostic, and question two is deliberately cost-shaped so it walks you straight into Part One.

**Part One — The gap (6–9).** Divider, the prototype-vs-production table, the four scale levers, and the 429 callback to Monday. This section's job is to make them uncomfortable about systems that currently work.

**Part Two — The arithmetic (10–13, plus the live calculator).** Divider, what you are paying for, the on-screen calculator, and the Arabic cost multiplier. This is the twenty minutes with the highest career value in the week and you should say so.

**Latency and reliability (14–15, with their code slides).** Four real speedups plus streaming; then timeouts, backoff, fallbacks and circuit breakers. Both slides have code immediately after them.

**Measurement and operations (16–19).** The six-number table they will produce, the four observability pillars, the deployed architecture, and UX for a system that is sometimes wrong.

**Lab and afternoon (20–22).** Notebook 4 against their own project, the README clinic, and the four-line recap.

**The throughline in one sentence:** Sunday made the model a reliable function, Monday made retrieval measurable, Tuesday made the model act, and today every one of those decisions gets a price and a latency attached to it.

---

## Slide 1 · Production and the numbers

- **The subtitle is a question — "What does this cost per user per month?" — and it is the question the whole day answers, so read it aloud rather than letting them skim it.**
- **Say the framing plainly: today you stop adding capability and start measuring what they already have.**
- **Promise the deliverable: by noon they will have a table of their own numbers — latency per request, tokens in and out, cost, and a measured cache hit rate.**
- **Say the presenter note out loud, because it is true and it motivates the room: engineers who can answer the question on this slide get hired.**
- Add the reason it is true, since a claim like that needs one: almost everyone in this field can build a demo, and almost nobody can tell you what the demo costs at a thousand users. The scarcity is not technical, it is that nobody bothers.
- **Callback to the whole week:** nothing new gets built today. Every number they measure comes from something they already made on Sunday, Monday or Tuesday.
- **Energy note.** This is Day 4 of five and the room is tired. Open at a higher energy than yesterday and lean on the hiring line.

---

## Slide 2 · Where we stand

- **Sunday, Monday and Tuesday are struck through, Wednesday is highlighted, and only Thursday is left.**
- **Say the shift explicitly: three days of building, and today it gets instrumented instead of extended.**
- **Tomorrow morning they attack each other's systems, so whatever runs today is what gets tested.**
- **The green box about dumb questions is still there — read it aloud, because by Day 4 the people who are lost have stopped asking.**
- Say the thing that makes today feel urgent rather than administrative: anything not working by lunch cannot be instrumented this afternoon, and anything not instrumented today has no numbers for tomorrow's presentation.
- **Ask the room:** "Whose project runs end to end right now?" Count the hands, because that number tells you how to spend Block 4 and you want it before the break, not at one o'clock.

---

## Slide 3 · How the day runs

- **Teaching runs 9:15 to 12:00 in three blocks, then the afternoon is build and the README clinic.**
- **Block 1 is fifty minutes on the gap and the arithmetic, including the Cost Auction activity.**
- **Block 3 at 11:20 runs Notebook 4 against their own project, which means the project has to be working before lunch — say that at 9:15, not at 11:20.**
- **The README clinic at two o'clock is not optional, because fifteen rubric points sit in the repository.**
- **The day ends with the Thursday briefing so nobody spends the evening guessing about the format.**
- ⚠️ **The 2:00–2:00 break is zero minutes long.** Same bug as the Day 3 deck. See fix list item 5.
- ⚠️ Slide 3 gives Block 5 as 2:00–2:30; Slide 21 splits it as README clinic 2:00–2:20 and briefing at 2:20. Those are compatible, but only if you say so.
- **Pacing reality check:** Block 1 has to cover slides 6 through 13 including the live calculator *and* the Cost Auction, in fifty minutes. That is your tightest block of the week. Slides 7 and 8 are your compressible ones; the calculator is not.
- **The Cost Auction appears on this slide and nowhere else in the deck.** See the end of this file — I have written one, since it is promised here and undefined everywhere.

---

## Slide 4 · What you will be able to do by 12:00

- **Five objectives, and number two is the one to dwell on: compute what an assistant costs per user per month, from token counts.**
- **Say why: that is the first question management asks, and almost nobody in this field can answer it without going away for a week.**
- **Number four — measure and report latency, tokens, cost and cache hit rate from real runs — is what they paste into tomorrow's presentation.**
- **Say the thing about persuasion: a real table of their own numbers is far more convincing than any claim about quality.**
- **Number one is the framing objective: name the concrete differences between a notebook and a production system.** Slide 7 is that objective, delivered.
- **Number five is the softest and the most interviewable: say what you would log, trace and alert on before you let anyone use it.** Nobody has to build it; they have to be able to answer it.
- **Ask the room:** "Which of these can you already do?" Very few hands on two and four is normal, and it tells them the day is worth their attention.

---

## Slide 5 · Three questions before we start

- **Ask three people who did not speak yesterday, take one answer each, and move — five minutes, then you start counting things.**
- **Question two is the bridge into today, because it is the first cost-shaped question of the week.**
- **If nobody gets question two, give it yourself: the conversation history grows with every step, and you re-send all of it every time.**

**Answer key, so you can correct quickly:**

- **Question one — who executes a tool call.** Your application does. The model returns a structured request naming a tool and its arguments; your code reads that request and decides whether to honour it. The model never runs anything.
- **Question two — why step twenty costs more than step one.** Every step re-sends the entire conversation so far, and the conversation has grown by twenty turns. The cost of *n* steps is closer to the sum 1+2+…+n than to *n* times one step, so it grows with roughly the square of the step count.
- **Question three — what a tool returns when it fails, and why.** A readable structured error, not a raised exception. It says what was wrong and what a valid input looks like, so the model can correct itself on the next pass. An exception kills the loop, and a swallowed exception makes the model invent an answer.
- If someone gives a partial answer to question two — "because the history is bigger" — push once for the shape. "Bigger" earns the point; "it accelerates rather than growing evenly" is the answer that makes today's cache lesson land.

---

## Slide 6 · Part One — The gap

- **A divider, and the subtitle is the definition: everything that is fine in a notebook and not fine with five hundred users.**
- **Open with the compliment, because it is sincere and it buys you the next twenty minutes: their projects currently work, that is genuinely an achievement, and it is also the easiest part.**
- **Then say what is coming: this section is the list of things that break the first week something real is in front of real people.**
- The tone here matters more than the content. If it sounds like criticism, the room defends its work. If it sounds like "here is what happens next", they lean in.

---

## Slide 7 · Prototype vs production

- **Six rows, notebook on the left and production on the right: users, errors, cost, latency, secrets, change.**
- **Users goes from one — you — to hundreds at the same moment at nine in the morning.**
- **Errors goes from re-running the cell to handled, retried, logged, or shown honestly** — and "shown honestly" is doing work there, because the fourth option is a product decision rather than an engineering one.
- **Cost goes from ignored, because it is free, to measured, budgeted and alerted on.**
- **Latency goes from "you wait, it's fine" to eight seconds of silence losing the user.**
- **Secrets goes from a Colab secret to a secret manager, rotated, never in git.**
- **Change goes from edit-and-re-run to versioned, reviewed and evaluated before release.**
- **Read the last line slowly, because it is the thesis of the day: none of this is AI-specific, it is ordinary engineering that AI projects skip because the demo was so easy.**
- **Say the failure mechanism out loud: generative AI projects almost never fail because of the model. They fail because a two-day prototype convinced everyone the hard part was done, so nothing in the right-hand column was ever budgeted.**
- **Ask the room which row will bite them first.** It is usually cost or latency, and whichever they say, ask "why that one?" — the reasoning is the useful part.
- The "change" row is the one nobody picks and the one that hurts longest. Say briefly that editing a prompt is a code change with no tests, and that Monday's golden set is the only test they have.
- **Forward to Slide 18:** every row on this table is one box on the architecture diagram later. Name that now so the diagram feels like a summary rather than a new topic.

---

## Slide 8 · Four things that decide whether it holds up

- **Four cards — concurrency, async, caching, rate limiting — and the green box says caching is the cheapest of the four and the one most often left out.**
- **Concurrency: fifty people at nine in the morning is fifty simultaneous calls, and one synchronous loop serves them one at a time.**
- **Async: these calls are almost entirely waiting, so async lets one process hold hundreds of open requests.**
- **Say the async point in one sentence of mechanism, because it is not obvious: your process is not computing anything, it is sitting on a socket waiting for a model, so blocking is pure waste.**
- The contrast that makes it click: a CPU-bound task needs more cores; a wait-bound task needs the ability to wait on many things at once, which is a much cheaper thing to buy.
- **Caching: the same question asked by forty people — answer it once, then it is free and instant.**
- **Rate limiting: the provider's limit on you, and the limit you impose on your own users so one script cannot drain the budget.**
- **Rate limiting in both directions is the part people forget** — say that explicitly. A plan for the provider's limit is not the same as a limit on your users, and only the second one stops a single loop from spending your month.
- Worth naming for the government context: an internal tool with a known user list can rate-limit per authenticated user, which is far easier than the public-internet version of this problem. That is one of the genuine advantages of their setting.
- **Forward to Slide 14:** caching appears again there as a latency fix, not just a cost fix. Say "this comes back" so the repetition reads as structure rather than as you losing your place.

---

## Slide 9 · Those 429s were the lesson

- **This is a callback to Monday: when everyone embedded their chunks at once, the room filled with `429 RESOURCE_EXHAUSTED`.**
- **Say the framing that makes it useful: that was a rate limit, they already know how it feels, and their users will feel the same thing unless they design for it.**
- **Say that Monday's rate limit was hit deliberately rather than quietly avoided, because lived experience beats a definition on a slide.**
- **Four responses on the right: batch, backoff, queue, degrade honestly.**
- **Batch means fewer, larger requests** — the same total work, arriving in a shape the provider is happy to serve.
- **Backoff means wait one second, then two, then four, and never retry immediately in a loop.**
- **Queue means smoothing the burst instead of amplifying it** — the work still happens, it just stops arriving all at once.
- **Degrade honestly means "busy, try again in a moment" beats a spinner that never resolves.**
- **Deliver the last line firmly, because it is the one they will remember: a retry without backoff is not a fix, it is a denial of service attack on yourself.**
- Add the mechanism in one sentence: when a provider is overloaded and every client retries instantly, the retries themselves become the load, and a brief limit becomes a sustained outage. Say you have watched it happen.
- Worth mentioning as the professional detail: real backoff adds *jitter* — a small random offset — so that a thousand clients that all failed at the same moment do not all retry at the same moment either. Exponential backoff without jitter still produces synchronised waves.
- **Callback to Monday, forward to Slide 15:** the backoff on this slide is the code on the slide after 15. Say "we write this in twenty minutes."

---

## Slide 10 · Part Two — The arithmetic

- **A divider, and the subtitle is the entire cost model in one line: tokens in, plus tokens out, times a price.**
- **Say the framing note, because it is a genuine motivator: this next twenty minutes is the part of the course that most directly changes how they are seen at work.**
- **Then say the second half, which is the useful part: nobody teaches this, and it is arithmetic. That combination is unusual and worth exploiting.**
- Add one sentence of honesty so it does not sound like a sales pitch: the arithmetic is easy, and the reason people cannot do it is that they never measured their token counts. The work is in the measuring, not the multiplying.
- **Energy note.** This is your best moment of the morning. Raise the energy here and spend it on the calculator.

---

## Slide 11 · What you are actually paying for

- **Every request has two meters: input tokens and output tokens, and output is usually priced higher.**
- **Input tokens are the system prompt, the retrieved chunks, the conversation so far, and the question — in that order of usual size.**
- **Output tokens are what it writes back, and they cost more per token**, which is why "be concise" is a cost control and not just a style preference.
- **In a RAG system the retrieved chunks dominate the input — four chunks of 500 tokens is 2,000 tokens on every single call, before anyone has typed a word.**
- **Point at that line and connect it to Monday: this is the direct consequence of their top-k decision, and it is why "just raise k" is an expensive habit.**
- **Four places the money goes: top-k too high, long system prompts, agent loops, and no cache.**
- **The system prompt point surprises people, so give it the arithmetic: a four-hundred-token system prompt sounds small until you multiply it by forty thousand requests a month, which is sixteen million tokens of the same text.**
- **Agent loops — history re-sent at every step — is yesterday's lesson arriving with a price attached.** Say the callback.
- **No cache means the same question paid for forty times**, which sets up Slide 14 and the calculator.
- Anticipated question: *"Do providers not cache the system prompt for me?"* Several offer prompt or context caching that discounts repeated prefixes, and the discount and the rules vary by provider and change often. Say that it exists, that it can help a lot with a long fixed prefix, and that they should read the current pricing page rather than trust a number from you. **Verify before you present** if you want to say anything specific — this is exactly the kind of detail that moves every few months.

---

## Slide 12 · Work it out on the screen

**This is the centrepiece of the morning. It is a live calculator, so it is also the slide most likely to embarrass you if it does not run.**

- **Eight inputs on the left, four outputs on the right, and the monthly figure is the highlighted one.**
- **The defaults are 500 users per day, 4 queries each, 2,200 input tokens, 400 output tokens, prices of $0.10 and $0.40 per million, 22 working days, and a cache hit rate of zero.**
- **The outputs at those defaults are $0.00038 per query, $0.76 per day, $16.72 per month, and $0.03 per user per month.**
- **Say the note under the inputs: prices are per million tokens and these are placeholders, so put today's real figures in.**
- **Work through the per-query arithmetic out loud once, slowly, because the whole day rests on them believing this box.** 2,200 input tokens is 0.0022 of a million, times $0.10 is $0.00022. 400 output tokens is 0.0004 of a million, times $0.40 is $0.00016. Add them and you get $0.00038.
- **Then scale it in front of them:** 500 users times 4 queries is 2,000 queries a day, times $0.00038 is $0.76 a day, times 22 working days is $16.72 a month.
- **Then change one thing at a time so they can see what moves the total.** Changing two at once teaches nothing.
- ⚠️ **Your presenter note says dropping input tokens from 2,200 to 1,200 makes the monthly figure "fall by nearly half." It does not — it falls by about a quarter.** See fix list item 1. This is the single most important correction in this file, because you will be saying the wrong number while the right one is on screen behind you.
- **The correct version of that move:** dropping input tokens from 2,200 to 1,200 — retrieving two chunks instead of four — takes the monthly figure from $16.72 to about $12.32, which is roughly a quarter off. Say "a quarter off, for a change that takes one line."
- **Then set the cache hit rate to 40% and it falls again**, to roughly $7.39 from the original $16.72. Those two moves together are most of the cost conversation.
- **The reason the input reduction is worth less than people expect is worth saying, because it is the real lesson:** the output tokens did not change and they are priced four times higher, so cutting the input alone cannot halve the bill. That is a better insight than the wrong claim was.
- **Ask the room:** "Which single number would you change first in your own project?" You want someone to say top-k or cache, and either answer earns a follow-up.
- **Set expectations about the size of the answer**, because $0.03 per user per month is anticlimactic and someone will say so. Say it plainly: at these prices, on a cheap model, an internal assistant is cheap. The number gets frightening when the model is expensive, the corpus is Arabic, the top-k is generous and there is no cache — and each of those is a decision, not a fact.
- ⚠️ **Have the numbers written down on paper.** If the calculator does not render in presentation mode you still need to teach this. See fix list item 3.

---

## Slide 13 · The same product costs more in Arabic

- **This is a callback to Sunday, where they measured it: the same sentence is two to three times the tokens in Arabic.**
- **Both meters are affected, and say them separately: Arabic documents make bigger chunks so the input grows, and Arabic answers are more tokens so the output grows.**
- **The bolded line is the payoff: put a bilingual assistant into the calculator and the monthly figure moves materially.**
- **Do that — go back to Slide 12 and multiply the token counts.** Doubling both input and output takes $16.72 to roughly $33.44, and that is a number people react to.
- **Four responses on the right: budget for it explicitly, cache harder, keep chunks tighter for Arabic sources, and measure both languages separately in your logs.**
- **"Cache harder" deserves its one sentence of reasoning: a cache hit on an Arabic question saves two to three times as much as a hit on an English one, so the same hit rate is worth more.**
- **The last bullet is the practical one: log the language on every request, so they can see the split rather than guessing at it.** That is one field in the log line and it makes the next budget conversation trivial.
- **Say the consequence firmly, because it is what makes this slide matter:** if they present a cost estimate to management based on English measurements for a service that will run in Arabic, they will be wrong by a factor that gets noticed.
- The mechanism, if anyone asks why: tokenisers are trained on a corpus that is mostly English, so common English words become one token while Arabic words are often split into several pieces, and the same meaning costs more units. Modern tokenisers have narrowed the gap and have not closed it.
- **Verify before you present:** the "two to three times" figure should be the one *they* measured on Sunday, not a general claim. If Sunday's measured ratio was different, use Sunday's number — it is more persuasive because they watched it happen.
- Worth adding as an honest caveat: the ratio varies with the text. Formal Arabic policy prose behaves differently from short conversational Arabic, and a mixed Arabic-English document is different again. Tell them to measure their own corpus rather than inherit a multiplier.

---

## Slide 14 · Four ways to make it faster, and one to make it feel faster

- **Four cards for real speedups, and a green box for streaming, which is a different kind of thing entirely.**
- **Right-size the model: most requests do not need your best model, so route the easy ones to the cheap fast one.**
- **Cache: a hit is zero latency and zero cost, and nothing else on this slide competes with that.**
- **Shorter prompts: fewer input tokens is less time to first token, so top-k discipline pays twice** — once in money on Slide 11, once in speed here.
- **Batch offline work: embedding, summarising and indexing do not belong on the user's request path.**
- **The green box is the distinction to nail: streaming changes none of the above, it changes when the first word appears, and users read that as speed.**
- **Separate the four real fixes from streaming very clearly, because people conflate them constantly.**
- **Give the numbers: streaming does not reduce total generation time by a millisecond, it moves time-to-first-token from about six seconds to about three hundred milliseconds.**
- **In the notebook they run both side by side with a timer and the total is the same. Tell them to watch for that surprise.**
- The reason this matters as a product point rather than an engineering one: the user has no way to perceive total generation time if words are appearing. Perceived latency and measured latency are different quantities, and only one of them is in your dashboard.
- **Forward to Slide 19:** streaming reappears there as a UX obligation. Name the connection.

### ▸ CODE SLIDE — Streaming, and a cache that pays for itself

*(The unnumbered code slide immediately after this one.)*

- **The streaming block is four lines: a `for` loop over `client.models.generate_content_stream(...)` printing each chunk with `end=""` and `flush=True`.**
- **`end=""` stops Python adding a newline after every chunk**, which is what makes the output read as one continuous sentence rather than a column of fragments.
- **`flush=True` forces the text out immediately instead of sitting in a buffer** — without it the whole point is lost, because the words appear all at once at the end and it looks exactly like non-streaming.
- **Say that: `flush=True` is the difference between a streaming demo and a broken streaming demo.** It is one keyword and it is the one people omit.
- **The cache is presented as twelve lines and "the best value in the file," and that framing is fair.**
- **`hashlib.sha256((prompt + json.dumps(kw, sort_keys=True)).encode()).hexdigest()` builds the key from the prompt *and* the settings.**
- **`sort_keys=True` is load-bearing:** without it, the same settings in a different order produce a different JSON string and therefore a different key, and your cache silently misses on requests it should have hit.
- **Hashing rather than using the prompt directly keeps keys short and fixed-length**, which matters when this becomes Redis rather than a dictionary.
- **The first note on the right says a different temperature is a different question**, and that is why the settings are in the key at all.
- **The second note is the one to say twice: count hits and misses from the start, because an unmeasured cache is a guess.**
- **The third note is the honest one: in production this is Redis with a time-to-live, not a dict, but the shape is identical.**
- **The last line on the slide is the trap: a cache with no expiry serves yesterday's policy after it changed, so set a TTL.** In a government policy assistant that is not a performance bug, it is a correctness bug with consequences.
- ⚠️ `stats` and `ask` are referenced and defined nowhere on the slide. See fix list item 7.
- ⚠️ The code has no TTL even though the slide's own last line demands one. That is arguably fine as a teaching sequence — show the simple version, then name what is missing — but say it out loud, or a sharp student will think you did not notice.
- **Arabic note worth thirty seconds:** cache keys are exact-match on the prompt string, and Arabic text can be byte-different while appearing identical — different forms of alef, presence or absence of diacritics, Arabic-Indic versus Western digits. Two users asking the same question in Arabic can produce two different keys and two cache misses. Normalising the text before hashing raises the hit rate measurably, and it is a one-line change that nobody makes.

---

## Slide 15 · Assume every call can fail

- **Four controls on the left, and a clear statement on the right about which errors are worth retrying.**
- **Timeout: never wait forever, and decide the number** — the point being that a timeout you did not choose is still a timeout, it is just whatever the library's default happens to be.
- **Retry with backoff: one second, two, four, then give up.**
- **Fallback chain: primary model, then a cheaper one, then a canned response.**
- **Circuit breaker: if it is failing for everyone, stop trying for a minute.** The reasoning: when a provider is down, your retries add load to a system that is already struggling and burn your budget on calls that cannot succeed.
- **The right-hand panel is the distinction that matters: a 429 or a 503 will probably succeed in two seconds, and a 400 will fail identically forever.**
- **Say why that distinction is worth money: retrying a 400 wastes your budget and your user's time, and it will do so on every single request of that shape, forever.**
- **The canned response matters, and the example on the slide is the right shape: "I can't reach the assistant right now — here is the policy page" is a better product than a spinner.**
- **The green box is the line to deliver firmly: users will forgive a degraded answer, and they will not forgive a page that hangs.**
- **The fallback chain is easy to build and almost never built — two lines of code turn a total outage into a slightly worse answer.**
- **In the notebook they break the primary model on purpose and watch the fallback engage.** Say that now so the notebook cell has a purpose before they reach it.
- Worth adding for the government context: "degrade honestly" is also a compliance-friendly position. A system that says it could not answer is defensible; a system that guesses confidently when its retrieval failed is not.

### ▸ CODE SLIDE — Retry, then fall back

*(The unnumbered code slide immediately after this one.)*

- **`RETRYABLE = (429, 500, 502, 503, 504)` is the whole policy in one line, and it is deliberately a short list.**
- **`def retry(tries=3, base=1.0)` is a decorator factory — a function that returns a decorator — and that three-level nesting is the thing that will lose the non-coders.**
- **Explain it once in plain language: `retry(tries=3)` is called first and hands back a decorator, that decorator wraps your function, and the wrapper is what actually runs when you call it.** The three levels exist only so that you can pass arguments like `tries=3`.
- **`@functools.wraps(fn)` copies the original function's name and docstring onto the wrapper**, so error messages and logs name the real function instead of saying `wrapper`. It is a one-line courtesy that saves an hour of confused debugging later.
- **`for n in range(tries)` bounds the attempts, exactly like yesterday's step cap** — say the callback, because it is the same idea in a different costume.
- **`if e.code not in RETRYABLE or n == tries - 1: raise` is two conditions in one line and both matter:** do not retry an error that cannot succeed, and do not swallow the failure on the final attempt.
- **`time.sleep(base * 2 ** n)` produces 1, 2 and 4 seconds** because `2 ** n` for n of 0, 1, 2 is 1, 2 and 4. Point at the arithmetic; several people will not see it.
- **`ask_with_fallback` loops over `(PRIMARY, CHEAPER)` and returns the first success, and returns `CANNED` if both fail.**
- **The comment on the last line is the product decision: honest, useful, never a spinner.**
- ⚠️ **The `retry` decorator is never actually applied to anything on this slide.** See fix list item 6 — this is the bug most likely to be noticed by a sharp student.
- ⚠️ `ApiError`, `ask`, `log`, `PRIMARY`, `CHEAPER` and `CANNED` are all undefined here. Fine as a slide showing the interesting lines; say "the plumbing is in the notebook" before someone asks.
- ⚠️ **`except Exception` in `ask_with_fallback` will also catch a `400`,** meaning a malformed request falls back to the cheaper model and then to the canned response, quietly, instead of surfacing a bug in your own code. That directly contradicts the retryable/non-retryable lesson on the slide beside it. See fix list item 6 for the fix — and note that keeping it makes an excellent exercise if you flag it deliberately.
- **No jitter in the backoff.** Correct for a teaching slide, worth one sentence: real backoff adds a small random offset so a thousand clients that failed together do not retry together.

---

## Slide 16 · The table you will produce today

- **Six metrics, each with an illustrative value and a reason it matters — and the point is that by noon they will have their own.**
- **Median latency, 2.1 seconds: what a typical user waits, and the thing to optimise first.**
- **p95 latency, 6.8 seconds: the bad experience, and what people actually complain about.**
- **Explain the median-versus-p95 distinction properly, because it is the single most useful idea in performance work and almost nobody arrives knowing it.** The median is the middle request when you line them all up. The p95 is the request that 95% of requests were faster than — so one user in twenty has an experience at least that bad, and with four queries each, a large fraction of users hit it at least once during a session.
- **Say the consequence: a median of two seconds and a p95 of nine seconds is a system that feels fast in your testing and slow to your users**, and averages hide this completely, which is why the table has no average latency in it.
- **Average input tokens, 2,240: mostly retrieved chunks, directly set by their top-k.**
- **Average output tokens, 380: priced higher than input, so shorter answers are cheaper answers.**
- **Cache hit rate, 38%: measured, not hoped for — every hit is free and instant.**
- **Cost per query, $0.00037: multiply by traffic and you have the monthly number.**
- **The green box is the claim to make confidently: six numbers, and with them they can answer any question management asks about this system.**
- **Say the figures are illustrative and theirs will differ, because the point is ownership, not these values.**
- ⚠️ **The table does not say whether cost per query is before or after the cache saving, and it changes the number by nearly 40%.** See fix list item 2 — they will hit this ambiguity the moment they build their own table.
- **Say what you want them to report, explicitly:** the raw cost of a query that actually calls the model, *and* the effective cost across all queries once the cache is counted. Two numbers, clearly labelled, and the second is the one that goes to management.
- **Put this table in tomorrow's presentation** — pairs who show measured numbers read as engineers, and pairs who say "it feels fast" do not.

---

## Slide 17 · If you cannot see it, you cannot run it

- **Four pillars: logging, tracing, metrics, and continuous evaluation.**
- **Logging is per-request: prompt id, tokens in and out, latency, model, cache hit, cost, outcome.** That list is a schema — tell them to write those eight fields into a dataframe from the start of their project and they get every metric on Slide 16 for free.
- **Tracing is one request across every step — retrieval, each tool call, generation — as a single timeline.**
- **Tracing is the one that is specific to this kind of system, and it is worth its own sentence: a single user question can become five model calls, and without a trace you cannot tell which one was slow or wrong.**
- **Metrics are the aggregates: p50 and p95 latency, error rate, cost per day, cache hit rate, tokens per request.**
- **Continuous eval is Monday's golden set, run on a schedule** — because documents drift, models change, and quality moves without anyone touching the code.
- **Say that clearly, because it is the payoff of Monday's afternoon: the golden set was not an exercise, it is the regression test for a system that has no other tests.**
- **The tools named are LangSmith, Langfuse and Phoenix — name them and do not sell them.**
- **Say what they build today instead: a dataframe and a plot, which is enough to understand what those products are for.** That is the honest framing, and it means nobody feels they are missing a paid tool.
- **Forward to the new toolbox slide:** these three names reappear there alongside the rest of the deployment stack. If you are adding that slide, say "we will see where these sit in a moment."

---

## Slide 18 · What the whole thing looks like deployed

- **One wide box for the user interface across the top, then eight boxes in two rows for everything underneath.**
- **User interface: web or chat, with streaming, citations, and honest failure states** — all three of which are Slide 19's content.
- **API layer: auth, rate limiting per user, request logging.**
- **Orchestration: prompts, the agent loop, retries, guardrails** — this is Tuesday plus this morning, in one box.
- **Cache: checked before any model call is made.** The position matters: the cache is *above* the model, not beside it, which is why a hit costs nothing at all.
- **Model: primary and fallback, swappable behind one interface.**
- **Vector store: their chunks and metadata** — Monday, in one box.
- **Tools: internal APIs, least privilege** — Tuesday, in one box.
- **Monitoring: logs, traces, metrics, alerts** — Slide 17, in one box.
- **Governance: audit trail, PII controls, evaluation runs.**
- **Walk the request through the diagram once, out loud, from the top:** interface, API layer, cache check, orchestration, retrieval, model, and back up with a citation. Trace it with your finger.
- **Then make the callout point: one box on this whole diagram is the model, and it is the box they will spend the least time on.**
- **Say the reassurance clearly: none of this is required for their project — it is the map for what happens after this week.** Without that sentence, this slide reads as a list of things they have failed to do.
- **Governance is the box to linger on for half a sentence in this room**, because in a government context the audit trail and the PII controls are not optional extras added later, they are usually part of the approval to run at all.
- **Callback to Slide 7:** every row of the prototype-vs-production table is a box on this diagram. Say it — it turns two slides into one idea.

---

## Slide 19 · UX for something that is sometimes wrong

- **Four do's and four don'ts, and the green box is the thesis: citations are not decoration, they are how a user decides whether to believe you.**
- **Do stream, so it feels alive within a second** — the Slide 14 point, now as a product obligation rather than a performance trick.
- **Do cite, with source and page, clickable, because trust comes from checkability.**
- **Do say "I don't know" and mean it, when retrieval came back empty.**
- **Do show the failure plainly, with something useful to do next.**
- **Don't hide that an AI produced it.**
- **Don't present an unsourced answer with the same confidence as a sourced one** — this is the subtlest item on the slide and worth a sentence: the interface should look different when the answer came from retrieved documents than when it did not.
- **Don't leave a spinner running when the call has already failed.**
- **Don't make the user retype the question after an error.**
- **Say the government-context point: the citation is the feature.** An answer someone can verify in ten seconds is worth more than a better-written answer they cannot check.
- **Say the hard truth about "I don't know": it needs building deliberately, because it does not happen by default** — the model's default behaviour is to produce something. And it is the thing that makes every other answer credible, because a system that never says "I don't know" gives you no signal at all.
- The practical implementation, if anyone asks: check whether retrieval returned anything above a relevance threshold *before* calling the model, and if it did not, do not call the model at all. That is cheaper and more reliable than asking the model to abstain.
- **Arabic/RTL, and this is the slide where it belongs:** citations in a right-to-left interface need care, because a source name in Latin script inside an Arabic sentence is a bidirectional run and can render in a confusing order — a page number can appear to belong to the wrong document. Tell them to test their citation rendering with real Arabic text before Thursday, because a broken citation undermines exactly the trust the citation was there to build.

---

## Slide 20 · Instrument your own project

- **The notebook is `day4_production.ipynb` and it has five parts listed on the left.**
- **A retry decorator with backoff, and a forced failure to prove it fires** — the forced failure is the important half, because untested error handling is not error handling.
- **Streaming against non-streaming, timed, so they see that the totals match.**
- **A cache, then twenty queries with eight repeats, to measure the hit rate.**
- **Log every request into a DataFrame and `describe()` it** — one method call that gives count, mean, standard deviation and the quartiles, which is where the median comes from.
- **Plot latency and cumulative cost, and fill in the cost formula themselves.**
- **The right panel is the important framing: this one runs against *their* project, not a toy, importing their own retrieval and agent functions from the last two days.**
- **They finish with a table of their own numbers, and that table goes in tomorrow's presentation.**
- **Say why the cost formula is deliberately left blank: reading a pricing page is a skill, and the prices change every few months.** A formula they filled in from a real pricing page today is one they can re-fill in six months; a formula you gave them is one they will re-use after it is wrong.
- **Say the warning loudly at 11:20, not at 1:00: if their project is not running yet, they should come and find you now, because this notebook needs something to instrument.**
- ⚠️ **Twenty queries with eight repeats gives a hit rate of exactly 40% every time, by construction.** Say that out loud rather than letting them think they measured something: the number is set by the test list, not by user behaviour, and a real hit rate only comes from real traffic. It is still worth doing, because the *machinery* is what they are testing.
- ⚠️ Slide 16's illustrative hit rate is 38% and the lab produces 40%. Harmless, but if someone asks, the honest answer is that 38% is meant to look like a real measurement and 40% is an artefact of the exercise.
- **What to look for while circulating:** pairs who instrument a toy function instead of their own retrieval, because it is easier. They will finish early and have nothing to present tomorrow. Push them back to their own code.
- ⚠️ **I have not seen `day4_production.ipynb`.** Everything above is read off this slide. Send it over and I will do a cell-by-cell pass like the Day 3 one — given the Day 3 notebook had never been run, that is worth doing before tomorrow.

---

## Slide 21 · Build, then the README clinic

- **The afternoon splits in two: build from 1:00 to 2:00 with you circulating, then the README clinic from 2:00 to 2:20.**
- **The build goal is specific: get the numbers table out of Notebook 4 and into their repository.**
- **Every pair writes their README during the clinic, with you checking, and all six SDAIA requirements go on screen.**
- **Say the reason firmly: READMEs written the night before are always bad, and this is not negotiable.**
- **Be firm about it — fifteen points of the rubric are repository quality, and it is the cheapest fifteen points available.**
- **At 2:20 you brief tomorrow's format: four minutes, plus two for questions.**
- **Say the last line clearly, and say it again tomorrow morning: an honestly-explained broken demo scores better than a fake working one.** Somebody's demo will break, and knowing this in advance is what stops them panicking or faking it.
- The reason that rule is not just kindness: a pair who can explain exactly why their demo failed has demonstrated they understand their own system, which is what you are assessing. A pair with a working demo they cannot explain has not.
- **What to look for during the clinic:** READMEs that describe what the code does and never say how to run it. The single most common gap is a missing "how to set the API key" line, which is the one thing the next person needs first.

---

## Slide 22 · What today was

- **Four lines, and the fourth is bolded because it is the one that separates them from most people who will claim this on a CV.**
- **First: the gap between a notebook and a system is ordinary engineering, and it is where these projects die.**
- **Second: cost is tokens in, plus tokens out, times a price — and they can now answer it for their own project.**
- **Third: retries, caching and fallbacks are a day's work, and they change what you can promise.**
- **Fourth: they measured their own system. Not estimated — measured.**
- **Set up tomorrow concretely: they try to break each other's systems, so bring the project running and bring a sense of humour.**
- **Say the logistics twice, because it is the last thing before they leave: the post-test is at quarter past nine, first thing, and they should not be late for it.**
- Close with one line of your own that the day has earned: the difference between "it feels fast" and "the median is 2.1 seconds and the p95 is 6.8" is the difference between someone describing a demo and someone running a system.

---

# New slide · insert after Slide 19

You asked for something in the shape of Slide 18 but naming the actual frameworks and services, so you can point students at them without opening any of them. Here is the slide content and then the notes.

Placement after Slide 19 is right: Slide 18 is the boxes, Slide 19 is the product surface, and this is "here is what fills the boxes" — landing immediately before the lab brief. **Adding it makes the deck 23 numbered slides**, so the current 20, 21 and 22 become 21, 22 and 23, and the footer total changes from 22 to 23.

## Slide content

**Kicker:** `THE TOOLBOX`
**Title:** What you would actually build it with

**Wide box across the top:**

> **BEFORE YOU PICK ANYTHING**
> Where the data is allowed to live decides the shortlist. Residency, hosting region and procurement come before any feature comparison.

**Eight boxes, two rows of four:**

| | |
|---|---|
| **ORCHESTRATION**<br>LangChain · LlamaIndex · Haystack · plain Python<br>Glue for prompts, retrieval and the agent loop. | **VECTOR STORE**<br>pgvector · Qdrant · Chroma · Milvus<br>Where your chunks, embeddings and metadata live. |
| **MODEL ACCESS**<br>Vertex AI · Azure AI Foundry · Amazon Bedrock · LiteLLM<br>One interface, swappable models, a choice of region. | **SERVING**<br>FastAPI · Uvicorn · Docker<br>Turns a notebook into an endpoint someone else can call. |
| **INTERFACE**<br>Streamlit · Gradio · Chainlit · Next.js<br>From a demo in an afternoon to a real product. | **CACHE & QUEUE**<br>Redis · Celery · RQ<br>This morning's cache, and the burst smoothing from Slide 8. |
| **OBSERVABILITY**<br>Langfuse · LangSmith · Phoenix · OpenTelemetry<br>Traces, token counts and cost per request, without building it. | **EVAL & GUARDRAILS**<br>Ragas · promptfoo · DeepEval · Llama Guard<br>Monday's golden set, run on a schedule instead of by hand. |

**Green callout box:**

> Every box here is an afternoon's work, and none of it is required for Thursday. Write the names down — you need them in month two, not this week.

**Suggested presenter notes for the deck file:**

> This slide is a reference, not a lesson. Read the category names, not the products.
> Say the callout clearly, because the room will otherwise leave thinking they were supposed to have used all of this.
> The top box is the one that actually applies here — in a government context the hosting region is decided before anything on the rest of the slide.

---

## Instructor notes · The toolbox slide

**How to run it: ninety seconds, category names only, then the callout.** You are not demonstrating anything and you should say so — "I am not going to open any of these, I am giving you the vocabulary so you know what to search for in month two." That framing stops it becoming a twenty-minute tangent, and it is honest.

- **Read the top box first and give it your emphasis, because it is the one that genuinely constrains this room: where the data is allowed to live decides the shortlist before any feature comparison happens.**
- Say the practical version: for a system holding internal government documents, the questions are which region the model is served from, whether the provider will contract on data residency, and whether prompts and outputs are retained for training. Those three answers eliminate most of the options on the slide before anyone compares features.
- **Verify before you present** if you want to name specific regions or in-Kingdom offerings — availability changes and I cannot check it from here. Safer phrasing that stays true: *"Every major provider now offers regional hosting and data-residency contracts, and which regions are available to you is a procurement question, not a technical one."*

**Orchestration — LangChain, LlamaIndex, Haystack, or plain Python.**

- **Say what the category is for: gluing prompts, retrieval and the agent loop together so you are not rewriting the same plumbing on every project.**
- **LangChain** is the largest ecosystem, with an integration for almost everything and a corresponding amount of abstraction. Its value is breadth; its cost is that when something breaks you are debugging someone else's abstraction rather than your own code.
- **LlamaIndex** is more focused on the retrieval side specifically — document loading, chunking, indexing strategies — so it maps closely onto what they built on Monday.
- **Haystack** sits between the two, with a pipeline model that some teams find easier to reason about.
- **Say "or plain Python" with a straight face, because it is a real answer.** Everything they built this week is plain Python and it works. The right time to adopt a framework is when they can name the specific thing it saves them, which is the same rule as Tuesday's advice about agent patterns. Name that callback.

**Vector store — pgvector, Qdrant, Chroma, Milvus.**

- **This is where the chunks, embeddings and metadata live once they stop being a Python list.**
- **pgvector** is a Postgres extension, and it is the answer that surprises people: if the organisation already runs Postgres, vector search is an extension away and needs no new system, no new backup policy and no new approval. In a government context that last part is worth more than any benchmark.
- **Qdrant** and **Milvus** are purpose-built vector databases that scale further and are separate systems to run.
- **Chroma** is the easy local one, good for development and for exactly the scale they worked at this week.
- **The honest guidance: below roughly a million chunks, pgvector is almost always the right answer**, and the reason to move is a specific measured problem, not ambition.

**Model access — Vertex AI, Azure AI Foundry, Amazon Bedrock, LiteLLM.**

- **The category exists so the model becomes a swappable component rather than a hard dependency** — which is the "primary and fallback behind one interface" box from Slide 18.
- **Vertex AI, Azure AI Foundry and Amazon Bedrock** are the enterprise fronts for the major clouds: regional hosting, contractual data handling, and access to several model families through one account.
- **LiteLLM** is a thin translation layer that gives many providers one common interface, which makes the fallback chain from this morning a configuration change rather than a rewrite.
- **Say the design point rather than the product point:** whatever they use, the goal is that the model name lives in configuration, so switching providers is one line and not a project.

**Serving — FastAPI, Uvicorn, Docker.**

- **This is what turns the notebook into something another system can call.**
- **FastAPI** gives you an HTTP endpoint with typed request and response models — and those types are the same JSON Schema idea from Sunday, one layer out. Name the callback; it lands well.
- **Uvicorn** is the server that runs it, and it is async, which is the Slide 8 point becoming a concrete choice.
- **Docker** is what makes "works on my machine" stop being a sentence anyone says. In a government deployment it is usually a hard requirement rather than a preference.

**Interface — Streamlit, Gradio, Chainlit, Next.js.**

- **Streamlit and Gradio** get a working chat interface in an afternoon and are perfect for an internal pilot or a demo to management.
- **Chainlit** is chat-shaped by default and has streaming and source display built in, which maps directly onto Slide 19's requirements.
- **Next.js** is the real-product answer and a different order of effort.
- **The guidance to give: Streamlit for the pilot, and only build a real front end once someone has decided the pilot is worth keeping.** Most internal tools never need to leave Streamlit.
- Worth one sentence for this room: whichever they pick, **check that it handles right-to-left text properly before committing**, because retro-fitting RTL into a front end is far more work than choosing one that already handles it.

**Cache and queue — Redis, Celery, RQ.**

- **Redis is the twelve-line dictionary from this morning, made real** — the same shape, with a TTL, shared across processes and surviving a restart. Say that connection explicitly, because it makes this box feel earned rather than new.
- **Celery and RQ are job queues**, and they are how the "batch offline work" card on Slide 14 actually gets implemented: embedding and indexing go on a queue and off the user's request path.
- **The queue is also the burst-smoothing from Slide 8**, so this one box quietly answers two earlier slides.

**Observability — Langfuse, LangSmith, Phoenix, OpenTelemetry.**

- **These are the products that do what they built by hand in Notebook 4 today** — the dataframe of requests, but with traces, token counts and cost attached automatically.
- **Langfuse** is open-source and can be self-hosted, which matters a great deal here, because self-hosting means the prompts and outputs never leave the organisation.
- **LangSmith** is the LangChain team's hosted offering. **Phoenix** is Arize's, and is strong on evaluation as well as tracing.
- **OpenTelemetry** is the vendor-neutral standard underneath much of this, and it is what lets these traces sit alongside the rest of the organisation's monitoring rather than in a separate silo.
- **Say the point that justifies the whole box: they now know what a trace is because they built one, so they can evaluate these tools instead of being sold to.** That is the payoff of doing it by hand today.

**Eval and guardrails — Ragas, promptfoo, DeepEval, Llama Guard.**

- **Ragas** scores retrieval-augmented systems specifically — whether the retrieved context was relevant and whether the answer was faithful to it. It is Monday's golden set with more metrics.
- **promptfoo** runs a suite of prompts against a set of assertions on every change, which is the closest thing to a unit test suite that this kind of system has.
- **DeepEval** takes a testing-framework shape, so it slots into an existing CI pipeline.
- **Llama Guard** and similar classifiers screen inputs and outputs for unsafe content, which is the automated half of tomorrow's topic.
- **Say the forward reference: tomorrow they attack each other's systems by hand, and this box is what does that continuously once nobody has time to do it by hand.**

**Closing the slide:**

- **Deliver the callout properly, because without it this slide does damage:** every box here is an afternoon's work, none of it is required for Thursday, and they need the names in month two rather than this week.
- **Say the sentence that makes it useful rather than intimidating:** they have now built a small version of five of these eight boxes themselves, so when a vendor demonstrates one, they will know what it is doing and whether they need it.
- **Ask the room, if you have thirty seconds:** "Which box would you add to your project first, after this week?" You want cache or observability. If someone says orchestration framework, ask what it would save them — that is Tuesday's "name the failure it fixes" rule, applied again.

---

# The Cost Auction — the activity Slide 3 promises

Slide 3 puts *Cost Auction* inside Block 1 and no slide defines it. Here is a version that runs in ten minutes and reinforces the calculator rather than competing with it.

**Setup.** Pairs. Each pair gets a card with a system spec and a monthly budget of **$50**.

**The spec card:**

> An internal HR assistant. 500 staff, 4 questions each per working day, 22 working days. Answers must cite a source. Roughly 60% of questions are in Arabic.

**The auction.** You put the Slide 12 calculator on screen with the defaults. Each pair has to get the monthly figure under $50 by *buying* changes, and every change has a stated cost in capability:

| Change | Effect | What it costs you |
|---|---|---|
| Drop top-k from 4 to 2 | Input tokens 2,200 → 1,200 | Retrieval misses more often |
| Cap output at 200 tokens | Output 400 → 200 | Shorter, blunter answers |
| Add a cache at 40% hit rate | ×0.6 on everything | Stale answers unless you set a TTL |
| Switch to a cheaper model | Halve both prices | Weaker tool selection, more retries |
| Answer Arabic questions only in Arabic | Avoids double-generation | No English fallback for non-Arabic speakers |

**Run it.** Two minutes for pairs to choose, then take three pairs and type their combination into the calculator live. The room watches the monthly figure move.

**The trap, and the reason the activity is worth doing.** With Arabic at 60% of traffic, the honest starting figure is not $16.72 — it is closer to double that, because both meters roughly double on Arabic questions. Pairs who did not apply the Slide 13 multiplier will "win" the auction with a number that is wrong. Reveal that at the end.

**Debrief in three questions, three minutes:**

1. Which change bought you the most money per unit of capability lost? *(The cache, every time — it is the only one that costs you nothing except a TTL you have to remember.)*
2. Which change did you refuse to make, and why? *(You want someone to defend citations or answer quality on principle. That is the right instinct.)*
3. Who accounted for Arabic? *(This is the reveal, and it is the whole point.)*

**If you are short on time,** cut the auction to the cache row and the Arabic reveal. Those two are the ones that transfer to their projects.

---

# Fix list — before you present

Ordered by how badly it will hurt you.

---

### 1. The "nearly half" claim on Slide 12 is wrong, and you will say it with the right number on screen

**Where:** Slide 12 presenter notes — *"Drop the input tokens from twenty-two hundred to twelve hundred… and watch the monthly figure fall by nearly half."*

It falls by about **26%**, not half.

At 2,200 in and 400 out, per query is $0.00022 + $0.00016 = **$0.00038**.
At 1,200 in and 400 out, per query is $0.00012 + $0.00016 = **$0.00028**.

That is 0.00028 ÷ 0.00038 = 0.737, so the monthly figure goes from **$16.72 to about $12.32** — roughly a quarter off, not a half.

The reason is the useful part: the output tokens did not change and they are priced four times higher per token, so cutting the input alone cannot halve the bill. The output cost is a floor.

**Fix the note to:**

> Drop the input tokens from twenty-two hundred to twelve hundred — that is retrieving two chunks instead of four — and the monthly figure falls from about sixteen seventy to about twelve thirty. A quarter off, for one line of code.
> Then say why it is not half: the output tokens did not move, and they cost four times as much per token. Output is a floor you cannot cut by touching retrieval.
> Then put the cache hit rate to forty percent and watch it drop again, to about seven forty. Those two numbers are the whole cost conversation.

The corrected version is a better lesson than the original claim was, because "cutting input has a floor" is a real insight and "it halves" is just a number.

**Check the second claim too when you run it:** 40% cache on top of the reduced input gives $16.72 × 0.737 × 0.6 ≈ **$7.39**, which is 56% off the original. So the *combined* effect is roughly half — which may be where the original note came from.

---

### 2. Slide 16 does not say whether cost per query includes the cache

**Where:** Slide 16, row six, `$0.00037` alongside a 38% cache hit rate in row five.

If 38% of queries are free, then "cost per query" could mean the cost of a query that reaches the model, or the average across all queries including the free ones. Those differ by nearly 40% and the table does not say which.

Every pair will hit this the moment they compute their own, and you will get the question during the lab rather than now.

**Fix — split the row:**

| Metric | Your run | Why it matters |
|---|---|---|
| Cost per model call | $0.00038 | What a cache miss costs you. |
| Effective cost per query | $0.00024 | After a 38% cache hit rate. This is the number for the budget. |

Two rows, clearly labelled, and it makes the cache's value visible in the table rather than only in the calculator.

**Separately, the arithmetic in the current row is slightly off.** At 2,240 input and 380 output with the Slide 12 prices, per call is $0.000224 + $0.000152 = $0.000376, which rounds to **$0.00038**, not $0.00037. Low severity, but somebody with a phone calculator will check it during the lab and you want to have fixed it rather than explained it.

---

### 3. Slide 12 is a live interactive widget and it is the centrepiece of the morning

**Where:** Slide 12.

Eight input fields and four computed outputs. If it does not render in presentation mode, or the room's machine handles the deck differently from yours, you lose the best twenty minutes of the day.

**Verify before you present:** open the deck in presentation mode on the machine you will actually use, in the room if you can, and type into every field. Confirm the outputs recompute and that the numbers are legible from the back.

**Have a paper fallback regardless.** Write these five rows on a card:

| Scenario | Per query | Per month |
|---|---|---|
| Defaults (2,200 / 400) | $0.00038 | $16.72 |
| Top-k halved (1,200 / 400) | $0.00028 | $12.32 |
| Plus 40% cache | — | $7.39 |
| Arabic, both meters doubled | $0.00076 | $33.44 |
| Arabic + top-k halved + cache | — | $14.78 |

With that card you can teach the whole slide on a whiteboard. Without it, a rendering failure costs you the block.

---

### 4. Notebook 4 has not been reviewed, and Day 3's notebook had never been run

**Where:** Slide 20 references `day4_production.ipynb`, which I have not seen.

Day 3's notebook arrived with zero execution counts and zero outputs on all fourteen code cells, and had four real bugs including one that would hang the Colab kernel. There is no reason to assume Notebook 4 is in better shape, and it is the notebook that has to run against thirty *different* projects rather than a fixed dataset — which is strictly harder.

**Two things to do, in order.** First, run it end to end yourself against one real project. Second, send it to me and I will do the cell-by-cell pass before tomorrow.

The specific risk on this one: the notebook imports *their* retrieval and agent functions, so it depends on interfaces that vary between pairs. Whatever it assumes about the shape of their `hybrid_search` or `run_agent` needs to be stated on Slide 20 before the lab starts, or you will spend the block fixing signature mismatches rather than teaching measurement.

---

### 5. The 2:00–2:00 break on Slide 3 is zero minutes long

**Where:** Slide 3.

Same bug as the Day 3 deck. Block 4 runs 1:00–2:00, then a break from 2:00 to 2:00, then Block 5 from 2:00 to 2:30.

Given Slide 21 puts the README clinic at 2:00–2:20 and the briefing at 2:20, the internally consistent version is: **Build 1:00–1:55, break 1:55–2:00, Block 5 2:00–2:30.**

Fix it in both decks while you are in there — someone will photograph this slide.

---

### 6. Two problems in the retry-and-fallback code slide

**Where:** the unnumbered code slide after Slide 15.

**6a — the `retry` decorator is never applied to anything.** The slide defines `retry`, then defines `ask_with_fallback`, which calls a bare `ask`. So the code as shown demonstrates a decorator and then does not use it, and a sharp student will ask why. Add one line:

```python
@retry(tries=3, base=1.0)
def ask(prompt, model=PRIMARY):
    ...
```

Even as a stub, that line makes the two halves of the slide connect.

**6b — `except Exception` in `ask_with_fallback` catches non-retryable errors too.** A `400` from a malformed request will fall through to the cheaper model, fail again, and return the canned response — silently. So a bug in your own code presents to the user as "the assistant is unavailable," and you never find out. That directly contradicts the retryable/non-retryable panel on Slide 15 beside it.

```python
def ask_with_fallback(prompt):
    for model in (PRIMARY, CHEAPER):
        try:
            return ask(prompt, model=model)
        except ApiError as e:
            if e.code not in RETRYABLE:
                raise                    # your bug, not their outage
            log.warning("falling back from %s", model)
    return CANNED
```

**Keeping 6b as-is would make a genuinely good exercise** — put the two slides side by side and ask the room to find the contradiction. That is a five-minute activity that teaches the distinction better than the panel does. Your call, but do not leave it unflagged, because it is the kind of thing one developer in the room will spot and mention at the break rather than in front of everyone.

---

### 7. `stats` and `ask` are undefined on the cache code slide

**Where:** the unnumbered code slide after Slide 14.

`stats["hits"]` and `stats["misses"]` are incremented and `stats` is never created, and `ask` is called and never defined. Presumably both exist in Notebook 4.

Low severity — it is a slide showing the interesting lines — but add one line above `CACHE = {}` so the slide is self-contained:

```python
CACHE, stats = {}, {"hits": 0, "misses": 0}
```

That is one line, it removes the question, and it makes the "count hits and misses from the start" note on the same slide literally true of the code beside it.

---

### 8. The lab's cache hit rate is predetermined

**Where:** Slide 20, *"20 queries with 8 repeats — measure the hit rate."*

Eight repeats out of twenty queries produces a 40% hit rate every single time, for everyone, by construction. It is not a measurement, it is arithmetic dressed as one.

This is fine as an exercise — the machinery is what they are testing — but it must be said, or they will report a fabricated number as a measured one in tomorrow's presentation, which is precisely the habit today is meant to break.

**Say this at 11:20:** *"Your hit rate will be forty percent. You did not measure that, the test list decided it. What you measured is that the cache works. A real hit rate comes from real traffic, and you will not have one until people are using this."*

If you want a better version, add a second query list weighted to look like real usage — a few very common questions and a long tail of rare ones — and let them see that a realistic distribution gives a *higher* hit rate than a uniform one. That is a genuinely useful thing to know and it costs one extra cell.

---

### 9. Verify the SDK surface on both code slides

**Where:** both unnumbered code slides.

Three things I cannot check from here:

- **`client.models.generate_content_stream(...)`** — confirm this is the current streaming method name and that iterating it yields objects with a `.text` attribute.
- **`ApiError` and `e.code`** — confirm the exception class name, where it is imported from, and that the HTTP status is exposed as `.code` rather than `.status_code` or nested inside a response object. This one is the most likely to be wrong, and it is load-bearing for the whole retry lesson.
- **Whether the SDK already retries internally.** Several clients retry 429s and 5xxs by default with their own backoff, which would mean the decorator on your slide is wrapping something that already does this. That is not a problem, but if a developer asks and you do not know, it undercuts the slide.

**One-line check for the second one:** in a notebook, make a call with a deliberately invalid model name, catch the exception, and `print(type(e), dir(e))`. Thirty seconds, and it tells you the class and the attribute.

---

# Not bugs — do not "fix" these

- **The Slide 12 per-query, per-day and per-month figures.** I checked all four: $0.00038, $0.76, $16.72 and $0.03 are all correct at the stated defaults. Only the presenter note about what happens when you change them is wrong.
- **Slide 16's illustrative figures differing from the lab's actual output.** They are meant to look like a real measurement rather than match the exercise.
- **`sort_keys=True` in the cache key.** Looks like a stylistic flourish, is load-bearing — without it the same settings in a different order produce a different key and silent cache misses.
- **`end=""` and `flush=True` on the streaming print.** Both necessary. `flush=True` in particular is the difference between streaming and a convincing imitation of non-streaming.
- **`base * 2 ** n` producing 1, 2, 4.** Correct operator precedence — `**` binds tighter than `*`.
- **`@functools.wraps(fn)`.** Not decoration. It preserves the wrapped function's name so your logs and tracebacks name the real function.
- **The cache code having no TTL** despite the slide demanding one. Deliberate teaching sequence: show the simple version, then name what is missing. Just say it out loud.
- **`RETRYABLE` not including 408 or 409.** A short, opinionated list is the right call for a teaching slide.
- **Slide 22's "Post-test at quarter past nine."** Consistent with the Day 3 deck's Thursday framing. No conflict.
- **The week running Sunday to Thursday.** Correct for SDAIA. Day 4 is Wednesday.
