from sqlalchemy import select, update, exists
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from ..data_mapping.visual_survey import VisualSurveyMapping
from ..data_mapping.visual_register import VisualRegisterMapping
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
            .options(selectinload(VisualSurveyMapping.image_registers))\
            .where(VisualSurveyMapping.stretch_id == stretch_id))

        visual_surveys = query.scalars().all()
    
        return Result.success(
            [vs.to_entity()\
               .load_registers([r.to_entity() for r in vs.image_registers]) \
                for vs in visual_surveys])
    
    async def get_visual_survey(self, visual_id: uuid.UUID):
        query = await self.db_session.execute(
            select(VisualSurveyMapping)\
            .options(selectinload(VisualSurveyMapping.image_registers)\
                    .selectinload(VisualRegisterMapping.objects))\
            .where(VisualSurveyMapping.id == visual_id))
        
        visual_survey = query.scalars().first()
        if (visual_survey is None):
            return Result.failure("Levantamento não encontrado", ErrorCode.NOT_FOUND)
        
        return Result.success(visual_survey.to_entity()\
                              .load_registers([r.to_entity()\
                                               .load_objects_registers([o.to_entity() for o in r.objects])\
                                for r in visual_survey.image_registers]))

    async def check_exist_visual_survey(self, visual_id: uuid.UUID) -> Result:
        query = await self.db_session.execute(
            select(exists().where(VisualSurveyMapping.id == visual_id)))
        
        road_exists = query.scalar()
        if (not road_exists):
            return Result.failure("Levantamento não existe!", ErrorCode.NOT_FOUND)
        
        return Result.success(True)