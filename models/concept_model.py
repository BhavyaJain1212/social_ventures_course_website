"""
Concept Model — SQLite persistence layer for saved design concepts.

Provides CRUD operations for the saved_concepts table.
Can be swapped for SQLAlchemy or another ORM later without
changing the service/route layer.
"""

import sqlite3
import os
from datetime import datetime

# Default database path (relative to project root)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "app.db")


def _get_connection(db_path=None):
    """Create a database connection with row factory for dict-like access."""
    path = db_path or DB_PATH
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path=None):
    """
    Initialize the database schema.
    Called once on application startup.
    """
    conn = _get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_concepts (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            title           TEXT NOT NULL,
            craft_type      TEXT NOT NULL,
            product_type    TEXT NOT NULL,
            target_audience TEXT,
            style           TEXT,
            color_palette   TEXT,
            motif_direction TEXT,
            prompt_text     TEXT,
            image_url       TEXT,
            summary         TEXT,
            created_at      TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()


def create_concept(data, db_path=None):
    """
    Insert a new design concept into the database.

    Args:
        data (dict): Concept fields (title, craft_type, product_type, etc.)

    Returns:
        int: The ID of the newly created concept.
    """
    conn = _get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO saved_concepts
            (title, craft_type, product_type, target_audience, style,
             color_palette, motif_direction, prompt_text, image_url, summary)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("title", "Untitled Concept"),
        data.get("craft_type", ""),
        data.get("product_type", ""),
        data.get("target_audience", ""),
        data.get("style", ""),
        data.get("color_palette", ""),
        data.get("motif_direction", ""),
        data.get("prompt_text", ""),
        data.get("image_url", ""),
        data.get("summary", ""),
    ))
    conn.commit()
    concept_id = cursor.lastrowid
    conn.close()
    return concept_id


def get_all_concepts(db_path=None):
    """Return all saved concepts, newest first."""
    conn = _get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM saved_concepts ORDER BY created_at DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_concept_by_id(concept_id, db_path=None):
    """Return a single concept by its ID, or None."""
    conn = _get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM saved_concepts WHERE id = ?", (concept_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def delete_concept(concept_id, db_path=None):
    """Delete a concept by its ID. Returns True if a row was deleted."""
    conn = _get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM saved_concepts WHERE id = ?", (concept_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted
