from passlib.context import CryptContext 


pwd_context = CryptContext(schemes=['bcrypt'],deprecated = ['auto'])

def validatePassword(plain_pwd:str,hashed_pwd:str)->bool:
    return pwd_context.verify(plain_pwd,hashed_pwd)

def hashPassword(plain_pwd:str)->str: 
    return pwd_context.hash(plain_pwd)