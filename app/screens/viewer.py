"""Экран 3: Просмотр заметки/файла."""
import flet as ft
from app import theme as T
from app.widgets.appbar import appbar
from app.widgets.chips import tag_chip
from app.services.files_service import open_external_file

def show_viewer(page: ft.Page, file: dict, current_folder: dict, on_back, on_review, on_delete, toast):
    file_path = file.get("path")
    
    if file_path and file.get("type") != "note":
        if open_external_file(file_path):
            return
        else:
            toast("Не удалось открыть файл")
            return

    # Если это заметка, берем её реальное содержимое
    content = file.get("content", "Нет содержимого") if file.get("type") == "note" else f"Этот файл ({file['name']}) не удалось открыть автоматически."

    view = ft.View(
        route="/viewer",
        padding=0,
        controls=[
            appbar(
                file.get("name", "Файл"),
                back=lambda e: on_back(current_folder),
                actions=[
                    ft.IconButton(ft.Icons.REPLAY, icon_color=T.TEXT_ON_PRIMARY, tooltip="Повторить", on_click=lambda e: on_review()),
                ],
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text(f'{file.get("type", "Файл")} · {file.get("date", "")}', size=T.FS_TINY, color=T.TEXT_HINT),
                    ft.Row([tag_chip(t) for t in file.get("tags", [])]),
                    ft.Divider(height=1, color=T.DIVIDER),
                    ft.Text(content, size=T.FS_BODY, color=T.TEXT_PRIMARY, selectable=True),
                ], spacing=T.GAP, scroll=ft.ScrollMode.AUTO),
                expand=True,
                padding=T.PAD_SCREEN,
                bgcolor=T.SURFACE,
                margin=T.PAD_SCREEN,
                border_radius=T.R_CARD,
            ),
            ft.Container(
                content=ft.Row([
                    ft.OutlinedButton(
                        "Удалить", icon=ft.Icons.DELETE_OUTLINE,
                        style=ft.ButtonStyle(color=T.DANGER, shape=ft.RoundedRectangleBorder(radius=T.R_BUTTON)),
                        on_click=lambda e: on_delete(file),
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER),
                padding=T.PAD_SCREEN,
            ),
        ],
    )
    page.views.clear()
    page.views.append(view)
    page.update()