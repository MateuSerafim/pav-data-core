from sqlalchemy import Column
from sqlalchemy import UUID, String, Float
from sqlalchemy.orm import relationship
import uuid
from src.utils.base_entity import BaseEntity

class RoadStretchMapping(BaseEntity):
    __tablename__ = "road_stretchs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(10), nullable=False)
    
    lat_initial = Column(Float, nullable=True)
    long_initial = Column(Float, nullable=True)

    lat_final = Column(Float, nullable=True)
    long_final = Column(Float, nullable=True)

    surveys = relationship("VisualSurvey", back_populates="strech")