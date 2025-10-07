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
        self.registers = []
    
    def load_registers(self, registers):
        self.registers = registers
        return self
    
    def registers_status(self) -> int:
        status_list = [r.process_status for r in self.registers]
        if 2 in status_list:
            return 2
        if 0 in status_list:
            return 0
        return 1
    
    def quant_item_by_class(self, item_class) -> int:
        q = 0
        for r in self.registers:
            q += r.quant_item_by_class(item_class)
        return q
