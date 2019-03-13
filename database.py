#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
import codecs
from PyQt5.QtCore import Qt
from question import Question
from custom_widgets import ScoreQLabel
import settings


class CouldNotLoadDatabaseException(Exception):
    pass


class Database:
    def __init__(self, tree_widget, *args, **kwargs):
        self._questions = []
        root = tree_widget.invisibleRootItem()
        self._load_directory(root)

    def print_all(self):
        for question in self._questions:
            print(question)

    def __is_utf8(self, filename):
        try:
            f = codecs.open(filename, encoding='utf-8', errors='strict')
            for line in f:
                pass
            return True
        except UnicodeDecodeError:
            return False

    def _load_directory(self, tree_item):
        if tree_item.childCount() == 0 and tree_item.is_checked():
            file_path = tree_item.get_path()
            is_utf8 = self.__is_utf8(file_path)
            if is_utf8:
                f = open(file_path, 'r', encoding=settings.UTF8_ENCODING)
            else:
                f = open(file_path, 'r', encoding=settings.WINDOWS_ENCODING)
            title = f.readline().strip('\n')
            for i, line in enumerate(f):
                try:
                    if line in settings.IGNORED_LINES:
                        continue
                    split_line = [x.strip(' ')
                                  for x in line.strip('\n').split(' - ')]
                    if len(split_line) < 2:
                        print('{}:{} / Couldn\'t parse line:\n{}'.format(f.name, f.fileno(), line))
                        continue
                    filename_wo_extension = os.path.splitext(os.path.basename(file_path))[0]
                    self._questions.append(Question(*split_line, filename_wo_extension))
                except TypeError as e:
                    print('T{}:{} / Couldn\'t parse line:\n{}'.format(f.name, f.fileno(), line))
            f.close()
        for i in range(tree_item.childCount()):
            item = tree_item.child(i)
            file_path = item.get_path()
            self._load_directory(item)

    def get_size(self):
        return len(self._questions)

    def get_questions(self):
        return self._questions
