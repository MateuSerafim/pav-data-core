from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from ..data_mapping.visual_register import VisualRegisterMapping
from ...utils.result import Result, ErrorCode
from ..domains.visual_register import VisualRegister

class VisualRegisterService():
    def __init__(self, session: AsyncSession, visual_survey_service):
        self.db_session = session
        self.visual_survey_service = visual_survey_service

    async def get_visual_register(self, visual_id: uuid.UUID):
        query = await self.db_session.execute(
            select(VisualRegisterMapping)\
            .options(selectinload(VisualRegisterMapping.objects))\
            .where(VisualRegisterMapping.id == visual_id))
        
        visual_survey = query.scalars().first()
        if (visual_survey is None):
            return Result.failure("Registro não encontrado!", ErrorCode.NOT_FOUND)
        
        return Result.success(visual_survey.to_entity()\
                              .load_objects_registers([r.to_entity() for r in visual_survey.objects]))

    async def add_visual_register(self, new_register: VisualRegisterMapping):
        survey_exists_result = await self.visual_survey_service\
            .check_exist_visual_survey(new_register.survey_id)
        if (survey_exists_result.is_failure()):
            return survey_exists_result
        
        try:
            self.db_session.add(new_register)

            await self.db_session.commit()

            return Result.success(new_register.to_entity().load_objects_registers([]))
        except Exception as e:
            await self.db_session.rollback()
            return Result.failure(e.args, ErrorCode.CRITICAL_ERROR)
        
    async def update_visual_register(self, register: VisualRegister):
        try:
            entity = await self.db_session.get(VisualRegisterMapping, register.id)
            if (not entity):
                return Result.failure("Entidade não encontrada!", ErrorCode.NOT_FOUND)
            entity.image_url = register.image_url
            entity.lat = register.lat
            entity.long = register.long
            entity.process_status = register.process_status
            await self.db_session.commit()
        except Exception as ex:
            await self.db_session.rollback()
            return Result.failure(str(ex))
    
