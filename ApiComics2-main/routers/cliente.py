from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from modelspydantic import Cliente
from DB.conexion import Session
from models.modelsDB import Cliente as DBCliente
from fastapi import APIRouter

routerCliente = APIRouter()

@routerCliente.post("/clientes", response_model=Cliente, tags=["Clientes"])
def crear_cliente(cliente: Cliente):
    db = Session()
    try:
        nuevo_cliente = DBCliente(**cliente.model_dump())
        db.add(nuevo_cliente)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Cliente creado", "cliente": cliente.model_dump()})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al crear cliente", "Exception": str(e)})
    finally:
        db.close()

@routerCliente.get("/clientes", tags=["Clientes"])
def obtener_clientes():
    db = Session()
    try:
        clientes = db.query(DBCliente).all()
        return JSONResponse(content=jsonable_encoder(clientes))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener clientes", "Exception": str(e)})
    finally:
        db.close()

@routerCliente.get("/clientes/{id}", tags=["Clientes"])
def obtener_cliente(id: int):
    db = Session()
    try:
        cliente = db.query(DBCliente).filter(DBCliente.id_cliente == id).first()
        if not cliente:
            return JSONResponse(status_code=404, content={"message": "Cliente no encontrado"})
        return JSONResponse(content=jsonable_encoder(cliente))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener cliente", "Exception": str(e)})
    finally:
        db.close()

@routerCliente.put("/clientes/{id}", response_model=Cliente, tags=["Clientes"])
def actualizar_cliente(id: int, cliente: Cliente):
    db = Session()
    try:
        cliente_existente = db.query(DBCliente).filter(DBCliente.id_cliente == id).first()
        if not cliente_existente:
            return JSONResponse(status_code=404, content={"message": "Cliente no encontrado"})

        for key, value in cliente.model_dump().items():
            setattr(cliente_existente, key, value)

        db.commit()
        return JSONResponse(content={"message": "Cliente actualizado", "cliente": jsonable_encoder(cliente_existente)})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al actualizar cliente", "Exception": str(e)})
    finally:
        db.close()

@routerCliente.delete("/clientes/{id}", tags=["Clientes"])
def eliminar_cliente(id: int):
    db = Session()
    try:
        cliente = db.query(DBCliente).filter(DBCliente.id_cliente == id).first()
        if not cliente:
            return JSONResponse(status_code=404, content={"message": "Cliente no encontrado"})
        db.delete(cliente)
        db.commit()
        return JSONResponse(content={"message": "Cliente eliminado correctamente"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al eliminar cliente", "Exception": str(e)})
    finally:
        db.close()