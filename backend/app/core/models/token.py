from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from app.core.models.base import Base




class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    token: Mapped[str] = mapped_column(unique = True)
    expire_at: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(default = datetime.utcnow)
    is_revoked: Mapped[bool] = mapped_column(default = False)
    user_username: Mapped[str]