from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from modelspydantic import Producto
from DB.conexion import Session
from models.modelsDB import Producto as DBProducto
from fastapi import APIRouter

routerProducto = APIRouter()

@routerProducto.post("/productos", response_model=Producto, tags=["Productos"])
def crear_producto(producto: Producto):
    db = Session()
    try:
        nuevo_producto = DBProducto(**producto.model_dump())
        db.add(nuevo_producto)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Producto creado", "producto": producto.model_dump()})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al crear producto", "Exception": str(e)})
    finally:
        db.close()

@routerProducto.get("/productos", tags=["Productos"])
def obtener_productos():
    db = Session()
    try:
        productos = db.query(DBProducto).all()
        return JSONResponse(content=jsonable_encoder(productos))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener productos", "Exception": str(e)})
    finally:
        db.close()

@routerProducto.get("/productos/{id}", tags=["Productos"])
def obtener_producto(id: int):
    db = Session()
    try:
        producto = db.query(DBProducto).filter(DBProducto.id_producto == id).first()
        if not producto:
            return JSONResponse(status_code=404, content={"message": "Producto no encontrado"})
        return JSONResponse(content=jsonable_encoder(producto))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener producto", "Exception": str(e)})
    finally:
        db.close()

@routerProducto.put("/productos/{id}", response_model=Producto, tags=["Productos"])
def actualizar_producto(id: int, producto: Producto):
    db = Session()
    try:
        producto_existente = db.query(DBProducto).filter(DBProducto.id_producto == id).first()
        if not producto_existente:
            return JSONResponse(status_code=404, content={"message": "Producto no encontrado"})

        for key, value in producto.model_dump().items():
            setattr(producto_existente, key, value)

        db.commit()
        return JSONResponse(content={"message": "Producto actualizado", "producto": jsonable_encoder(producto_existente)})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al actualizar producto", "Exception": str(e)})
    finally:
        db.close()

@routerProducto.delete("/productos/{id}", tags=["Productos"])
def eliminar_producto(id: int):
    db = Session()
    try:
        producto = db.query(DBProducto).filter(DBProducto.id_producto == id).first()
        if not producto:
            return JSONResponse(status_code=404, content={"message": "Producto no encontrado"})
        db.delete(producto)
        db.commit()
        return JSONResponse(content={"message": "Producto eliminado correctamente"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al eliminar producto", "Exception": str(e)})
    finally:
        db.close()