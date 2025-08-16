from sqlalchemy.orm import Session
from app.models.user import User
from schemas.user import UserCreate
from passlib.hash import bcrypt
from datetime import datetime
from app.schemas.user import UserUpdate

def create_user(db: Session, user_data: UserCreate):
    hashed_password = bcrypt.hash(user_data.password)
    user = User(
        name=user_data.name,
        phone=user_data.phone,
        hashed_password=hashed_password,
        role=user_data.role,
        location=user_data.location,
        qualification=user_data.qualification,
        rate=user_data.rate,
        status=user_data.status,
        address=None  # по умолчанию, потом можно обновить
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: int, user_data: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    if user_data.name is not None:
        user.name = user_data.name
    if user_data.phone is not None:
        user.phone = user_data.phone
    if user_data.password is not None:
        user.hashed_password = bcrypt.hash(user_data.password)
    if user_data.qualification is not None:
        user.qualification = user_data.qualification
    if user_data.rate is not None:
        user.rate = user_data.rate
    if user_data.location is not None:
        user.location = user_data.location
    if user_data.latitude is not None:
        user.latitude = user_data.latitude
    if user_data.longitude is not None:
        user.longitude = user_data.longitude
    if user_data.address is not None:
        user.address = user_data.address
    if user_data.status is not None:
        user.status = user_data.status
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
