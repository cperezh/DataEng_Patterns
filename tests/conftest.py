import pytest
from db.connection import ConexionBD

@pytest.fixture()
def borrar_movimientos_staging():

    conn = ConexionBD.obtener_conexion()

    if conn: 
        conn.execute("TRUNCATE TABLE bancapp.movimientos_staging")
        conn.commit()