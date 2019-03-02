from score import Score

class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.current_index = 0
        self.score = Score()

    def _get_question(self, index):
        if index < len(self.questions):
            return self.questions[index]

    def get_current_question(self):
        return self._get_question(self.index)

    def next_question(self):
        if self.current_index < len(self.questions) - 1:
            self.current_index += 1

    def check_answer(self, answer):
        if answer == self.get_current_question().get_answer()
