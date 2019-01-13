#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import os


def parse_german(word):
    return word.replace('ß', 'ss').replace('ü', 'ue').replace('ö', oe).replace('ä', ae)


class CouldNotLoadDatabaseException(Exception):
    pass


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
            '{} odpowiedzi blednych\n'.format(self.incorrect) +
            '\nSkutecznosc: {}%'.format(100*self.correct/self.total)
        )


class Program:
    word_bank_dir = 'slownictwo'
    points = Points()

    def __init__(self):
        self.db = Database()

    def run(self):
        try:
            self.db.load_database()
            preferences = self.get_test_preferences()
            test = self.get_random_questions(preferences, 10)
            self.solve_test(test)
            self.show_results()

        except CouldNotLoadDatabaseException:
            print('W katalogu "slownictwo" nie znaleziono zadnego pliku ze slownictwem.')
            print('Stworz plik i sprobuj jeszcze raz.')

        if os.name == 'nt':
            os.system('pause')

    def get_test_preferences(self):
        all_categories = self.db.get_categories()
        chosen_categories = []

        print('Dostepne kategorie: ')
        for i, cat in enumerate(all_categories):
            print('   {}. {}'.format(i, cat.get_title()))

        while True:
            ans = input('Czy chcesz test z wszystkich kategorii? [y/n]')
            if ans not in ('y', 'n'):
                continue
            if ans == 'y':
                return all_categories
            if ans == 'n':
                break

        print('\nWybierz kategorie:')
        for cat in all_categories:
            ans = input(cat.get_title() + '? [y/n]')
            if ans == 'y' or ans == '':
                chosen_categories.append(cat)

        return chosen_categories

    def get_random_questions(self, categories, size=10):
        questions = []
        for c in categories:
            questions += c.get_questions()

        if size > len(questions):
            size = len(questions)

        return random.sample(questions, size)

    def solve_test(self, test):
        for test_question in test:
            try:
                from_lang = 0
                to_lang = 1

                question = test_question.get_question()
                answer = test_question.get_answer()
                user_answer = input(question + ' - ')
                if user_answer == answer:
                    print('  Brawo!')
                    self.points.good_ans()
                else:
                    print('Jestes dupa. Prawidlowa odpowiedz to: {}'.format(answer))
                    self.points.bad_ans()
            except KeyboardInterrupt:
                return
            except EOFError:
                return

    def show_results(self):
        print()
        print('=== WYNIKI ===')
        print(self.points)


class Database:
    word_bank_dir = 'slownictwo'
    categories = []
    count = 0

    def load_database(self):
        if os.path.isdir(self.word_bank_dir):
            for filename in os.listdir(self.word_bank_dir):
                with open(os.path.join(self.word_bank_dir, filename), 'r') as f:
                    title = f.readline().strip('\n')
                    cat = Category(filename, title)
                    for line in f:
                        split_line = [x.strip(' ')
                                      for x in line.strip('\n').split('-')]
                        cat.add_question(Question(*split_line))
                        self.count += 1
                    self.categories.append(cat)
        else:
            os.makedirs(self.word_bank_dir)
            raise CouldNotLoadDatabaseException

    def get_categories(self):
        return self.categories

    def get_size(self):
        return self.count


class Category:
    def __init__(self, filename, title):
        self.filename = filename
        self.title = title
        self.questions = []

    def get_filename(self):
        return self.filename

    def get_title(self):
        return self.title

    def add_question(self, question):
        self.questions.append(question)

    def get_questions(self):
        return self.questions


class Question:
    def __init__(self, question, answer, dest='niemiecki'):
        self.question = question
        self.answer = answer
        self.dest = dest

    def get_question(self):
        return self.question

    def get_answer(self):
        return self.answer

    def dest_lang(self):
        return self.dest

    def invert(self):
        return Question(self.answer, self.question)


if __name__ == "__main__":
    Program().run()
