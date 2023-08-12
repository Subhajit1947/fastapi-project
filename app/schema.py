from pydantic import BaseModel,EmailStr
from typing import Optional
from pydantic.types import conint

class cuser(BaseModel):
    email:EmailStr
    password:str

class userout(BaseModel):
    id:int
    email:EmailStr
    class Config:
        orm_mode=True


class allpost(BaseModel):
    id:int
    title:str
    content:str
    owner:userout
    class Config:
        orm_mode=True

class Outpost(BaseModel):
    post:allpost
    votes:int
    class Config:
        orm_mode=True

class cpost(BaseModel):
    title:str
    content:str
    

class Token(BaseModel):
    access_token: str
    token_type: str
    class Config:
        orm_mode=True

class Tokendata(BaseModel):
    id:Optional[str]=None

class Setvote(BaseModel):
    post_id:int
    dir:conint(le=1)
