from pydantic import BaseModel, ConfigDict
from app.schemas.sub import SubscriptionResponse
from app.schemas.post import PostSchema


class UserSchema(BaseModel):
    id: int | None = None
    username: str
    status: bool
    isAdmin: bool = False
    isCreator: bool = False
    model_config = ConfigDict(from_attributes=True)


class UserWithSubsSchema(UserSchema):
    subscriptions: list[SubscriptionResponse]


class UserWithPostsSchema(UserSchema):
    posts: list[PostSchema]

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
    
    