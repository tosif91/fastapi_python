#AUTHENTICATION REQUIRED
#get all books 
#update book by uid 
#add book if user is librarian 
#issue book if user is member 
#remove book if user is librarian 
#get books whose summary contains [words]
#get all issued books 
#get all unIssued books 
#get all books issued by user 

from fastapi import APIRouter 


router = APIRouter(prefix='/books',tags=['book'])