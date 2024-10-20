import sqlite3
import hashlib

# Function to initialize the database
def initialize_db():
    conn = sqlite3.connect('mindguard.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
    ''')
    
    # Create blocks table with encrypted action_data column
    # Create blocks table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS blocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        action_data TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (username) REFERENCES users (username)
    )
    ''')

    # Create moods table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS moods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        mood TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (username) REFERENCES users (username)
    )
    ''')

    # Create posts table without block_id
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (username) REFERENCES users (username)
    )
    ''')

    # Create comments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (post_id) REFERENCES posts(post_id)
    )
    ''')

    # Create likes table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS likes (
        like_id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (post_id) REFERENCES posts(post_id)
    )
    ''')



    conn.commit()
    conn.close()

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to create a new user
def create_user(username, password):
    conn = sqlite3.connect('mindguard.db')
    cursor = conn.cursor()
    
    hashed_password = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        raise Exception("Username already exists.")
    
    conn.close()

# Function to get user details
def get_user(username):
    conn = sqlite3.connect('mindguard.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    
    conn.close()
    if user:
        return {"username": user[0], "password": user[1]}
    return None

# Function to validate user credentials
def authenticate_user(username, password):
    user = get_user(username)
    if user and user["password"] == hash_password(password):
        return True
    return False

# Function to encrypt action data
def encrypt_data(data):
    return hashlib.sha256(data.encode()).hexdigest()

# Function to add a block to the database
def add_block_to_db(username, action_data):
    conn = sqlite3.connect('mindguard.db')
    cursor = conn.cursor()
    
    encrypted_action_data = encrypt_data(action_data)
    cursor.execute("INSERT INTO blocks (username, action_data) VALUES (?, ?)", (username, encrypted_action_data))
    conn.commit()
    
    conn.close()

# Function to get blocks for a specific user
def get_user_blocks(username):
    conn = sqlite3.connect('mindguard.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM blocks WHERE username=?", (username,))
    blocks = cursor.fetchall()
    
    conn.close()

    return [{"id": block[0], "username": block[1], "action_data": block[2], "timestamp": block[3]} for block in blocks]

# Function to get all blocks from the database (Global Blockchain)
def get_all_blocks():
    conn = sqlite3.connect('mindguard.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM blocks")
    blocks = cursor.fetchall()
    
    conn.close()

    return [{"id": block[0], "username": block[1], "action_data": block[2], "timestamp": block[3]} for block in blocks]

# Function to add a mood entry to the database
def add_mood_to_db(username, mood):
    conn = sqlite3.connect('mindguard.db')
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO moods (username, mood) VALUES (?, ?)", (username, mood))
    conn.commit()
    
    conn.close()

# Function to get all moods for a specific user
def get_user_moods(username):
    conn = sqlite3.connect('mindguard.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM moods WHERE username=?", (username,))
    moods = cursor.fetchall()
    
    conn.close()
    return moods

# Function to add a new post
def add_post_block(username, content):
    # First, add the post as a block
    conn = sqlite3.connect('mindguard.db')  # Ensure the correct database file
    cursor = conn.cursor()
    
   
    cursor.execute('''
        INSERT INTO posts (username, content, timestamp)
        VALUES (?, ?, datetime('now'))
    ''', (username, content))   # Pass block_id as part of the insert
    
    conn.commit()
    conn.close()


# Function to fetch all posts, newest first
def get_post_blocks():
    conn = sqlite3.connect('mindguard.db')
    cursor = conn.cursor()
    
    # Join blocks and posts to fetch both the post content and the block details
    cursor.execute('''
        SELECT posts.post_id, posts.username, posts.content, blocks.action_data, posts.timestamp 
        FROM posts
        JOIN blocks ON posts.block_id = blocks.id
        ORDER BY posts.timestamp DESC
    ''')
    
    posts = cursor.fetchall()
    conn.close()

    return [{"block_id": post[0], "username": post[1], "content": post[2], "block_data": post[3], "timestamp": post[4]} for post in posts]

# Function to add a comment to a post
def add_comment(post_id, username, content):
    conn = sqlite3.connect('mindguard.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO comments (post_id, username, content) 
        VALUES (?, ?, ?)
    ''', (post_id, username, content))  # Removed timestamp, it will default to the current time
    conn.commit()
    conn.close()

# Function to fetch comments for a specific post
def get_comments_for_post(post_id):
    conn = sqlite3.connect('mindguard.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comments WHERE post_id = ? ORDER BY timestamp ASC', (post_id,))
    comments = cursor.fetchall()
    conn.close()
    return [{"comment_id": comment[0], "post_id": comment[1], "username": comment[2], "content": comment[3], "timestamp": comment[4]} for comment in comments]

# Function to add a like to a post
def add_like(post_id, username):
    conn = sqlite3.connect('mindguard.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO likes (post_id, username, timestamp)
        VALUES (?, ?, datetime('now'))
    ''', (post_id, username))
    conn.commit()
    conn.close()

# Function to count likes for a post
def count_likes(post_id):
    conn = sqlite3.connect('mindguard.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM likes WHERE post_id = ?', (post_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

# Function to check if a user has already liked a post
def user_has_liked(post_id, username):
    conn = sqlite3.connect('mindguard.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM likes WHERE post_id = ? AND username = ?', (post_id, username))
    has_liked = cursor.fetchone()[0] > 0
    conn.close()
    return has_liked

# Function to fetch all posts, newest first
def get_all_posts():
    conn = sqlite3.connect('mindguard.db')  # Ensure the correct database file
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts ORDER BY timestamp DESC')
    posts = cursor.fetchall()
    conn.close()
    return [{"post_id": post[0], "username": post[1], "content": post[2], "timestamp": post[3]} for post in posts]
