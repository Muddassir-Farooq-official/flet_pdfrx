import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';

import 'flet_pdfrx.dart';

class Extension extends FletExtension {
  @override
  Widget? createWidget(Key? key, Control control) {
    switch (control.type) {
      case "flet_pdfrx":
        return FletPdfrxControl(control: control);
      default:
        return null;
    }
  }
}
