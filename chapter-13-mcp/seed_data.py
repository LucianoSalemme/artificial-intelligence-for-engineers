# seed_data.py: inserts the three sample orders mentioned in the
# chapter, including ORD-1042 from Rossi Ltd in the "shipped"
# status (updated on 2026-08-02, total 149.00).
import orders

SAMPLE_ORDERS = [
    ("ORD-1042", "Rossi Ltd", "shipped", 149.00, "2026-08-02"),
    ("ORD-1039", "Bianchi Inc", "delivered", 89.90, "2026-07-21"),
    ("ORD-1051", "Rossi Ltd", "received", 320.00, "2026-08-05"),
]

def main():
    conn = orders.open_connection()
    try:
        for row in SAMPLE_ORDERS:
            conn.execute(
                "INSERT OR REPLACE INTO orders "
                "(number, customer, status, total, updated_at) "
                "VALUES (?, ?, ?, ?, ?)", row)
        conn.commit()
    finally:
        conn.close()
    print(f"Inserted {len(SAMPLE_ORDERS)} sample orders "
          "into orders.db.")

if __name__ == "__main__":
    main()
