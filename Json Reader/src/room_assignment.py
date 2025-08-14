class RoomAssignmentService:
    def assign(self, rooms_data, students_data):
        students_by_room= {}
        for student in students_data:
            room_id = student["room"]
            if room_id not in students_by_room:
                students_by_room[room_id] = []
            students_by_room[room_id].append({
                "id": student["id"],
                "name": student["name"]
            })

        result = []
        for room in rooms_data:
            result.append({
                "id": room["id"],
                "name": room["name"],
                "students": students_by_room.get(room["id"], [])
            })
        return result