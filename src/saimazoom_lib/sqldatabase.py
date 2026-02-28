import sqlite3
import os
import json

DATABASE_NAME = "data/saimazoom.db"

def create_connection():
    if not os.path.exists("data"):
        os.makedirs("data")
    return sqlite3.connect(DATABASE_NAME)

def create_table_clients():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_client(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO clients (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def find_client(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM clients WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return False
    return (row[0] == password)


def create_table_orders():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id TEXT PRIMARY KEY,
            client_username TEXT NOT NULL,
            products_json TEXT NOT NULL,
            status TEXT NOT NULL,
            total REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_order(order_id, client_username, products, status="Solicitado"):

    conn = create_connection()
    cursor = conn.cursor()
    products_str = json.dumps(products, ensure_ascii=False)
    total = sum(p.get("precio", 0) for p in products)

    try:
        cursor.execute("""
            INSERT INTO orders (id, client_username, products_json, status, total)
            VALUES (?, ?, ?, ?, ?)
        """, (order_id, client_username, products_str, status, total))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def get_orders_by_client(client_username):

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, products_json, status, total FROM orders WHERE client_username = ?", (client_username,))
    rows = cursor.fetchall()
    conn.close()

    pedidos = []
    for row in rows:
        pedidos.append({
            "pedido_id": row[0],
            "productos": json.loads(row[1]),
            "estado": row[2],
            "total": row[3]
        })
    return pedidos

def update_order_status(order_id, new_status):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
    changed = (cursor.rowcount > 0)
    conn.commit()
    conn.close()
    return changed

def get_order_status(order_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM orders WHERE id = ?", (order_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    return row[0]
