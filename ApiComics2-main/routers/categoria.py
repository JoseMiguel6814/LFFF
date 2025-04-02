from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from modelspydantic import Categoria
from DB.conexion import Session
from models.modelsDB import Categoria as DBCategoria
from fastapi import APIRouter

routerCategoria = APIRouter()

@routerCategoria.post("/categorias", response_model=Categoria, tags=["Categorías"])
def crear_categoria(categoria: Categoria):
    db = Session()
    try:
        nueva_categoria = DBCategoria(**categoria.model_dump())
        db.add(nueva_categoria)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Categoría creada", "categoria": categoria.model_dump()})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al crear categoría", "Exception": str(e)})
    finally:
        db.close()

@routerCategoria.get("/categorias", tags=["Categorías"])
def obtener_categorias():
    db = Session()
    try:
        categorias = db.query(DBCategoria).all()
        return JSONResponse(content=jsonable_encoder(categorias))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener categorías", "Exception": str(e)})
    finally:
        db.close()

@routerCategoria.get("/categorias/{id}", tags=["Categorías"])
def obtener_categoria(id: int):
    db = Session()
    try:
        categoria = db.query(DBCategoria).filter(DBCategoria.id_categoria == id).first()
        if not categoria:
            return JSONResponse(status_code=404, content={"message": "Categoría no encontrada"})
        return JSONResponse(content=jsonable_encoder(categoria))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener categoría", "Exception": str(e)})
    finally:
        db.close()

@routerCategoria.put("/categorias/{id}", response_model=Categoria, tags=["Categorías"])
def actualizar_categoria(id: int, categoria: Categoria):
    db = Session()
    try:
        categoria_existente = db.query(DBCategoria).filter(DBCategoria.id_categoria == id).first()
        if not categoria_existente:
            return JSONResponse(status_code=404, content={"message": "Categoría no encontrada"})

        for key, value in categoria.model_dump().items():
            setattr(categoria_existente, key, value)

        db.commit()
        return JSONResponse(content={"message": "Categoría actualizada", "categoria": jsonable_encoder(categoria_existente)})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al actualizar categoría", "Exception": str(e)})
    finally:
        db.close()

@routerCategoria.delete("/categorias/{id}", tags=["Categorías"])
def eliminar_categoria(id: int):
    db = Session()
    try:
        categoria = db.query(DBCategoria).filter(DBCategoria.id_categoria == id).first()
        if not categoria:
            return JSONResponse(status_code=404, content={"message": "Categoría no encontrada"})
        db.delete(categoria)
        db.commit()
        return JSONResponse(content={"message": "Categoría eliminada correctamente"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al eliminar categoría", "Exception": str(e)})
    finally:
        db.close()