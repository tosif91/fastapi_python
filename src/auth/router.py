from fastapi import Depends, APIRouter, HTTPException, status
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
import jwt
from datetime import time, timezone, timedelta, datetime
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.users.schemas import UserInputSchema
from src.auth.models import Token, TokenData
from sqlalchemy.orm import Session
from src.database import get_db
import src.auth.service as service


router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post("/token")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    user = service.authenticateUser(db, form.username, form.password)
    token = service. createAccessToken(
        user.model_dump(), 1)
    return Token(access_token=token)


@router.post("/signup")
def signUp(data: UserInputSchema, db: Session = Depends(get_db)):
    service. validateEmailAddress(db, data.email)
    user = service.create_user(db, data)
    token = service. createAccessToken(
        TokenData(email=user.email,  # type: ignore
                  name=user.name,  # type: ignore
                  id=user.id).model_dump(), 1)  # type: ignore
    return Token(access_token=token)
