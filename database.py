import sqlite3

DB_NAME = "promptbot.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        messages INTEGER DEFAULT 0,
        language TEXT DEFAULT 'en'
    )
    """)

try:
    cur.execute("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'en'")
except:
    pass
    
    conn.commit()
    conn.close()


def add_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO users(user_id) VALUES(?)",
        (user_id,)
    )

    conn.commit()
    conn.close()


def increase_messages(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET messages = messages + 1 WHERE user_id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()


def get_stats():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM users")
    users = cur.fetchone()[0]

    cur.execute("SELECT SUM(messages) FROM users")
    messages = cur.fetchone()[0] or 0

    conn.close()

def get_user_language(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "SELECT language FROM users WHERE user_id=?",
        (user_id,)
    )

    result = cur.fetchone()
    conn.close()

    if result and result[0]:
        return result[0]

    return "en"


def set_user_language(user_id, language):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET language=? WHERE user_id=?",
        (language, user_id)
    )

    conn.commit()
    conn.close()
    
    return users, messages


def get_user_language(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "SELECT language FROM users WHERE user_id=?",
        (user_id,)
    )

    result = cur.fetchone()
    conn.close()

    if result:
        return result[0]

    return "en"


def set_user_language(user_id, language):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET language=? WHERE user_id=?",
        (language, user_id)
    )

    conn.commit()
    conn.close()

