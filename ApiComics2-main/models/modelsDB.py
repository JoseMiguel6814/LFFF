from DB.conexion import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Categoria(Base):
    __tablename__ = 'categorias'
    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), unique=True, nullable=False)
    
    productos = relationship("Producto", back_populates="categoria")

class Cliente(Base):
    __tablename__ = 'clientes'
    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefono = Column(String(20))
    fecha_registro = Column(DateTime, server_default=func.now())
    
    direcciones = relationship("DireccionCliente", back_populates="cliente")
    pedidos = relationship("Pedido", back_populates="cliente")
    membresias = relationship("ClienteMembresia", back_populates="cliente")

class DireccionCliente(Base):
    __tablename__ = 'direccionesclientes'
    id_direccion = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'), nullable=False)
    direccion = Column(String(255), nullable=False)
    
    cliente = relationship("Cliente", back_populates="direcciones")

class EstadoPedido(Base):
    __tablename__ = 'estadospedidos'
    id_estado = Column(Integer, primary_key=True, autoincrement=True)
    nombre_estado = Column(Enum('pendiente', 'procesado', 'enviado', 'cancelado', name='estados_pedido'), unique=True, nullable=False)

class MarcaEditorial(Base):
    __tablename__ = 'marcaseditoriales'
    id_marca_editorial = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    
    productos = relationship("Producto", back_populates="marca_editorial")

class Membresia(Base):
    __tablename__ = 'membresias'
    id_membresia = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(Enum('regular', 'gold', 'platinum', name='tipos_membresia'), unique=True, nullable=False)
    
    clientes = relationship("ClienteMembresia", back_populates="membresia")

class Proveedor(Base):
    __tablename__ = 'proveedores'
    id_proveedor = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefono = Column(String(20))
    
    productos = relationship("Producto", back_populates="proveedor")
    abastecimientos = relationship("HistorialAbastecimiento", back_populates="proveedor")

class Producto(Base):
    __tablename__ = 'productos'
    id_producto = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    id_categoria = Column(Integer, ForeignKey('categorias.id_categoria'), nullable=False)
    stock_actual = Column(Integer)
    precio = Column(Float(10, 2), nullable=False)
    id_marca_editorial = Column(Integer, ForeignKey('marcaseditoriales.id_marca_editorial'))
    fecha_lanzamiento = Column(DateTime)
    imagen_url = Column(String(255))
    id_proveedor = Column(Integer, ForeignKey('proveedores.id_proveedor'))
    
    categoria = relationship("Categoria", back_populates="productos")
    marca_editorial = relationship("MarcaEditorial", back_populates="productos")
    proveedor = relationship("Proveedor", back_populates="productos")
    detalles_pedidos = relationship("DetallePedido", back_populates="producto")

class Pedido(Base):
    __tablename__ = 'pedidos'
    id_pedido = Column(Integer, primary_key=True, autoincrement=True)
    fecha_creacion = Column(DateTime, server_default=func.now())
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'), nullable=False)
    total = Column(Float(10, 2), nullable=False)
    id_estado = Column(Integer, ForeignKey('estadospedidos.id_estado'), nullable=False)
    id_direccion = Column(Integer, ForeignKey('direccionesclientes.id_direccion'), nullable=False)
    
    cliente = relationship("Cliente", back_populates="pedidos")
    estado = relationship("EstadoPedido")
    direccion = relationship("DireccionCliente")
    detalles = relationship("DetallePedido", back_populates="pedido")

class DetallePedido(Base):
    __tablename__ = 'detallespedidos'
    id_detalle = Column(Integer, primary_key=True, autoincrement=True)
    id_pedido = Column(Integer, ForeignKey('pedidos.id_pedido'), nullable=False)
    id_producto = Column(Integer, ForeignKey('productos.id_producto'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float(10, 2), nullable=False)
    
    pedido = relationship("Pedido", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_pedidos")

class HistorialAbastecimiento(Base):
    __tablename__ = 'historialabastecimiento'
    id_abastecimiento = Column(Integer, primary_key=True, autoincrement=True)
    id_proveedor = Column(Integer, ForeignKey('proveedores.id_proveedor'), nullable=False)
    id_producto = Column(Integer, ForeignKey('productos.id_producto'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    fecha_abastecimiento = Column(DateTime, server_default=func.now())
    
    proveedor = relationship("Proveedor", back_populates="abastecimientos")
    producto = relationship("Producto")

class ClienteMembresia(Base):
    __tablename__ = 'clientemembresia'
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'), primary_key=True)
    id_membresia = Column(Integer, ForeignKey('membresias.id_membresia'), primary_key=True)
    fecha_asignacion = Column(DateTime, server_default=func.now())
    
    cliente = relationship("Cliente", back_populates="membresias")
    membresia = relationship("Membresia", back_populates="clientes")