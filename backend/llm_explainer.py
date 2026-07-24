"""
llm_explainer.py
Calls Gemini (or falls back to a template) to turn a TriageResult into a
warm, plain-language explanation. This layer is explicitly NOT allowed to
change the triage level — it only narrates. If the API key is missing or
the call fails, we fall back to a deterministic template so the app still
works fully offline.
"""

import os
from rule_engine import TriageResult

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

SYSTEM_INSTRUCTIONS = """You are a calm, plain-language health explainer.
You are given a triage level that has ALREADY been decided by a clinical
rule engine. Your only job is to explain WHY in simple words a 10-year-old
could understand, in the requested language. You must NEVER:
- change the triage level
- suggest a diagnosis
- suggest specific medication doses
Keep it to 2-3 short sentences.
"""


def _template_fallback(result: TriageResult, language: str) -> str:
    templates = {
        "GREEN": "This looks like something you can manage safely at home. "
                 "Rest, drink fluids, and keep an eye on how you feel over the next day or two.",
        "YELLOW": "This isn't an emergency, but it's worth having a doctor take a look "
                  "within the next couple of days, just to be safe.",
        "RED": "This combination of signs can be serious. Please get to a hospital "
               "or call for emergency help right away — don't wait.",
    }
    return templates.get(result.level.value, "Please consult a healthcare professional.")


def explain(result: TriageResult, language: str = "en") -> str:
    if not GEMINI_API_KEY:
        return _template_fallback(result, language)

    try:
        import google.generativeai as genai

        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            f"{SYSTEM_INSTRUCTIONS}\n\n"
            f"Triage level: {result.level.value}\n"
            f"Reason: {result.reason}\n"
            f"Red flags: {', '.join(result.red_flags) or 'none'}\n"
            f"Respond in language code: {language}\n"
        )
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        # Network / quota / parsing failure -> fail safe to template, never crash
        return _template_fallback(result, language)
