import os
from pathlib import Path
from typing import List, Union

from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem

import settings
from custom_widgets import CustomQTreeWidgetItem
from question import Question
from utils import is_utf8


class CouldNotLoadDatabaseException(Exception):
    pass


class Database:
    def __init__(self, tree_widget: QTreeWidget, *args, **kwargs) -> None:
        self._questions: List[Question] = []
        root = tree_widget.invisibleRootItem()
        self._load_directory_recursively(root)

    def _load_directory_recursively(self, tree_item: Union[QTreeWidgetItem, CustomQTreeWidgetItem]) -> None:
        if tree_item.childCount() == 0 and tree_item.is_checked():
            file_path = Path(tree_item.get_path())
            encoding = (settings.UTF8_ENCODING if is_utf8(file_path)
                        else settings.WINDOWS_ENCODING)
            with open(file_path, 'r', encoding=encoding) as f:
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
                                category=file_path.stem,
                            )
                        )
                    except ValueError as e:
                        print("{}:{} / Couldn't parse line:\n{}".format(f.name, f.fileno(), line))

        for i in range(tree_item.childCount()):
            item = tree_item.child(i)
            file_path = item.get_path()
            self._load_directory_recursively(item)

    @property
    def questions(self) -> List[Question]:
        return self._questions
