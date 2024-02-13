from pydantic import BaseModel, Field
from datetime import datetime
from models import Status

class OrderBase(BaseModel):
    status: Status = Field(title="Status", default=Status.open)

class OrderCreate(OrderBase):
    created_at: datetime = Field(title="Date_time", default=datetime.utcnow)
    user_id: int = Field(title="User Id")
    product_id: int = Field(title="Product Id")

class Order(OrderCreate):
    id: int

class UserBase(BaseModel):
    lastname: str = Field(title="Lastname", max_length=40)
    firstname: str = Field(title="Firstname", max_length=40)
    email: str = Field(title="Email", max_length=100)


class UserCreate(UserBase):
    password: str = Field(title="Email", min_length=6)


class User(UserBase):
    id: int

class ProductBase(BaseModel):
    title: str = Field(title="Title", max_length=50)
    description: str = Field(title="Description", max_length=1000, default="")
    price: float = Field(0, title="Price", ge=0)


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
