from sqlalchemy.orm import Session
from sqlalchemy import and_
import models, schemas

def get_categoria(db: Session, categoria_id: int):
    return db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()

def get_categorias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Categoria).offset(skip).limit(limit).all()

def create_categoria(db: Session, categoria: schemas.CategoriasCreate):
    db_categoria = models.Categoria(nombre=categoria.nombre, descripcion=categoria.descripcion)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def update_categoria(db: Session, categoria_id: int, categoria: schemas.CategoriasCreate):
    db_categoria = get_categoria(db, categoria_id)
    if db_categoria:
        db_categoria.nombre = categoria.nombre
        db_categoria.descripcion = categoria.descripcion
        db.commit()
        db.refresh(db_categoria)
    return db_categoria

def delete_categoria(db: Session, categoria_id: int):
    db_categoria = get_categoria(db, categoria_id)
    if db_categoria:
        db.delete(db_categoria)
        db.commit()
        return True
    return False

def get_producto(db: Session, producto_id: int):
    return db.query(models.Producto).filter(models.Producto.id == producto_id).first()

def get_productos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Producto).offset(skip).limit(limit).all()

def get_productos_por_categoria(db: Session, categoria_id: int):
    return db.query(models.Producto).filter(models.Producto.categoria_id == categoria_id).all()

def create_producto(db: Session, producto: schemas.ProductosCreate):
    categoria = get_categoria(db, producto.categoria_id)
    if not categoria:
        return None
    
    db_producto = models.Producto(nombre=producto.nombre, precio=producto.precio, stock=producto.stock, categoria_id=producto.categoria_id)
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def update_producto(db: Session, producto_id: int, producto: schemas.ProductosCreate):
    db_producto = get_producto(db, producto_id)
    if db_producto:
        db_producto.nombre = producto.nombre
        db_producto.precio = producto.precio
        db_producto.stock = producto.stock
        db_producto.categoria_id = producto.categoria_id
        db.commit()
        db.refresh(db_producto)
    return db_producto

def delete_producto(db: Session, producto_id: int):
    db_producto = get_producto(db, producto_id)
    if db_producto:
        db.delete(db_producto)
        db.commit()
        return True
    return False

def actualizar_stock(db: Session, producto_id: int, cantidad: int):
    db_producto = get_producto(db, producto_id)
    if db_producto:
        db_producto.stock = cantidad
        db.commit()
        db.refresh(db_producto)
    return db_producto

# CRUD para Proveedores
def get_proveedor(db: Session, proveedor_id: int):
    return db.query(models.Proveedor).filter(models.Proveedor.id == proveedor_id).first()

def get_proveedores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Proveedor).offset(skip).limit(limit).all()

def create_proveedor(db: Session, proveedor: schemas.ProveedoresCreate):
    db_proveedor = models.Proveedor(
        nombre=proveedor.nombre,
        email=proveedor.email,
        telefono=proveedor.telefono,
        direccion=proveedor.direccion
    )
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

def update_proveedor(db: Session, proveedor_id: int, proveedor: schemas.ProveedoresCreate):
    db_proveedor = get_proveedor(db, proveedor_id)
    if db_proveedor:
        db_proveedor.nombre = proveedor.nombre
        db_proveedor.email = proveedor.email
        db_proveedor.telefono = proveedor.telefono
        db_proveedor.direccion = proveedor.direccion
        db.commit()
        db.refresh(db_proveedor)
    return db_proveedor

def delete_proveedor(db: Session, proveedor_id: int):
    db_proveedor = get_proveedor(db, proveedor_id)
    if db_proveedor:
        db.delete(db_proveedor)
        db.commit()
        return True
    return False

# Asignar proveedor a producto
def asignar_proveedor_a_producto(db: Session, producto_id: int, proveedor_id: int):
    db_producto = get_producto(db, producto_id)
    db_proveedor = get_proveedor(db, proveedor_id)
    if not db_producto or not db_proveedor:
        return None
    
    if db_proveedor not in db_producto.proveedores:
        db_producto.proveedores.append(db_proveedor)
        db.commit()
        db.refresh(db_producto)
    return db_producto

# Desasignar proveedor de producto
def desasignar_proveedor_de_producto(db: Session, producto_id: int, proveedor_id: int):
    db_producto = get_producto(db, producto_id)
    db_proveedor = get_proveedor(db, proveedor_id)
    
    if not db_producto or not db_proveedor:
        return None
    if db_proveedor in db_producto.proveedores:
        db_producto.proveedores.remove(db_proveedor)
        db.commit()
        db.refresh(db_producto)
    return db_producto

