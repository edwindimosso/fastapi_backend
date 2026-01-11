from pydantic import BaseModel
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Post(BaseModel):
    id: int | None = None
    title: str
    content: str

    #zinanipa option ya kuweka au niache bila error
    published: bool = True


class PostModel(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)
    #default ni kama nilisema published ni True kama mtu hataweka kitu