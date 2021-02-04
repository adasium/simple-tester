import random
from typing import List

from enums import Direction, Order
from question import Question
from score import Score


class Quiz:
    def __init__(self, questions: List[Question], order: Order, direction: Direction = Direction.LEFT_TO_RIGHT) -> None:
        if order == Order.RANDOM:
            random.shuffle(questions)
        self._questions = questions
        self._current_index = 0
        self._direction = direction
        self.score = Score()

    def current_question(self) -> Question:
        try:
            question_obj = self._questions[self._current_index]
            if self._direction == Direction.RIGHT_TO_LEFT:
                question_obj = question_obj.reversed()
            elif self._direction == Direction.RANDOM:
                if random.choice([True, False]):
                    question_obj = question_obj.reversed()
            return question_obj
        except IndexError:
            raise StopIteration from None

    def current_index(self) -> int:
        return self._current_index

    def set_next_question(self):
        self._current_index += 1

    @property
    def questions(self) -> List[Question]:
        return self._questions

    def is_finished(self):
        return self._current_index >= len(self._questions)
