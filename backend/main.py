from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import TriageRequest, TriageResponse, ChronicReading, ChronicTrendResponse
from rule_engine import run_triage, detect_unhealthy_trend

app = FastAPI(
    title="AI Health Companion API",
    description="Safety-first symptom triage + chronic disease tracking for TetraTHON 2026",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten before production
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for the hackathon demo. Swap for SQLite/IndexedDB sync later.
_READINGS: dict[str, list[float]] = {}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/triage", response_model=TriageResponse)
def triage(req: TriageRequest):
    from llm_explainer import explain  # imported lazily so rule engine works with zero deps

    result = run_triage(
        symptoms=req.symptoms,
        vitals=req.vitals.model_dump(),
        duration_days=req.duration_days,
    )
    explanation = explain(result, language=req.language)

    return TriageResponse(
        level=result.level.value,
        confidence=result.confidence,
        reason=result.reason,
        red_flags=result.red_flags,
        recommended_next_step=result.recommended_next_step,
        explanation=explanation,
    )


@app.post("/api/chronic/log", response_model=ChronicTrendResponse)
def log_chronic_reading(reading: ChronicReading):
    target_by_metric = {"blood_sugar": 120.0, "systolic_bp": 120.0}
    target = target_by_metric.get(reading.metric, reading.value)

    _READINGS.setdefault(reading.metric, []).append(reading.value)
    unhealthy = detect_unhealthy_trend(_READINGS[reading.metric], target=target)

    message = (
        f"Your last 3 {reading.metric.replace('_', ' ')} readings are consistently "
        f"outside the healthy range. Consider mentioning this to your doctor."
        if unhealthy else
        f"{reading.metric.replace('_', ' ').title()} looks within a reasonable range."
    )

    return ChronicTrendResponse(
        metric=reading.metric,
        unhealthy_trend=unhealthy,
        readings_considered=len(_READINGS[reading.metric]),
        message=message,
    )
