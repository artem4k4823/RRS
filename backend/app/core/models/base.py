from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from typing import Annotated

intpk = Annotated[int,  mapped_column(primary_key = True, index = True)]

class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[intpk] 