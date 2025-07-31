# milestone1/demo_script.py
import sqlite3

DB_FILE = "ecommerce.db"
conn = sqlite3.connect(DB_FILE)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# 1. Show the new 'departments' table with sample data
print("--- 1. Sample Data from 'departments' Table ---")
cursor.execute("SELECT * FROM departments LIMIT 5;")
rows = cursor.fetchall()
for row in rows:
    print(f"  ID: {row['id']}, Name: {row['name']}")

# 2. Show the updated 'products' table structure
print("\n--- 2. Updated 'products' Table Columns ---")
cursor.execute("PRAGMA table_info(products);")
columns = cursor.fetchall()
column_names = [col['name'] for col in columns]
print(f"  Columns: {column_names}")
if 'department_id' in column_names and 'department' not in column_names:
    print("  ✅ Structure is correct (has 'department_id', old 'department' column is removed).")
else:
    print("  ❌ Structure is incorrect.")

# 3. Execute a JOIN query
print("\n--- 3. Sample JOIN Query Result ---")
print("  Query: SELECT p.name, d.name AS department FROM products p JOIN departments d ON p.department_id = d.id LIMIT 5;")
cursor.execute("""
    SELECT p.name, d.name AS department 
    FROM products p 
    JOIN departments d ON p.department_id = d.id 
    LIMIT 5;
""")
rows = cursor.fetchall()
for row in rows:
    print(f"  Product: \"{row['name']}\", Department: \"{row['department']}\"")

conn.close()