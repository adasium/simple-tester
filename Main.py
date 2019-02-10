#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from stat import S_ISDIR, ST_MODE
from PyQt5.QtWidgets import QApplication, QLabel, QTreeWidget, QTreeWidgetItem, QWidget, QFileSystemModel, QTreeView, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton, QGridLayout, QTextEdit
from PyQt5.QtCore import Qt
from database import Database


class CustomQTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent, path, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.path = path

    def is_checked(self):
        return self.checkState(0) == Qt.CheckState.Checked

    def get_path(self):
        return self.path


class TestWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('New test')
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.database = None

        self.l_question = QLabel()
        self.te_logs = QTextEdit()
        self.te_answer = QTextEdit()
        self.initUI()

    def update_database(self, database):
        self.database = database
        self.show()

    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)

        # create stuff
        layout = QGridLayout()
        self.te_logs.setDisabled(True)
        b_submit_answer = QPushButton('Answer')
        b_submit_answer.clicked.connect(self.answer_question)


        # assemble
        layout.addWidget(self.te_logs, 0, 0)
        layout.addWidget(self.l_question, 1, 0)
        layout.addWidget(self.te_answer, 2, 0)
        layout.addWidget(b_submit_answer, 2, 1)


        self.setLayout(layout)

    def answer_question(self):
        self.te_logs.append(self.te_answer.toPlainText())


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Simple tester"
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.database = None
        self.test_widget = TestWidget()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.tree = QTreeWidget()

        # init layout and create widgets
        main_hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox2 = QVBoxLayout()
        self.fill_tree_view(self.tree, f'{os.getcwd()}/data')

        # add stuff
        l_test = QLabel('siemanko')
        b_load_database = QPushButton('Load database')
        b_load_database.clicked.connect(self.load_database)

        l_order = QLabel('Pick questions order:')
        r_file = QRadioButton('Just like in file')
        r_shuffled = QRadioButton('Shuffled')
        b_start_test = QPushButton('Start test')
        b_start_test.clicked.connect(self.generate_test)

        # append
        vbox.addWidget(l_test)
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
        self.test_widget.update_database(self.database)
        self.test_widget.show()
        pass

    def fill_tree_view(self, tree, path):
        directory = os.fsencode(path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            absolute_path = os.path.join(path, filename)
            mode = os.stat(absolute_path)[ST_MODE]

            new_item = CustomQTreeWidgetItem(tree, absolute_path)
            new_item.setText(0, filename)
            new_item.setFlags(new_item.flags()
                              | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            new_item.setCheckState(0, Qt.Unchecked)
            if S_ISDIR(mode):
                self.fill_tree_view(new_item, f'{path}/{filename}')

    def load_database(self):
        print('database loaded')
        self.database = Database(self.tree)
        self.database.print_all()


if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    app.exec_()
