from fastapi import FastAPI, status, HTTPException
from contextlib import asynccontextmanager
import uvicorn
import models, schemas
from database import init_models, database

# init_models()
@asynccontextmanager
async def lifespan(app: FastAPI):
    database.connect()
    yield
    database.disconnect()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Test API for FastAPI and Async SQLAlchemy."}

@app.get("/users/{user_id}", response_model=schemas.User, status_code=status.HTTP_200_OK)
async def get_user(user_id: int):
    query = models.users.select().where(models.users.c.id == user_id)
    result = await database.fetch_one(query)
    if result:
        return result
    return HTTPException(status_code=404, detail=f"User id = {user_id} not found")

@app.get("/users/", response_model=list[schemas.User], status_code=status.HTTP_200_OK)
async def get_users():
    query = models.users.select()
    result = await database.fetch_all(query)
    if result:
        return result
    return HTTPException(status_code=404, detail="Users not found")

@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def get_users(user: schemas.UserCreate):
    query = models.users.insert().values(lastname=user.lastname, firstname=user.firstname, email=user.email,
                                         password=user.password)
    last_record_id = await database.execute(query)
    if last_record_id:
        return {**user.dict(), "id": last_record_id}
    else:
        return HTTPException(status_code=404, detail="User not add")

@app.put("/users/{user_id}", response_model=schemas.User, status_code=status.HTTP_202_ACCEPTED)
async def update_user(user_id: int, new_user: schemas.UserCreate):
    query = models.users.update().where(models.users.c.id == user_id).values(**new_user.dict())
    result = await database.execute(query)
    if result:
        return {**new_user.dict(), "id": user_id}
    else:
        return HTTPException(status_code=404, detail=f"User id = {user_id} not update")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)