from pydantic import BaseModel
from typing import Optional, List


class UserBase(BaseModel):
    name: str
    username: str
    email: str
    phone: Optional[str] = None
    website: Optional[str] = None


class User(UserBase):
    id: int
    external_id: int

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title: str
    body: str


class Post(PostBase):
    id: int
    external_id: int
    user_id: int

    class Config:
        from_attributes = True


class CommentBase(BaseModel):
    body: str


class Comment(CommentBase):
    id: int
    external_id: int
    post_id: int
    user_id: int

    class Config:
        from_attributes = True


class UserWithPosts(User):
    posts: List[Post] = []


class PostWithComments(Post):
    comments: List[Comment] = []
