from pathlib import Path
from typing import List

import pyqtgraph as pg
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QWidget

import settings
from stats import Entry
from stats import STATS
from utils import move_to_screen


class StatsWindow(QWidget):
    def __init__(self, paths: List[Path], *args, **kwargs) -> None:
        super().__init__()
        title = paths[0] if len(paths) == 1 else ''

        self.setWindowTitle('Stats')
        self.setGeometry(*settings.WINDOW_GEOMETRY)
        self.setFixedSize(self.size())

        posx, posy, *_ = settings.WINDOW_GEOMETRY
        move_to_screen(widget=self, posx=posx, posy=posy)

        layout = QGridLayout()
        axis = pg.DateAxisItem()
        plot = pg.PlotWidget(title=title)
        plot.setAxisItems({'bottom': axis})
        plot.addLegend()

        layout.addWidget(plot)
        self.setLayout(layout)

        entries = self.get_entries(paths)
        timestamp_series = [e.timestamp.timestamp() for e in entries]
        plot.plot(
            x=timestamp_series,
            y=[e.correct for e in entries],
            pen='g',
            name='Correct count',
            symbol='o',
            symbolBrush='g',
        )
        plot.plot(
            x=timestamp_series,
            y=[e.incorrect for e in entries],
            fill_level=0,
            pen='r',
            symbol='o',
            name='Incorrect count',
            symbolBrush='r',
        )
        plot.plot(
            x=timestamp_series,
            y=[e.total for e in entries],
            pen='y',
            name='Total count',
            symbol='o',
            symbolBrush='y',
        )

        self.show()

    def get_entries(self, paths: List[Path]) -> List[Entry]:
        if len(STATS.entries) == 0:
            return []

        entries = [
            e for e in STATS.entries
            if e.quiz_path in set(paths)
        ]

        ret = []
        previous, *rest = sorted(entries, key=lambda e: e.timestamp)
        prev = {previous.quiz_path: previous}
        ret.append(previous)
        for entry in rest:
            prev[entry.quiz_path] = entry
            ret.append(sum(prev.values(), start=Entry()))
        return ret
