from score import Score
import random

class Quiz:
    def __init__(self, questions, order):
        if order == 'random':
            random.shuffle(questions)
        self._questions = questions
        self._current_index = 0
        self.score = Score()

    def _get_question(self, index):
        if index < len(self._questions):
            return self._questions[index]

    def get_question(self, index=None):
        index = index if index is not None else self._current_index
        try:
            return self._get_question(index).get_question_with_cat()
        except AttributeError:
            return None

    def get_answer(self, index=None):
        index = index if index is not None else self._current_index
        return self._get_question(index).get_answer()

    def get_question_index(self):
        return self._current_index

    def next_question(self):
        self._current_index += 1

    def question_count(self):
        return len(self._questions)

    def is_answer_correct(self, answer):
        return answer == self.get_current_question().get_answer()

    def is_finished(self):
        return self._current_index >= self.question_count()
