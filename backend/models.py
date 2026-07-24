from pydantic import BaseModel, Field


class Vitals(BaseModel):
    heart_rate: float | None = None
    spo2: float | None = None
    temperature_c: float | None = None
    systolic_bp: float | None = None


class TriageRequest(BaseModel):
    symptoms: list[str] = Field(..., examples=[["fever", "cough"]])
    vitals: Vitals = Vitals()
    duration_days: float = 0
    language: str = "en"  # for multilingual explanation, e.g. "hi", "fr"


class TriageResponse(BaseModel):
    level: str
    confidence: float
    reason: str
    red_flags: list[str]
    recommended_next_step: str
    explanation: str  # LLM-generated, plain-language narration


class ChronicReading(BaseModel):
    metric: str          # e.g. "blood_sugar"
    value: float
    unit: str
    timestamp: str        # ISO 8601


class ChronicTrendResponse(BaseModel):
    metric: str
    unhealthy_trend: bool
    readings_considered: int
    message: str
