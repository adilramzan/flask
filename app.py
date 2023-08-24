from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

def create_tables():
    conn = sqlite3.connect('cake_store.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS carts (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            item_name TEXT NOT NULL,
            item_price REAL NOT NULL,
            item_description TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_user(username, password, first_name, last_name, email, address):
    conn = sqlite3.connect('cake_store.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (username, password, first_name, last_name, email, address)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (username, password, first_name, last_name, email, address))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = sqlite3.connect('cake_store.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user

def create_cart(username):
    conn = sqlite3.connect('cake_store.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS carts (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            item_name TEXT NOT NULL,
            item_price REAL NOT NULL,
            item_description TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_item_to_cart(username, item_name, item_price, item_description):
    conn = sqlite3.connect('cake_store.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO carts (username, item_name, item_price, item_description)
        VALUES (?, ?, ?, ?)
    ''', (username, item_name, item_price, item_description))
    conn.commit()
    conn.close()

create_tables()

@app.route('/')
def main_menu():
    return render_template('main_menu.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = get_user_by_username(username)
        if user and user[2] == password:
            print(f"Login successful:\nUsername: {username}\nPassword: {password}")
            return redirect('/')
        else:
            error_message = "Invalid credentials. Please try again."
            return render_template('login.html', error_message=error_message)
    
    return render_template('login.html')

@app.route('/add_to_cart/<item_id>')
def add_to_cart(item_id):
    # Get item details based on item_id (you can modify this based on your item management)
    item_name = "Example Cake"
    item_price = 10.99
    item_description = "A delicious example cake."

    # Replace with the actual logged-in user's username
    username = "example_user"

    create_cart(username)
    insert_item_to_cart(username, item_name, item_price, item_description)
    return redirect(url_for('main_menu'))

if __name__ == '__main__':
    app.run(debug=True)
