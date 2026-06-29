from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String 
from app.core.models.base import Base
if TYPE_CHECKING:
    from app.core.models.subscribtion import Subscription
    from app.core.models.post import Post
       


class User(Base):
    __tablename__ = 'users'
    username: Mapped[str] = mapped_column(String(length=25),unique = True, nullable = False)
    password: Mapped[str] = mapped_column(String(length=128), nullable = False)
    isCreator: Mapped[bool] = mapped_column(default = False, server_default = '0')
    isAdmin: Mapped[bool] = mapped_column(default = False, server_default = '0')
    status: Mapped[bool] = mapped_column(default = True, server_default = '1')
    
    subscriptions: Mapped[List["Subscription"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",  
    )
    posts: Mapped[List["Post"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


    