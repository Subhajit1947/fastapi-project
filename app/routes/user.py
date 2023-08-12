from fastapi import APIRouter,status,Depends,HTTPException
from app.schema import cuser,userout
from sqlalchemy.orm import Session
from app import utils,models

router=APIRouter()

@router.post('/users',status_code=status.HTTP_201_CREATED,response_model=userout)
def get_users(user:cuser,db:Session=Depends(utils.get_db)):
    hash_pw=utils.get_hash_pw(user.password)
    user.password=hash_pw
    if hash_pw and user.email:
        new_user=models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='invalid email or password')

@router.get('/users/{id}',response_model=userout)
def get_user(id:int,db:Session=Depends(utils.get_db)):
    user=db.query(models.User).get(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'id {id} is not found')
    return user
