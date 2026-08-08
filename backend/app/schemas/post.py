from pydantic import BaseModel,ConfigDict
from datetime import datetime

class PostSchema(BaseModel):
    id: int | None = None
    title: str
    link: str
    summary: str | None = None
    published_at: datetime | None = None
    created_at: datetime | None = None
    feed_id: int

    
    model_config = ConfigDict(from_attributes=True)
    

    # title = entry.get('title', ''),
    #             link = link,
    #             summary = entry.get('summary') or entry.get('description'),
    #             published_at = published_at,
    #             feed_id = subscribe.id,
    #             user_id = subscribe.user_id,