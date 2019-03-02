from PyQt5.QtWidgets import *
from custom_widgets import CustomQTextEdit, ScoreQLabel, color_str
from quiz import Quiz


class QuizWidget(QWidget):
    def __init__(self, database, order):
        super().__init__()
        self.setWindowTitle('New test')
        self._left = 10
        self._top = 10
        self._width = 640
        self._height = 480
        self.setGeometry(self._left, self._top, self._width, self._height)
        self.setFixedSize(self.size())
        self._database = database
        self._order = order

        self._l_question = QLabel()
        self._te_logs = QTextEdit()
        self._te_answer = CustomQTextEdit(self.check_answer)
        self.initUI()
        self.__update_database()

    def __update_database(self):
        # print(self._database.get_questions())
        self._quiz = Quiz(self._database.get_questions(), self._order)
        self._progress.setMaximum(self._quiz.question_count())
        self._progress.setValue(0)

        self._l_question.setText(self._quiz.get_question())

    def initUI(self):
        self.setGeometry(self._left, self._top, self._width, self._height)

        # create stuff
        layout = QGridLayout()
        self._te_logs.setReadOnly(True)
        self._l_score = ScoreQLabel()
        b_submit_answer = QPushButton('Answer')
        b_submit_answer.clicked.connect(self.check_answer)
        self._progress = QProgressBar(self)
        self._progress.setMinimum(0)

        # assemble
        layout.addWidget(self._te_logs, 0, 0)
        layout.addWidget(self._l_question, 1, 0)
        layout.addWidget(self._l_score, 0, 1)
        layout.addWidget(self._te_answer, 2, 0)
        layout.addWidget(b_submit_answer, 2, 1)
        layout.addWidget(self._progress, 3, 0, 1, 2)

        self.setLayout(layout)

    def show(self):
        super().show()
        self._te_answer.setFocus()

    def check_answer(self):
        question = self._quiz.get_question()

        if question:
            answer = self._te_answer.toPlainText()
            correct_answer = self._quiz.get_answer()

            self._te_logs.append(question + ": " + answer)
            if answer == correct_answer:
                string = color_str('Brawo!', 'green')
                self._l_score.add_correct()
                self._te_logs.append(string)
            else:
                self._te_logs.append(color_str('Jesteś dupa! Prawidłowa odpowiedź to: ', 'red') + correct_answer)
                self._l_score.add_incorrect()

            self._quiz.next_question()
            self._progress.setValue(self._quiz.get_question_index())
            self._l_score.update()
            self._l_question.setText(self._quiz.get_question())

    def update_proggress_bar(self):
        val = self._quiz.get_current_question_index()
        self._progress.setValue(val)
