from celery import Task
from sqlalchemy.orm import Session

from app.celery_app import celery_app
from app.database import SessionLocal
from app.models import User, Post, Comment
from app.services.user_service import UserService
from app.services.post_service import PostService
from app.services.comment_service import CommentService
from app.services.api_client import APIClient


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
        users_data = APIClient.get_users()

        for user_data in users_data:
            UserService.create_or_update_user(db, user_data)

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

        posts_data = APIClient.get_posts(limit=limit, skip=skip)

        processed = 0
        for post_data in posts_data:
            user = db.query(User).filter(User.external_id == post_data.get("userId")).first()
            if not user:
                continue

            _, is_new = PostService.create_or_update_post(db, post_data, user)
            if is_new:
                processed += 1

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

        comments_data = APIClient.get_comments(limit=limit, skip=skip)

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

            _, is_new = CommentService.create_or_update_comment(db, comment_data, post, user)
            if is_new:
                processed += 1

        db.commit()
        return f"Processed {processed} new comments (skip={skip})"
    except Exception as e:
        db.rollback()
        raise e
