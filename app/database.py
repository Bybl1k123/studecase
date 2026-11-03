import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), "studecase.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, type TEXT, folder_id INTEGER, preview TEXT,
            tags TEXT, date TEXT, path TEXT, content TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_all_files():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, type, folder_id, preview, tags, date, path, content FROM files")
    rows = cursor.fetchall()
    conn.close()
    return [{
        "id": r[0], "name": r[1], "type": r[2], "folder_id": r[3],
        "preview": r[4], "tags": r[5].split(",") if r[5] else [],
        "date": r[6], "path": r[7], "content": r[8]
    } for r in rows]

def add_file_db(name, file_type, folder_id, preview, date, path, tags=None, content=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    tags_str = ",".join(tags) if tags else ""
    cursor.execute('''
        INSERT INTO files (name, type, folder_id, preview, tags, date, path, content)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, file_type, folder_id, preview, tags_str, date, path, content))
    conn.commit()
    conn.close()

def delete_file_db(file_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM files WHERE id = ?", (file_id,))
    conn.commit()
    conn.close()

# НОВАЯ ФУНКЦИЯ: обновление тегов
def update_file_tags(file_id, tags_list):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    tags_str = ",".join(tags_list) if tags_list else ""
    cursor.execute("UPDATE files SET tags = ? WHERE id = ?", (tags_str, file_id))
    conn.commit()
    conn.close()