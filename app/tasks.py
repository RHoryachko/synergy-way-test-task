import httpx
from celery import Task
from sqlalchemy.orm import Session

from app.celery_app import celery_app
from app.database import SessionLocal
from app.models import User, Post, Comment
from app.config import settings


class DatabaseTask(Task):
    _db = None

    @property
    def db(self):
        if self._db is None:
            self._db = SessionLocal()
        return self._db

    def after_return(self, *args, **kwargs):
        if self._db is not None:
            self._db.close()
            self._db = None


def get_last_processed_count(db: Session, model_class):
    return db.query(model_class).count()


@celery_app.task(base=DatabaseTask, bind=True)
def fetch_users(self):
    db: Session = self.db
    
    try:
        with httpx.Client() as client:
            response = client.get(f"{settings.jsonplaceholder_url}/users")
            response.raise_for_status()
            users_data = response.json()

        for user_data in users_data:
            user = db.query(User).filter(User.external_id == user_data["id"]).first()
            if not user:
                user = User(
                    external_id=user_data["id"],
                    name=user_data["name"],
                    username=user_data["username"],
                    email=user_data["email"],
                    phone=user_data.get("phone"),
                    website=user_data.get("website"),
                )
                db.add(user)
            else:
                user.name = user_data["name"]
                user.username = user_data["username"]
                user.email = user_data["email"]
                user.phone = user_data.get("phone")
                user.website = user_data.get("website")

        db.commit()
        return f"Processed {len(users_data)} users"
    except Exception as e:
        db.rollback()
        raise e


@celery_app.task(base=DatabaseTask, bind=True)
def fetch_posts(self, limit: int = 10, skip: int = None):
    db: Session = self.db
    
    try:
        if skip is None:
            skip = get_last_processed_count(db, Post)

        with httpx.Client() as client:
            response = client.get(
                f"{settings.dummyjson_url}/posts",
                params={"limit": limit, "skip": skip}
            )
            response.raise_for_status()
            data = response.json()
            posts_data = data.get("posts", [])

        processed = 0
        for post_data in posts_data:
            user = db.query(User).filter(User.external_id == post_data.get("userId")).first()
            if not user:
                continue

            post = db.query(Post).filter(Post.external_id == post_data["id"]).first()
            if not post:
                post = Post(
                    external_id=post_data["id"],
                    user_id=user.id,
                    title=post_data["title"],
                    body=post_data["body"],
                )
                db.add(post)
                processed += 1
            else:
                post.title = post_data["title"]
                post.body = post_data["body"]

        db.commit()
        return f"Processed {processed} new posts (skip={skip})"
    except Exception as e:
        db.rollback()
        raise e


@celery_app.task(base=DatabaseTask, bind=True)
def fetch_comments(self, limit: int = 10, skip: int = None):
    db: Session = self.db
    
    try:
        if skip is None:
            skip = get_last_processed_count(db, Comment)

        with httpx.Client() as client:
            response = client.get(
                f"{settings.dummyjson_url}/comments",
                params={"limit": limit, "skip": skip}
            )
            response.raise_for_status()
            data = response.json()
            comments_data = data.get("comments", [])

        processed = 0
        for comment_data in comments_data:
            post = db.query(Post).filter(Post.external_id == comment_data.get("postId")).first()
            if not post:
                continue

            user_id = comment_data.get("user", {}).get("id")
            user = db.query(User).filter(User.external_id == user_id).first() if user_id else None
            if not user:
                user = db.query(User).first()
                if not user:
                    continue

            comment = db.query(Comment).filter(Comment.external_id == comment_data["id"]).first()
            if not comment:
                comment = Comment(
                    external_id=comment_data["id"],
                    post_id=post.id,
                    user_id=user.id,
                    body=comment_data["body"],
                )
                db.add(comment)
                processed += 1
            else:
                comment.body = comment_data["body"]

        db.commit()
        return f"Processed {processed} new comments (skip={skip})"
    except Exception as e:
        db.rollback()
        raise e
