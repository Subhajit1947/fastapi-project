from fastapi import FastAPI
from .routes import user,post,auth
from app import models
from app.database import engine,SessionLocal


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}