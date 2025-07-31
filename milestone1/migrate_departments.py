# milestone1/migrate_departments.py
import sqlite3
import pandas as pd

DB_FILE = "ecommerce.db"

def migrate():
    """
    Refactors the database to move departments into a separate table.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    print("--- Starting Database Migration ---")

    try:
        # Step 1: Create the new 'departments' table
        print("1. Creating 'departments' table...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        """)
        print("   'departments' table created successfully.")

        # Step 2 & 3: Extract unique departments and populate the table
        print("2. Populating 'departments' table...")
        products_df = pd.read_sql_query("SELECT DISTINCT department FROM products", conn)
        departments_df = pd.DataFrame({'name': products_df['department'].unique()})
        departments_df.to_sql('departments', conn, if_exists='append', index=False)
        print(f"   {len(departments_df)} unique departments added.")
        
        # Step 4: Update the 'products' table
        print("3. Refactoring 'products' table...")
        # Add the new department_id column
        cursor.execute("ALTER TABLE products ADD COLUMN department_id INTEGER REFERENCES departments(id)")
        
        # Populate the new department_id foreign key column
        cursor.execute("""
        UPDATE products
        SET department_id = (SELECT id FROM departments WHERE departments.name = products.department)
        """)
        print("   'products.department_id' populated.")

        # Step 4 (cont.): Recreate the products table to drop the old column
        # This is the standard "safe" way to drop a column in SQLite
        print("4. Recreating 'products' table to finalize structure...")
        cursor.execute("""
        CREATE TABLE products_new (
            id INTEGER,
            cost REAL,
            category TEXT,
            name TEXT,
            brand TEXT,
            retail_price REAL,
            sku TEXT,
            distribution_center_id INTEGER,
            department_id INTEGER,
            PRIMARY KEY(id),
            FOREIGN KEY(department_id) REFERENCES departments(id)
        )
        """)
        cursor.execute("""
        INSERT INTO products_new (id, cost, category, name, brand, retail_price, sku, distribution_center_id, department_id)
        SELECT id, cost, category, name, brand, retail_price, sku, distribution_center_id, department_id
        FROM products
        """)
        cursor.execute("DROP TABLE products")
        cursor.execute("ALTER TABLE products_new RENAME TO products")
        print("   'products' table successfully recreated without old 'department' column.")

        conn.commit()
        print("\n--- Migration Completed Successfully! ---")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()