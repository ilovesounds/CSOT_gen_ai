import sqlite3

# Connects to (or creates) your_database.db in the current folder
conn = sqlite3.connect("your_database.db")
cursor = conn.cursor()

# Create a table for chat history
cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Example: Insert a sample chat
cursor.execute("INSERT INTO chat_history (question, answer) VALUES (?, ?)", 
               ("What is chunking?", "Chunking is splitting text into manageable pieces."))

conn.commit()
conn.close()

print("Database and chat_history table created with sample data.")