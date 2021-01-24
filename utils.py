import codecs
from stylesheet import GROUPBOX_CSS
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QApplication


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


def get_active_screen():
    return QApplication.screenAt(QCursor.pos())


def move_to_screen(widget, posx=0, posy=0, screen=None):
    app = QApplication
    screen = screen or get_active_screen()
    screen_number = app.screens().index(screen)
    screen_rect = app.desktop().screenGeometry(screen_number)
    widget.move(QPoint(screen_rect.x() + posx, screen_rect.y() + posy))
