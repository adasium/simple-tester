from PyQt5.QtWidgets import QTreeWidgetItem, QTextEdit, QLabel, QDialog, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QElapsedTimer, QTimer
from score import Score


def color_str(string, color='black'):
    if color == 'black':
        return string
    elif color in ('green', 'red'):
        string = f'<span style="color:{color};">{string}</span>'
        return string


class CustomQTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent, path, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.path = path

    def is_checked(self):
        return self.checkState(0) == Qt.CheckState.Checked

    def get_path(self):
        return self.path


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
        self.score.correct = 0
        self.score.incorrect = 0

class QElapsedTimerWidget(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._timer = QElapsedTimer()
        self._timer.start()
        self._check_thread_timer = QTimer(self)
        self._check_thread_timer.setInterval(1) #.5 seconds
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
