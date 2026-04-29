"""
Preorder Model — SQLite persistence for shop preorder interest.

For the MVP, a preorder records interest in a mock product listing.
It does not create a checkout, payment, or fulfillment workflow.
"""

import os
import sqlite3


DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "app.db")


def _get_connection(db_path=None):
    """Create a database connection with row factory for dict-like access."""
    path = db_path or DB_PATH
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_preorder_db(db_path=None):
    """Initialize the preorder interest table."""
    conn = _get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS preorder_interests (
            id                 INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id         TEXT NOT NULL,
            product_name       TEXT NOT NULL,
            artisan_name       TEXT,
            craft_type         TEXT,
            region             TEXT,
            price              INTEGER,
            currency           TEXT,
            availability_status TEXT,
            estimated_delivery TEXT,
            status             TEXT DEFAULT 'interest_recorded',
            created_at         TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()


def create_preorder_interest(product, db_path=None):
    """
    Save preorder interest for a product snapshot.

    Args:
        product (dict): Product data from the mock catalog.

    Returns:
        int: New preorder interest ID.
    """
    conn = _get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO preorder_interests
            (product_id, product_name, artisan_name, craft_type, region,
             price, currency, availability_status, estimated_delivery)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        product.get("id", ""),
        product.get("name", ""),
        product.get("artisan_name", ""),
        product.get("craft_type", ""),
        product.get("region", ""),
        product.get("price"),
        product.get("currency", ""),
        product.get("availability_status", ""),
        product.get("estimated_delivery", ""),
    ))
    conn.commit()
    preorder_id = cursor.lastrowid
    conn.close()
    return preorder_id
