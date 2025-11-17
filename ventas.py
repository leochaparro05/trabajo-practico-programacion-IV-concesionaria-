from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from database import get_session
from repository import VentaRepository, AutoRepository
from models import (
    Venta, VentaCreate, VentaUpdate, VentaResponse,
    VentaResponseWithAuto, AutoResponse
)

router = APIRouter(prefix="/ventas", tags=["ventas"])


def get_venta_repository(session: Session = Depends(get_session)) -> VentaRepository:
    return VentaRepository(session)


def get_auto_repository(session: Session = Depends(get_session)) -> AutoRepository:
    return AutoRepository(session)


@router.post("", response_model=VentaResponse, status_code=status.HTTP_201_CREATED, summary="Crear nueva venta")
def create_venta(
    venta: VentaCreate,
    venta_repo: VentaRepository = Depends(get_venta_repository),
    auto_repo: AutoRepository = Depends(get_auto_repository)
) -> VentaResponse:
    auto = auto_repo.get_by_id(venta.auto_id)
    if not auto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Auto con ID {venta.auto_id} no encontrado"
        )
    
    db_venta = venta_repo.create(venta)
    return VentaResponse.model_validate(db_venta)


@router.get("", response_model=List[VentaResponse], summary="Listar ventas")
def get_ventas(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    fecha_inicio: Optional[str] = Query(None, description="Fecha de inicio (ISO format)"),
    fecha_fin: Optional[str] = Query(None, description="Fecha de fin (ISO format)"),
    precio_min: Optional[float] = Query(None, ge=0, description="Precio mínimo"),
    precio_max: Optional[float] = Query(None, ge=0, description="Precio máximo"),
    venta_repo: VentaRepository = Depends(get_venta_repository)
) -> List[VentaResponse]:
    if fecha_inicio or fecha_fin:
        ventas = venta_repo.filter_by_fecha_range(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            skip=skip,
            limit=limit
        )
    elif precio_min is not None or precio_max is not None:
        ventas = venta_repo.filter_by_precio_range(
            precio_min=precio_min,
            precio_max=precio_max,
            skip=skip,
            limit=limit
        )
    else:
        ventas = venta_repo.get_all(skip=skip, limit=limit)
    
    return [VentaResponse.model_validate(venta) for venta in ventas]


@router.get("/{venta_id}", response_model=VentaResponse, summary="Obtener venta por ID")
def get_venta(venta_id: int, venta_repo: VentaRepository = Depends(get_venta_repository)) -> VentaResponse:
    venta = venta_repo.get_by_id(venta_id)
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Venta con ID {venta_id} no encontrada"
        )
    return VentaResponse.model_validate(venta)


@router.put("/{venta_id}", response_model=VentaResponse, summary="Actualizar venta")
def update_venta(
    venta_id: int,
    venta_update: VentaUpdate,
    venta_repo: VentaRepository = Depends(get_venta_repository),
    auto_repo: AutoRepository = Depends(get_auto_repository)
) -> VentaResponse:
    if venta_update.auto_id is not None:
        auto = auto_repo.get_by_id(venta_update.auto_id)
        if not auto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Auto con ID {venta_update.auto_id} no encontrado"
            )
    
    venta = venta_repo.update(venta_id, venta_update)
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Venta con ID {venta_id} no encontrada"
        )
    return VentaResponse.model_validate(venta)


@router.delete("/{venta_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar venta")
def delete_venta(venta_id: int, venta_repo: VentaRepository = Depends(get_venta_repository)):
    success = venta_repo.delete(venta_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Venta con ID {venta_id} no encontrada"
        )


@router.get("/auto/{auto_id}", response_model=List[VentaResponse], summary="Obtener ventas de un auto")
def get_ventas_by_auto(
    auto_id: int,
    venta_repo: VentaRepository = Depends(get_venta_repository),
    auto_repo: AutoRepository = Depends(get_auto_repository)
) -> List[VentaResponse]:
    auto = auto_repo.get_by_id(auto_id)
    if not auto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Auto con ID {auto_id} no encontrado"
        )
    
    ventas = venta_repo.get_by_auto_id(auto_id)
    return [VentaResponse.model_validate(venta) for venta in ventas]


@router.get("/comprador/{nombre}", response_model=List[VentaResponse], summary="Buscar ventas por comprador")
def get_ventas_by_comprador(nombre: str, venta_repo: VentaRepository = Depends(get_venta_repository)) -> List[VentaResponse]:
    ventas = venta_repo.get_by_comprador(nombre)
    return [VentaResponse.model_validate(venta) for venta in ventas]


@router.get("/{venta_id}/with-auto", response_model=VentaResponseWithAuto, summary="Obtener venta con información del auto")
def get_venta_with_auto(
    venta_id: int,
    venta_repo: VentaRepository = Depends(get_venta_repository),
    auto_repo: AutoRepository = Depends(get_auto_repository)
) -> VentaResponseWithAuto:
    venta = venta_repo.get_by_id(venta_id)
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Venta con ID {venta_id} no encontrada"
        )
    
    auto = auto_repo.get_by_id(venta.auto_id)
    
    venta_response = VentaResponse.model_validate(venta)
    auto_response = AutoResponse.model_validate(auto) if auto else None
    
    return VentaResponseWithAuto(
        **venta_response.model_dump(),
        auto=auto_response
    )

