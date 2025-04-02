from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from modelspydantic import DetallePedido
from DB.conexion import Session
from models.modelsDB import DetallePedido as DBDetallePedido
from fastapi import APIRouter

routerDetallePedido = APIRouter()

@routerDetallePedido.post("/detalles-pedido", response_model=DetallePedido, tags=["Detalles de Pedido"])
def crear_detalle(detalle: DetallePedido):
    db = Session()
    try:
        nuevo_detalle = DBDetallePedido(**detalle.model_dump())
        db.add(nuevo_detalle)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Detalle creado", "detalle": detalle.model_dump()})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al crear detalle", "Exception": str(e)})
    finally:
        db.close()

@routerDetallePedido.get("/detalles-pedido", tags=["Detalles de Pedido"])
def obtener_detalles():
    db = Session()
    try:
        detalles = db.query(DBDetallePedido).all()
        return JSONResponse(content=jsonable_encoder(detalles))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener detalles", "Exception": str(e)})
    finally:
        db.close()

@routerDetallePedido.get("/detalles-pedido/{id}", tags=["Detalles de Pedido"])
def obtener_detalle(id: int):
    db = Session()
    try:
        detalle = db.query(DBDetallePedido).filter(DBDetallePedido.id_detalle == id).first()
        if not detalle:
            return JSONResponse(status_code=404, content={"message": "Detalle no encontrado"})
        return JSONResponse(content=jsonable_encoder(detalle))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener detalle", "Exception": str(e)})
    finally:
        db.close()

@routerDetallePedido.put("/detalles-pedido/{id}", response_model=DetallePedido, tags=["Detalles de Pedido"])
def actualizar_detalle(id: int, detalle: DetallePedido):
    db = Session()
    try:
        detalle_existente = db.query(DBDetallePedido).filter(DBDetallePedido.id_detalle == id).first()
        if not detalle_existente:
            return JSONResponse(status_code=404, content={"message": "Detalle no encontrado"})

        for key, value in detalle.model_dump().items():
            setattr(detalle_existente, key, value)

        db.commit()
        return JSONResponse(content={"message": "Detalle actualizado", "detalle": jsonable_encoder(detalle_existente)})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al actualizar detalle", "Exception": str(e)})
    finally:
        db.close()

@routerDetallePedido.delete("/detalles-pedido/{id}", tags=["Detalles de Pedido"])
def eliminar_detalle(id: int):
    db = Session()
    try:
        detalle = db.query(DBDetallePedido).filter(DBDetallePedido.id_detalle == id).first()
        if not detalle:
            return JSONResponse(status_code=404, content={"message": "Detalle no encontrado"})
        db.delete(detalle)
        db.commit()
        return JSONResponse(content={"message": "Detalle eliminado correctamente"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al eliminar detalle", "Exception": str(e)})
    finally:
        db.close()