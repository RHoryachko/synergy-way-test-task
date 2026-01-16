from sqlalchemy.orm import Session

from app.models import User


class UserService:
    @staticmethod
    def create_or_update_user(db: Session, user_data: dict) -> User:
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
        return user
