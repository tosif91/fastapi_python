from sqlalchemy.orm import Session
from schemas.user_schema import UserSchema, UserInputSchema, UserResponse
from models.user_model import UserModel, UserMetaModel
from models.book_model import BookModel
from auth.password_service import hashPassword
from sqlalchemy import Column


def create_user(db: Session, user: UserInputSchema) -> UserModel:
    hash_pwd = hashPassword(user.password)
    input_dict = user.model_dump()
    del input_dict['password']
    db_user = UserModel(**input_dict, hashed_password=hash_pwd)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        _create_user_meta(db, db_user.id)  # type: ignore
    except Exception as e:
        db.rollback()
        raise e

    return db_user


def _create_user_meta(db: Session, uid: int) -> UserMetaModel:
    db_user_meta = UserMetaModel(
        totalbookissued=0, totalbookreturned=0, uid=uid)
    db.add(db_user_meta)
    db.commit()
    db.refresh(db_user_meta)
    return db_user_meta


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
