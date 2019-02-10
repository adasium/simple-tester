from PyQt5.QtWidgets import QTreeWidgetItem, QTextEdit, QLabel
from PyQt5.QtCore import Qt
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
        self.setText('Correct: {}\nIncorrect: {}\nScore: {}%'.format(self.score.correct, self.score.incorrect, self.score.get_percentage()))
