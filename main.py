import os
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, create_engine, Session, SQLModel, select
from dotenv import load_dotenv
from models.Product import Product, ProductRequest, ProductResponse, ProductPartial, ProductUpdateCamp, ProductUpdateTwoCamp

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

@app.post('/api/product', response_model=dict, tags=["Create"])
def add_product(product: ProductRequest, db: Session = Depends(get_db)):
    insert = Product.model_validate(product)
    db.add(insert)
    db.commit()

    return {"msg": "Producte afegit correctament"}

@app.get('/api/product/{id}', response_model=ProductResponse, tags=["Read one by ID"])
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    statement = select(Product).where(Product.id == id)
    result = db.exec(statement).first()

    return ProductResponse.model_validate(result)

@app.get('/api/products', response_model=list[ProductResponse], tags=["Read products"])
def get_products(db: Session = Depends(get_db)):
    statement = select(Product)
    results = db.exec(statement).all()
    return results

@app.get('/api/product_type/{type}', response_model=list[ProductResponse], tags=["Read all with type"])
def get_product_with_type(type: str, db: Session = Depends(get_db)):
    statement = select(Product).where(Product.type == type)
    results = db.exec(statement).all()
    return results 

@app.delete('/api/product/delete/{id}', response_model=dict, tags=["Delete product by ID"])
def delete_product(id: int, db: Session = Depends(get_db)):
    statement = select(Product).where(Product.id == id)
    result = db.exec(statement).one()
    db.delete(result)
    db.commit()
    return {"msg": "Producte eliminat correctament"}

@app.get('/api/product_partial/{id}', response_model=ProductPartial, tags=["Read product partial by ID"])
def read_product_partial_by_id(id: int, db: Session = Depends(get_db)):
    statement = select(Product).where(Product.id == id)
    result = db.exec(statement).first()
    return ProductPartial.model_validate(result)

@app.put('/api/product/{id}', response_model=dict, tags=["Update product"])
def update_product_by_id(id: int, product: ProductRequest, db: Session = Depends(get_db)):
    product_select = db.get(Product, id)

    if not product_select:
        return {"msg": "El producte no existeix"}
    
    product_data = product.model_dump(exclude_unset=True)
    product_select.sqlmodel_update(product_data)

    db.add(product_select)
    db.commit()
    db.refresh(product_select)

    return {"msg": "Producte actualizat correctament"}

@app.patch('/api/product/{id}', response_model=dict, tags=["Update partial one camp by id"])
def update_product_partial_by_id(id: int, product: ProductUpdateCamp, db: Session = Depends(get_db)):
    product_select = db.get(Product, id)

    if not product_select:
        return {"msg": "El producte no existeix"}
    
    product_data = product.model_dump(exclude_unset=True)
    product_select.sqlmodel_update(product_data)

    db.add(product_select)
    db.commit()
    db.refresh(product_select)

    return {"msg": "Camp nom de producte actualizat correctament"}

@app.patch('/api/product_dos_camps/{id}', response_model=dict, tags=["Update partial two camps by id"])
def update_product_partial_by_id(id: int, product: ProductUpdateTwoCamp, db: Session = Depends(get_db)):
    product_select = db.get(Product, id)

    if not product_select:
        return {"msg": "El producte no existeix"}
    
    product_data = product.model_dump(exclude_unset=True)
    product_select.sqlmodel_update(product_data)

    db.add(product_select)
    db.commit()
    db.refresh(product_select)

    return {"msg": "Camp nom i preu de producte actualizat correctament"}