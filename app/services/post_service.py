from sqlalchemy.orm import Session

from app.models import Post, User


class PostService:
    @staticmethod
    def create_or_update_post(db: Session, post_data: dict, user: User) -> Post:
        post = db.query(Post).filter(Post.external_id == post_data["id"]).first()
        if not post:
            post = Post(
                external_id=post_data["id"],
                user_id=user.id,
                title=post_data["title"],
                body=post_data["body"],
            )
            db.add(post)
            return post, True
        else:
            post.title = post_data["title"]
            post.body = post_data["body"]
            return post, False
