from fastapi import APIRouter,status,Depends,HTTPException,Response
from app.schema import cpost,allpost,Setvote,Outpost
from sqlalchemy.orm import Session
from app import utils,models,auth2
from typing import List
from sqlalchemy import func

router=APIRouter()

# @router.get('/posts',response_model=List[allpost])
@router.get('/posts',response_model=List[Outpost])
def get_post(db:Session=Depends(utils.get_db),current_user: int = Depends(auth2.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f'unauthorized')
    # posts=db.query(models.Post).all()
    result=db.query(models.Post,func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True)\
        .group_by(models.Post.id)\
        .all()
    posts = []
    for post, vote_count in result:
        posts.append({
            "post": post,
            "votes": vote_count
        })
    if posts:
        return posts
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post not found')
   



@router.get('/posts/{id}',response_model=Outpost)
def get_one_post(id:int,db:Session=Depends(utils.get_db),current_user: int = Depends(auth2.get_current_user)):
    
    # posts11=db.query(models.Post).get(id)
    result=db.query(models.Post,func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True)\
        .group_by(models.Post.id).filter(models.Post.id==id)\
        .first()
   
    
    # print(posts['post'].owner_id)
    if result:
        post1, vote_count=result
        posts={"post":post1,"votes":vote_count}
        if current_user.id!=posts['post'].owner_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f'unauthorized')
        
        return posts
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'id {id} not found')
    
    
    
@router.post('/posts',response_model=allpost)
def create_post(post:cpost,db:Session=Depends(utils.get_db),current_user: int = Depends(auth2.get_current_user)):
    if current_user:
        try:
            new_post=models.Post(owner_id=current_user.id,**post.dict())
            
            db.add(new_post)
            db.commit()
            db.refresh(new_post)
            return new_post
        except:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='somthing went to wrong')
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='not authorized')
    

@router.put('/posts/{id}',response_model=allpost)
def update_one_post(post:cpost,id:int,db:Session=Depends(utils.get_db),current_user: int = Depends(auth2.get_current_user)):
    
    posts=db.query(models.Post).get(id)
    
    if posts:
        if current_user.id!=posts.owner_id:
            
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f'unauthorized')
        posts.title=post.title
        posts.content=post.content
        db.commit()
        return posts
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'id {id} not found')


@router.delete('/posts/{id}',response_model=allpost)
def update_one_post(id:int,db:Session=Depends(utils.get_db),current_user: int = Depends(auth2.get_current_user)):
    
    posts=db.query(models.Post).get(id)
    
    if posts:
        if current_user.id!=posts.owner_id:
            
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f'unauthorized')
        db.delete(posts)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'id {id} not found')



@router.post('/posts/vote')
def create_vote(v:Setvote,db:Session=Depends(utils.get_db),current_user:int=Depends(auth2.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='not authorized')
    vote=db.query(models.Vote).filter_by(post_id=v.post_id,user_id=current_user.id).first()
    if v.dir==1:
        if vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail='you are already vote this post')
        new_vote=models.Vote(user_id=current_user.id,post_id=v.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail='you are already vote this post')
        db.delete(vote)
        db.commit()
        return {"message": "successfully delete vote"}
        

        



