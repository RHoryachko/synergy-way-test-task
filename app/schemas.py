from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class UserBase(BaseModel):
    name: str
    username: str
    email: str
    phone: Optional[str] = None
    website: Optional[str] = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    external_id: int


class PostBase(BaseModel):
    title: str
    body: str


class Post(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    external_id: int
    user_id: int


class CommentBase(BaseModel):
    body: str


class Comment(CommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    external_id: int
    post_id: int
    user_id: int


class UserWithPosts(User):
    posts: List[Post] = []


class PostWithComments(Post):
    comments: List[Comment] = []
