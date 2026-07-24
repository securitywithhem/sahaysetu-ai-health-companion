import pytest
from backend.rule_engine import evaluate_triage

def test_triage_green():
    """Test mild symptoms with normal vitals and short duration."""
    symptoms = ["mild headache", "runny nose"]
    vitals = {
        "heart_rate": 80,
        "spo2": 98,
        "temperature": 37.0,
        "systolic_bp": 120
    }
    assert evaluate_triage(symptoms, vitals, duration_days=1) == "GREEN"

def test_triage_red_symptom():
    """Test immediate red flag symptom."""
    symptoms = ["I have severe chest pain"]
    vitals = {
        "heart_rate": 80,
        "spo2": 98,
        "temperature": 37.0,
        "systolic_bp": 120
    }
    assert evaluate_triage(symptoms, vitals, duration_days=1) == "RED"

def test_triage_red_vitals():
    """Test critical vitals overriding mild symptoms."""
    symptoms = ["mild headache"]
    vitals = {
        "heart_rate": 135, # RED threshold
        "spo2": 98,
        "temperature": 37.0,
        "systolic_bp": 120
    }
    assert evaluate_triage(symptoms, vitals, duration_days=1) == "RED"

def test_triage_yellow_vitals():
    """Test borderline vitals resulting in YELLOW."""
    symptoms = ["mild headache"]
    vitals = {
        "heart_rate": 105, # YELLOW threshold
        "spo2": 96,
        "temperature": 37.0,
        "systolic_bp": 120
    }
    assert evaluate_triage(symptoms, vitals, duration_days=1) == "YELLOW"

def test_triage_yellow_duration():
    """Test duration >= 3 days nudges GREEN to YELLOW."""
    symptoms = ["mild headache"]
    vitals = {
        "heart_rate": 80,
        "spo2": 98,
        "temperature": 37.0,
        "systolic_bp": 120
    }
    assert evaluate_triage(symptoms, vitals, duration_days=3) == "YELLOW"

def test_triage_missing_vitals():
    """Test missing vitals don't crash and default safely based on symptoms."""
    symptoms = ["cough"]
    vitals = {}
    assert evaluate_triage(symptoms, vitals, duration_days=1) == "GREEN"

def test_triage_empty_symptoms():
    """Test empty symptoms."""
    symptoms = []
    vitals = {
        "heart_rate": 80,
        "spo2": 98,
        "temperature": 37.0,
        "systolic_bp": 120
    }
    assert evaluate_triage(symptoms, vitals, duration_days=1) == "GREEN"

def test_triage_failsafe():
    """Test fail-safe triggers on unexpected exceptions."""
    symptoms = ["cough"]
    # Passing an invalid type to trigger an internal exception during vitals checking
    vitals = {"heart_rate": "invalid_string_not_int"}
    assert evaluate_triage(symptoms, vitals, duration_days=1) == "RED"
