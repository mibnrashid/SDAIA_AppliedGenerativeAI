# `day4_production.ipynb` — cell-by-cell instructor notes
**Day 4 · Production and the numbers · Applied Generative AI · SDAIA Academy**

---

## How to read this

- One section per cell, in notebook order, numbered 1–16 the way Colab counts them (markdown cells included).
- **Bold = what is actually in the cell, unpacked.** Read these and you have covered the cell.
- Plain text = depth to have ready that is *not* on screen: mechanism, idioms the non-coders will trip on, anticipated questions, honest caveats.
- Bullets run foundation → detail → payoff. Stop anywhere and you have still said something complete.

**Two things before anything else.**

**This notebook has never been run.** All eleven code cells have `execution_count: null` and zero stored outputs. Same as the Day 3 notebook. Everything below about what a cell *will* print is reasoning from the code, not from a recorded run.

**And the headline problem is not a bug, it is a gap.** Slide 20 promises *"This one runs against your project. Not a toy. Import your own retrieval and agent functions from the last two days."* The notebook never touches their retrieval or their agent. It measures bare one-line questions sent straight to the model. That means the token counts it produces will be roughly a hundredth of a real RAG request, and the central lesson of Day 4 — that retrieved chunks dominate the input — will be contradicted by their own measurements. **Fix list item 1 is the whole morning.**

---

## Shape of the notebook

**Cells 1–2 — setup.** Client, key, model constants, and a markdown statement of what they walk out with.

**Cells 3–4 — reliability.** A retry decorator with exponential backoff, given complete, then a cell that proves it fires on a retryable error and correctly refuses to fire on a non-retryable one. That second half is the good part.

**Cells 5–6 — latency perception.** Streaming against non-streaming, timed, then the markdown that says plainly what did and did not change.

**Cells 7–8 — caching.** A twelve-line cache keyed on prompt and settings, then twenty queries with eight repeats to measure the hit rate.

**Cells 9–13 — measurement.** The cost-formula TODO, `log_request`, fifteen logged calls into a DataFrame, two plots, and a written TODO turning the table into a per-user-per-month figure.

**Cell 14 — fallbacks.** A primary → cheaper → canned chain, with the primary deliberately broken.

**Cells 15–16 — reflection and troubleshooting.**

**Deck ↔ notebook mapping:**

| Deck slide | Notebook cells |
|---|---|
| 9 · Those 429s were the lesson | 3, 4 |
| 14 · Four ways faster + code slide | 5, 6, 7 |
| 15 · Assume every call can fail + code slide | 3, 14 |
| 16 · The table you will produce | 9, 10, 11 |
| 17 · If you cannot see it | 10, 11, 12 |
| 12 · The cost calculator | 9, 13 |
| 13 · The same product costs more in Arabic | 13 |

⚠️ **One deck promise has no notebook cell at all:** "import your own retrieval and agent functions." See fix list item 1.

---

## Cell 1 — Setup, imports and the API key

**Purpose:** working client, plus every library the rest of the notebook needs, with a loud failure if the key is missing.

- **`!pip install -q google-genai pandas matplotlib` — three packages today rather than one, because this notebook produces a table and two plots.**
- **The imports add `pandas`, `matplotlib.pyplot`, `functools`, `random` and `datetime` on top of Day 3's set — say that the new ones are for measurement, not for the model.**
- **`functools` is for the retry decorator in cell 3, `random` is for sampling the query list, and `datetime` is for the timestamp on every log row.**
- **The key block is identical to Day 3's: Colab Secrets, `userdata.get('GEMINI_API_KEY')`, and a `SystemExit` with six numbered steps if it fails.**
- Say the same thing you said on Tuesday: if this cell fails, it is the key, and they should not debug anything else until it prints Ready. Step 5 — the "Notebook access" toggle — is the one people skip, and it produces exactly the same failure as having no secret at all.
- **`MODEL = "gemini-2.5-flash-lite"` — and today the model choice matters differently from Tuesday.** On Tuesday it needed to select tools correctly; today it only needs to answer, and every number they measure is a number *for this model*. Say that explicitly, because a cost figure without a model name attached is meaningless.
- ⚠️ **`EMBED_MODEL` is defined and never used in this notebook.** Same as Day 3. It is there so pasted Day 2 code finds the name.
- **The comment at the bottom is the important one and it is easy to miss: bring in your own `ask()`, `hybrid_search()` and `run_agent()` from the last two days, because today is about measuring *their* project, not a toy.**
- ⚠️ **That comment is the only place the notebook asks for their own code, and nothing downstream uses it.** See fix list item 1. Also, `ask()` does not exist in any notebook this week — it appears on the Day 4 deck's code slides and in this comment, and nowhere else. See fix list item 8.
- **What will go wrong in the first ten minutes:** three people will get the key error because "Notebook access" is off for *this* notebook — the toggle is per-notebook, and having set it on Tuesday does not carry over. Say that at 11:20.

---

## Cell 2 — Markdown: what you walk out with

- **The promise is concrete: a table of their own numbers — latency per request, tokens in and out, cost, and a measured cache hit rate — plus a per-user-per-month figure they can say out loud in a meeting.**
- **The word "measured" is bolded and it is the point of the day.**
- **Read the last two sentences aloud, because they are the motivation: pairs who show measured numbers read as engineers, and pairs who say "it feels fast" do not.**
- Add the thing that makes it stick: the per-user-per-month figure is the one sentence of this course that their manager will remember, and it is arithmetic. The scarcity is not skill, it is that nobody measures.
- **Say that this table goes in tomorrow's presentation**, so they treat the notebook as producing a deliverable rather than as an exercise.

---

## Cell 3 — The retry decorator

**Purpose:** given complete so the forty minutes go into reading rather than typing. It demonstrates that the interesting decision in retrying is *what* to retry, not *how*.

- **The comment states the design point before any code: the important decision is not the retrying, it is deciding what to retry — a 429 will probably succeed in two seconds, and a 400 will fail identically forever.**
- **`RETRYABLE` is a tuple of eight strings: five HTTP status codes and three Google API status names — `RESOURCE_EXHAUSTED`, `UNAVAILABLE`, `DEADLINE_EXCEEDED`.**
- **Including both the numeric codes and the named statuses is deliberate**, because the SDK's exception text sometimes carries one and sometimes the other, and matching on both is more robust than picking one.
- **`def retry(tries=3, base=1.0)` is a decorator factory — a function that returns a decorator — and that three-level nesting is what will lose the non-coders.**
- **Explain it once in plain language: `retry(tries=3)` runs first and hands back a decorator, that decorator wraps the function, and the wrapper is what actually executes when you call it.** The three levels exist purely so you can pass `tries=3`.
- **`@functools.wraps(fn)` copies the original function's name and docstring onto the wrapper**, so tracebacks and logs name the real function instead of saying `wrapper`. One line, saves an hour of confused debugging later.
- **`for attempt in range(tries)` bounds the attempts — the same idea as Tuesday's step cap, in a different costume.** Name the callback.
- **`text = str(e)` then `any(code in text for code in RETRYABLE)` decides whether to retry by looking for those strings in the exception's message.**
- ⚠️ **Say honestly that this is string matching and it is fragile.** It is the right choice for a teaching notebook — it works across SDK versions and needs no knowledge of the exception hierarchy — but in production you check a status field on the exception object. See fix list item 4 for the specific failure mode.
- **`if not retryable or attempt == tries - 1: raise` is two conditions in one line and both matter:** do not retry something that cannot succeed, and do not swallow the failure on the last attempt.
- **`wait = base * (2 ** attempt)` produces 1, 2, 4 because `2 ** attempt` for 0, 1, 2 is 1, 2, 4.** Point at the arithmetic; several people will not see it.
- **The `print` inside the retry is a deliberate teaching choice — they will *see* the backoff happen in cell 4 rather than being told about it.**
- **`@retry(tries=3)` is then applied to `generate`, which is the thin wrapper around `client.models.generate_content` that the rest of the notebook uses.**
- **`model=model or MODEL` is the idiom to explain: if `model` is `None`, fall through to the module default.** It is Python's version of a default argument that can be overridden at call time, and it is what makes the fallback chain in cell 14 possible.
- **`print(generate("Say OK in one word.").text)` is the smoke test.** If this prints, the client, the key, the model name and the decorator are all working, and any later failure is in their code rather than the setup.
- **No jitter in the backoff.** Correct for a teaching notebook, worth one sentence: real backoff adds a small random offset so a thousand clients that failed together do not retry together.

---

## Cell 4 — Prove the retry fires, and prove it does not fire

**Purpose:** the best cell in the notebook. It tests both halves of the design decision, with no API calls, so it is instant and cannot fail on the network.

- **`attempts = {"n": 0}` is a counter in a dictionary rather than a plain integer, and the reason is a real Python gotcha worth naming: a plain `attempts = 0` inside a nested function would need `global`, but mutating a dictionary does not.** It is a small idiom that appears constantly and confuses people once.
- **`flaky()` raises a simulated `503 UNAVAILABLE` on its first two calls and succeeds on the third, so with `tries=4` it should print "succeeded on attempt 3".**
- **Before you run it, tell them what to watch for: two "retryable error, waiting" lines, with the waits being 0.5 and 1.0 seconds because `base=0.5`.** Then the success.
- **The waits are audible — half a second, then a full second — so the exponential shape is something they experience rather than read.** Say "listen to the gap" and pause.
- **The second half is the half that matters: `bad_request()` raises a simulated `400 INVALID_ARGUMENT`, and the decorator should give up after exactly one attempt.**
- **The printed line says so explicitly: "gave up after 1 attempt(s) - correct, 400 is not retryable."**
- **Say why that is the more important test: retrying correctly is easy, and *not* retrying is what saves money.** A system that retries everything three times triples the cost of every permanent failure and delays the error the user needs to see.
- I traced both paths and they behave as intended — `"400 INVALID_ARGUMENT (simulated)"` contains none of the eight retryable strings, so it raises immediately.
- **Ask the room:** "What would happen if I put 400 in the RETRYABLE list?" You want someone to say three attempts, four and a half seconds of waiting, and the same failure at the end.
- **Invariant to flag:** `attempts` is reset between the two tests by the line `attempts["n"] = 0`. Running only the second half of the cell after the first will double-count. Not a bug, but if someone splits the cell they will get confusing output.

---

## Cell 5 — Streaming versus non-streaming, timed

**Purpose:** produce the number that separates real speed from perceived speed, from their own machine rather than from a slide.

- **The same prompt is used for both — a 150-word explanation of RAG to a manager — so the comparison is fair.**
- **`t0 = time.time()` before each call and a subtraction after is the whole measurement technique.** No library, no profiler. Say that, because people assume measuring latency requires tooling.
- **For the non-streaming call, first-word time and total time are the same number by definition**, which is why the print statement uses the same variable twice. That is not a copy-paste error — it is the point.
- **In the streaming loop, `first_token_at` is captured on the first chunk only, guarded by `if first_token_at is None`.**
- **The iterator is lazy, so the network request is issued when the loop starts, not when `generate_content_stream` is called — which means `t0` to first chunk is a correct time-to-first-token measurement.** Worth saying, because it looks like the timer starts in the wrong place.
- **Tell them what to compare before you run it: the two *totals* against each other, and then the two *first-word* numbers against each other.** Without that instruction, they read four numbers and take nothing from it.
- ⚠️ **The gap will probably be less dramatic than the deck claims.** Slide 14's presenter note says six seconds to three hundred milliseconds. With flash-lite and a 150-word answer, non-streaming total will likely be one to three seconds, so the contrast is real but modest. See fix list item 3 for a one-word change that makes it dramatic.
- ⚠️ **The loop never prints anything, so nobody sees text streaming.** The numbers are the lesson, but a printed stream is more persuasive than a printed float. See fix list item 3.
- **Order effect worth mentioning if a developer asks:** the non-streaming call runs first and warms the connection, so if anything the comparison is biased *against* streaming, which makes the result more trustworthy rather than less.
- **What to say if the totals differ noticeably:** they are two samples of a noisy quantity, not a controlled experiment. Run the cell twice. If streaming is consistently slower by a small margin, that is per-chunk overhead and it is real — streaming trades a tiny amount of total time for a large amount of perceived time, and that is still the right trade.

---

## Cell 6 — Markdown: streaming does not make it faster

- **The claim is stated plainly: the two totals are within noise, and total generation time did not change by a millisecond.**
- **What changed is time to first token — from several seconds of blank screen to a few hundred milliseconds — and users read that as speed.**
- **The honest caveat is the best sentence in the cell: it is a perception fix, and if their p95 latency is too high, streaming hides it rather than fixing it.**
- **Read that last paragraph aloud even though it is markdown**, because it is the distinction people conflate and the whole reason the cell exists.
- Give the product framing: perception is most of user experience, and a fix that only changes perception is still a fix — as long as they know which problem they solved. The failure mode is shipping streaming, closing the latency ticket, and discovering in month three that nothing got faster.
- ⚠️ **The markdown asserts the totals are within noise, and that is an empirical claim about a run nobody has done.** See fix list item 3 — if the numbers disagree with the paragraph, you are reading a contradiction off the screen.
- **Forward to tomorrow:** streaming is on Day 5's UX slide as an obligation, not an optimisation. Say "this comes back" so the repetition reads as structure.

---

## Cell 7 — The cache

**Purpose:** show that the highest-value performance change in the notebook is twelve lines of dictionary manipulation.

- **`CACHE = {}` and `stats = {"hits": 0, "misses": 0, "time_saved": 0.0}` — and the stats dictionary existing from line one is the lesson, not an afterthought.**
- **Say the principle from the deck: an unmeasured cache is a guess.** They are counting hits from before the first hit exists.
- **`hashlib.sha256((prompt + json.dumps(kw, sort_keys=True)).encode()).hexdigest()` builds the key from the prompt and the settings together.**
- **`sort_keys=True` is load-bearing, not tidiness:** without it, the same settings passed in a different order produce a different JSON string and therefore a different key, and the cache silently misses on requests that should have hit.
- **Hashing rather than using the prompt as the key keeps keys short and fixed-length**, which matters when this becomes Redis rather than a dict. It also means the key does not contain the user's question, which is a small privacy benefit worth naming given tomorrow's material.
- **`.encode()` converts the string to bytes because hashlib works on bytes, not text** — a one-line explanation that saves a question.
- **The comment explains why settings are in the key: a different temperature is a different question and must not share a cache entry.**
- ⚠️ **That comment describes behaviour the code does not have.** `**kw` goes into the key and is never passed to `generate`, so two "different questions" produce identical API calls under different keys. See fix list item 2 — this is the notebook's one silent logic bug, and it undermines the exact lesson the comment teaches.
- **On a hit, the cache returns the stored text and adds the *original* latency to `time_saved`** — which is the right definition, because that is the time they would have spent had they called again.
- **On a miss, it times the call, stores both the text and the latency, and returns the text.** Storing the latency is what makes `time_saved` possible later.
- **The closing comment is the production caveat: in production this is Redis with a TTL, and a cache with no expiry serves yesterday's policy after it changed — a correctness bug, not a performance detail.**
- **Say that last distinction carefully in this room.** A policy assistant confidently serving a superseded policy is a governance incident, not a stale response.
- **The three print statements are the demo: the same question twice, with the second labelled `(cached)`, then the stats dictionary showing one hit and one miss.**
- **Watch the second print appear instantly.** Point at it — the absence of a pause is the whole demonstration.

---

## Cell 8 — Twenty queries, eight repeats, measured hit rate

**Purpose:** turn the cache from a demo into a measurement, and produce the number that goes in their table.

- **`BASE_QUESTIONS` is twelve realistic internal-policy questions — leave, training, breach reporting, procurement, remote work, MFA, overtime, sick leave, retention, IT response times, gifts, and personal cloud storage.**
- **The questions are worth ten seconds of attention: they are the kind of thing an actual employee asks, which is why the cache hit rate exercise is meaningful at all.** Real internal assistants have very repetitive traffic.
- **`queries = BASE_QUESTIONS + random.sample(BASE_QUESTIONS, 8)` builds twenty queries — twelve unique plus eight duplicates — then `random.shuffle` mixes the order.**
- **`random.sample(list, 8)` picks eight *distinct* items, which is why exactly eight questions appear twice and four appear once.** If it were `random.choices` you could get the same duplicate twice and the arithmetic would change.
- **`CACHE.clear()` and `stats.update(...)` reset both before measuring** — and that reset is why the cell can be re-run without the numbers drifting. Say it; out-of-order execution is the notebook's usual failure mode and this cell defends against it.
- **The loop calls `cached_generate(q)` for each query, and the wall clock is measured around the whole loop.**
- **The printed output is five lines: total queries, cache hits, hit rate as a percentage, time saved, and wall clock.**
- ⚠️ **The hit rate will be exactly 40%, every time, for everyone.** Twelve unique first occurrences are misses; the eight duplicates are hits; 8 ÷ 20 = 40%. The shuffle changes the order and not the arithmetic. See fix list item 5 — you must say this out loud or they will report a predetermined number as a measurement, which is the exact habit today exists to break.
- **`time saved` is the interesting number and the one to point at.** Eight hits at roughly a second and a half each is around twelve seconds saved out of a loop that took about thirty — meaning the cache cut wall-clock time by a third, on a workload nobody optimised.
- **Say the cost version of the same fact: those eight calls also cost nothing.** Forty percent fewer calls is forty percent off the bill for that workload.
- ⚠️ **This cell makes twelve real API calls.** With thirty people running it simultaneously on a shared free tier, see fix list item 6.
- **Ask the room:** "Would a real system have a higher or lower hit rate than this?" The honest answer is usually higher for an internal policy assistant, because real traffic is dominated by a handful of very common questions — and that is a genuinely useful thing for them to know.

---

## Cell 9 — TODO: the cost formula

**Purpose:** the deliberate blank. Reading a pricing page is a skill and it changes every few months, so they fill this in rather than inheriting it.

- **Say why it is blank before they ask: you left it out on purpose, because reading a pricing page is a skill and a formula they filled in themselves is one they can re-fill in six months.**
- **`PRICE_PER_1M_INPUT` and `PRICE_PER_1M_OUTPUT` are both `0.0` with TODO markers, and the comment stresses that prices are quoted per *million* tokens and that input and output are priced differently.**
- **The "per million" point is the one people get wrong**, and the error is always three orders of magnitude, which produces a monthly bill in the tens of thousands and a very confused pair.
- **`cost_of(prompt_tokens, output_tokens)` returns `0.0` and is marked as a one-line fix.**
- **The answer is one line:**

```python
return (prompt_tokens / 1_000_000) * PRICE_PER_1M_INPUT + \
       (output_tokens / 1_000_000) * PRICE_PER_1M_OUTPUT
```

- **Underscores in `1_000_000` are legal Python and purely for human eyes** — worth showing, because it prevents exactly the counting error above.
- **The sanity check at the bottom is well designed: a 2,000-in / 400-out request should be a fraction of a cent.** If their answer prints something larger than that, they have a units error, and the check catches it before it reaches the DataFrame.
- ⚠️ **Verify the current prices yourself before the lab and have them on a card.** Not to hand out — to check theirs against. If half the room quotes different figures because they read different pages, you need to know which is right in ten seconds.
- ⚠️ **Whatever they fill in must match the Slide 12 calculator's placeholders,** or their notebook figure and the figure on your screen will disagree and neither of you will know which is wrong.
- ⚠️ **The comment claims the ordering "means the notebook cannot break if someone runs cells out of order," and that reasoning is wrong** — see fix list item 7. Harmless, but cell 16 contradicts it.
- **What to look for while circulating:** anyone whose `cost_of` divides by 1,000 instead of 1,000,000, and anyone who adds the two prices together before multiplying. Both produce plausible-looking numbers.

---

## Cell 10 — `log_request`

**Purpose:** one row per call. This is observability at small scale, and it is what the paid tools do for you at large scale.

- **`LOG = []` is a plain list of dictionaries, which becomes a DataFrame in one line later.** Say that the whole of today's observability is a list.
- **`u = getattr(response, "usage_metadata", None)` reaches for the token counts the API returns alongside the answer.**
- **This is the cell's real content: the provider *tells you* how many tokens you used, on every response.** They do not have to estimate, count words, or run a tokeniser. Point at it — most people do not know this field exists, and it is the reason today's arithmetic is measurement rather than guesswork.
- **`prompt_token_count` and `candidates_token_count` are input and output respectively** — the naming is not obvious and "candidates" meaning "the thing it generated" catches people.
- **The nested `getattr(..., 0) if u else 0` means a response with no usage metadata logs zeros instead of crashing.** Defensive, and the right call, though it also means a broken field shows up as a suspiciously round zero rather than an error. Tell them to check the first row.
- **The row has seven fields: timestamp, model, prompt tokens, output tokens, latency, cached, and cost.**
- **Compare that list to Slide 17's logging bullet — prompt id, tokens in and out, latency, model, cache hit, cost, outcome — and note that this is that list, minus the prompt id and outcome.** See fix list item 9.
- **`datetime.now().isoformat(timespec="seconds")` produces a sortable, readable timestamp** without the microsecond noise that makes a printed table unreadable.
- **`cost_of(...)` is called here, at logging time, which is why the cost column reads 0.0 until they fill in cell 9.**
- **The print statement says exactly that**, which is a good piece of notebook design — it pre-empts the most likely confusion instead of letting them discover it in the DataFrame.
- ⚠️ **The `prompt` parameter is accepted and never used**, and **`cached` is never passed as `True` anywhere** because `cached_generate` does not log. See fix list items 9 and 10.

---

## Cell 11 — Fifteen logged calls into a DataFrame

**Purpose:** produce the actual table. This is the cell whose output goes into tomorrow's presentation.

- **`LOG.clear()` first, so re-running the cell replaces the measurements rather than appending to them.** Say it — this is the cell people run three times.
- **`random.sample(BASE_QUESTIONS, 12) + BASE_QUESTIONS[:3]` gives fifteen queries, three of which are repeats.**
- **These calls use `generate`, not `cached_generate`, so all fifteen are real API calls** — deliberately, because you cannot measure latency and tokens on a cache hit.
- **The loop is the whole pattern of instrumentation in four lines: start the timer, make the call, stop the timer, log the row.** Say that this is what every observability product is doing underneath.
- **`pd.DataFrame(LOG)` turns the list of dictionaries into a table in one line**, with the dictionary keys becoming column names. For the non-coders that is the entire reason the log rows are dictionaries.
- **`df.head()` shows the first five rows so they can see the shape.**
- **`df[[...]].describe()` is the payoff line — count, mean, standard deviation, min, the quartiles and max, for four columns at once.**
- **The double brackets are worth explaining once: the outer pair is indexing, the inner pair is a list of column names.** Single brackets with a list is the most common pandas error the non-coders will hit.
- **`describe()` gives them the median for free — it is the 50% row.** Point at it.
- **The three explicit prints are the numbers that go in the table: median latency, p95 latency, and total cost.**
- **`df['latency'].quantile(0.95)` on fifteen samples is a very rough p95** — it is interpolating near the top of a small sample, so it is really "roughly the worst one." Say so, because the concept matters and the precision does not. With fifteen points, p95 is essentially the second-slowest request.
- **Explain the median-versus-p95 distinction here if you did not on Slide 16**, because now it is their own data: the median is what a typical user waits, and the p95 is the experience one user in twenty gets. Averages hide this, which is why the table has no average latency in it.
- **What to say about the numbers being small:** these are one-line questions, so the latencies will be short and the token counts tiny. That is the problem fix list item 1 solves.
- ⚠️ **Fifteen sequential API calls at one to two seconds each is twenty to thirty seconds of nothing happening.** Warn them before they run it, or three people will interrupt the cell thinking it hung.

---

## Cell 12 — Two plots

**Purpose:** make the shape of the latency distribution visible, and make cost accumulation visible.

- **`plt.subplots(1, 2, figsize=(12, 4))` creates one row of two plots and returns the figure plus an array of axes.** The `axes[0]` / `axes[1]` indexing follows from that.
- **The left plot is a histogram of latency with a dashed vertical line at the median.**
- **A histogram is the right choice and worth one sentence of justification: it shows the *shape*, and shape is what a mean hides.** A long right tail is visible instantly and invisible in a summary statistic.
- **The right plot is `df["cost"].cumsum()` against request number** — cumulative sum, meaning each point is the total spent up to that request.
- **`cumsum()` is the idiom to name for the non-coders: running total.**
- **The closing comment is the lesson: the median is what a typical user waits, the right-hand tail is what people complain about, so optimise the median but design for the tail.**
- ⚠️ **If they have not filled in cell 9, the cumulative cost plot is a flat line at zero.** That is arguably a good forcing function, but say it out loud when it happens rather than letting them think matplotlib is broken.
- ⚠️ **`bins=10` on fifteen data points gives a sparse, ugly histogram** — mostly empty bins with one or two counts each. Not wrong, just unconvincing. `bins=6` reads much better at this sample size, and it is a one-character change if you want the plot to look like something.
- **What to look for while circulating:** pairs whose latency histogram is a single bar. That means every request took about the same time, which is normal for identical short prompts and will not be true once fix list item 1 is applied.

---

## Cell 13 — TODO: from your table to the real numbers

**Purpose:** the bridge from a DataFrame to a sentence they can say in a meeting. This is objective two of the day, and it is the written half.

- **Five questions, and they build: cost per query, then per user per month, then the monthly bill for 500 users, then the cache adjustment, then the Arabic adjustment.**
- **Question one is mean cost per query, straight from `df["cost"].mean()`.**
- **Question two multiplies by four queries per user per working day and twenty-two working days.**
- **Question three multiplies by 500 users** — and that is the number their management would actually ask for.
- **Question four applies their measured cache hit rate, which will be 40%, meaning multiply by 0.6.**
- **Question five applies the 2.5× Arabic token multiplier from Day 1.**
- **Say the important framing about question five: the multiplier applies to *both* meters**, because Arabic documents make bigger chunks and Arabic answers are more tokens. Multiplying only the input is the common error and it understates the result.
- **Use the Slide 12 calculator here.** Have them do the arithmetic in the notebook, then type their own numbers into the calculator on screen and watch the monthly figure move. That connects the two halves of the day and takes ninety seconds.
- **Have the expected shape ready so you can spot a wrong answer at a glance while circulating:** with the deck's placeholder prices and a real RAG request, cost per query lands around three or four hundredths of a cent, the monthly bill for 500 users lands in the teens of dollars, the cache takes about 40% off, and Arabic roughly doubles what remains.
- ⚠️ **With the notebook as written, their answers will be roughly a hundredth of that**, because the queries carry no retrieved context. See fix list item 1 — this is where the gap becomes visible to the students.
- **Ask the room after they finish:** "Is that number bigger or smaller than you expected?" It is almost always smaller, and the follow-up is the useful one: what would make it big? Answers you want are an expensive model, a large top-k, a long system prompt, no cache, and Arabic.

---

## Cell 14 — The fallback chain

**Purpose:** show that turning a total outage into a degraded answer costs about four lines.

- **`CANNED` is the last-resort response, and it is well written: it says the assistant is unavailable *and* tells the user where the policy documents actually are.**
- **Point at that second half.** A canned response that only apologises is a dead end; one that routes the user somewhere useful is a product. That is Slide 19's "show the failure plainly, with something useful to do next," arriving a day early.
- **`for model in (models or [MODEL, MODEL])` walks a list of models in order, returning the first success.**
- **The `or` idiom again: if no list is passed, use the default.**
- ⚠️ **The default list is the same model twice, and the inline comment admits it — "replace the second with a genuinely cheaper model."** So the default demonstrates the mechanism without demonstrating the benefit. See fix list item 11.
- **`except Exception as e:` prints which model failed and falls through to the next.**
- **The demo is the good part: `models=["does-not-exist-model", MODEL]` breaks the primary on purpose, so they watch the fallback engage and still get an answer.**
- **Then `models=["nope-1", "nope-2"]` breaks both, so they see the canned response.** Two lines, both failure modes, no waiting for a real outage.
- **Say the sentence from the deck as the closing line: users will forgive a degraded answer, and they will not forgive a page that hangs.**
- ⚠️ **`except Exception` also catches non-retryable errors like a malformed request**, which means a bug in their own code presents to the user as "the assistant is unavailable" and they never find out. That directly contradicts the retryable-versus-not lesson from cell 3. See fix list item 12 — and note this is the same flaw as the deck's code slide, so it is at least consistent.
- **Interaction worth knowing about:** `generate` is decorated with `@retry(tries=3)`, so each failing model in the chain goes through the retry logic first. An invalid model name produces a non-retryable error and fails fast, so the demo is quick. But if a real outage produced a retryable error, the chain would wait one second, two seconds, then move to the next model and do it again — up to fourteen seconds before the canned response. Worth saying, because it is a genuine production consideration: the retry budget and the fallback budget multiply.

---

## Cell 15 — Markdown: reflection

- **Four questions, and the cell says explicitly that this is what you check when you come round — so actually check it.**
- **Question one asks for their median and p95 and which one users will complain about.** The answer is the p95, and anyone who says the median has not understood Slide 16.
- **Question two asks for cost per user per month *and what they assumed to get there*** — and the second half is the real question. A number without its assumptions is not an answer, it is a guess with a decimal point.
- **Question three asks which single change would raise their cache hit rate most.** Good answers: normalising the question before hashing, caching retrieval results separately from generations, or a longer TTL.
- **Question four asks which of retries, caching, streaming or fallbacks they would add first, and why that one.** There is no single right answer, and the "why" is what you are marking.
- **Question four is the best predictor of who understood the day.** Caching for cost, streaming for perceived latency, fallbacks for reliability, retries for transient failures — any of them is defensible with the right reason, and none is defensible without one.
- **Do not let them skip this cell because it has no code.** Say you will read it, then read it.

---

## Cell 16 — Markdown: if this breaks

- **Three rows of symptom, cause and fix, and it is worth reading before the lab rather than after.**
- **Row one: an all-zeros cost column means the TODO in cell 9 is still returning 0.0, and the fix is to fill in the two prices and the return line, then re-run the logging cell.**
- **The "then re-run the logging cell" half is the part people miss** — the cost was computed at logging time, so fixing the formula does not retroactively fix rows already in `LOG`.
- **Row two: a `NameError` on `cost_of` means running out of order, and the explanation given is correct — `log_request` calls `cost_of` at call time, not at definition time.**
- **Row three: missing plots means matplotlib backend trouble or `df` not existing yet, and in Colab `plt.show()` is enough with no magic needed.**
- ⚠️ **Row two's stated cause — "the cost cell was defined after `log_request`" — describes a notebook layout that is not this one.** Cell 9 comes before cell 10. The *explanation* is right and the *cause* is wrong. See fix list item 7.
- **A fourth row worth adding**, once you have applied fix list item 1: *"`NameError: hybrid_search` → you have not pasted your Day 2 retriever in → paste it above the RAG cell, along with the records it closes over."*

---

# Fix list — before you present

Ordered by how badly it will hurt you.

---

### 1. The notebook does not instrument their project, and the numbers it produces teach the opposite of the lesson

**Where:** everywhere. Cell 1 asks them to paste in `hybrid_search()` and `run_agent()`. Nothing else in the notebook ever calls either.

Every measured request in this notebook is a bare one-line question sent straight to the model. Cells 5, 8 and 11 all call `generate(q)` where `q` is something like *"Who approves overtime?"* — about a dozen tokens.

**What that does to the numbers.** Their measured average input will be roughly 10–15 tokens. Slide 16's table says 2,240, "mostly retrieved chunks." Slide 11 says four chunks of 500 tokens is 2,000 tokens on every call before anyone types a word. So:

- Their cost per query will come out around a hundredth of the realistic figure.
- Input will be about 3% of their cost instead of the roughly 58% the deck teaches.
- **The central claim of Day 4 — that retrieved chunks dominate the input — will be directly contradicted by their own measurement.** A sharp pair will notice, and they will be right.
- The per-user-per-month figure in cell 13 will be so small it sounds like a rounding error, which undercuts the "say it in a meeting" framing from cell 2.

**Fix — one new cell, inserted before cell 11, and a two-line change to cell 11.**

```python
# ── Instrument YOUR project, not a toy ────────────────────────────────
# Paste your Day 2 hybrid_search (and the records it closes over) ABOVE
# this cell first. This is the cell that makes today's numbers real:
# a bare question is ~12 tokens, a real RAG request is ~2,000.

SYSTEM_PROMPT = (
    "You are a policy assistant. Answer only from the reference material "
    "between the tags. Cite the source and page. If the material does not "
    "answer the question, say so.\n\n"
)

def answer_with_rag(question, k=4):
    """One realistic request: retrieve, build the prompt, generate."""
    try:
        hits = hybrid_search(question, k=k)
    except NameError:
        # No retriever pasted in. Padded context so the token counts are at
        # least the right ORDER OF MAGNITUDE. Label this in your write-up —
        # these are illustrative numbers, not measurements.
        hits = [{"source": "placeholder.pdf", "page": 1,
                 "text": "policy text " * 250}] * k

    context = "\n\n".join(
        f"[{h['source']} p.{h['page']}] {h['text'][:600]}" for h in hits)
    prompt = f"{SYSTEM_PROMPT}<document>\n{context}\n</document>\n\nQuestion: {question}"

    t0 = time.time()
    r = generate(prompt)
    return r.text, r, time.time() - t0
```

Then cell 11's loop becomes:

```python
for q in random.sample(BASE_QUESTIONS, 12) + BASE_QUESTIONS[:3]:
    text, r, latency = answer_with_rag(q)
    log_request(q, r, latency)
```

**Three things this buys you beyond correct numbers.** The input token count becomes something they can *change* — halving `k` visibly halves it, which makes Slide 12's top-k lesson tangible. The latency becomes realistic, so the histogram in cell 12 has an actual shape. And the `<document>` tags plus "answer only from the reference material" seed tomorrow's layer-one defence, so Day 5 opens with something they already wrote.

**The `NameError` guard matters** — it is the same pattern the Day 3 notebook used successfully, and it means the notebook still runs for anyone who has not pasted their retriever. But make them say so in their write-up, because padded context is not a measurement.

---

### 2. `cached_generate` builds the cache key from settings it never applies

**Where:** cell 7.

```python
def cached_generate(prompt, **kw):
    key = hashlib.sha256((prompt + json.dumps(kw, sort_keys=True)).encode()).hexdigest()
    ...
    r = generate(prompt)          # ← kw is never passed
```

`**kw` goes into the key and is dropped before the call. So `cached_generate(p, temperature=0.9)` and `cached_generate(p, temperature=0.1)` occupy two different cache entries and make two *identical* API calls — the settings have no effect on anything except the key.

Nothing errors. The cache appears to work. And the comment directly above teaches the lesson the code contradicts: *"a different temperature is a different question and must not share a cache entry."* It does not share a cache entry, and it is also not a different question.

**Fix — widen `generate` and pass the settings through:**

```python
@retry(tries=3)
def generate(prompt, model=None, **kw):
    cfg = types.GenerateContentConfig(**kw) if kw else None
    return client.models.generate_content(
        model=model or MODEL, contents=prompt, config=cfg)
```

and in `cached_generate`:

```python
    r = generate(prompt, **kw)
```

**Verify before you present:** confirm `types.GenerateContentConfig(temperature=0.9)` is accepted and that passing `config=None` is equivalent to omitting it in the current SDK. One-line check: run `generate("hi", temperature=0.9)` and see whether it raises.

**This would make a good exercise if you flag it deliberately** — "the comment and the code disagree, find it" is a two-minute activity that teaches caching properly. Do not leave it silent, though; a pair who tries to demonstrate the temperature point will get a baffling result.

---

### 3. The streaming demo will underclaim, and nobody sees anything stream

**Where:** cells 5 and 6.

Two problems that compound.

**3a — the prompt is too short for the effect to be dramatic.** A 150-word answer from flash-lite will finish in roughly one to three seconds. Slide 14's presenter note promises "about six seconds to about three hundred milliseconds." At 150 words the gap is real but modest, and the slide will sound like an exaggeration.

**Fix: ask for 600 words.** Change the prompt to *"Explain retrieval-augmented generation to a manager in about 600 words."* Non-streaming becomes an unmistakable pause; time to first token barely moves. Same code, one number, far better demo.

**3b — the streaming loop prints nothing.** The measurement is right and the *experience* is missing. They read four floats.

**Fix — one line inside the loop:**

```python
for chunk in client.models.generate_content_stream(model=MODEL, contents=PROMPT):
    if first_token_at is None:
        first_token_at = time.time() - t0
    print(chunk.text, end="", flush=True)
```

`flush=True` is not optional — without it Python buffers and the whole answer appears at once, which looks exactly like non-streaming and destroys the demo. Say that to the room; it is one keyword and it is the one people omit.

**3c — cell 6 asserts the totals are "within noise" and nobody has checked.** If your run shows streaming consistently slower by 20%, you are reading a contradiction off the screen.

**Verify before you present:** run cell 5 three times and look at the spread. If the totals differ consistently, soften cell 6 to *"the totals are close, and any difference is per-chunk overhead — streaming trades a little total time for a lot of perceived time."* That is still the right lesson and it has the advantage of being true.

---

### 4. `RETRYABLE` matches on substrings of the error text

**Where:** cell 3.

```python
text = str(e)
retryable = any(code in text for code in RETRYABLE)
```

`"500"` is three characters. It matches a status code, and it also matches a request id containing 500, a token count of 1500, a byte offset, or a model name. A non-retryable error whose message happens to contain those digits gets retried three times, costing seven seconds and two extra API calls before failing anyway.

This is the right choice for a teaching notebook — it is readable, it works across SDK versions, and it needs no knowledge of the exception hierarchy. But it should be labelled rather than presented as production code.

**Fix — add a comment, and give them the production version:**

```python
# NOTE: matching on the error TEXT is fragile — "500" also matches a token
# count or a request id. It is used here because it works across SDK
# versions. In production, check the status field on the exception object.
```

**Verify before you present:** find out what the current SDK exception actually exposes. In a notebook, call `generate("hi", model="does-not-exist")`, catch the exception, and `print(type(e), e.__dict__)`. Thirty seconds, and it tells you whether there is a `.code` or `.status` you could point at when a developer asks — which someone will.

---

### 5. The cache hit rate is arithmetic, not a measurement

**Where:** cell 8.

Twelve unique questions plus eight distinct duplicates gives twelve misses and eight hits, every run, for every person. 40%, deterministically. The shuffle changes the order and not the result.

The machinery is what they are testing, and that is legitimate. But cell 2 promises "a **measured** cache hit rate" with the word bolded, and reporting a predetermined number as measured is exactly the habit today exists to break.

**Say this at 11:20, before they run it:**

> "Your hit rate will be forty percent. You did not measure that — the query list decided it. What you measured is that the cache works and how much time it saved. A real hit rate comes from real traffic, and you will not have one until people are using this."

**A better version, if you want it, costs one line.** Replace the uniform duplicate sample with a realistic traffic shape — a few very common questions and a long tail:

```python
# Real traffic is not uniform: a few questions dominate.
weights = [10, 8, 6, 4, 3, 2, 2, 1, 1, 1, 1, 1]
queries = random.choices(BASE_QUESTIONS, weights=weights, k=20)
```

Now the hit rate is genuinely variable, it will typically come out *higher* than 40%, and the lesson lands: skewed traffic caches better than uniform traffic, which is why internal assistants cache so well. That is a real insight and it costs two lines.

---

### 6. Roughly thirty-four API calls per person, times thirty people

**Where:** cells 3, 5, 7, 8, 11 and 14.

Counting: 1 smoke test, 2 for streaming, 1 for the cache demo, 12 in the hit-rate loop, 15 in the logging loop, and about 3 in the fallback chain. Call it thirty-four per person, concentrated into a forty-minute block.

Thirty people is around a thousand requests, mostly in two bursts (cells 8 and 11) as the room moves through the notebook together. On a shared free-tier key that is a rate limit; on individual free keys it is a per-minute limit that hits several people at once.

**The irony is useful and you should name it out loud when it happens:** the retry decorator in cell 3 is about to be tested for real, by them, on a 429. That is Slide 9's Monday callback happening live. If it fires, stop and point at it.

**Two mitigations.** Drop cell 11 from fifteen queries to ten — the statistics are barely worse and it removes a third of the load. And stagger the room: tell the left half to start at cell 8 and the right half to start at cell 11, then swap. Both are one-sentence instructions.

**Verify before you present:** confirm whether the room is on one shared key or individual keys. It changes your instructions completely, and it is the same question I flagged for Day 3.

---

### 7. Cell 9's comment gives a wrong reason, and cell 16 contradicts it

**Where:** cell 9's header comment versus cell 16's second troubleshooting row.

Cell 9 says: *"This comes BEFORE log_request, which calls it — so the notebook cannot break if someone runs cells out of order."*

That is not why. Python resolves `cost_of` when `log_request` is *called*, not when it is defined, so the definition order is irrelevant — what matters is that both cells have been run before the logging loop. Cell 16 states this correctly: *"`log_request` calls `cost_of` at call time, not at definition time."*

So the notebook contains both the right explanation and the wrong one, four cells apart.

**Also, cell 16's row two describes a cause that does not match this notebook** — "the cost cell was defined after `log_request`" — when cell 9 comes before cell 10.

**Fix both:**

- Cell 9 comment → *"This comes before `log_request` for readability. Both must be run before the logging loop — `log_request` resolves `cost_of` at call time, not at definition time."*
- Cell 16 row two cause → *"You have not run the cost cell in this session."*

Small, but it is a factual claim about how Python works in a notebook aimed at people who do not yet know how Python works.

---

### 8. `ask()` is referenced twice and defined nowhere in the course

**Where:** cell 1's closing comment ("paste your `ask()`, `hybrid_search()` and `run_agent()`"), and the Day 4 deck's two code slides, which both call `ask(...)`.

No notebook this week defines `ask()`. The Day 3 notebook defines `run_agent`, `calculate`, `get_weather` and `search_documents`. This notebook defines `generate`. Nobody has an `ask()` to paste.

**Fix — rename consistently, and `generate` is the name that already exists in working code.** Change cell 1's comment to ask for `hybrid_search()` and `run_agent()` only, and change the deck's two code slides from `ask(...)` to `generate(...)` so the projector matches the notebook.

Students read the screen and type into Colab. A function name that exists in one and not the other is twenty minutes of confusion for whoever tries.

---

### 9. `log_request` drops the prompt, so you cannot trace a slow request back to its question

**Where:** cell 10.

`prompt` is the first parameter and it is never used in the body. Every log row has a timestamp, tokens, latency and cost, and no indication of what was asked.

That breaks the actual purpose. When cell 11's histogram shows one request at four seconds, there is no way to find out which question caused it — and "which requests are slow, and why" is the entire point of a request log. Slide 17's logging list starts with "prompt id" for exactly this reason.

**Fix — one line:**

```python
LOG.append({
    "timestamp": datetime.now().isoformat(timespec="seconds"),
    "question": prompt[:60],          # so you can find the slow one
    "model": model or MODEL,
    ...
```

Then `df.sort_values("latency").tail(3)` in cell 11 shows them their three slowest requests *and what they were*, which is a far better lesson than a histogram alone.

**Truncating to 60 characters is deliberate** and worth saying: you want enough to identify the request, not a log full of full prompts. That is also the honest starting point for tomorrow's privacy conversation — a log of user questions is a data store with its own obligations.

---

### 10. The `cached` column is always `False`

**Where:** cells 7 and 10.

`log_request` takes `cached=False` and nothing ever passes `True`, because `cached_generate` does not log at all. So the column exists, is always False, and can never be used.

More importantly, it means **the notebook cannot produce the effective-cost-per-query number** — the one that accounts for the cache — which is the number that actually goes to management. The cache measurement (cell 8) and the cost measurement (cell 11) are two separate experiments that never meet.

**Fix — log from inside `cached_generate` too:**

```python
    if key in CACHE:
        stats["hits"] += 1
        stats["time_saved"] += CACHE[key]["latency"]
        log_request(prompt, None, 0.0, cached=True)     # free, instant
        return CACHE[key]["text"]
```

`log_request` already handles a `None` response — the `getattr` guard logs zero tokens and zero cost, which is exactly right for a cache hit.

Then in cell 13 they can compute both numbers honestly:

```python
cost_per_call = df[~df["cached"]]["cost"].mean()   # what a miss costs
cost_per_query = df["cost"].mean()                 # after the cache
```

That is the two-row table I recommended for Slide 16, produced from their own data. It is the difference between "our queries cost X" and "our queries cost X, and after caching we actually pay Y" — and the second is the one that gets budget approved.

---

### 11. The default fallback chain falls back to the same model

**Where:** cell 14, `models or [MODEL, MODEL]`.

The inline comment admits it: *"replace the second with a genuinely cheaper model."* As written, the default demonstrates the mechanism and not the benefit — if the primary is down, so is the fallback.

The explicit demos below it work fine, so this only bites someone who calls `ask_with_fallback(prompt)` with no arguments, which is the natural thing to do when adapting it for their own project.

**Fix — define a second model in cell 1 and use it:**

```python
MODEL = "gemini-2.5-flash-lite"
FALLBACK_MODEL = "gemini-2.5-flash-lite"   # ← put a different model here
```

and `models or [MODEL, FALLBACK_MODEL]`.

Even if both names end up the same today, the *structure* is right, and the constant at the top is where they will change it. A TODO on that line would also work and would make it an exercise.

---

### 12. `except Exception` in the fallback chain swallows your own bugs

**Where:** cell 14.

A malformed request — a 400 — falls through to the second model, fails again, and returns the canned response. Silently. A bug in their prompt-building code presents to the user as "the assistant is unavailable," and nothing in the logs says otherwise.

That contradicts cell 3, which spends its entire header comment teaching the retryable-versus-not distinction, and then cell 4 proves it. Two cells later the notebook throws the distinction away.

**Fix:**

```python
def ask_with_fallback(prompt, models=None):
    for model in (models or [MODEL, FALLBACK_MODEL]):
        try:
            return generate(prompt, model=model).text
        except Exception as e:
            if not any(code in str(e) for code in RETRYABLE + ("NOT_FOUND", "404")):
                raise                       # your bug, not their outage
            print(f"  {model} failed ({str(e)[:50]}), falling back")
    return CANNED
```

`NOT_FOUND` and `404` are added so the deliberate broken-model demo still works — an invalid model name is a legitimate reason to fall back, and without them the demo would raise instead.

**This is the same flaw as the deck's code slide, which makes it a genuinely good five-minute exercise:** put cell 3 and cell 14 side by side and ask the room what is inconsistent. A pair that finds it has understood the day. Your call whether to fix it or teach it — just do not leave it silent, because it is the kind of thing one developer spots and mentions at the break rather than in front of everyone.

---

### 13. Run it end to end tonight

Eleven code cells, zero execution counts, zero outputs. Same as Day 3.

Items 2, 3, 4 and 6 above can only be *resolved* by running it. Specifically, you need to know:

- Does `usage_metadata.prompt_token_count` populate, or does the token column read zero? **If it reads zero, the entire day has no numbers** — that is the single highest-consequence unknown in this notebook.
- Do cell 5's two totals actually come out within noise of each other?
- Does cell 14's invalid-model call fail fast, or does the retry decorator wait seven seconds first?
- How long does the full notebook take end to end? You have forty minutes and they also have to fill in two TODOs and write four reflections.

**Keep the outputs in the copy you distribute.** Anyone whose key fails can still read what should have happened, and it gives you something to point at if the room's quota goes.

---

# Not bugs — do not "fix" these

- **`attempts = {"n": 0}` instead of a plain integer** (cell 4). A dictionary is mutated in the enclosing scope without needing `global`. Deliberate and correct.
- **The non-streaming print using the same variable for first-word and total** (cell 5). Correct by definition — for a non-streaming call they are the same moment.
- **`t0` being set before `generate_content_stream` is called** (cell 5). The iterator is lazy, so the request is issued when the loop starts. This measures time-to-first-token correctly.
- **`sort_keys=True` in the cache key** (cell 7). Looks like tidiness, is load-bearing — without it the same settings in a different order produce a different key.
- **`random.sample` rather than `random.choices` for the duplicates** (cell 8). Sample gives distinct items, which is what makes the arithmetic clean. Not an error.
- **`CACHE.clear()` and the `stats.update()` reset** (cell 8). Defensive against re-running the cell. Good practice, keep it.
- **`base * (2 ** attempt)`** (cell 3). Correct precedence — `**` binds tighter than `*`.
- **`@functools.wraps(fn)`** (cell 3). Not decoration. It preserves the wrapped function's name in tracebacks and logs.
- **The cost column reading 0.0 before the TODO is filled** (cells 9, 10). Deliberate, and cell 10's print pre-empts the confusion. Good notebook design.
- **`getattr(response, "usage_metadata", None)` with nested defaults** (cell 10). Defensive, and it means a missing field logs zero instead of crashing the loop mid-run.
- **Using `generate` rather than `cached_generate` in cell 11.** Deliberate — you cannot measure latency or tokens on a cache hit.
- **`p95` on fifteen samples being crude** (cell 11). The concept is what matters at this scale, and the notebook is honest that these are their own small numbers.
- **`SystemExit` in cell 1's `except`.** Stops the cell cleanly in Colab instead of printing a long traceback.
- **`EMBED_MODEL` defined and unused** (cell 1). Forward-declared for pasted Day 2 code, not dead.

---

# One thing I added

**The `answer_with_rag` wrapper in fix list item 1** is the change that makes this notebook deliver what Slide 20 promises. It is about fifteen lines, it has a `NameError` guard so the notebook still runs for anyone who has not pasted their retriever, and it turns three of the day's numbers — input tokens, cost per query, and the latency distribution — from meaningless to real.

It also quietly seeds tomorrow. The prompt it builds wraps retrieved text in `<document>` tags and tells the model to answer only from that material, which is Day 5's layer-one defence. When you reach Slide 13 tomorrow you can say "you already wrote this yesterday" and put their own cell on screen.

If you take one change from this list, take that one.
