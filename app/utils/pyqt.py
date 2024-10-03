def find_element(root, type, name, cb_name, default):
    widget = root.findChild(type, name)
    if widget is None:
        return default
    if hasattr(widget, cb_name):
        return getattr(widget, cb_name)()
