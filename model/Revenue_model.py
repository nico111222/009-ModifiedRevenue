from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, UniqueConstraint, event
from bd.conn import Base
from datetime import datetime

class Depart_ModifiedRevenue(Base):
    __tablename__ = "Depart_ModifiedRevenue"

    IDRevenue = Column(Integer, primary_key=True, autoincrement=True)
    Year = Column(Integer, nullable=False)
    Month = Column(Integer, nullable=False)  # En SQL es TINYINT, Integer funciona bien
    Units = Column(Integer, nullable=False)
    Revenue = Column(DECIMAL(18, 2), nullable=False)
    Fob_per_unit = Column(DECIMAL(18, 2), nullable=False)
    Comment = Column(String(255))
    Goal = Column(DECIMAL(18, 2))
    Customer = Column(String(255))
    StatusRevenue = Column(Integer, default=1)
    CreateDate = Column(DateTime)
    LastUpdate = Column(DateTime)

    # --- Restricción única Year + Month ---
    __table_args__ = (
        UniqueConstraint('Year', 'Month', name='UQ_Year_Month'),
    )


class Depart_ModifiedRevenue_Log(Base):
    __tablename__ = "Depart_ModifiedRevenue_Log"

    IDLog = Column(Integer, primary_key=True, autoincrement=True)
    IDRevenue = Column(Integer, nullable=False)
    Year = Column(Integer, nullable=False)
    Month = Column(Integer, nullable=False)
    Units = Column(Integer, nullable=False)
    Revenue = Column(DECIMAL(18, 2), nullable=False)
    Fob_per_unit = Column(DECIMAL(18, 2), nullable=False)
    Comment = Column(String(255))
    Goal = Column(DECIMAL(18, 2))
    Customer = Column(String(255))
    StatusRevenue = Column(Integer, default=1)
    CreateDate = Column(DateTime)
    LastUpdate = Column(DateTime)
    ActionType = Column(String(10), nullable=False)
    LogDate = Column(DateTime, default=datetime.now)