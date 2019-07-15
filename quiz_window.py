from PyQt5.QtWidgets import *
from custom_widgets import CustomQTextEdit, ScoreQLabel, color_str, QElapsedTimerWidget
from quiz import Quiz
import settings


class QuizWidget(QWidget):
    def __init__(self, database, order, **kwargs):
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
        self._range = kwargs.get('range')
        self.initUI()
        self.__update_database()

    def __get_questions(self):
        questions = self._database.get_questions()
        if self._range:
            questions = questions[self._range]
        return questions


    def __update_database(self):
        self._quiz = Quiz(self.__get_questions(), self._order)
        self._progress.setMaximum(self._quiz.question_count())
        self.update_progress_bar()

        self._l_question.setText(self._quiz.get_question_object().get_question())

    def initUI(self):
        self.setGeometry(self._left, self._top, self._width, self._height)

        # create stuff
        layout = QGridLayout()
        left_column = QGridLayout()
        right_column = QGridLayout()

        layout.addLayout(left_column, 0, 0)
        layout.addLayout(right_column, 0, 1)

        #left_column
        self._te_logs.setReadOnly(True)
        self._l_score = ScoreQLabel()

        #right_column
        b_submit_answer = QPushButton('Answer')
        b_submit_answer.clicked.connect(self.check_answer)
        b_redo_test = QPushButton('Restart')
        b_redo_test.clicked.connect(self.redo_test)
        self._b_redo_test = b_redo_test

        #bottom
        self._progress = QProgressBar(self)
        self._progress.setMinimum(0)

        # assemble
        left_column.addWidget(self._te_logs, 0, 0)
        left_column.addWidget(self._l_question, 1, 0)
        left_column.addWidget(self._te_answer, 2, 0)

        right_column.addWidget(self._l_score, 0, 0)
        right_column.addWidget(self._timer, 1, 0)
        right_column.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding), 2, 0, 3, 1)
        right_column.addWidget(b_submit_answer, 5, 0)
        right_column.addWidget(b_redo_test, 6, 0)

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

        self._te_logs.append(color_str(question_object.get_question() + ": " + answer))
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

    def redo_test(self):
        self._te_answer.setFocus()
        self._l_score.clear()
        self._l_score.update()
        self._quiz = Quiz(self.__get_questions(), self._order)
        self._l_question.setText(self._quiz.get_question_object().get_question(category=True))
        self.update_progress_bar()
        self._te_logs.setText('')
        self._timer.start()
        pass

    def update_question(self):
        self._quiz.set_next_question()
        self.update_progress_bar()
        self._l_score.update()
        try:
            self._l_question.setText(self._quiz.get_question_object().get_question(category=True))
        except AttributeError:
            self._l_question.setText('')

    def update_progress_bar(self):
        val = self._quiz.get_current_question_index()
        self._progress.setValue(val)
        question_count = len(self.__get_questions())
        self._progress.setFormat("{:.2f}% ({}/{})".format(100*(val/question_count), val, question_count))

    def perform_end_quiz_actions(self):
        self._timer.stop()
        if settings.SAVE_ERRORS:
            with open(settings.ERROR_FILE_LOCATION, 'w', encoding='utf-8') as f:
                for q in self._mistakes:
                    f.write('\n')
                    f.write(str(q))

