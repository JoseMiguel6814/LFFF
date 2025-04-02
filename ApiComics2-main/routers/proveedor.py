from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from modelspydantic import Proveedor
from DB.conexion import Session
from models.modelsDB import Proveedor as DBProveedor
from fastapi import APIRouter

routerProveedor = APIRouter()

@routerProveedor.post("/proveedores", response_model=Proveedor, tags=["Proveedores"])
def crear_proveedor(proveedor: Proveedor):
    db = Session()
    try:
        nuevo_proveedor = DBProveedor(**proveedor.model_dump())
        db.add(nuevo_proveedor)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Proveedor creado", "proveedor": proveedor.model_dump()})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al crear proveedor", "Exception": str(e)})
    finally:
        db.close()

@routerProveedor.get("/proveedores", tags=["Proveedores"])
def obtener_proveedores():
    db = Session()
    try:
        proveedores = db.query(DBProveedor).all()
        return JSONResponse(content=jsonable_encoder(proveedores))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener proveedores", "Exception": str(e)})
    finally:
        db.close()

@routerProveedor.get("/proveedores/{id}", tags=["Proveedores"])
def obtener_proveedor(id: int):
    db = Session()
    try:
        proveedor = db.query(DBProveedor).filter(DBProveedor.id_proveedor == id).first()
        if not proveedor:
            return JSONResponse(status_code=404, content={"message": "Proveedor no encontrado"})
        return JSONResponse(content=jsonable_encoder(proveedor))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener proveedor", "Exception": str(e)})
    finally:
        db.close()

@routerProveedor.put("/proveedores/{id}", response_model=Proveedor, tags=["Proveedores"])
def actualizar_proveedor(id: int, proveedor: Proveedor):
    db = Session()
    try:
        proveedor_existente = db.query(DBProveedor).filter(DBProveedor.id_proveedor == id).first()
        if not proveedor_existente:
            return JSONResponse(status_code=404, content={"message": "Proveedor no encontrado"})

        for key, value in proveedor.model_dump().items():
            setattr(proveedor_existente, key, value)

        db.commit()
        return JSONResponse(content={"message": "Proveedor actualizado", "proveedor": jsonable_encoder(proveedor_existente)})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al actualizar proveedor", "Exception": str(e)})
    finally:
        db.close()

@routerProveedor.delete("/proveedores/{id}", tags=["Proveedores"])
def eliminar_proveedor(id: int):
    db = Session()
    try:
        proveedor = db.query(DBProveedor).filter(DBProveedor.id_proveedor == id).first()
        if not proveedor:
            return JSONResponse(status_code=404, content={"message": "Proveedor no encontrado"})
        db.delete(proveedor)
        db.commit()
        return JSONResponse(content={"message": "Proveedor eliminado correctamente"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al eliminar proveedor", "Exception": str(e)})
    finally:
        db.close()