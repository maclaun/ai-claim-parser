"""
SQLite database layer for the claims system.

Handles table creation, inserts, queries, and status updates.
The database file (claims.db) is created automatically on first run.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "claims.db"


def get_connection() -> sqlite3.Connection:
    """Return a connection with row_factory set to sqlite3.Row."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    """Create the claims table if it does not exist."""
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS claims (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_email     TEXT    NOT NULL,
            raw_text         TEXT    NOT NULL,
            client_name      TEXT,
            accident_date    TEXT,
            claim_type       TEXT,
            damage_estimation REAL,
            ai_summary       TEXT,
            status           TEXT    NOT NULL DEFAULT 'Pending',
            created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def insert_claim(data: dict) -> dict:
    """
    Insert a new claim into the database.

    Args:
        data: Dictionary with keys matching the claims table columns.

    Returns:
        The full inserted row as a dictionary (including generated id and created_at).
    """
    conn = get_connection()
    cursor = conn.execute(
        """
        INSERT INTO claims
            (sender_email, raw_text, client_name, accident_date,
             claim_type, damage_estimation, ai_summary, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data["sender_email"],
            data["raw_text"],
            data.get("client_name"),
            data.get("accident_date"),
            data.get("claim_type"),
            data.get("damage_estimation"),
            data.get("ai_summary"),
            data.get("status", "Pending"),
        ),
    )
    claim_id = cursor.lastrowid
    conn.commit()

    # Fetch the full row to return (includes created_at)
    row = conn.execute("SELECT * FROM claims WHERE id = ?", (claim_id,)).fetchone()
    conn.close()
    return dict(row)


def get_all_claims() -> list[dict]:
    """Return all claims ordered by newest first."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM claims ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def update_claim_status(claim_id: int, status: str) -> dict | None:
    """
    Update the status of a claim.

    Args:
        claim_id: The ID of the claim to update.
        status: New status value.

    Returns:
        The updated row as a dictionary, or None if claim not found.
    """
    conn = get_connection()
    conn.execute(
        "UPDATE claims SET status = ? WHERE id = ?",
        (status, claim_id),
    )
    conn.commit()

    row = conn.execute("SELECT * FROM claims WHERE id = ?", (claim_id,)).fetchone()
    conn.close()
    return dict(row) if row else None
