from dataclasses import dataclass

@dataclass(frozen=True)
class Room:
    id: int
    name: str

@dataclass(frozen=True)
class Student:
    birthday: str
    id: int
    name: str
    room: int
    sex: str