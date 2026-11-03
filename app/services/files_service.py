"""Сервис для работы с файлами."""
import os
import platform
import subprocess
import shutil

STORAGE_DIR = os.path.join(os.getcwd(), "uploads")

def open_external_file(file_path: str) -> bool:
    if not file_path or not os.path.exists(file_path): return False
    try:
        if platform.system() == "Windows": os.startfile(file_path)
        elif platform.system() == "Darwin": subprocess.call(("open", file_path))
        else: subprocess.call(("xdg-open", file_path))
        return True
    except Exception: return False

def detect_file_type(filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext in ("png", "jpg", "jpeg", "gif", "webp", "bmp"): return "image"
    if ext == "pdf": return "pdf"
    if ext in ("doc", "docx", "odt", "rtf"): return "doc"
    if ext in ("txt", "md"): return "note"
    return "file"

def human_size(num_bytes: int) -> str:
    if num_bytes < 1024: return f"{num_bytes} Б"
    if num_bytes < 1024 * 1024: return f"{num_bytes / 1024:.1f} КБ"
    return f"{num_bytes / (1024 * 1024):.1f} МБ"

def copy_to_storage(src_path: str) -> str:
    os.makedirs(STORAGE_DIR, exist_ok=True)
    name = os.path.basename(src_path)
    dest = os.path.join(STORAGE_DIR, name)
    base, ext = os.path.splitext(name)
    counter = 1
    while os.path.exists(dest):
        dest = os.path.join(STORAGE_DIR, f"{base}_{counter}{ext}")
        counter += 1
    shutil.copy2(src_path, dest)
    return dest

def delete_stored_file(file_path: str) -> bool:
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
            return True
        except Exception: return False
    return True