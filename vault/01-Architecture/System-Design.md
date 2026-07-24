---
tags: [architecture]
---

# System Design

```mermaid
flowchart LR
    U[User: symptoms + vitals] --> RE[Rule Engine\n(deterministic, offline)]
    RE -->|Green/Yellow/Red + reason| LLM[LLM Explainer\n(Gemini — narration only)]
    LLM --> UI[React UI: color-coded result]
    U --> CT[Chronic Tracker]
    CT --> TrendCheck[Trend Detector]
    TrendCheck --> DocSummary[Weekly Doctor Summary]
    UI --> LocalDB[(IndexedDB / SQLite\nlocal-first storage)]
    LocalDB -.optional, consent-based.-> CloudSync[(Encrypted Cloud Sync)]
```

## Key decision: separation of concerns
| Layer | Responsibility | Can it be wrong? |
|---|---|---|
| Rule Engine | Decide triage level | No — tested, deterministic |
| LLM | Explain in plain language | Yes, but bounded — wording only |
| Frontend | Present clearly, never bury red flags | N/A |

## Data flow / privacy
Patient phone → encrypted local DB → optional opt-in cloud sync → consent-based doctor sharing (QR code). Core functionality works fully offline.

## Stack
- Frontend: React + Tailwind (Vite)
- Backend: FastAPI (Python)
- AI: Gemini API (swap-able for any LLM — architecture doesn't care)
- Storage: SQLite (backend) / IndexedDB (offline client cache)
