from pathlib import Path

import pyqtgraph as pg
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget

import settings
from stats import STATS
from utils import move_to_screen


class StatsWindow(QWidget):
    def __init__(self, path: Path, *args, **kwargs) -> None:
        super().__init__()

        self.setWindowTitle('Stats')
        self.setGeometry(*settings.WINDOW_GEOMETRY)
        self.setFixedSize(self.size())

        posx, posy, *_ = settings.WINDOW_GEOMETRY
        move_to_screen(widget=self, posx=posx, posy=posy)

        layout = QGridLayout()
        axis = pg.DateAxisItem()
        plot = pg.PlotWidget(title="Multiple curves")
        plot.setAxisItems({'bottom': axis})
        plot.addLegend()

        layout.addWidget(plot)
        self.setLayout(layout)

        entries = [
            e for e in STATS.entries
            if e.quiz_path.samefile(path)
        ]
        plot.plot(
            x=[e.timestamp.timestamp() for e in entries],
            y=[e.correct for e in entries],
            pen='g',
            name='Correct count',
        )
        plot.plot(
            x=[e.timestamp.timestamp() for e in entries],
            y=[e.incorrect for e in entries],
            fill_level=0,
            pen='r',
            name='Incorrect count',
        )
        plot.plot(
            x=[e.timestamp.timestamp() for e in entries],
            y=[e.total for e in entries],
            pen='y',
            name='Total count',
        )

        self.show()
