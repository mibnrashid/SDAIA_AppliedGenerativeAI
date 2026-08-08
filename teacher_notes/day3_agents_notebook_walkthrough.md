# `day3_agents.ipynb` — cell-by-cell instructor notes
**Day 3 · Tools and agents · Applied Generative AI · SDAIA Academy**

---

## How to read this

- One section per cell, in notebook order, numbered 1–20 the way Colab counts them (markdown cells included).
- **Bold = what is actually in the cell, unpacked.** Read these and you have covered the cell.
- Plain text = depth to have ready that is *not* on screen: mechanism, idioms the non-coders will trip on, anticipated questions, honest caveats.
- Bullets run foundation → detail → payoff. Stop anywhere and you have still said something complete.
- Every bullet is a full sentence you can say out loud without supplementing from memory.

**Before anything else:** this notebook has **no execution counts and no stored outputs** on any of the fourteen code cells. It has not been run end to end, or the outputs were stripped. Everything I say below about what a cell *will* print is reasoning from the code, not from a recorded run. Fix list item 1 is "run it once yourself" and I mean it literally.

---

## Shape of the notebook

**Cells 1–5 — the parts.** Setup and key, two real tool functions, a markdown aside about mocking, then the two declarations wired into `TOOLS` and `CFG`. Nothing agentic yet. This is the "a tool is two objects" lesson made concrete.

**Cells 6–10 — the round trip, by hand.** Four code cells, one per step of the loop, then a markdown cell that says the load-bearing thing out loud. This is the heart of the morning and it maps exactly to the deck's "Doing it by hand, once" slide.

**Cells 11–13 — automation and extension.** `run_agent` given complete, a two-step demo with a printed trace, then the TODO where they add a third tool and see that registration is a two-place change.

**Cells 14–16 — the failure and the control.** The expensive-loop demo, a markdown cell on cost, then an output validator that closes the loop back to Day 1's structured output.

**Cells 17–18 — the ceiling.** Agentic RAG: their Day 2 retriever wrapped as a tool, with a question that needs retrieval *and* arithmetic.

**Cells 19–20 — reflection and troubleshooting.** A written reflection you collect by walking round, and a symptom/cause/fix table.

**Deck ↔ notebook mapping:**

| Deck (PDF page) | Notebook cells |
|---|---|
| Code — a tool declaration (p.10) | 2, 3, 5 |
| A vague description (p.11) | 5, and the TODO in 13 |
| Code — doing it by hand (p.12) | 6, 7, 8, 9, 10 |
| Code — the agent loop (p.13) | 11, 12 |
| Take the cap off (p.14) | 14, 15 |
| Guardrails (p.16) | 2, 11, 16 |
| Error messages (p.17) | 3, 4 |
| Your retriever as a tool (p.20) | 17, 18 |
| Reading the trace (p.21) | 12, 18 |

⚠️ **The deck and the notebook do not show the same code.** Three real divergences — `run_agent`'s signature, the Day 2 import, and the helper functions. See fix list items 3 and 4. Students *will* compare the screen to the notebook.

---

## Cell 1 — Setup, imports and the API key

**Purpose:** get a working client and fail loudly with instructions if the key is missing. Every classroom minute lost in the first ten minutes is lost to this cell, so it is written defensively.

- **`!pip install -q google-genai` installs the SDK, and the `-q` is there so the output stays readable on a projector — say that, because it explains why nothing appears to happen.**
- **The imports are `from google import genai` for the SDK and `from google.genai import types` for the config and content classes, and those two names appear constantly for the rest of the notebook.**
- Explain the split once: `genai` gives you the client that makes network calls, and `types` gives you the little data classes that describe what you are sending. Almost every confusing error today will be a `types` object built wrong.
- **The key comes from Colab Secrets via `userdata.get('GEMINI_API_KEY')` and never lives in the notebook — say why: a notebook gets shared, screenshotted and committed, and a key in a cell is a key on GitHub.**
- **The `try`/`except` wraps the whole key lookup and raises `SystemExit` with six numbered setup steps, so a missing key produces instructions rather than a traceback.**
- `SystemExit` is deliberate and worth naming: in Colab it stops the cell quietly instead of printing forty lines of red, which is exactly what you want in front of thirty people.
- The `except Exception` catches everything, including the `ImportError` you would get outside Colab. That is fine here and it means the message is always the same one. If anyone runs this locally, the message will be misleading — tell them to set `API_KEY = os.environ[...]` instead.
- **`MODEL = "gemini-2.5-flash-lite"` is described in the comment as fast and cheap, and it is what the whole week uses.**
- ⚠️ Flash-lite is the smallest model in the family, and *everything today depends on it choosing tools correctly*. See fix list item 2 — this is worth thirty seconds of your time before class.
- **`EMBED_MODEL = "gemini-embedding-001"` is defined here but never used in this notebook** — it is there so that pasted Day 2 code finds the name it expects. Say that when someone spots it, rather than letting it look like a leftover.
- `import os, json, time` — `json` is used constantly, `os` and `time` are not used at all in this notebook. Harmless.
- **What will go wrong in the next ten minutes:** three people will have created the secret but left "Notebook access" off, which produces exactly the same failure as having no secret at all. Say the toggle out loud before they run the cell — it is step 5 in the message and it is the step everyone skips.
- **Say verbatim:** *"If this cell fails, it is almost certainly the key. Do not debug anything else until this prints Ready."*

---

## Cell 2 — Tool 1, `calculate`

**Purpose:** show that a tool is an ordinary function, and demonstrate argument validation before the concept has even been named.

- **The comment says it plainly: this is a real function and there is nothing AI about it.**
- **`def calculate(expression: str) -> str` takes a string and returns a string, and the return being a *string* rather than a number is deliberate — everything a tool returns has to survive being put back into a conversation.**
- **`allowed = set("0123456789+-*/(). ")` is a character allow-list, and the comment states the principle: the model can produce ANY string, so validating the argument is your job.**
- **`if not set(expression) <= allowed` is subset-checking between sets, and for the non-coders that reads as "is every character in the expression one of the permitted ones."** The `<=` on sets means "is a subset of", not "less than" — say that, because it looks like a comparison and is not.
- Point out why an allow-list rather than a block-list: you cannot enumerate everything dangerous, but you can enumerate the fourteen characters arithmetic needs. This is the same reasoning as the tool allow-list in `run_agent`.
- **`eval(expression)` is the actual evaluation, with the `# noqa` comment acknowledging that raw `eval` is normally forbidden and is being permitted here because the input was validated above.**
- ⚠️ **The validation has a real hole: `**` is two allowed characters, so `9**9**9` passes and will hang the kernel.** See fix list item 5. This is genuinely worth fixing *and* genuinely worth showing.
- **Both the success and failure paths return `json.dumps({...})`, so the model always receives the same shape** — a JSON object with either a `result` key or an `error` key. Consistency of shape is what lets the model handle both without special-casing.
- **The two print statements at the bottom are a self-test: `(420 + 75) * 3` succeeds and `import os` is rejected, and the comment says "rejected, as it should be."**
- **Run this cell and read both lines of output out loud.** The second line is the first time the room sees a guardrail actually firing, and it costs you five seconds.
- **Callback to Day 1:** they already learned that the model produces text, not values. This function is the boundary that turns text back into a value you can trust.
- **Forward to Thursday:** this cell is the first thing an attacker will look at. Say so now, lightly, and it will pay off on Thursday when someone tries to get past that character set.

---

## Cell 3 — Tool 2, `get_weather`

**Purpose:** a deliberately mocked tool, so the lesson is the loop rather than somebody else's API. It also sets up the good-error-message principle before you teach it.

- **`WEATHER` is a hardcoded dictionary of three Saudi cities with a temperature and a sky condition each — Riyadh, Jeddah and Abha.**
- **The cities are chosen so the numbers are memorable: Riyadh at 41, Jeddah at 34 and humid, Abha at 22 and cloudy.** The Abha number is the one to point at, because a room in Riyadh knows exactly why it is twenty degrees cooler and it makes the mock feel real.
- **`data = WEATHER.get(city.strip().lower())` normalises the input before lookup**, and that matters because the model might send `"Riyadh"`, `"riyadh"` or `" Jeddah "` on different runs. Without `.lower()` this tool would fail intermittently, which is the worst kind of failure to debug in a classroom.
- **The failure branch returns a JSON object with an `error` *and* a `known_cities` list, and the comment above it states the principle: a good error says what was wrong AND what a valid input looks like, so the model can recover instead of hallucinating.**
- **`sorted(WEATHER.keys())` returns the valid inputs in a stable order** — stability matters more than it looks, because a changing list changes the prompt and therefore the model's behaviour between runs.
- **The success branch returns the city, the temperature in Celsius, and the sky.** Note the key is `"celsius"` and not `"temp"` — units in the key name, so the model cannot guess wrong. That is the same lesson as the deck's "scope, units, and an explicit exclusion" slide.
- **The two prints test both paths: `Riyadh` works and `Paris` fails.**
- ⚠️ This error message is *so* good that it will probably prevent the spiral demo in cell 14 from spiralling. That is not a contradiction to hide — see fix list item 6, where I suggest turning it into the best five minutes of the lab.
- **Ask the room:** "What would this have returned if I had just written `return None`?" You want someone to say that the model would have had nothing to work with and would have made something up.

---

## Cell 4 — Markdown: why a mock is fine here

- **The claim is that the loop is the lesson, not the API, and that a real weather service would add an account, a key and a failure mode while teaching nothing about agents.**
- **The reassurance for their projects is that only the function body changes — the declaration, the loop and the guardrails all stay identical.**
- **The last paragraph re-states the error-message principle: error messages are prompts, so write them for the model rather than for your log file.**
- Read the last paragraph aloud even though it is markdown, because it is the deck's page 17 arriving early and the repetition is what makes it stick.
- Useful addition for the developers, who will be itching to wire something real: the mock is also *deterministic*, which means everyone in the room sees the same trace and you can debug collectively. A live API would give twenty different traces.
- **Energy note.** This is a good thirty-second breather before cell 5, which is the densest cell in the first half.

---

## Cell 5 — Declarations, `TOOLS`, and `CFG`

**Purpose:** the second half of "a tool is two objects." The functions exist; now they get described to the model and registered. This is the cell that the whole notebook's wiring depends on.

- **The comment calls the declarations "the menu the model reads," and that is the metaphor to use — the model gets a menu, not a kitchen.**
- **`calc_decl = types.FunctionDeclaration(...)` starts with `name="calculate"`, and the inline comment says it must match your function name.** It must actually match the *key in `TOOLS`*, which happens to equal the function name here; say that distinction if anyone renames something.
- **The `description` field carries an arrow comment saying it is THE most important field, and it does two jobs: it says what the tool returns, and it says when to use it.**
- **The second sentence — "Use this for any calculation instead of doing arithmetic yourself" — is an instruction to the model, not a description of the function.** That is the trick worth naming: descriptions can contain policy, and this one is preventing the failure from the deck's "unreliable arithmetic" card.
- **The parentheses around the two string fragments join them into one string automatically** — no `+` needed, and the trailing space at the end of the first fragment is doing real work.
- **`parameters` is JSON Schema with `"type": "object"` at the top, one property, and a `required` list — the same structure they wrote on Day 1.**
- **`"description": "Arithmetic only, e.g. '(420 + 75) * 3'"` includes a worked example, and the example teaches the format better than any amount of prose.**
- **`weather_decl` follows the identical pattern, and its description ends with an explicit limit: "Only covers Riyadh, Jeddah and Abha."**
- **That closing sentence is the "explicit exclusion" from the deck's page 11, and it is the reason the model will not confidently try Paris more than once.** Point at it.
- **`TOOLS = {"calculate": calculate, "get_weather": get_weather}` maps names to actual functions and is the allow-list.**
- **`tool_config = types.Tool(function_declarations=[calc_decl, weather_decl])` bundles the declarations, and `CFG = types.GenerateContentConfig(tools=[tool_config], temperature=0.0)` is what actually gets sent.**
- **Name the two-level nesting explicitly, because it causes real errors: a `Tool` holds a list of declarations, and the config holds a list of `Tool`s.** Passing a bare `FunctionDeclaration` into `tools=` produces a confusing type error.
- **`temperature=0.0` makes tool choice as deterministic as it gets**, which is why the room mostly sees the same trace. Say that you set it deliberately for teaching, and that in production you would still want it low for tool selection specifically.
- **Say the structural point out loud: `TOOLS` and `tool_config` are two separate lists of the same tools, and adding a tool means updating both.** This is the exact thing cell 13 makes them do and cell 18 gets wrong.
- **`print("Declared:", list(TOOLS))` should print both names.** If it prints one, they edited the dict.
- **Hidden dependency:** every later cell reads `TOOLS` and `CFG` from module scope. Cells 13 and 18 both *rebuild* them. Anyone running cells out of order gets whichever version ran most recently, and no error.

---

## Cell 6 — Round trip, step 1 of 4: ask

**Purpose:** demonstrate that a request containing tools produces a *request back*, not an answer. This is the cell that makes page 8 of the deck concrete.

- **`history` is created here as a list containing one `types.Content` with `role="user"`, and this is the only place `history` is initialised in the first half of the notebook.**
- **`types.Part.from_text(text=...)` builds the text part**, and the `text=` keyword is required — positional will fail in current SDK versions.
- **The question is "What is the temperature in Jeddah, and what is that in Fahrenheit?", and it is deliberately two-part: one lookup, then one calculation that depends on the lookup's answer.**
- **That dependency is what makes this an agent problem rather than a script problem — the model cannot do the conversion until it knows the number.** Say this before you run the cell, so they know what to watch for.
- **`r1 = client.models.generate_content(model=MODEL, contents=history, config=CFG)` sends the conversation plus the tool menu.**
- **`print("Any text answer?", repr(r1.text))` is the punchline: it should print `None` or an empty string, because the model did not answer.**
- **`repr()` is used rather than plain printing so that `None` and `''` are visibly different from a real answer** — without `repr`, `None` prints as the word None and an empty string prints as nothing at all, which looks like a bug.
- ⚠️ In recent SDK versions, accessing `.text` when the response contains only a function call may emit a warning to stderr alongside the `None`. That yellow text is expected and is not an error. Warn the room before it appears, or somebody will put their hand up.
- **The last print says it plainly: it did not answer, it made a request, look at the next cell.**
- **Pause here for five seconds.** This is the moment the abstract claim from the deck becomes something they watched happen.

---

## Cell 7 — Round trip, step 2 of 4: inspect

**Purpose:** open up the response object so they can see the request as data. Nothing has executed yet and the cell says so.

- **`part = r1.candidates[0].content.parts[0]` walks down the response structure, and `call = part.function_call` pulls out the request.**
- **Explain the chain in plain language once: a response can hold several candidate answers, each candidate has content, content has parts, and one of those parts may be a function call.** It looks long because the same structure has to carry text, images and multiple parallel calls.
- **`print("tool requested :", call.name)` should print `get_weather`, and `print("arguments :", dict(call.args))` should print something like `{'city': 'Jeddah'}`.**
- **`dict(call.args)` is a conversion, not decoration** — `call.args` is a protobuf map object that prints unhelpfully, and wrapping it in `dict()` gives you a normal Python dictionary you can read on a projector.
- **The closing print is the line to say aloud: nothing has executed, no function has run, this is a message.**
- ⚠️ **`parts[0]` assumes the function call is the first part, and this cell will crash with `AttributeError: 'NoneType' object has no attribute 'name'` if the model answers with text first.** See fix list item 7 — this is the cell most likely to fail live.
- **What to say if it does crash:** "That is the model deciding it did not need a tool, which is a legitimate outcome — and it is exactly why the real loop on cell 11 checks whether a function call is present instead of assuming." Then move to cell 11's logic. That recovery turns a failure into the lesson.
- **Ask the room:** "Has anything happened in Jeddah yet?" You want a no. The point is that a request and an action are different objects.

---

## Cell 8 — Round trip, step 3 of 4: execute

**Purpose:** the single most important cell in the notebook. This is where code runs, and it is code they wrote.

- **`fn = TOOLS[call.name]` looks the name up in the allow-list, and the comment says it: allow-list lookup, not `eval`.**
- **Say the alternative out loud so the allow-list means something: without it you would be doing `globals()[call.name]` or `eval(call.name)`, which hands a remote system the ability to name any function in your process.**
- **`result = fn(**dict(call.args))` is dictionary unpacking**, and for the non-coders that means "take this dictionary of names and values and pass them in as named arguments" — so `{'city': 'Jeddah'}` becomes `get_weather(city='Jeddah')`.
- **The comment on the first line is the one to read verbatim: delete this cell and nothing happens.** That is the entire deck in seven words.
- **The closing print says this is also where you check whether this user is allowed to call this tool with these arguments** — and the model has no idea who is asking, and never will.
- ⚠️ `TOOLS[call.name]` uses direct indexing, so an unknown name raises `KeyError` here, whereas `run_agent` in cell 11 uses `.get()` and returns a readable error instead. That difference is defensible in a step-by-step teaching cell, but be ready to explain it — see fix list item 9.
- ⚠️ `fn(**dict(call.args))` will raise `TypeError` if the model supplies a key the function does not accept. That is a real thing that happens, and it is the second row of the troubleshooting table in cell 20.
- **Put your finger on this cell when you talk about permissions.** Physically pointing at one cell and saying "this, here, is where your organisation's access control lives" lands better than any slide.

---

## Cell 9 — Round trip, step 4 of 4: return

**Purpose:** close the loop once, and reveal that a second tool call is needed — which motivates automating it.

- **There are two appends and the order matters: first `r1.candidates[0].content`, which is what the model said, then the function response, which is what your code found.**
- **If you append only the result, the conversation contains an answer to a question it does not contain, and the model gets confused or refuses.** Say that; it is the first row of the cell 20 troubleshooting table and it is the most common student bug.
- **`types.Part.from_function_response(name=call.name, response={"result": result})` wraps the result, and the `name=` must match so the model can pair the answer with its own request.**
- **The `role="user"` on the function response looks wrong and is correct** — in this SDK the tool result arrives on the user turn, because from the model's point of view the environment is what spoke. Flag it before someone helpfully "fixes" it.
- **`response={"result": result}` wraps a JSON string inside a dict, so it is technically double-encoded** — the model reads it fine, and the API requires a structured object rather than a bare value. Not a bug; see the "not bugs" list.
- **`r2` is the second call, and the cell then checks whether the model wants *another* tool.**
- **This is the reveal: the comment says it may want the Fahrenheit conversion, and that is the loop.** If the trace shows `calculate` requested at this point, you have earned cell 11 — say "and that is why we stop doing this by hand."
- **`if getattr(part2, "function_call", None)` is the same defensive check that `run_agent` uses**, and it is here so this cell does not crash when the model is finished.
- ⚠️ **Running this cell twice appends the same pair again**, and the model then sees a duplicated tool exchange. The symptom is a strange repetitive answer, and the fix is to re-run from cell 6. Warn them before they run it, because at least one person will click twice.
- **Invariant to state plainly:** `history` grows every time this cell runs and is never reset except in cell 6. On a kernel restart, cell 9 alone raises `NameError`. Cells 6 through 9 are a unit and must be run in order.

---

## Cell 10 — Markdown: say it again

- **The claim is that across four cells, the only thing that executed any code was cell 8, which they wrote and control.**
- **The model produced a message meaning "I would like `get_weather` with `city='Jeddah'`", and the application read that message and chose to honour it.**
- **That choice point is the only place permissions can be enforced.**
- **On Thursday it is the difference between a prompt injection being a nuisance and being a breach, because whatever an attacker makes the model *ask* for, your code decides whether to actually *do*.**
- **This is the second of the three times you say this today.** Read the whole cell aloud rather than letting them skim it.
- **Pause point.** Ten seconds of silence after the Thursday sentence.

---

## Cell 11 — `run_agent`, given complete

**Purpose:** the same four steps, in a bounded loop, with all four guardrails visible. Given complete on purpose so the forty minutes go into reading rather than typing.

- **The first comment says GIVEN COMPLETE — read it, do not retype it. Say that out loud; twenty people typing this is fifteen minutes you do not have.**
- **`def run_agent(goal, max_steps=5, verbose=True)` — three parameters, and the defaults are decisions rather than placeholders.**
- ⚠️ **This signature differs from the deck**, which shows an extra `tools` parameter. The notebook version is the correct one. See fix list item 3.
- **`history = [...]` starts a fresh conversation containing only the goal, so every call to `run_agent` is independent and remembers nothing from previous calls.**
- **`for step in range(max_steps)` is the cap, and this single line is the difference between an agent and an incident.**
- **Inside the loop, `generate_content` is called with the growing history — say that the network call is now inside a loop and therefore happens up to five times.**
- **`if not getattr(part, "function_call", None)` is the exit condition, and the comment says it: no tool requested means it is finished.**
- **`getattr` with a default asks for an attribute and returns `None` instead of crashing if it is missing** — defensive, and not a bug.
- **`print(f"  step {step}: {call.name}({dict(call.args)})")` is the trace**, and this one line is what turns a black box into something you can debug and later explain to an auditor. It is the "A trace" bullet from the guardrails slide, in one line of code.
- **The f-string with two levels of braces is worth naming for the non-coders: the outer braces interpolate, and the literal parentheses around the arguments are there to make the printed line look like a function call.**
- **`fn = TOOLS.get(call.name)` is the allow-list**, and unlike cell 8 it uses `.get()` so an unknown name returns `None` rather than raising.
- **The unknown-tool branch returns a JSON error that *lists the available tools*, which means the model can read it and correct itself.** That is the error-message principle applied to the agent's own plumbing, and almost nobody does it.
- **`print(f"           → {result}")` prints the tool's return alongside the request, so the trace shows both halves of every round trip.**
- **The two appends at the bottom are identical to cell 9, and they have to be, because this is cell 9 in a loop.**
- **`return "Stopped: step limit reached without a final answer."` is what happens when the cap fires, and it is a string rather than an exception so the caller gets a result to inspect.**
- **Count the guardrails on screen with them: the bound, the allow-list, the readable unknown-tool error, and the trace. Four guardrails, six lines.** That is the point of the cell.
- **Hidden dependency worth stating:** `run_agent` reads `CFG` and `TOOLS` from module scope, not from arguments. Cells 13 and 18 both rebuild those. This is the mechanism behind fix list item 8, and it is the single most confusing thing that can happen this afternoon.
- ⚠️ `parts[0]` again — same assumption as cell 7, same caveat.
- **Ask the room:** "Which line makes this an agent rather than the four cells we just ran?" The answer you want is `for step in range(max_steps)` — the loop and the bound, together.

---

## Cell 12 — A two-step task, with the trace

**Purpose:** the payoff. Two tools, chosen in the right order, without being told the order.

- **The goal is Abha's temperature converted to Fahrenheit, and the prompt explicitly says "Use the calculator for the conversion."**
- **That instruction is in the prompt because flash-lite will otherwise do the arithmetic itself and get away with it** — 22°C to Fahrenheit is easy enough that the model may not reach for the tool. Say that you nudged it, because it is honest and it teaches something: prompts can steer tool selection when the description alone does not.
- **The expected trace is `step 0: get_weather({'city': 'Abha'})`, then `step 1: calculate({'expression': '22 * 9 / 5 + 32'})`, then a final answer of 71.6°F.**
- **Check the arithmetic with them: 22 × 9 ÷ 5 + 32 is 71.6, and if the model wrote the expression differently the number should still be 71.6.**
- **The dependency is the lesson: the model could not have written that expression until step 0 came back with 22.** Nothing planned it; the second step exists because the first one returned a number.
- **Read the trace aloud, line by line.** It is the clearest picture of the week that exists, and it is the notebook equivalent of the deck's "Reading the trace" slide.
- **When the demo underwhelms** — if the model skips the calculator and just answers 71.6 directly — do not fight it. Say: "It did the arithmetic itself, and it happened to be right. On 1,247 × 0.83 it would not be, and you would have no way to tell." Then edit the prompt live to a harder number and re-run.
- **What to look for while circulating:** the pairs who ran cell 12 before cell 11 and got a `NameError`. It is the most common ordering mistake in the notebook.

---

## Cell 13 — TODO: write a third tool

**Purpose:** the exercise. It forces them through all three registration steps themselves, which is the only way the two-place update becomes memorable.

- **The comment states the pattern in three numbered steps: write the function, write the declaration, add both to `TOOLS` and the tool config.**
- **The comment also says the pattern is written three times above, which it is — cells 2, 3 and 5.** Point them there rather than answering the question.
- **`convert_currency(amount, to_currency)` has `RATES` hardcoded inside it with usd, eur and gbp against the Saudi riyal.**
- **The rates being hardcoded is itself a teaching point: this is a tool with no live data, which is precisely the limitation from the deck's first content slide, reappearing one level down.** A real one would call an FX API; nothing else about the tool would change.
- **There are two TODOs and both matter: the function body returns "not implemented yet", and the declaration's `description` literally says "TODO: write a description the model can act on."**
- **The description TODO is the better half of the exercise**, because a student who fills in the body and leaves the description will get a tool that is never called, or called for the wrong thing — which is the deck's page 11 lesson delivered by experience rather than by slide.
- **The registration lines below are already written for them: `TOOLS["convert_currency"] = ...`, then a rebuilt `tool_config` with all three declarations, then a rebuilt `CFG`.**
- **Point at those three lines and say that adding a tool is a change in two places, and forgetting the second is why "my tool is never called" is the most common agent bug.**
- **The final line runs `run_agent("How much is 1485 SAR in US dollars?", max_steps=4)`, and with the stub in place the trace will show the tool being called and returning "not implemented yet."**
- **Expected answer once implemented: 1485 × 0.267 is 396.5 US dollars.** Have that number ready so you can confirm a correct implementation at a glance while circulating.
- ⚠️ The comment says "2 lines" and a correct implementation with a good error is closer to five. Do not let a literal-minded student think they have missed something.

**Model answer, for when you are circulating:**

```python
def convert_currency(amount: float, to_currency: str) -> str:
    """Convert an amount in SAR to another currency."""
    RATES = {"usd": 0.267, "eur": 0.245, "gbp": 0.211}
    rate = RATES.get(to_currency.strip().lower())
    if rate is None:
        return json.dumps({"error": f"Unknown currency '{to_currency}'.",
                           "valid_currencies": sorted(RATES)})
    return json.dumps({"amount_sar": amount, "currency": to_currency.lower(),
                       "converted": round(amount * rate, 2)})
```

And a description that actually works:

> "Convert an amount of money from Saudi riyals (SAR) into US dollars, euros or British pounds. Takes the amount in SAR and the target currency code. Only supports usd, eur and gbp, and does not convert in the other direction."

- **The `.strip().lower()` mirrors `get_weather`, and the `rate is None` check rather than `if not rate` is the correct form** — a rate of `0` would be falsy, and while no currency has a zero rate, teaching `is None` here costs nothing.
- **The "does not convert in the other direction" clause is the explicit exclusion from page 11.** If a student writes it unprompted, say so out loud to the room.
- **What to look for while circulating:** students who implement the body perfectly and leave the description as "TODO". Ask them to run it and watch the model's choice, rather than telling them.

---

## Cell 14 — Take the cap off

**Purpose:** show what an unbounded loop costs, by letting them watch it happen.

- **The comment is explicit and correct: `max_steps=40` is not "no cap", it is a cap high enough to be expensive, and you should never run an actually-unbounded loop on a paid key.**
- **The instruction is to interrupt the cell yourself with the stop button.**
- **The goal is "What is the weather in Paris, France? Keep trying until you find it," and the "keep trying" clause is there to defeat the model's natural inclination to give up.**
- ⚠️ **This demo will very probably not spiral, and the reason is cell 3.** `get_weather("Paris")` returns an excellent error listing the three valid cities. A model at temperature 0 reads that, concludes Paris is not available, and stops at step 0 or 1. See fix list item 6 — I think this is the most interesting thing in the notebook and I would not just patch it.
- **If it does not spiral, say this rather than apologising:** *"Look at what just happened. It did not loop, and the reason is the error message we wrote in cell 3 — it told the model what was wrong and what valid inputs look like, so the model had enough information to stop. A good error message is a cost control."* That is a better lesson than the spiral.
- **If it does spiral, count the steps out loud with the room** and then move straight to cell 15's arithmetic.
- ⚠️ **Forty steps, thirty people, one shared free-tier key is a quota problem.** See fix list item 6 for the mitigation.
- **What will go wrong in the next ten minutes:** somebody will not find the stop button, and somebody else will run this cell twice. Show the stop button on the projector before you let them run it.

---

## Cell 15 — Markdown: what that would have cost

- **The key sentence is that the conversation is re-sent on every step, so step twenty is far more expensive than step one, and the cost curve accelerates rather than being flat.**
- **The worked number is ten steps at roughly 4,000 input tokens each, which is 40,000 tokens for a question that had no answer.**
- Make the shape explicit, because it is the bit people miss: the cost of *n* steps is not *n* × the cost of one step, it is closer to the sum 1+2+3+…+n, which grows with the square of the number of steps. Twenty steps is roughly four times the cost of ten, not twice.
- **On a free tier you hit a rate limit and stop, and the markdown says plainly that this is luck, not design.**
- **On a paid key, running overnight, this is the invoice that ends up in a post-mortem.**
- **The cell also names the two stop conditions beyond a step cap: a check for repeated identical calls, and a wall-clock timeout.**
- **Forward to Wednesday:** tomorrow they will measure tokens and cost on their own project. This cell is where that number stops being abstract. Say it, because it makes Wednesday feel earned rather than bolted on.
- **Ask the room:** "What cap would you set on your own project, and why that number?" You want a reason based on how many steps the task actually needs.

---

## Cell 16 — `validated_agent`, output validation

**Purpose:** close the loop back to Day 1. The agent produces free text; a schema forces it into a shape you can check before you act on it.

- **`ANSWER_SCHEMA` is a JSON Schema with two required fields: `answer` as a string and `confident` as a boolean.**
- **`validated_agent` calls `run_agent` with `verbose=False`, so the trace is hidden and only the final answer comes through.**
- **The second `generate_content` call rewrites the raw answer as structured output, using `response_mime_type="application/json"` and `response_schema=ANSWER_SCHEMA`.**
- **The comment names the callback explicitly: this is Day 1's lesson used as a control, and a shape you can check is a shape you can act on.**
- **`json.loads(r.text)` parses it, and `if not data["confident"]` is the gate — an unconfident answer is replaced with an honest admission rather than passed through.**
- **The two test calls are the contrast: Riyadh should give a real answer and Paris should give "I could not answer that reliably."**
- ⚠️ **The Paris case will probably not produce the intended output**, because the rewriting model is being asked to restructure text, not to assess whether the original task succeeded. "I don't have weather data for Paris" is a confident statement of inability. See fix list item 10, with the one-line prompt fix.
- **Say the cost honestly, because Wednesday is coming:** this doubles the API calls per question and adds a full round trip of latency. Validation is not free, and whether it is worth it depends on what happens downstream when the answer is wrong.
- **`json.loads` has no `try`/`except` here.** With `response_mime_type` set it should be safe, but if the model ever returns fenced output this raises. Worth mentioning as a "what would you add in production" question rather than fixing.
- **Ask the room:** "What else would you put in that schema?" Good answers: a citation field, a list of tools used, a numeric confidence rather than a boolean.
- **Callback to Sunday:** on Day 1 structured output was about making the model's answer *usable*. Here it is about making the answer *checkable*. Same mechanism, different job. Name that shift — it is one of the better throughlines in the week.

---

## Cell 17 — Markdown: the ceiling, agentic RAG

- **The claim is that everything they built yesterday becomes one tool that today's agent can choose to call.**
- **Plain retrieval always searches, always once, even when the question needs no documents at all or needs three different searches.**
- **An agent decides whether to search, what to search for, and whether the first result was good enough.**
- **The word "whether" is doing the work in that sentence — emphasise it, because it is the entire difference from Monday.**
- **The last paragraph is an instruction, not commentary: they must copy their `hybrid_search` function and the `records` it closes over from Notebook 2, or re-run Notebook 2's Part A cells here.**
- ⚠️ **This contradicts the deck**, which shows `from day2 import hybrid_search`. The notebook's approach is the workable one. See fix list item 4.
- **Say the "records it closes over" part explicitly and slowly.** Pasting the function alone gives a `NameError` on whatever the corpus variable is called, and that will happen to several people. Tell them to paste the corpus, the embeddings and the function.
- ⚠️ Warn them **not** to re-run Notebook 2's embedding step if it embeds the whole corpus — that burns quota they need for the rest of this cell. Pasting is safer than re-running.
- **This is the payoff moment of the week. Slow down and let it land before you run cell 18.**

---

## Cell 18 — Your Day 2 retriever, as a tool

**Purpose:** demonstrate that wrapping an existing capability as a tool is a wrapper function plus a schema, and that the result is a genuinely more capable system.

- **The comment at the top says to paste `hybrid_search` above this cell first, and that the stub keeps the notebook runnable if they have not.**
- **`try: hits = hybrid_search(query, k=3) / except NameError:` is defensive design and it is well done** — the notebook does not collapse for anyone who has not pasted their Day 2 work, and the error it returns is one the *model* can read. Praise this out loud; it is the notebook practising what it preaches.
- ⚠️ **Only `NameError` is caught.** If their `hybrid_search` exists but takes different arguments or returns a different shape, they get an uncaught `TypeError` or `KeyError` instead. See fix list item 11.
- **`h["text"][:600]` is slicing, and the comment gives the reason: every passage is re-sent on every later step of the loop.** Slicing has appeared before in this course — name the callback.
- **The wrapper returns `text`, `source` and `page` for each hit, and carrying `source` and `page` through is what makes a cited answer possible.** Those fields exist because of a decision made on Monday morning about keeping metadata.
- **The list comprehension is a compact `for` loop** — read it aloud as "for each hit, make a small dictionary with these three fields."
- **`search_decl`'s description says to use it for any question about internal policy, procedure or entitlement**, which is scope written in the vocabulary the users will actually use.
- **`"description": "Search terms, not the raw question"` is query rewriting delegated to the model, expressed as one sentence of documentation.** That is the cleverest line in the notebook; point at it.
- ⚠️ **`tool_config = types.Tool(function_declarations=[calc_decl, search_decl])` silently drops `weather_decl` and `currency_decl`.** `TOOLS` still contains all four functions, so the allow-list and the declared menu now disagree. See fix list item 8 — this one will produce a genuinely baffling afternoon for anyone who scrolls back up.
- **The final call asks for grade 11's annual leave *and* how many days remain after taking 12, and asks for a citation.**
- **The expected trace is `search_documents` first, then `calculate`, then a final answer carrying a source and page** — and that is the deck's "Reading the trace" slide, produced live from their own Monday code.
- **`max_steps=6` rather than 5, because this question genuinely needs more room** — a retrieval that misses on the first query needs a retry, and that retry is the whole argument for agentic RAG.
- **What to look for while circulating:** a retrieval that returns empty. Nine times out of ten it is a language mismatch, not a code bug — see the Arabic note below.

**Arabic/RTL, and this is the cell where it matters:**

- **`h["text"][:600]` counts characters, not tokens.** Arabic runs roughly two to four times more tokens per character than English with most tokenisers, so the truncation that keeps an English loop affordable can be several times more expensive on an Arabic corpus. If their project uses Arabic policy documents, 600 is not a safe default — tell them to measure it rather than inherit it.
- **Slicing mid-string cuts words in half**, and in a mixed Arabic-English passage a cut inside a bidirectional run can make the trailing fragment *render* in a confusing order even though the bytes are fine. The model copes; the human reading the trace does not. Truncate on a word boundary if they are printing traces.
- **The description is in English and their corpus may be in Arabic**, and at temperature 0 the model will sometimes emit English search terms against an Arabic index and retrieve nothing at all. If someone's retrieval mysteriously returns empty, check the language of the emitted query first — it is the fastest diagnosis in the room and it looks like magic when you spot it. The fix is one sentence in the description: *"Search terms must be in the same language as the user's question."*

---

## Cell 19 — Markdown: reflection

- **Three questions, and the cell says explicitly that this is what you check when you come round — so actually check it.**
- **Question one asks what executed their function and what the model actually did**, which is the third and final time the day's central claim gets stated. This one is stated by *them*, which is the point.
- **Question two asks how many steps the agentic RAG question took and whether that was the minimum**, which quietly introduces efficiency as something measurable — and hands Wednesday a running start.
- **Question three asks for one task at their own work where an agent is right and one where a fixed sequence would be better**, and this is the question that connects the day to the deck's "when not to build an agent" slide.
- **Question three is also the best predictor of who has a good project.** Anyone who cannot name a fixed-sequence case has not understood the trade, and this afternoon is your chance to catch it.
- **Do not let them skip this cell because it has no code in it.** Say that you will read it, then read it.

---

## Cell 20 — Markdown: if this breaks

- **A three-row table of symptom, cause and fix, and it is worth reading aloud before the lab rather than after, so they recognise the symptoms when they see them.**
- **Row one: the model asks for the same tool over and over because the tool result was never appended to history — both appends in the loop are required.**
- **Row two: a `TypeError` when calling the tool means the schema type does not match the Python signature, and the mapping is `"number"` for floats, `"integer"` for ints and `"string"` for text.**
- **Row three: the loop never ending is cell 14 on purpose, and the fix is to keep `max_steps` and add a repeated-call stop condition.**
- The table is accurate and the row-one diagnosis is the one they will actually need. Say it before the lab: *"If your agent repeats itself, you dropped an append."*
- **A fourth row worth adding** — see fix list item 8 — is: *"A tool that worked earlier stops being called → you rebuilt `tool_config` in a later cell and dropped it → rebuild `CFG` with every declaration you still want."*

---

# Fix list — before you present

Ordered by how badly it will hurt you.

---

### 1. The notebook has never been run

All fourteen code cells have `execution_count: null` and zero stored outputs. That means either it has not been executed end to end, or the outputs were stripped before you sent it. Either way, nothing below this line has been observed — including by me, since I cannot reach the API from here.

**Do this first, tonight or early tomorrow:** open a fresh Colab runtime, run every cell in order, and keep the outputs. It takes about ten minutes and it is the only thing that will tell you which of items 2, 6, 7 and 10 actually fire.

While you do it, note the three things that determine your morning:

- Does cell 7 print a tool name, or does it crash? (item 7)
- Does cell 14 spiral, or does it stop at step 0? (item 6)
- Does `validated_agent("What is the weather in Paris?")` print the honest refusal, or a confident non-answer? (item 10)

Keeping the outputs in the distributed copy is also a kindness: anyone whose key fails can still read what should have happened.

---

### 2. `gemini-2.5-flash-lite` is doing a job the whole day depends on

**Where:** cell 1.

Flash-lite is the smallest and cheapest model in the family, and every single lesson today rests on it *choosing tools correctly* — a capability that scales with model size more than most. If it declines to call `calculate` in cell 12, skips `search_documents` in cell 18, or misreads a schema, your demos fail in front of the room and the failures look like your material rather than the model.

**Verify before you present:** run cells 1–12 and check that the cell 12 trace shows two tool calls in order. If it shows one, or none, switch:

```python
MODEL = "gemini-2.5-flash"          # tool selection is the whole lesson today
```

I cannot check current model availability, tool-calling support or free-tier quotas for either name from here, so run it rather than trusting either of us. If flash-lite works reliably, keep it — cheaper is better with thirty people on a shared quota — but you need to *know*, not hope.

Also confirm `gemini-embedding-001` in the same run if anyone will re-run Day 2 code inside this notebook.

---

### 3. The deck and the notebook show different `run_agent` functions

**Where:** deck PDF page 13 vs notebook cell 11.

| | Deck | Notebook |
|---|---|---|
| Signature | `run_agent(goal, tools, max_steps=5, verbose=True)` | `run_agent(goal, max_steps=5, verbose=True)` |
| History init | `user_message(goal)` | `types.Content(role="user", parts=[...])` |
| Result append | `tool_result(call.name, result)` | the full `types.Content(...)` expression |

**The notebook is correct on all three counts.** In particular the deck's `tools` parameter is accepted and never used — I flagged it in the slide notes as a silent-wrong-behaviour bug, and the notebook has simply never had it. So the fix is one-directional: **change the deck to match the notebook.**

The `user_message` / `tool_result` helpers on the deck do not exist anywhere in the notebook. If you keep them on the slide for readability, add one line saying "helpers, defined in the notebook" — otherwise a student who searches for `tool_result` finds nothing and concludes the notebook is broken.

---

### 4. The deck says `from day2 import`; the notebook says paste it

**Where:** deck PDF page 20 vs notebook cells 17 and 18.

The deck's `from day2 import hybrid_search` fails on a fresh Colab runtime because no `day2.py` exists. The notebook's approach — paste `hybrid_search` and the records it closes over, with a `NameError` guard so the notebook stays runnable either way — is the one that works.

**Fix the deck to match the notebook.** Change the slide's first two lines to:

```python
# Yesterday's function, pasted in from Notebook 2. Unchanged.
# (hybrid_search and its records live in a cell above this one.)
```

This matters more than it looks: they will be reading the slide on the projector while typing into the notebook, and the slide currently tells them to do the thing that does not work.

---

### 5. `calculate` accepts `**`, and `9**9**9` will hang the kernel

**Where:** cell 2.

The character allow-list `"0123456789+-*/(). "` is good design and blocks every name-based attack — no letters, no underscores, no quotes, no subscripts. But `*` appears twice in `9**9**9`, which passes the filter and asks Python to compute nine to the power of nine to the power of nine. The kernel hangs, memory climbs, and Colab eventually kills the runtime.

I verified the filter accepts it. Cheap to trigger, annoying to recover from, and on Thursday it is the first thing a red-teamer will find.

**Fix — three extra lines, and they teach something:**

```python
def calculate(expression: str) -> str:
    """Evaluate a simple arithmetic expression and return the result."""
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed:
        return json.dumps({"error": "Only arithmetic is allowed: digits and + - * / ( )"})
    if "**" in expression:                       # 9**9**9 hangs the kernel
        return json.dumps({"error": "Exponentiation is not supported. Use + - * / only."})
    if len(expression) > 100:                    # bound the input as well as the charset
        return json.dumps({"error": "Expression too long. Keep it under 100 characters."})
    try:
        return json.dumps({"result": eval(expression)})
    except Exception as e:
        return json.dumps({"error": f"Could not evaluate: {e}"})
```

**Keeping the flaw would make an excellent exercise, and I would genuinely consider it** — but not silently, and not today. It belongs on Thursday: hand them cell 2 as written, ask them to break it without using a single letter, and let someone find `**`. That is a far better red-teaming lesson than an abstract one, and it retroactively makes today's "the model can produce ANY string" comment land hard. Your call; just do not leave it unpatched *and* unmentioned, because a bored developer will find it during the lab and take the runtime down.

Note also that the two new error messages follow cell 3's principle — they say what was wrong and what is valid — so the fix doubles as a worked example of the thing you are teaching.

---

### 6. The spiral demo will probably not spiral, and cell 15 assumes it did

**Where:** cells 3, 14 and 15.

Cell 3's error message is deliberately excellent: it names the failure and lists the three valid cities. Cell 4's markdown praises it for exactly that. So when cell 14 asks for Paris, a model at temperature 0 reads a clear, actionable error and stops — probably at step 0 or 1, regardless of the "keep trying until you find it" instruction.

Cell 15 then says "count the steps you let it run" and does arithmetic on ten steps. If it stopped at one, that markdown is describing something nobody saw.

**This is the most interesting thing in the notebook and I would not just patch it.** The notebook has accidentally demonstrated that a well-written error message *is* a cost control — which is a better lesson than the spiral. My recommendation is to have both.

**Add one tool above cell 14 that returns nothing useful:**

```python
# A deliberately unhelpful tool. Compare its error to get_weather's.
def search_flights(destination: str) -> str:
    """Search for flights to a destination."""
    return json.dumps({"results": []})          # no guidance, no valid inputs, nothing

flights_decl = types.FunctionDeclaration(
    name="search_flights",
    description="Search for available flights to a destination city.",
    parameters={"type": "object",
                "properties": {"destination": {"type": "string",
                                               "description": "Destination city"}},
                "required": ["destination"]})

TOOLS["search_flights"] = search_flights
tool_config = types.Tool(function_declarations=[calc_decl, weather_decl, flights_decl])
CFG = types.GenerateContentConfig(tools=[tool_config], temperature=0.0)

print(run_agent("Find me a flight to Jeddah. Keep trying until you find one.",
                max_steps=12))
```

An empty result with no explanation gives the model nothing to reason about, so it retries with variations — which is exactly the trace on deck page 14, `JED` then `Jeddah` then `JED ` with a trailing space.

**Then run the Paris cell straight afterwards and put the two traces side by side.** One tool loops, the other stops after one call, and the only difference is what the error said. That comparison is worth more than either cell alone, and it makes cell 4's markdown retroactively land.

**Reduce `max_steps=40` to `12` in cell 14 regardless.** Twelve near-identical lines makes the point as well as forty does, it terminates on its own so nobody has to find the stop button, and forty steps of growing history across thirty machines is a real quota risk. Rewrite cell 15's arithmetic to match whatever number you settle on.

**Verify before you present:** find out whether the room shares one API key or has individual keys. With one shared key, the spiral cell needs staggering or a screenshot; with individual keys, it fails locally and harmlessly. This changes your instructions completely.

---

### 7. Cell 7 crashes if the model answers with text

**Where:** cells 7, 9 and 11 all index `parts[0]`.

Cell 7 does `call = part.function_call` and then `call.name` with no guard. If the model returns a text part first — a sentence of preamble, a thinking-style part, or a direct answer — `function_call` is `None` and you get `AttributeError: 'NoneType' object has no attribute 'name'` on the projector.

Cells 9 and 11 already guard with `getattr(..., None)`. Cell 7 is the only unguarded one, and it is the one you run live in front of everyone.

**Fix — four lines that also teach the point:**

```python
part = r1.candidates[0].content.parts[0]
call = getattr(part, "function_call", None)

if call is None:
    print("No tool requested — the model answered directly:")
    print(r1.text)
else:
    print("tool requested :", call.name)
    print("arguments      :", dict(call.args))
    print()
    print("Nothing has executed. No function has run. This is a message.")
```

The `else` branch is not a workaround; answering directly is a legitimate outcome and this makes the notebook say so.

**Separately, `parts[0]` will silently drop a second call** if the model ever requests two tools in one turn. For a workshop this is acceptable — flag it verbally rather than complicating cell 11 — but if you want the robust version:

```python
parts = r.candidates[0].content.parts or []
calls = [p.function_call for p in parts if getattr(p, "function_call", None)]
```

**Verify before you present:** in your end-to-end run, add `print(len(r1.candidates[0].content.parts))` after cell 6. If it prints 1 every time, the current code is fine for today and the multi-part case is a caveat you mention. If it ever prints more than 1, patch cell 11.

---

### 8. Cell 18 silently drops two tools from the menu

**Where:** cell 18, `tool_config = types.Tool(function_declarations=[calc_decl, search_decl])`.

After cell 13, `TOOLS` holds four functions: `calculate`, `get_weather`, `convert_currency` and `search_documents`. But cell 18 rebuilds `tool_config` with only `calc_decl` and `search_decl`, then rebuilds `CFG` from it. The allow-list and the declared menu now disagree.

Nothing errors. But anyone who scrolls back and re-runs cell 12 gets an agent that no longer knows `get_weather` exists — it will apologise, or hallucinate a temperature, or call `calculate` for no reason. The symptom is "the weather thing worked twenty minutes ago and now it doesn't," which is exactly the kind of bug that eats an afternoon.

**Fix — declare everything you still want:**

```python
tool_config = types.Tool(function_declarations=[
    calc_decl, weather_decl, currency_decl, search_decl])
CFG = types.GenerateContentConfig(tools=[tool_config], temperature=0.0)
```

**Better still, make the invariant impossible to break.** Keep declarations and implementations in one place from cell 5 onward:

```python
DECLS = {"calculate": calc_decl, "get_weather": weather_decl}

def rebuild_config():
    """Call this after adding any tool. Keeps TOOLS and DECLS in sync."""
    missing = set(TOOLS) - set(DECLS)
    if missing:
        print(f"WARNING: implemented but not declared, so unreachable: {missing}")
    return types.GenerateContentConfig(
        tools=[types.Tool(function_declarations=list(DECLS.values()))],
        temperature=0.0)

CFG = rebuild_config()
```

Then cells 13 and 18 each add to both dictionaries and call `rebuild_config()`. The warning line turns the most confusing failure in the notebook into a printed message, and the two-place-update lesson survives — they still have to update both, they just find out immediately when they don't.

**Add a fourth row to cell 20's troubleshooting table:** *"A tool that worked earlier stops being called → you rebuilt `tool_config` later and dropped it → rebuild with every declaration you still want."*

---

### 9. Cell 8 uses `TOOLS[...]` where cell 11 uses `TOOLS.get(...)`

**Where:** cell 8 vs cell 11.

`TOOLS[call.name]` raises `KeyError`; `TOOLS.get(call.name)` returns `None` and the loop turns it into a readable error. Both are defensible — the step-by-step cell wants to fail visibly, the loop wants to recover — but a sharp student will ask why the same lookup is written two ways, and "no reason" is not the answer you want.

**Either make them consistent, or make the difference deliberate.** I would add one comment to cell 8:

```python
fn = TOOLS[call.name]     # crashes loudly here on purpose; the loop in cell 11
                          # uses .get() and returns an error the model can read
```

Low severity. But it is a free opportunity to teach that "fail loudly" and "fail recoverably" are different design choices for different contexts, which is a genuinely useful thing for them to carry into their projects.

---

### 10. The output validator probably won't refuse the Paris case

**Where:** cell 16.

`run_agent("What is the weather in Paris?")` returns something like *"I don't have weather data for Paris — I can only provide Riyadh, Jeddah and Abha."* The second model call is then asked to "rewrite this as structured output". A model rewriting that text has no reason to set `confident: false` — the text is a confident, accurate statement of a limitation. So `validated_agent` most likely prints the refusal text with `confident: true`, and the intended contrast between the two test lines never appears.

The validator is checking the model's confidence about *the rewrite*, not about *the task*.

**Fix — put the criterion in the prompt:**

```python
    r = client.models.generate_content(
        model=MODEL,
        contents=(
            "Rewrite the following as structured output. "
            "Set confident=false if the text says it could not find the "
            "information, does not know, or only partially answered. "
            "Set confident=true only if it contains a complete answer.\n\n"
            f"{raw}"),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ANSWER_SCHEMA,
            temperature=0.0,
        ),
    )
```

**Verify before you present:** run both `validated_agent` lines and check that Paris prints "I could not answer that reliably." If it does not even with the fixed prompt, drop the `confident` field to a simple `answered_fully` boolean, which models judge more reliably than self-reported confidence.

**Also verify:** that a plain dict is accepted as `response_schema` in the current SDK. Some versions want a `types.Schema` or a pydantic model. One-line check: run cell 16 and see whether it raises before the API call. I cannot check the current SDK surface from here, so run it rather than trusting either of us.

Worth saying to the room either way: self-reported confidence from a language model is weak evidence. It is better than nothing as a control, and it is not a substitute for the golden set from Monday.

---

### 11. Cell 18 catches only `NameError`

**Where:** cell 18, the `try`/`except` around `hybrid_search`.

The guard is good and it is the right instinct. But it only handles "the function does not exist." If a student's Day 2 `hybrid_search` takes different arguments, or returns tuples, or returns dicts keyed `"content"` rather than `"text"`, they get an uncaught `TypeError` or `KeyError` from inside a tool — which propagates up through `run_agent` and kills the loop, contradicting everything you taught in cell 3.

**Fix — broaden the catch and keep the message readable by the model:**

```python
def search_documents(query: str) -> str:
    """Search the policy documents. Returns passages with their sources."""
    try:
        hits = hybrid_search(query, k=3)
        return json.dumps([{"text": h["text"][:600],
                            "source": h["source"], "page": h["page"]} for h in hits])
    except NameError:
        return json.dumps({"error": "Retriever not loaded. "
                                    "Paste hybrid_search from Notebook 2 first."})
    except Exception as e:
        return json.dumps({"error": f"Retriever failed: {type(e).__name__}: {e}. "
                                    "Check that hybrid_search accepts k= and returns "
                                    "dicts with 'text', 'source' and 'page' keys."})
```

Note that the whole body moved inside the `try`, because the failure can happen in the comprehension as easily as in the call.

**Tell the room the required shape before the lab:** `hybrid_search(query, k=3)` returning a list of dicts with `text`, `source` and `page`. If Monday's notebook returns something else, say so now — it is thirty seconds that saves several people ten minutes each.

---

### 12. Cell 13's "2 lines" is closer to five

**Where:** cell 13's TODO comment.

A correct implementation with the good error message the comment asks for is four or five lines, not two. Trivial, but literal-minded students will assume they have missed a clever one-liner and waste time looking for it. Change the comment to "(a few lines)".

---

# Not bugs — do not "fix" these

- **`role="user"` on the function response** (cells 9, 11). Looks wrong, is the documented pattern for this SDK — the tool result arrives on the user turn because from the model's perspective the environment is what spoke.
- **`response={"result": result}` wrapping an already-JSON string** (cells 9, 11). Technically double-encoded, works fine, and the API requires a structured object rather than a bare value. Leave it.
- **`getattr(part, "function_call", None)` in cells 9 and 11.** `part.function_call` normally exists and is `None` when absent, so the `getattr` is belt-and-braces. Harmless, good defensive style.
- **`eval` in cell 2.** With the character allow-list in place this is a *considered* use, not a careless one — no letters means no names means nothing to reference. Fix item 5 closes the one real hole; the overall approach is sound and the `# noqa` comment shows the author thought about it.
- **`EMBED_MODEL` defined and never used** (cell 1). It is there so pasted Day 2 code finds the name. Not dead code, forward-declared code.
- **`import os, time` unused.** Harmless.
- **`get_weather` returning a JSON string rather than a dict.** Every tool in the notebook returns a string, consistently, and that consistency is what lets `run_agent` handle all of them identically.
- **`RATES` defined inside `convert_currency` rather than at module level** (cell 13). Rebuilt on every call, costs nothing, keeps the exercise self-contained in one cell.
- **`max_steps=6` in cell 18 rather than 5.** Deliberate — that question genuinely needs room for a retry.
- **`temperature=0.0` everywhere.** Set for classroom determinism so the room sees the same trace. Correct choice.
- **The `SystemExit` in cell 1's `except`.** Deliberate: it stops the cell cleanly in Colab instead of printing a long traceback.
- **`verbose=False` inside `validated_agent`** (cell 16). Intentional — the point of that cell is the validated output, not the trace, and they have already seen traces twice.

---

# One thing I added

**A fourth troubleshooting row and a `rebuild_config()` helper** are both in fix item 8. The helper is optional, but it converts the notebook's nastiest silent failure — implemented-but-not-declared tools — into a printed warning, without removing the two-place-update lesson you actually want them to feel. If you only take one structural change from this list, take that one.
