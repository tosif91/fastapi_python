import src.database as db
from sqlalchemy import Column, Boolean, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class UserMetaModel(db.Base):
    __tablename__ = 'usersmeta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    totalbookissued = Column(Integer, nullable=True, default=0)
    totalbookreturned = Column(Integer, nullable=True, default=0)

    uid = Column(Integer, ForeignKey("users.id"), unique=True)
    user = relationship("UserModel", back_populates='meta')


class UserModel(db.Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(20), index=True)  # indexing done
    email = Column(String(50), index=True, unique=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String(50), nullable=False, index=True)

    meta = relationship("UserMetaModel", back_populates="user", uselist=False)
    book_rel = relationship(
        "BookModel", back_populates='user_rel', uselist=True)
