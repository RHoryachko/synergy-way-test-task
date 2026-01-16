from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Comment
from app.schemas import Comment as CommentSchema

router = APIRouter(prefix="/comments", tags=["comments"])


@router.get("", response_model=dict)
def get_comments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    comments = db.query(Comment).offset(skip).limit(limit).all()
    total = db.query(func.count(Comment.id)).scalar()
    return {"total": total, "comments": [CommentSchema.model_validate(c) for c in comments]}
