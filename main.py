from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables
from autos import router as autos_router
from ventas import router as ventas_router

app = FastAPI(
    title="API de Ventas de Autos",
    description="""
    API REST completa para la gestión de ventas de autos.
    
    ## Características
    
    * **Gestión de Autos**: CRUD completo para el inventario de autos
    * **Gestión de Ventas**: CRUD completo para las ventas realizadas
    * **Búsquedas Avanzadas**: Filtros por marca, modelo, comprador, fechas y precios
    * **Relaciones**: Consultas que incluyen información relacionada entre entidades
    
    ## Tecnologías
    
    * FastAPI
    * SQLModel
    * PostgreSQL
    * Pydantic
    """,
    version="1.0.0",
    contact={
        "name": "API de Ventas de Autos",
        "email": "support@example.com",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(autos_router)
app.include_router(ventas_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/", tags=["root"], summary="Endpoint raíz")
def read_root():
    return {
        "message": "Bienvenido a la API de Ventas de Autos",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "autos": "/autos",
            "ventas": "/ventas"
        }
    }


@app.get("/health", tags=["health"], summary="Health check")
def health_check():
    return {
        "status": "healthy",
        "service": "API de Ventas de Autos"
    }

