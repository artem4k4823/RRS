from datetime import datetime, timedelta
from fastapi import HTTPException, status
import jwt
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models.token import RefreshToken

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

async def verify_refresh_token(
    session: AsyncSession,
    refresh_token: str,
):
    
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is required"
        )
    
    try:
        payload = jwt.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        token_type = payload.get("type")
        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        exp = payload.get("exp")
        if exp and datetime.utcnow() > datetime.fromtimestamp(exp):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired"
            )
        
        
        stmt = select(RefreshToken).where(
            RefreshToken.token == refresh_token,
            RefreshToken.is_revoked == False,
            RefreshToken.expire_at > datetime.utcnow()
        )
        result = await session.execute(stmt)
        db_token = result.scalar_one_or_none()
        
        if not db_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token not found or has been revoked"
            )
        
        if str(db_token.user_id) != str(user_id):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token-user mismatch"
            )
        
        return int(user_id)
        
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid refresh token: {str(e)}"
        )
        
        
async def invalidate_refresh_token(
    session: AsyncSession, 
    refresh_token: str
):
    
    stmt = select(RefreshToken).where(RefreshToken.token == refresh_token)
    result = await session.execute(stmt)
    db_token = result.scalar_one_or_none()
    
    if db_token and not db_token.is_revoked:
        
        db_token.is_revoked = True
        db_token.revoked_at = datetime.utcnow()
        db_token.revoked_reason = "Manual invalidation"
        
        await session.commit()
        return True
    
    return False

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
    
    
   
    
    


