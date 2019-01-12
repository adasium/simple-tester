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


class Database:
    word_bank_dir = 'slownictwo'
    dictionary = {}
    count = 0

    def load_database(self):
        if os.path.isdir(self.word_bank_dir):
            for filename in os.listdir(self.word_bank_dir):
                with open(os.path.join(self.word_bank_dir, filename), 'r') as f:
                    title = f.readline().strip('\n')
                    self.dictionary[filename] = {
                        'title': title,
                        'value': []
                    }
                    for line in f:
                        split_line = [x.strip(' ') for x in line.strip('\n').split('-')]
                        self.dictionary[filename]['value'].append(
                            Question(*split_line))
                        self.count += 1
        else:
            os.makedirs(self.word_bank_dir)
            print('W katalogu "slownictwo" nie znaleziono żadnego pliku ze słownictwem.')
            print('Stwórz plik i spróbuj jeszcze raz.')

    def get_size(self):
        return self.count

    def get_random_questions(self, prefs, size=10):
        # TODO: validate number is le count of chosen categories
        if size > self.count:
            size = self.count

        all_words = []
        for unit_name in prefs:
            words = self.dictionary[unit_name]['value']
            all_words += words

        return random.sample(all_words, size)

class Question:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def get_question(self):
        return self.question

    def get_answer(self):
        return self.answer

    def invert(self):
        return Question(self.answer, self.question)

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
        self.total = 1 if self.total == 0 else self.total
        return (
            '{} odpowiedzi poprawnych\n'.format(self.correct) +
            '{} odpowiedzi błędnych\n'.format(self.incorrect) +
            '\nSkuteczność: {}%'.format(100*self.correct/self.total)
        )


class Program:
    word_bank_dir = 'slownictwo'
    points = Points()

    def __init__(self):
        self.db = Database()

    def run(self):
        self.db.load_database()
        preferences = self.get_test_preferences()
        test = self.db.get_random_questions(preferences, 10)
        self.solve_test(test)
        self.show_results()

        if os.name == 'nt':
            os.system('pause')

    def show_results(self):
        print()
        print('=== WYNIKI ===')
        print(self.points)

    def solve_test(self, test):
        for test_question in test:
            try:

                #from_lang = Dict.RANDOM
                #to_lang = Dict.german.value if from_lang == Dict.polish.value else Dict.polish.value
                from_lang = 0
                to_lang = 1

                question = test_question.get_question()
                answer = test_question.get_answer()
                user_answer = input(question + ' - ')
                if user_answer == answer:
                    print('  Brawo!')
                    self.points.good_ans()
                else:
                    print('Jesteś dupa. Prawidłowa odpowiedź to: {}'.format(answer))
                    self.points.bad_ans()
            except KeyboardInterrupt:
                return

    def get_test_preferences(self):
        all_categories = list(self.db.dictionary.keys())
        print('Dostępne kategorie: ')
        for i,cat in enumerate(all_categories):
            print('   {}'.format(i), self.db.dictionary[cat]['title'])

        while True:
            ans = input('Czy chcesz test z wszystkich kategorii? [y/n]')
            if ans in ('y', 'n'):
                break

        if ans == 'y':
            return all_categories

        chosen_categories = []
        # Wybierz kategorie
        print('\nWybierz kategorie:')
        for cat in all_categories:
            ans = input(self.db.dictionary[cat]['title'] + '? [y/n]')
            if ans == 'y' or ans == '':
                chosen_categories.append(cat)

        return chosen_categories


if __name__ == "__main__":
    Program().run()
