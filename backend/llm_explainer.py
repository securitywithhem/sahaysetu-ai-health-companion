import os
from google import genai
from backend.models import Vitals

# Initialize client if API key is available
try:
    client = genai.Client()
except Exception:
    client = None

def get_deterministic_explanation(triage_level: str, language: str) -> str:
    """Fallback deterministic explanation when LLM is unavailable."""
    # A simple dictionary for a few languages; default to English if not found
    templates = {
        "english": {
            "RED": "Critical situation detected. Please visit a hospital immediately.",
            "YELLOW": "Potential concern detected. Please consult a doctor within 48 hours.",
            "GREEN": "No immediate critical concerns detected. Home care is sufficient."
        },
        "hindi": {
            "RED": "गंभीर स्थिति का पता चला है। कृपया तुरंत अस्पताल जाएं।",
            "YELLOW": "संभावित चिंता का पता चला है। कृपया 48 घंटे के भीतर डॉक्टर से सलाह लें।",
            "GREEN": "कोई तत्काल महत्वपूर्ण चिंता नहीं पाई गई। घरेलू देखभाल पर्याप्त है।"
        }
    }
    
    lang_key = language.lower().strip()
    if lang_key not in templates:
        lang_key = "english"
        
    return templates[lang_key].get(triage_level, templates["english"][triage_level])

def explain_triage(triage_level: str, symptoms: list[str], vitals: dict | Vitals, language: str) -> str:
    """
    Calls the Gemini API to explain the triage level in plain language.
    Does NOT change the triage level.
    Falls back to a deterministic string if it fails or API key is absent.
    """
    if not client:
        return get_deterministic_explanation(triage_level, language)
        
    vitals_dict = vitals.model_dump() if hasattr(vitals, 'model_dump') else vitals

    prompt = f"""
    You are an AI medical explainer. The clinical rule engine has already determined the patient's triage level as: {triage_level}.
    Under NO CIRCUMSTANCES should you change this level or suggest a different level. Your only job is to explain why this decision was made in plain language, in {language}.
    
    Patient Data:
    - Symptoms: {', '.join(symptoms) if symptoms else 'None provided'}
    - Vitals: {vitals_dict}
    
    Triage meaning:
    - RED: Visit hospital immediately.
    - YELLOW: Consult doctor within 48 hours.
    - GREEN: Home care.
    
    Keep the explanation brief, empathetic, and clear.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        if response and response.text:
            return response.text.strip()
        else:
            return get_deterministic_explanation(triage_level, language)
    except Exception as e:
        print(f"LLM explanation failed: {e}")
        return get_deterministic_explanation(triage_level, language)
