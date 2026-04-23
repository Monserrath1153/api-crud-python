from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Tabla de asociación para relación muchos a muchos entre Producto y Proveedor
producto_proveedor = Table(
    'producto_proveedor',
    Base.metadata,
    Column('producto_id', Integer, ForeignKey('productos.id'), primary_key=True),
    Column('proveedor_id', Integer, ForeignKey('proveedores.id'), primary_key=True)
)

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True, nullable=False)
    descripcion = Column(String)

    productos = relationship("Producto", back_populates="categoria")

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))

    categoria = relationship("Categoria", back_populates="productos")
    proveedores = relationship("Proveedor", secondary=producto_proveedor, back_populates="productos")

class Proveedor(Base):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telefono = Column(String)
    direccion = Column(String)

    productos = relationship("Producto", secondary=producto_proveedor, back_populates="proveedores")