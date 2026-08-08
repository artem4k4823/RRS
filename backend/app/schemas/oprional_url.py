from pydantic import ConfigDict
from pydantic import BaseModel


class OptionalUrlSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int | None = None
    name: str
    description: str
    url: str