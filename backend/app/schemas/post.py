from pydantic import BaseModel,ConfigDict


class PostSchema(BaseModel):
    title: str
    description: str
    text: str
    
    model_config = ConfigDict(from_attributes=True)
    