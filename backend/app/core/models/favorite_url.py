from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from app.core.models.base import Base
from typing import TYPE_CHECKING 

if TYPE_CHECKING:
    from app.core.models.user import User
    from app.core.models.rss_list import OptionalUrl

class FavoriteUrl(Base):
    __tablename__ = "favorite_urls"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    url_id: Mapped[int] = mapped_column(
        ForeignKey("optional-urls-list.id", ondelete="CASCADE"),
        nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="favorite_urls")
    optional_url: Mapped["OptionalUrl"] = relationship(back_populates="favorite_entries")

    __table_args__ = (
        UniqueConstraint("user_id", "url_id", name="uq_user_favorite_url"),
    )