from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from modelspydantic import HistorialAbastecimiento
from DB.conexion import Session
from models.modelsDB import HistorialAbastecimiento as DBHistorialAbastecimiento
from fastapi import APIRouter

routerHistorialAbastecimiento = APIRouter()

@routerHistorialAbastecimiento.post("/historial-abastecimiento", response_model=HistorialAbastecimiento, tags=["Historial Abastecimiento"])
def crear_abastecimiento(abastecimiento: HistorialAbastecimiento):
    db = Session()
    try:
        nuevo_abastecimiento = DBHistorialAbastecimiento(**abastecimiento.model_dump())
        db.add(nuevo_abastecimiento)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Abastecimiento registrado", "abastecimiento": abastecimiento.model_dump()})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al registrar abastecimiento", "Exception": str(e)})
    finally:
        db.close()

@routerHistorialAbastecimiento.get("/historial-abastecimiento", tags=["Historial Abastecimiento"])
def obtener_abastecimientos():
    db = Session()
    try:
        abastecimientos = db.query(DBHistorialAbastecimiento).all()
        return JSONResponse(content=jsonable_encoder(abastecimientos))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener abastecimientos", "Exception": str(e)})
    finally:
        db.close()

@routerHistorialAbastecimiento.get("/historial-abastecimiento/{id}", tags=["Historial Abastecimiento"])
def obtener_abastecimiento(id: int):
    db = Session()
    try:
        abastecimiento = db.query(DBHistorialAbastecimiento).filter(DBHistorialAbastecimiento.id_abastecimiento == id).first()
        if not abastecimiento:
            return JSONResponse(status_code=404, content={"message": "Abastecimiento no encontrado"})
        return JSONResponse(content=jsonable_encoder(abastecimiento))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener abastecimiento", "Exception": str(e)})
    finally:
        db.close()

@routerHistorialAbastecimiento.put("/historial-abastecimiento/{id}", response_model=HistorialAbastecimiento, tags=["Historial Abastecimiento"])
def actualizar_abastecimiento(id: int, abastecimiento: HistorialAbastecimiento):
    db = Session()
    try:
        abastecimiento_existente = db.query(DBHistorialAbastecimiento).filter(DBHistorialAbastecimiento.id_abastecimiento == id).first()
        if not abastecimiento_existente:
            return JSONResponse(status_code=404, content={"message": "Abastecimiento no encontrado"})

        for key, value in abastecimiento.model_dump().items():
            setattr(abastecimiento_existente, key, value)

        db.commit()
        return JSONResponse(content={"message": "Abastecimiento actualizado", "abastecimiento": jsonable_encoder(abastecimiento_existente)})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al actualizar abastecimiento", "Exception": str(e)})
    finally:
        db.close()

@routerHistorialAbastecimiento.delete("/historial-abastecimiento/{id}", tags=["Historial Abastecimiento"])
def eliminar_abastecimiento(id: int):
    db = Session()
    try:
        abastecimiento = db.query(DBHistorialAbastecimiento).filter(DBHistorialAbastecimiento.id_abastecimiento == id).first()
        if not abastecimiento:
            return JSONResponse(status_code=404, content={"message": "Abastecimiento no encontrado"})
        db.delete(abastecimiento)
        db.commit()
        return JSONResponse(content={"message": "Abastecimiento eliminado correctamente"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al eliminar abastecimiento", "Exception": str(e)})
    finally:
        db.close()