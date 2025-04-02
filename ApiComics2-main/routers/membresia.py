from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from modelspydantic import Membresia
from DB.conexion import Session
from models.modelsDB import Membresia as DBMembresia
from fastapi import APIRouter

routerMembresia = APIRouter()

@routerMembresia.post("/membresias", response_model=Membresia, tags=["Membresías"])
def crear_membresia(membresia: Membresia):
    db = Session()
    try:
        nueva_membresia = DBMembresia(**membresia.model_dump())
        db.add(nueva_membresia)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Membresía creada", "membresia": membresia.model_dump()})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al crear membresía", "Exception": str(e)})
    finally:
        db.close()

@routerMembresia.get("/membresias", tags=["Membresías"])
def obtener_membresias():
    db = Session()
    try:
        membresias = db.query(DBMembresia).all()
        return JSONResponse(content=jsonable_encoder(membresias))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener membresías", "Exception": str(e)})
    finally:
        db.close()

@routerMembresia.get("/membresias/{id}", tags=["Membresías"])
def obtener_membresia(id: int):
    db = Session()
    try:
        membresia = db.query(DBMembresia).filter(DBMembresia.id_membresia == id).first()
        if not membresia:
            return JSONResponse(status_code=404, content={"message": "Membresía no encontrada"})
        return JSONResponse(content=jsonable_encoder(membresia))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener membresía", "Exception": str(e)})
    finally:
        db.close()

@routerMembresia.put("/membresias/{id}", response_model=Membresia, tags=["Membresías"])
def actualizar_membresia(id: int, membresia: Membresia):
    db = Session()
    try:
        membresia_existente = db.query(DBMembresia).filter(DBMembresia.id_membresia == id).first()
        if not membresia_existente:
            return JSONResponse(status_code=404, content={"message": "Membresía no encontrada"})

        for key, value in membresia.model_dump().items():
            setattr(membresia_existente, key, value)

        db.commit()
        return JSONResponse(content={"message": "Membresía actualizada", "membresia": jsonable_encoder(membresia_existente)})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al actualizar membresía", "Exception": str(e)})
    finally:
        db.close()

@routerMembresia.delete("/membresias/{id}", tags=["Membresías"])
def eliminar_membresia(id: int):
    db = Session()
    try:
        membresia = db.query(DBMembresia).filter(DBMembresia.id_membresia == id).first()
        if not membresia:
            return JSONResponse(status_code=404, content={"message": "Membresía no encontrada"})
        db.delete(membresia)
        db.commit()
        return JSONResponse(content={"message": "Membresía eliminada correctamente"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al eliminar membresía", "Exception": str(e)})
    finally:
        db.close()