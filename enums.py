from enum import Enum


class Order(Enum):
    SEQUENTIAL = 'sequential'
    RANDOM = 'random'


class Direction(Enum):
    LEFT_TO_RIGHT = 0
    RIGHT_TO_LEFT = 1
    RANDOM = 2
