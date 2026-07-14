"""
AI Claim Parser module.

Supports multiple AI providers with automatic fallback:
  1. Groq (Llama 3.1 8B) — primary, fast and reliable
  2. Google Gemini — secondary fallback
  3. Mock parser — regex-based, works without any API key

The active provider is determined by environment variables:
  - GROQ_API_KEY → uses Groq
  - GEMINI_API_KEY → uses Gemini (if Groq unavailable)
  - Neither → uses mock parser
"""

import json
import os
import re

from models import ClaimAnalysis

# ---------------------------------------------------------------------------
# System prompt shared across all AI providers
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are an expert insurance claim analyst working for a legal compensation company. 
Your job is to analyze incoming claim emails and extract structured information.

RULES:
1. Extract the client's full name. If not found, set client_name to null.
2. Extract the accident/incident date in YYYY-MM-DD format if possible. If the exact date is unclear, use whatever date info is available. If none, set to null.
3. Classify the claim into one of these types:
   - "Car Accident" — vehicle collisions, traffic incidents
   - "Medical" — medical malpractice, hospital injuries
   - "Property Damage" — home, building, or property damage
   - "Workplace Injury" — injuries at work
   - "Other" — anything that doesn't fit above
4. Extract the estimated damage amount as a plain number (no currency symbols). If not mentioned, set to null.
5. Write a brief 2-3 sentence summary of the claim.
6. Suggest a status:
   - "Pending" — if the claim has sufficient data and damage < 50000
   - "Requires Human Review" — if key information is missing, damage >= 50000, or the claim seems unusual/complex
   - "Approved" — only if the claim is very straightforward with complete information and low damage

You MUST respond ONLY with valid JSON matching this exact schema:
{
  "client_name": "string or null",
  "accident_date": "string or null",
  "claim_type": "string",
  "damage_estimation": number or null,
  "ai_summary": "string",
  "suggested_status": "string"
}"""


# ---------------------------------------------------------------------------
# Groq provider (primary) — Llama 3.1 8B via Groq
# ---------------------------------------------------------------------------

GROQ_MODEL = "llama-3.1-8b-instant"


def parse_claim_with_groq(raw_text: str) -> ClaimAnalysis:
    """
    Parse claim using Groq API (Llama 3.1 8B Instant).

    Args:
        raw_text: The raw text of the insurance claim.

    Returns:
        ClaimAnalysis object with extracted fields.
    """
    from groq import Groq

    api_key = os.environ.get("GROQ_API_KEY", "")
    client = Groq(api_key=api_key)

    print(f"[AI] Calling Groq ({GROQ_MODEL})...")
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": raw_text},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
        max_tokens=1024,
    )

    result = json.loads(response.choices[0].message.content)
    print(f"[AI] Groq ({GROQ_MODEL}) success!")
    return ClaimAnalysis(**result)


# ---------------------------------------------------------------------------
# Gemini provider (secondary fallback)
# ---------------------------------------------------------------------------

GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-2.5-flash-lite",
]


def parse_claim_with_gemini(raw_text: str) -> ClaimAnalysis:
    """
    Parse claim using Google Gemini with structured output.

    Tries multiple models in order if one is unavailable.

    Args:
        raw_text: The raw text of the insurance claim.

    Returns:
        ClaimAnalysis object with extracted fields.

    Raises:
        Exception: If all Gemini models fail.
    """
    from google import genai
    from google.genai import types

    api_key = os.environ.get("GEMINI_API_KEY", "")
    client = genai.Client(api_key=api_key)

    last_error = None

    for model_name in GEMINI_MODELS:
        try:
            print(f"[AI] Trying Gemini model: {model_name}")
            response = client.models.generate_content(
                model=model_name,
                contents=raw_text,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    response_mime_type="application/json",
                    response_schema=ClaimAnalysis,
                    temperature=0.2,
                ),
            )
            result = json.loads(response.text)
            print(f"[AI] Gemini ({model_name}) success!")
            return ClaimAnalysis(**result)

        except Exception as e:
            last_error = e
            print(f"[AI] Gemini {model_name} failed: {e}")
            continue

    raise last_error or RuntimeError("All Gemini models failed")


# ---------------------------------------------------------------------------
# Mock parser — used when no API keys are available
# ---------------------------------------------------------------------------

def _extract_name_mock(text: str) -> str | None:
    """Try to extract a name from common patterns."""
    patterns = [
        r"(?:my name is|i am|i'm|this is)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
        r"(?:name|client|claimant)[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip().title()
    return None


def _extract_amount_mock(text: str) -> float | None:
    """Try to extract a monetary amount from text."""
    patterns = [
        r"(\d[\d\s,.]*)\s*(?:PLN|USD|EUR|GBP|zł|\$|€|£)",
        r"(?:cost|damage|amount|worth|estimate)[^\d]*(\d[\d\s,.]*)",
        r"(?:around|about|approximately|roughly)\s*(\d[\d\s,.]*)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            num_str = match.group(1).replace(" ", "").replace(",", "")
            try:
                return float(num_str)
            except ValueError:
                continue
    return None


def _detect_claim_type_mock(text: str) -> str:
    """Simple keyword-based claim type detection."""
    text_lower = text.lower()
    if any(w in text_lower for w in ["car", "vehicle", "truck", "collision", "traffic", "driving"]):
        return "Car Accident"
    if any(w in text_lower for w in ["hospital", "doctor", "medical", "surgery", "treatment"]):
        return "Medical"
    if any(w in text_lower for w in ["house", "property", "building", "roof", "flood", "fire"]):
        return "Property Damage"
    if any(w in text_lower for w in ["work", "workplace", "factory", "office injury"]):
        return "Workplace Injury"
    return "Other"


def parse_claim_mock(raw_text: str) -> ClaimAnalysis:
    """
    Mock parser that extracts basic info using regex patterns.
    Used when no API keys are available.

    Returns:
        ClaimAnalysis with [MOCK] prefix in summary.
    """
    name = _extract_name_mock(raw_text)
    amount = _extract_amount_mock(raw_text)
    claim_type = _detect_claim_type_mock(raw_text)

    # Simple date extraction
    date_match = re.search(
        r"(\w+\s+\d{1,2}(?:st|nd|rd|th)?,?\s*\d{4}|\d{1,2}[./]\d{1,2}[./]\d{2,4})",
        raw_text,
    )
    accident_date = date_match.group(1) if date_match else None

    # Determine status
    missing_fields = sum([name is None, accident_date is None, amount is None])
    if missing_fields >= 2:
        status = "Requires Human Review"
    elif amount and amount >= 50000:
        status = "Requires Human Review"
    else:
        status = "Pending"

    summary = f"[MOCK] Claim from {name or 'unknown client'} regarding {claim_type.lower()}."
    if amount:
        summary += f" Estimated damage: {amount:,.0f}."
    if missing_fields > 0:
        summary += f" Note: {missing_fields} field(s) could not be extracted automatically."

    return ClaimAnalysis(
        client_name=name,
        accident_date=accident_date,
        claim_type=claim_type,
        damage_estimation=amount,
        ai_summary=summary,
        suggested_status=status,
    )


# ---------------------------------------------------------------------------
# Main entry point — cascading provider fallback
# ---------------------------------------------------------------------------

def get_active_provider() -> str:
    """Return the name of the currently active AI provider."""
    if os.environ.get("GROQ_API_KEY", "").strip():
        return "groq"
    if os.environ.get("GEMINI_API_KEY", "").strip():
        return "gemini"
    return "mock"


def parse_claim(raw_text: str) -> ClaimAnalysis:
    """
    Parse a raw claim text using the best available AI provider.

    Priority: Groq (Llama 3.1 8B) -> Gemini -> Mock

    Args:
        raw_text: The raw text of the insurance claim email.

    Returns:
        ClaimAnalysis with structured claim data.
    """
    groq_key = os.environ.get("GROQ_API_KEY", "").strip()
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()

    # 1. Try Groq (primary)
    if groq_key:
        try:
            return parse_claim_with_groq(raw_text)
        except Exception as e:
            print(f"[WARNING] Groq API failed: {e}")

    # 2. Try Gemini (secondary)
    if gemini_key:
        try:
            return parse_claim_with_gemini(raw_text)
        except Exception as e:
            print(f"[WARNING] Gemini API failed: {e}")

    # 3. Fallback to mock
    if not groq_key and not gemini_key:
        print("[INFO] No API keys found (GROQ_API_KEY / GEMINI_API_KEY). Using mock parser.")
    else:
        print("[WARNING] All AI providers failed. Falling back to mock parser.")

    return parse_claim_mock(raw_text)
