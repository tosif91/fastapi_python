# AUTHENTICATION REQUIRED
# get all books
# update book by uid
# add book if user is librarian
# issue book if user is member
# remove book if user is librarian
# get books whose summary contains [words]
# get all issued books
# get all unIssued books
# get all books issued by user

from fastapi import APIRouter, Depends
import src.books.crud as crud
from sqlalchemy.orm import Session
from src.database import get_db
from src.auth.service import authBearer
from src.users.models import UserModel
from src.books.schemas import BookInput
from src.dependencies import parse_jwt_token, getCurrentUser
from typing import List, Dict, Any


router = APIRouter(
    prefix='/books', tags=['book'], dependencies=[Depends(authBearer)])


@router.get('/')
def getAllBooks(db: Session = Depends(get_db)):
    return crud.getAllBooks(db)


@router .get('/{book_id}')
def getBookByID(book_id: int, db: Session = Depends(get_db)):
    return crud.getBookByID(db, book_id)


@router.get('/issued/all/',)
def getAllIssuedBooks(
        db: Session = Depends(get_db),
        payload: dict = Depends(parse_jwt_token)):
    current_user: UserModel = getCurrentUser(db, payload['email'])
    books = crud.getBookBy(db, current_user, True)
    return {"books": books}


@router.post('/add/')
def addBooks(book_data: BookInput, db: Session = Depends(get_db),):

    return crud.add_book(db, book_data)
