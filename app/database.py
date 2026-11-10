import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), "studecase.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS folders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            parent_id INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, type TEXT, folder_id INTEGER, preview TEXT,
            tags TEXT, date TEXT, path TEXT, content TEXT
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM folders")
    if cursor.fetchone()[0] == 0:
        default_folders = [
            (1, "Учёба", None),
            (2, "Математика", 1),
            (3, "Геометрия", 1),
            (4, "Алгебра", 1),
            (5, "Личное", None),
            (6, "Идеи", 5),
        ]
        cursor.executemany(
            "INSERT INTO folders (id, name, parent_id) VALUES (?, ?, ?)",
            default_folders
        )
    conn.commit()
    conn.close()

def get_folder_tree_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, parent_id FROM folders ORDER BY id")
    rows = cursor.fetchall()
    conn.close()

    nodes = {}
    for row in rows:
        f_id = row[0]
        f_name = str(row[1])
        nodes[f_id] = {"id": f_id, "name": f_name, "parent_id": row[2], "children": []}

    tree = []
    for row in rows:
        f_id = row[0]
        parent_id = row[2]
        if parent_id is None or parent_id not in nodes:
            tree.append(nodes[f_id])
        else:
            nodes[parent_id]["children"].append(nodes[f_id])
    return tree

def add_folder_db(name: str, parent_id: int = None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO folders (name, parent_id) VALUES (?, ?)",
        (name, parent_id)
    )
    conn.commit()
    conn.close()

def delete_folder_db(folder_id: int) -> list[str]:
    """Удаляет папку, все её подпапки и файлы внутри. Возвращает пути физических файлов для удаления с диска."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    to_delete = [folder_id]
    idx = 0
    while idx < len(to_delete):
        curr = to_delete[idx]
        cursor.execute("SELECT id FROM folders WHERE parent_id = ?", (curr,))
        to_delete.extend([r[0] for r in cursor.fetchall()])
        idx += 1

    placeholders = ",".join("?" for _ in to_delete)
    cursor.execute(f"SELECT path FROM files WHERE folder_id IN ({placeholders})", to_delete)
    file_paths = [r[0] for r in cursor.fetchall() if r[0]]

    cursor.execute(f"DELETE FROM files WHERE folder_id IN ({placeholders})", to_delete)
    cursor.execute(f"DELETE FROM folders WHERE id IN ({placeholders})", to_delete)

    conn.commit()
    conn.close()
    return file_paths

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

def update_file_tags(file_id, tags_list):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    tags_str = ",".join(tags_list) if tags_list else ""
    cursor.execute("UPDATE files SET tags = ? WHERE id = ?", (tags_str, file_id))
    conn.commit()
    conn.close()
