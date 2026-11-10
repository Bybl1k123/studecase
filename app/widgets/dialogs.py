"""Всплывающие окна."""
import flet as ft
from app import theme as T

def show_create_note_dialog(page: ft.Page, on_save):
    title_field = ft.TextField(label="Название (Тема)", border_radius=T.R_FIELD, autofocus=True)
    content_field = ft.TextField(label="Содержимое (Ответ)", multiline=True, min_lines=3, max_lines=5, border_radius=T.R_FIELD)
    tags_field = ft.TextField(label="Теги (через запятую)", hint_text="математика, формулы", border_radius=T.R_FIELD)

    def close_dialog(e):
        if modal_window in page.overlay:
            page.overlay.remove(modal_window)
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
        if modal_window in page.overlay:
            page.overlay.remove(modal_window)
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

def show_create_folder_dialog(page: ft.Page, folders_tree: list, on_save, default_parent_id: int = None):
    """Окно создания новой папки."""
    name_field = ft.TextField(
        label="Название папки",
        hint_text="Например: Физика",
        border_radius=T.R_FIELD,
        autofocus=True
    )

    options = [ft.dropdown.Option(key="root", text="Корневой уровень (без родителя)")]
    def collect_options(nodes, prefix=""):
        for n in nodes:
            options.append(ft.dropdown.Option(key=str(n["id"]), text=f"{prefix}{n['name']}"))
            collect_options(n.get("children", []), prefix + "— ")
    collect_options(folders_tree)

    parent_dropdown = ft.Dropdown(
        label="Родительская папка",
        value=str(default_parent_id) if default_parent_id is not None else "root",
        options=options,
        border_radius=T.R_FIELD,
    )

    def close_dialog(e):
        if modal_window in page.overlay:
            page.overlay.remove(modal_window)
            page.update()

    def save(e):
        name = name_field.value.strip()
        if not name:
            return
        parent_id = None if parent_dropdown.value == "root" else int(parent_dropdown.value)
        on_save(name, parent_id)
        close_dialog(e)

    modal_window = ft.Container(
        bgcolor="#80000000", expand=True, alignment=ft.Alignment.CENTER,
        content=ft.Container(
            width=400, bgcolor=T.SURFACE, border_radius=T.R_CARD, padding=20,
            content=ft.Column([
                ft.Row([
                    ft.Text("Новая папка", size=T.FS_HEADING, weight=ft.FontWeight.W_600),
                    ft.IconButton(ft.Icons.CLOSE, on_click=close_dialog),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                name_field,
                parent_dropdown,
                ft.Row([
                    ft.FilledButton("Создать", on_click=save, style=ft.ButtonStyle(bgcolor=T.PRIMARY))
                ], alignment=ft.MainAxisAlignment.END)
            ], spacing=15, tight=True)
        )
    )
    page.overlay.append(modal_window)
    page.update()
