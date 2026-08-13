import sqlite3

def init_database():
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()

    # Drop existing tables if re-running
    cursor.execute("DROP TABLE IF EXISTS order_items")
    cursor.execute("DROP TABLE IF EXISTS orders")
    cursor.execute("DROP TABLE IF EXISTS users")

    # 1. Users table
    cursor.execute("""
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        signup_date TEXT NOT NULL,
        country TEXT NOT NULL
    )
    """)

    # 2. Orders table
    cursor.execute("""
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        total_amount REAL NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    """)

    # 3. Order Items table
    cursor.execute("""
    CREATE TABLE order_items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders (order_id)
    )
    """)

    # Populate Users
    cursor.executemany("""
    INSERT INTO users (name, email, signup_date, country) VALUES (?, ?, ?, ?)
    """, [
        ('George Papadopoulos', 'george@example.com', '2024-01-15', 'Greece'),
        ('Maria Silva', 'maria@example.com', '2024-02-10', 'Portugal'),
        ('John Smith', 'john@example.com', '2024-03-01', 'UK'),
        ('Elena Antoniou', 'elena@example.com', '2024-03-20', 'Greece'),
        ('Alex Johnson', 'alex@example.com', '2024-04-05', 'USA')
    ])

    # Populate Orders
    cursor.executemany("""
    INSERT INTO orders (user_id, order_date, total_amount, status) VALUES (?, ?, ?, ?)
    """, [
        (1, '2024-04-01', 150.00, 'completed'),
        (1, '2024-05-10', 45.00, 'completed'),
        (2, '2024-05-12', 200.00, 'pending'),
        (3, '2024-05-15', 80.00, 'cancelled'),
        (4, '2024-06-01', 120.00, 'completed'),
        (5, '2024-06-15', 310.00, 'completed')
    ])

    # Populate Order Items
    cursor.executemany("""
    INSERT INTO order_items (order_id, product_name, category, price, quantity) VALUES (?, ?, ?, ?, ?)
    """, [
        (1, 'Wireless Mouse', 'Electronics', 25.00, 2),
        (1, 'Mechanical Keyboard', 'Electronics', 100.00, 1),
        (2, 'Coffee Mug', 'Home & Kitchen', 15.00, 3),
        (3, '24-inch Monitor', 'Electronics', 200.00, 1),
        (4, 'Running Shoes', 'Sports', 80.00, 1),
        (5, 'Bluetooth Speaker', 'Electronics', 120.00, 1),
        (6, 'Smart Watch', 'Electronics', 250.00, 1),
        (6, 'Leather Wallet', 'Accessories', 60.00, 1)
    ])

    conn.commit()
    conn.close()
    print("Database 'ecommerce.db' created successfully!")

if __name__ == "__main__":
    init_database()