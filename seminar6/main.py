from fastapi import FastAPI
import uvicorn
# from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
import models, schemas

app = FastAPI()

@app.get("/users/{user_id}", response_model=schemas.User)
async def get_user(db: AsyncSession, user_id: int):
    return await db.query(models.User).filter(models.User.id == user_id).first()

@app.get("/users/", response_model=list[schemas.User])
async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    return awadb.query(models.User).offset(skip).limit(limit).all()

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)