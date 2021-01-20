import codecs
from stylesheet import GROUPBOX_CSS
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout


def is_utf8(filename: str) -> bool:
    try:
        f = codecs.open(filename, encoding='utf-8', errors='strict')
        for line in f:
            pass
        return True
    except UnicodeDecodeError:
        return False


def group_widgets(*widgets, title='', layout=None, checkable=False, kwargs=None):
    layout = (layout or QVBoxLayout)()
    kwargs = kwargs or {}

    gb = QGroupBox()
    gb.setTitle(title)
    gb.setStyleSheet(GROUPBOX_CSS)
    gb.setCheckable(checkable)
    gb.setChecked(False)
    _kwargs = {
        'max_width': gb.setMaximumWidth,
        'title': gb.setTitle,
    }
    for kwarg, fun in _kwargs.items():
        if kwarg in kwargs:
            fun(kwargs.pop(kwarg))
    for widget in widgets:
        layout.addWidget(widget)
    gb.setLayout(layout)
    return gb
