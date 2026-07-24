---
tags: [prompts, antigravity, github]
---

# Master Prompts

Copy-paste these into **Antigravity** (or whichever agentic coding tool you're
driving). Run them in order. Each is self-contained — paste the whole block.

---

## Prompt 1 — Repo + file structure scaffold

```
You are setting up a new hackathon project called "SahaySetu — AI Health
Companion" for TetraTHON 2026 (Indo-French AI hackathon).

Create a new local git repository named `ai-health-companion` with this
exact folder structure, and initialize git with an initial commit:

ai-health-companion/
├── README.md
├── .gitignore
├── backend/
│   ├── main.py
│   ├── rule_engine.py
│   ├── models.py
│   ├── llm_explainer.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── src/
│       ├── main.jsx
│       ├── index.css
│       ├── App.jsx
│       └── components/
│           ├── SymptomChecker.jsx
│           ├── TriageResult.jsx
│           └── ChronicTracker.jsx
├── vault/                      # Obsidian vault — open this folder directly in Obsidian
│   ├── 00-Hackathon/
│   ├── 01-Architecture/
│   ├── 02-Prompts/
│   ├── 03-Demo-Script/
│   └── 04-Daily-Log/
└── docs/

Do not overwrite any file that already has content — only create what's
missing. Once the structure exists, run `git add . && git commit -m "chore: scaffold project structure"`.
```

---

## Prompt 2 — Create the GitHub repo and push

```
Create a new GitHub repository using the GitHub CLI (`gh repo create`) with:

- Name: sahaysetu-ai-health-companion
- Description: "AI-powered symptom triage & chronic disease self-management for rural India — built for TetraTHON 2026. Rule engine decides, LLM explains, never the other way around."
- Visibility: public
- Do NOT initialize with a README (we already have one locally)

After creating it, add it as the `origin` remote for the local repo, set the
default branch to `main`, and push. Then add these topics to the repo via
`gh repo edit --add-topic`: healthtech, ai, hackathon, fastapi, react,
triage, gemini, rural-healthcare.
```

---

## Prompt 3 — Build the rule engine + API (if not already scaffolded from files provided)

```
Implement `backend/rule_engine.py` as a fully deterministic, offline,
zero-dependency clinical triage engine with three levels: GREEN (home care),
YELLOW (consult doctor within 48 hours), RED (visit hospital immediately).

Requirements:
- Red-flag symptom keyword list (chest pain, difficulty breathing, loss of
  consciousness, uncontrolled bleeding, severe abdominal pain, etc.) → instant RED
- Vital sign thresholds (heart rate, SpO2, temperature, systolic BP) that can
  independently trigger RED or YELLOW
- Symptom duration >= 3 days nudges toward YELLOW even without hard flags
- Fail-safe default: if anything is ambiguous or a check errors, default to
  the MORE cautious level, never less
- Write pytest unit tests covering at least one clear case per level plus
  edge cases (missing vitals, empty symptom list, borderline thresholds)

Then implement `backend/main.py` as a FastAPI app exposing:
- POST /api/triage — takes symptoms, vitals, duration_days, language;
  calls the rule engine, then calls an LLM explainer layer that can ONLY
  narrate the result in plain language, never change the triage level
- POST /api/chronic/log — logs a chronic-disease metric reading and returns
  whether the last 3 readings show an unhealthy trend
- GET /health — basic health check

The LLM explainer (backend/llm_explainer.py) must have a deterministic
template fallback so the API still works with zero network access if the
Gemini API key is missing or the call fails.
```

---

## Prompt 4 — Build the React frontend

```
Build a React + Tailwind (Vite) frontend with two tabs: "Symptom Checker"
and "Chronic Tracker".

Symptom Checker: a chip-style multi-select of common symptoms, a duration
input, and a submit button that POSTs to /api/triage and renders a
color-coded result card (green/yellow/red background matching the returned
triage level) showing the plain-language explanation, confidence, red
flags, and recommended next step.

Chronic Tracker: a simple numeric input to log a blood sugar reading,
POSTs to /api/chronic/log, and shows a message about whether there's an
unhealthy trend.

Keep the design clean, mobile-first, and add a persistent disclaimer
footer: "This app assists — it never diagnoses. In an emergency, call your
local emergency number immediately."
```

---

## Prompt 5 — Obsidian vault population (daily use during the hackathon)

```
Inside vault/04-Daily-Log/, create a new markdown file for today's date
(YYYY-MM-DD.md) with sections: "Goals for today", "What shipped",
"Blockers", "Decisions made", "Tomorrow's first task". Link it from a
running index note called vault/04-Daily-Log/Index.md. Use this same
template every time I ask you to "log today" during the hackathon.
```

---

## Prompt 6 — Demo script + judge Q&A prep

```
Using vault/00-Hackathon/Pitch.md and vault/00-Hackathon/Judging-Criteria.md
as source material, write a 3-minute spoken pitch script and a 2-minute
live-demo script (click-by-click) into vault/03-Demo-Script/Demo-Script.md.
Include a "if the live demo breaks" backup plan referencing a pre-recorded
video, and a Q&A prep section with 5 likely judge questions and crisp
answers.
```

---

## How to chain these in Antigravity
Run Prompt 1 → Prompt 3 → Prompt 4 → Prompt 2 (so you commit working code
before creating/pushing the GitHub repo) → Prompt 5 daily → Prompt 6 near
the end. Antigravity can execute shell + git + gh commands directly, so it
can run this whole sequence with minimal supervision — just review diffs
before each commit.
