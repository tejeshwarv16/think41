# milestone1/verify_db.py
import sqlite3

DB_FILE = "ecommerce.db"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

print("--- Verifying 'departments' table ---")
cursor.execute("SELECT * FROM departments LIMIT 5;")
rows = cursor.fetchall()
for row in rows:
    print(f"  ID: {row[0]}, Name: {row[1]}")

print("\n--- Verifying 'products' table columns ---")
cursor.execute("PRAGMA table_info(products);")
columns = cursor.fetchall()
column_names = [col[1] for col in columns]
print(f"  Columns: {column_names}")

if 'department_id' in column_names and 'department' not in column_names:
    print("  ✅ 'products' table structure is correct.")
else:
    print("  ❌ 'products' table structure is incorrect.")

conn.close()