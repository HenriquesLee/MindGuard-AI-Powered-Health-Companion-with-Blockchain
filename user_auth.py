import sqlite3
import hashlib
from db import get_user  # Import get_user from db

# Hash password using SHA256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to create a new user
def register_user(username, password):
    conn = sqlite3.connect('mindguard.db')
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

# Function to authenticate user
def authenticate_user(username, password):
    user = get_user(username)
    if user and user["password"] == hash_password(password):  # Check hashed password
        return True
    return False

# Function to get current user
def get_current_user(username):
    return get_user(username)  # Reuse get_user function
