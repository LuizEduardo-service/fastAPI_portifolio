from fastapi.requests import Request

from controllers.core.configs import settings
from controllers.core.database import get_session
from models.area_model import AreaModel
from controllers.base_controller import BaseController

class AreaController(BaseController):

    def __init__(self, request: Request):
        super().__init__(request, AreaModel)


    async def post_crud(self) -> None:
        form =  await self.request.form()

        area: str = form.get('area')
        area_model: AreaModel = AreaModel(area=area)

        async with get_session() as session:
            session.add(area_model)
            await session.commit()
    
    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            area_model: AreaModel = await session.get(AreaModel, obj.id)

            if area_model:
                form = await self.request.form()
                area: str = form.get('area')

                if area_model.area != area:
                    area_model.area = area

                await session.commit()

