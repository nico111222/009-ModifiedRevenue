from fastapi import FastAPI
from bd.conn import engine, Base
from routes.Revenue_routes import router as Revenue_routes


app = FastAPI()
Base.metadata.create_all(bind=engine)
# Incluir los routers en la aplicación
app.include_router(Revenue_routes)


#levantar server uvicorn main:app --reload
#http://127.0.0.1:8000/docs#/
