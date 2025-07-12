from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from datetime import datetime
import hashlib

app = Flask(__name__)
app.secret_key = 'vaultify-secret-key-2024'  # Change this in production

# Database setup
def init_db():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            phone TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            original_price REAL NOT NULL,
            description TEXT,
            image_url TEXT,
            category TEXT,
            stock_quantity INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            customer_phone TEXT,
            customer_address TEXT,
            product_id INTEGER,
            quantity INTEGER DEFAULT 1,
            total_amount REAL,
            order_status TEXT DEFAULT 'pending',
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    # Create admin table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Insert default admin if not exists
    cursor.execute('SELECT * FROM admin WHERE username = ?', ('admin',))
    if not cursor.fetchone():
        cursor.execute('INSERT INTO admin (username, password) VALUES (?, ?)', ('admin', 'admin123'))
    
    # Insert premium products if table is empty
    cursor.execute('SELECT COUNT(*) FROM products')
    if cursor.fetchone()[0] == 0:
        premium_products = [
            ('iPhone 15 Pro Max', 1299.99, 999.99, 'Latest iPhone with titanium design and advanced camera system', 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400', 'Electronics', 10),
            ('MacBook Pro M3', 2499.99, 1999.99, 'Professional laptop with M3 chip for ultimate performance', 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400', 'Electronics', 5),
            ('Sony WH-1000XM5', 399.99, 299.99, 'Premium noise-cancelling headphones with exceptional sound', 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400', 'Electronics', 15),
            ('iPad Pro 12.9"', 1099.99, 899.99, 'Professional tablet with M2 chip and Liquid Retina display', 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400', 'Electronics', 8),
            ('Apple Watch Ultra', 799.99, 649.99, 'Premium smartwatch with titanium case and advanced health features', 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400', 'Electronics', 12),
            ('Samsung Galaxy S24 Ultra', 1199.99, 999.99, 'Flagship Android phone with S Pen and advanced AI features', 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400', 'Electronics', 7),
            ('Dell XPS 15', 1899.99, 1499.99, 'Premium laptop with OLED display and powerful performance', 'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=400', 'Electronics', 6),
            ('Bose QuietComfort 45', 349.99, 279.99, 'Premium wireless headphones with world-class noise cancellation', 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400', 'Electronics', 20)
        ]
        cursor.executemany('INSERT INTO products (name, price, original_price, description, image_url, category, stock_quantity) VALUES (?, ?, ?, ?, ?, ?, ?)', premium_products)
    
    conn.commit()
    conn.close()

# Initialize database
init_db()

def get_db_connection():
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def home():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('home.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        phone = request.form.get('phone', '')
        
        conn = get_db_connection()
        
        # Check if username or email already exists
        existing_user = conn.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email)).fetchone()
        if existing_user:
            conn.close()
            flash('Username or email already exists!', 'error')
            return render_template('register.html')
        
        # Hash password and create user
        password_hash = hash_password(password)
        conn.execute('''
            INSERT INTO users (username, email, password_hash, full_name, phone)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, email, password_hash, full_name, phone))
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, username)).fetchone()
        conn.close()
        
        if user and user['password_hash'] == hash_password(password):
            session['user_logged_in'] = True
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['full_name'] = user['full_name']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/order/<int:product_id>', methods=['GET', 'POST'])
def order(product_id):
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        customer_email = request.form['customer_email']
        customer_phone = request.form['customer_phone']
        customer_address = request.form.get('customer_address', '')
        quantity = int(request.form['quantity'])
        
        conn = get_db_connection()
        product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
        
        if product:
            total_amount = product['price'] * quantity
            user_id = session.get('user_id')
            
            conn.execute('''
                INSERT INTO orders (user_id, customer_name, customer_email, customer_phone, customer_address, product_id, quantity, total_amount)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, customer_name, customer_email, customer_phone, customer_address, product_id, quantity, total_amount))
            conn.commit()
            conn.close()
            flash('Order placed successfully! We will process your order and contact you soon.', 'success')
            return redirect(url_for('home'))
        else:
            conn.close()
            flash('Product not found!', 'error')
            return redirect(url_for('home'))
    
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    
    if not product:
        flash('Product not found!', 'error')
        return redirect(url_for('home'))
    
    return render_template('order.html', product=product)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        admin = conn.execute('SELECT * FROM admin WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        
        if admin:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials!', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        flash('Please login as admin first!', 'error')
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products ORDER BY created_at DESC').fetchall()
    orders = conn.execute('''
        SELECT orders.*, products.name as product_name, users.username as user_username
        FROM orders 
        JOIN products ON orders.product_id = products.id 
        LEFT JOIN users ON orders.user_id = users.id
        ORDER BY order_date DESC
    ''').fetchall()
    users = conn.execute('SELECT * FROM users ORDER BY created_at DESC').fetchall()
    conn.close()
    
    return render_template('admin_dashboard.html', products=products, orders=orders, users=users)

@app.route('/admin/add_product', methods=['POST'])
def add_product():
    if not session.get('admin_logged_in'):
        flash('Please login as admin first!', 'error')
        return redirect(url_for('admin_login'))
    
    name = request.form['name']
    price = float(request.form['price'])
    original_price = float(request.form['original_price'])
    description = request.form['description']
    image_url = request.form['image_url']
    category = request.form.get('category', 'Electronics')
    stock_quantity = int(request.form.get('stock_quantity', 0))
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO products (name, price, original_price, description, image_url, category, stock_quantity) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, price, original_price, description, image_url, category, stock_quantity))
    conn.commit()
    conn.close()
    
    flash('Product added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_product/<int:product_id>')
def delete_product(product_id):
    if not session.get('admin_logged_in'):
        flash('Please login as admin first!', 'error')
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()
    
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/profile')
def profile():
    if not session.get('user_logged_in'):
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    user_orders = conn.execute('''
        SELECT orders.*, products.name as product_name 
        FROM orders 
        JOIN products ON orders.product_id = products.id 
        WHERE user_id = ? 
        ORDER BY order_date DESC
    ''', (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('profile.html', user=user, orders=user_orders)

if __name__ == '__main__':
    app.run(debug=True) 