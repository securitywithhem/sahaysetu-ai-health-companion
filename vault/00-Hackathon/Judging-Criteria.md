---
tags: [hackathon, judging]
---

# Judging Criteria Checklist (generic hackathon rubric — adapt once official rubric is posted)

- [ ] **Working demo** — symptom checker + triage result end-to-end, live, no crashes
- [ ] **Technical depth** — rule engine + LLM separation is the story; be ready to show `rule_engine.py` and explain *why* it's deterministic
- [ ] **Real-world relevance** — rural India connectivity story, offline-first
- [ ] **Responsible AI / safety** — "AI assists, never diagnoses"; fail-safe defaults; explainability
- [ ] **UI/UX polish** — clean triage color coding (green/yellow/red), multilingual toggle if time allows
- [ ] **Business viability** — stakeholder impact slide (patients / doctors / system)
- [ ] **Presentation** — 3-minute pitch + 2-minute live demo + Q&A prep (see [[../03-Demo-Script/Demo-Script]])
- [ ] **Originality** — lean into the "rule engine as safety backbone" framing; most teams will just wrap an LLM

## Common judge questions to pre-answer
1. "What happens if the LLM hallucinates?" → It can't change the triage level, only the wording. Show the code.
2. "How does this work offline?" → Rule engine has zero network dependency; LLM explanation falls back to templates.
3. "Is this a medical device?" → No — informational triage + guidance, explicit disclaimers, always defers to professionals for Yellow/Red.
4. "How do you validate the rules?" → Reference clinical red-flag guidelines (WHO/IMCI-style symptom checklists) — cite sources in the slide.
