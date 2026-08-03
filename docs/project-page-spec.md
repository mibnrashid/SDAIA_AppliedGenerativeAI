# Spec — rebuild `project/index.html`

**Applied Generative AI · SDAIA Academy · August 2026**

This replaces the current project page entirely. Follow it exactly. Where it
says "verbatim", use the text as written — it has been worded deliberately.

---

## 0. Constraints (unchanged from the rest of the site)

- Plain HTML/CSS/vanilla JS. No build step, no framework.
- **No CDN or network assets.** Venue wifi is unreliable.
- **Relative paths only** — this serves from `/repo-name/` on GitHub Pages.
- Reuse the existing chrome: `assets/theme.css`, `assets/site.css`, the
header with `sdaia-academy.svg` top-left and `sdaia.svg` top-right, and
the standard footer.
- Any Arabic wrapped in `<span lang="ar" dir="rtl">`.
- `localStorage` keys prefixed `agai:`.



## 1. Remove first

The scaffold notebook is being dropped. Students now build a **repository**,
not a notebook.

1. Dont delete `notebooks/project_scaffold.ipynb` but delete its entry in
  `notebooks/notebooks.json` and `notebooks/index.html`. The five day
   notebooks stay.
2. Remove the `build_project_scaffold` function from `notebooks/build.py`.
3. Delete the "Start from the scaffold" section from the project page.
4. Search the whole site for `project_scaffold` and `scaffold` and remove
  every remaining reference. Report what you found.
5. create a new part called additional resources under the project and activities  
tabs and add the notebook in that page. that additional resources i will be uploading  
in it different things such as slides or links etc so make the format of the page suitable.



## 2. Page structure

Six sections in this order. Each is a full-width band alternating
`--paper` and `--card` backgrounds, with the content in the standard
container.

---



### Section 1 — Hero

Same as home page

- Eyebrow, teal small-caps: `SDAIA ACADEMY · THE PROJECT`
- Headline (serif display): **Ship something that runs.**
- Paragraph, verbatim:
  > Build an assistant that answers from documents you choose, calls tools
  > when retrieval isn't enough, and proves it works with numbers. Then ship
  > it as a repository a stranger can clone and run.
- A row of four small stat chips:
`Teams of 2–3` · `70% of your grade` · `Due Thursday 2:30` · `Python`

---



### Section 2 — How it is graded (put this high, not at the bottom)

A short intro line, verbatim:

> Published on day one. 100 points total — 70 from the project, 30 from
> Thursday's theory exam. The team shares one build mark.

Then **three cards in a row** showing the top-level split:


| Card         | Value  | Caption                         |
| ------------ | ------ | ------------------------------- |
| Build        | **60** | The repository and what it does |
| Presentation | **10** | Four minutes on Thursday        |
| Theory exam  | **30** | Written, Thursday morning       |


Below the cards, one line in muted text, verbatim:

> Optional deployment is worth up to **+5 bonus**, capped at 100. Pass mark
> is 60 overall.

The detailed rubric table goes in Section 6 — this is the summary only.

---



### Section 3 — What must be in it

Intro line, verbatim:

> Six requirements. All six are graded. "Working" means it runs on a laptop
> from a fresh clone — no deployment needed.

Six numbered cards in a 2-column grid (single column on mobile). Each card:
a large number, a bold title, a body paragraph, and a small muted
`Where it comes from` line naming the lab.

**1 · Your own documents**

> Ten to thirty pages you actually care about — a policy, a manual, a
> handbook, a set of regulations. Not a tutorial dataset. Nothing
> confidential: we are on a free tier and Google may use free-tier inputs to
> improve their models.
> *Where it comes from — you.*

**2 · A retrieval pipeline**

> Ingest, chunk, embed, store, and retrieve. Hybrid search — keyword and
> vector combined — because pure vector search misses exact identifiers,
> acronyms and names.
> *Where it comes from — Lab 2, cells 3–19.*

**3 · Grounded answers with citations**

> Every fact traceable to a source and a page. And when the documents do not
> contain the answer, the assistant says so instead of inventing one. An
> assistant that always answers is worse than one that sometimes declines.
> *Where it comes from — Lab 2, cell 11.*

**4 · At least one tool**

> A plain Python function is fine — no MCP, no external service required.
> The rule is that it must do something **retrieval cannot**: compute
> something, look something up in structured data, filter, or check a live
> value. A tool that just searches your documents again is not a tool.
> *Where it comes from — Lab 3, cells 2–5.*

**5 · An agent loop**

> The model decides when to retrieve and when to call a tool, rather than
> you hard-coding the order. Keep the step cap. Print the trace so you can
> show it on Thursday.
> *Where it comes from — Lab 3, cell 8.*

**6 · Evidence that it works**

> A golden set of at least five questions you know the answers to, a measured hit rate.  
> *Where it comes from — Lab 2, cells 21–24.*

---



### Section 4 — Pick a project

Intro, verbatim:

> Bring your own, or take one of these. Whatever you choose has to pass two
> tests: **nobody has a clean dataset for it**, and **the tool does
> something retrieval cannot**.

A table with three columns — `Domain` · `Your documents` · `A tool that earns its place`. Rows:


| Domain                            | Your documents                                 | A tool that earns its place                                |
| --------------------------------- | ---------------------------------------------- | ---------------------------------------------------------- |
| Employee handbook assistant       | HR policy, leave rules, conduct code           | Calculate remaining leave from a start date and days taken |
| Government service guide          | Ministry service manuals, eligibility rules    | Check a fee table and compute the total for a given case   |
| University regulations advisor    | Academic regulations, credit rules             | Compute GPA impact, or credits remaining to graduate       |
| Technical documentation assistant | A library's docs, changelogs, migration guides | Check version compatibility between two package versions   |
| Maintenance manual assistant      | Equipment manuals, service schedules           | Look up a part number in a parts table and report stock    |
| Insurance policy explainer        | Policy wordings, exclusions, schedules         | Compute what is covered for a stated claim amount          |


Below the table, a bordered callout, verbatim:

> **Bringing your own?** Say it out loud on Monday and I will tell you
> whether it passes the two tests before you spend a day on it.

---



### Section 5 — How to build it

Two parts.

#### 5a — The repository blueprint

Intro, verbatim:

> There is no scaffold notebook this year. You are building a repository,
> because that is what goes in a portfolio — nobody hires anyone off a Colab
> link. The logic is code you have already run in the labs. The work is
> moving it out of notebooks and making it run on a laptop.

Then a file tree in a `<pre>` block, styled, with a copy button:

```
your-project/
├── README.md            how to run it — a stranger must succeed
├── requirements.txt     pin your versions
├── .env.example         GEMINI_API_KEY=your_key_here
├── .gitignore           must contain .env and data/ if private
├── data/                your documents
├── ingest.py            load → chunk → embed → save the index
├── retrieve.py          hybrid search
├── tools.py             your tool functions
├── assistant.py         the agent loop
├── evaluate.py          golden set → hit rate
└── app.py               how a person actually talks to it
```

Beside or beneath it, a mapping table — `File` · `What it does` ·
`Start from`:


| File           | What it does                                                        | Start from           |
| -------------- | ------------------------------------------------------------------- | -------------------- |
| `ingest.py`    | Loads your documents, chunks them, embeds, writes the index to disk | Lab 2, cells 3–9     |
| `retrieve.py`  | Hybrid search over the stored index                                 | Lab 2, cells 15–19   |
| `tools.py`     | Your tool functions and their schemas                               | Lab 3, cells 2–5     |
| `assistant.py` | The agent loop with a step cap and the tool allow-list              | Lab 3, cell 8        |
| `evaluate.py`  | Runs the golden set, prints the hit rate                            | Lab 2, cells 21–24   |
| `app.py`       | A command-line loop, or Streamlit if you want a UI                  | New — about 20 lines |


Then a callout headed **The one new thing**, verbatim:

> Outside Colab there is no Secrets panel. Your key goes in a `.env` file
> that is **never committed**, and `python-dotenv` loads it:
>
> ```python
> from dotenv import load_dotenv
> import os
> load_dotenv()
> API_KEY = os.getenv("GEMINI_API_KEY")
> ```
>
> Commit `.env.example` with the variable name and no value. Put `.env` in
> `.gitignore` on your first commit, not your last. A leaked key in git
> history is the most common way a portfolio repository embarrasses its
> author.



#### 5b — The timeline

Four cards in a row, one per day, with the day name as a coloured header.

**Monday** — *Pitch*

> Form your team of 2–3. Choose your documents and check them against the
> two tests. State your idea in one sentence to the room.

**Tuesday** — *Get it retrieving* · 1 hour in class, then at home

> Repository created, `.gitignore` and `.env` in place from the first
> commit. `ingest.py` and `retrieve.py` working. **Gate by Tuesday night:**
> a real question returns relevant chunks from your own documents.

**Wednesday** — *Tools, agent, evidence* · 2 hours in class, then at home

> `tools.py` and `assistant.py` working. Write the golden set and run
> `evaluate.py`. Make one change and record the numbers before and after.
> README clinic runs 2:00–2:20 in class — you write it in the room, with me
> checking.

**Thursday** — *Present*

> Four minutes plus questions, scored live. Repository pushed and public by
> 2:30.

---



### Section 6 — The rubric in full

Intro, verbatim:

> One shared mark for the team on the sixty build points. Marked from your
> repository and your Thursday demo.

**Table 1 — Build, 60 points.** Columns: `Criterion` · `Points` ·
`What full marks looks like`.


| Criterion               | Points | What full marks looks like                                                                                                                           |
| ----------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Prompt Engineering      | 10     | Good Prompts and Day 1 Good Use.                                                                                |
| Retrieval and grounding | 25     | Your own documents, hybrid retrieval, answers with source and page, and an honest "I don't know" when the documents do not cover it.                 |
| Agent and tools         | 25     | At least one tool that does what retrieval cannot, wired into a loop with a step cap, where the model chooses the path and the trace shows it.       |



**Table 2 — Presentation, 10 points.** Four minutes plus questions.


| Criterion                                                         | Points |                                                                              |
| ----------------------------------------------------------------- | ------ | ---------------------------------------------------------------------------- |
| The problem and why it needed this                                | 3      |                                                                              |
| Architecture, and **why** — in one sentence tied to your use case | 4      | Wrong-but-justified beats right-but-unexplained.                             |
| A live demo                                                       | 3      | A demo that breaks and is explained honestly scores higher than a recording. |

**Table 3 — Theory exam, 30 points.** Thursday morning, written, covering
all five days.

Then a bonus callout, verbatim:

> **Optional: deploy it. +5 bonus, capped at 100.**
>
> Not required, and it earns nothing if the basics are missing — do it only
> once the six requirements are met.
>
> - **Streamlit Community Cloud** — wrap `app.py` in Streamlit calls, push,
> connect the repository. About thirty minutes. Free, and it persists.
> - **HuggingFace Spaces** — Gradio or Streamlit, same shape, and the link
> looks good in a portfolio.
>
> A note on Vercel: it runs Python as serverless functions, which means no
> persistent filesystem, so your Chroma index will not survive between
> requests. Making it work means moving to an external vector store such as
> Supabase pgvector. That is a genuine project in itself, not a deploy step
> — worth doing after the course, not during it.

---



### Section 7 — SDAIA repository requirements

Keep the existing six-item checklist and the copy button. Intro line,
verbatim:

> These six are SDAIA's requirements for every project repository. They
> overlap with the engineering quality marks above — meeting them is the
> cheapest eight points on the rubric.

- A clear, comprehensive project description
- A professional `README.md`: the idea, how to run it, how to use it
- Appropriate technical documentation
- Git version-control best practice — real, meaningful commits, not one dump
at the end
- The training programme named: **Applied Generative AI, SDAIA Academy,
August 2026**
- A link to [https://github.com/SDAIAAcademy](https://github.com/SDAIAAcademy)

---



### Section 8 — README template

Keep this section, with the copy-to-clipboard button. Replace the template
body with the version below — the old one referenced the scaffold notebook.

```markdown
# TODO: Project name

TODO: One sentence — what this does and who it is for.

## Team Members
Full Names.

## The problem

TODO: Two or three sentences. What was hard before this existed?

## Architecture

TODO: One sentence on why this shape, tied to your use case.

```
documents → chunk → embed → index
                              ↓
question → agent ─→ retrieve ─┘
              └──→ tool
                    ↓
          answer with citations
```

TODO: Adjust the diagram to what you actually built.

## Running it

```bash
git clone TODO
cd TODO
pip install -r requirements.txt
cp .env.example .env        # then add your key from aistudio.google.com
python ingest.py            # builds the index — run once
python app.py
```

## Using it

TODO: Three example questions and the answers you get back.
TODO: One question it correctly refuses to answer.

## The tool

TODO: What it does, and why retrieval could not do it.

## Does it work?

Golden set: TODO/5 questions retrieved correctly.

TODO: One change you made, with the numbers.
Example: "Chunk size 800 → 500 tokens took the hit rate from 3/5 to 5/5."

## What does not work

TODO: Be specific. What breaks, what you tried, what is still broken.

## Technical notes

- Model: `gemini-2.5-flash-lite`
- Embeddings: `gemini-embedding-001`
- Vector store: Chroma
- Retrieval: hybrid BM25 + vector, alpha = TODO
- Chunking: TODO tokens, TODO overlap
- Guardrails: TODO

## Training programme

Built during **Applied Generative AI**, SDAIA Academy, Riyadh,
2–6 August 2026.

More SDAIA Academy projects: https://github.com/SDAIAAcademy

## Team

TODO: names
```

---



## 3. Interactive behaviour

Keep it light — this is a reference page, not an activity.

1. **Copy buttons** on the file tree, the SDAIA checklist, and the README
  template. Show a "Copied" state for 2 seconds.
2. **A requirement tracker.** Each of the six cards in Section 3 gets a
  checkbox. State persists in `localStorage` under `agai:project:reqs`. A
   sticky bar at the bottom of that section reads `3 of 6 requirements  ticked` with a reset link. This is for the students' own tracking — make
   clear in small muted text that it is local to their browser and not
   submitted anywhere.
3. **A print button** in the header that prints the rubric sections cleanly
  — students will want the rubric on paper.



## 4. When you are done

Report:

- Every file you changed or deleted
- Every `project_scaffold` reference you removed and where it was
- Confirmation that no absolute paths or network assets were introduced
- What I should click to verify each section

