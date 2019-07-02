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

    def get_percentage(self):
        return self.correct*100/self.total if self.total != 0.0 else 0.0

    def clear(self):
        self.correct = 0
        self.incorrect = 0
        self.total = 0

    def __str__(self):
        total = 1 if self.total == 0 else self.total
        percent = 100*self.correct/self.total
        return (
            '{} odpowiedzi poprawnych\n'.format(self.correct) +
            '{} odpowiedzi blednych\n'.format(self.incorrect) +
            '\nSkutecznosc: {0:.2f}%'.format(percent)
        )
