from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

from backend.models import TriageRequest, TriageResponse, ChronicLogRequest, ChronicLogResponse
from backend.rule_engine import evaluate_triage
from backend.llm_explainer import explain_triage

app = FastAPI(title="SahaySetu AI Health Companion API")

# Setup CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for chronic logs: metric_name -> list of values
chronic_logs_store: Dict[str, List[float]] = {}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/triage", response_model=TriageResponse)
def perform_triage(request: TriageRequest):
    try:
        # 1. Deterministic Rule Engine Decision
        # Ensure vitals is a dictionary if provided
        vitals_dict = request.vitals.model_dump() if request.vitals else {}
        triage_level = evaluate_triage(
            symptoms=request.symptoms,
            vitals=vitals_dict,
            duration_days=request.duration_days
        )
        
        # 2. LLM Explanation (or deterministic fallback)
        explanation = explain_triage(
            triage_level=triage_level,
            symptoms=request.symptoms,
            vitals=vitals_dict,
            language=request.language
        )
        
        return TriageResponse(
            triage_level=triage_level,
            explanation=explanation
        )
    except Exception as e:
        # Fallback in case of absolute failure
        return TriageResponse(
            triage_level="RED",
            explanation="An unexpected error occurred. Please seek medical attention immediately."
        )

@app.post("/api/chronic/log", response_model=ChronicLogResponse)
def log_chronic_metric(request: ChronicLogRequest):
    metric = request.metric_name.lower()
    
    if metric not in chronic_logs_store:
        chronic_logs_store[metric] = []
        
    chronic_logs_store[metric].append(request.value)
    
    readings = chronic_logs_store[metric]
    
    if len(readings) < 3:
        return ChronicLogResponse(
            trend_status="insufficient_data",
            message=f"Logged successfully. Need {3 - len(readings)} more readings to establish a trend."
        )
        
    # Take the last 3 readings
    last_three = readings[-3:]
    
    # Simple logic for trend: 
    # If it's increasing consecutively, mark as unhealthy (simplistic, for the hackathon).
    # For actual clinical use, it depends on the metric (e.g. blood_sugar increasing is bad, spo2 decreasing is bad).
    # Let's apply a generic variance or consecutive bad direction check.
    # To keep it generic but safe: if the last 3 readings are strictly increasing, we call it out.
    if last_three[0] < last_three[1] < last_three[2]:
        return ChronicLogResponse(
            trend_status="unhealthy",
            message=f"Warning: Your {request.metric_name} readings show a consistent increasing trend."
        )
    elif last_three[0] > last_three[1] > last_three[2]:
        return ChronicLogResponse(
            trend_status="unhealthy",
            message=f"Warning: Your {request.metric_name} readings show a consistent decreasing trend."
        )
    else:
        return ChronicLogResponse(
            trend_status="healthy",
            message=f"Your recent {request.metric_name} readings appear stable."
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
