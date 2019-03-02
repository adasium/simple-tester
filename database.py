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
        print('asdf')
        self._questions = []
        root = tree_widget.invisibleRootItem()
        self._load_directory(root)

    def print_all(self):
        for question in self._questions:
            print(question)

    def _load_directory(self, tree_item):
        if tree_item.childCount() == 0 and tree_item.is_checked():
            with open(tree_item.get_path(), 'r', encoding=ENC) as f:
                title = f.readline().strip('\n')
                for i, line in enumerate(f):
                    try:
                        split_line = [x.strip(' ') for x in line.strip('\n').split(' - ')]
                        if len(split_line) < 2:
                            print('{}:{} / Couldn\'t parse line:\n{}'.format(f.name, f.fileno(), line))
                            continue
                        self._questions.append(Question(*split_line))
                    except TypeError as e:
                        print('{}:{} / Couldn\'t parse line:\n{}'.format(f.name, f.fileno(), line))
        for i in range(tree_item.childCount()):
            item = tree_item.child(i)
            file_path = item.get_path()
            self._load_directory(item)


    def get_size(self):
        return len(self._questions)

    def get_questions(self):
        return self._questions
