from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Type

from serializable import JSONSerializable
from settings import STATS_PATH


@dataclass
class Entry(JSONSerializable):
    correct: int = 0
    incorrect: int = 0
    quiz_path: Path = field(default_factory=Path)
    time_total: timedelta = field(default_factory=timedelta)
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def total(self) -> int:
        return self.correct + self.incorrect

    @classmethod
    def from_json(cls: Type[Entry], json: Dict[str, Any]) -> Entry:
        correct = json.get('correct', 0)
        incorrect = json.get('incorrect', 0)
        days, seconds, microseconds = [int(val) for val in json.get('time_total', '0:00:01.520000').split(':')]
        quiz_path = Path(json.get('quiz_path', Path()))
        timestamp = datetime.fromisoformat(json.get('timestamp', datetime.now().isoformat()))

        return Entry(
            correct,
            incorrect,
            quiz_path,
            time_total=timedelta(days=days, seconds=seconds, microseconds=microseconds),
            timestamp=timestamp,
        )

    def __add__(self, o: Entry) -> Entry:
        return Entry(
            correct=self.correct + o.correct,
            incorrect=self.correct + o.incorrect,
            quiz_path=o.quiz_path,
            time_total=self.time_total + o.time_total,
            timestamp=o.timestamp,
        )


@dataclass
class Stats(JSONSerializable):
    entries: List[Entry] = field(default_factory=list)

    @classmethod
    def from_json(cls: Type[Stats], json: Dict[str, Any]) -> Stats:
        entries = json.get('entries', [])

        return Stats(
            [Entry.from_json(entry) for entry in entries],
        )

    def add(self, entry: Entry) -> None:
        self.entries.append(entry)


STATS = Stats.load(STATS_PATH)
