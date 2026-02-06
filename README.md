# Introducing flet-pdfrx - High-Performance PDF Viewer for Flet.

I'm excited to share flet-pdfrx, a new Flet extension that brings the powerful pdfrx Flutter package to the Flet ecosystem!

## Features
📄 Multi-source PDF loading - URLs, local files, assets, and memory<br>
🎨 Dark mode support - Built-in color inversion for night reading<br>
🔍 Text selection - Native text selection and copying<br>
📱 Cross-platform - Works on Android, iOS, Windows, macOS, Linux, and Web<br>
⚡ High performance - Powered by PDFium rendering engine<br>
🎯 Simple API - Easy-to-use Python interface<br>

## Current Features
✅ Load PDFs from URL, local files, or assets<br>
✅ Dark mode with color inversion<br>
✅ Text selection support<br>
✅ Event callbacks (on_loaded, on_page_changed)<br>
✅ Custom background colors<br>
✅ Page navigation methods (go_to_page, next_page, prev_page)<br>

## Installation

Add dependency to `pyproject.toml` of your Flet app:

* **Git dependency**

Link to git repository:

```
dependencies = [
  "flet-pdfrx @ git+https://github.com/Muddassir-Farooq-official/flet_pdfrx.git",
  "flet>=0.80.5",
]
```

* **uv/pip dependency**  

If the package is published on pypi.org:

```
dependencies = [
  "flet-pdfrx",
  "flet>=0.80.5",
]
```

Build your app:
```
flet build macos -v
```

## Documentation

[Link to documentation](https://MyGithubAccount.github.io/flet-pdfrx/)
