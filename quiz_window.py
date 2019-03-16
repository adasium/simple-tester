from PyQt5.QtWidgets import *
from custom_widgets import CustomQTextEdit, ScoreQLabel, color_str, QElapsedTimerWidget
from quiz import Quiz
import settings


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
        self._timer = QElapsedTimerWidget()
        self._timer.start()
        self._mistakes = []

        self._l_question = QLabel()
        self._te_logs = QTextEdit()
        self._te_answer = CustomQTextEdit(self.check_answer)
        self.initUI()
        self.__update_database()

    def __update_database(self):
        self._quiz = Quiz(self._database.get_questions(), self._order)
        self._progress.setMaximum(self._quiz.question_count())
        self._progress.setValue(0)

        self._l_question.setText(self._quiz.get_question_object().get_question())

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
        layout.addWidget(self._timer, 1, 1)
        layout.addWidget(self._te_answer, 2, 0)
        layout.addWidget(b_submit_answer, 3, 1)
        layout.addWidget(self._progress, 4, 0, 1, 2)

        self.setLayout(layout)

    def show(self):
        super().show()
        self._te_answer.setFocus()

    def check_answer(self):
        question_object = self._quiz.get_question_object()

        if question_object is None:
            return

        answer = self._te_answer.toPlainText()
        correct_answer = question_object.get_answer()

        self._te_logs.append(question_object.get_question() + ": " + answer)
        if answer == correct_answer:
            string = color_str(settings.GOOD_ANS_TEXT, settings.GOOD_ANS_COLOR)
            self._l_score.add_correct()
            self._te_logs.append(string)
        else:
            self._te_logs.append(color_str(settings.BAD_ANS_TEXT, settings.BAD_ANS_COLOR) + correct_answer)
            self._l_score.add_incorrect()
            self._mistakes.append(question_object)

        self.update_question()
        if self._quiz.is_finished():
            self.perform_end_quiz_actions()

    def update_question(self):
        self._quiz.set_next_question()
        self.update_proggress_bar()
        self._l_score.update()
        try:
            self._l_question.setText(self._quiz.get_question_object().get_question(category=True))
        except AttributeError:
            self._l_question.setText('')

    def update_proggress_bar(self):
        val = self._quiz.get_current_question_index()
        self._progress.setValue(val)

    def perform_end_quiz_actions(self):
        self._timer.stop()
        with open(settings.ERROR_FILE_LOCATION, 'w', encoding='utf-8') as f:
            for q in self._mistakes:
                f.write('\n')
                f.write(str(q))

