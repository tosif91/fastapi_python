from sqlalchemy.orm import Session
from src.users.schemas import UserInputSchema, UserResponse
from src.users.models import UserModel, UserMetaModel
from src.books.models import BookModel
from sqlalchemy import Column
import src.exceptions as exp


def get_users(db: Session, skip: int = 0, limit: int = 10):
    query_result = db.query(UserModel, UserMetaModel).join(
        UserMetaModel, UserModel.id == UserMetaModel.uid).offset(skip).limit(limit=limit).all()
    userList = []
    for user, meta in query_result:
        user_dict = user.__dict__
        meta_dict = meta.__dict__

        user_dict.pop('_sa_instance_state', None)
        user_dict.pop('hashed_password', None)
        meta_dict.pop('_sa_instance_state', None)
        meta_dict.pop('uid', None)

        user_with_metadata = {**user_dict, **meta_dict}
        userList.append(user_with_metadata)

    return userList


def get_user_by_email(db: Session, email: str):
    query_result = db.query(UserModel).filter(UserModel.email == email).first()
    return query_result


def getIssuedBooks(db: Session, uid: int):
    return db.query(BookModel).filter(BookModel.issued_by == uid).all()
