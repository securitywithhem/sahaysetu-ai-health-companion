---
tags: [hackathon, pitch, tetrathon2026]
---

# AI Health Companion — Pitch

## One-liner
AI-powered symptom triage and chronic disease self-management for semi-urban and rural India — early guidance, better decisions, healthier lives.

## Problem (see [[Problem-Statement]])
- Symptom ambiguity → patients can't judge severity
- Unnecessary hospital visits vs. delayed care for real emergencies
- Poor medication adherence for chronic conditions
- Fragmented data reaching doctors
- Low connectivity in rural areas

## Solution — 4 modules
1. **AI Symptom Checker** — instant, personalized triage (Green/Yellow/Red)
2. **Chronic Disease Tracker** — continuous logging → trend detection
3. **AI Health Coach** — adapts guidance to tracked data
4. **Weekly Doctor Summary** — concise report, QR-shareable

## Why we win on safety (judges love this)
> Rule Engine decides. LLM explains. Never the other way around.

- Deterministic red-flag detection for emergencies (works offline)
- LLM (Gemini) only narrates the decision in plain language / local language
- "AI Assists, Never Diagnoses" on every screen

## Differentiators to say out loud in the demo
- Offline-first: rule engine has zero external dependencies
- Explainable: every triage result shows *why*
- Built for low-bandwidth: React + IndexedDB, optional cloud sync
- Weekly QR doctor report — turns messy patient stories into structured data

## Tagline
**Early Guidance. Better Decisions. Healthier Lives.**
