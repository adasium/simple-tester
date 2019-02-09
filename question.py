class Question:
    def __init__(self, question, answer, dest='polski'):
        self.question = question
        self.answer = answer
        self.dest = dest

    def get_question(self):
        return self.question

    def get_answer(self):
        return self.answer

    def dest_lang(self):
        return self.dest

    def get_inverted(self):
        new_dest = 'niemiecki' if self.dest == 'polski' else 'polski'
        return Question(self.answer, self.question, new_dest)
