#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from PyQt5.QtCore import Qt
from question import Question
from custom_widgets import ScoreQLabel

enc = ['windows-1250', 'utf-8']
ENC = enc[0]

class CouldNotLoadDatabaseException(Exception):
    pass

class Database:
    def __init__(self, tree_widget, *args, **kwargs):
        self.questions = []
        self.order = kwargs.get('order', None)
        print(self.order)
        root = tree_widget.invisibleRootItem()
        self.__load_directory(root)

    def print_all(self):
        for question in self.questions:
            print(question)

    def __load_directory(self, tree_item):
        if tree_item.childCount() == 0 and tree_item.is_checked():
            with open(tree_item.get_path(), 'r', encoding=ENC) as f:
                title = f.readline().strip('\n')
                for i, line in enumerate(f):
                    try:
                        split_line = [x.strip(' ') for x in line.strip('\n').split('-')]
                        if len(split_line) < 2:
                            print('{}:{} / Couldn\'t parse line: {}'.format(f.name, f.fileno(), line))
                            continue
                        self.questions.append(Question(*split_line))
                    except TypeError as e:
                        print(f'TYPE ERROR: {e}')
                        print(line)
        for i in range(tree_item.childCount()):
            item = tree_item.child(i)
            file_path = item.get_path()
            # if item.checkState(0) ==
            self.__load_directory(item)


    def get_size(self):
        return len(self.questions)

    def get_questions(self):
        questions = self.questions
        if self.order == 'random':
           random.shuffle(questions)
           return questions
        return self.questions
