# milestone2/app.py
import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

# --- App Initialization ---
app = Flask(__name__)
# CORS allows your frontend (on a different URL) to access this API
CORS(app)

# --- Database Configuration ---
# The path is relative to where you run the flask app
DATABASE_PATH = '../milestone1/ecommerce.db'

def get_db_connection():
    """Creates a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_PATH)
    # This allows accessing columns by name (e.g., row['name'])
    conn.row_factory = sqlite3.Row
    return conn

# --- API Endpoints ---

@app.route('/api/products', methods=['GET'])
def get_all_products():
    """API endpoint to get a paginated list of all products."""
    # Get page and per_page from query parameters, with default values
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query for the products on the current page
    cursor.execute("SELECT * FROM products LIMIT ? OFFSET ?", (per_page, offset))
    products_page = cursor.fetchall()

    conn.close()
    
    # Convert list of Row objects to a list of dictionaries
    products_list = [dict(row) for row in products_page]
    
    return jsonify(products_list)

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    """API endpoint to get a single product by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    
    conn.close()
    
    # Handle the error case where the product is not found
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    
    return jsonify(dict(product))

# --- Main Execution ---
if __name__ == '__main__':
    # Running on port 5000 in debug mode for development
    app.run(debug=True, port=5000)