from PyQt5.QtWidgets import *
from custom_widgets import CustomQTextEdit, ScoreQLabel, color_str


class TestWidget(QWidget):
    def __init__(self, database):
        super().__init__()
        self.setWindowTitle('New test')
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.size())
        self.database = database

        self.l_question = QLabel()
        self.te_logs = QTextEdit()
        self.te_answer = CustomQTextEdit(self.check_answer)
        self.initUI()
        self.__update_database()

    def __update_database(self):
        self.questions = self.database.get_questions()
        self.current_question = 0
        self.progress.setMaximum(len(self.questions))
        self.progress.setValue(0)

        self.l_question.setText(self.questions[self.current_question].get_question())

    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)

        # create stuff
        layout = QGridLayout()
        self.te_logs.setReadOnly(True)
        self.l_score = ScoreQLabel()
        b_submit_answer = QPushButton('Answer')
        b_submit_answer.clicked.connect(self.check_answer)
        self.progress = QProgressBar(self)
        self.progress.setMinimum(0)

        # assemble
        layout.addWidget(self.te_logs, 0, 0)
        layout.addWidget(self.l_question, 1, 0)
        layout.addWidget(self.l_score, 0, 1)
        layout.addWidget(self.te_answer, 2, 0)
        layout.addWidget(b_submit_answer, 2, 1)
        layout.addWidget(self.progress, 3, 0, 1, 2)

        self.setLayout(layout)

    def show(self):
        super().show()
        self.te_answer.setFocus()

    def check_answer(self):
        question = self.get_current_question()
        answer = self.te_answer.toPlainText()
        correct_answer = self.get_current_answer()
        self.te_logs.append(question + ": " + answer)
        if answer == correct_answer:
            string = color_str('Brawo!', 'green')
            self.l_score.add_correct()
            self.te_logs.append(string)
        else:
            self.te_logs.append(color_str('Jesteś dupa! Prawidłowa odpowiedź to: ', 'red') + correct_answer)
            self.l_score.add_incorrect()
        self.inc_question()
        self.progress.setValue(self.current_question)
        self.l_score.update()

    def get_current_question(self):
        return self.questions[self.current_question].get_question() if self.current_question < len(self.questions) else ''

    def get_current_answer(self):
        return self.questions[self.current_question].get_answer()

    def inc_question(self):
        self.current_question += 1
        self.l_question.setText(self.get_current_question())
