"""
Flask backend for the AI Insurance Claim Parser.

Serves the dashboard and provides REST API endpoints
for submitting and managing insurance claims.
"""

import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from ai_parser import get_active_provider, parse_claim
from database import get_all_claims, init_db, insert_claim, update_claim_status

# Load environment variables from .env file (if it exists)
load_dotenv()

app = Flask(__name__)


# ---------------------------------------------------------------------------
# Initialize database on startup
# ---------------------------------------------------------------------------
with app.app_context():
    init_db()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.route("/")
def index():
    """Serve the main dashboard page."""
    claims = get_all_claims()
    provider = get_active_provider()
    return render_template("index.html", claims=claims, provider=provider)


@app.route("/api/claims", methods=["GET"])
def api_get_claims():
    """Return all claims as JSON (for dynamic frontend updates)."""
    claims = get_all_claims()
    return jsonify(claims)


@app.route("/api/incoming-claim", methods=["POST"])
def api_incoming_claim():
    """
    Process an incoming claim.

    Expects JSON body:
        {
            "sender_email": "...",
            "raw_text": "..."
        }

    Sends raw_text to AI parser, stores result in SQLite,
    and returns the parsed claim as JSON.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    sender_email = data.get("sender_email", "").strip()
    raw_text = data.get("raw_text", "").strip()

    if not sender_email:
        return jsonify({"error": "sender_email is required"}), 400
    if not raw_text:
        return jsonify({"error": "raw_text is required"}), 400

    # Parse the claim with AI (or mock)
    try:
        analysis = parse_claim(raw_text)
    except Exception as e:
        return jsonify({"error": f"AI parsing failed: {str(e)}"}), 500

    # Store in database
    claim_data = {
        "sender_email": sender_email,
        "raw_text": raw_text,
        "client_name": analysis.client_name,
        "accident_date": analysis.accident_date,
        "claim_type": analysis.claim_type,
        "damage_estimation": analysis.damage_estimation,
        "ai_summary": analysis.ai_summary,
        "status": analysis.suggested_status,
    }

    saved_claim = insert_claim(claim_data)

    # Notify n8n workflow about the new processed claim (optional integration)
    n8n_new_claim_url = os.environ.get("N8N_NEW_CLAIM_WEBHOOK_URL", "").strip()
    if n8n_new_claim_url:
        try:
            import requests
            requests.post(n8n_new_claim_url, json=saved_claim, timeout=5)
            print(f"[Webhook] Notified n8n about new claim #{saved_claim['id']}")
        except Exception as e:
            print(f"[Warning] Failed to notify n8n about new claim: {e}")

    return jsonify(saved_claim), 201


@app.route("/api/claim/<int:claim_id>/status", methods=["POST"])
def api_update_status(claim_id: int):
    """
    Update the status of a claim.

    Expects JSON body:
        {
            "status": "Approved" | "Rejected" | "Pending" | "Requires Human Review"
        }
    """
    data = request.get_json()

    if not data or "status" not in data:
        return jsonify({"error": "status field is required"}), 400

    new_status = data["status"].strip()
    valid_statuses = {"Pending", "Approved", "Rejected", "Requires Human Review"}

    if new_status not in valid_statuses:
        return jsonify({"error": f"Invalid status. Must be one of: {valid_statuses}"}), 400

    updated = update_claim_status(claim_id, new_status)

    if updated is None:
        return jsonify({"error": "Claim not found"}), 404

    # Notify n8n workflow about status change (optional integration)
    n8n_url = os.environ.get("N8N_STATUS_WEBHOOK_URL", "").strip()
    if n8n_url:
        try:
            import requests
            requests.post(n8n_url, json=updated, timeout=5)
            print(f"[Webhook] Notified n8n about status change for claim #{claim_id}")
        except Exception as e:
            print(f"[Warning] Failed to notify n8n: {e}")

    return jsonify(updated)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
