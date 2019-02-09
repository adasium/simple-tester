#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import os


def parse_german(word):
    return word.replace('ß', 'ss').replace('ü', 'ue').replace('ö', 'oe').replace('ä', 'ae')

class Program:
    word_bank_dir = 'slownictwo'
    points = Points()

    def __init__(self):
        self.db = Database()
        self.langs = ['niemiecki', 'polski']
        self.dest_lang = 0

    def run(self):
        try:
            self.db.load_database()
        except CouldNotLoadDatabaseException:
            print('W katalogu "slownictwo" nie znaleziono zadnego pliku ze slownictwem.')
            print('Stworz plik i sprobuj jeszcze raz.')
            return
        while True:
            answer = input('Wybierz jezyk na jaki chcesz tlumaczyc:\n\
1. Niemiecki\n\
2. Polski\n')
            if not answer in ('1', '2'):
                continue

            if answer == '1':
                self.dest_lang = 0
            else:
                self.dest_lang = 1
            break


        new_test = True
        new_categories = True
        while True:
            if new_categories:
                preferences = self.get_test_preferences()
            if new_test:
                test = self.get_random_questions(preferences)
            self.solve_test(test)
            self.show_results()
            while True:
                print()
                print('Co teraz?')
                print('1. Jeszcze raz ten sam test')
                print('2. Jeszcze raz ten sam test, ale pytania w losowej kolejnosci')
                print('3. Nowy test z tych samych kategorii')
                print('4. Nowy test z innych kategorii')
                print('5. Zmien tryb na tłumaczenie na {}'.format(self.langs[(self.dest_lang + 1) % 2]))
                print('0. Wyjscie')
                try:
                    choice = int(input())
                    if choice == 0:
                        return
                    if choice == 1:
                        new_categories = False
                        new_test = False
                        break
                    if choice == 2:
                        new_categories = False
                        new_test = False
                        random.shuffle(test)
                        break
                    if choice == 3:
                        new_categories = False
                        new_test = True
                        break
                    if choice == 4:
                        new_categories = True
                        new_test = True
                        break
                    if choice == 5:
                        self.dest_lang = (self.dest_lang + 1) % 2
                        continue
                except ValueError:
                    continue



        if os.name == 'nt':
            os.system('pause')

    def get_test_preferences(self):
        all_categories = self.db.get_categories()
        chosen_categories = []

        print('Dostepne kategorie: ')
        for i, cat in enumerate(all_categories):
            print('   {}. {}'.format(i + 1, cat.get_title()))

        while True:
            try:
                ans = input('Czy chcesz test z wszystkich kategorii? [y/n]')
                if ans not in ('y', 'n'):
                    continue
                if ans == 'y':
                    chosen_categories = all_categories
                    break
                if ans == 'n':
                    choice = input('Podaj numery kategorii (przedzialy rozdzielone przecinkami): ')
                    cats_no = range_from_string(choice)
                    chosen_categories = [cat for index, cat in enumerate(all_categories) if index+1 in cats_no]
                    break
            except ValueError:
                continue

        return chosen_categories

    def get_random_questions(self, categories, size=10):
        test = []
        print('Podaj ile chcesz zagadnień z kategorii:')
        for c in categories:
            count = int(input(c.title + ': '))
            questions = c.get_questions()
            if len(questions) < count:
                count = len(questions)
            random_questions = random.sample(questions, count)
            test += random_questions

        return test

    def solve_test(self, test):
        for test_question in test:
            try:
                if self.dest_lang == 0:
                    test_question = test_question.get_inverted()

                question = test_question.get_question()
                answer = test_question.get_answer()
                user_answer = input(question + ' - ')
                if user_answer == parse_german(answer):
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

if __name__ == "__main__":
    Program().run()
