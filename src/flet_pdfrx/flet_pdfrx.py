from typing import Any, Optional
import flet as ft


@ft.control("flet_pdfrx")
class FletPdfrx(ft.LayoutControl):
    """
    FletPdfrx Control for high-performance PDF viewing (Flet v1 compatible).
    """

    # --- Properties (synced to Dart via update()) ---
    src: Optional[str] = None
    """PDF source URL or local path."""

    is_asset: bool = False
    """True if the source is a Flutter asset."""

    page_number: int = 1
    """Current page number (kept in sync by on_page_changed)."""

    enable_selection: bool = True
    """Whether text selection is enabled."""

    dark_mode: bool = False
    """Enable color inversion for night reading."""

    bgcolor: Optional[str] = None
    """Custom background color for the viewer area."""

    # --- Events (Dart → Python via triggerEvent) ---
    on_loaded: Optional[ft.ControlEventHandler[Any]] = None
    """Fires when the PDF is loaded. e.data = total pages."""

    on_page_changed: Optional[ft.ControlEventHandler[Any]] = None
    """Fires when the page changes. e.data = current page."""

    # --- Public API (Python → Dart via invoke_method) ---
    async def go_to_page(self, page: int):
        """Jump to a specific page."""
        self.page_number = page
        await self._invoke_method("go_to_page", {"page": page})

    async def next_page(self):
        """Go to next page."""
        self.page_number += 1
        await self._invoke_method("go_to_page", {"page": self.page_number})

    async def prev_page(self):
        """Go to previous page."""
        self.page_number = max(1, self.page_number - 1)
        await self._invoke_method("go_to_page", {"page": self.page_number})

    async def search_text(self, text: str):
        """Trigger a text search in the PDF."""
        await self._invoke_method("search_text", {"text": text})