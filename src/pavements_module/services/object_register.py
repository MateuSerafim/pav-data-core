from sqlalchemy.ext.asyncio import AsyncSession
from ..data_mapping.object_register import ObjectRegisterMapping

from ...utils.result import ErrorCode, Result

class ObjectRegisterService():
    def __init__(self, session: AsyncSession, visual_register_service):
        self.db_session = session
        self.visual_register_service = visual_register_service

    async def add(self, new_data: ObjectRegisterMapping) -> Result:
        try:
            self.db_session.add(new_data)

            await self.db_session.commit()
            
            return Result.success(new_data.to_entity())
        except:
            return Result.failure("Falha ao adicionar entidade", ErrorCode.CRITICAL_ERROR)