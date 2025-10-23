from sqlmodel import SQLModel, Field

class Product(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str
    weight: float
    stock: int
    price: float
    type: str

class ProductRequest(SQLModel):
    name: str
    description: str
    weight: float
    stock: int
    price: float
    type: str

class ProductResponse(SQLModel):
    id: int
    name: str
    description: str
    weight: float
    stock: int
    price: float
    type: str