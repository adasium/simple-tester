#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import random
import signal
from stat import S_ISDIR, ST_MODE, S_ISREG
from PyQt5.QtWidgets import QApplication, QLabel, QTreeWidget, QTreeWidgetItem, QWidget, QFileSystemModel, QTreeView, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton, QGridLayout, QTextEdit, QProgressBar, QDialog
from PyQt5.QtCore import Qt
from database import Database
from custom_widgets import CustomQTreeWidgetItem, CustomQTextEdit, ScoreQLabel, QInfoDialog
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
        b_select_all = QPushButton('All')
        b_select_all.clicked.connect(self.select_all)
        b_select_none = QPushButton('None')
        b_select_none.clicked.connect(self.select_none)

        l_order = QLabel('Pick questions order:')
        r_file = QRadioButton('Just like in file')
        r_shuffled = QRadioButton('Shuffled')
        self.r_shuffled = r_shuffled
        r_shuffled.setChecked(True)
        b_start_test = QPushButton('Start test')
        b_start_test.clicked.connect(self.generate_test)

        # append
        vbox.addWidget(self.tree)

        tree_view_buttons_layout = QGridLayout()
        tree_view_buttons_layout.addWidget(b_select_all, 0, 0)
        tree_view_buttons_layout.addWidget(b_select_none, 0, 1)
        vbox.addLayout(tree_view_buttons_layout)

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
        if self.checkedCount(self.tree.invisibleRootItem()) == 0:
            d = QInfoDialog(text='You have to select at least one file')
            d.exec_()
            return
        database = self.load_database()
        if len(database.get_questions()) == 0:
            d = QInfoDialog(text='No questions found in selected files')
            d.exec_()
            return
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

    def select_all(self):
        self.check_subtree(self.tree.invisibleRootItem(), Qt.Checked)

    def select_none(self):
        self.check_subtree(self.tree.invisibleRootItem(), Qt.Unchecked)

    def check_subtree(self, tree_item, state):
        tree_item.setCheckState(0, state)
        for i in range(tree_item.childCount()):
            tree_item.child(i).setCheckState(0, state)

    def checkedCount(self, tree_item):
        count = 0
        for i in range(tree_item.childCount()):
            if tree_item.child(i).checkState(0) == Qt.Checked:
                count += 1
        return count


if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    app.exec_()
