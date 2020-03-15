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
from custom_widgets import CustomQTreeWidgetItem, CustomQTextEdit, ScoreQLabel, QInfoDialog, QQuestionRange
from quiz_window import QuizWidget
import settings

signal.signal(signal.SIGINT, signal.SIG_DFL)


class App(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.title = "Simple tester"
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480

        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        if not settings.WINDOW_RESIZABLE:
            self.setFixedSize(self.size())
        self.tree = QTreeWidget()
        self.tree.headerItem().setHidden(True)

        # init layout and create widgets
        main_hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox2 = QVBoxLayout()
        self.fill_tree_view(self.tree, settings.DATA_PATH)

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

        self.range_widget = QQuestionRange()

        # append
        vbox.addWidget(self.tree)

        tree_view_buttons_layout = QGridLayout()
        tree_view_buttons_layout.addWidget(b_select_all, 0, 0)
        tree_view_buttons_layout.addWidget(b_select_none, 0, 1)
        vbox.addLayout(tree_view_buttons_layout)

        vbox2.addWidget(self.range_widget)
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

    def generate_test(self) -> None:
        if not self._is_anything_checked(self.tree.invisibleRootItem()):
            QInfoDialog(text='You have to select at least one file').exec_()
            return None

        database = Database(self.tree)
        if len(database.questions) == 0:
            QInfoDialog(text='No questions found in selected files').exec_()
            return None

        order = 'random' if self.r_shuffled.isChecked() else ''
        QuizWidget(database, order, range=self.range_widget.get_range()).show()

    def fill_tree_view(self, tree, path) -> None:
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

    def select_all(self) -> None:
        self.check_subtree(self.tree.invisibleRootItem(), Qt.Checked)

    def select_none(self) -> None:
        self.check_subtree(self.tree.invisibleRootItem(), Qt.Unchecked)

    def check_subtree(self, tree_item, state) -> None:
        tree_item.setCheckState(0, state)
        for i in range(tree_item.childCount()):
            tree_item.child(i).setCheckState(0, state)

    def _is_anything_checked(self, tree_item) -> bool:
        count = 0
        for i in range(tree_item.childCount()):
            if tree_item.child(i).checkState(0) in (Qt.Checked, Qt.PartiallyChecked):
                count += 1
        return count != 0


if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    app.exec_()
