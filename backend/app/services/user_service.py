from sqlalchemy.orm import Session
from app.models.user import User
from schemas.user import UserCreate
from passlib.hash import bcrypt
from datetime import datetime

def create_user(db: Session, user_data: UserCreate):
    hashed_password = bcrypt.hash(user_data.password)
    user = User(
        username=user_data.username,
        hashed_password=hashed_password,
        role=user_data.role,
        created_at=datetime.utcnow()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
