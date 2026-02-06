import flet as ft
from flet_pdfrx import FletPdfrx


async def main(page: ft.Page):
    page.title = "FletPdfrx Test"
    page.padding = 10

    current_page = 1
    total_pages = 1

    pdf = FletPdfrx(
        src="https://ontheline.trincoll.edu/images/bookdown/sample-local-pdf.pdf",
        expand=True,
        dark_mode=False,
        bgcolor="grey200",
        page_number=2,
    )

    debug_text = ft.Text("Debug: Waiting...", size=12, color=ft.Colors.RED)

    # ---------- EVENT HANDLERS ----------

    def on_loaded(e):
        nonlocal total_pages
        total_pages = int(e.data)
        page_info.value = f"Page {current_page} / {total_pages}"
        page_slider.max = total_pages
        page_slider.divisions = total_pages - 1 if total_pages > 1 else 1
        debug_text.value = f"Debug: PDF loaded with {total_pages} pages"
        page.update()

    def on_page_changed(e):
        nonlocal current_page
        current_page = int(e.data)
        page_input.value = str(current_page)
        page_slider.value = current_page
        page_info.value = f"Page {current_page} / {total_pages}"
        prev_btn.disabled = current_page <= 1
        next_btn.disabled = current_page >= total_pages
        debug_text.value = f"Debug: Page changed to {current_page}"
        page.update()

    async def next_page(e):
        debug_text.value = f"Debug: Next clicked, current={current_page}, pdf.page_number={pdf.page_number}"
        page.update()
        if current_page < total_pages:
            pdf.next_page()
            debug_text.value = f"Debug: Called next_page(), new page_number={pdf.page_number}"
            page.update()

    async def prev_page(e):
        debug_text.value = f"Debug: Prev clicked, current={current_page}, pdf.page_number={pdf.page_number}"
        page.update()
        if current_page > 1:
            pdf.prev_page()
            debug_text.value = f"Debug: Called prev_page(), new page_number={pdf.page_number}"
            page.update()

    async def jump_to_page(e):
        try:
            p = int(page_input.value)
            if 1 <= p <= total_pages:
                debug_text.value = f"Debug: Jumping to page {p}"
                page.update()
                pdf.go_to_page(p)
                debug_text.value = f"Debug: Called go_to_page({p}), pdf.page_number={pdf.page_number}"
                page.update()
            else:
                page_input.error_text = f"Enter 1-{total_pages}"
                page.update()
        except ValueError:
            page_input.error_text = "Invalid number"
            page.update()

    async def slider_changed(e):
        pdf.go_to_page(int(page_slider.value))

    async def toggle_dark(e):
        pdf.dark_mode = dark_switch.value
        pdf.bgcolor = "grey900" if pdf.dark_mode else "grey200"
        pdf.update()

    async def input_focus(e):
        page_input.error_text = None
        page.update()

    # ---------- UI CONTROLS ----------

    page_info = ft.Text(
        "Page 1 / ?",
        size=16,
        weight=ft.FontWeight.BOLD,
    )

    page_input = ft.TextField(
        width=80,
        value="1",
        keyboard_type=ft.KeyboardType.NUMBER,
        hint_text="Page",
        text_align=ft.TextAlign.CENTER,
        on_submit=jump_to_page,
        on_focus=input_focus,
    )

    prev_btn = ft.ElevatedButton(
        "◀ Prev",
        on_click=prev_page,
        disabled=True,
        icon=ft.Icons.ARROW_BACK,
    )

    next_btn = ft.ElevatedButton(
        "Next ▶",
        on_click=next_page,
        icon=ft.Icons.ARROW_FORWARD,
    )

    jump_btn = ft.ElevatedButton(
        "Go",
        on_click=jump_to_page,
        icon=ft.Icons.SEND,
    )

    dark_switch = ft.Switch(
        label="Dark Mode",
        on_change=toggle_dark,
        value=False,
    )

    page_slider = ft.Slider(
        min=1,
        max=1,
        value=1,
        divisions=1,
        label="{value}",
        width=300,
        on_change_end=slider_changed,
    )

    # Top Controls Row
    controls_top = ft.Row(
        controls=[
            prev_btn,
            next_btn,
            ft.VerticalDivider(),
            page_input,
            jump_btn,
            ft.VerticalDivider(),
            page_info,
            ft.VerticalDivider(),
            dark_switch,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )

    # Slider Row
    slider_row = ft.Row(
        controls=[
            ft.Icon(ft.Icons.PICTURE_AS_PDF, color=ft.Colors.BLUE_400),
            page_slider,
            ft.Icon(ft.Icons.PICTURE_AS_PDF, color=ft.Colors.BLUE_400),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Attach events
    pdf.on_loaded = on_loaded
    pdf.on_page_changed = on_page_changed

    # Layout
    page.add(
        ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[controls_top, slider_row, debug_text],
                    spacing=5,
                ),
                padding=10,
            ),
            elevation=2,
        ),
        ft.Divider(height=1, color=ft.Colors.GREY_400),
        ft.Container(
            content=pdf,
            expand=True,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
        ),
    )


ft.app(target=main)