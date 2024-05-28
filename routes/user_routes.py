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
from auth.auth_service import getCurrentUser, authBearer
import database as db
import crud.user_crud as crud
from schemas.user_schema import UserInputSchema, UserSchema, UserResponse, Meta
from sqlalchemy.orm import Session


router = APIRouter(
    prefix='/user', tags=['user'],
    dependencies=[Depends(authBearer)]
)


@router.get('/me')
def getUserProfile(user_dict: dict = Depends(getCurrentUser), db: Session = Depends(db.get_db)):
    user = crud.get_user_by_email(db, user_dict['email'])
    if user:
        user_dict = user.__dict__
        del user_dict['hashed_password']
    return user_dict


@router.get("/",)
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(db.get_db)):
    userList = crud.get_users(db, skip=skip, limit=limit)
    return userList
