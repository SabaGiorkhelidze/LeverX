import json
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
    
@dataclass
class Result:
    id: int
    name: str #room name (number)
    student: list[Student]

class JsonLoader:
    def load(self, path: Path):
        try:
            with path.open('r', encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {path}: {e}") from e
        return data            


class RoomAssignmentService:
    def assign(self, rooms_data: list[Room], students_data: list[Student]) -> list[Result]:
        result: list[Result] = []

        for room in rooms_data:
            student_match = [{"id": s["id"], "name": s["name"]} for s in students_data if room['id'] == s["room"]]
            result.append({
                "id": room["id"],
                "name": room["name"],
                "students": student_match
            })
        return result




class JsonEXporter:
    def export(self, data, output_path: Path = None):
        if output_path is None:
            output_path = Path(__file__).parent / "jsons" / "results.json"

        try:
            with output_path.open('w', encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise ValueError(f"Failed to write JSON to {output_path}: {e}") from e



json_folder = Path(__file__).parent / "jsons"
rooms_path = json_folder / "rooms.json"
students_path = json_folder / "students.json"

loader = JsonLoader()


rooms_data = loader.load(rooms_path)
students_data = loader.load(students_path)


room_assignment = RoomAssignmentService()

result = room_assignment.assign(rooms_data, students_data)

exporter = JsonEXporter()
exporter.export(result)

