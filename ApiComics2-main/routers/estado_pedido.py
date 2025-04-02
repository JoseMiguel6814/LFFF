from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from modelspydantic import EstadoPedido
from DB.conexion import Session
from models.modelsDB import EstadoPedido as DBEstadoPedido
from fastapi import APIRouter

routerEstadoPedido = APIRouter()

@routerEstadoPedido.post("/estados-pedido", response_model=EstadoPedido, tags=["Estados de Pedido"])
def crear_estado_pedido(estado: EstadoPedido):
    db = Session()
    try:
        nuevo_estado = DBEstadoPedido(**estado.model_dump())
        db.add(nuevo_estado)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Estado creado", "estado": estado.model_dump()})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al crear estado", "Exception": str(e)})
    finally:
        db.close()

@routerEstadoPedido.get("/estados-pedido", tags=["Estados de Pedido"])
def obtener_estados_pedido():
    db = Session()
    try:
        estados = db.query(DBEstadoPedido).all()
        return JSONResponse(content=jsonable_encoder(estados))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener estados", "Exception": str(e)})
    finally:
        db.close()

@routerEstadoPedido.get("/estados-pedido/{id}", tags=["Estados de Pedido"])
def obtener_estado_pedido(id: int):
    db = Session()
    try:
        estado = db.query(DBEstadoPedido).filter(DBEstadoPedido.id_estado == id).first()
        if not estado:
            return JSONResponse(status_code=404, content={"message": "Estado no encontrado"})
        return JSONResponse(content=jsonable_encoder(estado))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener estado", "Exception": str(e)})
    finally:
        db.close()

@routerEstadoPedido.put("/estados-pedido/{id}", response_model=EstadoPedido, tags=["Estados de Pedido"])
def actualizar_estado_pedido(id: int, estado: EstadoPedido):
    db = Session()
    try:
        estado_existente = db.query(DBEstadoPedido).filter(DBEstadoPedido.id_estado == id).first()
        if not estado_existente:
            return JSONResponse(status_code=404, content={"message": "Estado no encontrado"})

        for key, value in estado.model_dump().items():
            setattr(estado_existente, key, value)

        db.commit()
        return JSONResponse(content={"message": "Estado actualizado", "estado": jsonable_encoder(estado_existente)})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al actualizar estado", "Exception": str(e)})
    finally:
        db.close()

@routerEstadoPedido.delete("/estados-pedido/{id}", tags=["Estados de Pedido"])
def eliminar_estado_pedido(id: int):
    db = Session()
    try:
        estado = db.query(DBEstadoPedido).filter(DBEstadoPedido.id_estado == id).first()
        if not estado:
            return JSONResponse(status_code=404, content={"message": "Estado no encontrado"})
        db.delete(estado)
        db.commit()
        return JSONResponse(content={"message": "Estado eliminado correctamente"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al eliminar estado", "Exception": str(e)})
    finally:
        db.close()