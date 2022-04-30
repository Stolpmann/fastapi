from passlib.context import CryptContext

## defines what hashing algorimth passlib will use
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)
