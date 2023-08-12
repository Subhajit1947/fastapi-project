from datetime import datetime, timedelta
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app import schema,utils,models
from sqlalchemy.orm import Session
from app.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY =settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({'exp':expire})
    token=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token

def varify_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        uid:str=payload.get('user_id')
        
        # if uid is None:
        #     raise credentials_exception
        tokendata=schema.Tokendata(id=str(uid))
        
        return tokendata  
    except:
        raise credentials_exception
    

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(utils.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    uid=varify_token(token,credentials_exception)
    user=db.query(models.User).get(int(uid.id))
    return user
