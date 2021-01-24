import random
from typing import List

from question import Question
from enums import Order
from score import Score


class Quiz:
    def __init__(self, questions: List[Question], order: Order) -> None:
        if order == Order.RANDOM:
            random.shuffle(questions)
        self._questions = questions
        self._current_index = 0
        self.score = Score()

    def get_question_object(self, index=None):
        index = index if index is not None else self._current_index
        try:
            return self._questions[index]
        except IndexError:
            return None

    def get_current_question_index(self):
        return self._current_index

    def set_next_question(self):
        self._current_index += 1

    def question_count(self):
        return len(self._questions)

    def is_finished(self):
        return self._current_index >= self.question_count()
