from app.core.models.base import intpk
from app.core.models.base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, String, Boolean
from datetime import datetime
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from app.core.models.user import User 
    from app.core.models.post import Post


class Subscription(Base):
    __tablename__ = "subscriptions"
    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    feed_url: Mapped[str] = mapped_column(String(500), nullable = False)
    custom_name: Mapped[str] = mapped_column(String(60), nullable = True)
    is_active: Mapped[bool] = mapped_column(Boolean, default = True)
    created_at: Mapped[datetime] = mapped_column(default = datetime.utcnow)
    
    user: Mapped["User"] = relationship(back_populates = 'subscriptions')
    posts: Mapped[List["Post"]] = relationship(back_populates = 'feed', cascade="all, delete-orphan")