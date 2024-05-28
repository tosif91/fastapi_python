from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.book_model import BookModel
from fastapi import HTTPException, status


def getBookByID(db: Session, id: int):
    return db.query(BookModel).filter(BookModel.id == id).first()


def getAllBooks(db: Session):
    return db.query(BookModel).all()


def getBookBy(db: Session, isIssued: bool | None = False):
    books = []
    if isIssued:
        books.append(db.query(BookModel).filter(BookModel.is_issued).all())
    else:
        books.append(db.query(BookModel).filter(
            BookModel.is_issued == False).all())
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


def removeBook(db: Session, book_id: int):
    book = db.query(BookModel).filter(BookModel.id == book_id).delete()
    db.commit()
