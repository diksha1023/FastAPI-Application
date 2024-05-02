from .. import models, schemas, oauth2 # to go up into the directory, add one more dot
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func #gives access to function like count

from sqlalchemy.orm import Session
from ..database import SessionLocal, get_db


router = APIRouter(
    prefix="/posts", # anytime you call an api, it wull prefix '/posts'
    tags=['Posts']
)
#--------------------------------------------------------------------------------------------------------------------------------------------
#API CALLS using SQLALCHEMY to access the database
#--------------------------------------------------------------------------------------------------------------------------------------------
# @app.get("/posts", response_model=List[schemas.Post])
@router.get("/")
# @router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db),current_user: str=Depends(oauth2.get_current_user), limit: int =10, skip:int =0,
              search: Optional[str]=""):
    # print(current_user.email)

    print(search)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # By default in postgres - it is ‘left outer’ join. By default in sqlalchemy - it is ‘left inner’ join. We need the left outer join.

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes") ).join(models.Vote, models.Vote.post_id==models.Post.id, 
                                                                                          isouter=True).group_by(models.Post.id).all()

    print(results)
    return results
    return posts

    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)
    # return {"Posts": posts}

# @app.post("/posts", status_code=status.HTTP_201_CREATED) #without reponse schema included
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_posts(post:schemas.Post, db: Session = Depends(get_db)):
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db), current_user:  str=Depends(oauth2.get_current_user)):

    #Convert the post message to dictionary object for efficient processing
    # Old - new_post=models.Post(title=post.title, content=post.content, published=post.published)
    # print("user_id:",current_user)
    new_post=models.Post(owner_id= current_user.id, **post.model_dump()) #unpacks the dictionary
    db.add(new_post)
    db.commit()
    #return back the newly created post. In sqlalchemy, we add the new post to the database, then commit it to it.
    #and then refresh the db and retrieve the post we created to new_post variable
    db.refresh(new_post) #-> not a dict, but a sqlalchemy model, so need to convert the sqlalchemy model to pydantic model
    return new_post

    

    #use the below methods -%s method, makes sure no weird sql statements are there and prevent any vulenrability to SQL injections.
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """ , 
    #                (post.title,post.content, post.published ))
    
    # new_post= cursor.fetchone()
    # #need to coomit changes to reflect into the database
    # conn.commit()
    # return {"data":new_post}


@router.get("/{id}",  response_model=schemas.Post)
# def get_post(id: int, response: Response):
def get_post(id: int, db: Session = Depends(get_db), current_user: str=Depends(oauth2.get_current_user)):

    get_post= db.query(models.Post).filter(models.Post.id == id).first()
    # print(id)
    # post=find_post(int(id))
    # cursor.execute( """SELECT * FROM posts WHERE id=(%s) """,(id,))
    # get_post=cursor.fetchone()
    # if not post:
    #     response.status_code= status.HTTP_404_NOT_FOUND
    #     return {"Message":f"Post with {id} was not found."}

    if not get_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} was not found.")

    return get_post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user: str=Depends(oauth2.get_current_user)):
    deleted_post= db.query(models.Post).filter(models.Post.id == id)

    post= deleted_post.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"post with id : {id} was not found.")
    
    print(post)
    
    if current_user.id!= post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform the requested action.")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    # index= find_index_post(id)
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING * """,(str(id),))
    # deleted_post=cursor.fetchone()
    # conn.commit()
    # # if index==-1:
    # if not deleted_post:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"post with id : {id} was not found.")
    # # my_posts.pop(index)
    # print(deleted_post)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",  response_model=schemas.Post)
def update_post(id:int, updated_post:schemas.PostCreate,db: Session = Depends(get_db), current_user: str=Depends(oauth2.get_current_user)):

    post_query= db.query(models.Post).filter(models.Post.id == id)
    post= post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} was not found.")
    

    if current_user.id!= post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform the requested action.")
    
    post_query.update(updated_post.model_dump(), synchronize_session= False)
    db.commit()
    return post_query.first()
    # print(post)
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """,
    #                (post.title, post.content, post.published,id))
    # updated_post= cursor.fetchone()
    # conn.commit()

    # index= find_index_post(id)
    

    # if index==-1:
    # if not updated_post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} was not found.")
    # post_dict=post.model_dump()
    # post_dict["id"]=id
    # my_posts[index]=post_dict


    # return {"data":updated_post}