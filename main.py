import os
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, create_engine, Session, SQLModel, select
from dotenv import load_dotenv
from models.Product import Product, ProductRequest, ProductResponse

app = FastAPI() # Iniciar la API

load_dotenv() # Cargar las variables de entorno

DATABASE_URL = os.getenv("DATABASE_URL") # Obtener la url de la base de datos

engine = create_engine(DATABASE_URL) # Motor de la base de datos

SQLModel.metadata.create_all(engine)

def get_db():
    db = Session(engine)

    try:
        yield db
    finally:
        db.close() 

@app.post('api/product', response_model=dict, tags=["Create"])
def add_product(product: ProductRequest, db: Session = Depends(get_db)):
    insert = Product.model_validate(product)
    db.add(insert)
    db.commit()

    return {"msg": "Producte afegit"}

@app.get('api/product/{id}', response_model=ProductResponse, tags=["Read one by ID"])
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    statement = select(Product).where(Product.id == id)
    result = db.exec(statement).first()

    return ProductResponse.model_validate(result)

@app.get('api/products', response_model=list[ProductResponse], tags=["Read products"])
def get_products(db: Session = Depends(get_db)):
    statement = select(Product)
    results = db.exec(statement).all()
    return results

@app.get('api/product/{type}', response_model=list[ProductResponse], tags=["Read all with type"])
def get_product_with_type(type: str, db: Session = Depends(get_db)):
    statement = select(Product).where(Product.type == type)
    results = db.exec(statement).all()
    return results 