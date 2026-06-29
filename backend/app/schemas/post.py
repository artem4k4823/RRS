from pydantic import BaseModel,ConfigDict
from datetime import datetime

class PostSchema(BaseModel):
    title: str
    link: str
    summary: str
    # published_at: datetime
    feed_id: int
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)
    

    # title = entry.get('title', ''),
    #             link = link,
    #             summary = entry.get('summary') or entry.get('description'),
    #             published_at = published_at,
    #             feed_id = subscribe.id,
    #             user_id = subscribe.user_id,