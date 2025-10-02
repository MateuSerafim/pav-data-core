from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

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
