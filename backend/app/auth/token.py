from datetime import datetime, timedelta
from fastapi import HTTPException, status
import jwt
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.models import Token
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


def create_jwt(data):
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes= settings.EXPIRE_TIME)
    payload.update({'exp': expire})
    return encode_jwt(payload)


async def get_token(session: AsyncSession, user_id: int):
    stmt = select(Token).where(Token.user_id == user_id)
    result = await session.execute(stmt)
    token = result.scalar_one_or_none()
    return token    

async def create_access_token(session: AsyncSession, user_id: int, user_data: Optional[dict] = None):
    jwt_data = {
        'sub': str(user_id),
        'type': 'access',
        'iat':  datetime.utcnow().timestamp(),
    }
    
    if user_data:
        jwt_data.update(user_data)
        
    access_token = create_jwt(jwt_data)
    
    expire_at = datetime.utcnow() + timedelta(minutes=settings.EXPIRE_TIME)
    
    
    existing_token = await get_token(session=session, user_id=user_id)
    
    if existing_token:
        
        existing_token.acces_token = access_token
        existing_token.expire_at = expire_at
    else:
        
        existing_token = Token(
            acces_token=access_token,
            user_id=user_id,
            expire_at=expire_at
        )
        session.add(existing_token)
    
    
    await session.commit()
    await session.refresh(existing_token)
    
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "expires_at": expire_at.isoformat(),
        
    }
    
    
    


