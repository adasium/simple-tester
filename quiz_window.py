from typing import Any, List, Optional

import settings
from PyQt5.QtWidgets import (QGridLayout, QLabel, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QTextEdit, QWidget)
from custom_widgets import (CustomQTextEdit, QElapsedTimerWidget, QInfoDialog,
    ScoreQLabel, color_str)
from database import Database
from enums import Order
from question import Question
from quiz import Quiz
from utils import move_to_screen


class QuizWidget(QWidget):
    def __init__(self, database: Database, order: Order, **kwargs: Any) -> None:
        super().__init__()
        self.setWindowTitle('New test')
        self.setGeometry(*settings.WINDOW_GEOMETRY)
        self.setFixedSize(self.size())
        self._database = database
        self._order = order
        self._timer = QElapsedTimerWidget()
        self._timer.setMinimumWidth(100)
        self._timer.start()
        self._mistakes: List[Question] = []

        self._l_question = QLabel()
        self._te_logs = QTextEdit()
        self._te_answer = CustomQTextEdit(self.check_answer)
        self._range = kwargs.get('range')
        self.initUI()
        self.redo_test(self.__get_questions())

    def __get_questions(self) -> List[Question]:
        questions = self._database.questions
        if self._range is not None:
            questions = questions[self._range]
        return questions

    def initUI(self) -> None:
        self.setGeometry(*settings.WINDOW_GEOMETRY)

        # create stuff
        layout = QGridLayout()
        left_column = QGridLayout()
        right_column = QGridLayout()

        layout.addLayout(left_column, 0, 0)
        layout.addLayout(right_column, 0, 1)

        # left_column
        self._te_logs.setReadOnly(True)
        self._l_score = ScoreQLabel()

        # right_column
        self._b_redo_errors = QPushButton('Redo mistakes')
        self._b_redo_errors.clicked.connect(self.redo_errors)

        # left_column
        self._te_logs.setReadOnly(True)
        self._l_score = ScoreQLabel()

        # right_column
        b_submit_answer = QPushButton('Answer')
        b_submit_answer.clicked.connect(self.check_answer)
        self._b_redo_test = QPushButton('Restart')
        self._b_redo_test.clicked.connect(self.redo_test)

        # bottom
        self._progress = QProgressBar(self)
        self._progress.setMinimum(0)

        # assemble
        left_column.addWidget(self._te_logs, 0, 0)
        left_column.addWidget(self._l_question, 1, 0)
        left_column.addWidget(self._te_answer, 2, 0)

        right_column.addWidget(self._l_score, 0, 0)
        right_column.addWidget(self._timer, 1, 0)
        right_column.addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding),
            2, 0, 3, 1,
        )
        right_column.addWidget(self._b_redo_errors, 4, 0)
        right_column.addWidget(b_submit_answer, 5, 0)
        right_column.addWidget(self._b_redo_test, 6, 0)

        layout.addWidget(self._progress, 4, 0, 1, 2)

        self.setLayout(layout)
        posx, posy, *_ = settings.WINDOW_GEOMETRY
        move_to_screen(widget=self, posx=posx, posy=posy)

    def show(self):
        super().show()
        self._te_answer.setFocus()

    def check_answer(self):
        question_object = self._quiz.get_question_object()

        if question_object is None:
            return

        answer = self._te_answer.toPlainText()

        self._te_logs.append(color_str(question_object.get_question() + ": " + answer))
        if question_object.is_correct(answer):
            string = color_str(settings.GOOD_ANS_TEXT, settings.GOOD_ANS_COLOR)
            self._l_score.add_correct()
            self._te_logs.append(string)
        else:
            self._te_logs.append(color_str(settings.BAD_ANS_TEXT, settings.BAD_ANS_COLOR) + question_object.answers)
            self._l_score.add_incorrect()
            self._mistakes.append(question_object)

        self.update_question()
        if self._quiz.is_finished():
            self.perform_end_quiz_actions()

    def redo_test(self, questions: Optional[List[Question]]) -> None:
        questions = questions or self.__get_questions()
        self._te_answer.setFocus()
        self._l_score.clear()
        self._l_score.update()
        self._quiz = Quiz(questions, self._order)
        self._l_question.setText(self._quiz.get_question_object().get_question(category=True))
        self.update_progress_bar()
        self._te_logs.setText('')
        self._timer.start()

    def redo_errors(self) -> None:
        if len(self._mistakes) == 0:
            QInfoDialog(text='There are no errors (yet)', parent=self).exec_()
            return
        self.redo_test(questions=self._mistakes)
        self._mistakes = []

    def update_question(self):
        self._quiz.set_next_question()
        self.update_progress_bar()
        self._l_score.update()
        try:
            self._l_question.setText(self._quiz.get_question_object().get_question(category=True))
        except AttributeError:
            self._l_question.setText('')

    def update_progress_bar(self) -> None:
        self._progress.setMaximum(len(self._quiz.questions))
        question_index = self._quiz.get_current_question_index()
        question_count = len(self._quiz.questions)
        self._progress.setValue(question_index)
        self._progress.setFormat("{:.2f}% ({}/{})".format(
            100 * (question_index/question_count),
            question_index,
            question_count,
        ))

    def perform_end_quiz_actions(self):
        self._timer.stop()
        if settings.SAVE_ERRORS:
            with open(settings.ERROR_FILE_LOCATION, 'w', encoding='utf-8') as f:
                for q in self._mistakes:
                    f.write('\n')
                    f.write(str(q))
