from sqlalchemy import Boolean,Column,ForeignKey,Integer,String,DECIMAL
from database import  Base

class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer,primary_key=True,index=True) #index increase search performance
    # creatorID = Column(Integer, ForeignKey("users.id"))
    title = Column(String,index=True)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean,default=False)

# class User(Base):
#     __tablename__ = 'users'
#
#     id = Column(Integer,primary_key =True)
#     name = Column(String)
#     email = Column(String)
#     mobile = Column(String)
