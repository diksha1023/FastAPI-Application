from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Annotated

# from pydantic.types import conint - deprecated in pydantic 3.0

#using pydantic library to define the database schema
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#     # rating: Optional[int] = None

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass #whatever is passed ll be included. extends the postbase class, inheritance

#response schema
class UserOut(BaseModel):
    id:int
    email: EmailStr
    created_at: datetime

    #convert sqlalchemy to pydantic model
    class Config:
        from_attributes = True

#response schema, inheriting the postbase class fields
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut


    #convert sqlalchemy to pydantic model
    class Config:
        from_attributes = True

#request schema for creating user
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

#access_token - user data schema
class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1, description="Value must be between 0 and 1 inclusive")]
    # dir: conint(le=1)

# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: bool #for updating, want to provide value for each column.




