# milestone1/show_schema.py
import sqlite3

# Change this line
DB_FILE = 'ecommerce.db'
TABLES_TO_SHOW = ['products', 'users', 'orders']

print("--- Database Schema ---")
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

for table_name in TABLES_TO_SHOW:
    cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    result = cursor.fetchone()
    if result:
        print(f"\n-- Table: {table_name} --")
        print(result[0])
    else:
        print(f"\nTable '{table_name}' not found.")

conn.close()