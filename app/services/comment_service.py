from sqlalchemy.orm import Session

from app.models import Comment, Post, User


class CommentService:
    @staticmethod
    def create_or_update_comment(
        db: Session, comment_data: dict, post: Post, user: User
    ) -> Comment:
        comment = db.query(Comment).filter(
            Comment.external_id == comment_data["id"]
        ).first()
        if not comment:
            comment = Comment(
                external_id=comment_data["id"],
                post_id=post.id,
                user_id=user.id,
                body=comment_data["body"],
            )
            db.add(comment)
            return comment, True
        else:
            comment.body = comment_data["body"]
            return comment, False
