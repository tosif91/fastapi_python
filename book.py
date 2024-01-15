import database.book_db as db

from fastapi import FastAPI,Body
app = FastAPI()

#how many apis we have to create
"""
1. getbooks => returns all books data 
2. getbookbytitle => returns a book with given title
3. getbookbyauthor => retusn a list of book  written by given author
4. getbookbycountryandyear => returns a list of book of a given country written in a given year
5. createbook => add book from the boody in the database
6. updatebook => update the data present in databse by author and title
7. deletebook -> """

@app.get('/books')
async def getBooks():
    return db.books

@app.get('/books/{title}')
async def getBookByTitle(title):
    for book in db.books:
         if title.casefold() == book.get('title').casefold() :
            return book

@app.get('/books/author/')
async def getBookByAuthor(author:str):
    booksFound =[]
    for book in db.books:
        if author.casefold() == book.get('author').casefold():
            booksFound.append(book)
    return booksFound

@app.get('/books/')
async def getBookByCountryandYear(country:str,year:int):
    booksFound = []
    for book in db.books:
        if country.casefold() == book.get('country').casefold() and\
            year == book.get('year'):
            booksFound.append(book)

    return booksFound

@app.post('/books/createbook')
async def createBook(data=Body()):
    db.books.append(data)
    return True

@app.put('/books/updatebook')
async def udpateBook(newbook = Body()):
    for i in range(len(db.books)):
        if newbook.get('title') == db.books[i].get('title'):
            db.books[i] = newbook
            return True
    return False

@app.delete('/books/delete_book/{booktitle}')
async def deletebook(booktitle:str):
    pass
