from typing import Any, List, Optional


# TODO(#19): Question should be renamed to Flashcard
# TODO(#20): Implement test suite
class Question:
    def __init__(self, question: str, answers: List[str], category: Optional[str] = None, **kwargs: Any) -> None:
        assert len(answers) > 0
        self._question = question
        self._answers = answers
        self._category = category

    @property
    def question(self) -> str:
        return self._question

    @property
    def answer(self) -> str:
        return self._answers[0]

    @property
    def answers(self) -> str:
        return ', '.join(self._answers)

    def get_question(self, category: bool = False) -> str:
        if category:
            return f'{self._question} ({self._category})'
        else:
            return self._question

    def is_correct(self, answer: str) -> bool:
        return answer in self._answers

    def get_answer(self) -> str:
        return self._answers[0]

    def __str__(self) -> str:
        return f'{self._question} - {self._answers}'

    def dumps(self) -> str:
        return '{question} - {answers}'.format(
            question=self._question,
            answers=', '.join(self._answers),
        )
