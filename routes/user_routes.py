#AUTHENTICATION REQUIRED
#get all users 
#get logged in user 
#get users who issued atleast one book 
#get users who did not issue any book 
#get users whoo issued books with title :$title 
#get users whose issue books description  contains [words]
#issue book (uid) to the user
#unissue book (uid) from the user 


from fastapi import APIRouter,Depends
from typing import Annotated
from auth.auth_service import getCurrentUser ,authBearer
import database as db 

router = APIRouter(prefix='/user',tags=['user'],dependencies= [Depends(authBearer)] )


@router.get('/')
def getAllUser( ):
    return db.user_db

@router.get('/me')
def getUserProfile(user_dict:dict=Depends(getCurrentUser) ):
    user = next((user for user in db.user_db if user['email']== user_dict['email']) , None)
    return user 
    


