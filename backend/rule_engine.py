from typing import List, Dict, Any

RED_FLAG_KEYWORDS = [
    "chest pain",
    "difficulty breathing",
    "loss of consciousness",
    "uncontrolled bleeding",
    "severe abdominal pain",
    "stroke symptoms",
    "paralysis",
    "seizure",
    "choking",
]

def check_symptoms(symptoms: List[str]) -> str:
    if not symptoms:
        return "GREEN"
    
    # Normalize to lowercase for checking
    symptoms_lower = [s.lower() for s in symptoms]
    
    for symptom in symptoms_lower:
        for flag in RED_FLAG_KEYWORDS:
            if flag in symptom:
                return "RED"
                
    return "GREEN"

def check_vitals(vitals: Dict[str, Any]) -> str:
    if not vitals:
        return "GREEN"
        
    highest_level = "GREEN"
    
    hr = vitals.get("heart_rate")
    if hr is not None:
        if hr > 130 or hr < 40:
            return "RED"
        elif hr > 100 or hr < 50:
            highest_level = "YELLOW"
            
    spo2 = vitals.get("spo2")
    if spo2 is not None:
        if spo2 < 90:
            return "RED"
        elif spo2 < 95:
            highest_level = "YELLOW"
            
    temp = vitals.get("temperature")
    if temp is not None:
        if temp > 40.0 or temp < 35.0:
            return "RED"
        elif temp > 38.5 or temp < 36.0:
            highest_level = "YELLOW"
            
    sbp = vitals.get("systolic_bp")
    if sbp is not None:
        if sbp > 180 or sbp < 90:
            return "RED"
        elif sbp > 140 or sbp < 100:
            highest_level = "YELLOW"
            
    return highest_level

def evaluate_triage(symptoms: List[str], vitals: Dict[str, Any], duration_days: int) -> str:
    """
    Evaluates clinical triage level. Returns 'RED', 'YELLOW', or 'GREEN'.
    Failsafe: returns 'RED' if an unexpected error occurs.
    """
    try:
        # Check symptoms for hard red flags
        sym_level = check_symptoms(symptoms)
        if sym_level == "RED":
            return "RED"
            
        # Check vitals thresholds
        vit_level = check_vitals(vitals)
        if vit_level == "RED":
            return "RED"
            
        # Nudge to YELLOW if duration >= 3 days
        if duration_days >= 3:
            return "YELLOW"
            
        # If neither RED was triggered, and duration is short, return the worst of symptoms or vitals
        # Note: sym_level is GREEN here, so it only depends on vit_level
        return vit_level
        
    except Exception:
        # Fail-safe default to most cautious level
        return "RED"
