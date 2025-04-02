from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from modelspydantic import Pedido
from DB.conexion import Session
from models.modelsDB import Pedido as DBPedido
from fastapi import APIRouter

routerPedido = APIRouter()

@routerPedido.post("/pedidos", response_model=Pedido, tags=["Pedidos"])
def crear_pedido(pedido: Pedido):
    db = Session()
    try:
        nuevo_pedido = DBPedido(**pedido.model_dump())
        db.add(nuevo_pedido)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Pedido creado", "pedido": pedido.model_dump()})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al crear pedido", "Exception": str(e)})
    finally:
        db.close()

@routerPedido.get("/pedidos", tags=["Pedidos"])
def obtener_pedidos():
    db = Session()
    try:
        pedidos = db.query(DBPedido).all()
        return JSONResponse(content=jsonable_encoder(pedidos))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener pedidos", "Exception": str(e)})
    finally:
        db.close()

@routerPedido.get("/pedidos/{id}", tags=["Pedidos"])
def obtener_pedido(id: int):
    db = Session()
    try:
        pedido = db.query(DBPedido).filter(DBPedido.id_pedido == id).first()
        if not pedido:
            return JSONResponse(status_code=404, content={"message": "Pedido no encontrado"})
        return JSONResponse(content=jsonable_encoder(pedido))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener pedido", "Exception": str(e)})
    finally:
        db.close()

@routerPedido.put("/pedidos/{id}", response_model=Pedido, tags=["Pedidos"])
def actualizar_pedido(id: int, pedido: Pedido):
    db = Session()
    try:
        pedido_existente = db.query(DBPedido).filter(DBPedido.id_pedido == id).first()
        if not pedido_existente:
            return JSONResponse(status_code=404, content={"message": "Pedido no encontrado"})

        for key, value in pedido.model_dump().items():
            setattr(pedido_existente, key, value)

        db.commit()
        return JSONResponse(content={"message": "Pedido actualizado", "pedido": jsonable_encoder(pedido_existente)})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al actualizar pedido", "Exception": str(e)})
    finally:
        db.close()

@routerPedido.delete("/pedidos/{id}", tags=["Pedidos"])
def eliminar_pedido(id: int):
    db = Session()
    try:
        pedido = db.query(DBPedido).filter(DBPedido.id_pedido == id).first()
        if not pedido:
            return JSONResponse(status_code=404, content={"message": "Pedido no encontrado"})
        db.delete(pedido)
        db.commit()
        return JSONResponse(content={"message": "Pedido eliminado correctamente"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al eliminar pedido", "Exception": str(e)})
    finally:
        db.close()