class Score:
    def __init__(self):
        self.correct = 0
        self.incorrect = 0
        self.total = 0

    def good_ans(self):
        self.correct += 1
        self.total += 1

    def bad_ans(self):
        self.incorrect += 1
        self.total += 1

    def __str__(self):
        self.total = 1 if self.total == 0 else self.total
        return (
            '{} odpowiedzi poprawnych\n'.format(self.correct) +
            '{} odpowiedzi blednych\n'.format(self.incorrect) +
            '\nSkutecznosc: {}%'.format(100*self.correct/self.total)
        )
