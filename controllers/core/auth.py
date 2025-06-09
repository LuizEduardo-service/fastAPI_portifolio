import hashlib
from typing import Optional
from fastapi import Response

from controllers.core.configs import settings

def __gerar_hash_cookie(text: str) -> str:
    texto = settings.SALTY + str(text) + '_cookie'
    return hashlib.sha512(texto.encode('utf-8')).hexdigest()

def set_auth(response: Response, membro_id: int) -> None:
    valor_hash: str  = __gerar_hash_cookie(str(membro_id))

    membro_id_hex: str = hex(membro_id)[2:]

    valor: str = membro_id_hex + '.' + valor_hash

    response.set_cookie(key=settings.AUTH_COOKIE_NAME, value=valor, httponly=True)