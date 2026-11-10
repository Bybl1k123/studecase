"""Экран 2: Список файлов и подпапок в папке."""
import flet as ft
from app import theme as T
from app.widgets.appbar import appbar
from app.widgets.cards import file_card, empty_state
from app.demo_data import DEMO_FILES, DEMO_TREE
from app.widgets.dialogs import show_create_note_dialog

def find_folder_in_tree(nodes: list, target_id: int) -> dict | None:
    for n in nodes:
        if n["id"] == target_id:
            return n
        found = find_folder_in_tree(n.get("children", []), target_id)
        if found:
            return found
    return None

def show_files(
    page: ft.Page, folder: dict, on_back, on_open_folder,
    on_delete_folder, on_view_file, on_delete_file, on_create_note,
    on_create_folder, on_edit_tags, file_picker
):
    folder_id = folder.get("id")
    current_node = find_folder_in_tree(DEMO_TREE, folder_id) or folder
    subfolders = current_node.get("children", [])
    files = [f for f in DEMO_FILES if f.get("folder_id") == folder_id]

    items = []

    # Отображаем вложенные папки с кнопкой удаления
    for sub in subfolders:
        items.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.FOLDER, color=T.FOLDER_COLOR, size=22),
                    ft.Text(sub["name"], size=T.FS_BODY, color=T.TEXT_PRIMARY, weight=ft.FontWeight.W_500, expand=True),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color=T.TEXT_HINT,
                        icon_size=20,
                        tooltip="Удалить подпапку",
                        on_click=lambda e, s=sub: on_delete_folder(s),
                    ),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color=T.TEXT_HINT, size=20),
                ], spacing=T.GAP_SM),
                bgcolor=T.SURFACE,
                border_radius=T.R_CARD,
                padding=T.PAD_CARD,
                margin=ft.Margin.only(bottom=T.GAP),
                on_click=lambda e, s=sub: on_open_folder(s),
                ink=True,
                shadow=ft.BoxShadow(blur_radius=8, color=T.SHADOW_SOFT, offset=ft.Offset(0, 2)),
            )
        )

    # Отображаем файлы
    for f in files:
        items.append(
            file_card(
                f,
                on_click=lambda e, f=f: on_view_file(f),
                on_delete=on_delete_file,
                on_tag_click=on_edit_tags
            )
        )

    if items:
        content = ft.Column(items, scroll=ft.ScrollMode.AUTO, spacing=0)
    else:
        content = empty_state(ft.Icons.FOLDER_OPEN, "В этой папке пока пусто")

    view = ft.View(
        route="/files",
        padding=0,
        controls=[
            appbar(
                folder["name"],
                back=lambda e: on_back(),
                actions=[
                    # Кнопка создания подпапки
                    ft.IconButton(
                        ft.Icons.CREATE_NEW_FOLDER,
                        icon_color=T.TEXT_ON_PRIMARY,
                        tooltip="Создать подпапку",
                        on_click=lambda e: on_create_folder(folder_id)
                    ),
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
                    # Кнопка удаления текущей папки
                    ft.IconButton(
                        ft.Icons.DELETE_OUTLINE,
                        icon_color=T.TEXT_ON_PRIMARY,
                        tooltip="Удалить эту папку",
                        on_click=lambda e: on_delete_folder(current_node)
                    ),
                ],
            ),
            ft.Container(content=content, expand=True, padding=T.PAD_SCREEN),
        ],
    )
    page.views.clear()
    page.views.append(view)
    page.update()
