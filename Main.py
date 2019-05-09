#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import random
import signal
from stat import S_ISDIR, ST_MODE, S_ISREG
from PyQt5.QtWidgets import QApplication, QLabel, QTreeWidget, QTreeWidgetItem, QWidget, QFileSystemModel, QTreeView, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton, QGridLayout, QTextEdit, QProgressBar
from PyQt5.QtCore import Qt
from database import Database
from custom_widgets import CustomQTreeWidgetItem, CustomQTextEdit, ScoreQLabel
from quiz_window import QuizWidget
import settings

signal.signal(signal.SIGINT, signal.SIG_DFL)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Simple tester"
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480

        self.database = None
        self.data_path = f'{os.getcwd()}/data'

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        if not settings.WINDOW_RESIZABLE:
            self.setFixedSize(self.size())
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel('')

        # init layout and create widgets
        main_hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox2 = QVBoxLayout()
        self.fill_tree_view(self.tree, self.data_path)

        # add stuff
        b_load_database = QPushButton('Load database')
        b_load_database.clicked.connect(self.load_database)

        l_order = QLabel('Pick questions order:')
        r_file = QRadioButton('Just like in file')
        r_shuffled = QRadioButton('Shuffled')
        self.r_shuffled = r_shuffled
        r_shuffled.setChecked(True)
        b_start_test = QPushButton('Start test')
        b_start_test.clicked.connect(self.generate_test)

        # append
        vbox.addWidget(self.tree)
        vbox.addWidget(b_load_database)

        vbox2.addWidget(l_order)
        vbox2.addWidget(r_file)
        vbox2.addWidget(r_shuffled)
        vbox2.addWidget(b_start_test)

        # assemble
        main_hbox.addLayout(vbox)
        main_hbox.addLayout(vbox2)
        self.setLayout(main_hbox)

        # show app
        self.show()

    def generate_test(self):
        database = self.load_database()
        order = 'random' if self.r_shuffled.isChecked() else ''
        self.test_widget = QuizWidget(database, order)
        self.test_widget.show()

    def fill_tree_view(self, tree, path):
        directory = os.fsencode(path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            absolute_path = os.path.join(path, filename)
            mode = os.stat(absolute_path)[ST_MODE]

            if S_ISREG(mode) and filename.endswith(tuple(settings.EXCLUDED_EXTENSIONS)):
                continue

            new_item = CustomQTreeWidgetItem(tree, absolute_path)
            new_item.setText(0, filename)
            new_item.setFlags(new_item.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            new_item.setCheckState(0, Qt.Unchecked)
            if S_ISDIR(mode):
                self.fill_tree_view(new_item, f'{path}/{filename}')

    def load_database(self):
        return Database(self.tree)


if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    app.exec_()
