#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from question import Question
class CouldNotLoadDatabaseException(Exception):
    pass

class Database:
    word_bank_dir = 'slownictwo'
    questions = []
    count = 0

    def __init__(self, tree_widget):
        root = tree_widget.invisibleRootItem()
        self.__load_directory(root)

    def print_all(self):
        for question in self.questions:
            print(question)

    def __load_directory(self, tree_item):
        child_count = tree_item.childCount()
        if child_count == 0:
            with open(tree_item.get_path(), 'r') as f:
                title = f.readline().strip('\n')
                for line in f:
                    split_line = [x.strip(' ')
                                  for x in line.strip('\n').split('-')]
                    if len(split_line) < 2:
                        print('Nie mozna bylo sparsowac linii: {}'.format(line))
                        continue
                    self.questions.append(Question(*split_line))
        for i in range(child_count):
            item = tree_item.child(i)
            file_path = item.get_path()
            self.__load_directory(item)


    def get_size(self):
        return len(self.questions)
