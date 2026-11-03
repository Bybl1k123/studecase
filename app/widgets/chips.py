"""Виджеты чипов (теги)."""
import flet as ft
from app import theme as T


def tag_chip(text: str) -> ft.Container:
    """Маленький чип тега."""
    return ft.Container(
        content=ft.Text(f"#{text}", size=T.FS_TINY, color=T.TAG_TEXT),
        bgcolor=T.TAG_BG,
        border_radius=T.R_CHIP,
        padding=ft.Padding.symmetric(horizontal=8, vertical=3),
        margin=ft.Margin.only(right=4),
    )