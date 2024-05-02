from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from .config import settings

#tokenURL is the login endpoint
oauth2_scheme= OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY
#Algorithm
#Expiration time - to prevent any user to be logged in forever


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    #datetime.utcnow() - has been deprecated timezone.utc
    expire= datetime.utcnow()+ timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(
        to_encode, SECRET_KEY, algorithm=ALGORITHM
    )

    return encoded_jwt

#credentials_exception - throws exeception if the token has expired or the credentials are not valid
def verify_access_token(token:str, credentials_exception):

    try:
        # print("verify outh2, acces",token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data= schemas.TokenData(id=str(id))
        
    
    except JWTError: #coming from jose lib
        # print("inside execeptipon", e)
        raise credentials_exception
    
    return token_data

def get_current_user(token:str =Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail=f"Couldn't validate credentials.", 
                                          headers={"WWW-Authenticate":"Bearer"})
    
    token= verify_access_token(token, credentials_exception)
    # print("gdf",token)
    #token is in format id='11'. thats why token.id
    user = db.query(models.User).filter(models.User.id==token.id).first()

    return user
