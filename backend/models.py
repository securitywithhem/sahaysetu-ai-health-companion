from pydantic import BaseModel, Field
from typing import List, Optional

class Vitals(BaseModel):
    heart_rate: Optional[int] = Field(None, description="Heart rate in bpm")
    spo2: Optional[int] = Field(None, description="Blood oxygen saturation in %")
    temperature: Optional[float] = Field(None, description="Body temperature in Celsius")
    systolic_bp: Optional[int] = Field(None, description="Systolic blood pressure in mmHg")

class TriageRequest(BaseModel):
    symptoms: List[str] = Field(..., description="List of patient symptoms")
    vitals: Optional[Vitals] = Field(None, description="Patient vital signs")
    duration_days: int = Field(0, ge=0, description="Duration of symptoms in days")
    language: str = Field("English", description="Preferred language for the explanation")

class TriageResponse(BaseModel):
    triage_level: str = Field(..., description="Triage level: RED, YELLOW, or GREEN")
    explanation: str = Field(..., description="Plain-language explanation of the triage result")

class ChronicLogRequest(BaseModel):
    metric_name: str = Field(..., description="Name of the metric (e.g., blood_sugar, blood_pressure)")
    value: float = Field(..., description="Value of the metric")
    unit: str = Field(..., description="Unit of the metric (e.g., mg/dL, mmHg)")

class ChronicLogResponse(BaseModel):
    trend_status: str = Field(..., description="Trend status: healthy, unhealthy, or insufficient_data")
    message: str = Field(..., description="Explanation of the trend")
