# orders.py: access to the ACME orders database.
# No dependency on MCP: this is plain Python, easy to test.
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
    number     TEXT PRIMARY KEY,
    customer   TEXT NOT NULL,
    status     TEXT NOT NULL,   -- received|shipped|delivered
    total      REAL NOT NULL,
    updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS complaints (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number TEXT NOT NULL,
    reason       TEXT NOT NULL);
"""

def open_connection(path="orders.db"):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row   # rows readable by column name
    conn.executescript(SCHEMA)
    return conn

def order_status(conn, number):
    """Order data, or None if the number does not exist."""
    row = conn.execute(
        "SELECT number, customer, status, total, updated_at "
        "FROM orders WHERE number = ?", (number,)).fetchone()
    return dict(row) if row else None

def orders_for(conn, customer, limit=10):
    """The most recent orders of a customer (partial match)."""
    rows = conn.execute(
        "SELECT number, status, total FROM orders "
        "WHERE customer LIKE ? ORDER BY updated_at DESC "
        "LIMIT ?", (f"%{customer}%", limit)).fetchall()
    return [dict(r) for r in rows]

def open_complaint(conn, order_number, reason):
    """Record a complaint; return the assigned id."""
    cur = conn.execute(
        "INSERT INTO complaints (order_number, reason) "
        "VALUES (?, ?)", (order_number, reason))
    conn.commit()
    return cur.lastrowid
