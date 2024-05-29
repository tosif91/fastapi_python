# AUTHENTICATION REQUIRED
# get all users
# get logged in user
# get users who issued atleast one book
# get users who did not issue any book
# get users whoo issued books with title :$title
# get users whose issue books description  contains [words]
# issue book (uid) to the user
# unissue book (uid) from the user


from fastapi import APIRouter, Depends
from typing import Annotated
from src.auth.service import authBearer
from src.dependencies import parse_jwt_token, getCurrentUser
import src.database as db
import src.users.crud as crud
from src.users.schemas import UserInputSchema,   UserResponse, Meta
from sqlalchemy.orm import Session


router = APIRouter(
    prefix='/user', tags=['user'],
    dependencies=[Depends(authBearer)]
)


@router.get('/me')
def getUserProfile(payload: dict = Depends(parse_jwt_token), db: Session = Depends(db.get_db)):

    user = getCurrentUser(db, payload['email'])
    if user:
        user_dict = user.__dict__
        del user_dict['hashed_password']
    return user_dict


@router.get("/",)
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(db.get_db)):
    userList = crud.get_users(db, skip=skip, limit=limit)
    return userList
