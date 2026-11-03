"""Виджеты карточек и заглушек."""
import flet as ft
from app import theme as T
from app.widgets.chips import tag_chip

def icon_for_type(file_type: str) -> tuple[str, str]:
    return {
        "note":  (ft.Icons.EDIT_NOTE, T.NOTE_COLOR),
        "image": (ft.Icons.IMAGE, T.IMAGE_COLOR),
        "pdf":   (ft.Icons.PICTURE_AS_PDF, T.PDF_COLOR),
        "doc":   (ft.Icons.DESCRIPTION, T.NOTE_COLOR),
    }.get(file_type, (ft.Icons.INSERT_DRIVE_FILE, T.FILE_COLOR))

def file_card(f: dict, on_click, on_delete, on_tag_click) -> ft.Container:
    icon, color = icon_for_type(f["type"])
    
    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(icon, color=color, size=22),
                ft.Text(f["name"], size=T.FS_BODY, color=T.TEXT_PRIMARY, weight=ft.FontWeight.W_500, expand=True),
                # Кнопка добавления тега на карточке
                ft.IconButton(
                    icon=ft.Icons.LOCAL_OFFER_OUTLINED,
                    icon_color=T.TEXT_HINT,
                    icon_size=20,
                    tooltip="Добавить/изменить теги",
                    on_click=lambda e: on_tag_click(f),
                ),
                # Кнопка удаления
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    icon_color=T.TEXT_HINT,
                    icon_size=20,
                    tooltip="Удалить файл",
                    on_click=lambda e: on_delete(f),
                ),
            ], spacing=T.GAP_SM),
            
            ft.Text(f["preview"], size=T.FS_SMALL, color=T.TEXT_SECONDARY, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
            ft.Row(
                [tag_chip(t) for t in f.get("tags", [])] +
                [ft.Text(f["date"], size=T.FS_TINY, color=T.TEXT_HINT)],
                spacing=T.GAP_SM,
                wrap=True # Чтобы теги переносились на новую строку, если их много
            ),
        ], spacing=T.GAP_SM),
        bgcolor=T.SURFACE, border_radius=T.R_CARD, padding=T.PAD_CARD, margin=ft.Margin.only(bottom=T.GAP),
        on_click=on_click, ink=True,
        shadow=ft.BoxShadow(blur_radius=8, color=T.SHADOW_SOFT, offset=ft.Offset(0, 2)),
    )

def empty_state(icon: str, text: str) -> ft.Container:
    return ft.Container(
        content=ft.Column([
            ft.Icon(icon, size=64, color=T.TEXT_HINT),
            ft.Text(text, size=T.FS_BODY, color=T.TEXT_SECONDARY),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=T.GAP),
        alignment=ft.Alignment.CENTER, padding=40,
    )