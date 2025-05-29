from controllers.base_controller import BaseController
from models.tag_model import TagModel
from controllers.core.database import get_session

class TagController(BaseController):
    def __init__(self, request):
        super().__init__(request, TagModel)


    async def post_crud(self):
        form = await self.request.form()
        tags: str = form.get('tag')

        tag: TagModel = TagModel(tag=tags)
        async with get_session() as session:
            session.add(tag)
            await session.commit()


    async def put_crud(self, obj: object):
        async with get_session() as session:
            tag: TagModel = await session.get(self.model, obj.id)

            if tag:
                form = await self.request.form()
                tags: str = form.get('tag')

                if tag and tag.tags != tags:
                    tag.tags = tags

                await session.commit()
                