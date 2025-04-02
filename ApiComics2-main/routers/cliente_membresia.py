from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from modelspydantic import ClienteMembresia
from DB.conexion import Session
from models.modelsDB import ClienteMembresia as DBClienteMembresia
from fastapi import APIRouter

routerClienteMembresia = APIRouter()

@routerClienteMembresia.post("/cliente-membresia", response_model=ClienteMembresia, tags=["Cliente-Membresía"])
def asignar_membresia(cliente_membresia: ClienteMembresia):
    db = Session()
    try:
        nueva_asignacion = DBClienteMembresia(**cliente_membresia.model_dump())
        db.add(nueva_asignacion)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Membresía asignada", "asignacion": cliente_membresia.model_dump()})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al asignar membresía", "Exception": str(e)})
    finally:
        db.close()

@routerClienteMembresia.get("/cliente-membresia", tags=["Cliente-Membresía"])
def obtener_asignaciones():
    db = Session()
    try:
        asignaciones = db.query(DBClienteMembresia).all()
        return JSONResponse(content=jsonable_encoder(asignaciones))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener asignaciones", "Exception": str(e)})
    finally:
        db.close()

@routerClienteMembresia.get("/cliente-membresia/{cliente_id}", tags=["Cliente-Membresía"])
def obtener_asignacion(cliente_id: int):
    db = Session()
    try:
        asignacion = db.query(DBClienteMembresia).filter(DBClienteMembresia.id_cliente == cliente_id).first()
        if not asignacion:
            return JSONResponse(status_code=404, content={"message": "Asignación no encontrada"})
        return JSONResponse(content=jsonable_encoder(asignacion))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener asignación", "Exception": str(e)})
    finally:
        db.close()

@routerClienteMembresia.put("/cliente-membresia/{cliente_id}", response_model=ClienteMembresia, tags=["Cliente-Membresía"])
def actualizar_asignacion(cliente_id: int, cliente_membresia: ClienteMembresia):
    db = Session()
    try:
        asignacion_existente = db.query(DBClienteMembresia).filter(DBClienteMembresia.id_cliente == cliente_id).first()
        if not asignacion_existente:
            return JSONResponse(status_code=404, content={"message": "Asignación no encontrada"})

        for key, value in cliente_membresia.model_dump().items():
            setattr(asignacion_existente, key, value)

        db.commit()
        return JSONResponse(content={"message": "Asignación actualizada", "asignacion": jsonable_encoder(asignacion_existente)})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al actualizar asignación", "Exception": str(e)})
    finally:
        db.close()

@routerClienteMembresia.delete("/cliente-membresia/{cliente_id}", tags=["Cliente-Membresía"])
def eliminar_asignacion(cliente_id: int):
    db = Session()
    try:
        asignacion = db.query(DBClienteMembresia).filter(DBClienteMembresia.id_cliente == cliente_id).first()
        if not asignacion:
            return JSONResponse(status_code=404, content={"message": "Asignación no encontrada"})
        db.delete(asignacion)
        db.commit()
        return JSONResponse(content={"message": "Asignación eliminada correctamente"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al eliminar asignación", "Exception": str(e)})
    finally:
        db.close()