from .. import models, schemas, utils # to go up into the directory, add one more dot
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import SessionLocal, get_db

#to access the app, we need to import the APIRouter library from  the fastapi library
router = APIRouter(
    prefix="/users",
    tags=['Users']
)

#replace app with router variable
# @app.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    #create hash of the password. -  user.password
    #reference the password context, defined at the top
    hashed_password = utils.hash(user.password)
    user.password= hashed_password
    new_user= models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


#get user info based on the USER id. Useful in retrieving profiles and passsing to the frontend, or keeping users logged in using jwt tokens
@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} doesn't exist.")
    return user
