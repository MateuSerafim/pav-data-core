from sqlalchemy import Column
from sqlalchemy import UUID
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from src.utils.base_entity import BaseEntity
import uuid
from datetime import datetime, timezone

class VisualSurveyMapping(BaseEntity):
    __tablename__ = "visual_surveys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    suyvey_date = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    stretch_id = Column(UUID(as_uuid=True), ForeignKey("road_stretchs.id"))
    stretch = relationship("RoadStretch", back_populates="surveys")

    image_registers = relationship("VisualRegister", back_populates="visual_survey")
