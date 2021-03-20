from pathlib import Path
from typing import Any
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar

from PyQt5.QtCore import QElapsedTimer
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from score import Score
from utils import Timedelta


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

    def set_path(self, path: Path) -> None:
        self._path = path


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
            self.setText('{}m {}s {:03d}ms'.format(self.elapsed.minutes_, self.elapsed.seconds_, self.elapsed.milliseconds_))
            self._check_thread_timer.start()

    @property
    def elapsed(self) -> Timedelta:
        return Timedelta(milliseconds=self._timer.elapsed())


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

    def __init__(
            self,
            first_label='start',
            second_label='end',
            first_default: int = 10,
            second_default: int = 0,
            *args: Any,
            **kwargs: Any,
    ) -> None:
        self.first_label = first_label
        self.second_label = second_label
        super().__init__(*args, **kwargs)
        self.initUI()
        self.e0.setText(str(first_default))
        self.e1.setText(str(second_default))

    def initUI(self) -> None:
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

    def get_range(self) -> Optional[slice]:
        try:
            limit = int(self.e0.text())
            offset = int(self.e1.text())
            return slice(offset, limit + offset)
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
        kwargs['width'] = True
        super().__init__(*args, **kwargs)


class HeightFillerWidget(FillerWidget):
    def __init__(self, *args, **kwargs) -> None:
        kwargs['height'] = True
        super().__init__(*args, **kwargs)


T = TypeVar('T')


class ValueRadioButton(QRadioButton, Generic[T]):
    def __init__(self, value: T, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._value = value

    @property
    def value(self) -> T:
        return self._value


class RadioGroupWidget(QWidget):
    def __init__(self, widgets: List[ValueRadioButton[T]], default: T, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._widgets = {widget.value: widget for widget in widgets}
        self._widgets[default].setChecked(True)

    @property
    def selected(self) -> ValueRadioButton:
        for widget in self._widgets.values():
            if widget.isChecked():
                return widget
        raise ValueError('At least one radio should be selected')

    @property
    def widgets(self) -> List[QRadioButton]:
        return list(self._widgets.values())


class Label(QLabel):
    def __init__(self, *args: Any, max_height: Optional[int] = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignCenter)
        if max_height is not None:
            self.setMaximumHeight(max_height)
