from sqlalchemy import Column, ForeignKey
from sqlalchemy import UUID, Integer, Float
from sqlalchemy.orm import relationship
import uuid

from ...utils.base_entity import BaseEntity
from ..domains.object_register import ObjectRegister

class ObjectRegisterMapping(BaseEntity):
    __tablename__ = "object_registers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    class_type = Column(Integer, nullable=False)

    confidence = Column(Float, nullable=False)
    
    coord_x1 = Column(Integer, nullable=False)
    coord_y1 = Column(Integer, nullable=False)

    coord_x2 = Column(Integer, nullable=False)
    coord_y2 = Column(Integer, nullable=False)

    visual_register_id = Column(UUID(as_uuid=True), ForeignKey("visual_registers.id"))

    visual_register = relationship("VisualRegisterMapping", 
                                   back_populates="objects")

    def to_entity(self) -> ObjectRegister:
        return ObjectRegister(self.id, self.class_type, 
                              self.confidence, 
                              self.coord_x1, self.coord_y1, 
                              self.coord_x2, self.coord_y2)
    
    @staticmethod
    def create(class_type:int, confidence:float, 
               positions:list, visual_register_id: uuid.UUID):
        return ObjectRegisterMapping(id=uuid.uuid4(), class_type=class_type, 
                                     confidence=confidence, coord_x1=positions[0],
                                     coord_y1 = positions[1], coord_x2 = positions[2],
                                     coord_y2 = positions[3], visual_register_id=visual_register_id)