from app.database import SessionLocal
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_hash_pw(password):
    return pwd_context.hash(password)

def varify_password(hash_pw,password):
    return pwd_context.verify(password,hash_pw)