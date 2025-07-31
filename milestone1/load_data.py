# D:\project\think41\milestone1\load_data.py
import sqlite3
import pandas as pd
import os
from datetime import datetime

# --- Configuration ---
DB_FILE = 'ecommerce.db'
CSV_DIR = os.path.join('..', 'ecommerce-dataset-main', 'ecommerce-dataset-main', 'archive', 'archive')
REPORT_FILE = 'verification_report.md' # The name of our output file
CSV_FILES = [
    'users.csv',
    'products.csv',
    'distribution_centers.csv',
    'inventory_items.csv',
    'orders.csv',
    'order_items.csv'
]

def load_data():
    """
    Loads data from multiple CSV files into separate tables in an SQLite database.
    (This function remains the same)
    """
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    print("Database 'ecommerce.db' created.")

    for file_name in CSV_FILES:
        try:
            csv_path = os.path.join(CSV_DIR, file_name)
            df = pd.read_csv(csv_path)
            table_name = os.path.splitext(file_name)[0]
            df.to_sql(table_name, conn, index=False, if_exists='replace')
            print(f"  - Loaded '{file_name}' into '{table_name}' table.")
        except Exception as e:
            print(f"  - ERROR processing {file_name}: {e}")
            
    conn.close()
    print("Data loading complete.")

def verify_data():
    """
    Verifies the data and saves the results to a Markdown file.
    """
    if not os.path.exists(DB_FILE):
        print(f"Database file '{DB_FILE}' not found. Cannot verify.")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # --- Generate Report Content ---
    report_content = []
    report_content.append("# Database Verification Report\n")
    # Using 'Asia/Kolkata' for IST.
    report_content.append(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}\n\n")
    
    # Create the Markdown table header
    report_content.append("| Table Name               | Row Count |\n")
    report_content.append("|--------------------------|-----------|\n")

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    for table_name_tuple in tables:
        table_name = table_name_tuple[0]
        cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')
        count = cursor.fetchone()[0]
        # Add a row to our Markdown table
        report_content.append(f"| {table_name:<24} | {count:<9} |\n")
        
    conn.close()

    # --- Write to File and Print to Console ---
    try:
        with open(REPORT_FILE, 'w') as f:
            f.writelines(report_content)
        print(f"\nVerification complete. Report saved to '{REPORT_FILE}'")
        
        print("\n--- Verification Summary ---")
        for line in report_content:
            print(line.strip())

    except IOError as e:
        print(f"\nError writing report to file: {e}")

if __name__ == '__main__':
    print("--- Starting Data Loading Process ---")
    load_data()
    verify_data()
    print("\n--- Process Complete! ---")