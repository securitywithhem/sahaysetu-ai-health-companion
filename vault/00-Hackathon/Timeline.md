---
tags: [hackathon, planning]
---

# 36-Hour Timeline

## Hours 0–4: Foundation
- [ ] Repo + Obsidian vault scaffolded (this structure)
- [ ] Rule engine logic finalized on paper (symptom list, thresholds) — do this with pen/whiteboard first, THEN code
- [ ] Figma/paper sketch of 3 core screens: Symptom Checker, Triage Result, Chronic Tracker

## Hours 4–14: Core build
- [ ] `rule_engine.py` implemented + unit tests for green/yellow/red cases
- [ ] FastAPI endpoints wired up
- [ ] React frontend: symptom picker → API call → result card
- [ ] Basic chronic tracker (log + trend flag)

## Hours 14–20: AI layer
- [ ] Gemini integration for plain-language explanation
- [ ] Fallback templates when API unavailable (offline story)
- [ ] Multilingual toggle (even just English/Hindi) if time allows

## Hours 20–26: Polish
- [ ] Color-coded UI, mobile-responsive check
- [ ] Emergency medical card / QR doctor report (stretch goal)
- [ ] Seed demo data for chronic tracker chart

## Hours 26–32: Demo prep
- [ ] Write + rehearse [[../03-Demo-Script/Demo-Script]]
- [ ] Record backup demo video (in case live wifi fails)
- [ ] Slides finalized from [[Pitch]]

## Hours 32–36: Buffer + submission
- [ ] Freeze code, tag a release on GitHub
- [ ] Submit, sleep if possible, final rehearsal
