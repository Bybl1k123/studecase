"""Всплывающие окна."""
import flet as ft
from app import theme as T

def show_create_note_dialog(page: ft.Page, on_save):
    title_field = ft.TextField(label="Название (Тема)", border_radius=T.R_FIELD, autofocus=True)
    content_field = ft.TextField(label="Содержимое (Ответ)", multiline=True, min_lines=3, max_lines=5, border_radius=T.R_FIELD)
    tags_field = ft.TextField(label="Теги (через запятую)", hint_text="математика, формулы", border_radius=T.R_FIELD)

    def close_dialog(e):
        page.overlay.pop()
        page.update()

    def save(e):
        title = title_field.value.strip()
        content = content_field.value.strip()
        tags_raw = tags_field.value.strip()
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()] if tags_raw else []
        
        if not title or not content:
            return
        on_save(title, content, tags)
        close_dialog(e)

    modal_window = ft.Container(
        bgcolor="#80000000", expand=True, alignment=ft.Alignment.CENTER,
        content=ft.Container(
            width=400, bgcolor=T.SURFACE, border_radius=T.R_CARD, padding=20,
            content=ft.Column([
                ft.Row([
                    ft.Text("Создать заметку", size=T.FS_HEADING, weight=ft.FontWeight.W_600),
                    ft.IconButton(ft.Icons.CLOSE, on_click=close_dialog),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                title_field, content_field, tags_field,
                ft.Row([
                    ft.FilledButton("Создать", on_click=save, style=ft.ButtonStyle(bgcolor=T.PRIMARY))
                ], alignment=ft.MainAxisAlignment.END)
            ], spacing=15, tight=True)
        )
    )
    page.overlay.append(modal_window)
    page.update()

def show_add_tags_dialog(page: ft.Page, file: dict, on_save):
    """Окно для добавления/редактирования тегов у файла."""
    tags_field = ft.TextField(
        label="Теги (через запятую)", 
        value=",".join(file.get("tags", [])),
        hint_text="например: математика, важное",
        border_radius=T.R_FIELD,
        autofocus=True
    )

    def close_dialog(e):
        page.overlay.pop()
        page.update()

    def save(e):
        tags_raw = tags_field.value.strip()
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()] if tags_raw else []
        on_save(file, tags)
        close_dialog(e)

    modal_window = ft.Container(
        bgcolor="#80000000", expand=True, alignment=ft.Alignment.CENTER,
        content=ft.Container(
            width=400, bgcolor=T.SURFACE, border_radius=T.R_CARD, padding=20,
            content=ft.Column([
                ft.Row([
                    ft.Text("Редактировать теги", size=T.FS_HEADING, weight=ft.FontWeight.W_600),
                    ft.IconButton(ft.Icons.CLOSE, on_click=close_dialog),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                tags_field,
                ft.Row([
                    ft.FilledButton("Сохранить", on_click=save, style=ft.ButtonStyle(bgcolor=T.PRIMARY))
                ], alignment=ft.MainAxisAlignment.END)
            ], spacing=15, tight=True)
        )
    )
    page.overlay.append(modal_window)
    page.update()