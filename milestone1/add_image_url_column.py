# milestone1/add_image_url_column.py
import sqlite3
import urllib.parse

DB_FILE = "ecommerce.db"

def add_and_populate_image_url():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    print("--- Updating database for product images ---")

    try:
        # Step 1: Add the image_url column if it doesn't exist
        cursor.execute("ALTER TABLE products ADD COLUMN image_url TEXT")
        print("1. 'image_url' column added to 'products' table.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("1. Column 'image_url' already exists. Proceeding to populate.")
        else:
            raise e # Re-raise other operational errors

    try:
        # Step 2: Fetch products to generate URLs for them
        cursor.execute("SELECT id, category, name FROM products")
        products = cursor.fetchall()
        print(f"2. Fetched {len(products)} products to update.")

        # Step 3: Loop through products and generate/update image_url
        update_count = 0
        for product in products:
            product_id, category, name = product
            
            # Use safe defaults if name or category is missing (None)
            safe_category = category if category and category.strip() else "product"
            safe_name_part = name.split(' ')[0] if name and name.strip() else "item"
            
            keywords = f"{safe_category},{safe_name_part}"
            encoded_keywords = urllib.parse.quote(keywords)
            image_url = f"https://source.unsplash.com/400x400/?{encoded_keywords}"
            
            cursor.execute("UPDATE products SET image_url = ? WHERE id = ?", (image_url, product_id))
            update_count += 1
        
        print(f"3. Populated 'image_url' for {update_count} products.")
        conn.commit()
        print("\n--- Image URL update completed successfully! ---")

    except Exception as e:
        print(f"\nAn error occurred during population: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    add_and_populate_image_url()