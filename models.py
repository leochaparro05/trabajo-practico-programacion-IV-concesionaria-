from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator, ConfigDict

class AutoBase(SQLModel):
    marca: str = Field(..., description="Marca del vehículo")
    modelo: str = Field(..., description="Modelo específico del vehículo")
    año: int = Field(..., description="Año de fabricación")
    numero_chasis: str = Field(..., unique=True, index=True, description="Número único de chasis")

    @field_validator("año")
    @classmethod
    def validate_año(cls, v: int) -> int:
        año_actual = datetime.now().year
        if v < 1900 or v > año_actual:
            raise ValueError(f"El año debe estar entre 1900 y {año_actual}")
        return v

    @field_validator("numero_chasis")
    @classmethod
    def validate_numero_chasis(cls, v: str) -> str:
        if not v.replace(" ", "").replace("-", "").isalnum():
            raise ValueError("El número de chasis debe ser alfanumérico")
        return v.upper()


class VentaBase(SQLModel):
    nombre_comprador: str = Field(..., description="Nombre completo del comprador")
    precio: float = Field(..., description="Precio de venta del vehículo")
    fecha_venta: datetime = Field(default_factory=datetime.now, description="Fecha y hora de la venta")

    @field_validator("precio")
    @classmethod
    def validate_precio(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        return v

    @field_validator("nombre_comprador")
    @classmethod
    def validate_nombre_comprador(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El nombre del comprador no puede estar vacío")
        return v.strip()

    @field_validator("fecha_venta")
    @classmethod
    def validate_fecha_venta(cls, v: datetime) -> datetime:
        if v > datetime.now():
            raise ValueError("La fecha de venta no puede ser futura")
        return v


class Auto(AutoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ventas: List["Venta"] = Relationship(back_populates="auto")


class Venta(VentaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    auto_id: int = Field(foreign_key="auto.id", description="ID del auto vendido")
    auto: Optional[Auto] = Relationship(back_populates="ventas")


class AutoCreate(AutoBase):
    pass


class VentaCreate(VentaBase):
    auto_id: int = Field(..., description="ID del auto vendido")


class AutoUpdate(SQLModel):
    marca: Optional[str] = None
    modelo: Optional[str] = None
    año: Optional[int] = None
    numero_chasis: Optional[str] = None

    @field_validator("año")
    @classmethod
    def validate_año(cls, v: Optional[int]) -> Optional[int]:
        if v is not None:
            año_actual = datetime.now().year
            if v < 1900 or v > año_actual:
                raise ValueError(f"El año debe estar entre 1900 y {año_actual}")
        return v

    @field_validator("numero_chasis")
    @classmethod
    def validate_numero_chasis(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.replace(" ", "").replace("-", "").isalnum():
                raise ValueError("El número de chasis debe ser alfanumérico")
            return v.upper()
        return v


class VentaUpdate(SQLModel):
    nombre_comprador: Optional[str] = None
    precio: Optional[float] = None
    fecha_venta: Optional[datetime] = None
    auto_id: Optional[int] = None

    @field_validator("precio")
    @classmethod
    def validate_precio(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        return v

    @field_validator("nombre_comprador")
    @classmethod
    def validate_nombre_comprador(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError("El nombre del comprador no puede estar vacío")
            return v.strip()
        return v

    @field_validator("fecha_venta")
    @classmethod
    def validate_fecha_venta(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is not None and v > datetime.now():
            raise ValueError("La fecha de venta no puede ser futura")
        return v


class AutoResponse(AutoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class VentaResponse(VentaBase):
    id: int
    auto_id: int
    model_config = ConfigDict(from_attributes=True)


class VentaResponseSimple(SQLModel):
    id: int
    nombre_comprador: str
    precio: float
    fecha_venta: datetime
    model_config = ConfigDict(from_attributes=True)


class AutoResponseWithVentas(AutoResponse):
    ventas: List[VentaResponseSimple] = []


class VentaResponseWithAuto(VentaResponse):
    auto: Optional[AutoResponse] = None

