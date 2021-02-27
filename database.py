import logging
import os
from pathlib import Path
from typing import List
from typing import Union

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtWidgets import QTreeWidgetItem

import settings
from custom_widgets import TreeWidgetItem
from question import Question
from utils import is_utf8


class CouldNotLoadDatabaseException(Exception):
    pass


class Database:
    def __init__(self, tree_widget: QTreeWidget, *args, **kwargs) -> None:
        self._questions: List[Question] = []
        self._paths: List[Path] = []
        root = tree_widget.invisibleRootItem()
        self._load_directory_recursively(root)

    def _load_directory_recursively(self, tree_item: TreeWidgetItem) -> None:
        tree_item_status = tree_item.checkState(0)

        if tree_item_status == Qt.Checked and tree_item.path.is_file():
            encoding = (
                settings.UTF8_ENCODING if is_utf8(tree_item.path)
                else settings.WINDOWS_ENCODING
            )
            self._paths.append(tree_item.path)
            with open(tree_item.path, 'r', encoding=encoding) as f:
                for i, line in enumerate(f):
                    try:
                        if line in settings.IGNORED_LINES:
                            continue
                        question, answers = [
                            x.strip(' ')
                            for x in line.strip('\n').split(' - ')
                        ]

                        self._questions.append(
                            Question(
                                question=[question.strip() for question in question.split(',')],
                                answers=[answer.strip() for answer in answers.split(',')],
                                category=tree_item.path.stem,
                            ),
                        )
                    except ValueError as e:
                        logging.warning("{}:{} / Couldn't parse line:\n{}".format(f.name, f.fileno(), line))

        for i in range(tree_item.childCount()):
            item = tree_item.child(i)
            self._load_directory_recursively(item)

    @property
    def questions(self) -> List[Question]:
        return self._questions

    @property
    def paths(self) -> List[Path]:
        return self._paths
