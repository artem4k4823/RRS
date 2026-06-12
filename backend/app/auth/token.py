from datetime import datetime, timedelta
from fastapi import HTTPException, status
import jwt
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from sqlalchemy import select


def encode_jwt(payload):
    return jwt.encode(payload, str(settings.SECRET_KEY), algorithm=str(settings.ALGORITHM))

def decode_jwt(token):
    try: 
        payload = jwt.decode(token, str(settings.SECRET_KEY), algorithms=[str(settings.ALGORITHM)])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail='Token expired'
        )
    except jwt.PyJWTError as e:
        print(f'ошибка jwt: {e}')
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail=f'Token invalid: {e}'
        )
    payload.update()
    return encode_jwt(payload)


def create_token(type: str, data:dict, ):
    data = data.copy()
    data['TOKEN_TYPE']= type
    data.update(data)
    token = encode_jwt(data)
    return token

def create_refresh_token(user_id: str):
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_EXPIRE_TIME_DAYS)
    jwt_data = {
        'sub': str(user_id),
        'exp': expire,
        'iat': datetime.utcnow(),
    }

    return create_token(
        'refresh',
        jwt_data
    )
    
    
def create_access_token(user_id: int):
   
    jwt_data = {
        'sub': str(user_id),
        'type': 'access',
        'iat':  datetime.utcnow().timestamp(),
    }
    return create_token(
        'access', 
        jwt_data
        )
    
    
   
    
    


