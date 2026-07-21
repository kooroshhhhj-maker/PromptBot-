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
        language TEXT DEFAULT 'en',
        image_size TEXT DEFAULT '1024x1024',
        image_style TEXT DEFAULT 'realistic'
    )
    """)

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

def get_image_settings(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "SELECT image_size, image_style FROM users WHERE user_id=?",
        (user_id,)
    )

    result = cur.fetchone()
    conn.close()

    if result:
        return result[0], result[1]

    return "1024x1024", "realistic"


def set_image_size(user_id, size):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET image_size=? WHERE user_id=?",
        (size, user_id)
    )

    conn.commit()
    conn.close()


def set_image_style(user_id, style):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET image_style=? WHERE user_id=?",
        (style, user_id)
    )

    conn.commit()
    conn.close()

def get_image_settings(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "SELECT image_size, image_style FROM users WHERE user_id=?",
        (user_id,)
    )

    result = cur.fetchone()
    conn.close()

    if result:
        return result[0], result[1]

    return "1024x1024", "realistic"


def set_image_size(user_id, size):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET image_size=? WHERE user_id=?",
        (size, user_id)
    )

    conn.commit()
    conn.close()


def set_image_style(user_id, style):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET image_style=? WHERE user_id=?",
        (style, user_id)
    )

    conn.commit()
    conn.close()

