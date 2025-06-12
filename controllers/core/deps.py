from typing import Optional
from datetime import datetime

from fastapi.requests import Request

from controllers.membro_controller import MembroController
from models.member_model import MemberModel
from controllers.core.auth import get_membro_id

async def valida_login(request: Request) -> Optional[MemberModel]:
    context = {'request': request, 'ano': datetime.now().year}
    membro_id: int = get_membro_id(request=request)

    if membro_id and membro_id > 0:
        membro_controller: MembroController = MembroController(request=request)
        membro = await membro_controller.get_one_crud(membro_id)

        context.update({'membro': membro})

    return context