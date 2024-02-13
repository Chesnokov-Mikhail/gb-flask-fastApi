from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base


class Status(enum.Enum):
    open: int = 0
    paid: int = 1
    delivery: int = 2
    closed: int = 3


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    lastname = Column(String(40), nullable=False)
    firstname = Column(String(40), nullable=False)
    email = Column(String(100), nullable=False)
    hashed_password = Column(String)

    orders = relationship("Order", back_populates="owner")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String(1000))
    price = Column(Float, nullable=False)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(Status), nullable=False)

    owner = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")