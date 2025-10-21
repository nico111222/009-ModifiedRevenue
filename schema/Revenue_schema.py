from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ============================================================
# 📘  SCHEMA PRINCIPAL: Depart_ModifiedRevenue
# ============================================================

class RevenueBase(BaseModel):
    Year: int
    Month: int
    Units: int
    Revenue: float
    Fob_per_unit: float
    Comment: Optional[str] = None
    Goal: Optional[float] = None
    Customer: Optional[str] = None
    StatusRevenue: Optional[int] = 1


class RevenueCreate(RevenueBase):
    """Schema para crear nuevos registros"""
    pass


class RevenueUpdate(BaseModel):
    """Schema para actualizar registros"""
    Year: Optional[int] = None
    Month: Optional[int] = None
    Units: Optional[int] = None
    Revenue: Optional[float] = None
    Fob_per_unit: Optional[float] = None
    Comment: Optional[str] = None
    Goal: Optional[float] = None
    Customer: Optional[str] = None
    StatusRevenue: Optional[int] = None
    LastUpdate: Optional[datetime] = None


class Revenue(RevenueBase):
    """Schema para devolver datos al cliente"""
    IDRevenue: int
    CreateDate: Optional[datetime] = None
    LastUpdate: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================
# 📙  SCHEMA DEL LOG: Depart_ModifiedRevenue_Log
# ============================================================

class RevenueLogBase(BaseModel):
    IDRevenue: int
    Year: int
    Month: int
    Units: int
    Revenue: float
    Fob_per_unit: float
    Comment: Optional[str] = None
    Goal: Optional[float] = None
    Customer: Optional[str] = None
    StatusRevenue: int
    CreateDate: Optional[datetime] = None
    LastUpdate: Optional[datetime] = None
    ActionType: str
    LogDate: Optional[datetime] = None


class RevenueLogCreate(RevenueLogBase):
    """Schema para crear registros manuales en el log (si se requiere)"""
    pass


class RevenueLog(RevenueLogBase):
    """Schema para devolver registros del log"""
    IDLog: int

    class Config:
        from_attributes = True
