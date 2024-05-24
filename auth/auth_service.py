from fastapi import Depends,APIRouter,HTTPException,status
from jwt.exceptions import InvalidTokenError,ExpiredSignatureError
import jwt 
from datetime import time,timezone,timedelta,datetime
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
import database  as db 
from auth.password_service import validatePassword,hashPassword
from models.user_model import UserData,UserInput
from auth.token_models import Token,TokenData

router = APIRouter(prefix='/auth',tags=['Authentication'])


authBearer = OAuth2PasswordBearer('/auth/token')

_credentialException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid username or password')

# - openssl rand -hex 32  
SECRET_KEY = 'fdebadb7a1472709cf78e8dede61062a47328a59dd14cf9de457d69e404e3856'
ALGORITHM = 'HS256'


def _authenticateUser(email:str,password:str)->UserData:
    #check from the database 
    user = next((user for user in db.user_db if  user['email'] == email), None) 
    if user is None:
        raise _credentialException 
    status = validatePassword(password,user['hashed_password'])
    if not status:
        raise _credentialException 
    #user is authenticated 
    return UserData(**user)

    
    
def _createAccessToken(data:dict,expire_in_min:float)->str:
    to_encode = data.copy()
    to_encode['exp'] =  datetime.now(timezone.utc) + timedelta(minutes=expire_in_min)
     
    try:
        token = jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    except InvalidTokenError:
        raise _credentialException 
    return token 
        

def _decodeToken(token:str)->dict: 
    try:
        payload =  jwt.decode(token,SECRET_KEY,[ALGORITHM]) 
    except ExpiredSignatureError:
        raise _credentialException
    return payload

def getCurrentUser(token :str = Depends(authBearer)):
    payload = _decodeToken(token)
    if payload is None:
        raise _credentialException 
    return payload 
    

@router.post("/token")
def login(form:OAuth2PasswordRequestForm = Depends())->Token: 
    user = _authenticateUser(form.username,form.password)
    token = _createAccessToken(TokenData(email=user.email,name=user.name).model_dump(),1)
    return Token(access_token=token)
    
    
    
@router.post("/signup")
def signUp(data:UserInput):
    encrypted_pwd = hashPassword(data.password)
    user_data = UserData(**data.model_dump(),uid=db.CURR_USER_UID,hashed_password=encrypted_pwd)
    _insetUserInDB(user_data)
    token = _createAccessToken(TokenData(email=data.email,name=data.name).model_dump(),1) 
    return Token(access_token=token)
    
    
 
def _insetUserInDB(user:UserData):
    db.user_db.append(user.model_dump())
    db.CURR_USER_UID +=1

