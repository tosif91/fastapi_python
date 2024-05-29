from fastapi import Depends, APIRouter, HTTPException, status
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
import jwt
from datetime import time, timezone, timedelta, datetime
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.users.schemas import UserInputSchema
from src.auth.models import Token, TokenData
import src.users.crud as crud
from sqlalchemy.orm import Session
import src.exceptions as exp
from starlette.config import Config
from passlib.context import CryptContext
from src.users.models import UserModel, UserMetaModel
from starlette.config import Config


config = Config(".env")

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")

pwd_context = CryptContext(schemes=['bcrypt'], deprecated=['auto'])
authBearer = OAuth2PasswordBearer('/auth/token')


def authenticateUser(db: Session, email: str, password: str) -> TokenData:
    # check from the database
    user = crud.get_user_by_email(db, email)
    if not user:
        raise exp.notFoundException
    status = validatePassword(password, user.hashed_password)  # type:ignore
    if not status:
        raise exp.unauthorizedException
    return TokenData(name=user.name,  # type: ignore
                     email=user.email,  # type: ignore
                     id=user.id,)  # type: ignore


def createAccessToken(data: dict, expire_in_min: float) -> str:
    to_encode = data.copy()
    to_encode['exp'] = datetime.now(
        timezone.utc) + timedelta(minutes=expire_in_min)

    try:
        token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    except InvalidTokenError:
        raise exp.unauthorizedException
    return token


def validateEmailAddress(db: Session, email: str):
    user = crud.get_user_by_email(db, email)
    if user:
        raise exp.conflictException


def validatePassword(plain_pwd: str, hashed_pwd: str) -> bool:
    return pwd_context.verify(plain_pwd, hashed_pwd)


def hashPassword(plain_pwd: str) -> str:
    return pwd_context.hash(plain_pwd)


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
        raise exp.badRequestException

    return db_user


def _create_user_meta(db: Session, uid: int) -> UserMetaModel:
    db_user_meta = UserMetaModel(
        totalbookissued=0, totalbookreturned=0, uid=uid)
    db.add(db_user_meta)
    db.commit()
    db.refresh(db_user_meta)
    return db_user_meta
