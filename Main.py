#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import random
from stat import S_ISDIR, ST_MODE
from PyQt5.QtWidgets import QApplication, QLabel, QTreeWidget, QTreeWidgetItem, QWidget, QFileSystemModel, QTreeView, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton, QGridLayout, QTextEdit, QProgressBar
from PyQt5.QtCore import Qt
from database import Database
from score import Score


class CustomQTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent, path, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.path = path

    def is_checked(self):
        return self.checkState(0) == Qt.CheckState.Checked

    def get_path(self):
        return self.path


class CustomQTextEdit(QTextEdit):
    def __init__(self, enter_method, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enter_method = enter_method

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == Qt.Key_Return:
            self.enter_method()
            self.setText('')
        else:
            super().keyPressEvent(qKeyEvent)


def color_str(string, color='black'):
    if color == 'black':
        return string
    elif color in ('green', 'red'):
        string = f'<span style="color:{color};">{string}</span>'
        return string


class ScoreQLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.score = Score()
        self.update()

    def add_correct(self):
        self.score.good_ans()

    def add_incorrect(self):
        self.score.bad_ans()

    def update(self):
        self.setText('Correct: {}\nIncorrect: {}\nScore: {}%'.format(self.score.correct, self.score.incorrect, self.score.get_percentage()))



class TestWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('New test')
        self.left=10
        self.top=10
        self.width=640
        self.height=480
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.size())
        self.database=None

        self.l_question=QLabel()
        self.te_logs=QTextEdit()
        self.te_answer=CustomQTextEdit(self.check_answer)
        self.initUI()

    def update_database(self, database):
        self.database=database
        self.show()
        self.questions=self.database.get_questions()
        self.current_question=0
        self.progress.setMaximum(len(self.questions))
        self.progress.setValue(0)

        self.l_question.setText(self.questions[self.current_question].get_question())
    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)

        # create stuff
        layout=QGridLayout()
        self.te_logs.setReadOnly(True)
        self.l_score=ScoreQLabel()
        b_submit_answer=QPushButton('Answer')
        b_submit_answer.clicked.connect(self.check_answer)
        self.progress=QProgressBar(self)
        self.progress.setMinimum(0)

        # assemble
        layout.addWidget(self.te_logs, 0, 0)
        layout.addWidget(self.l_question, 1, 0)
        layout.addWidget(self.l_score, 0, 1)
        layout.addWidget(self.te_answer, 2, 0)
        layout.addWidget(b_submit_answer, 2, 1)
        layout.addWidget(self.progress, 3, 0, 1, 2)

        self.setLayout(layout)

    def show(self):
        super().show()
        self.te_answer.setFocus()

    def check_answer(self):
        question=self.get_current_question()
        answer=self.te_answer.toPlainText()
        correct_answer=self.get_current_answer()
        self.te_logs.append(question + ": " + answer)
        if answer == correct_answer:
            string=color_str('Brawo!', 'green')
            self.l_score.add_correct()
            self.te_logs.append(string)
        else:
            self.te_logs.append(color_str('Jesteś dupa! Prawidłowa odpowiedź to: ', 'red') + correct_answer)
            self.l_score.add_incorrect()
        self.inc_question()
        self.progress.setValue(self.current_question)
        self.l_score.update()



    def get_current_question(self):
        return self.questions[self.current_question].get_question() if self.current_question < len(self.questions) else ''

    def get_current_answer(self):
        return self.questions[self.current_question].get_answer()

    def inc_question(self):
        self.current_question += 1
        self.l_question.setText(self.get_current_question())


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title="Simple tester"
        self.left=10
        self.top=10
        self.width=640
        self.height=480
        self.database=None
        self.test_widget=TestWidget()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.size())
        self.tree=QTreeWidget()

        # init layout and create widgets
        main_hbox=QHBoxLayout()
        vbox=QVBoxLayout()
        vbox2=QVBoxLayout()
        self.fill_tree_view(self.tree, f'{os.getcwd()}/data')

        # add stuff
        l_test=QLabel('siemanko')
        b_load_database=QPushButton('Load database')
        b_load_database.clicked.connect(self.load_database)

        l_order=QLabel('Pick questions order:')
        r_file=QRadioButton('Just like in file')
        r_shuffled=QRadioButton('Shuffled')
        self.r_shuffled=r_shuffled
        r_shuffled.setChecked(True)
        b_start_test=QPushButton('Start test')
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
        self.load_database()
        self.test_widget.update_database(self.database)
        self.test_widget.show()

    def fill_tree_view(self, tree, path):
        directory=os.fsencode(path)
        for file in os.listdir(directory):
            filename=os.fsdecode(file)
            absolute_path=os.path.join(path, filename)
            mode=os.stat(absolute_path)[ST_MODE]

            new_item=CustomQTreeWidgetItem(tree, absolute_path)
            new_item.setText(0, filename)
            new_item.setFlags(new_item.flags()
                              | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            new_item.setCheckState(0, Qt.Checked)
            if S_ISDIR(mode):
                self.fill_tree_view(new_item, f'{path}/{filename}')

    def load_database(self):
        print('database loaded')
        order='random' if self.r_shuffled.isChecked() else ''
        self.database=Database(self.tree, order=order)
        # self.database.print_all()


if __name__ == '__main__':
    app=QApplication([])
    ex=App()
    app.exec_()
