from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

import models, schemas, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "API de tienda con base de datos",
    description = "API RESTful para gestionar productos, categorías y proveedores",
    version = "1.0.0"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/categorias/", response_model=schemas.Categorias, status_code=status.HTTP_201_CREATED)
def crear_categoria(categoria: schemas.CategoriasCreate, db: Session = Depends(get_db)):
    return crud.create_categoria(db=db, categoria=categoria)

@app.get("/categorias/", response_model=List[schemas.Categorias])
def leer_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categorias = crud.get_categorias(db, skip=skip, limit=limit)
    return categorias

@app.get("/categorias/{categoria_id}", response_model=schemas.Categorias)
def leer_categoria(categoria_id: int, db: Session = Depends(get_db)):
    db_categoria = crud.get_categoria(db, categoria_id=categoria_id)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria

@app.put("/categorias/{categoria_id}", response_model=schemas.Categorias)
def actualizar_categoria(categoria_id: int, categoria: schemas.CategoriasCreate, db: Session = Depends(get_db)):

    db_categoria = crud.update_categoria(db, categoria_id, categoria)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria

@app.delete("/categorias/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    eliminado = crud.delete_categoria(db, categoria_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return None

@app.post("/productos/", response_model=schemas.Productos, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: schemas.ProductosCreate, db: Session = Depends(get_db)):
    db_producto = crud.create_producto(db=db, producto=producto)
    if db_producto is None:
        raise HTTPException(status_code=400, detail="No se pudo crear el producto. Verifica que la categoria existe")
    return db_producto

@app.get("/productos/", response_model=List[schemas.Productos])
def leer_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    productos = crud.get_productos(db, skip=skip, limit=limit)
    return productos

@app.get("/productos/{producto_id}", response_model=schemas.Productos)
def leer_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = crud.get_producto(db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

@app.get("/categorias/{categoria_id}/productos/", response_model=List[schemas.Productos])
def leer_productos_por_categoria(categoria_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    productos = crud.get_productos_por_categoria(db, categoria_id)
    return productos

@app.put("/productos/{producto_id}", response_model=schemas.Productos)
def actualizar_producto(producto_id: int, producto: schemas.ProductosCreate, db: Session = Depends(get_db)):
    db_producto = crud.update_producto(db, producto_id=producto_id, producto=producto)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado o categoría no existe")
    return db_producto

@app.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    eliminado = crud.delete_producto(db, producto_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return None
@app.patch("/productos/{producto_id}/stock/")
def modificar_stock(producto_id: int, cantidad: int, db: Session = Depends(get_db)):
    db_producto=crud.actualizar_stock(db, producto_id=producto_id, cantidad=cantidad)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    if db_producto.stock < 0:
        raise HTTPException(status_code=400, detail=f"Stock no puede ser negativo, Stock actual: {db_producto.stock}")
    return {"message": f"Stock actualizado, Stock actual: {db_producto.stock}"}

# ENDPOINTS PARA PROVEEDORES
@app.post("/proveedores/", response_model=schemas.Proveedores, status_code=status.HTTP_201_CREATED)
def crear_proveedor(proveedor: schemas.ProveedoresCreate, db: Session = Depends(get_db)):
    return crud.create_proveedor(db=db, proveedor=proveedor)

@app.get("/proveedores/", response_model=List[schemas.Proveedores])
def leer_proveedores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    proveedores = crud.get_proveedores(db, skip=skip, limit=limit)
    return proveedores

@app.get("/proveedores/{proveedor_id}", response_model=schemas.Proveedores)
def leer_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    db_proveedor = crud.get_proveedor(db, proveedor_id=proveedor_id)
    if db_proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return db_proveedor

@app.put("/proveedores/{proveedor_id}", response_model=schemas.Proveedores)
def actualizar_proveedor(proveedor_id: int, proveedor: schemas.ProveedoresCreate, db: Session = Depends(get_db)):
    db_proveedor = crud.update_proveedor(db, proveedor_id, proveedor)
    if db_proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return db_proveedor

@app.delete("/proveedores/{proveedor_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    eliminado = crud.delete_proveedor(db, proveedor_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return None

# ENDPOINTS PARA ASIGNAR/DESASIGNAR PROVEEDORES A PRODUCTOS
@app.post("/productos/{producto_id}/proveedores/{proveedor_id}/", response_model=schemas.Productos, status_code=status.HTTP_201_CREATED)
def asignar_proveedor(producto_id: int, proveedor_id: int, db: Session = Depends(get_db)):
    db_producto = crud.asignar_proveedor_a_producto(db, producto_id, proveedor_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto o proveedor no encontrado")
    return db_producto

@app.delete("/productos/{producto_id}/proveedores/{proveedor_id}/", status_code=status.HTTP_204_NO_CONTENT)
def desasignar_proveedor(producto_id: int, proveedor_id: int, db: Session = Depends(get_db)):
    db_producto = crud.desasignar_proveedor_de_producto(db, producto_id, proveedor_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto o proveedor no encontrado")
    return None