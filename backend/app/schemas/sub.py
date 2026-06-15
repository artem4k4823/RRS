from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AddSubSchema(BaseModel):
    url: str
    custom_name: str
    
class SubscriptionResponse(BaseModel):
   
    
    feed_url: str
    custom_name: Optional[str] = None
    is_active: bool
    # created_at: datetime
    last_fetched_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  