from __future__ import annotations

import re
from typing import Any
from typing import List
from typing import Optional


class Question:
    def __init__(self, question: List[str], answers: List[str], category: Optional[str] = None, **kwargs: Any) -> None:
        assert len(answers) > 0
        self._question = question
        self._answers = answers
        self._category = category

    @property
    def question(self) -> str:
        return ', '.join(self._question)

    @property
    def answer(self) -> str:
        return self._answers[0]

    @property
    def answers(self) -> str:
        return ', '.join(self._answers)

    def get_question(self, category: bool = False) -> str:
        if category:
            return f'{self.question} ({self._category})'
        else:
            return self.question

    def is_correct(self, answer: str) -> bool:
        return answer in [self.get_parenless(answer) for answer in self._answers]

    def __str__(self) -> str:
        return f'{self.question} - {self.answers}'

    def dumps(self) -> str:
        return '{question} - {answers}'.format(
            question=self.question,
            answers=self.answers,
        )

    def reversed(self) -> 'Question':
        return Question(question=self._answers, answers=self._question, category=self._category)

    @staticmethod
    def get_parenless(expression: str) -> str:
        return re.sub(' ?\(\w+\)', '', expression)
