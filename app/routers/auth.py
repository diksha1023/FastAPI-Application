from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
# from ..database import get_db 
from .. import database, schemas, models, utils, oauth2

router= APIRouter(
    tags=['Authentication']
)



@router.post('/login', response_model=schemas.Token)
# def login(user_credentails: schemas.UserLogin, db:Session=Depends(database.get_db)):
def login(user_credentials: OAuth2PasswordRequestForm= Depends(), db:Session=Depends(database.get_db)):
    # OAuth2PasswordRequestForm has fields - usernams, password : {"username":"fsdfs", "password":"dde"}

    # user = db.query(models.User).filter(models.User.email== user_credentials.email).first()
    user = db.query(models.User).filter(models.User.email== user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials.")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials.")
    
    #create token

    access_token= oauth2.create_access_token(data= {"user_id": user.id})

    #return token
    return {"access_token":access_token, "token_type":"bearer"}
