from datetime import datetime
from pydantic import BaseModel
    
class PostBase(BaseModel):

    title: str
    content: str

    #zinanipa option ya kuweka au niache bila error
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id : int
    created_at: datetime
    
    class Config:
        orm_mode = True
