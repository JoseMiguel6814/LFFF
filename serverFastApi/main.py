from fastapi import FastAPI, HTTPException
from DB.conexion import engine,Base
from routers.usuarios import routerUsuario
from routers.auth import routerAuth

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Mi primer API",
    description="Ivan Isay Guerra",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)