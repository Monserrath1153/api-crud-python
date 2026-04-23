from pydantic import BaseModel
from typing import List, Optional

class CategoriasBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class CategoriasCreate(CategoriasBase):
    pass

class Categorias(CategoriasBase):
    id: int

    class Config:
        from_attributes = True

class ProductosBase(BaseModel):
    nombre: str
    precio: float
    stock: int = 0
    categoria_id: int

class ProductosCreate(ProductosBase):
    pass

class Productos(ProductosBase):
    id: int

    categoria: Optional[Categorias] = None
    proveedores: List['Proveedores'] = []
    class Config:
        from_attributes = True

class ProveedoresBase(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None

class ProveedoresCreate(ProveedoresBase):
    pass

class Proveedores(ProveedoresBase):
    id: int

    class Config:
        from_attributes = True

Categorias.model_rebuild()
Productos.model_rebuild()
Proveedores.model_rebuild()