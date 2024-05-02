from passlib.context import CryptContext

#mentioning which hashing algo to use
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)


#checking if the hashed password from database equals password entered by the user.
def verify(plain_password, hashed_password):
    #verify method in the pwd_context lib will perform the required operations and verify the plain and hashed password 
    return pwd_context.verify(plain_password, hashed_password)