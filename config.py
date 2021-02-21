from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Optional

from settings import CONFIG_PATH


@dataclass
class Config:
    data_path: Optional[Path] = field(default_factory=Path)

    def __post_init__(self) -> None:
        if self.data_path is not None:
            if not Path(self.data_path).exists():
                logging.warning('Path %s does not exist', self.data_path)
                self.data_path = None

    def to_json(self) -> Dict[str, Any]:
        return {
            key: str(getattr(self, key))
            for key in self.__annotations__
        }

    @staticmethod
    def from_json(json: Dict[str, Any]) -> Config:
        return Config(
            json.get('data_path'),
        )

    @staticmethod
    def load(file_path: Path) -> Config:
        try:
            with open(file_path) as f:
                return Config.from_json(json.load(f))
        except FileNotFoundError:
            return Config()


CONFIG = Config.load(CONFIG_PATH)
