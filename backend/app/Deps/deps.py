from app.core.models import User
from sqlalchemy import select
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Header, Depends, HTTPException, status
from app.core.database import db

router = APIRouter(prefix="/test-deps", tags=["test-deps"])

def verify_token(x_token: str = Header(...)):
    if x_token != "super-secret-key":
        raise HTTPException(status.HTTP_403_FORBIDDEN)


def get_db_session():
    print("start")
    db = {"session": "ok"}
    try:
        yield db
    finally:
        print("Закрытие соединения с базой...")
        print("---end---")


@router.get("/db-test")
def db_test(session: Annotated[None, Depends(get_db_session)]):
    return session

def get_query(q: str | None = None):
    return q

def validate_query(q: Annotated[str, Depends(get_query)]):
    if q is None or "":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail = "Строка пуста")
    return q


@router.get('/search')
async def search(q: Annotated[str, Depends(validate_query)]):
    return q

@router.get("/user-deps", dependencies=[Depends(verify_token)])
async def get_user(session: Annotated[AsyncSession, Depends(db.session_getter)]):
    stmt = select(User).where(User.id == 1)
    res = await session.execute(stmt)
    return res.scalar_one_or_none()

class ItemFilters:
    def __init__(self, q: str | None = None, min_price:float = 0, max_price: float = 10000 ):
        self.q = q
        self.min_price = min_price
        self.max_price = max_price

    def is_expinsive(self):
        if self.max_price > 10000:
            return True
        return False

@router.get('/filters')
async def filters(
    filters: Annotated[ItemFilters, Depends()],
    
):
    is_expensive = filters.is_expinsive()
    return filters, is_expensive




def verif_token_admin(token: str = Header(...)):
    if token != "admin-pass":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail = "No admin")
    return token

def get_db():
    print("Connect")
    db = {"session": "ok"}
    try:
        yield db
    finally:
        print("disconnect")


def process_data(token: Annotated[str, Depends(verif_token_admin)], session: Annotated[dict, Depends(get_db)], text: str):
    return text.upper()


@router.get('/create-note')
async def create_note(process_data: Annotated[str, Depends(process_data)]):
    return process_data