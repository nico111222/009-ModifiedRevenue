from bd.conn import engine

def test_connection():
    try:
        # Abre conexión y ejecuta una consulta simple
        with engine.connect() as connection:
            result = connection.execute("SELECT DB_NAME() AS DatabaseName;")
            db_name = result.scalar()
            print(f"✅ Conexión exitosa a la base de datos: {db_name}")
    except Exception as e:
        print("❌ Error al conectar a la base de datos:")
        print(e)

if __name__ == "__main__":
    test_connection()
