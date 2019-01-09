#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum, EnumMeta
import random
import os

class RANDOM_ATTR(EnumMeta):
    @property
    def RANDOM(self):
        return random.choice([Dict.german, Dict.polish]).value

class Dict(Enum, metaclass=RANDOM_ATTR):
    polish = 0
    german = 1




class Points:
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
        return (
            '{} odpowiedzi poprawnych\n'.format(self.correct) +
            '{} odpowiedzi błędnych\n'.format(self.incorrect) +
            '\nSkuteczność: {}%'.format(100*self.correct/self.total)
        )


class Program:
    data_file = 'data.dat'
    dictionary = []
    test_words = []
    points = Points()

    def run(self):
        self.load_database()
        self.generate_test()
        self.solve_test()
        self.show_results()

        if os.name == 'nt':
            os.system('pause')

    def show_results(self):
        print()
        print('=== WYNIKI ===')
        print(self.points)

    def solve_test(self):
        for test_question in self.test_words:
            from_lang = Dict.RANDOM
            to_lang = Dict.german.value if from_lang == Dict.polish.value else Dict.polish.value
            question = test_question[from_lang]
            answer = test_question[to_lang]
            user_answer = input(question + ' - ')
            if user_answer == answer:
                print('Brawo!')
                self.points.good_ans()
            else:
                print('Jesteś dupa. Prawidłowa odpowiedź to: {}'.format(answer))
                self.points.bad_ans()

    def generate_test(self):
        count = int(input('Ile chcesz wylosować słów? '))
        for _ in range(count):
            self.test_words.append(random.choice(self.dictionary))

    def load_database(self):
        with open(self.data_file, 'r') as f:
            for line in f:
                split_line = [x.lstrip(' ').rstrip(' ')
                              for x in line.strip('\n').split('-')]
                self.dictionary.append(tuple(split_line))


if __name__ == "__main__":
    Program().run()
