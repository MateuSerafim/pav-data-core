from sqlalchemy import Column, ForeignKey
from sqlalchemy import UUID, String, Float
from sqlalchemy.orm import relationship
import uuid
from ...utils.base_entity import BaseEntity
from ..domains.visual_register import VisualRegister

class VisualRegisterMapping(BaseEntity):
    __tablename__ = "visual_registers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image_url = Column(String(), nullable=False)
    lat = Column(Float(), nullable=True)
    long = Column(Float(), nullable=True)

    survey_id = Column(UUID(as_uuid=True), ForeignKey("visual_surveys.id"))
    visual_survey = relationship("VisualSurveyMapping", back_populates="image_registers")

    objects = relationship("ObjectRegisterMapping", 
                           back_populates="visual_register", 
                           cascade="all, delete-orphan")

    def to_entity(self) -> VisualRegister:
        return VisualRegister(self.id, self.image_url, self.lat, self.long, self.survey_id)

