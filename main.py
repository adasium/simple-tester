#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import signal
from enum import Enum
from stat import S_ISDIR, S_ISREG, ST_MODE
from typing import Union

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QStackedLayout,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

import settings
from custom_widgets import (
    CustomQTreeWidgetItem,
    HeightFillerWidget,
    QInfoDialog,
    QQuestionRange,
    RadioGroupWidget,
    ValueRadioButton,
)
from database import Database
from enums import Direction, Order
from quiz_window import QuizWidget
from utils import get_active_screen, group_widgets, move_to_screen

signal.signal(signal.SIGINT, signal.SIG_DFL)


class App(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.title = "Simple tester"

        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle(self.title)
        self.setGeometry(*settings.WINDOW_GEOMETRY)
        if not settings.WINDOW_RESIZABLE:
            self.setFixedSize(self.size())
        self.tree = QTreeWidget()
        self.tree.headerItem().setHidden(True)

        # init layout and create widgets
        main_hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        right_column = QVBoxLayout()
        self.fill_tree_view(self.tree, settings.DATA_PATH)

        # add stuff
        # TODO(#1): 'Load database' button doesn't update file list
        b_select_all = QPushButton('All')
        b_select_all.clicked.connect(self.select_all)
        b_select_none = QPushButton('None')
        b_select_none.clicked.connect(self.select_none)

        self.r_shuffled = QRadioButton('shuffled')
        self.r_shuffled.setChecked(True)

        b_start_test = QPushButton('Start test')
        b_start_test.clicked.connect(self.generate_test)

        self.range_widget = QQuestionRange(first_label='start', second_label='end')

        # append
        vbox.addWidget(self.tree)

        tree_view_buttons_layout = QGridLayout()
        tree_view_buttons_layout.addWidget(b_select_all, 0, 0)
        tree_view_buttons_layout.addWidget(b_select_none, 0, 1)
        vbox.addLayout(tree_view_buttons_layout)

        self.range_gb = group_widgets(
            *[
                self.range_widget,
            ],
            title='question range',
            layout=QStackedLayout,
            checkable=True,
            kwargs={
                'max_width': 150,
            },
        )
        right_column.addWidget(
            self.range_gb,
        )
        right_column.addWidget(
            group_widgets(
                *[
                    QRadioButton('sequential'),
                    self.r_shuffled,
                ],
                title='question order',
                kwargs={
                    'max_width': 150,
                },
            )
        )
        self._direction_radio_group = RadioGroupWidget(widgets=[
            ValueRadioButton(Direction.LEFT_TO_RIGHT, 'left ⟶ right'),
            ValueRadioButton(Direction.RIGHT_TO_LEFT, 'right ⟶ left'),
            ValueRadioButton(Direction.RANDOM, 'random'),
        ])
        right_column.addWidget(
            group_widgets(
                *self._direction_radio_group.widgets,
                title='question direction',
                kwargs={
                    'max_width': 150,
                },
            )
        )
        right_column.addWidget(HeightFillerWidget())
        right_column.addWidget(b_start_test)

        # assemble
        main_hbox.addLayout(vbox)
        main_hbox.addLayout(right_column)
        self.setLayout(main_hbox)

        # show app
        posx, posy, *_ = settings.WINDOW_GEOMETRY
        move_to_screen(widget=self, posx=posx, posy=posy)
        self.show()

    def generate_test(self) -> None:
        if not self._is_anything_checked(self.tree.invisibleRootItem()):
            QInfoDialog(text='You have to select at least one file').exec_()
            return None

        database = Database(self.tree)
        if len(database.questions) == 0:
            QInfoDialog(text='No questions found in selected files').exec_()
            return None

        order = Order.RANDOM if self.r_shuffled.isChecked() else Order.SEQUENTIAL
        range = self.range_widget.get_range() if self.range_gb.isChecked() else None
        QuizWidget(database, order, range=range, direction=self._direction_radio_group.selected.value).show()

    def fill_tree_view(self, tree: Union[QTreeWidgetItem, CustomQTreeWidgetItem], path: str) -> None:
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

    def check_subtree(self, tree_item: QTreeWidgetItem, state: Qt.CheckState) -> None:
        tree_item.setCheckState(0, state)
        for i in range(tree_item.childCount()):
            tree_item.child(i).setCheckState(0, state)

    def _is_anything_checked(self, tree_item: QTreeWidgetItem) -> bool:
        count = 0
        for i in range(tree_item.childCount()):
            if tree_item.child(i).checkState(0) in (Qt.Checked, Qt.PartiallyChecked):
                count += 1
        return count != 0


if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    app.exec_()
