# Day 3 — Tools and agents · Instructor notes
**Applied Generative AI · SDAIA Academy · Tuesday 4 August 2026**

---

## How to read this

- One section per slide, in deck order.
- **Bold = what is actually on the slide, unpacked.** Read these and you have covered the slide.
- Plain text = depth you should have ready but that is *not* on screen: mechanism, anticipated questions, honest caveats. Skip freely when you are behind.
- Bullets run foundation → detail → payoff. Stop anywhere and you will still have said something complete.
- Every bullet is a full sentence you can say out loud without supplementing from memory.

**Numbering warning.** The PDF is **24 pages**; the footer counts only **20**. The four code slides carry no footer, no logos and no presenter notes, so the deck's own numbers drift from page 10 onward. These notes use **PDF page order (1–24)**, which is what your swipe count will match. The footer number is given in brackets where it exists.

| PDF page | Footer | Slide |
|---|---|---|
| 1–9 | 1–9 | title → the loop in five steps |
| **10** | *(none)* | **CODE — a tool declaration** |
| 11 | 10 | a vague description is a broken tool |
| **12** | *(none)* | **CODE — doing it by hand, once** |
| **13** | *(none)* | **CODE — the agent loop** |
| 14–19 | 11–16 | spiral → retrieval as one tool |
| **20** | *(none)* | **CODE — your retriever, as a tool** |
| 21–24 | 17–20 | trace → what today was |

---

## Shape of the deck

**Frame (pages 1–5, ~10 min).** Title, week map, day map, objectives, three recall questions from Day 2. Pure orientation. Move fast; the recall questions are diagnostic, not revision.

**Part One — Giving the model hands (pages 6–14, the bulk of Block 1 and part of Block 2).**
Motivation (three things a model cannot do) → the single load-bearing claim (*the model does not run your code*) → the five-step loop → the tool declaration in code → why the description field decides everything → the round trip executed by hand → the same loop automated → what happens when you remove the cap.
This arc is one idea told four times at increasing resolution: prose, diagram, code, failure.

**Control (pages 15–17).** Patterns reference table, guardrails checklist, error-message design. This is the "make it survivable" section and it is where Thursday is seeded.

**Part Two — Agentic RAG (pages 18–21).** Section divider, plain-RAG vs agentic-RAG trade, Day 2's retriever wrapped as a tool, and a decision trace read line by line. This is the emotional peak of the week: their own Monday code becomes a component.

**Judgement and close (pages 22–24).** When *not* to build an agent, the lab brief, the four-line recap.

**The throughline in one sentence:** Sunday made the model a reliable function, Monday made retrieval measurable, today the model *chooses* which function to call — and Wednesday will price those choices while Thursday attacks them.

---

## Slide 1 [1/20] · Tools and agents

- **The subtitle is "Let it act — but keep the leash short," and that phrase is the entire day in six words, so say it out loud rather than letting them read it.**
- **The date on the slide is Tuesday 4 August, and this is Day 3 of five, because the SDAIA week runs Sunday to Thursday.**
- Open with the shift: for two days the model has only produced text, and from this morning it starts causing things to happen in the world.
- Say plainly that this is the point where the technology becomes genuinely useful and genuinely dangerous in the same step, because both come from the same mechanism.
- Tell them the afternoon is theirs — teaching stops at noon — because that changes how they pace their attention this morning.
- **Callback to Sunday:** on Sunday you taught them to constrain the model's *output* into a typed shape; today that same typed shape becomes a *request for action*. It is the same JSON Schema doing a much bigger job.

---

## Slide 2 [2/20] · Where we stand

- **Sunday and Monday are struck through, Tuesday is highlighted, and Wednesday and Thursday are still ahead — point at the highlighted row so nobody has to hunt for it.**
- **Say the payoff sentence exactly: Monday's retriever becomes one tool inside today's agent, and that is the week joining up.**
- **The green box says there is no such thing as a dumb question — read it aloud rather than skipping it, because Day 3 is when the quiet people stop asking.**
- Name what is coming so today has a destination: Wednesday measures latency, tokens and cost per user, and Thursday breaks what they built and then defends it.
- If anyone missed Monday, tell them now that they can still complete today's lab using a stub retriever, so they do not spend the morning quietly panicking.
- **Pause point.** Five seconds of silence after the "dumb question" line does more than saying it twice.

---

## Slide 3 [3/20] · How the day runs

- **Teaching runs 9:15 to 12:00 in three blocks, and from 1:00 the afternoon is project time with you circulating rather than presenting.**
- **Block 1 is fifty minutes on function calling plus the Be the Agent activity, Block 2 is forty minutes on patterns and guardrails, and Block 3 is forty minutes in the notebook.**
- **The gate at 2:30 is documents loaded, chunked, embedded, and one query returning something — running, not polished.**
- **Say that anyone still stuck at 2:00 gets you sitting next to them, because that turns "I'm stuck" from an admission into an appointment.**
- Notice the gate is a *Day 2* deliverable, not a Day 3 one; that is deliberate, because the project needs retrieval working before an agent can sit on top of it. Say that out loud or someone will ask why today's lab is not the gate.
- ⚠️ **The 2:25–2:25 break is zero minutes long.** See fix list item 6.
- **Pacing reality check:** Block 1 has to cover pages 6 through 12 *and* run Be the Agent in fifty minutes. That is roughly four minutes per slide with nothing left over. Your compressible slides are 7 and 15; your incompressible ones are 8, 9 and 12.

---

## Slide 4 [4/20] · What you will be able to do by 12:00

- **There are five objectives, and number five is bold on the slide because it is the payoff — the agent gets their Day 2 retriever as a tool and they read its decision trace.**
- **Objective one is to explain exactly who executes a tool call and who does not, and you should say that this sounds trivial and is the thing most people get wrong, including people who have shipped agents in production.**
- **Objective four names the three guardrails they will actually implement: a step cap, a tool allow-list, and an output validator.**
- Frame objectives as a checklist they can self-assess against at noon, because a stated objective they cannot demonstrate is the fastest way to surface a gap before the afternoon.
- **Ask the room:** "Which of these five do you already think you can do?" Hands on one and three usually mean you can move faster through pages 6–9.

---

## Slide 5 [5/20] · Three questions before we start

- **Ask three people who did not speak yesterday, take one answer each, and move — this is five minutes, not a revision session.**
- **The purpose is to find out who did not follow Monday, not to re-teach Monday.**
- **If two or more people stumble on question three, spend two extra minutes on it, because their project score depends on the golden set.**

**Answer key, so you can correct quickly:**

- **Question one — why vector search failed on the reference number.** Embeddings encode meaning, and a reference code like `E-10482` has no meaning to encode, so it lands in a vague region of the space near other short alphanumeric strings. The fix was hybrid search: keyword matching (BM25 or similar) catches exact tokens that embeddings smear.
- **Question two — what re-ranking buys over a bigger top-k.** A bigger top-k retrieves more candidates but does not reorder them, so the right passage may sit at position 40 and get truncated or diluted in the prompt. A re-ranker scores each candidate *against the actual query* with a slower, more accurate model, so the right passage moves to position 1. More candidates is recall; re-ranking is precision.
- **Question three — what a golden set measures.** It measures whether *retrieval* returned the right passages, independently of whether the model wrote a good answer. It separates a retrieval failure from a generation failure. Without it, every bad answer looks like the same bug.
- If nobody can answer question three, say the consequence rather than repeating the definition: without a golden set they cannot tell you tomorrow whether their caching change made the system worse.

---

## Slide 6 [6/20] · Part One — Giving the model hands

- **This is a divider slide, so the only job is to state that the next hour rests on one idea about where execution happens.**
- **Tell them you will repeat that idea more times than feels necessary, and that this is on purpose.**
- **Promise the concrete outcome: they will run the loop manually, by hand, before any library is allowed to do it for them.**
- The reason for hand-running is that every agent framework hides the loop behind one function call, and people who only ever saw the framework cannot debug it. Say that.

---

## Slide 7 [7/20] · Three things a model cannot do alone

- **Three cards: no live data, no actions, unreliable arithmetic — and the green box says tools fix all three the same way, because the model asks and your code does the work.**
- **No live data means it cannot see today's exchange rate, your ticket queue, or whether an employee is still on leave, because its knowledge stopped at a training cut-off.**
- **No actions means it can write a beautiful email and cannot send one — text in, text out is the whole interface.**
- **Unreliable arithmetic means it predicts the next token, so "1,247 × 0.83" produces a number that looks exactly like a correct answer and is not one.**
- **Say the general rule: anything with a correct answer — arithmetic, dates, lookups, unit conversions — should be a tool, not something you hope the model gets right.**
- The arithmetic card gets a laugh; take it seriously anyway, because the failure is invisible. A wrong sum arrives formatted, confident, and in the same font as a right one.
- Useful nuance if a developer pushes back with "but the newer models do arithmetic fine": they are better, not correct, and the failure mode has not changed — it still returns a plausible number rather than an error. A tool turns a silent wrong answer into a right one.
- **Callback to Sunday:** you already told them the model is a next-token predictor. This slide is that fact cashed out into three business consequences.

---

## Slide 8 [8/20] · The model does not run your code

- **This is a full-bleed statement slide, so stop, say the sentence, and let it sit before you explain it.**
- **The model returns a request, and your application decides whether to honour it.**
- **Say it concretely: the model emits a structured message meaning "I would like to call `calculate`, with this argument," and your code reads that message and chooses what to do.**
- **Tell them this is the first of three times you will say it today, so they notice the repetition is deliberate.**
- Name what the model does *not* do, item by item, because the negatives are what stick: it does not run your function, it does not run a shell command, it does not touch your database, it has no network access of its own.
- **This is not a technicality — it is the only place in the whole system where you can enforce permissions**, and on Thursday it is the difference between a nuisance and a breach.
- Anticipated question: *"But ChatGPT runs Python."* Answer: that product ships a sandbox that the vendor's application code operates on the model's behalf — the application is still the executor, it just happens to be theirs rather than yours. The boundary has not moved; you have merely rented someone else's side of it.
- Anticipated question: *"What about MCP?"* Same answer, one layer out. MCP standardises how your application discovers and describes tools; the execution still happens in a process you or your vendor control.
- **Pause here.** This is the highest-value ten seconds of silence in the deck.

---

## Slide 9 [9/20] · The loop, in five steps

- **Five cards left to right: declare, decide, execute, return, repeat — and "Your code" is bold in card three because that is the step everyone skips when they describe this.**
- **Declare means you send the prompt plus a list of tools the model is permitted to request.**
- **Decide means the model either answers directly or returns a tool call with arguments — and answering directly is a legitimate outcome, not a failure.**
- **Execute means your code runs the function, or refuses to.**
- **Return means you append the result to the conversation and send the whole thing back.**
- **Repeat means it goes round until the model gives a final answer or your step cap fires.**
- **The green box defines an agent: this loop, with a goal, and a cap on how many times it may go round. That is the whole definition — there is nothing else in it.**
- **Walk left to right and physically put your finger on card three as you say it.**
- Say the deflating truth: nothing here is magic, it is a `while` loop with a network call inside it. All the intelligence lives in the model's choice at step two.
- Point out that step five is where every runaway-cost story of the last two years comes from, which sets up page 14.
- Worth naming: the conversation history is the agent's entire memory. There is no hidden state. If you drop the history, the agent forgets everything it just learned — which is also why the loop gets more expensive every time round.
- **Callback to Monday:** step four is exactly what they did with retrieved chunks — put text into the conversation and ask again. The mechanism is identical; only the source of the text has changed.

---

## Slide 10 *(unnumbered)* · CODE — A tool declaration, argument by argument

**Block purpose:** this slide exists to show that a "tool" is two separate things — an ordinary Python function, and a *description of that function written for the model*. Most confusion on this topic dissolves once people see that these are two objects.

- **The first thing on the slide is a completely ordinary Python function, `get_leave_balance`, and it has no AI in it at all — say that explicitly.**
- **`from google.genai import types` is the current Google GenAI SDK, and everything on this slide is that SDK's way of expressing a schema.**
- **`def get_leave_balance(employee_id: str, year: int) -> dict` carries type hints, and those hints are for humans and your IDE — the model never sees them, which is precisely why you have to repeat the types in the schema below.**
- **The comment "a perfectly ordinary Python function" is on the slide on purpose; read it aloud.**
- **`types.FunctionDeclaration(...)` is the description object, and it is what actually gets sent to the model — the function body is never transmitted.**

**Line by line, argument by argument:**

- **`name="get_leave_balance"` is the string that comes back in the model's request, so it must match how you look the function up later.** If it drifts from your dictionary key, the allow-list on page 13 returns "unknown tool" and the agent flails in a way that looks like a model problem and is a typo.
- **`description=(...)` is the highlighted block and it is what the model actually reads.** This is the single most important string in the file, and page 11 is entirely about it.
- Note the Python idiom for the non-coders: **adjacent string literals in parentheses are automatically joined**, so those four quoted lines become one sentence. The trailing space at the end of each fragment is load-bearing — without it you get `annualleave`. Point at it.
- **`parameters={...}` is JSON Schema, and it is the same JSON Schema they wrote on Day 1 — say the callback, because this idea is now on its third appearance.**
- **`"type": "object"` at the top level is required**, because the model must return a named-argument bundle rather than a bare value; there is no positional-argument concept here.
- **`"properties"` gives each argument its own type and its own description**, and the per-argument description is where you disambiguate. `"HR id, e.g. E-10482"` is doing real work: the example teaches the format better than any prose could.
- **`"year": {"type": "integer"}` matters because without it the model will happily send the string `"2026"`**, and your function will pass it into an HR lookup that does an integer comparison and silently returns nothing.
- **`"required": ["employee_id", "year"]` is what the model must supply, and everything not listed is optional.** If you mark something required that the user has not specified, the model will invent it — that is not a hallucination bug, it is you telling it the field is mandatory.
- The payoff sentence: **the schema is not documentation, it is the interface contract**, and the model's behaviour is downstream of it in the same way an API client's behaviour is downstream of an OpenAPI spec.

⚠️ This slide creates `leave_tool` but never registers it with the model — registration happens on page 12. Say "we wire this up in a moment" or someone will think the slide is incomplete.

**Arabic/RTL note worth thirty seconds:** if the corpus is Arabic, the `description` field should still be written in English *unless* the model is being asked to match Arabic query vocabulary. Descriptions are read by the model in whatever language you write them; English descriptions cost fewer tokens and are what the model has seen most of. But the `"e.g. E-10482"` style example must use the *real* format your HR system uses, including any Arabic-Indic digits (`٢٠٢٦`) if that is what the source data contains — because the model will pattern-match to your example and hand you back digits your `int()` call cannot parse.

---

## Slide 11 [10/20] · A vague description is a broken tool

- **Two columns, bad and good, and the good one is a single sentence containing three things: scope, units, and an explicit exclusion.**
- **The bad description is "Gets leave data," and the questions underneath are the ones the model cannot ask you: when should it be called, what does it return, and what is "leave data" anyway.**
- **The consequence of the bad version is that the model guesses, and calls it for sick leave, for policy questions, and for anything with the word "leave" in it.**
- **The good description says it returns *remaining annual* leave, in *working days*, for a given year, and explicitly says it does not cover sick leave.**
- **The green box is the rule to remember: write descriptions for a competent new colleague who cannot ask you a follow-up question.**
- **Say the diagnostic loudly: when an agent misbehaves, the first place to look is not the prompt and not the model — it is the tool descriptions.**
- **If your agent keeps calling the wrong tool, you have a documentation problem, not an intelligence problem.**
- The exclusion clause is the part nobody writes and the part that does the most work, because it is the only mechanism that stops a plausible-but-wrong tool from being selected when two tools have overlapping names.
- Units are the second-most-skipped element. "Leave balance: 22" is meaningless — working days, calendar days and hours are all defensible readings, and the model will pick one and present it with total confidence.
- **Ask the room:** "Give me a bad description for a tool that sends an email." You want to hear something like "sends messages," then ask what breaks. Someone will get to "it will use it for Slack, or for SMS, or to reply to a customer without approval."
- **Forward to Thursday:** a tool description is untrusted-adjacent territory. If a retrieved document contains text that reads like a tool description, the model may treat it as one. That is the injection surface you will attack on Thursday.

---

## Slide 12 *(unnumbered)* · CODE — Doing it by hand, once

**Block purpose:** this is the payoff of page 8. They watch the round trip happen in four explicit steps, with nothing hidden, so that when a framework does it in one line later they know what that line contains.

- **Say the frame first: there is no library doing anything here, and every one of these four steps is something you wrote.**
- **`types.Tool(function_declarations=[leave_tool])` bundles declarations, and `types.GenerateContentConfig(tools=[tools])` is what actually registers them with the request — this is the wiring that page 10 was missing.**
- Note the shape for the non-coders: a `Tool` holds a *list* of declarations, and the config holds a *list* of Tools. Two levels of list, which is why people get a confusing error when they pass a bare `FunctionDeclaration` in.
- **Step 1, `r = client.models.generate_content(model=MODEL, contents=history, config=cfg)` — and the comment on the slide says the model does NOT answer the question, so read that comment aloud.**
- **`contents=history` is the whole conversation, not just the latest message**, because the model is stateless and every call must carry everything it needs to know.
- **Step 2, `call = r.candidates[0].content.parts[0].function_call` — this is where you inspect what came back, and the comment says it is a REQUEST, not an answer.**
- **`print(call.name)` gives you `get_leave_balance` and `print(call.args)` gives you the dictionary of arguments, so they can *see* that the model has produced a structured request and nothing more.**
- Explain the attribute chain in plain language once: a response can contain several candidate answers, each candidate has content, content has parts, and one of those parts may be a function call. It reads like a long chain because the API is designed for a general case that includes images and multiple parallel calls.
- ⚠️ **`parts[0]` assumes the function call is the first part, and that is not guaranteed.** See fix list item 2 — this is the one most likely to bite in the room.
- **Step 3, `result = get_leave_balance(**call.args)` — put your finger on this line and say that nothing ran until this moment, and if you delete this line nothing happens at all.**
- **`**call.args` is dictionary unpacking**, and for the non-coders it means "take this dictionary of names and values and hand them in as named arguments" — so `{"employee_id": "E-10482", "year": 2026}` becomes `get_leave_balance(employee_id="E-10482", year=2026)`.
- **The comment says "Check permissions here," and this is the sentence to linger on: this is where you decide whether *this* user is allowed to look up *that* employee.** The model has no idea who is asking, and it never will.
- **Step 4 has two appends, and the order matters: first the model's own turn (`r.candidates[0].content`), then the function result.** If you append only the result, the conversation has an answer to a question it never contains, and the model gets confused or refuses.
- **`types.Part.from_function_response(name=call.name, response={"result": result})` returns the result wrapped in a dict**, because the API requires a structured object rather than a bare value.
- **The `role="user"` on the function response looks wrong and is correct** — in this SDK the tool result comes back on the user turn, because from the model's point of view the environment is speaking. Flag it before someone "fixes" it.
- **The final call sends the enlarged history back and gets a natural-language answer, and only now does the model actually answer the original question.**
- **Say the closing line on the slide: in the notebook these four steps are four separate cells, so the round trip is impossible to miss.**
- **Hidden dependency to warn about:** `history` must already exist and already contain the user's question. It is not created on this slide. On a kernel restart, or if they run these cells out of order, they get a `NameError` on `history` — or worse, a stale `history` from a previous run that makes the model answer a question nobody asked.
- **What will go wrong in the next ten minutes:** somebody runs the step-4 cell twice, appends the same result again, and gets a duplicated tool response. The symptom is a strange, repetitive answer. The fix is to re-run from the cell that initialises `history`.

---

## Slide 13 *(unnumbered)* · CODE — The agent loop

**Block purpose:** the same four steps as page 12, wrapped in a `for` loop, with the guardrails already present so they see that safety is structural rather than bolted on.

- **Say the frame: this is page 12 in a loop, and nothing new has been added except the ability to go round more than once.**
- **`def run_agent(goal, tools, max_steps=5, verbose=True)` — the defaults matter, because a cap of five is a decision, not a placeholder.**
- ⚠️ **The `tools` parameter is accepted and never used inside the function.** See fix list item 1.
- **`history = [user_message(goal)]` starts a fresh conversation containing only the goal**, which means each `run_agent` call is independent and has no memory of previous calls.
- **`for step in range(max_steps)` is the bound**, and this single line is the difference between an agent and an incident.
- **Inside the loop, the same `generate_content` call as before**, so point out that the network call is now inside a loop and therefore happens up to five times.
- **`part = r.candidates[0].content.parts[0]` — same indexing assumption as page 12, same caveat.**
- **`if not getattr(part, "function_call", None): return r.text` is the exit condition, and the comment says it plainly: no tool requested means it is finished.**
- Explain `getattr` in one sentence for the non-coders: it asks for an attribute and returns a default instead of crashing if it is not there. It is defensive, and it is not a bug.
- **`if verbose: print(f"step {step}: {call.name}({dict(call.args)})")` is the trace**, and this one line is what turns a black box into something you can debug and later explain to an auditor.
- **`fn = TOOLS.get(call.name)` is the allow-list, and the comment says never call by name blindly.** Say what the alternative would have been: looking the name up in `globals()` or calling `eval` on it, which hands a remote system the ability to name any function in your process.
- **`result = fn(**call.args) if fn else {"error": "unknown tool"}` — the unknown-tool branch returns an error the model can *read*, rather than raising.** That is page 17's principle, appearing here before you have taught it; mention that you will come back to it.
- **The two appends are identical to page 12, and `tool_result(...)` is the helper that wraps step 4's two lines.**
- **`return "Stopped: step limit reached."` is what happens when the cap fires**, and it is a string rather than an exception so the caller sees a result rather than a crash.
- **The right-hand panel names four guardrails already present: the bound, the allow-list, the readable error, and the trace.** The point is that these cost four lines total.
- **The closing line says this is given complete in the notebook — read it, don't retype it.** Say that verbatim; twenty people typing this is fifteen minutes you do not have.
- **Undefined names to be ready for:** `user_message`, `tool_result`, `cfg`, `TOOLS`, `MODEL` and `client` are all referenced and none are defined on this slide. They exist in the notebook. Someone will notice and ask; the honest answer is that the slide shows the interesting eight lines, not the plumbing.
- **The `cfg` closure is a genuine gotcha:** `run_agent` reads `cfg` from module scope, so if a student registers a new tool by rebuilding `cfg` in a later cell and then calls `run_agent` in an *earlier* cell, they get whichever `cfg` was defined most recently. Symptom: "my new tool is never called" — or, more confusing, "my new tool *is* called and I don't know why."

---

## Slide 14 [11/20] · Take the cap off and watch

- **The left panel is a real trace of an agent calling `search_flights` five times in a row with almost the same argument each time.**
- **Look at the arguments: JED, JED, Jeddah, JED, and then JED with a trailing space — the model is not stuck, it is trying trivial variations and getting nothing back.**
- **The caption names the three ingredients: a goal it cannot satisfy, a tool that keeps returning nothing, and no reason to stop.**
- **The right panel is the cost, and the key sentence is bolded on the slide: each step costs more than the last, because every step is a paid call and the history grows each time.**
- **Say the number intuition out loud: step twenty is not twenty times step one, it is much worse, because step twenty carries all nineteen previous turns in its prompt. The cost curve is not flat, it is roughly quadratic in the number of steps.**
- **"Left overnight, this is the invoice that ends up in a post-mortem."**
- **"On a free tier you hit a rate limit and stop — that is luck, not design."**
- **The closing line is absolute and should be delivered as such: every agent gets a cap, no exceptions.**
- **In the notebook they remove the cap themselves, run it, watch it spiral, and interrupt the cell.** Watching it happen once is worth more than any warning you can give.
- **Ask the room: "What is a sensible cap?"** You want an answer between three and ten, and you want the *reason* to be "how many steps this task actually needs," not a round number.
- Useful extra failure mode to mention: the spiral is not always identical calls. A more expensive version alternates between two tools forever, each one undoing what the other did. A cap catches both; a "stop on repeated identical call" check catches only the first.
- **The trailing space in `dest="JED "` looks like a typo in your deck and is the whole point** — say so, because someone will helpfully tell you about it afterwards.

⚠️ **Classroom risk:** thirty people running an uncapped loop against a shared free-tier key will exhaust the quota for the room. See fix list item 3.

---

## Slide 15 [12/20] · Six shapes, and when to use them

- **Six patterns with a one-line definition and a one-line "use when" each — this is a reference slide they will come back to, not something to teach in depth.**
- **ReAct is think, act, observe, repeat, and you use it when the next step depends on what you just found.**
- **Plan-and-Execute plans all steps first and then runs them, and you use it when the task is predictable and you want the plan reviewable before anything happens.**
- **Reflection produces output, critiques its own output, and revises, and you use it when quality matters more than latency or cost.**
- **Routing uses a cheap classifier to pick a specialist, and you use it when you have several narrow jobs rather than one broad one.**
- **Hierarchical has a manager agent delegating to workers, and you use it rarely, for genuinely separable sub-tasks, because it is expensive.**
- **Human-in-the-loop pauses for approval before acting, and you use it when the action is irreversible — money, messages, deletions.**
- **The green box is the advice: start with ReAct and a step cap, and add a pattern only when you can name the failure it fixes.**
- **Linger only on human-in-the-loop.** Anything irreversible gets a human, and no amount of model quality changes that, because the question is not "will it be right" but "what happens the one time it is wrong."
- **Say that hierarchical is fashionable and usually wrong.** They will have seen multi-agent demos online; give them permission to be unimpressed.
- Useful framing if someone asks which one their project should use: the loop they wrote on page 13 *is* ReAct. They have already implemented one of the six.
- Plan-and-Execute has a specific institutional advantage worth naming in a government context: the plan is an artefact you can show someone before anything executes.
- **Energy dip warning.** This is a six-row table forty minutes into Block 2 and it is where the room goes quiet. One line each, keep moving, and get to page 16 where there is something to argue with.

---

## Slide 16 [13/20] · Guardrails, concretely

- **Two columns: four things you do before the call and four you do after, and the green box says the agent is the easy part while this slide is the work.**
- **Step cap — a bounded loop, always, and this is the third time today you have said it.**
- **Tool allow-list — a dictionary lookup, never dynamic dispatch on a model-supplied name.** The model can emit any string; if that string reaches `getattr` or `eval`, you have handed control of your process to whatever text happened to be in the context window.
- **Least privilege — use read-only tools wherever reading is enough.** A tool that can only read cannot be tricked into writing, no matter how good the injection is.
- **Argument validation — the model can produce any string it likes**, so a field typed `"integer"` in your schema is a request, not a guarantee. Validate on arrival.
- **Output validation — check the shape of what came back before you act on it.**
- **Stop conditions — budget, wall clock, and repeated identical calls.** Call out the last one specifically: it catches the spiral from page 14 cheaply, without waiting for the cap.
- **Human approval — for anything you cannot undo.**
- **A trace — every decision logged, so you can explain what happened.**
- **Say the line about time honestly: building an agent takes an afternoon, and making one you would be willing to leave running takes weeks, and all of that work is on this slide.**
- **The trace is what you will want at nine in the morning when somebody asks why the system did something strange.** In a government context, "we don't know why it did that" is not an acceptable answer, and the trace is the only thing that prevents it.
- Worth adding as your own line: the guardrails are not there because the model is malicious, they are there because the model is *unpredictable in a way that compounds*. One odd decision is fine; five odd decisions in a loop is an incident.
- **Forward to Thursday:** every item in the left column is a defence against something they will try to break on Thursday. Say that, because it makes this slide feel like preparation rather than a lecture on discipline.

---

## Slide 17 [14/20] · What a tool returns when it fails

- **Bad is `raise ValueError("not found")` and good is a returned dictionary containing an error message written for the model to read.**
- **The bad case has two failure modes and both are on the slide: the exception kills your loop, or you swallow it and the model sees nothing and invents an answer.**
- **The second failure mode is the dangerous one, because the output looks completely normal.**
- **The good message does three things: it says what was wrong, it shows what a valid id looks like, and it tells the model what to do next — ask the user to confirm.**
- **The model can read that, correct itself, and recover, which is the whole reason the loop exists.** A loop that cannot recover from a failed step is just a slower single call.
- **The green box is the line to remember: error messages are prompts, so write them for the model rather than for your log file.**
- **Say that this is a small idea that changes agent behaviour more than almost anything else, and almost nobody does it.**
- Practical version for their projects: log the stack trace for you, and return a short structured explanation to the model. Two different audiences, two different messages, from the same `except` block.
- Anticipated question: *"Won't a detailed error leak information?"* Yes, and that is a real trade-off — the error goes into the context, which means it can end up in the answer. Return the shape of a valid id, not a real one belonging to someone else.
- **The Be the Agent activity hits exactly this: a tool returns an error and the human "agent" has to recover from it, and that recovery is where the learning is.**

---

## Slide 18 [15/20] · Part Two — Agentic RAG

- **A divider, and the subtitle is the sentence of the week: yesterday's retriever becomes today's tool.**
- **Say it slowly and deliberately, because this is the moment the week joins up.**
- **Everything they built yesterday — chunking, hybrid search, re-ranking — is about to become a single function that an agent can choose to call, or not.**
- The word "or not" is doing real work in that sentence; emphasise it, because it is the entire difference from Monday.
- **Energy note.** This lands around 11:20 when attention is thinning. It is a good place to raise your voice slightly and get people looking up.

---

## Slide 19 [16/20] · Retrieval as one tool among several

- **Plain RAG always retrieves, always exactly once, even when the question needs no documents at all or needs three different searches.**
- **Agentic RAG lets the model decide three things: whether to search, what to search for, and whether the first result was good enough to answer from.**
- **The unlocks are on the right: a question needing retrieval *and* arithmetic, a bad first search that can be retried with better terms, and questions that skip retrieval entirely.**
- **The example question is the one to read aloud, because it needs two different capabilities in sequence: "What is our leave policy, and how many days would I have left after two weeks off?"**
- **The cost is stated honestly on the slide: unpredictable calls per question, and it is a trade, not an upgrade.**
- **Say the government-context point plainly: agentic retrieval is more capable and less predictable, and predictability is worth a great deal here.**
- **Give the project advice explicitly: build plain retrieval first, prove it works against the golden set, then add the agent on top only if they actually need multi-step behaviour.**
- The measurement problem is worth naming, because it is subtle and it will bite them tomorrow: their golden set scores *retrieval*, and with agentic RAG the retrieval query is no longer the user's question — the model rewrote it. So a golden set keyed to user questions no longer measures what they think it measures.
- **Callback to Monday, forward to Wednesday:** Monday gave them a fixed cost per question, which made caching easy. Agentic RAG gives them a variable cost per question, which is precisely what Wednesday's latency and cost session is about.

---

## Slide 20 *(unnumbered)* · CODE — Your retriever, as a tool

**Block purpose:** to show that wrapping an existing capability as a tool is a wrapper function and a schema — that they are ten lines away from an agentic system, and the ten lines are boring.

- **The first line is a comment saying "yesterday's function, unchanged," and the second is `from day2 import hybrid_search` — say that this is their own Monday code being imported rather than rewritten.**
- ⚠️ **`from day2 import hybrid_search` will fail in Colab unless a `day2.py` exists.** See fix list item 4 — this is the one that stops the lab dead.
- **`def search_documents(query: str, k: int = 4) -> list` is a thin wrapper, and its only job is to reshape the output for a model rather than for a human.**
- **The comment says to return the text AND the citation so the answer can cite, and that is the design decision on this slide.**
- **The return is a list comprehension, and for the non-coders that is a compact `for` loop that builds a list — read it as "for each result `r` in the search, make a small dictionary with these three fields."**
- **`r["text"][:600]` is slicing: take the first six hundred characters and discard the rest.** Slicing has appeared in this course before; name the callback.
- **The truncation is what keeps the loop affordable**, because these passages enter the conversation history and then get re-sent on *every* subsequent step. Untruncated passages are how a five-step agent becomes expensive.
- **`"source"` and `"page"` carry through because they kept the metadata on Monday morning** — that decision is what makes a cited answer possible today.
- **`search_decl` mirrors page 10 exactly: name, description, one typed property, one required field.**
- **The description says to use it for any question about internal policy, procedure or entitlement**, which is scope written in the vocabulary the users will actually use.
- **`"description": "Search terms, not the raw question"` is the clever line on the slide** — that is query rewriting, delegated to the model, expressed in a single string. Monday's re-ranking work happened in code; this achieves something similar with one sentence of documentation.
- **`TOOLS = {"search_documents": search_documents, "calculate": calculate}` is the allow-list from page 13, now with two entries.**
- ⚠️ **`search_decl` is created but never registered into a `cfg`, and `calculate` is never defined or declared anywhere in the deck.** See fix list items 5 and 8.
- **Note the deliberate asymmetry:** the Python function accepts `k`, and the schema does not expose it. That is not an oversight — it means the model cannot ask for a hundred results and blow up the context. Say it out loud, because it is a small, concrete example of least privilege from page 16.

**Arabic/RTL — this is the slide where it genuinely matters:**

- `r["text"][:600]` counts **characters, not tokens**. Arabic text runs roughly two to four times more tokens per character than English with most tokenisers, so the same 600-character truncation that keeps an English loop affordable can be several times more expensive on an Arabic corpus. If their project is on Arabic policy documents, 600 is not a safe default — suggest they measure it rather than inherit it.
- Slicing mid-string will cut a word in half, and in a mixed Arabic-English passage a cut inside a bidirectional run can make the trailing fragment *render* in a confusing order even though the bytes are fine. The model usually copes; the human reading the trace does not. If they print traces for Arabic content, truncate on a word boundary instead.
- The `"Search terms, not the raw question"` instruction interacts with language: with an Arabic question and an English tool description, the model sometimes emits English search terms against an Arabic index and retrieves nothing. If anyone's retrieval mysteriously returns empty in the lab, check the language of the emitted query first — it is the fastest diagnosis and it looks like magic when you spot it.

---

## Slide 21 [17/20] · Reading the trace

- **This is a real trace of two tool calls and a final answer, and the instruction is to read it out loud, line by line — it is the clearest picture of the week that exists.**
- **The goal combines two things: what is the annual leave for grade 11, and what would be left after taking twelve days.**
- **Step zero is `search_documents(query="annual leave entitlement grade 11")` returning "Grade 11 — 30 days" with the citation `leave_policy.pdf, p.4`.**
- **Notice the query is not the user's question — the model rewrote it into search terms, exactly as the tool description asked.**
- **Step one is `calculate(expression="30 - 12")` returning 18, and it is a tool because we do not trust the model with arithmetic.**
- **The model could not have known to do the subtraction until step zero came back with the number 30 — that dependency is what makes this an agent rather than a script.**
- **The final answer carries the citation through, and it carries it because the metadata was kept on Monday morning.**
- **Say the closing sentence and let it land: every decision on this screen was the model's, and every execution was yours.**
- **Point out that steps zero and one used different tools in the right order, chosen without being told.** That is the capability being demonstrated; everything else on the slide is scaffolding.
- **Callback chain worth naming explicitly, because this is the slide where it all connects:** the citation exists because of Monday's metadata, the arithmetic is a tool because of Sunday's next-token-predictor lesson, the query rewrite happened because of page 20's description string, and the whole thing is bounded because of page 13's cap.
- ⚠️ A `calculate` tool that evaluates a string expression is a code-execution surface. See fix list item 7 — worth knowing before someone asks how `calculate` is implemented.

---

## Slide 22 [18/20] · When not to build an agent

- **Two columns, and this slide will save somebody in the room a quarter of their project time.**
- **Do not build one when the task is one retrieval and one answer.**
- **Do not build one when the path is always the same, because that is a script, and scripts are testable.**
- **Do not build one when the action is irreversible and nobody is checking.**
- **Do not build one when you cannot afford unpredictable per-question cost.**
- **Do build one when the next step genuinely depends on what the last step returned.**
- **Do build one when several tools are needed and you cannot know which in advance.**
- **Do build one when the system must recover from partial failure on its own.**
- **The green box is the test to apply: "Could I write this as a fixed sequence?" — and if yes, write the fixed sequence.**
- **Say the honest thing: agents are the most interesting thing this course covers and the least often the right answer, and both of those are true at the same time.**
- **State the assessment rule explicitly, because this is what they are anxious about: an agent is not required for full marks, but a justified architecture is.** Say it twice.
- The testability point deserves ten extra seconds: a fixed sequence gives the same output for the same input, so you can write a unit test. An agent gives you a distribution, and testing a distribution needs an evaluation set — which is more work than the agent saved.
- **Ask the room:** "Whose project is actually one retrieval and one answer?" A few honest hands here will save you three rescue conversations this afternoon.

---

## Slide 23 [19/20] · Lab — Build the loop yourself

- **The notebook is `day3_agents.ipynb`, and it has five parts listed on the left.**
- **They build two real tools and then their schemas, so declaration comes after the function, in that order.**
- **The round trip is done by hand in four separate cells, which is page 12 made unavoidable.**
- **Then `run_agent` with a step cap and a printed trace, which is page 13, given complete — read it, don't retype it.**
- **Then they remove the cap and watch it spiral, deliberately, and they should run it and interrupt it themselves.**
- **Finally their Day 2 retriever gets registered as `search_documents`, which is the payoff.**
- **The right panel is project time from 1:00, and the gate at 2:30 is documents loaded, chunked, embedded, and one query returning something — running, not polished.**
- **Say that anyone still stuck at 2:00 gets you sitting next to them, and mean it.**
- **Tell them you are not presenting this afternoon at all, that you will be circulating, and that you will check on every pair at least twice.**
- **The day ends with a five-minute stand-up, one sentence per pair on where they got to.**

**What to look for while circulating, in the order it will happen:**

- First fifteen minutes: import errors and missing API keys. Nothing conceptual. Have the key setup cell ready to point at.
- Next: someone whose `history` is stale from an out-of-order run, whose agent answers a question they did not ask. The tell is an answer that is coherent and irrelevant.
- Then: someone whose tool is never called. Ninety per cent of the time it is the description, not the code — send them back to page 11 before you read their loop.
- Then: someone whose `**call.args` throws a `TypeError` because the model supplied an argument their function does not accept. That is a real lesson; let them find it, then point at page 16's "argument validation."
- Late in the session: the pair who got it working and are now adding a third tool. Give them the Arabic-query problem from page 20 to chew on.
- **When the spiral demo underwhelms** — the model answers sensibly and refuses to loop — say that a well-behaved model is exactly why the cap looks unnecessary right up until it isn't, and show them the trace from page 14 instead. Do not fight the demo.

---

## Slide 24 [20/20] · What today was

- **Four lines, and the first is the one you have said three times today on purpose: the model requests, your code executes, and that boundary is where all your control lives.**
- **Second, the tool description is the interface — vague description, broken tool.**
- **Third, an agent is a bounded loop, and the cap, the allow-list and the trace are not optional extras.**
- **Fourth, yesterday's retriever is now a tool, and that is the whole week joining up.**
- **Set up tomorrow precisely: you stop adding capability and start measuring what exists — latency, tokens, cost, and a cache hit rate taken from their own project.**
- **Tell them to bring their project running even if it is ugly, because tomorrow only works if there is something to instrument.**
- Add one closing line of your own that page 22 has earned: the best answer some of them will give tomorrow is "I looked at an agent and decided not to build one, and here is why."

---

# Fix list — before you present

Ordered by how badly it will hurt you.

---

### 1. `run_agent` accepts a `tools` argument it never uses — silent wrong behaviour

**Where:** page 13, `def run_agent(goal, tools, max_steps=5, verbose=True)`.

The body never touches `tools`. It reads `cfg` and `TOOLS` from module scope instead. So a student who does the natural thing —

```python
run_agent("what is my leave balance?", tools=[leave_tool])
```

— gets a run that uses whatever `cfg` and `TOOLS` happen to be defined globally, which may be a completely different tool set. It does not error. It produces a plausible answer using the wrong tools. This is the worst kind of bug for a classroom because the failure looks like success.

**Fix (deck and notebook), option A — make the parameter real:**

```python
def run_agent(goal, tools, tool_impls, max_steps=5, verbose=True):
    cfg = types.GenerateContentConfig(
        tools=[types.Tool(function_declarations=tools)])
    history = [user_message(goal)]
    ...
        fn = tool_impls.get(call.name)
```

**Fix, option B — remove the parameter and be honest about the globals:**

```python
def run_agent(goal, max_steps=5, verbose=True):   # uses module-level cfg and TOOLS
```

Option B is fewer characters on the slide and easier to read at the back of the room. Option A is better engineering and sets up the "least privilege" idea from page 16 nicely — you can give one agent two tools and another agent five. **My recommendation: option B on the slide, option A in the notebook**, with a comment saying why they differ.

**Keeping it as-is would make a decent exercise** — "this function takes an argument it ignores, find it" — but only if you flag it deliberately. If you leave it silent, at least two pairs will lose twenty minutes to it this afternoon and you will not get that time back.

---

### 2. `parts[0]` will not always be the function call

**Where:** page 12 (`r.candidates[0].content.parts[0].function_call`) and page 13 (`part = r.candidates[0].content.parts[0]`).

A response can contain more than one part. Three realistic cases:

- The model emits a sentence of text *before* the function call, so `parts[0]` is a text part and `parts[0].function_call` is `None` — the loop concludes the agent has finished and returns a half-answer.
- The model requests two tools in one turn (parallel function calling), and you silently execute only the first — the second result never comes back and the model retries, which looks exactly like a spiral.
- Thinking-style output is enabled and a reasoning part arrives first.

None of these crash. All of them produce a wrong answer that reads fine.

**Fix — scan the parts instead of indexing:**

```python
parts = r.candidates[0].content.parts or []
calls = [p.function_call for p in parts if getattr(p, "function_call", None)]
if not calls:
    return r.text
for call in calls:            # handles the parallel case too
    fn = TOOLS.get(call.name)
    ...
```

**Verify before you present:** run one prompt that should trigger two tools at once — for example *"what is my leave balance and what is 17 times 3"* — and `print(len(r.candidates[0].content.parts))`. If it prints more than 1, the current slide code is broken for that prompt and you should say so when you show it. If it prints 1, the slide is fine for today and you can mention the multi-part case as a caveat rather than a bug.

Whether the model actually emits parallel calls depends on current SDK and model behaviour that I cannot check from here, so run it rather than trusting either of us.

---

### 3. The uncapped spiral demo, times thirty, on a shared free tier

**Where:** page 14 and the corresponding notebook cell.

Deliberately uncapped loops running simultaneously on thirty machines against a free-tier quota will exhaust the room's rate limit. If they share one project key, the first pair to run it takes everyone else down, and you lose Block 3. If each has their own free key, they will each hit a per-minute limit, which at least fails locally.

**Fix — cap the "uncapped" demo at a number large enough to feel bad and small enough to be safe:**

```python
# "Uncapped" — in a classroom, 12 is plenty to make the point.
run_agent(impossible_goal, max_steps=12, verbose=True)
```

Twelve printed lines of near-identical calls makes the point as well as infinity does, and it terminates on its own so nobody has to remember to interrupt it.

Also: have a screenshot or a pre-recorded trace ready. If the room's quota is gone, you show the screenshot and carry on rather than debugging in front of thirty people.

**Verify before you present:** confirm whether the room is on one shared key or individual keys. The answer changes your instructions completely — with one shared key, tell them to run the spiral cell in a specific order or not at all.

---

### 4. `from day2 import hybrid_search` will fail for everyone in Colab

**Where:** page 20, first line of code.

Day 2 was a notebook. There is no `day2.py` on a fresh Colab runtime, so this import raises `ModuleNotFoundError` and the agentic-RAG section of the lab dies at line one. This is the single most likely thing to stop the lab.

**Fix — pick one and make sure the deck and the notebook agree:**

- **Cleanest:** ship a `day2_utils.py` alongside the notebooks and have the lab download it, then change the slide to `from day2_utils import hybrid_search`.
- **Simplest:** put `hybrid_search` in a cell in `day3_agents.ipynb` with a comment saying it is Monday's function copied verbatim. Costs a slide of scrolling, works every time.
- **Most fragile:** `%run day2_rag.ipynb`, which re-executes Monday's whole notebook including its embedding step. Do not do this — it re-embeds the corpus and burns quota.

Whichever you choose, the slide should say it. If the slide says `from day2 import` and the notebook does something else, half the room will type what is on the screen.

---

### 5. `search_decl` is never registered, so the agent cannot call the retriever

**Where:** page 20.

The slide builds `search_decl` and builds the `TOOLS` dictionary, but never rebuilds `cfg`. The implementation is in the allow-list and the declaration is not in the config, so the model is never told the tool exists. The agent will simply never call it, and the symptom — "my retriever tool is never used" — looks like a description problem from page 11 and is not.

**Fix — add two lines to the slide, after `TOOLS`:**

```python
cfg = types.GenerateContentConfig(
    tools=[types.Tool(function_declarations=[search_decl, calculate_decl])])
```

This also closes the loop on page 12's wiring and makes the "declaration and implementation are two separate things" lesson land properly: they have to update *both* to add a tool. That is a genuinely useful thing for them to feel.

---

### 6. Two schedule errors on page 3

- **`2:25 – 2:25 Break` is zero minutes long.** It should almost certainly be `2:20 – 2:25`, with project time ending at 2:20.
- **Page 3 says project time runs `1:00 – 2:25`; page 23 says `1:00–2:30`.** Pick one. Given the gate is stated as 2:30 on page 23 and "half past two" in page 3's presenter notes, and the stand-up is 2:25–2:30, the consistent reading is: project time 1:00–2:20, break 2:20–2:25, stand-up 2:25–2:30 — and the *gate* is 2:20, not 2:30.

Someone will photograph this slide and hold you to it. Fix both before you print.

---

### 7. `calculate(expression="30 - 12")` — check what is inside it

**Where:** page 20 (`TOOLS`) and page 21 (the trace).

A tool that takes a string expression and returns a number is almost always implemented with `eval()`. If the notebook's `calculate` uses bare `eval`, you have a live remote-code-execution path in a course that teaches prompt injection on Thursday — the model chooses that string, and on Thursday they will be trying to make the model choose strings. Somebody sharp will notice, and you want to have noticed first.

**Verify before you present:** open the notebook and search for `def calculate`. If you see `eval(`, replace it.

**Fix — restrict to arithmetic:**

```python
import ast, operator

_OPS = {ast.Add: operator.add, ast.Sub: operator.sub,
        ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.USub: operator.neg}

def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp):
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp):
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError("unsupported expression")

def calculate(expression: str) -> dict:
    try:
        return {"result": _eval(ast.parse(expression, mode="eval").body)}
    except Exception:
        return {"error": f"Could not evaluate '{expression}'. "
                         "Use plain arithmetic like '30 - 12'."}
```

Note that the error branch follows page 17's rule — it returns a readable message rather than raising — so this doubles as a worked example of the slide you just taught. **This is worth showing in Block 2 if you have the time**, because it makes "least privilege" concrete: the tool does arithmetic and *only* arithmetic, by construction rather than by hope.

---

### 8. `calculate` is used but never defined or declared in the deck

**Where:** page 20's `TOOLS` dict and page 21's trace both reference it; no slide defines it and no slide shows a `FunctionDeclaration` for it.

Less severe than item 7 because the notebook presumably has it, but someone reading only the deck cannot reproduce page 21. If you have room, add `calculate_decl` beside `search_decl` on page 20 — it costs four lines and makes the point that a two-tool agent needs two declarations.

---

### 9. The four code slides have no footer, no logos, and no presenter notes

**Where:** pages 10, 12, 13, 20.

Consequences, in order of annoyance:

- The footer counts 20 slides where there are 24, so "we're on slide 12" means different things to you and to the room.
- **Page 13's slide title, "CODE · AUTOMATING IT / The agent loop", is orphaned at the bottom of page 12** in the PDF export, with the code body alone on page 13. If you present from this PDF, one page ends with a heading and the next has no heading at all.
- The SDAIA and Academy logos are missing on those four pages. If any of this is being filmed or archived, that is a branding inconsistency someone will raise.

**Fix:** in the deck source, apply the standard slide chrome to the code slide template, and give the code slides a `page-break-inside: avoid` (or the equivalent in your export path) so a code slide cannot split across two printed pages. Then re-export and confirm the count reads `24 / 24`.

If you cannot fix it this morning: know that PDF pages 10, 12, 13 and 20 are code slides, and do not trust the footer.

---

### 10. Undefined helpers on the code slides

**Where:** pages 12 and 13 reference `history`, `MODEL`, `client`, `cfg`, `TOOLS`, `user_message` and `tool_result`; none are defined on any slide.

This is a legitimate slide-design choice — you are showing the eight interesting lines — but somebody will ask, and "it's in the notebook" is only a good answer if it is true.

**Verify before you present:** open `day3_agents.ipynb` and confirm all seven names exist and are defined *before* the cell that uses them. In particular `user_message` and `tool_result` are the two most likely to have been written on a slide and never actually implemented.

---

### 11. Page 3's presenter note describes a Day 2 gate

**Where:** page 3 notes, "The gate at half past two is documents loaded, chunked, embedded, and one query returning something."

Chunking and embedding are Monday's work, and today's lab is agents. This is consistent with page 23, so I assume it is deliberate — the *project* gate is the RAG pipeline, independent of today's *lab*. But say that distinction out loud, because on a day about agents a room will hear "the gate is retrieval" and think they have misunderstood the assignment.

---

# Not bugs — do not "fix" these

- **`role="user"` on the function response** (page 12). It looks wrong. It is the documented pattern for this SDK — the tool result arrives on the user turn because, from the model's perspective, the environment is what spoke. Leave it.
- **`getattr(part, "function_call", None)`** (page 13). `part.function_call` normally exists and is `None` when absent, so the `getattr` is belt-and-braces rather than necessary. It is harmless and it is good defensive style. Leave it.
- **`dest="JED "` with a trailing space** (page 14). Looks like a typo in your deck; it is the entire point of the example — the model perturbing an argument trivially rather than changing strategy. Keep it, and say so before someone tells you about it afterwards.
- **`search_documents` accepts `k` but the schema does not expose it** (page 20). This is deliberate least privilege, not an omission. Call it out as a feature.
- **The adjacent string literals in the `description` fields** (pages 10 and 20). Python joins them automatically. Not a missing `+`.
- **`response={"result": result}`** (page 12). The API wants a structured object, so wrapping a return value in a single-key dict is correct even when the value is already a dict.
- **`return "Stopped: step limit reached."` rather than raising** (page 13). Returning a string when the cap fires is the right call — the caller gets a result to inspect rather than an exception to catch, which matches page 17's philosophy.
- **The five-day week running Sunday to Thursday** (page 2). Correct for SDAIA. Day 3 is Tuesday. No inconsistency.

---

# Two things I added that aren't in your material

## A. "Be the Agent" — the activity your agenda promises and no slide describes

Page 3 puts *Be the Agent* inside Block 1, and page 17's notes reference it as though it is defined, but nothing in the deck explains it. Here is a version that runs in twelve minutes and lands pages 8, 9 and 17 at once.

**Setup.** Pairs. One person is the **Model**, one is the **Application**. The Model gets a goal on a card and a printed list of two tool descriptions. The Model may *not* look anything up, do arithmetic, or use a phone — the Model can only write requests on paper.

**The rules.**
- The Model writes a request on a slip: tool name plus arguments. Nothing else.
- The Application reads the slip and decides: honour it, or refuse it.
- If honoured, the Application looks up the answer on a **results sheet you hold** and writes it back on the slip.
- Repeat until the Model can write a final answer, or until five slips have been exchanged — the cap.

**The goal card:** *"What is the annual leave for grade 11, and how many days would be left after taking 12?"*

**Tool descriptions given to the Model:**
- `search_documents(query)` — searches organisation policy documents, returns passages with source and page.
- `calculate(expression)` — evaluates a plain arithmetic expression.

**The trap, which is the whole point.** Your results sheet returns an *error* for the first plausible query. Make `search_documents(query="grade 11 leave")` return:

> `{"error": "No results. Try naming the entitlement type, e.g. 'annual leave entitlement'."}`

Now the pair has to do exactly what page 17 describes: read an error written for them, correct the query, and recover. The pairs who recover in one step wrote the second query using the hint. The pairs who spiral will re-send the same query — and you now have a live, human-generated version of page 14 to point at.

**Debrief in three questions, three minutes:**
1. Who executed anything? *(Only the Application. The Model wrote requests.)*
2. What did the error message have to contain for you to recover? *(What was wrong, and what a valid input looks like.)*
3. Did anyone hit the five-slip cap? *(If so, why — and would a smarter Model have helped?)*

If you are short on time, cut the calculate step and keep the error — the recovery is where the learning is, and it is what page 17 promises they will experience.

## B. The answer key for page 5

Included in the Slide 5 section above, since you will be standing in front of the room when you need it rather than scrolling to the end.
