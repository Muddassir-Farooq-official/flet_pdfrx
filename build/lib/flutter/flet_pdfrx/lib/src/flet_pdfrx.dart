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
  int _lastKnownPage = 1;

  @override
  void didUpdateWidget(FletPdfrxControl oldWidget) {
    super.didUpdateWidget(oldWidget);

    // Check if page_number property changed
    final oldPage = oldWidget.control.getInt("pageNumber", 1) ?? 1;
    final newPage = widget.control.getInt("pageNumber", 1) ?? 1;

    debugPrint(
        "FletPdfrx didUpdateWidget: oldPage=$oldPage, newPage=$newPage, lastKnown=$_lastKnownPage");

    if (newPage != oldPage && _totalPages != null) {
      _navigateToPage(newPage);
    }
  }

  void _navigateToPage(int page) {
    if (_totalPages == null) {
      debugPrint("FletPdfrx: Cannot navigate - document not loaded");
      return;
    }

    final validPage = page.clamp(1, _totalPages!);
    debugPrint("FletPdfrx: Navigating to page $validPage");

    // Navigate immediately
    if (_pdfController.isReady && mounted) {
      _pdfController.goToPage(pageNumber: validPage);
      _lastKnownPage = validPage;
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
        debugPrint("FletPdfrx: PDF loaded with ${document.pages.length} pages");
        _totalPages = document.pages.length;
        widget.control.triggerEvent("loaded", _totalPages.toString());

        // Navigate to initial page
        final initialPage = widget.control.getInt("pageNumber", 1) ?? 1;
        _navigateToPage(initialPage);
      },
      onPageChanged: (page) {
        if (page != null) {
          debugPrint("FletPdfrx: Page changed to $page");
          _lastKnownPage = page;
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
