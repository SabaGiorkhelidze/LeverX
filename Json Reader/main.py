import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Room:
    id: int
    name: str

@dataclass(frozen=True)
class Student:
    id: int
    name: str
    room: int
    


class JsonLoader:
    def load(self, path: Path):
        try:
            with path.open('r', encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {path}: {e}") from e
        return data            

class JsonParser:
    def parse(self, data, instance_constructor):
        try:
            parsed_obj = [instance_constructor(**info) for info in data]
        except TypeError as e:
            raise ValueError(f"not match {instance_constructor.__name__} fields: {e}") from e
        return parsed_obj

class RoomAssignmentService:
    def assign(self):
        pass



class JsonEXporter:
    def export(self, rooms):
        pass



# json_path = Path(__file__).parent / "jsons" / "rooms.json"

json_folder = Path(__file__).parent / "jsons"
rooms_path = json_folder / "rooms.json"
students_path = json_folder / "students.json"

loader = JsonLoader()
parser = JsonParser()

rooms_data = loader.load(rooms_path)
students_data = loader.load(students_path)


print("Rooms JSON:")
print(rooms_data)

print("\nStudents JSON:")
print(students_data)


rooms = parser.parse(rooms_data, Room)
students = parser.parse(students_data, Student)

# print("\nRooms (dataclasses):")
# for r in rooms:
#     print(r)

# print("\nStudents (dataclasses):")
# for s in students:
#     print(s)