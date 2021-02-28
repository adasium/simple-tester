#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import signal
from pathlib import Path
from stat import S_ISDIR
from stat import S_ISREG
from stat import ST_MODE
from typing import List
from typing import Union

from PyQt5.QtCore import QEvent
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QStackedLayout
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

import settings
from config import CONFIG
from custom_widgets import HeightFillerWidget
from custom_widgets import Label
from custom_widgets import QInfoDialog
from custom_widgets import QQuestionRange
from custom_widgets import RadioGroupWidget
from custom_widgets import TreeWidget
from custom_widgets import TreeWidgetItem
from custom_widgets import ValueRadioButton
from database import Database
from enums import Direction
from enums import Order
from quiz_window import QuizWidget
from settings import CONFIG_PATH
from settings import STATS_PATH
from stats import STATS
from stats_window import StatsWindow
from utils import group_widgets
from utils import move_to_screen


signal.signal(signal.SIGINT, signal.SIG_DFL)


class App(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.title = "Simple tester"
        self._current_path = Label(str(CONFIG.data_path or ''), max_height=10)

        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle(self.title)
        self.setGeometry(*settings.WINDOW_GEOMETRY)
        if not settings.WINDOW_RESIZABLE:
            self.setFixedSize(self.size())
        self.tree = TreeWidget(path=CONFIG.data_path or settings.DATA_PATH)
        self.tree.headerItem().setHidden(True)
        self._no_data_path_widget = Label('Select data dir')

        # init layout and create widgets
        main_hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        self._main_vbox = vbox
        right_column = QVBoxLayout()
        self.fill_tree_view(self.tree)

        # add stuff
        b_select_all = QPushButton('All')
        b_select_all.clicked.connect(self.select_all)
        b_select_none = QPushButton('None')
        b_select_none.clicked.connect(self.select_none)
        b_refresh = QPushButton('Refresh')
        b_refresh.clicked.connect(self.refresh_file_tree)
        b_change_dir = QPushButton('Change dir')
        b_change_dir.clicked.connect(self.change_dir)

        self.r_shuffled = QRadioButton('shuffled')
        self.r_shuffled.setChecked(True)

        b_start_test = QPushButton('Start test')
        b_start_test.clicked.connect(self.generate_test)
        b_stats = QPushButton('Show stats')
        b_stats.clicked.connect(self.show_stats)

        self.range_widget = QQuestionRange(first_label='limit', second_label='offset')

        # append
        vbox.addWidget(self._current_path)
        vbox.addWidget(self.tree if CONFIG.data_path is not None else self._no_data_path_widget)

        tree_view_buttons_layout = QGridLayout()
        tree_view_buttons_layout.addWidget(b_select_all, 0, 0)
        tree_view_buttons_layout.addWidget(b_select_none, 0, 1)
        tree_view_buttons_layout.addWidget(b_refresh, 0, 2)
        tree_view_buttons_layout.addWidget(b_change_dir, 0, 3)
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
            ),
        )
        self._direction_radio_group = RadioGroupWidget(
            widgets=[
                ValueRadioButton(Direction.LEFT_TO_RIGHT, 'left ⟶ right'),
                ValueRadioButton(Direction.RIGHT_TO_LEFT, 'right ⟶ left'),
                ValueRadioButton(Direction.RANDOM, 'random'),
            ],
        )
        right_column.addWidget(
            group_widgets(
                *self._direction_radio_group.widgets,
                title='question direction',
                kwargs={
                    'max_width': 150,
                },
            ),
        )
        right_column.addWidget(HeightFillerWidget())
        right_column.addWidget(b_stats)
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
            QInfoDialog(text='You have to select at least one file', parent=self).exec_()
            return None

        database = Database(self.tree)
        if len(database.questions) == 0:
            QInfoDialog(text='No questions found in selected files', parent=self).exec_()
            return None

        order = Order.RANDOM if self.r_shuffled.isChecked() else Order.SEQUENTIAL
        range = self.range_widget.get_range() if self.range_gb.isChecked() else None
        QuizWidget(database, order, range=range, direction=self._direction_radio_group.selected.value)

    def fill_tree_view(self, tree: Union[TreeWidget, TreeWidgetItem]) -> None:
        directory = os.fsencode(tree.path)
        for file in sorted(os.listdir(directory)):
            filename = os.fsdecode(file)
            file_path = tree.path.joinpath(filename)
            mode = os.stat(file_path)[ST_MODE]

            if S_ISREG(mode) and filename.endswith(tuple(settings.EXCLUDED_EXTENSIONS)):
                continue

            new_item = TreeWidgetItem(file_path, tree)
            new_item.setText(0, filename)
            new_item.setFlags(new_item.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            if file_path in CONFIG.recent_files:
                new_item.setCheckState(0, Qt.Checked)
            else:
                new_item.setCheckState(0, Qt.Unchecked)
            if S_ISDIR(mode):
                self.fill_tree_view(new_item)

    def select_all(self) -> None:
        self.check_subtree(self.tree.invisibleRootItem(), Qt.Checked)

    def select_none(self) -> None:
        self.check_subtree(self.tree.invisibleRootItem(), Qt.Unchecked)

    def refresh_file_tree(self) -> None:
        CONFIG.recent_files = self._get_checked(self.tree.invisibleRootItem())
        self.tree.clear()
        self.fill_tree_view(self.tree)

    def change_dir(self) -> None:
        data_dir = QFileDialog.getExistingDirectory(parent=self, caption='Select a folder:', directory=".")
        if data_dir != '':
            data_dir = Path(data_dir)
            self._current_path.setText(str(data_dir))
            if CONFIG.data_path is None:
                self._main_vbox.removeWidget(self._no_data_path_widget)
                self._main_vbox.insertWidget(1, self.tree)
            self.tree.set_path(data_dir)
            self.refresh_file_tree()
            CONFIG.data_path = data_dir

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

    def _get_checked(self, tree_item: TreeWidgetItem) -> List[Path]:
        ret = []

        for i in range(tree_item.childCount()):
            item = tree_item.child(i)
            if item.path.is_file():
                if item.checkState(0) == Qt.Checked:
                    ret.append(item.path)
            else:
                if item.checkState(0) != Qt.Unchecked:
                    ret.extend(self._get_checked(item))
        return ret

    def show_stats(self) -> None:
        selected = self._get_checked(self.tree.invisibleRootItem())
        if len(selected) == 0:
            QInfoDialog(text='You have to select at least one file', parent=self).exec_()
            return
        if len(STATS.get_entries_for_paths(selected)) == 0:
            QInfoDialog(text='No data to show for selected entries', parent=self).exec_()
            return

        self._w = StatsWindow(selected)

    def closeEvent(self, event: QEvent) -> None:
        CONFIG.recent_files = self._get_checked(self.tree.invisibleRootItem())
        CONFIG.dump(CONFIG_PATH)
        STATS.dump(STATS_PATH)
        event.accept()


if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    app.exec_()
