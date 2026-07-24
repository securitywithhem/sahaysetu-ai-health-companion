"""
rule_engine.py
Deterministic symptom-triage engine.

Design principle: this module makes the ONLY decision that matters (Green /
Yellow / Red). It never calls an LLM and never depends on network access, so
it is fast, testable, and fully offline-capable — critical for low-connectivity
rural deployment.

The LLM layer (llm_explainer.py) is only ever allowed to *narrate* the result
this engine produces. It cannot change the triage level.
"""

from dataclasses import dataclass, field
from enum import Enum


class TriageLevel(str, Enum):
    GREEN = "GREEN"    # home care
    YELLOW = "YELLOW"  # consult doctor within 48 hours
    RED = "RED"        # visit hospital immediately


# --- Red-flag symptom keywords -> instant RED ---------------------------------
RED_FLAG_SYMPTOMS = {
    "severe chest pain", "chest pain", "difficulty breathing",
    "shortness of breath", "loss of consciousness", "unconscious",
    "uncontrolled bleeding", "heavy bleeding", "severe abdominal pain",
    "slurred speech", "one-sided weakness", "seizure", "coughing blood",
    "blue lips", "suicidal", "severe allergic reaction", "anaphylaxis",
}

# --- Yellow-flag keywords -> at least YELLOW -----------------------------------
YELLOW_FLAG_SYMPTOMS = {
    "persistent pain", "high fever", "fever", "vomiting", "diarrhea",
    "dizziness", "rash", "swelling", "moderate pain", "cough",
    "sore throat", "fatigue", "nausea",
}

# --- Vital sign thresholds -----------------------------------------------------
VITAL_RED_THRESHOLDS = {
    "heart_rate": lambda v: v is not None and (v > 130 or v < 40),
    "spo2": lambda v: v is not None and v < 90,
    "temperature_c": lambda v: v is not None and v >= 40.0,
    "systolic_bp": lambda v: v is not None and (v > 180 or v < 80),
}

VITAL_YELLOW_THRESHOLDS = {
    "heart_rate": lambda v: v is not None and (v > 110 or v < 50),
    "spo2": lambda v: v is not None and v < 94,
    "temperature_c": lambda v: v is not None and v >= 38.5,
    "systolic_bp": lambda v: v is not None and (v > 150 or v < 90),
}


@dataclass
class TriageResult:
    level: TriageLevel
    confidence: float
    reason: str
    red_flags: list[str] = field(default_factory=list)
    recommended_next_step: str = ""


def _normalize(symptoms: list[str]) -> list[str]:
    return [s.strip().lower() for s in symptoms]


def run_triage(symptoms: list[str], vitals: dict, duration_days: float = 0) -> TriageResult:
    """
    symptoms: list of free-text symptom strings (already lightly normalized
              upstream, e.g. via a symptom-picker UI rather than raw free text)
    vitals:   dict with optional keys heart_rate, spo2, temperature_c, systolic_bp
    duration_days: how long symptoms have persisted
    """
    norm_symptoms = _normalize(symptoms)
    matched_red = [s for s in norm_symptoms if any(rf in s for rf in RED_FLAG_SYMPTOMS)]
    matched_yellow = [s for s in norm_symptoms if any(yf in s for yf in YELLOW_FLAG_SYMPTOMS)]

    vital_red = [k for k, check in VITAL_RED_THRESHOLDS.items() if check(vitals.get(k))]
    vital_yellow = [k for k, check in VITAL_YELLOW_THRESHOLDS.items() if check(vitals.get(k))]

    # --- RED: any hard red flag wins immediately, fail-safe by design ---
    if matched_red or vital_red:
        flags = matched_red + [f"abnormal {k}" for k in vital_red]
        return TriageResult(
            level=TriageLevel.RED,
            confidence=0.98,
            reason="Symptoms or vitals indicate a potentially severe or "
                   "life-threatening condition requiring urgent medical intervention.",
            red_flags=flags,
            recommended_next_step="Proceed to the nearest emergency department "
                                   "or call emergency services immediately. Do not delay.",
        )

    # --- YELLOW: soft flags, persistence, or borderline vitals ---
    if matched_yellow or vital_yellow or duration_days >= 3:
        flags = matched_yellow + [f"borderline {k}" for k in vital_yellow]
        return TriageResult(
            level=TriageLevel.YELLOW,
            confidence=0.80,
            reason="Symptoms suggest a condition that requires medical attention "
                   "but is not immediately life-threatening.",
            red_flags=flags,
            recommended_next_step="Schedule an appointment with a primary care "
                                   "physician within two days. Prepare a symptom list.",
        )

    # --- GREEN: nothing concerning matched ---
    return TriageResult(
        level=TriageLevel.GREEN,
        confidence=0.95,
        reason="Symptoms indicate a common, non-severe condition manageable with self-care.",
        red_flags=[],
        recommended_next_step="Rest, hydration, and over-the-counter remedies as "
                               "appropriate. Observe for 24-48 hours and re-check "
                               "if symptoms worsen.",
    )


def detect_unhealthy_trend(readings: list[float], target: float, tolerance: float = 0.15) -> bool:
    """Simple chronic-disease trend flag: are the last 3 readings consistently
    outside the target range by more than `tolerance`?"""
    if len(readings) < 3:
        return False
    recent = readings[-3:]
    band = target * tolerance
    return all(r > target + band for r in recent) or all(r < target - band for r in recent)
