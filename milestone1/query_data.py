# milestone1/query_data.py
import sqlite3

DB_FILE = 'ecommerce.db'

print("--- First 5 Sample Records from 'products' Table ---")
conn = sqlite3.connect(DB_FILE)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Removed the "WHERE category = 'Clothing'" filter
cursor.execute("SELECT id, name, retail_price FROM products LIMIT 5;")
rows = cursor.fetchall()

for row in rows:
    print(f"ID: {row['id']}, Name: {row['name']}, Price: ${row['retail_price']:.2f}")

conn.close()