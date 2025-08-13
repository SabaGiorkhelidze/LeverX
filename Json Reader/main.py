from abc import ABC, abstractmethod
import json
from dataclasses import dataclass
from pathlib import Path
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

# dataclasses
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

class DataLoader(ABC):
    @abstractmethod
    def load(self, path: Path) -> list[dict]:
        pass


class JsonLoader(DataLoader):
    def load(self, path: Path):
        try:
            with path.open('r', encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {path}: {e}") from e
        return data            

class XmlDataLoader(DataLoader):
    def load(self, path: Path) -> list[dict]:
        try:
            tree = ET.parse(path)
            root = tree.getroot()
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML in {path}: {e}") from e
        
        data = []
        if root.tag == "rooms":
            for el in root.findall("room"):
                room_data = {
                    "id": int(el.get("id")),
                    "name": el.get("name")
                }
                data.append(room_data)
        elif root.tag == "students":
            for elem in root.findall("student"):
                student_data = {
                    "id": int(elem.get("id")),
                    "name": elem.get("name"),
                    "room": int(elem.get("room"))
                }
                data.append(student_data)
        else:
            raise ValueError(f"Unexpected root tag in XML file {path}: {root.tag}")
        
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


class Exporter(ABC):
    @abstractmethod
    def export(self, data: list[dict], output_path: Path = None):
        pass

class JsonExporter(Exporter):
    def export(self, data, output_path: Path = None):
        if output_path is None:
            output_path = Path(__file__).parent / "jsons" / "results.json"

        try:
            with output_path.open('w', encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise ValueError(f"Failed to write JSON to {output_path}: {e}") from e

class XmlExporter(Exporter):
    def export(self, data: list[dict], output_path: Path = None):
        if output_path is None:
            output_path = Path(__file__).parent / "jsons" / "results.xml"
            
        root = ET.Element("rooms")
        for room in data:
            room_el = ET.SubElement(root, "room", id=str(room["id"]), name=room["name"])
            students_elem = ET.SubElement(room_el, "students")
            for student in room["students"]:
                ET.SubElement(students_elem, "student", id=str(student["id"]), name=student["name"])

        rough_str = ET.tostring(root, encoding='unicode')
        pretty_xml = minidom.parseString(rough_str).toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")

        try:
            with output_path.open('w', encoding="utf-8") as f:
                f.write(pretty_xml)
        except IOError as e:
            raise ValueError(f"Failed to write XML to {output_path}: {e}") from e  

json_folder = Path(__file__).parent / "jsons"
rooms_json_path = json_folder / "rooms.json"
students_json_path = json_folder / "students.json"

json_loader = JsonLoader()
rooms_data_json = json_loader.load(rooms_json_path)
students_data_json = json_loader.load(students_json_path)

room_assignment = RoomAssignmentService()
result_json = room_assignment.assign(rooms_data_json, students_data_json)

json_exporter = JsonExporter()
json_exporter.export(result_json)

xml_exporter = XmlExporter()
xml_exporter.export(result_json)

