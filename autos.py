from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from database import get_session
from repository import AutoRepository
from models import (
    Auto, AutoCreate, AutoUpdate, AutoResponse,
    AutoResponseWithVentas, VentaResponseSimple
)

router = APIRouter(prefix="/autos", tags=["autos"])


def get_auto_repository(session: Session = Depends(get_session)) -> AutoRepository:
    return AutoRepository(session)


@router.post("", response_model=AutoResponse, status_code=status.HTTP_201_CREATED, summary="Crear nuevo auto")
def create_auto(auto: AutoCreate, repo: AutoRepository = Depends(get_auto_repository)) -> AutoResponse:
    existing_auto = repo.get_by_chasis(auto.numero_chasis)
    if existing_auto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un auto con el número de chasis: {auto.numero_chasis}"
        )
    
    db_auto = repo.create(auto)
    return AutoResponse.model_validate(db_auto)


@router.get("", response_model=List[AutoResponse], summary="Listar autos")
def get_autos(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    marca: Optional[str] = Query(None, description="Filtrar por marca (búsqueda parcial)"),
    modelo: Optional[str] = Query(None, description="Filtrar por modelo (búsqueda parcial)"),
    repo: AutoRepository = Depends(get_auto_repository)
) -> List[AutoResponse]:
    if marca or modelo:
        autos = repo.search_by_marca_modelo(marca=marca, modelo=modelo, skip=skip, limit=limit)
    else:
        autos = repo.get_all(skip=skip, limit=limit)
    
    return [AutoResponse.model_validate(auto) for auto in autos]


@router.get("/{auto_id}", response_model=AutoResponse, summary="Obtener auto por ID")
def get_auto(auto_id: int, repo: AutoRepository = Depends(get_auto_repository)) -> AutoResponse:
    auto = repo.get_by_id(auto_id)
    if not auto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Auto con ID {auto_id} no encontrado"
        )
    return AutoResponse.model_validate(auto)


@router.put("/{auto_id}", response_model=AutoResponse, summary="Actualizar auto")
def update_auto(auto_id: int, auto_update: AutoUpdate, repo: AutoRepository = Depends(get_auto_repository)) -> AutoResponse:
    if auto_update.numero_chasis:
        existing_auto = repo.get_by_chasis(auto_update.numero_chasis)
        if existing_auto and existing_auto.id != auto_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un auto con el número de chasis: {auto_update.numero_chasis}"
            )
    
    auto = repo.update(auto_id, auto_update)
    if not auto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Auto con ID {auto_id} no encontrado"
        )
    return AutoResponse.model_validate(auto)


@router.delete("/{auto_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar auto")
def delete_auto(auto_id: int, repo: AutoRepository = Depends(get_auto_repository)):
    success = repo.delete(auto_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Auto con ID {auto_id} no encontrado"
        )


@router.get("/chasis/{numero_chasis}", response_model=AutoResponse, summary="Buscar auto por número de chasis")
def get_auto_by_chasis(numero_chasis: str, repo: AutoRepository = Depends(get_auto_repository)) -> AutoResponse:
    auto = repo.get_by_chasis(numero_chasis)
    if not auto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Auto con número de chasis {numero_chasis} no encontrado"
        )
    return AutoResponse.model_validate(auto)


@router.get("/{auto_id}/with-ventas", response_model=AutoResponseWithVentas, summary="Obtener auto con sus ventas")
def get_auto_with_ventas(
    auto_id: int,
    repo: AutoRepository = Depends(get_auto_repository),
    session: Session = Depends(get_session)
) -> AutoResponseWithVentas:
    from repository import VentaRepository
    
    auto = repo.get_by_id(auto_id)
    if not auto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Auto con ID {auto_id} no encontrado"
        )
    
    venta_repo = VentaRepository(session)
    ventas = venta_repo.get_by_auto_id(auto_id)
    
    auto_response = AutoResponse.model_validate(auto)
    ventas_response = [VentaResponseSimple.model_validate(venta) for venta in ventas]
    
    return AutoResponseWithVentas(
        **auto_response.model_dump(),
        ventas=ventas_response
    )

