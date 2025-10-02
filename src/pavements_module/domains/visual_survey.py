import uuid
from datetime import datetime

class VisualSurvey():
    def __init__(self, id: uuid.UUID, survey_date: datetime, 
                 is_open: bool, road_stretch_id: uuid.UUID):
        self.id = id
        self.date = survey_date
        self.is_open = is_open
        self.road_stretch_id = road_stretch_id 

        self.road_stretch = None
        self.registers = None
    
    def load_registers(self, registers):
        self.registers = registers
        return self