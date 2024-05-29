from datetime import datetime
from pydantic import Field, BaseModel
from typing import Optional


class BookInput(BaseModel):
    date: datetime = Field(..., description='book publishing date')
    title: str = Field(..., description='book title')
    writer: str = Field(..., description='book writer name')
    rack_no: int = Field(..., description="rack number where book is placed")
    publisher: str = Field(None, description='book publisher name')
    description:  Optional[str] = Field(None, description='book summary')


class BookSchema(BookInput):
    id: int = Field(gt=0)
    is_issued: bool = Field(False, description='Is book issued')
    issued_by:  Optional[str] = Field(
        None, description='user uid who issued this book')

    class Config:
        orm_mode = True
