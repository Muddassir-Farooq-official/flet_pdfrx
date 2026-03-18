import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:pdfrx/pdfrx.dart';

class FletPdfrxControl extends StatefulWidget {
  final Control control;
  const FletPdfrxControl({super.key, required this.control});

  @override
  State<FletPdfrxControl> createState() => _FletPdfrxControlState();
}

class _FletPdfrxControlState extends State<FletPdfrxControl> {
  final _pdfController = PdfViewerController();
  int? _totalPages;

  @override
  void initState() {
    super.initState();
    widget.control.addInvokeMethodListener(_onInvokeMethod);
  }

  @override
  void dispose() {
    widget.control.removeInvokeMethodListener(_onInvokeMethod);
    super.dispose();
  }

  /// Receives method calls from Python via _invoke_method().
  Future<dynamic> _onInvokeMethod(String name, dynamic args) async {
    Map<String, dynamic> arguments = {};
    if (args != null && args is Map) {
      arguments = Map<String, dynamic>.from(args);
    }

    switch (name) {
      case "go_to_page":
        final page = arguments["page"] as int? ?? 1;
        _navigateToPage(page);
        return null;
      case "search_text":
        // TODO: implement search
        debugPrint("FletPdfrx: search_text not yet implemented");
        return null;
      default:
        throw Exception("Unknown FletPdfrx method: $name");
    }
  }

  void _navigateToPage(int page) {
    if (_totalPages == null) {
      debugPrint("FletPdfrx: Cannot navigate - document not loaded");
      return;
    }

    final validPage = page.clamp(1, _totalPages!);
    debugPrint("FletPdfrx: Navigating to page $validPage");

    if (_pdfController.isReady && mounted) {
      _pdfController.goToPage(pageNumber: validPage);
    }
  }

  @override
  Widget build(BuildContext context) {
    String src = widget.control.getString("src", "") ?? "";
    bool isAsset = widget.control.getBool("isAsset", false) ?? false;
    bool darkMode = widget.control.getBool("darkMode", false) ?? false;

    Color? bgcolor = widget.control.getColor("bgcolor", context) ??
        (darkMode ? Colors.grey[900] : Colors.grey[200]);

    final params = PdfViewerParams(
      backgroundColor: bgcolor!,
      onViewerReady: (document, controller) {
        debugPrint(
            "FletPdfrx: PDF loaded with ${document.pages.length} pages");
        _totalPages = document.pages.length;
        widget.control.triggerEvent("loaded", _totalPages.toString());

        // Navigate to initial page if not page 1
        final initialPage = widget.control.getInt("pageNumber", 1) ?? 1;
        if (initialPage != 1) {
          _navigateToPage(initialPage);
        }
      },
      onPageChanged: (page) {
        if (page != null) {
          debugPrint("FletPdfrx: Page changed to $page");
          widget.control.triggerEvent("page_changed", page.toString());
        }
      },
    );

    Widget viewer = isAsset
        ? PdfViewer.asset(src, controller: _pdfController, params: params)
        : PdfViewer.uri(Uri.parse(src),
            controller: _pdfController, params: params);

    if (darkMode) {
      viewer = ColorFiltered(
        colorFilter: const ColorFilter.matrix([
          -1,
          0,
          0,
          0,
          255,
          0,
          -1,
          0,
          0,
          255,
          0,
          0,
          -1,
          0,
          255,
          0,
          0,
          0,
          1,
          0,
        ]),
        child: viewer,
      );
    }

    return LayoutControl(control: widget.control, child: viewer);
  }
}