from enum import Enum
from uuid import UUID

class ObjectType(Enum):
    POTHOLE = 1
    PATCH = 2
    ISOLATED_CRACK = 3
    CONNECTED_CRACK = 4

class ObjectRegister():
    def __init__(self, id: UUID, class_type: int, 
                 confidence: float,
                 coord_x1: int, coord_y1: int, 
                 coord_x2: int, coord_y2: int):
        self.id: UUID = id
        self.class_type: ObjectType = ObjectType(class_type)
        self.confidence: float = confidence
        self.position: list = [[coord_x1, coord_y1], 
                               [coord_x2, coord_y2]]
        
    def get_color(self):
        match self.class_type.value:
            case 1:
                return (0, 0, 255) # vermerlho
            case 2:
                return (255, 0, 0) # azul
            case 3:
                return (0, 255, 0) #verde
            case _:
                return (0, 255, 255)