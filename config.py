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
from typing import Type

from serializable import _jsonify
from serializable import JSONSerializable
from settings import CONFIG_PATH


@dataclass
class Config(JSONSerializable):
    data_path: Optional[Path] = None
    recent_files: List[Path] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.data_path is not None:
            if not Path(self.data_path).exists():
                logging.warning('Path %s does not exist', self.data_path)
                self.data_path = None

    @classmethod
    def from_json(cls: Type[Config], json: Dict[str, Any]) -> Config:
        data_path = json.get('data_path')
        recent_files = json.get('recent_files', [])

        return Config(
            Path(data_path) if data_path is not None else None,
            [Path(file) for file in recent_files],
        )


CONFIG = Config.load(CONFIG_PATH)
