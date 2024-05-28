import database as db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Relationship


class BookModel:
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=True)
    title = Column(String(50), nullable=True, index=True)
    writer = Column(String(30), nullable=True, index=True)
    rack_no = Column(Integer, nullable=True, index=True)
    publisher = Column(String(30), nullable=True, index=True)
    description = Column(String(100), nullable=False)
    is_issued = Column(Boolean, default=False)
    issued_by = Column(Integer, ForeignKey('users.id'),
                       nullable=False, unique=False)

    user_rel = Relationship("UserModel", back_populates='book_rel')
