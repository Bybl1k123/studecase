import flet as ft
import os
from datetime import datetime

from app import theme as T
from app.demo_data import DEMO_FILES, DEMO_TREE
from app.services.files_service import copy_to_storage, detect_file_type, human_size, delete_stored_file
from app.database import init_db, get_all_files, add_file_db, delete_file_db, update_file_tags
from app.widgets.appbar import appbar
from app.widgets.dialogs import show_create_note_dialog, show_add_tags_dialog

from app.screens.folders import show_folders
from app.screens.files import show_files
from app.screens.viewer import show_viewer
from app.screens.search import show_search
from app.screens.review import show_review

def main(page: ft.Page):
    page.title = "StudeCase"
    page.bgcolor = T.BACKGROUND
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    init_db()
    DEMO_FILES.clear()
    DEMO_FILES.extend(get_all_files())

    nav = {"folder": None}

    def toast(text: str):
        page.snack_bar = ft.SnackBar(ft.Text(text))
        page.snack_bar.open = True
        page.update()

    def handle_files_selected(e: ft.FilePickerResultEvent):
        if not e.files: return
        target_folder = nav["folder"] or DEMO_TREE[0]
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

    # ИСПРАВЛЕННАЯ ФУНКЦИЯ РЕДАКТИРОВАНИЯ ТЕГОВ
    def edit_tags(file: dict, new_tags: list):
        update_file_tags(file["id"], new_tags)
        toast("Теги обновлены")
        DEMO_FILES.clear(); DEMO_FILES.extend(get_all_files())
        
        # Если мы находимся в поиске (текущий экран search), обновляем поиск
        if page.views and page.views[-1].route == "/search":
            open_search_menu()
        else:
            # Иначе возвращаемся в текущую папку
            open_folder(nav["folder"] or {"id": 2, "name": "Математика"})

    def delete_file(file: dict = None, folder_id: int = None):
        if file:
            if file.get("path"): delete_stored_file(file["path"])
            delete_file_db(file["id"])
            msg = "Файл удален"
        else: msg = "Ошибка"
        toast(msg)
        DEMO_FILES.clear(); DEMO_FILES.extend(get_all_files())
        
        # Аналогично: если мы в поиске, обновляем поиск
        if page.views and page.views[-1].route == "/search":
            open_search_menu()
        else:
            open_folder(nav["folder"] or {"id": 2, "name": "Математика"})

    def open_folder(folder: dict):
        nav["folder"] = folder
        show_files(
            page, folder,
            on_back=lambda: show_folders(page, open_folder, open_search_menu, open_review_menu, file_picker),
            on_view_file=lambda f: open_viewer(f),
            on_delete_file=delete_file,
            on_create_note=create_note,
            on_edit_tags=lambda f: show_add_tags_dialog(page, f, edit_tags),
            file_picker=file_picker
        )

    def open_viewer(file: dict):
        show_viewer(
            page, file, nav["folder"],
            on_back=lambda folder: open_folder(folder),
            on_review=lambda: open_review_menu(),
            on_delete=delete_file,
            toast=toast
        )

    def open_search_menu():
        show_search(
            page,
            on_back=lambda: show_folders(page, open_folder, open_search_menu, open_review_menu, file_picker),
            on_view_file=lambda f: open_viewer(f),
            on_delete_file=delete_file,
            on_edit_tags=lambda f: show_add_tags_dialog(page, f, edit_tags) # Передаем в поиск
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
                appbar("Выберите папку для повторения", back=lambda e: show_folders(page, open_folder, open_search_menu, open_review_menu, file_picker)),
                ft.Container(content=ft.Column(rows, spacing=0, scroll=ft.ScrollMode.AUTO), expand=True, padding=ft.Padding.only(top=T.GAP)),
            ],
        )
        page.views.clear()
        page.views.append(view)
        page.update()

    def open_review(folder: dict):
        show_review(page, folder, on_back=open_review_menu)

    show_folders(page, open_folder, open_search_menu, open_review_menu, file_picker=file_picker)

if __name__ == "__main__":
    ft.run(main)