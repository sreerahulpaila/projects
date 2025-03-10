import sqlite3

def create_database():
    conn = sqlite3.connect('meal_planner.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY,
            meal_time TEXT,
            date TEXT,
            meal_type TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY,
            name TEXT,
            ingredients TEXT,
            description TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groceries (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL,
            image_path TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY,
            grocery_id INTEGER,
            quantity INTEGER,
            FOREIGN KEY (grocery_id) REFERENCES groceries (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS discounts (
            id INTEGER PRIMARY KEY,
            description TEXT,
            percentage REAL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            product_id INTEGER,
            review TEXT,
            FOREIGN KEY (product_id) REFERENCES groceries (id)
        )
    ''')

    conn.commit()
    conn.close()

create_database()