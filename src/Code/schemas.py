from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class UpPut(PostBase):
    pass

class PostResponse(PostBase):
    id: int