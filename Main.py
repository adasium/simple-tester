#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from stat import S_ISDIR, ST_MODE
from PyQt5.QtWidgets import QApplication, QLabel, QTreeWidget, QTreeWidgetItem, QWidget, QFileSystemModel, QTreeView, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from database import Database

class CustomQTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent, path, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.path = path

    def get_path(self):
        return self.path

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Simple tester"
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.database = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.tree = QTreeWidget()

        # init layout and create widgets
        vbox = QVBoxLayout()
        self.fill_tree_view(self.tree, f'{os.getcwd()}/data')

        # add stuff
        l_test = QLabel('siemanko')
        b_load_database = QPushButton('Load database')
        b_load_database.clicked.connect(self.load_database)

        # append
        vbox.addWidget(l_test)
        vbox.addWidget(self.tree)
        vbox.addWidget(b_load_database)

        # assemble
        self.setLayout(vbox)

        # show app
        self.show()

    def fill_tree_view(self, tree, path):
        print(path)
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
        self.database = Database(self.tree)
        self.database.load_database()



if __name__ == '__main__':
    app=QApplication([])
    ex=App()
    app.exec_()

