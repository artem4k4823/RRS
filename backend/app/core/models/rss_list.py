from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app.core.models.base import Base


class OptionalUrl(Base):
    __tablename__ = 'optional-urls-list'
    id: Mapped[int] = mapped_column(unique = True, primary_key = True)
    name: Mapped[str] = mapped_column(String(128))
    url: Mapped[str] 
    description: Mapped[str] = mapped_column(String(256), nullable = False)
    raiting: Mapped[float] = mapped_column(default = 0, server_default = '0')
    likes: Mapped[int] = mapped_column(default = 0, server_default = '0')
