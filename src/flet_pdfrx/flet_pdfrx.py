from typing import Any, Optional, Union
import flet as ft

from typing import Any, Optional
import flet as ft


@ft.control("flet_pdfrx")
class FletPdfrx(ft.LayoutControl):
    """
    FletPdfrx Control for high-performance PDF viewing (Flet v1 compatible).
    """

    # --- Properties ---
    src: Optional[str] = None
    """PDF source URL or local path."""

    is_asset: bool = False
    """True if the source is a Flutter asset."""

    page_number: int = 1
    """Current page to display."""

    enable_selection: bool = True
    """Whether text selection is enabled."""

    dark_mode: bool = False
    """Enable color inversion for night reading."""

    bgcolor: Optional[str] = None
    """Custom background color for the viewer area."""

    # --- Events ---
    on_loaded: Optional[ft.ControlEventHandler[Any]] = None
    """Fires when the PDF is loaded. e.data = total pages."""

    on_page_changed: Optional[ft.ControlEventHandler[Any]] = None
    """Fires when the page changes. e.data = current page."""

    # --- Public API ---
    def go_to_page(self, page: int):
        """Jump to a specific page."""
        self.page_number = page
        self.update()  # In Flet v1, update() is enough to sync to Flutter

    def next_page(self):
        """Go to next page."""
        self.page_number += 1
        self.update()

    def prev_page(self):
        """Go to previous page."""
        self.page_number = max(1, self.page_number - 1)
        self.update()

    def search_text(self, text: str):
        """
        Optional: trigger a search in the PDF.
        The Dart side should implement search logic and return results via an event.
        """
        self.trigger_event("search_text", text)
