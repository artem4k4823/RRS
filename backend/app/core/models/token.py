from enum import unique
from prometheus_fastapi_instrumentator.metrics import default
from app.core.models import User
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String 
from app.core.models.base import Base


# class Token(Base):
#     __tablename__ = 'tokens'
#     acces_token: Mapped[str] = mapped_column()
#     expire_at: Mapped[datetime]
#     refresh_token: Mapped[str] = mapped_column()
#     user_id : Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
#     user: Mapped["User"] = relationship('User', back_populates = 'tokens')


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    token: Mapped[str] = mapped_column(unique = True)
    expire_at: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(default = datetime.utcnow)
    user_username: Mapped[str]