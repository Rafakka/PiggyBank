
import sqlite3

from flask import jsonify

def init_db():
    """Initialize the database and create tables"""
    conn = sqlite3.connect('piggybank.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            balance REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def create_user(username, name, initial_balance):
    """Create a new user with initial balance"""
    try:
        conn = sqlite3.connect('piggybank.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO users (username, name, balance) VALUES (?, ?, ?)",
            (username, name, initial_balance)
        )
        
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        print(f"User {username} created successfully with ID: {user_id}")
        return user_id
        
    except sqlite3.IntegrityError:
        print("Error: Username already exists!")
        return None
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

def get_user_by_username(username):
    """Get user by username and return as dictionary"""
    try:
        conn = sqlite3.connect('piggybank.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            user_dict = {
                'id': user['id'],
                'username': user['username'],
                'name': user['name'],
                'balance': user['balance']
            }
            return user_dict
        else:
            return None
            
    except Exception as e:
        print(f"Error finding user: {e}")
        return None

def get_all_users():
        conn = sqlite3.connect('piggybank.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        users = [
             {
                "user.id":r[0],
                "username":r[1],
                "name":r[2],
                "balance":r[3]
            } for r in rows
        ]
        return users

def update_balance(username, amount):
    """Update user's balance (positive for deposit, negative for withdrawal)"""
    try:
        conn = sqlite3.connect('piggybank.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE users SET balance = balance + ? WHERE username = ?",
            (amount, username)
        )
        
        conn.commit()
        conn.close()
        
        print(f"Balance updated by: ${amount:.2f}")
        return True
        
    except Exception as e:
        print(f"Error updating balance: {e}")
        return False

def delete_user(username):
    try:
            conn = sqlite3.connect('piggybank.db')
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM users WHERE username = ?",
                (username,))
            conn.commit()
            conn.close()
            return True        
    except Exception as e:
            print(f"Error deleting user: {e}")
            return False

def clean_wipe_user_db():
    try:
            conn = sqlite3.connect('piggybank.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='users'")
            conn.commit()
            conn.close()
            return True
    except Exception as e:
            print(f"Error: {e}")
            return False