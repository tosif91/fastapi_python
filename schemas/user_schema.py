from enum import Enum
from pydantic import BaseModel, Field


class _UserRole(str, Enum):
    Librarian = 'Librarian',
    Member = 'Member'


class Meta(BaseModel):
    total_book_issued: int = 0
    total_book_returned: int = 0


class UserInputSchema(BaseModel):
    name: str = Field(..., max_length=20, min_length=5,
                      description='user full name', examples=['tosif khan'])
    email: str = Field(..., max_length=40, min_length=5, pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                       description="User's email address", examples=['tosifmid@gmail.com'])
    password: str = Field(..., max_length=10, min_length=6,
                          description='user password', examples=['pwd123'])
    role: _UserRole = Field(...,
                            description='enter user role ie Librarion | Member')


class UserSchema(UserInputSchema):
    uid: int = Field(gt=0,)
    hashed_password: str
    meta: Meta = Field(Meta())

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    name: str
    email: str
    role: _UserRole
    meta: Meta
