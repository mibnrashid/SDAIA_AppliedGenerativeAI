# Teaching checklist

For me, not for students. One section per morning, plus how the day runs.

**Announce 9:00. Start 9:15.** Those fifteen minutes are the API-key and
laptop-problem buffer. Never announce the real start time.

---

## Every morning, before anyone arrives

**On the projector**

- [ ] Deck open at `slides/dayN.html`, **fullscreen (F)**, on slide 1
- [ ] Press **P** once to check the notes panel renders, then press it again
- [ ] Resolution check: the slide scales to fit — if it is clipped, the venue
      is running something unusual, so reload and re-check
- [ ] Browser zoom at 100% (Ctrl+0). Zoom breaks the canvas fit calculation

**Tabs to have open, in this order**

1. The day's deck
2. `notebooks/index.html` — the Colab links
3. Today's notebook, already open in Colab, **already run once**
4. Today's activity
5. `project/index.html` — the rubric, for when someone asks
6. aistudio.google.com — for the student whose key does not work

**On me**

- [ ] Two or three spare API keys in my pocket for people who cannot make an
      account
- [ ] Day 1 deck printed to PDF and on the iPad — this is the fallback if the
      venue wifi dies entirely
- [ ] Phone hotspot tested, in case the projector laptop loses the network

**Sanity check the site**

```bash
python qa.py
```

---

## Sunday · Day 1 — From token to typed output

**Extra, today only**

- [ ] Screenshots of every step of API-key creation, ready to show. Key setup
      failing live is the highest-probability disaster of the week
- [ ] Cards and pens for the icebreaker
- [ ] A small prize for the icebreaker winner
- [ ] Flipchart and marker — for the "what I want AI to do for me by Thursday"
      round, which becomes the project idea pool
- [ ] `assessment/pretest.html` open and tested

**How the day runs**

| Time | Block | What happens |
|---|---|---|
| 9:15–10:05 | 1 | Two Truths and a Lie (20 min, heats then a final, I go last out of competition) · pre-test (15 min) · course map, site tour, project reveal and rubric |
| 10:20–11:00 | 2 | How the thing works: tokens, the live tokenizer widget on slide 7, context window, next-token prediction, temperature, hallucination, the four ways slide · **Activity 1 · Tokenizer Race** |
| 11:20–12:00 | 3 | API key creation walked on screen · **Notebook 1, cells 1–8**. Start before lunch so lunch absorbs the stragglers. Circulate. Do not sit down |
| 1:00–1:50 | 4 | System vs user role (seed Day 5) · prompt anatomy · few-shot · **Notebook 1, cells 9–14** |
| 2:00–2:30 | 5 | **The ceiling:** JSON mode, schema, parse and branch · **Notebook 1, cells 15–20** · summary · homework |

**Say out loud**

- "This pre-test measures me, not you. Zero is a fine score right now."
- Everyone creates **their own** key. One shared key means one student's loop
  throttles the whole room.
- Free tier: no real SDAIA data, no personal data, no client data. Callback to
  this on Thursday.
- Homework: a GitHub account, and pick a document set they care about.

**Watch for** — the key not being in Colab Secrets. Show the key panel on
screen before they start, not after twenty people are stuck.

---

## Monday · Day 2 — Retrieval you can measure

The longest day, and the highest ceiling. Pace it.

**Extra**

- [ ] Notebook 2 run end to end this morning, including the vision cell — that
      cell is the high point of the day and must not fail live
- [ ] `activities/chunk-lab.html` open
- [ ] Yesterday's flipchart on the wall for the afternoon team formation

**How the day runs**

| Time | Block | What happens |
|---|---|---|
| 9:15–10:05 | 1 | Three recall questions to the room (slide 3 — ask three people who did not speak yesterday) · RAG vs agents · the decision rule |
| 10:20–11:00 | 2 | The pipeline: ingestion, **multimodal ingestion**, chunking, embeddings, retrieval |
| 11:20–12:00 | 3 | **Activity 2 · Chunk Lab** (20 min) then **Notebook 2, cells 1–12** |
| 1:00–1:50 | 4 | Where vector search fails · hybrid · re-ranking · query rewriting · **Notebook 2, cells 13–20** |
| 2:00–2:30 | 5 | Golden set · **cells 21–25** · the comparison table · **team formation and idea pitching** |

**Say out loud**

- "Everyone builds RAG. Almost nobody measures it." Then make them measure it.
- 500 tokens with 10% overlap is a **starting point**, not a law.
- Screenshot your comparison table — it goes in Thursday's presentation.

**Watch for** — 429s when the whole room embeds at once (the batching and sleep
are already in the notebook; do not let anyone delete them), and re-running the
Chroma cell duplicating the collection.

---

## Tuesday · Day 3 — Tools and agents

Teaching stops at noon. The afternoon is project time.

**Extra**

- [ ] `activities/be-the-agent.html` open
- [ ] Notebook 3 run, **including the runaway cell** so I know how long it takes
      to spiral before I interrupt it
- [ ] The gate written on the whiteboard: *by 2:30 — documents loaded, chunked,
      embedded, one query returning something*

**How the day runs**

| Time | Block | What happens |
|---|---|---|
| 9:15–10:05 | 1 | Why tools · **"the model does not run your code"** (full-bleed slide, say it three times today) · the 5-step loop · schemas · **Activity 3 · Be the Agent** |
| 10:20–11:00 | 2 | Patterns, guardrails, error recovery |
| 11:20–12:00 | 3 | **Notebook 3** — the manual round trip in four cells, `run_agent`, the spiral, then **agentic RAG** |
| 1:00–2:25 | 4+5 | **Project time.** I circulate. I do not present. Checkpoint every pair twice |
| 2:25–2:30 | — | Stand-up: one sentence per pair. Public accountability, and it tells me who to rescue tomorrow |

**Say out loud**

- Yesterday's retriever becomes today's tool. That is the week joining up.
- Anyone stuck at 2:00 gets me sitting next to them.

---

## Wednesday · Day 4 — Production and the numbers

**Extra**

- [ ] The live cost calculator on deck slide 10 — type real numbers into it in
      front of them; change top-k and the cache rate and let them watch the
      monthly figure move
- [ ] Current pricing page open, so the notebook TODO can be filled in with
      real figures
- [ ] `activities/cost-auction.html` open
- [ ] The six SDAIA repository requirements ready to put on screen at 2:00

**How the day runs**

| Time | Block | What happens |
|---|---|---|
| 9:15–10:05 | 1 | Prototype vs production · scalability · **connect rate limiting back to Monday's 429s** · the cost slide, live · **Activity 4 · Cost Auction** |
| 10:20–11:00 | 2 | Reliability, observability, deployment architecture, UX for AI |
| 11:20–12:00 | 3 | **Notebook 4**, applied to their own project. They finish with their own numbers table |
| 1:00–2:00 | 4 | Build. I circulate |
| 2:00–2:20 | 5 | **README clinic.** Requirements on screen, every pair writes their README now, with me checking. Non-negotiable — READMEs written the night before are always bad |
| 2:20–2:30 | — | Thursday briefing: four minutes, what to demo, and that an honestly-explained broken demo scores better than a fake working one |

**Say out loud**

- "What does this cost per user per month?" Engineers who can answer that get
  hired.
- Arabic costs more. The same assistant, two and a half times the bill.

---

## Thursday · Day 5 — Break it, then defend it

**Extra, and time-critical**

- [ ] `assessment/posttest.html` open **before 9:15** — it runs first
- [ ] Course evaluation link ready to send at 9:30, at the *start* of the day.
      Attendance decays; a link sent at 2:30 gets half the responses
- [ ] `activities/red-team.html` open
- [ ] Notebook 5 run, including the poisoned-document cell
- [ ] Printed rubric sheets, one per pair, for live scoring
- [ ] Two small prizes: best attacker, most resilient system
- [ ] Camera or phone ready for the group photo

**How the day runs**

| Time | Block | What happens |
|---|---|---|
| 9:15–9:30 | 1 | **Post-test.** Both scores go on the SDAIA sheet — the "copy my result" button does it in one tap |
| 9:30–9:35 | — | Course evaluation link |
| 9:35–10:05 | — | Prompt injection: direct, then **indirect**, demoed against a planted document |
| 10:20–11:05 | 2 | Layered defences · **"this is not solved"** · privacy callback to Day 1 · governance · responsible AI · pre-launch checklist · **Activity 5 · Red Team** (25 min), then 10 minutes of fixes |
| 11:20–12:00 | 3 | Presentations begin. 4 minutes + 2 for questions. Score live, on paper |
| 1:00–1:50 | 4 | Presentations continue |
| 2:00–2:30 | 5 | Journey summary · where to go next · **confirm every repo is pushed, public, and links github.com/SDAIAAcademy** · group photo |

**If more than 14 pairs** — switch to a gallery walk: laptops open, 40 minutes
of circulation with scoring sheets, then five teams present to the room.

**Say out loud**

- "Nobody attacked the system. The attack was in the data."
- This is not solved. No patch exists. You reduce risk in layers.
- An honestly-explained broken demo scores better than a fake working one. It
  is in the rubric, and I mean it.

**Before anyone leaves** — every repository pushed, public, and linked. That is
the one thing that cannot be fixed afterwards.

---

## Fallbacks

| If this dies | Do this |
|---|---|
| Venue wifi | Every page on this site already works offline. Serve it from my laptop: `python3 -m http.server 8000`, and give the room the local IP |
| The projector | Students open the site on their own laptops — it is the same content, and the decks are keyboard-driven |
| Everything | The Day 1 deck is printed to PDF on the iPad. Teach from that |
| A student's API key | Hand out one of the spare keys from my pocket, quietly |
| A student's Colab | `notebooks/index.html` offers a direct `.ipynb` download; they can run it locally or pair with a neighbour |
