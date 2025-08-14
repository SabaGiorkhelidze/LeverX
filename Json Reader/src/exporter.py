from abc import ABC, abstractmethod
import json
from dataclasses import dataclass
from pathlib import Path
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


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



class ExporterFactory:
    _exporters = {
        "json": JsonExporter,
        "xml": XmlExporter
    }
    
    @classmethod
    def get_exporter(cls, output_format: str) -> Exporter:
        exporter_class = cls._exporters.get(output_format)
        if not exporter_class:
            raise ValueError(f"Unsupported output format: {output_format}")
        return exporter_class()