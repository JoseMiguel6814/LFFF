from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from modelspydantic import MarcaEditorial
from DB.conexion import Session
from models.modelsDB import MarcaEditorial as DBMarcaEditorial
from fastapi import APIRouter

routerMarcaEditorial = APIRouter()

@routerMarcaEditorial.post("/marcas-editoriales", response_model=MarcaEditorial, tags=["Marcas/Editoriales"])
def crear_marca_editorial(marca_editorial: MarcaEditorial):
    db = Session()
    try:
        nueva_marca = DBMarcaEditorial(**marca_editorial.model_dump())
        db.add(nueva_marca)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Marca/Editorial creada", "marca_editorial": marca_editorial.model_dump()})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al crear marca/editorial", "Exception": str(e)})
    finally:
        db.close()

@routerMarcaEditorial.get("/marcas-editoriales", tags=["Marcas/Editoriales"])
def obtener_marcas_editoriales():
    db = Session()
    try:
        marcas = db.query(DBMarcaEditorial).all()
        return JSONResponse(content=jsonable_encoder(marcas))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener marcas/editoriales", "Exception": str(e)})
    finally:
        db.close()

@routerMarcaEditorial.get("/marcas-editoriales/{id}", tags=["Marcas/Editoriales"])
def obtener_marca_editorial(id: int):
    db = Session()
    try:
        marca = db.query(DBMarcaEditorial).filter(DBMarcaEditorial.id_marca_editorial == id).first()
        if not marca:
            return JSONResponse(status_code=404, content={"message": "Marca/Editorial no encontrada"})
        return JSONResponse(content=jsonable_encoder(marca))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener marca/editorial", "Exception": str(e)})
    finally:
        db.close()

@routerMarcaEditorial.put("/marcas-editoriales/{id}", response_model=MarcaEditorial, tags=["Marcas/Editoriales"])
def actualizar_marca_editorial(id: int, marca_editorial: MarcaEditorial):
    db = Session()
    try:
        marca_existente = db.query(DBMarcaEditorial).filter(DBMarcaEditorial.id_marca_editorial == id).first()
        if not marca_existente:
            return JSONResponse(status_code=404, content={"message": "Marca/Editorial no encontrada"})

        for key, value in marca_editorial.model_dump().items():
            setattr(marca_existente, key, value)

        db.commit()
        return JSONResponse(content={"message": "Marca/Editorial actualizada", "marca_editorial": jsonable_encoder(marca_existente)})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al actualizar marca/editorial", "Exception": str(e)})
    finally:
        db.close()

@routerMarcaEditorial.delete("/marcas-editoriales/{id}", tags=["Marcas/Editoriales"])
def eliminar_marca_editorial(id: int):
    db = Session()
    try:
        marca = db.query(DBMarcaEditorial).filter(DBMarcaEditorial.id_marca_editorial == id).first()
        if not marca:
            return JSONResponse(status_code=404, content={"message": "Marca/Editorial no encontrada"})
        db.delete(marca)
        db.commit()
        return JSONResponse(content={"message": "Marca/Editorial eliminada correctamente"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al eliminar marca/editorial", "Exception": str(e)})
    finally:
        db.close()