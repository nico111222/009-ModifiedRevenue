from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus

# Cadena de conexión ODBC
SupplyNew = "Driver=SQL Server;Server=localhost\\SQLEXPRESS;Database=SUPPLYPLANNING_NEW;UID=sa;PWD=Pass1234;"

# Codificar la cadena para SQLAlchemy
DATABASE_URL = "mssql+pyodbc:///?odbc_connect=" + quote_plus(SupplyNew)

# Crear el motor y la sesión
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

