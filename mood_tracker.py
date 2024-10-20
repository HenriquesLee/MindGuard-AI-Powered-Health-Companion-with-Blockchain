import sqlite3

# Function to save user mood to the database
def save_mood(username, mood):
    conn = sqlite3.connect('mindguard.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO moods (username, mood) VALUES (?, ?)", (username, mood))
    conn.commit()
    conn.close()

# Function to get all moods for a user
def get_user_moods(username):
    conn = sqlite3.connect('mindguard.db')
    cursor = conn.cursor()
    cursor.execute("SELECT mood, timestamp FROM moods WHERE username=?", (username,))
    moods = cursor.fetchall()
    conn.close()
    return moods
