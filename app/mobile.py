import flet as ft
import os
from datetime import datetime

from app import theme as T
from app.demo_data import DEMO_FILES, DEMO_TREE
from app.services.files_service import copy_to_storage, detect_file_type, human_size, delete_stored_file
from app.database import (
    init_db, get_all_files, add_file_db, delete_file_db,
    update_file_tags, get_folder_tree_db, add_folder_db, delete_folder_db
)
from app.widgets.appbar import appbar
from app.widgets.dialogs import show_create_note_dialog, show_add_tags_dialog, show_create_folder_dialog

from app.screens.folders import show_folders
from app.screens.files import show_files, find_folder_in_tree
from app.screens.viewer import show_viewer
from app.screens.search import show_search
from app.screens.review import show_review

def main(page: ft.Page):
    page.title = "StudeCase"
    page.bgcolor = T.BACKGROUND
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    init_db()
    DEMO_TREE.clear()
    DEMO_TREE.extend(get_folder_tree_db())
    DEMO_FILES.clear()
    DEMO_FILES.extend(get_all_files())

    nav = {"folder": None}

    def toast(text: str):
        page.snack_bar = ft.SnackBar(ft.Text(text))
        page.snack_bar.open = True
        page.update()

    def refresh_home():
        nav["folder"] = None
        show_folders(
            page, open_folder, delete_folder, open_search_menu,
            open_review_menu, open_create_folder_dialog, file_picker
        )

    def create_folder(name: str, parent_id: int = None):
        add_folder_db(name, parent_id)
        DEMO_TREE.clear()
        DEMO_TREE.extend(get_folder_tree_db())
        toast(f"Папка «{name}» создана")
        if nav["folder"]:
            open_folder(nav["folder"])
        else:
            refresh_home()

    def delete_folder(folder: dict):
        if not folder:
            return
        folder_id = folder["id"]
        parent_id = folder.get("parent_id")
        
        paths = delete_folder_db(folder_id)
        for p in paths:
            delete_stored_file(p)
            
        DEMO_TREE.clear()
        DEMO_TREE.extend(get_folder_tree_db())
        DEMO_FILES.clear()
        DEMO_FILES.extend(get_all_files())
        toast(f"Папка «{folder['name']}» удалена")

        # Если удалили папку, внутри которой сейчас находимся — выходим в родителя или домой
        if nav["folder"] and nav["folder"]["id"] == folder_id:
            parent_node = find_folder_in_tree(DEMO_TREE, parent_id) if parent_id else None
            if parent_node:
                open_folder(parent_node)
            else:
                refresh_home()
        elif nav["folder"]:
            open_folder(nav["folder"])
        else:
            refresh_home()

    def open_create_folder_dialog(default_parent_id: int = None):
        show_create_folder_dialog(page, DEMO_TREE, create_folder, default_parent_id=default_parent_id)

    def handle_files_selected(e: ft.FilePickerResultEvent):
        if not e.files: return
        target_folder = nav["folder"] or (DEMO_TREE[0] if DEMO_TREE else None)
        if not target_folder:
            toast("Сначала создайте папку")
            return
        added_count = 0
        
        for f in e.files:
            file_type = detect_file_type(f.name)
            new_path = None
            size = f.size or 0
            if f.path:
                try:
                    new_path = copy_to_storage(f.path)
                    size = os.path.getsize(new_path)
                except Exception as ex:
                    print(f"Ошибка: {ex}")
                    continue

            add_file_db(
                name=f.name, file_type=file_type, folder_id=target_folder.get("id"),
                preview=f"{f.name.rsplit('.', 1)[-1].upper()} · {human_size(size)}",
                date=datetime.now().strftime("%Y-%m-%d"), path=new_path
            )
            added_count += 1
            
        if added_count > 0:
            toast(f"Добавлено файлов: {added_count}")
            DEMO_FILES.clear(); DEMO_FILES.extend(get_all_files())
            open_folder(target_folder)

    file_picker = ft.FilePicker(on_result=handle_files_selected)
    page.services.append(file_picker)

    def create_note(folder: dict, title: str, content: str, tags: list):
        add_file_db(
            name=title, file_type="note", folder_id=folder.get("id"),
            preview=content[:40] + "..." if len(content) > 40 else content,
            date=datetime.now().strftime("%Y-%m-%d"), path=None, tags=tags, content=content
        )
        toast("Заметка создана")
        DEMO_FILES.clear(); DEMO_FILES.extend(get_all_files())
        open_folder(folder)

    def edit_tags(file: dict, new_tags: list):
        update_file_tags(file["id"], new_tags)
        toast("Теги обновлены")
        DEMO_FILES.clear(); DEMO_FILES.extend(get_all_files())
        
        if page.views and page.views[-1].route == "/search":
            open_search_menu()
        else:
            open_folder(nav["folder"] or DEMO_TREE[0])

    def delete_file(file: dict = None, folder_id: int = None):
        if file:
            if file.get("path"): delete_stored_file(file["path"])
            delete_file_db(file["id"])
            msg = "Файл удален"
        else: msg = "Ошибка"
        toast(msg)
        DEMO_FILES.clear(); DEMO_FILES.extend(get_all_files())
        
        if page.views and page.views[-1].route == "/search":
            open_search_menu()
        elif nav["folder"]:
            open_folder(nav["folder"])
        else:
            refresh_home()

    def open_folder(folder: dict):
        nav["folder"] = folder
        parent_id = folder.get("parent_id")
        parent_node = find_folder_in_tree(DEMO_TREE, parent_id) if parent_id else None
        go_back = (lambda: open_folder(parent_node)) if parent_node else refresh_home

        show_files(
            page, folder,
            on_back=go_back,
            on_open_folder=open_folder,
            on_delete_folder=delete_folder,
            on_view_file=lambda f: open_viewer(f),
            on_delete_file=delete_file,
            on_create_note=create_note,
            on_create_folder=open_create_folder_dialog,
            on_edit_tags=lambda f: show_add_tags_dialog(page, f, edit_tags),
            file_picker=file_picker
        )

    def open_viewer(file: dict):
        show_viewer(
            page, file, nav["folder"],
            on_back=lambda folder: open_folder(folder) if folder else refresh_home(),
            on_review=lambda: open_review_menu(),
            on_delete=delete_file,
            toast=toast
        )

    def open_search_menu():
        show_search(
            page,
            on_back=refresh_home,
            on_view_file=lambda f: open_viewer(f),
            on_delete_file=delete_file,
            on_edit_tags=lambda f: show_add_tags_dialog(page, f, edit_tags)
        )

    def open_review_menu():
        def folder_row(node: dict, depth: int = 0) -> list:
            controls = [
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.FOLDER, color=T.FOLDER_COLOR, size=22),
                        ft.Text(node["name"], size=T.FS_BODY, color=T.TEXT_PRIMARY),
                    ], spacing=T.PAD_ROW),
                    padding=ft.Padding.only(left=T.PAD_SCREEN + depth * 20, right=T.PAD_SCREEN, top=12, bottom=12),
                    on_click=lambda e, n=node: open_review(n),
                    ink=True,
                ),
                ft.Divider(height=1, color=T.DIVIDER, thickness=0.5),
            ]
            for child in node.get("children", []):
                controls.extend(folder_row(child, depth + 1))
            return controls

        rows = []
        for node in DEMO_TREE:
            rows.extend(folder_row(node))

        view = ft.View(
            route="/review_menu", padding=0,
            controls=[
                appbar("Выберите папку для повторения", back=lambda e: refresh_home()),
                ft.Container(content=ft.Column(rows, spacing=0, scroll=ft.ScrollMode.AUTO), expand=True, padding=ft.Padding.only(top=T.GAP)),
            ],
        )
        page.views.clear()
        page.views.append(view)
        page.update()

    def open_review(folder: dict):
        show_review(page, folder, on_back=open_review_menu)

    refresh_home()

if __name__ == "__main__":
    ft.run(main)
