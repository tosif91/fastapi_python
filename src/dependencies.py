from fastapi import Depends
import src.auth.service as auth_service
import jwt
from jwt.exceptions import ExpiredSignatureError
from starlette.config import Config
import src.exceptions as exp
import src.users.crud as user_crud
from sqlalchemy.orm import Session
from src.users.models import UserModel
config = Config(".env")

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")


def parse_jwt_token(token: str = Depends(auth_service.authBearer)) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
    except ExpiredSignatureError:
        raise exp.unauthorizedException
    return payload


def getCurrentUser(db: Session, email: str) -> UserModel:
    return user_crud.get_user_by_email(db, email)
