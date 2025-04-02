import re
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum as PyEnum

# Expresión regular para validar correos electrónicos
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

def validate_email(value: str) -> str:
    if not re.match(EMAIL_REGEX, value):
        raise ValueError('Formato de email inválido')
    return value

class Categoria(BaseModel):
    id_categoria: Optional[int] = None
    nombre: str = Field(..., max_length=50)

    class Config:
        from_attributes = True

class Cliente(BaseModel):
    id_cliente: Optional[int] = None
    nombre: str = Field(..., max_length=100)
    email: str = Field(..., max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    fecha_registro: Optional[datetime] = None

    class Config:
        from_attributes = True

    def __init__(self, **data):
        super().__init__(**data)
        self.email = validate_email(self.email)

class DireccionCliente(BaseModel):
    id_direccion: Optional[int] = None
    id_cliente: int
    direccion: str = Field(..., max_length=255)

    class Config:
        from_attributes = True

class EstadoPedido(BaseModel):
    class NombreEstado(str, PyEnum):
        pendiente = "pendiente"
        procesado = "procesado"
        enviado = "enviado"
        cancelado = "cancelado"
    
    id_estado: Optional[int] = None
    nombre_estado: NombreEstado

    class Config:
        from_attributes = True

class MarcaEditorial(BaseModel):
    id_marca_editorial: Optional[int] = None
    nombre: str = Field(..., max_length=100)

    class Config:
        from_attributes = True

class Membresia(BaseModel):
    class TipoMembresia(str, PyEnum):
        regular = "regular"
        gold = "gold"
        platinum = "platinum"
    
    id_membresia: Optional[int] = None
    tipo: TipoMembresia

    class Config:
        from_attributes = True

class Proveedor(BaseModel):
    id_proveedor: Optional[int] = None
    nombre: str = Field(..., max_length=100)
    email: str = Field(..., max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)

    class Config:
        from_attributes = True

    def __init__(self, **data):
        super().__init__(**data)
        self.email = validate_email(self.email)

class Producto(BaseModel):
    id_producto: Optional[int] = None
    nombre: str = Field(..., max_length=100)
    descripcion: Optional[str] = None
    id_categoria: int
    stock_actual: Optional[int] = None
    precio: float = Field(..., gt=0)
    id_marca_editorial: Optional[int] = None
    fecha_lanzamiento: Optional[datetime] = None
    imagen_url: Optional[str] = Field(None, max_length=255)
    id_proveedor: Optional[int] = None

    class Config:
        from_attributes = True

class Pedido(BaseModel):
    id_pedido: Optional[int] = None
    fecha_creacion: Optional[datetime] = None
    id_cliente: int
    total: float = Field(..., gt=0)
    id_estado: int
    id_direccion: int

    class Config:
        from_attributes = True

class DetallePedido(BaseModel):
    id_detalle: Optional[int] = None
    id_pedido: int
    id_producto: int
    cantidad: int = Field(..., gt=0)
    precio_unitario: float = Field(..., gt=0)

    class Config:
        from_attributes = True

class HistorialAbastecimiento(BaseModel):
    id_abastecimiento: Optional[int] = None
    id_proveedor: int
    id_producto: int
    cantidad: int = Field(..., gt=0)
    fecha_abastecimiento: Optional[datetime] = None

    class Config:
        from_attributes = True

class ClienteMembresia(BaseModel):
    id_cliente: int
    id_membresia: int
    fecha_asignacion: Optional[datetime] = None

    class Config:
        from_attributes = True
