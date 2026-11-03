"""Экран 4: Поиск."""
import flet as ft
from app import theme as T
from app.widgets.appbar import appbar
from app.widgets.cards import file_card, empty_state
from app.demo_data import DEMO_FILES

def show_search(page: ft.Page, on_back, on_view_file, on_delete_file, on_edit_tags):
    state = {"active_tag": None, "query": ""}
    results_col = ft.Column(spacing=T.GAP)

    # Собираем уникальные теги из всех файлов
    def get_all_unique_tags():
        all_tags = set()
        for f in DEMO_FILES:
            for t in f.get("tags", []):
                all_tags.add(t)
        return sorted(list(all_tags))

    def filtered_files():
        result = DEMO_FILES
        if state["active_tag"]:
            result = [f for f in result if state["active_tag"] in f.get("tags", [])]
        q = state["query"].strip().lower()
        if q:
            result = [f for f in result if q in f["name"].lower()]
        return result

    def render_results():
        results_col.controls.clear()
        matches = filtered_files()
        if not matches:
            results_col.controls.append(empty_state(ft.Icons.SEARCH_OFF, "Ничего не найдено"))
        else:
            for f in matches:
                results_col.controls.append(
                    file_card(f, on_click=lambda e, f=f: on_view_file(f), on_delete=on_delete_file, on_tag_click=on_edit_tags)
                )
        found_label.value = f"Найдено: {len(matches)}"
        page.update()

    found_label = ft.Text("Найдено: 0", size=T.FS_SMALL, color=T.TEXT_SECONDARY)
    chips_row = ft.Row(scroll=ft.ScrollMode.AUTO, spacing=T.GAP_SM)

    def make_chip(tag: str) -> ft.Container:
        active = state["active_tag"] == tag
        return ft.Container(
            content=ft.Text(f"#{tag}", size=T.FS_SMALL, color=T.TEXT_ON_PRIMARY if active else T.TAG_TEXT),
            bgcolor=T.PRIMARY if active else T.TAG_BG,
            border_radius=T.R_CHIP,
            padding=ft.Padding.symmetric(horizontal=12, vertical=6),
            on_click=lambda e, t=tag: toggle_tag(t),
            ink=True,
        )

    def toggle_tag(tag: str):
        state["active_tag"] = None if state["active_tag"] == tag else tag
        update_chips()
        render_results()

    def update_chips():
        tags = get_all_unique_tags()
        chips_row.controls = [make_chip(t) for t in tags]
        page.update()

    def on_search_change(e):
        state["query"] = e.control.value
        render_results()

    view = ft.View(
        route="/search",
        padding=0,
        controls=[
            appbar("Поиск", back=lambda e: on_back()),
            ft.Container(
                content=ft.Column([
                    ft.TextField(
                        hint_text="Введите запрос...", prefix_icon=ft.Icons.SEARCH,
                        border_radius=T.R_FIELD, bgcolor=T.SURFACE,
                        border_color=T.DIVIDER, focused_border_color=T.PRIMARY,
                        on_change=on_search_change,
                    ),
                    chips_row,
                    found_label,
                    results_col,
                ], spacing=T.GAP, scroll=ft.ScrollMode.AUTO),
                expand=True,
                padding=T.PAD_SCREEN,
            ),
        ],
    )
    page.views.clear()
    page.views.append(view)
    page.update()
    
    # При запуске обновляем список тегов и результаты
    update_chips()
    render_results()