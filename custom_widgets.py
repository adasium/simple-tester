from typing import List, Optional, TypeVar
from pathlib import Path
from typing import Any

from PyQt5.QtCore import QElapsedTimer, Qt, QTimer
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (
    QDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from score import Score


def color_str(string, color='black'):
    string = f'<span style="color:{color};">{string}</span>'
    return string


class TreeWidget(QTreeWidget):
    def __init__(self, path: Path, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._path = path

    @property
    def path(self) -> Path:
        return self._path


class TreeWidgetItem(QTreeWidgetItem):
    def __init__(self, path: Path, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._path = path

    @property
    def is_checked(self) -> bool:
        return self.checkState(0) == Qt.Checked

    @property
    def path(self) -> Path:
        return self._path


class CustomQTextEdit(QTextEdit):
    def __init__(self, enter_method, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enter_method = enter_method

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == Qt.Key_Return:
            self.enter_method()
            self.setText('')
        else:
            super().keyPressEvent(qKeyEvent)


class ScoreQLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.score = Score()
        self.update()

    def add_correct(self):
        self.score.good_ans()

    def add_incorrect(self):
        self.score.bad_ans()

    def update(self):
        self.setText('Correct: {}\nIncorrect: {}\nScore: {:.2f}%'.format(self.score.correct, self.score.incorrect, self.score.get_percentage()))

    def clear(self):
        self.score.clear()


class QElapsedTimerWidget(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._timer = QElapsedTimer()
        self._timer.start()
        self._check_thread_timer = QTimer(self)
        self._check_thread_timer.setInterval(1)  # .5 seconds
        self._check_thread_timer.timeout.connect(self.update)
        self.stopped = True

    def start(self):
        self.stopped = False
        self._timer.start()
        self.update()

    def stop(self):
        self.stopped = True

    def update(self):
        if not self.stopped:
            total_milliseconds = self._timer.elapsed()

            minutes = total_milliseconds // 60000
            seconds = (total_milliseconds - minutes*60000) // 1000
            milliseconds = total_milliseconds - minutes*60000 - seconds*1000
            self.setText('{}m {}s {:03d}ms'.format(minutes, seconds, milliseconds))
            self._check_thread_timer.start()


class QInfoDialog(QDialog):
    def __init__(self, text='', title=' ', *args, **kwargs):
        super().__init__(*args, **kwargs)
        l = QLabel()
        l.setText(text)
        self.setWindowTitle(title)

        d_layout = QVBoxLayout()
        self.setLayout(d_layout)

        b = QPushButton()
        b.clicked.connect(self.close)
        b.setText("OK")

        d_layout.addWidget(l)
        d_layout.addWidget(b)


class QQuestionRange(QWidget):

    def __init__(self, first_label='start', second_label='end', *args, **kwargs):
        self.first_label = first_label
        self.second_label = second_label
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        self.setFixedWidth(100)

        self.e0 = QLineEdit()
        self.e0.setValidator(QIntValidator())
        self.e0.setMaxLength(4)

        self.e1 = QLineEdit()
        self.e1.setValidator(QIntValidator())
        self.e1.setMaxLength(4)

        layout.addWidget(QLabel(self.first_label), 0, 0)
        layout.addWidget(self.e0, 0, 1)
        layout.addWidget(QLabel(self.second_label), 1, 0)
        layout.addWidget(self.e1, 1, 1)

        self.setLayout(layout)

    def get_range(self):
        # TODO(#4): set default value
        # TODO(#5): validate e1 >= e2
        try:
            start = int(self.e0.text())
            end = int(self.e1.text())

            if end-start < 0 or start <=0 or end <= 0:
                return None

            return slice(start-1, end)

        except ValueError:
            return None


class FillerWidget(QWidget):
    def __init__(self, width=False, height=True, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        width_policy = QSizePolicy.Expanding if width else QSizePolicy.Minimum
        height_policy = QSizePolicy.Expanding if height else QSizePolicy.Minimum
        self.setSizePolicy(width_policy, height_policy)


class WidthFillerWidget(FillerWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(width=True, *args, **kwargs)


class HeightFillerWidget(FillerWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(height=True, *args, **kwargs)


T = TypeVar('T')


class ValueRadioButton(QRadioButton):
    def __init__(self, value: T, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._value = value

    @property
    def value(self) -> T:
        return self._value


class RadioGroupWidget(QWidget):
    def __init__(self, widgets: List[ValueRadioButton], default: int = 0, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._widgets = widgets
        self._widgets[default].setChecked(True)

    def get_selected(self) -> Optional[int]:
        for i, widget in enumerate(self._widgets):
            if widget.isChecked():
                return i
        return None

    @property
    def selected(self) -> ValueRadioButton:
        for i, widget in enumerate(self._widgets):
            if widget.isChecked():
                return widget
        raise ValueError('At least one radio should be selected')

    @property
    def widgets(self) -> List[QRadioButton]:
        return self._widgets
