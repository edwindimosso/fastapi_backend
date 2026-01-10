from pydantic import BaseModel


class Post(BaseModel):
    id: int | None = None
    title: str
    content: str

    #zinanipa option ya kuweka au niache bila error
    published: bool = True