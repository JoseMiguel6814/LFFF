from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from modelspydantic import DireccionCliente
from DB.conexion import Session
from models.modelsDB import DireccionCliente as DBDireccionCliente
from fastapi import APIRouter

routerDireccionCliente = APIRouter()

@routerDireccionCliente.post("/direcciones-clientes", response_model=DireccionCliente, tags=["Direcciones de Clientes"])
def crear_direccion_cliente(direccion: DireccionCliente):
    db = Session()
    try:
        nueva_direccion = DBDireccionCliente(**direccion.model_dump())
        db.add(nueva_direccion)
        db.commit()
        return JSONResponse(
            status_code=201,
            content={
                "message": "Dirección creada",
                "direccion": direccion.model_dump()
            }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error al crear dirección",
                "Exception": str(e)
            }
        )
    finally:
        db.close()

@routerDireccionCliente.get("/direcciones-clientes", tags=["Direcciones de Clientes"])
def obtener_direcciones_clientes():
    db = Session()
    try:
        direcciones = db.query(DBDireccionCliente).all()
        return JSONResponse(content=jsonable_encoder(direcciones))
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error al obtener direcciones",
                "Exception": str(e)
            }
        )
    finally:
        db.close()

@routerDireccionCliente.get("/direcciones-clientes/{id}", tags=["Direcciones de Clientes"])
def obtener_direccion_cliente(id: int):
    db = Session()
    try:
        direccion = db.query(DBDireccionCliente).filter(DBDireccionCliente.id_direccion == id).first()
        if not direccion:
            return JSONResponse(
                status_code=404,
                content={"message": "Dirección no encontrada"}
            )
        return JSONResponse(content=jsonable_encoder(direccion))
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error al obtener dirección",
                "Exception": str(e)
            }
        )
    finally:
        db.close()

@routerDireccionCliente.put("/direcciones-clientes/{id}", response_model=DireccionCliente, tags=["Direcciones de Clientes"])
def actualizar_direccion_cliente(id: int, direccion: DireccionCliente):
    db = Session()
    try:
        direccion_existente = db.query(DBDireccionCliente).filter(DBDireccionCliente.id_direccion == id).first()
        if not direccion_existente:
            return JSONResponse(
                status_code=404,
                content={"message": "Dirección no encontrada"}
            )

        for key, value in direccion.model_dump().items():
            setattr(direccion_existente, key, value)

        db.commit()
        return JSONResponse(
            content={
                "message": "Dirección actualizada",
                "direccion": jsonable_encoder(direccion_existente)
            }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error al actualizar dirección",
                "Exception": str(e)
            }
        )
    finally:
        db.close()

@routerDireccionCliente.delete("/direcciones-clientes/{id}", tags=["Direcciones de Clientes"])
def eliminar_direccion_cliente(id: int):
    db = Session()
    try:
        direccion = db.query(DBDireccionCliente).filter(DBDireccionCliente.id_direccion == id).first()
        if not direccion:
            return JSONResponse(
                status_code=404,
                content={"message": "Dirección no encontrada"}
            )
        db.delete(direccion)
        db.commit()
        return JSONResponse(
            content={"message": "Dirección eliminada correctamente"}
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error al eliminar dirección",
                "Exception": str(e)
            }
        )
    finally:
        db.close()