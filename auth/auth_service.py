from fastapi import Depends, APIRouter, HTTPException, status
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
import jwt
from datetime import time, timezone, timedelta, datetime
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import database as db
from auth.password_service import validatePassword, hashPassword
from schemas.user_schema import UserInputSchema, UserSchema
from auth.token_models import Token, TokenData
import crud.user_crud as crud
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(prefix='/auth', tags=['Authentication'])


authBearer = OAuth2PasswordBearer('/auth/token')

_credentialException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')

# - openssl rand -hex 32
SECRET_KEY = 'fdebadb7a1472709cf78e8dede61062a47328a59dd14cf9de457d69e404e3856'
ALGORITHM = 'HS256'


def _authenticateUser(db: Session, email: str, password: str) -> TokenData:
    # check from the database
    user = crud.get_user_by_email(db, email)
    if not user:
        raise _credentialException
    status = validatePassword(password, user.hashed_password)  # type:ignore
    if not status:
        raise _credentialException
    # user is authenticated
    return TokenData(name=user.name, email=user.email)  # type:ignore


def _createAccessToken(data: dict, expire_in_min: float) -> str:
    to_encode = data.copy()
    to_encode['exp'] = datetime.now(
        timezone.utc) + timedelta(minutes=expire_in_min)

    try:
        token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    except InvalidTokenError:
        raise _credentialException
    return token


def _decodeToken(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
    except ExpiredSignatureError:
        raise _credentialException
    return payload


def getCurrentUser(token: str = Depends(authBearer)):
    payload = _decodeToken(token)
    if payload is None:
        raise _credentialException
    return payload


def _validateEmailAddress(db: Session, email: str):
    user = crud.get_user_by_email(db, email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Email already used")


@router.post("/token")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    user = _authenticateUser(db, form.username, form.password)
    token = _createAccessToken(
        user.model_dump(), 1)
    return Token(access_token=token)


@router.post("/signup")
def signUp(data: UserInputSchema, db: Session = Depends(get_db)):
    _validateEmailAddress(db, data.email)
    crud.create_user(db, data)
    token = _createAccessToken(
        TokenData(email=data.email, name=data.name).model_dump(), 1)
    return Token(access_token=token)
