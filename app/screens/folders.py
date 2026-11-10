"""Экран 1: Корневые папки."""
import flet as ft
from app import theme as T
from app.demo_data import DEMO_TREE
from app.widgets.cards import empty_state

def show_folders(page: ft.Page, on_open_folder, on_delete_folder, on_search, on_review, on_create_folder, file_picker):
    rows = []
    for node in DEMO_TREE:
        rows.extend([
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.FOLDER, color=T.FOLDER_COLOR, size=22),
                    ft.Text(node["name"], size=T.FS_BODY, color=T.TEXT_PRIMARY, expand=True),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color=T.TEXT_HINT,
                        icon_size=20,
                        tooltip="Удалить папку",
                        on_click=lambda e, n=node: on_delete_folder(n),
                    ),
                ], spacing=T.PAD_ROW),
                padding=ft.Padding.only(left=T.PAD_SCREEN, right=T.PAD_SCREEN, top=8, bottom=8),
                on_click=lambda e, n=node: on_open_folder(n),
                ink=True,
            ),
            ft.Divider(height=1, color=T.DIVIDER, thickness=0.5),
        ])

    content = ft.Column(rows, spacing=0, scroll=ft.ScrollMode.AUTO) if rows else empty_state(ft.Icons.FOLDER_OPEN, "Папок пока нет")

    view = ft.View(
        route="/",
        padding=0,
        controls=[
            ft.AppBar(
                title=ft.Text("StudeCase", color=T.TEXT_ON_PRIMARY, size=T.FS_TITLE, weight=ft.FontWeight.W_600),
                bgcolor=T.PRIMARY, elevation=0,
                actions=[
                    ft.IconButton(ft.Icons.SEARCH, icon_color=T.TEXT_ON_PRIMARY, tooltip="Поиск", on_click=lambda e: on_search()),
                    ft.IconButton(ft.Icons.SCHOOL, icon_color=T.TEXT_ON_PRIMARY, tooltip="Повторение", on_click=lambda e: on_review()),
                    ft.IconButton(
                        ft.Icons.CREATE_NEW_FOLDER,
                        icon_color=T.TEXT_ON_PRIMARY,
                        tooltip="Создать папку",
                        on_click=lambda e: on_create_folder(),
                    ),
                    ft.IconButton(
                        ft.Icons.ADD, 
                        icon_color=T.TEXT_ON_PRIMARY, 
                        tooltip="Добавить файл", 
                        action=ft.PickFiles(file_picker) 
                    ),
                ],
            ),
            ft.Container(
                content=content,
                expand=True,
                padding=ft.Padding.only(top=T.GAP),
            ),
        ],
    )
    page.views.clear()
    page.views.append(view)
    page.update()
