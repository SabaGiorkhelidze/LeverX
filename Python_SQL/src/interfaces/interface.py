from abc import ABC, abstractmethod

'''

class db_connector

cursor

close connection

commit

'''

class DatabaseConnectorInterface(ABC):
    @abstractmethod
    def cursor(self):
        pass
    
    @abstractmethod
    def close_connection(self):
        pass
    
    def commit(self):
        pass
    



'''
class schemaCreator

create_db

'''


class SchemaCreatorInterface(ABC):
    
    @abstractmethod
    def create_db(self):
        pass


'''
class DataInserterInterface

inser rooms

insert students


insert(table, data)  - ? possible?


'''

class DataInserterInterface(ABC):
    @abstractmethod
    def insert_rooms(self):
        pass
    
    @abstractmethod
    def insert_students(self):
        pass
    
    
'''
class QueriExecutorInterface

get_room_with_student_count

get_top_5_rooms_smallest_avg_age

get_top_5_rooms_largest_age_diff

get_rooms_with_mixed_sexes
'''
class QueriExecutorInterface(ABC):
    
    @abstractmethod
    def get_room_with_student_count(self):
        pass
    
    @abstractmethod
    def get_top_5_rooms_smallest_avg_age(self):
        pass
    
    @abstractmethod
    def get_top_5_rooms_largest_age_diff(self):
        pass
    
    @abstractmethod
    def get_rooms_with_mixed_sexes(self):
        pass
