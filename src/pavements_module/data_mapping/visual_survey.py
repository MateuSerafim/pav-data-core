from sqlalchemy import Column
from sqlalchemy import UUID, DateTime, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone

from ..domains.visual_survey import VisualSurvey
from ...utils.base_entity import BaseEntity

class VisualSurveyMapping(BaseEntity):
    __tablename__ = "visual_surveys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    suyvey_date = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    is_open = Column(Boolean, default=True)

    stretch_id = Column(UUID(as_uuid=True), ForeignKey("road_stretchs.id"))
    stretch = relationship("RoadStretchMapping", back_populates="surveys")

    image_registers = relationship("VisualRegisterMapping", 
                                   back_populates="visual_survey", 
                                   cascade="all, delete-orphan")

    def to_entity(self) -> VisualSurvey:
        return VisualSurvey(self.id, self.suyvey_date, self.is_open, self.stretch_id)
    
    @staticmethod
    def create(suyvey_date: datetime, stretch_id: uuid.UUID):
        return VisualSurveyMapping(id=uuid.uuid4(), suyvey_date=suyvey_date, 
                                   is_open=True, stretch_id=stretch_id)

