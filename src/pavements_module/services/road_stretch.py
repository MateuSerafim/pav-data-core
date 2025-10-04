from sqlalchemy import select, exists
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from ...utils.result import Result, ErrorCode
from ..data_mapping.road_stretch import RoadStretchMapping

class RoadStretchService():
    def __init__(self, session: AsyncSession):
        self.db_session = session

    async def add_road_stretch(self, new_data: RoadStretchMapping) -> Result:
        try:
            self.db_session.add(new_data)

            await self.db_session.commit()
            
            return Result.success(new_data.to_entity())
        except:
            return Result.failure("Falha ao adicionar entidade", ErrorCode.CRITICAL_ERROR)

    async def get_road_stretchs(self) -> Result:
        query = await self.db_session.execute(
            select(RoadStretchMapping)\
            .options(selectinload(RoadStretchMapping.surveys)))

        road_stretchs = query.scalars().all()
        
        return Result.success(
            [rs.to_entity()\
               .load_surveys([vs.to_entity() for vs in rs.surveys]) \
                for rs in road_stretchs])
    
    async def check_exists_stretch(self, stretch_id: uuid.UUID) -> Result:
        query = await self.db_session.execute(
            select(exists().where(RoadStretchMapping.id == stretch_id)))
        
        road_exists = query.scalar()
        if (not road_exists):
            return Result.failure("Trecho de rodovia não existe!", ErrorCode.NOT_FOUND)
        
        return Result.success(True)
    
    async def delete_stretch(self, stretch_id: uuid.UUID) -> Result:
        exist_result = await self.check_exists_stretch(stretch_id)
        if (exist_result.is_failure()):
            return exist_result
        try:
            stretch = await self.db_session.get(RoadStretchMapping, stretch_id)
            
            await self.db_session.delete(stretch)
            
            await self.db_session.commit()

            return Result.success()

        except Exception as e:
            await self.db_session.rollback()

            return Result.failure(ErrorCode.CRITICAL_ERROR, str(e))