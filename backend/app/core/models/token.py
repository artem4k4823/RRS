from app.core.models import User
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String 
from app.core.models.base import Base


class Token(Base):
    __tablename__ = 'tokens'
    acces_token: Mapped[str] = mapped_column()
    expire_at: Mapped[datetime]
    refresh_token: Mapped[str] = mapped_column()
    user_id : Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    user: Mapped["User"] = relationship('User', back_populates = 'tokens')