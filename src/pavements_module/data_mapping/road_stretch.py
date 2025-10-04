from sqlalchemy import Column
from sqlalchemy import UUID, String, Float
from sqlalchemy.orm import relationship
import uuid
from ..domains.road_stretch import RoadStretch
from ...utils.base_entity import BaseEntity

class RoadStretchMapping(BaseEntity):
    CODE_MAX_LENGTH: int = 10

    __tablename__ = "road_stretchs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(CODE_MAX_LENGTH), nullable=False)
    
    lat_initial = Column(Float, nullable=True)
    long_initial = Column(Float, nullable=True)

    lat_final = Column(Float, nullable=True)
    long_final = Column(Float, nullable=True)

    surveys = relationship("VisualSurveyMapping", 
                           back_populates="stretch", 
                           cascade="all, delete-orphan")

    def to_entity(self) -> RoadStretch:
        return RoadStretch(self.id, self.code, 
                           self.lat_initial, self.long_initial, 
                           self.lat_final, self.long_final)
    
    @staticmethod
    def create(code, lat_init, long_init, lat_final, long_final):
        return RoadStretchMapping(id=uuid.uuid4(), code=code, 
                                  lat_initial=lat_init, 
                                  long_initial=long_init, 
                                  lat_final=lat_final,
                                  long_final=long_final)