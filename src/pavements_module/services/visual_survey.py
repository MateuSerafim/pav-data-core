from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from ..data_mapping.visual_survey import VisualSurveyMapping
from ..services.road_stretch import RoadStretchService
from ...utils.result import Result, ErrorCode

class VisualSurveyService():
    def __init__(self, session: AsyncSession, road_stretch_service: RoadStretchService):
        self.db_session = session
        self.road_stretch_service = road_stretch_service

    async def add_visual_survey(self, new_vs: VisualSurveyMapping) -> Result:
        stretch_exists_result = await self.road_stretch_service.check_exists_stretch(new_vs.stretch_id)
        if (stretch_exists_result.is_failure()):
            return stretch_exists_result
        
        try:
            await self.db_session.execute(
                update(VisualSurveyMapping).\
                where(VisualSurveyMapping.stretch_id == new_vs.stretch_id).\
                values(is_open=False).\
                execution_options(synchronize_session="fetch"))

            self.db_session.add(new_vs)

            await self.db_session.commit()

            return Result.success(new_vs.to_entity().load_registers([]))
        except Exception as e:
            await self.db_session.rollback()
            return Result.failure(e.args, ErrorCode.CRITICAL_ERROR)
        
    async def get_visual_surveys(self, stretch_id: uuid.UUID):
        stretch_exists_result = await self.road_stretch_service.check_exists_stretch(stretch_id)
        if (stretch_exists_result.is_failure()):
            return stretch_exists_result
        
        query = await self.db_session.execute(
            select(VisualSurveyMapping)\
            .options(selectinload(VisualSurveyMapping.image_registers)))

        visual_surveys = query.scalars().all()
    
        return Result.success(
            [vs.to_entity()\
               .load_registers([r.to_entity() for r in vs.image_registers]) \
                for vs in visual_surveys])