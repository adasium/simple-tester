from __future__ import annotations

import codecs
from datetime import timedelta
from pathlib import Path
from typing import NamedTuple
from typing import Optional
from typing import TypedDict

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from stylesheet import GROUPBOX_CSS


class _GroupWidgetKwargs(TypedDict, total=False):
    max_width: int


def is_utf8(filename: str | Path) -> bool:
    try:
        f = codecs.open(str(filename), encoding='utf-8', errors='strict')
        for line in f:
            pass
        return True
    except UnicodeDecodeError:
        return False


def group_widgets(
        *widgets: QWidget,
        title: str = '',
        layout: Optional[QLayout] = None,
        checkable: bool = False,
        kwargs: _GroupWidgetKwargs = None,
) -> QGroupBox:
    layout = (layout or QVBoxLayout)()
    kwargs = kwargs or {}

    gb = QGroupBox()
    gb.setTitle(title)
    gb.setStyleSheet(GROUPBOX_CSS)
    gb.setCheckable(checkable)
    gb.setChecked(False)

    if (max_width := kwargs.get('max_width')) is not None:
        gb.setMaximumWidth(max_width)

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


class Timedelta(timedelta):
    @property
    def hours_(self) -> int:
        return self.minutes_ // 60

    @property
    def minutes_(self) -> int:
        return self.seconds // 60

    @property
    def seconds_(self) -> int:
        return self.seconds % 60

    @property
    def milliseconds_(self) -> int:
        return self.microseconds // 1000

    def to_timedelta(self) -> timedelta:
        return timedelta(days=self.days, seconds=self.seconds, microseconds=self.microseconds)
