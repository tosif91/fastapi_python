from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.books.models import BookModel
from fastapi import Depends
import src.exceptions as exp
from src.users.models import UserModel
from src.dependencies import getCurrentUser
from src.users.crud import get_user_by_email
from typing import List
from src.books.schemas import BookInput


def getBookByID(db: Session, id: int):
    book = db.query(BookModel).filter(BookModel.id == id).first()
    if not book:
        exp.notFoundException
    return book


def getAllBooks(db: Session):
    return db.query(BookModel).all()


def getBookBy(db: Session, user: UserModel, isIssued: bool | None = False,):
    if user.role != "Librarian":  # type:ignore
        raise exp.forbiddenException
    books: List[BookModel] = []
    if isIssued:
        result = db.query(BookModel).filter(BookModel.is_issued).all()
        books.extend(result)
    else:
        result = db.query(BookModel).filter(~BookModel.is_issued).all()
        books.extend(result)
    return books


def update_book_status(db: Session, uid: int, book_id: int, book_status: bool):
    book = db.query(BookModel).filter(
        and_(BookModel.issued_by == uid, BookModel.id == book_id)).first()

    if not book:
        return {"message": "no book issue with this id"}
    if book_status and book.is_issued:  # type:ignore
        return {"message": "this book is already issued"}
    book.is_issued = book_status  # type:ignore
    book.issued_by = None  # type:ignore
    db.commit()


def add_book(db: Session, book_data: BookInput):
    book_db = BookModel(**book_data.model_dump(), is_issued=True, issued_by=1)

    db.add(BookModel(**book_data.model_dump()))
    db.commit()
    db.refresh(BookModel)

    return book_db


def removeBook(db: Session, book_id: int):
    book = db.query(BookModel).filter(BookModel.id == book_id).delete()
    db.commit()
