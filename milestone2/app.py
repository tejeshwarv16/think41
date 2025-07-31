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

# --- Existing Product API Endpoints ---

@app.route('/api/products', methods=['GET'])
def get_all_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    offset = (page - 1) * per_page
    conn = get_db_connection()
    cursor = conn.cursor()
    
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

# --- NEW: Department API Endpoints ---

@app.route('/api/departments', methods=['GET'])
def get_all_departments():
    """Endpoint to list all departments with their product counts."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT
            d.id,
            d.name,
            COUNT(p.id) AS product_count
        FROM departments d
        LEFT JOIN products p ON d.id = p.department_id
        GROUP BY d.id, d.name
        ORDER BY d.name
    """)
    
    departments = cursor.fetchall()
    conn.close()
    
    departments_list = [dict(row) for row in departments]
    # Return in the specified format: {"departments": [...]}
    return jsonify({"departments": departments_list})


@app.route('/api/departments/<int:department_id>', methods=['GET'])
def get_department_by_id(department_id):
    """Endpoint to get details for a specific department."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM departments WHERE id = ?", (department_id,))
    department = cursor.fetchone()
    conn.close()
    
    if department is None:
        return jsonify({"error": "Department not found"}), 404
    
    return jsonify(dict(department))


@app.route('/api/departments/<int:department_id>/products', methods=['GET'])
def get_products_by_department(department_id):
    """Endpoint to list all products within a specific department."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # First, check if the department exists and get its name
    cursor.execute("SELECT name FROM departments WHERE id = ?", (department_id,))
    department = cursor.fetchone()
    
    if department is None:
        conn.close()
        return jsonify({"error": "Department not found"}), 404
    
    # If it exists, get all products for that department
    cursor.execute("SELECT * FROM products WHERE department_id = ?", (department_id,))
    products = cursor.fetchall()
    conn.close()
    
    products_list = [dict(row) for row in products]
    
    # Return in the specified format
    return jsonify({
        "department": department['name'],
        "products": products_list
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)