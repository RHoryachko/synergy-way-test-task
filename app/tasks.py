import logging
from celery import Task
from sqlalchemy.orm import Session

from app.celery_app import celery_app
from app.database import SessionLocal
from app.models import User, Post, Comment
from app.services.user_service import UserService
from app.services.post_service import PostService
from app.services.comment_service import CommentService
from app.services.api_client import APIClient

logger = logging.getLogger(__name__)


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
        logger.info("Starting fetch_users task")
        users_data = APIClient.get_users()
        logger.info(f"Fetched {len(users_data)} users from API")

        for user_data in users_data:
            UserService.create_or_update_user(db, user_data)

        db.commit()
        logger.info(f"Successfully processed {len(users_data)} users")
        return f"Processed {len(users_data)} users"
    except Exception as e:
        db.rollback()
        logger.error(f"Error in fetch_users: {str(e)}", exc_info=True)
        raise e


@celery_app.task(base=DatabaseTask, bind=True)
def fetch_posts(self, limit: int = 30, skip: int = None):
    db: Session = self.db

    try:
        if skip is None:
            skip = get_last_processed_count(db, Post)

        max_skip = 1000
        batch_limit = limit
        total_processed = 0

        while skip < max_skip:
            logger.info(f"Starting fetch_posts task with limit={batch_limit}, skip={skip}")
            posts_data = APIClient.get_posts(limit=batch_limit, skip=skip)
            
            if not posts_data:
                logger.info("No more posts to fetch")
                break

            logger.info(f"Fetched {len(posts_data)} posts from API")

            processed = 0
            for post_data in posts_data:
                user = db.query(User).filter(User.external_id == post_data.get("userId")).first()
                if not user:
                    continue

                _, is_new = PostService.create_or_update_post(db, post_data, user)
                if is_new:
                    processed += 1

            db.commit()
            total_processed += processed
            
            if processed > 0:
                logger.info(f"Successfully processed {processed} new posts in this batch")
                break
            
            skip += batch_limit

        logger.info(f"Total processed {total_processed} new posts")
        return f"Processed {total_processed} new posts (final skip={skip})"
    except Exception as e:
        db.rollback()
        logger.error(f"Error in fetch_posts: {str(e)}", exc_info=True)
        raise e


@celery_app.task(base=DatabaseTask, bind=True)
def fetch_comments(self, limit: int = 30, skip: int = None):
    db: Session = self.db

    try:
        if skip is None:
            skip = get_last_processed_count(db, Comment)

        max_skip = 1000
        batch_limit = limit
        total_processed = 0

        while skip < max_skip:
            logger.info(f"Starting fetch_comments task with limit={batch_limit}, skip={skip}")
            comments_data = APIClient.get_comments(limit=batch_limit, skip=skip)
            
            if not comments_data:
                logger.info("No more comments to fetch")
                break

            logger.info(f"Fetched {len(comments_data)} comments from API")

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
                        logger.warning("No users found in database")
                        continue

                _, is_new = CommentService.create_or_update_comment(db, comment_data, post, user)
                if is_new:
                    processed += 1

            db.commit()
            total_processed += processed
            
            if processed > 0:
                logger.info(f"Successfully processed {processed} new comments in this batch")
                break
            
            skip += batch_limit

        logger.info(f"Total processed {total_processed} new comments")
        return f"Processed {total_processed} new comments (final skip={skip})"
    except Exception as e:
        db.rollback()
        logger.error(f"Error in fetch_comments: {str(e)}", exc_info=True)
        raise e
