from fastapi import APIRouter,status,Depends,HTTPException

from sqlalchemy.orm import Session
from app import utils,models
from fastapi.security import OAuth2PasswordRequestForm
from app import auth2
router=APIRouter()

@router.post('/login')
def login(credential:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(utils.get_db)):
    user=db.query(models.User).filter_by(email=credential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    if not utils.varify_password(user.password,credential.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    access_token=auth2.create_access_token(data={'user_id':user.id})
    return {'access_token':access_token,'token_type':'bearer'}
