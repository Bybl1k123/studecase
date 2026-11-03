"""Экран 2: Список файлов в папке."""
import flet as ft
from app import theme as T
from app.widgets.appbar import appbar
from app.widgets.cards import file_card, empty_state
from app.demo_data import DEMO_FILES
from app.widgets.dialogs import show_create_note_dialog

def show_files(page: ft.Page, folder: dict, on_back, on_view_file, on_delete_file, on_create_note, on_edit_tags, file_picker):
    folder_id = folder.get("id")
    files = [f for f in DEMO_FILES if f.get("folder_id") == folder_id]

    if files:
        # Передаем on_edit_tags в каждую карточку
        cards = [file_card(f, on_click=lambda e, f=f: on_view_file(f), on_delete=on_delete_file, on_tag_click=on_edit_tags) for f in files]
        content = ft.Column(cards, scroll=ft.ScrollMode.AUTO)
    else:
        content = empty_state(ft.Icons.FOLDER_OPEN, "В этой папке пока нет файлов")

    view = ft.View(
        route="/files",
        padding=0,
        controls=[
            appbar(
                folder["name"],
                back=lambda e: on_back(),
                actions=[
                    # Кнопка создания заметки
                    ft.IconButton(
                        ft.Icons.NOTE_ADD, 
                        icon_color=T.TEXT_ON_PRIMARY, 
                        tooltip="Создать заметку",
                        on_click=lambda e: show_create_note_dialog(page, lambda title, text, tags: on_create_note(folder, title, text, tags))
                    ),
                    # Кнопка загрузки файла с диска
                    ft.IconButton(
                        ft.Icons.ADD, 
                        icon_color=T.TEXT_ON_PRIMARY, 
                        tooltip="Загрузить файл", 
                        action=ft.PickFiles(file_picker)
                    ),
                ],
            ),
            ft.Container(content=content, expand=True, padding=T.PAD_SCREEN),
        ],
    )
    page.views.clear()
    page.views.append(view)
    page.update()