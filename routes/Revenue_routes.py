from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from bd.conn import get_db
from model.Revenue_model import Depart_ModifiedRevenue, Depart_ModifiedRevenue_Log
from schema.Revenue_schema import Revenue, RevenueCreate, RevenueUpdate, RevenueLog
from datetime import datetime

router = APIRouter(tags=["Revenue"])

# ============================================================
# 🔹 Obtener todos los registros
# ============================================================
@router.get("/get_revenue", response_model=list[Revenue])
def get_revenue(db: Session = Depends(get_db)):
    data = db.query(Depart_ModifiedRevenue).all()
    if not data:
        raise HTTPException(status_code=404, detail="No records found")
    return data


# ============================================================
# 🔹 Obtener un registro por ID
# ============================================================
@router.get("/get_revenue/{id}", response_model=Revenue)
def get_revenue_by_id(id: int, db: Session = Depends(get_db)):
    data = db.query(Depart_ModifiedRevenue).filter(Depart_ModifiedRevenue.IDRevenue == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Record not found")
    return data


# ============================================================
# 🔹 Crear nuevo registro
# ============================================================
@router.post("/create_revenue", response_model=Revenue)
def create_revenue(rev: RevenueCreate, db: Session = Depends(get_db)):
    # Validar duplicado Year+Month
    exists = db.query(Depart_ModifiedRevenue).filter(
        Depart_ModifiedRevenue.Year == rev.Year,
        Depart_ModifiedRevenue.Month == rev.Month
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail=f"Ya existe un registro para Year={rev.Year} y Month={rev.Month}")

    # Crear registro principal
    new_rev = Depart_ModifiedRevenue(
        Year=rev.Year,
        Month=rev.Month,
        Units=rev.Units,
        Revenue=rev.Revenue,
        Fob_per_unit=rev.Fob_per_unit,
        Comment=rev.Comment,
        Goal=rev.Goal,
        StatusRevenue=rev.StatusRevenue,
        CreateDate=datetime.now(),
        LastUpdate=datetime.now()
    )

    try:
        db.add(new_rev)
        db.commit()
        db.refresh(new_rev)

        # Guardar log tipo INSERT
        log = Depart_ModifiedRevenue_Log(
            IDRevenue=new_rev.IDRevenue,
            Year=new_rev.Year,
            Month=new_rev.Month,
            Units=new_rev.Units,
            Revenue=new_rev.Revenue,
            Fob_per_unit=new_rev.Fob_per_unit,
            Comment=new_rev.Comment,
            Goal=new_rev.Goal,
            StatusRevenue=new_rev.StatusRevenue,
            CreateDate=new_rev.CreateDate,
            LastUpdate=new_rev.LastUpdate,
            ActionType="INSERT",
            LogDate=datetime.now()
        )
        db.add(log)
        db.commit()

        return new_rev

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error de integridad (posible duplicado Year+Month).")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# 🔹 Actualizar registro existente
# ============================================================
@router.put("/update_revenue/{id}", response_model=Revenue)
def update_revenue(id: int, rev: RevenueUpdate, db: Session = Depends(get_db)):
    db_rev = db.query(Depart_ModifiedRevenue).filter(Depart_ModifiedRevenue.IDRevenue == id).first()
    if not db_rev:
        raise HTTPException(status_code=404, detail="Record not found")

    # Validar duplicado Year+Month (si cambia)
    new_year = rev.Year if rev.Year is not None else db_rev.Year
    new_month = rev.Month if rev.Month is not None else db_rev.Month
    if (new_year != db_rev.Year or new_month != db_rev.Month):
        other = db.query(Depart_ModifiedRevenue).filter(
            Depart_ModifiedRevenue.Year == new_year,
            Depart_ModifiedRevenue.Month == new_month,
            Depart_ModifiedRevenue.IDRevenue != id
        ).first()
        if other:
            raise HTTPException(status_code=400, detail=f"Ya existe otro registro para Year={new_year} y Month={new_month}")

    # Actualizar campos
    for key, value in rev.model_dump(exclude_unset=True).items():
        setattr(db_rev, key, value)
    db_rev.LastUpdate = datetime.now()

    try:
        db.commit()
        db.refresh(db_rev)

        # Guardar log tipo UPDATE
        log = Depart_ModifiedRevenue_Log(
            IDRevenue=db_rev.IDRevenue,
            Year=db_rev.Year,
            Month=db_rev.Month,
            Units=db_rev.Units,
            Revenue=db_rev.Revenue,
            Fob_per_unit=db_rev.Fob_per_unit,
            Comment=db_rev.Comment,
            Goal=db_rev.Goal,
            StatusRevenue=db_rev.StatusRevenue,
            CreateDate=db_rev.CreateDate,
            LastUpdate=db_rev.LastUpdate,
            ActionType="UPDATE",
            LogDate=datetime.now()
        )
        db.add(log)
        db.commit()

        return db_rev

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error de integridad al actualizar.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# 🔹 Eliminar registro (cambia estado a 0 y guarda log)
# ============================================================
@router.delete("/delete_revenue/{id}", response_model=Revenue)
def delete_revenue(id: int, db: Session = Depends(get_db)):
    db_rev = db.query(Depart_ModifiedRevenue).filter(Depart_ModifiedRevenue.IDRevenue == id).first()
    if not db_rev:
        raise HTTPException(status_code=404, detail="Record not found")

    db_rev.StatusRevenue = 0
    db_rev.LastUpdate = datetime.now()

    try:
        db.commit()
        db.refresh(db_rev)

        # Guardar log tipo DELETE
        log = Depart_ModifiedRevenue_Log(
            IDRevenue=db_rev.IDRevenue,
            Year=db_rev.Year,
            Month=db_rev.Month,
            Units=db_rev.Units,
            Revenue=db_rev.Revenue,
            Fob_per_unit=db_rev.Fob_per_unit,
            Comment=db_rev.Comment,
            Goal=db_rev.Goal,
            StatusRevenue=0,
            CreateDate=db_rev.CreateDate,
            LastUpdate=db_rev.LastUpdate,
            ActionType="DELETE",
            LogDate=datetime.now()
        )
        db.add(log)
        db.commit()

        return db_rev

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# 🔹 Obtener registros del log
# ============================================================
@router.get("/get_revenue_log", response_model=list[RevenueLog])
def get_revenue_log(db: Session = Depends(get_db)):
    data = db.query(Depart_ModifiedRevenue_Log).order_by(Depart_ModifiedRevenue_Log.LogDate.desc()).all()
    if not data:
        raise HTTPException(status_code=404, detail="No log records found")
    return data
