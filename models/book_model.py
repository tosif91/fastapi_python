from  pydantic import  BaseModel,Field
from typing import  Optional

# "author": "Chinua Achebe",
# "country": "Nigeria",
# "imageLink": "images/things-fall-apart.jpg",
# "language": "English",
# "link": "https://en.wikipedia.org/wiki/Things_Fall_Apart\n",
# "pages": 209,
# "title": "Things Fall Apart",
# "year": 1958
class Book:
    author: str
    country: str
    imageLink: str
    language: str
    pages: int
    title: str
    year: int
    link: str

    def __init__(self,author,country,imageLink,language,pages,title,year,link):
        self.author = author
        self.country = country
        self.imageLink = imageLink
        self.language = language
        self.pages = pages
        self.title = title
        self.year = year
        self.link = link




class BookRequest(BaseModel):
    author: str = Field(min_length=3, )  # filed is used for data validation
    country: str = Field(min_length=1)
    imageLink: Optional[str] = Field(title='image link  is not needed')  # to make any field optional
    # title helps in understanding the schema
    language: str
    pages: int
    title: str = Field(min_length=1, max_length=200)
    link: str = Field(min_length=1)
    year: int = Field(gt=1900, lt=2023)  # greater then and lesser then

    class Config:#you can change the example present on swagger ui according to you somplicity
        json_schema_extra = {
            'example':{
                'title':'this ia title'
            }
        }

