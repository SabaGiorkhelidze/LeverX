from dataclasses import dataclass

@dataclass(frozen=True)
class Room:
    id: int
    name: str

@dataclass(frozen=True)
class Student:
    id: int
    name: str
    room: int
    
@dataclass
class Result:
    id: int
    name: str #room name (number)
    student: list[Student]
