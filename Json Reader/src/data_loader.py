from abc import ABC, abstractmethod
from pathlib import Path
import json
import xml.etree.ElementTree as ET

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

class XmlLoader(DataLoader):
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


class LoaderFactory:
    _loaders = {
        "json": JsonLoader,
        "xml": XmlLoader
    }
    
    @classmethod
    def get_loader(cls, file_type: str) -> DataLoader:
        loader_class = cls._loaders.get(file_type)
        if not loader_class:
            raise ValueError(f"Unsupported file type: {file_type}")
        return loader_class()