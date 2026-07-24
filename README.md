# SahaySetu — AI Health Companion

**AI-Powered Symptom Triage & Chronic Disease Self-Management for Rural India**
Built for TetraTHON 2026 — 36-Hour Indo-French AI Hackathon

> Early Guidance. Better Decisions. Healthier Lives.

## What this is

A safety-first health companion that:
1. Takes a patient's symptoms + vitals and runs them through a **deterministic clinical rule engine** first (never an LLM alone) to catch red-flag emergencies.
2. Uses an **LLM (Gemini)** only to *explain* the rule engine's output in plain language — it never overrides a red-flag decision and never diagnoses.
3. Tracks chronic-disease metrics (e.g. blood sugar) over time and flags unhealthy trends.
4. Generates a **weekly doctor summary** so clinicians get clean, structured data instead of a patient's raw recollection.

This mirrors the pitch deck (`/vault/00-Hackathon/Pitch.md`) — the rule engine is the safety backbone, the LLM is the "translator," never the decision-maker.

## Repo structure

```
ai-health-companion/
├── backend/                # FastAPI service
│   ├── main.py              # API routes
│   ├── rule_engine.py       # Deterministic triage logic (Green/Yellow/Red)
│   ├── models.py            # Pydantic schemas
│   ├── llm_explainer.py     # Gemini call — explanation only, no diagnosis
│   └── requirements.txt
├── frontend/                 # React + Tailwind
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   │       ├── SymptomChecker.jsx
│   │       ├── TriageResult.jsx
│   │       └── ChronicTracker.jsx
│   └── package.json
├── vault/                    # Obsidian vault — team's second brain for this hackathon
│   ├── 00-Hackathon/         # Problem statement, judging rubric, pitch, timeline
│   ├── 01-Architecture/      # System design notes, diagrams (link to draw.io / mermaid)
│   ├── 02-Prompts/           # Master prompts for Antigravity + Gemini/Claude
│   ├── 03-Demo-Script/       # Word-for-word demo script + backup plan
│   └── 04-Daily-Log/         # Hour-by-hour hackathon log (great for judges + retros)
├── docs/                     # Architecture diagram exports, screenshots for README
└── README.md
```

## Quickstart

```bash
# backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# frontend
cd frontend
npm install
npm run dev
```

Set `GEMINI_API_KEY` as an env var before starting the backend (optional — the rule engine works standalone without it).

## Safety principles (say this out loud to judges)

- **Rule engine decides, LLM explains.** The red/yellow/green call is 100% deterministic and testable — no hallucination risk on the part that matters most.
- **AI assists, never diagnoses.** Every screen says so.
- **Fail safe, not silent.** Any parsing/LLM failure defaults to the more cautious triage level, never a lower one.
