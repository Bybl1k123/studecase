"""Единый AppBar."""
import flet as ft
from app import theme as T

def appbar(title: str, back=None, actions=None, title_size=None) -> ft.AppBar:
    return ft.AppBar(
        title=ft.Text(title, color=T.TEXT_ON_PRIMARY, size=title_size or T.FS_HEADING,
                      weight=ft.FontWeight.W_600),
        bgcolor=T.PRIMARY,
        color=T.TEXT_ON_PRIMARY,
        elevation=0,
        leading=ft.IconButton(
            ft.Icons.ARROW_BACK, icon_color=T.TEXT_ON_PRIMARY,
            on_click=back,
        ) if back else None,
        actions=actions or [],
    )