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
    raise HTTPException(status_code=404, detail=f"User id = {user_id} not found")

@app.get("/users/", response_model=list[schemas.User], status_code=status.HTTP_200_OK)
async def get_users():
    query = models.users.select()
    result = await database.fetch_all(query)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Users not found")

@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def post_user(user: schemas.UserCreate):
    query = models.users.insert().values(lastname=user.lastname, firstname=user.firstname, email=user.email,
                                         password=user.password)
    last_record_id = await database.execute(query)
    if last_record_id:
        return {**user.dict(), "id": last_record_id}
    else:
        raise HTTPException(status_code=404, detail="User not add")

@app.put("/users/{user_id}", response_model=schemas.User, status_code=status.HTTP_202_ACCEPTED)
async def update_user(user_id: int, new_user: schemas.UserCreate):
    query = models.users.update().where(models.users.c.id == user_id).values(**new_user.dict())
    result = await database.execute(query)
    if result:
        return {**new_user.dict(), "id": user_id}
    else:
        raise HTTPException(status_code=404, detail=f"User id = {user_id} not update")

@app.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
async def deleted_user(user_id: int):
    query = models.orders.select().where(models.orders.c.user_id == user_id)
    result = await database.fetch_all(query)
    if result:
        raise HTTPException(status_code=404, detail=f"The user id = {user_id} is used in orders {result},"
                                                    f" connot be deleted")
    else:
        query = models.users.delete().where(models.users.c.id == user_id)
        result = await database.execute(query)
        if result:
            return {'id': user_id,
                    'message': 'User deleted'
                    }
    raise HTTPException(status_code=404, detail=f"User id = {user_id} not deleted")

@app.get("/products/{prod_id}", response_model=schemas.Product, status_code=status.HTTP_200_OK)
async def get_product(prod_id: int):
    query = models.products.select().where(models.products.c.id == prod_id)
    result = await database.fetch_one(query)
    if result:
        return result
    raise HTTPException(status_code=404, detail=f"Product id = {prod_id} not found")

@app.get("/products/", response_model=list[schemas.Product], status_code=status.HTTP_200_OK)
async def get_products():
    query = models.products.select()
    result = await database.fetch_all(query)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Products not found")

@app.post("/products/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
async def post_product(product: schemas.ProductCreate):
    query = models.products.insert().values(title=product.title, description=product.description, price=product.price)
    last_record_id = await database.execute(query)
    if last_record_id:
        return {**product.dict(), "id": last_record_id}
    else:
        raise HTTPException(status_code=404, detail="Product not add")

@app.put("/products/{prod_id}", response_model=schemas.Product, status_code=status.HTTP_202_ACCEPTED)
async def update_product(prod_id: int, new_prod: schemas.ProductCreate):
    query = models.products.update().where(models.products.c.id == prod_id).values(**new_prod.dict())
    result = await database.execute(query)
    if result:
        return {**new_prod.dict(), "id": prod_id}
    else:
        raise HTTPException(status_code=404, detail=f"Product id = {prod_id} not update")

@app.delete("/products/{prod_id}",  status_code=status.HTTP_200_OK)
async def deleted_product(prod_id: int):
    query = models.orders.select().where(models.orders.c.product_id == prod_id)
    result = await database.fetch_all(query)
    if result:
        raise HTTPException(status_code=404, detail=f"The product id = {prod_id} is used in orders {result},"
                                                    f" connot be deleted")
    else:
        query = models.products.delete().where(models.products.c.id == prod_id)
        result = await database.execute(query)
        if result:
            return {'id': prod_id,
                    'message': 'Product deleted'
                    }
    raise HTTPException(status_code=404, detail=f"Product id = {prod_id} not deleted")

@app.get("/orders/{ord_id}", response_model=schemas.Order, status_code=status.HTTP_200_OK)
async def get_order(ord_id: int):
    query = models.orders.select().where(models.orders.c.id == ord_id)
    result = await database.fetch_one(query)
    if result:
        return result
    raise HTTPException(status_code=404, detail=f"Orders id = {ord_id} not found")

@app.get("/orders/user/{user_id}", response_model=list[schemas.Order], status_code=status.HTTP_200_OK)
async def get_order_user(user_id: int):
    query = models.orders.select().where(models.orders.c.user_id == user_id)
    result = await database.fetch_all(query)
    if result:
        return result
    raise HTTPException(status_code=404, detail=f"Orders id = {user_id} not found")

@app.get("/orders/", response_model=list[schemas.Order], status_code=status.HTTP_200_OK)
async def get_orders():
    query = models.orders.select()
    result = await database.fetch_all(query)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Orders not found")

@app.post("/orders/", response_model=schemas.Order, status_code=status.HTTP_201_CREATED)
async def post_order(order: schemas.OrderCreate):
    query = models.orders.insert().values(user_id=order.user_id, product_id=order.product_id,
                                          created_at=order.created_at, status=order.status)
    last_record_id = await database.execute(query)
    if last_record_id:
        return {**order.dict(), "id": last_record_id}
    else:
        raise HTTPException(status_code=404, detail="Order not add")

@app.put("/orders/{ord_id}", response_model=schemas.Order, status_code=status.HTTP_202_ACCEPTED)
async def update_order(ord_id: int, new_ord: schemas.OrderCreate):
    query = models.orders.update().where(models.orders.c.id == ord_id).values(**new_ord.dict())
    result = await database.execute(query)
    if result:
        return {**new_ord.dict(), "id": ord_id}
    else:
        raise HTTPException(status_code=404, detail=f"Order id = {ord_id} not update")

@app.delete("/orders/{ord_id}", status_code=status.HTTP_200_OK)
async def update_order(ord_id: int):
    query = models.orders.delete().where(models.orders.c.id == ord_id)
    result = await database.execute(query)
    if result:
        return {'id': ord_id,
                'message': 'Order deleted'
                }
    raise HTTPException(status_code=404, detail=f"Order id = {ord_id} not deleted")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)