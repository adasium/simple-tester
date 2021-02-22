from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import overload

from settings import CONFIG_PATH


@overload
def _jsonify(value: str) -> str: ...

@overload
def _jsonify(value: None) -> None: ...

@overload
def _jsonify(value: Path) -> str: ...

def _jsonify(value):
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, list):
        return [_jsonify(val) for val in value]
    return value


@dataclass
class Config:
    data_path: Optional[Path] = None
    recent_files: List[Path] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.data_path is not None:
            if not Path(self.data_path).exists():
                logging.warning('Path %s does not exist', self.data_path)
                self.data_path = None

    def to_json(self) -> Dict[str, Any]:
        return {
            key: _jsonify(getattr(self, key))
            for key in self.__annotations__
        }

    @staticmethod
    def from_json(json: Dict[str, Any]) -> Config:
        data_path = json.get('data_path')
        recent_files = json.get('recent_files', [])

        return Config(
            Path(data_path) if data_path is not None else None,
            [Path(file) for file in recent_files],
        )

    @staticmethod
    def load(file_path: Path) -> Config:
        try:
            with open(file_path) as f:
                return Config.from_json(json.load(f))
        except FileNotFoundError:
            return Config()

    def dump(self) -> None:
        with open(CONFIG_PATH, 'w') as f:
            f.write(json.dumps(self.to_json(), indent=4, sort_keys=True))



CONFIG = Config.load(CONFIG_PATH)
