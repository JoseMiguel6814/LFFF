from fastapi import FastAPI
from DB.conexion import engine, Base

from routers.categoria import routerCategoria
from routers.cliente_membresia import routerClienteMembresia
from routers.cliente import routerCliente
from routers.detalle_pedido import routerDetallePedido
from routers.direccion_cliente import routerDireccionCliente
from routers.estado_pedido import routerEstadoPedido
from routers.historial_abastecimiento import routerHistorialAbastecimiento
from routers.marca_editorial import routerMarcaEditorial
from routers.membresia import routerMembresia
from routers.pedido import routerPedido
from routers.proveedor import routerProveedor
from routers.producto import routerProducto

app = FastAPI(
    title="API Sistema de Gestión"
)

Base.metadata.create_all(bind=engine)

@app.get("/", tags=["Inicio"])
def home():
    return {"mensaje": "Bienvenido a la API de gestión"}

app.include_router(routerCategoria)
app.include_router(routerClienteMembresia)
app.include_router(routerCliente)
app.include_router(routerDetallePedido)
app.include_router(routerDireccionCliente)
app.include_router(routerEstadoPedido)
app.include_router(routerHistorialAbastecimiento)
app.include_router(routerMarcaEditorial)
app.include_router(routerMembresia)
app.include_router(routerPedido)
app.include_router(routerProveedor)
app.include_router(routerProducto)