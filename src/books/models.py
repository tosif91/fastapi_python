import src.database as db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class BookModel(db.Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False)
    title = Column(String(50), nullable=False, index=True)
    writer = Column(String(30), nullable=False, index=True)
    rack_no = Column(Integer, nullable=False, index=True)
    publisher = Column(String(30), nullable=False, index=True)
    description = Column(String(100), nullable=True)
    is_issued = Column(Boolean, default=False)
    issued_by = Column(Integer, ForeignKey('users.id'),
                       nullable=True)

    user_rel = relationship("UserModel", back_populates='book_rel')
