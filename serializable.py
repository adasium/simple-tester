import json
from abc import ABC
from abc import abstractmethod
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Generic
from typing import overload
from typing import Protocol
from typing import Type
from typing import TypeVar
from typing import Union

from utils import Timedelta


T = TypeVar('T', bound='_JSONSerializable', covariant=True)


class _JSONSerializable(Protocol[T]):
    def to_json(self) -> Dict[str, Any]: ...

    @classmethod
    def from_json(cls: Type[T], json: Dict[str, Any]) -> T: ...


@overload
def _jsonify(value: Union[str, Path, timedelta, Timedelta, datetime]) -> str: ...

@overload
def _jsonify(value: None) -> None: ...

@overload
def _jsonify(value: _JSONSerializable) -> Dict[str, Any]: ...

def _jsonify(value):
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, list):
        return [_jsonify(val) for val in value]
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, JSONSerializable):
        return value.to_json()
    if isinstance(value, (timedelta, Timedelta)):
        return '{}:{}:{}'.format(value.days, value.seconds, value.microseconds)
    return value


class JSONSerializable(ABC, _JSONSerializable):

    def to_json(self) -> Dict[str, Any]:
        return {
            key: _jsonify(getattr(self, key))
            for key in self.__annotations__
        }

    @classmethod
    @abstractmethod
    def from_json(cls: Type[T], json: Dict[str, Any]) -> T:
        pass

    @classmethod
    def load(cls: Type[T], file_path: Path) -> T:
        try:
            with open(file_path) as f:
                return cls.from_json(json.load(f))
        except FileNotFoundError:
            return cls()

    def dump(self, path: Path) -> None:
        with open(path, 'w') as f:
            f.write(json.dumps(self.to_json(), indent=4, sort_keys=True))
