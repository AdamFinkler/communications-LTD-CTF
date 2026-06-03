# -*- coding: utf-8 -*-
"""
Delete / list customers in the database.

Usage (run from backend folder):
  python delete_customer.py              list all customers
  python delete_customer.py 175          delete customer by ID
  python delete_customer.py --reset      restore 6 default customers

Windows: double-click delete_customer.bat
"""
import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).parent / "database" / "database.db"

SEED = [
    (2, "Pizza America"),
    (3, "Southern Garage Ltd"),
    (1, "Blue Market Cafe"),
    (4, "TechVision Office"),
    (4, "KSP"),
    (3, "Ivory"),
]


def list_customers():
    conn = sqlite3.connect(DB)
    rows = conn.execute(
        "SELECT id, package_id, customer_name FROM customers ORDER BY id"
    ).fetchall()
    conn.close()
    print(f"\n=== Customers in database ({len(rows)} rows) ===")
    if not rows:
        print("(empty)")
        return rows
    print(f"{'ID':<6} {'Package':<8} {'Name'}")
    print("-" * 50)
    for cid, pkg, name in rows:
        print(f"{cid:<6} {pkg:<8} {name}")
    print()
    return rows


def delete_by_id(customer_id: int):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT customer_name FROM customers WHERE id = ?", (customer_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        print(f"Customer ID {customer_id} not found.")
        return False
    name = row[0]
    c.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    conn.commit()
    conn.close()
    print(f"Deleted: ID {customer_id} ({name})")
    return True


def reset_customers():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    before = c.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    c.execute("DELETE FROM customers")
    for package_id, name in SEED:
        c.execute(
            "INSERT INTO customers (package_id, customer_name) VALUES (?, ?)",
            (package_id, name),
        )
    conn.commit()
    after = c.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    conn.close()
    print(f"Reset done: {before} -> {after} customers (default list)")
    return True


def main():
    if not DB.exists():
        print(f"Database not found: {DB}")
        print("Start the server once (uvicorn) to create the database file.")
        sys.exit(1)

    if len(sys.argv) == 1:
        list_customers()
        print("To delete:  python delete_customer.py <ID>")
        print("To reset:   python delete_customer.py --reset")
        return

    if sys.argv[1] in ("--reset", "-r", "reset"):
        reset_customers()
        list_customers()
        return

    try:
        customer_id = int(sys.argv[1])
    except ValueError:
        print("Error: enter a numeric ID, e.g. python delete_customer.py 175")
        sys.exit(1)

    delete_by_id(customer_id)
    list_customers()


if __name__ == "__main__":
    main()
