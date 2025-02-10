import sqlite3
import os

DB_PATH = "/mnt/data/database.db" if os.getenv("STREAMLIT_SERVER") else "database.db"


def create_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
  
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL
    )
    """)
    
   
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        image_path TEXT NOT NULL,
        description TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)
    
    conn.commit()
    conn.close()



def register_user(username, password, age, gender):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO users (username, password, age, gender) VALUES (?, ?, ?, ?)", 
                       (username, password, age, gender))
        conn.commit()
        return True  
    except sqlite3.IntegrityError:
        return False  
    finally:
        conn.close()



def login_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username, age, gender FROM users WHERE username = ? AND password = ?", 
                   (username, password))
    user = cursor.fetchone()
    
    conn.close()
    
    return user  



def insert_history(user_id, image_path, description):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO history (user_id, image_path, description) VALUES (?, ?, ?)", 
                   (user_id, image_path, description))
    
    conn.commit()
    conn.close()


DB_PATH2 = "users.db"
def get_user_age(user_id):
    """Fetch the user's age from the database using their user_id."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Fetch age from users table based on user_id
        cursor.execute("SELECT age FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        
        conn.close()

        if result:  
            return result[0]  # Return the age (first column in result)
        else:
            return None  # No matching user_id found

    except Exception as e:
        print(f"Error fetching user age: {e}")
        return None