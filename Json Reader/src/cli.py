import argparse
from pathlib import Path
from .data_loader import LoaderFactory
from .room_assignment import RoomAssignmentService
from .exporter import ExporterFactory

def parse_args():
    parser = argparse.ArgumentParser(description="select arguments which type of file generation you want")
    
    parser.add_argument("--input-format", type=str, choices=['json', 'xml'], default="json")
    parser.add_argument("--student-path", type=str, default=Path(__file__).parent.parent / "jsons" / "students.json")
    parser.add_argument("--rooms-path", type=str, default=Path(__file__).parent.parent / "jsons" / "rooms.json")
    parser.add_argument("--output-format", choices=['json', 'xml'], default="json")
    parser.add_argument('--output-destination-path', type=str, default=str(Path(__file__).parent.parent / "jsons" / "results"))
    
    return parser.parse_args()

def run():
    args = parse_args()
    
    students_path = Path(args.student_path)
    rooms_path = Path(args.rooms_path)
    output_path = Path(args.output_destination_path).with_suffix(f".{args.output_format}")
    
    if not students_path.is_file() or not rooms_path.is_file():
        print(f"Error: Input file not found: {students_path}, {rooms_path}")
        return
        
        
    loader = LoaderFactory.get_loader(args.input_format)
    rooms_data = loader.load(rooms_path)
    students_data = loader.load(students_path)
        
    result = RoomAssignmentService().assign(rooms_data, students_data)
        
    exporter = ExporterFactory.get_exporter(args.output_format)
    output_path.parent.mkdir(parents=True, exist_ok=True) 
    exporter.export(result, output_path)
    print(f"Results successfully exported to {output_path}")
        