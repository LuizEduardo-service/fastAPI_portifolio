import hashlib
from typing import Optional
from fastapi import Response
from passlib.handlers.sha2_crypt import sha512_crypt
from fastapi import Request
from controllers.core.configs import settings


def try_hex_to_int(valor_hex: str) -> int:
    "tenta converter um valor hexadecimal em inteiro"
    try:
        return int(valor_hex, 16)
    except:
        return 0

def __gerar_hash_cookie(text: str) -> str:
    texto = settings.SALTY + str(text) + '_cookie'
    return hashlib.sha512(texto.encode('utf-8')).hexdigest()

def set_auth(response: Response, membro_id: int) -> None:
    valor_hash: str  = __gerar_hash_cookie(str(membro_id))

    membro_id_hex: str = hex(membro_id)[2:]

    valor: str = membro_id_hex + '.' + valor_hash

    response.set_cookie(key=settings.AUTH_COOKIE_NAME, value=valor, httponly=True)

def gerar_hash_senha(senha: str) -> str:
    hash_senha = sha512_crypt.hash(senha, rounds=123_456)
    return hash_senha

def verificar_senha(senha: str, hash_senha: str) -> bool:
    return sha512_crypt.verify(secret=senha,hash=hash_senha)

def get_membro_id(request: Request) -> Optional[int]:

    if not settings.AUTH_COOKIE_NAME in request.cookies:
        return None
    
    valor = request.cookies[settings.AUTH_COOKIE_NAME]

    parts = valor.split('.')

    membro_id_hex: str = parts[0]

    membro_id_int: int = try_hex_to_int(membro_id_hex)

    check_valor_hash: str = __gerar_hash_cookie(membro_id_int)

    check_valor_hash = membro_id_hex + '.' + check_valor_hash

    # validar hash do cookie
    if valor != check_valor_hash:
        return None
    
    return membro_id_int

def unset_auth(response: Response):
    response.delete_cookie(settings.AUTH_COOKIE_NAME)
