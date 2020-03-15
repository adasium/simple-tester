import os
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
        self._questions = []
        root = tree_widget.invisibleRootItem()
        self._load_directory_recursively(root)

    def _load_directory_recursively(self, tree_item: Union[QTreeWidgetItem, CustomQTreeWidgetItem]) -> None:
        if tree_item.childCount() == 0 and tree_item.is_checked():
            file_path = tree_item.get_path()
            encoding = (settings.UTF8_ENCODING if is_utf8(file_path)
                        else settings.WINDOWS_ENCODING)
            with open(file_path, 'r', encoding=encoding) as f:
                _ = f.readline().strip('\n')
                for i, line in enumerate(f):
                    try:
                        if line in settings.IGNORED_LINES:
                            continue
                        split_line = [x.strip(' ')
                                      for x in line.strip('\n').split(' - ')]
                        if len(split_line) < 2:
                            print('{}:{} / Couldn\'t parse line:\n{}'.format(f.name, f.fileno(), line))
                            continue
                        filename_wo_extension = os.path.splitext(os.path.basename(file_path))[0]
                        self._questions.append(Question(*split_line, filename_wo_extension))
                    except TypeError as e:
                        print('TypeError {}:{} / Couldn\'t parse line:\n{}'.format(f.name, f.fileno(), line))
        for i in range(tree_item.childCount()):
            item = tree_item.child(i)
            file_path = item.get_path()
            self._load_directory_recursively(item)

    @property
    def questions(self) -> List[Question]:
        return self._questions
