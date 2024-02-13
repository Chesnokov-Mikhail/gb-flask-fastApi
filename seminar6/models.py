from datetime import datetime
import sqlalchemy
import enum
from database import metadata


class Status(enum.Enum):
    open: int = 0
    paid: int = 1
    delivery: int = 2
    closed: int = 3


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("lastname", sqlalchemy.String(40), nullable=False),
    sqlalchemy.Column("firstname", sqlalchemy.String(40), nullable=False),
    sqlalchemy.Column("email", sqlalchemy.String(100), nullable=False),
    sqlalchemy.Column("password", sqlalchemy.String)
)

products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(50), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String(1000)),
    sqlalchemy.Column("price", sqlalchemy.Float, nullable=False)
)

products = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("product_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("products.id")),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.utcnow),
    sqlalchemy.Column("status", sqlalchemy.Enum(Status), nullable=False),
)