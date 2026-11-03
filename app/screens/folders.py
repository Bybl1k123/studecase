"""Экран 1: Дерево папок."""
import flet as ft
from app import theme as T
from app.demo_data import DEMO_TREE
from app.widgets.appbar import appbar

def show_folders(page: ft.Page, on_open_folder, on_search, on_review, file_picker):
    def folder_row(node: dict, depth: int = 0) -> list:
        controls = [
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.FOLDER, color=T.FOLDER_COLOR, size=22),
                    ft.Text(node["name"], size=T.FS_BODY, color=T.TEXT_PRIMARY),
                ], spacing=T.PAD_ROW),
                padding=ft.Padding.only(left=T.PAD_SCREEN + depth * 20, right=T.PAD_SCREEN, top=12, bottom=12),
                on_click=lambda e, n=node: on_open_folder(n),
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
        route="/",
        padding=0,
        controls=[
            ft.AppBar(
                title=ft.Text("StudeCase", color=T.TEXT_ON_PRIMARY, size=T.FS_TITLE, weight=ft.FontWeight.W_600),
                bgcolor=T.PRIMARY, elevation=0,
                actions=[
                    ft.IconButton(ft.Icons.SEARCH, icon_color=T.TEXT_ON_PRIMARY, tooltip="Поиск", on_click=lambda e: on_search()),
                    ft.IconButton(ft.Icons.SCHOOL, icon_color=T.TEXT_ON_PRIMARY, tooltip="Повторение", on_click=lambda e: on_review()),
                    # ИСПОЛЬЗУЕМ ACTION ДЛЯ ФАЙЛОВ
                    ft.IconButton(
                        ft.Icons.ADD, 
                        icon_color=T.TEXT_ON_PRIMARY, 
                        tooltip="Добавить файл", 
                        action=ft.PickFiles(file_picker) 
                    ),
                ],
            ),
            ft.Container(
                content=ft.Column(rows, spacing=0, scroll=ft.ScrollMode.AUTO),
                expand=True,
                padding=ft.Padding.only(top=T.GAP),
            ),
        ],
    )
    page.views.clear()
    page.views.append(view)
    page.update()