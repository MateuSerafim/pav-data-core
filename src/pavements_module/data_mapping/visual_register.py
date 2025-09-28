from sqlalchemy import Column, ForeignKey
from sqlalchemy import UUID, String, Float
from sqlalchemy.orm import relationship
import uuid
from src.utils.base_entity import BaseEntity

class VisualRegisterMapping(BaseEntity):
    __tablename__ = "visual_registers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image_url = Column(String(), nullable=False)
    lat = Column(Float(), nullable=True)
    long = Column(Float(), nullable=True)

    survey_id = Column(UUID(as_uuid=True), ForeignKey("visual_surveys.id"))
    visual_survey = relationship("VisualSurvey", back_populates="image_registers")

    objects = relationship("ObjectRegister", back_populates="visual_register")
