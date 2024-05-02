from typing import Optional
from fastapi import Body, FastAPI
from . import models
from .database import engine, get_db
from .routers import post, user, auth, vote
from .config import settings

# print("sdfsf",settings.database_password)

# from psycopg.extras import RealDictCursor  

#Create an instance of FastAPI
app= FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"msg": "World"}

#creste array with each post stored as a dictionary
# my_posts=[{"title":"title of post 1","content":"content of post 1", "id":1},{"title":"favourite foods","content":"I like pizza","id":2}]

#Path Operation in FASTApi/Route in others
#/ - root path


#not the best practice to retrieve the post : Loops
# def find_post(id):
#     for i in my_posts:
#         if i['id']==id:
#             print("Df",i)
#             return i


# def find_index_post(id:int):
#     for i,ind in enumerate(my_posts):
#         print("i: ",i," ind:",ind)
#         if ind["id"]==id:
#             return i
#     return -1


# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):

#     #pass in the model, currently we only ve the Post model.
#     posts = db.query(models.Post).all()
#     return {"data":posts}







#--------------------------------------------------------------------------------------------------------------------------------------------
#API CALLS using SQL to access the database
#--------------------------------------------------------------------------------------------------------------------------------------------

# @app.get("/posts")
# def get_posts():

#     cursor.execute(""" SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     print(posts)
#     return {"Posts": posts}

# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(post:schemas.Post):
    
#     #use the below methods -%s method, makes sure no weird sql statements are there and prevent any vulenrability to SQL injections.
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """ , 
#                    (post.title,post.content, post.published ))
    
#     new_post= cursor.fetchone()
#     #need to coomit changes to reflect into the database
#     conn.commit()
#     return {"data":new_post}

# # @app.get("/posts/latest")
# # def get_latest():
# #     post=my_posts[len(my_posts)-1]
# #     return {"Latest Post": post} 

# #id is the path parameter

# @app.get("/posts/{id}")
# # def get_post(id: int, response: Response):
# def get_post(id: int):
#     # print(id)
#     # post=find_post(int(id))
#     cursor.execute( """SELECT * FROM posts WHERE id=(%s) """,(id,))
#     get_post=cursor.fetchone()
#     # if not post:
#     #     response.status_code= status.HTTP_404_NOT_FOUND
#     #     return {"Message":f"Post with {id} was not found."}

#     if not get_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} was not found.")

#     return {"post_detail":get_post}


# @app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):

#     # index= find_index_post(id)
#     cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING * """,(str(id),))
#     deleted_post=cursor.fetchone()
#     conn.commit()
#     # if index==-1:
#     if not deleted_post:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"post with id : {id} was not found.")
#     # my_posts.pop(index)
#     print(deleted_post)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.put("/posts/{id}")
# def update_post(id:int, post:schemas.Post):

#     print(post)
#     cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """,
#                    (post.title, post.content, post.published,id))
#     updated_post= cursor.fetchone()
#     conn.commit()

#     # index= find_index_post(id)
    

#     # if index==-1:
#     if not updated_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} was not found.")
#     # post_dict=post.model_dump()
#     # post_dict["id"]=id
#     # my_posts[index]=post_dict


#     return {"data":updated_post}


