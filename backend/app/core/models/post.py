from app.core.models.base import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Text




class Post(Base):
    __tablename__ = "posts"
    title: Mapped[str] = mapped_column(nullable = False, )
    description: Mapped[str] = mapped_column(nullable = False)
    text: Mapped[str] = mapped_column(Text, nullable = False)
    
