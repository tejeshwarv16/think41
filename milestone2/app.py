# milestone2/app.py
import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
DATABASE_PATH = '../milestone1/ecommerce.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/products', methods=['GET'])
def get_all_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    offset = (page - 1) * per_page
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Added image_url to the SELECT statement
    cursor.execute("""
        SELECT
            p.id, p.name, p.brand, p.category, p.retail_price, p.image_url,
            d.name AS department_name
        FROM products p
        LEFT JOIN departments d ON p.department_id = d.id
        LIMIT ? OFFSET ?
    """, (per_page, offset))
    
    products_page = cursor.fetchall()
    conn.close()
    products_list = [dict(row) for row in products_page]
    return jsonify(products_list)

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Added image_url to the SELECT statement
    cursor.execute("""
        SELECT
            p.id, p.name, p.brand, p.category, p.retail_price, p.cost, p.sku, p.image_url,
            d.name AS department_name
        FROM products p
        LEFT JOIN departments d ON p.department_id = d.id
        WHERE p.id = ?
    """, (product_id,))
    
    product = cursor.fetchone()
    conn.close()
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(dict(product))

if __name__ == '__main__':
    app.run(debug=True, port=5000)