"""Экран 5: Повторение."""
import flet as ft
from app import theme as T
from app.widgets.appbar import appbar
from app.demo_data import DEMO_FILES

def show_review(page: ft.Page, folder: dict, on_back):
    notes = [f for f in DEMO_FILES if f.get("folder_id") == folder.get("id") and f.get("type") == "note"]
    idx = {"i": 0}
    total = len(notes)

    if total == 0:
        view = ft.View(
            route="/review",
            padding=0,
            controls=[
                appbar("Повторение", back=lambda e: on_back()),
                ft.Container(content=ft.Text("В этой папке нет заметок для повторения.", size=T.FS_BODY), alignment=ft.Alignment.CENTER, expand=True)
            ]
        )
        page.views.clear()
        page.views.append(view)
        page.update()
        return

    progress = ft.ProgressBar(value=0, color=T.PRIMARY, bgcolor=T.DIVIDER, bar_height=4)
    counter = ft.Text(f"1 / {total}", size=T.FS_SMALL, color=T.TEXT_ON_PRIMARY)
    card_title = ft.Text("", size=T.FS_TITLE, weight=ft.FontWeight.W_600, color=T.TEXT_PRIMARY, text_align=ft.TextAlign.CENTER)
    
    answer_text = ft.Text("", size=T.FS_BODY, color=T.TEXT_PRIMARY, text_align=ft.TextAlign.CENTER)
    answer_box = ft.Container(content=answer_text, visible=False, padding=T.PAD_CARD)
    
    show_answer_btn = ft.FilledButton(
        "Показать ответ", style=ft.ButtonStyle(bgcolor=T.PRIMARY, color=T.TEXT_ON_PRIMARY, shape=ft.RoundedRectangleBorder(radius=T.R_BUTTON)),
        on_click=lambda e: show_answer(),
    )
    
    quality_row = ft.Row([
        ft.Button(
            str(i), width=48, height=48, style=ft.ButtonStyle(bgcolor=T.SURFACE_ALT, color=T.TEXT_PRIMARY, shape=ft.RoundedRectangleBorder(radius=T.R_BUTTON)),
            on_click=lambda e, q=i: answer(q),
        ) for i in range(6)
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)
    
    quality_labels = ft.Row([
        ft.Text("забыл", size=T.FS_TINY, color=T.TEXT_HINT),
        ft.Text("легко", size=T.FS_TINY, color=T.TEXT_HINT),
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def render_current():
        if idx["i"] >= total:
            card_title.value = "🎉 Всё повторено!"
            answer_box.visible = False
            show_answer_btn.visible = False
            quality_row.visible = False
            quality_labels.visible = False
            progress.value = 1
            counter.value = f"{total} / {total}"
            page.update()
            return
        
        item = notes[idx["i"]]
        card_title.value = item["name"]
        answer_text.value = item.get("content", "Нет содержимого")
        answer_box.visible = False
        show_answer_btn.visible = True
        quality_row.visible = True
        quality_labels.visible = True
        counter.value = f'{idx["i"] + 1} / {total}'
        progress.value = idx["i"] / total
        page.update()

    def show_answer():
        answer_box.visible = True
        page.update()

    def answer(quality: int):
        idx["i"] += 1
        render_current()

    view = ft.View(
        route="/review",
        padding=0,
        controls=[
            appbar("Повторение", back=lambda e: on_back(), actions=[ft.Container(content=counter, padding=ft.Padding.only(right=16))]),
            progress,
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Column([card_title, answer_box, show_answer_btn], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=T.GAP),
                        bgcolor=T.SURFACE, border_radius=T.R_CARD, padding=24, margin=ft.Margin.symmetric(vertical=40),
                        shadow=ft.BoxShadow(blur_radius=12, color=T.SHADOW_CARD, offset=ft.Offset(0, 4)),
                    ),
                    ft.Text("Насколько легко вспомнил?", size=T.FS_SMALL, color=T.TEXT_SECONDARY),
                    quality_row,
                    quality_labels,
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=T.GAP),
                expand=True, padding=T.PAD_SCREEN,
            ),
        ],
    )
    page.views.clear()
    page.views.append(view)
    page.update()
    render_current()